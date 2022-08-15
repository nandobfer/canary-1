from crypt import methods
from flask import Flask, request, url_for, redirect, render_template, request
import subprocess

app = Flask(__name__)


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


def run(port=80):
    app.run(debug=True, host="0.0.0.0", port=port, use_reloader=False)
