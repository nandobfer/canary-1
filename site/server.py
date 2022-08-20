from datetime import datetime, timedelta, date
from flask import Flask, request, url_for, redirect, render_template, request
import subprocess
import sys
import mysql.connector

TIMELIMIT = 15

# MYSQL DATABASE
database_auth = {
    'host': '127.0.0.1',
    'database': 'canary',
    'user': 'root',
    'password': 'mfux6xpj'
}


class Mysql():
    # def __init__(self) -> None:
    #     pass

    def connect(self, auth):
        ''' Try to connect to a database with auth params defined in config file '''
        try:
            self.connection = mysql.connector.connect(host=auth['host'],
                                                      database=auth['database'],
                                                      user=auth['user'],
                                                      password=auth['password'])
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = self.connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                # cursor.close()
                self.auth = auth

                return self.connection

        except Exception as e:
            print(e)

    def disconnect(self):
        ''' Disconnect from database '''
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

    def fetchTable(self, rows, table, condition=None, value=None, reversed=None, ordered=None):
        ''' Fetch a number of rows from a table that exists in database.
        Number of rows and table defined in config file.
        if number of rows equals to 0, will try to fetch all rows.'''

        if condition:
            sql = f'SELECT * FROM `{table}` WHERE {condition} = "{value}"'
            if reversed:
                sql = f'SELECT * FROM `{table}` WHERE {condition} = "{value}" ORDER BY {reversed} DESC'
        else:
            sql = f"SELECT * FROM `{table}` WHERE 1"

        if ordered:
            sql = f'{sql} ORDER BY {ordered} ASC'

        cursor = self.connection.cursor(buffered=True)
        cursor.execute(sql)
        if rows > 1:
            records = cursor.fetchmany(rows)
        else:
            records = cursor.fetchall()

        # print(f'Total number of rows in table: {cursor.rowcount}')
        # print(f'Rows fetched: {len(records)}')

        data = []
        for row in records:
            row = list(row)
            data.append(row)

        cursor.close()
        return data

    def newAccount(self, data):
        ''' Função utilizada para inserir novo membro no banco de dados.
        DATA requer (ID, USUÁRIO, SENHA, NOME, ENDEREÇO, TIPO DE MEMBRO) '''

        try:
            sql = f"INSERT INTO accounts (id, name, password, email, premdays, lastday, type, coins, creation, recruiter) VALUES ({data['id']}, 'none', '{data['password']}', '{data['email']}', '0', '0', '1', '0', '0', '0')"
            cursor = self.connection.cursor()
            cursor.execute(sql)
        except:
            sql = f'INSERT INTO accounts (id, name, password, email, premdays, lastday, type, coins, creation, recruiter) VALUES ({data["id"]}, "none", "{data["password"]}", "{data["email"]}", "0", "0", "1", "0", "0", "0")'
            cursor = self.connection.cursor()
            cursor.execute(sql)

        self.connection.commit()
        cursor.close()

    def newCharacter(self, data):
        ''' Função utilizada para inserir novo membro no banco de dados.
        DATA requer (ID, USUÁRIO, SENHA, NOME, ENDEREÇO, TIPO DE MEMBRO) '''

        try:
            sql = f"INSERT INTO players (id, name, account_id, vocation, race) VALUES ({data['id']}, '{data['name']}', {data['account_id']}, {data['vocation_id']}, {data['race']})"
            cursor = self.connection.cursor()
            cursor.execute(sql)
        except:
            sql = f'INSERT INTO players (id, name, account_id, vocation, race) VALUES ({data["id"]}, "{data["name"]}", {data["account_id"]}, {data["vocation_id"]}, {data["race"]})'
            cursor = self.connection.cursor()
            cursor.execute(sql)

        self.connection.commit()
        cursor.close()

    def updateTable(self, table, id, column, value, id_column):
        command = f'Update {table} set {column} = "{value}" where {id_column} = {id}'
        cursor = self.connection.cursor()
        cursor.execute(command)
        self.connection.commit()
        # cursor.close()
        print("Record Updated successfully ")


class Connection():
    def __init__(self, ip, id):
        self.ip = ip
        self.id = id
        
        self.buildPlayer()
        self.getCharacters()
        self.expira = datetime.now() + timedelta(minutes=TIMELIMIT)

    def buildPlayer(self):
        data = session.database.fetchTable(1, 'accounts', 'id', self.id)[0]

        self.id = data[0]
        self.name = data[1]
        self.password = data[2]
        self.user = data[3]
        self.member = data[5]
        self.characters = []

    def isExpired(self):
        if not datetime.now() < self.expira:
            return True

    def getCharacters(self):
        try:
            self.characters = []
            characters = session.database.fetchTable(
                0, 'players', 'account_id', self.id)
            for item in characters:
                try:
                    guild_db = session.database.fetchTable(1, 'guild_membership', 'player_id', item[0])[0]
                    guild_id = guild_db[1]
                    guild = session.database.fetchTable(1, 'guilds', 'id', guild_id)[0][1]
                    guild_position_id = guild_db[2]
                    guild_position = session.database.fetchTable(1, 'guild_ranks', 'id', guild_position_id)[0][2]
                except:
                    guild = ''
                    guild_position = ''

                character = {
                    'id': item[0],
                    'name': item[1],
                    'level': item[4],
                    'vocation_id': item[5],
                    'vocation': session.database.fetchTable(1, 'classes', 'id', item[5])[0][1],
                    'magic_level': item[15],
                    'city_id': item[20],
                    'city': session.database.fetchTable(1, 'towns', 'id', item[20])[0][1],
                    'fist': item[48],
                    'club': item[50],
                    'sword': item[52],
                    'axe': item[54],
                    'distance': item[56],
                    'shield': item[58],
                    'fishing': item[60],
                    'critical_chance': item[62],
                    'critical_damage': item[64],
                    'life_leech': item[66],
                    'life_leech_chance': item[68],
                    'mana_leech': item[70],
                    'mana_leech_chance': item[72],
                    'race_id': item[92],
                    'race': session.database.fetchTable(1, 'races', 'id', item[98])[0][1],
                    'guild': guild,
                    'guild_position': guild_position,
                }
                self.characters.append(character)
        except:
            pass


