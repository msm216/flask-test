import os

from flask import Flask, render_template, send_from_directory


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<page>')
def page(page):
    return render_template(f'{page}.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)