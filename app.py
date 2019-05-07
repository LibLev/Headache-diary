from flask import Flask, render_template, redirect, session, request
from database import queries

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('login.html')


if __name__ == '__main__':
    app.run()
