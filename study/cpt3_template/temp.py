import os

from flask import g, Flask, request, session, current_app, make_response, render_template, redirect, abort, url_for



app = Flask(__name__)
# 获取环境变量.env中的密钥，第二个参数为获取失败时采用的默认值
app.secret_key = os.getenv('SECRET_KEY', 'HardToGuessStringAsDefaulKey')
# 设置Flask-WTF密钥，以保护表单免受CSRF攻击
#app.config['SECRET_KEY'] = 'HardToGuessStringAsKey'


# 一些虚拟数据
services = [
    'consulting', 
    'training', 
    'commissioning', 
    'repair', 
    'replacement'
]

user = {
    'username': 'Grey Li',
    'bio': 'A boy who loves movies and music.'
}

movies = [
    {'name': 'My Neighbor Totoro', 'year': '1988'},
    {'name': 'Three Colours Trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'Perfect Blue', 'year': '1997'},
    {'name': 'The Matrix', 'year': '1999'},
    {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket List', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'},
    {'name': 'Gone Girl', 'year': '2014'},
    {'name': 'CoCo', 'year': '2017'},
]

# 如果没指定 methods 参数，默认只把视图函数注册为 GET 请求的处理程序
@app.route('/')
def index():
    return render_template('index.html')

# 如果没指定 methods 参数，默认只把视图函数注册为 GET 请求的处理程序
@app.route('/watchlist')
def watch_list():
    return render_template('watchlist.html', user=user, movies=movies)

######################## 上下文 ########################





######################## 反回先前页面 ########################






######################## URL安全验证 ########################
# http://localhost:5OOO/do-something?next=http://helloflask.com
# referrer或next参数容易被篡改和劫持，形成开放重定向Open Redirect漏洞

from urllib.parse import urlparse, urljoin




######################## AJAX异步请求 ########################
# 处理AJAX请求的视图函数不返回完整的html响应而是局部数据

from jinja2.utils import generate_lorem_ipsum





######################## 运行应用 ########################

if __name__ == '__main__':

    app.run(debug=True)