class Session():
    def __init__(self):
        self.connections = []
        self.member_list = []
        self.database = Mysql()
        self.database.connect(database_auth)
        self.getMembers()

    def getMembers(self):
        try:
            if not self.database.connection.is_connected():
                self.reconnectDatabase()
        except:
            pass

        self.member_list = []
        members = self.database.fetchTable(0, 'accounts')

        for member in members:
            data = {
                'id': member[0],
                'name': member[1],
                'password': member[2],
                'user': member[3],
                'member': member[5]
            }
            self.member_list.append(data)

    def reconnectDatabase(self):
        self.database.connect(database_auth)

    def getConnection(self, ip):
        for connection in self.connections:
            if connection.ip == ip:
                if not connection.isExpired():
                    return connection
                else:
                    self.connections.remove(connection)

    def login(self, user, password, ip):
        try:
            data = self.database.fetchTable(1, 'accounts', 'email', user)[0]
            if data:
                if password == data[2]:
                    id = data[0]

                    # check if user is already logged and update it' connection if it exists
                    is_logged = self.getConnection(ip)
                    if is_logged and is_logged.id == id:
                        self.connections.remove(is_logged)

                    connection = Connection(ip, id)
                    self.connections.append(connection)
                    connection.buildPlayer()
                    connection.getCharacters()
                    return connection
        except Exception as error:
            print(error)
            return None

    def signup(self, data):
        try:
            usuario = self.database.fetchTable(
                1, 'accounts', 'email', data['email'])[0]
            if usuario:
                return 'Usuário já cadastrado', False

        except:
            data.update({'id': len(self.member_list)+1})
            self.database.newAccount(data)
            self.member_list.append(data)
            return 'Usuário cadastrado', True


app = Flask(__name__)
session = Session()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
    # redirecting to another endpoint


# @app.route('/home/', methods=['GET'])
# def home():
#     return redirect(url_for(''))


@app.route('/login.php', methods=['GET', 'POST'])
def login_php():
    out = subprocess.run(["php", "login.php"], stdout=subprocess.PIPE)
    return out.stdout


@app.route('/login/', methods=['POST'])
def login():
    ip = request.remote_addr
    email = request.form['email']
    password = request.form['password']
    connection = session.login(email, password, ip)
    if connection:
        data = vars(connection)
        return data
    else:
        return 'None'


@app.route('/signup/', methods=['POST'])
def signup():
    ip = request.remote_addr
    email = request.form['email']
    password = request.form['password']
    response = session.signup({'email': email, 'password': password})
    if response[1]:
        return str(['Sucesso', 'Usuário cadastrado'])
    else:
        return 'None'

@app.route('/get_races/', methods=['POST'])
def get_races():
    races = session.database.fetchTable(0, 'races', 'type', request.form['type'])
    if str(request.form['type']) == '0':
        return str(races)
    else:
        monsters = []
        for race in races:
            char_class = session.database.fetchTable(1, 'classes', 'id', race[4])[0]
            data = {
                'race': race,
                'class': char_class
            }
            monsters.append(data)
        print(monsters)
        return str(monsters)

@app.route('/get_classes/', methods=['GET', 'POST'])
def get_classes():
    classes = session.database.fetchTable(0, 'classes')
    return str(classes)

@app.route('/new_character/', methods=['POST'])
def new_character():
    id = len(session.database.fetchTable(0, 'players')) + 1
    data = {
        'id': id,
        'name': request.form['name'],
        'vocation_id': request.form['vocation_id'],
        'account_id': request.form['account_id'],
        'race_id': request.form['race_id'],
        'type': request.form['type'],
        'sex': request.form['sex'],
        'race': request.form['race_id'],
    }
    print(data)
    try:
        session.database.newCharacter(data)
        connection = session.getConnection(request.remote_addr)
        connection.getCharacters()
        return str(connection.characters[len(connection.characters)-1])
    except Exception as error:
        print(error)
        return str(None)

    

def run():

    if len(sys.argv) > 1:
        app.run(debug=True, host="0.0.0.0",
                port=sys.argv[1], use_reloader=False)
    else:
        app.run(debug=True, host="0.0.0.0", port="80")


run()
