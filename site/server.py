from crypt import methods
from flask import Flask, request, url_for, redirect, render_template, request
import subprocess

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    # redirecting to another endpoint
    return redirect(url_for('home'))

@app.route('/home/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/login.php', methods=['GET', 'POST'])
def login_php():
    out = subprocess.run(["php", "login.php"], stdout=subprocess.PIPE)
    return out.stdout

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="80")