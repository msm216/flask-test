import os

from flask import g, Flask, request, session, current_app, make_response, render_template, redirect, abort, url_for



app = Flask(__name__)
# 获取环境变量.env中的密钥，第二个参数为获取失败时采用的默认值
app.secret_key = os.getenv('SECRET_KEY', 'HardToGuessStringAsDefaulKey')
# 设置Flask-WTF密钥，以保护表单免受CSRF攻击
#app.config['SECRET_KEY'] = 'HardToGuessStringAsKey'



# 如果没指定 methods 参数，默认只把视图函数注册为 GET 请求的处理程序
@app.route('/')
@app.route('/hello')
def index():
    # 获取查询参数中name的值
    # Flask在每个请求产生后自动激活当前请求线程内的上下文
    # 激活上下文后请求被临时设为全局可访问，请求结束后Flask销毁对应上下文
    name = request.args.get('name')
    # 如果请求的查询参数中没有name的值则尝试从cookie中获取
    if name is None:
        name = request.cookies.get('name', 'Nobody')
    # 判断session中'logged_in'的值是否为真
    if 'logged_in' in session:
        authenticated = True
    else:
        authenticated = False
    return f'<h1>Hello, {name}</h1><p>Authentication: {authenticated}</p>'

######################## 上下文和Cookie ########################

# 设置名为name的cookie
@app.route('/set/<name>')
def set(name):
    # 一个重定向的响应
    resp = make_response(redirect(url_for('hello')))
    resp.set_cookie('name', name)
    return resp

# http://127.0.0.1:5000/login
@app.route('/login')
def login():
    # 在登陆时向session对象 的cookie中添加logged-in的值以表示用户已认证
    # session 对象的cookie的内容都被自动加密
    session['logged_in'] = True
    return redirect(url_for('hello'))

# http://127.0.0.1:5000/logout
@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))

# http://127.0.0.1:5000/admin
@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return redirect(url_for('hello'))

# 一个在每个请求处理前执行的钩子Hook函数
@app.before_request
def get_name():
    # g 用于存储当前程序上下文的全局数据
    # g 随着每一个请求激活和销毁，每次都被重设
    # 结合钩子函数来保存每个请求处理前所需要的全局变量
    g.name = request.args.get('name')


######################## 反回先前页面 ########################

# 两个不同的页面Foo和Bar都有指向另一个视图do_something的链接
# 需要在执行完do_something之后重定向回上一个页面而不是index

# request.full_path 获取当前页面的完整地址并保存在next参数中

@app.route('/foo')
def foo():
    did = session.get('did')
    return '<h1>Foo page</h1><a href="{0}">Do something</a><p>Did? {1}</p>'\
        .format(url_for('do_something', next=request.full_path), did)

@app.route('/bar')
def bar():
    did = session.get('did')
    return '<h1>Bar page</h1><a href="{0}">Do something</a><p>Did? {1}</p>'\
        .format(url_for('do_something', next=request.full_path), did)

@app.route('/do_something')
def do_something():
    # do somethihng
    if not session['did']:
        session['did'] = True
    else:
        session['did'] = False
    return redirect_back()


######################## URL安全验证 ########################
# http://localhost:5OOO/do-something?next=http://helloflask.com
# referrer或next参数容易被篡改和劫持，形成开放重定向Open Redirect漏洞

from urllib.parse import urlparse, urljoin

# 验证当前目标URL：/foo 或 /bar
def is_safe_url(target):
    # 获取程序内主机URL(http://127.0.0.1:5000/)并用urlparse进行解析
    # urlparse 返回一个 ParseResult 对象
    ref_url = urlparse(request.host_url)
    # urljoin 函数将目标URL转换为绝对URL并用urlparse进行解析
    # joined_url 参数值为 http://127.0.0.1:5000/foo
    joined_url = urljoin(request.host_url, target)
    test_url = urlparse(joined_url)
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc

# 先尝试获取next参数，若为空则尝试获取referer，如果仍为空，则重定向到默认视图
def redirect_back(default='hello', **kwargs):
    # target 参数值为 /foo? 或 /bar?
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        # 创建URL验证函数用来验证next参数值是否属于程序内部URL
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default), **kwargs)


######################## AJAX异步请求 ########################
# 处理AJAX请求的视图函数不返回完整的html响应而是局部数据

from jinja2.utils import generate_lorem_ipsum

# 点击Load More按钮时，发送AJAX请求获取1段随机字符串并直接动态地插入文章下方
@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    return render_template('post.html', body=post_body)

@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)



######################## 运行应用 ########################

if __name__ == '__main__':

    app.run(debug=True)