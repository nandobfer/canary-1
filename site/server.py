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

    def updateTable(self, table, id, column, value, id_column):
        command = f'Update {table} set {column} = "{value}" where {id_column} = {id}'
        cursor = self.connection.cursor()
        cursor.execute(command)
        self.connection.commit()
        # cursor.close()
        print("Record Updated successfully ")


class Connection():
    def __init__(self, ip, data, database):
        self.ip = ip
        self.id = data[0]
        self.name = data[1]
        self.password = data[2]
        self.user = data[3]
        self.member = data[5]
        self.characters = []

        self.getCharacters()
        self.expira = datetime.now() + timedelta(minutes=TIMELIMIT)

    def isExpired(self):
        if not datetime.now() < self.expira:
            return True

    def getCharacters(self):
        try:
            characters = session.database.fetchTable(
                0, 'players', 'account_id', self.id)
            for item in characters:
                character = {
                    'id': item[0],
                    'name': item[1],
                    'level': item[4],
                    'vocation': item[5],
                    'magic_level': item[15],
                    'city': item[20],
                    'fist': item[47],
                    'club': item[49],
                    'sword': item[51],
                    'axe': item[53],
                    'distance': item[55],
                    'shield': item[57],
                    'fishing': item[59],
                    'critical_chance': item[61],
                    'critical_damage': item[63],
                    'life_leech': item[65],
                    'life_leech_chance': item[67],
                    'mana_leech': item[69],
                    'mana_leech_chance': item[71],
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

                    connection = Connection(ip, data, self.database)
                    self.connections.append(connection)
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


def run():

    if len(sys.argv) > 1:
        app.run(debug=True, host="0.0.0.0",
                port=sys.argv[1], use_reloader=False)
    else:
        app.run(debug=True, host="0.0.0.0", port="80")


run()
