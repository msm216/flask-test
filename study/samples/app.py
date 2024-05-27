import os

from flask import Flask
from flask import request
from flask import render_template, jsonify, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<page>')
def page(page):
    return render_template(f'{page}.html')


if __name__ == '__main__':

    app.run(debug=True)