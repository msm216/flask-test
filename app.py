import os

from datetime import datetime, timezone

from flask import g, Flask, request, session, current_app, make_response, render_template, redirect, abort, url_for, flash
#from flask_script import Manager, Shell
#from flask_migrate import Migrate, MigrateCommand
from flask_bootstrap import Bootstrap
from flask_moment import Moment
# Flask-WTF 是一个构建在 WTForms 之上的 Flask 扩展，专门为在 Flask 中更方便地使用 WTForms 提供支持
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy

# WTForms 是一个独立的表单处理库，它用于创建和验证Web表单
from wtforms import StringField, SubmitField
#from wtforms.validators import Required
from wtforms.validators import DataRequired, Length






basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# 获取环境变量.env中的密钥，第二个参数为获取失败时采用的默认值
app.secret_key = os.getenv('SECRET_KEY', 'HardToGuessStringAsDefaulKey')
# 设置Flask-WTF密钥，以保护表单免受CSRF攻击
#app.config['SECRET_KEY'] = 'HardToGuessStringAsKey'


###########################################################################################################

# 定义本地数据库的URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# 该设置使得每次请求结束后都自动提交数据库的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 初始化数据库
db = SQLAlchemy(app)
# 数据库迁移框架用于跟踪数据库模式变化
#migrate = Migrate(app, db)

###########################################################################################################


bootstrap = Bootstrap(app)


# 一些自定义变量
services = [
    'consulting', 
    'training', 
    'commissioning', 
    'repair', 
    'replacement'
]

comments = {
        "Micheal":"Ok", 
        "David":"Good", 
        "Alex": "Bad"
    }

######## 类 ########

# 继承定义个表单类
class NameForm(FlaskForm):
    # 名为name的文本字段， StringField 类表示属性为type="text" 的 <input> 元素
    # 可选参数 validators 指定一个由验证函数组成的列表，在接受用户提交的数据之前验证数据
    # 验证函数 DataRequired() 确保提交的字段不为空
    name = StringField('Name?', validators=[DataRequired()])
    # 名为submit的提交按钮，SubmitField 类表示属性为type="submit" 的 <input> 元素
    submit = SubmitField('Submit')

# 定义一个角色模型类
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # 角色到用户为一对多关系，该属性代表关系的面向对象视角
    # 一个Role类实例的users属性返回与该实例相关联的User模型中的记录作为list
    # backref参数向User模型中添加一个role属性
    users = db.relationship('User', backref='role', lazy='dynamic')
    # 用于返回具有可读性的字符串模型
    def __repr__(self):
        return '<Role %r>' % self.name

# 定义一个用户模型类
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    regist = db.Column(db.Boolean, default=False)
    comment = db.Column(db.String(432))    # 最长为144汉字
    # 通过外键与角色建立关系
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # 用于返回具有可读性的字符串模型
    def __repr__(self):
        return '<User %r>' % self.username


######## 视图函数 ########

# 设置名为name的cookie
@app.route('/set/<name>')
def set(name):
    # 一个重定向的响应
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('name', name)
    return resp

# http://127.0.0.1:5000/login
@app.route('/login')
def login():
    # 在登陆时向session对象 的cookie中添加logged-in的值以表示用户已认证
    # session 对象的cookie的内容都被自动加密
    session['logged_in'] = True
    return redirect(url_for('index'))

# http://127.0.0.1:5000/logout
@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('index'))

# http://127.0.0.1:5000/admin
@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return redirect(url_for('index'))

# 如果没指定 methods 参数，默认只把视图函数注册为 GET 请求的处理程序
@app.route('/', methods=['GET', 'POST'])
def index():
    name_form = NameForm()
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
    '''
    # 如果数据能被验证函数接受则开始执行
    if form.validate_on_submit():
        # 验证表单输入内容是否变化
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        # 过滤器查询在数据库中有记录的名字
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        # 使用session字典存储输入的表单信息，保存在客户端中
        session['name'] = form.name.data
        form.name.data = ''
        # 重定向作为POST请求的响应；生成的URL在修改路由名字后依然可用，参数为视图函数名
        return redirect(url_for('index'))  
    '''
    return render_template(
        'index.html', 
        form=name_form, 
        name=name, 
        status=session.get('logged_in'),
        auth=authenticated,
        comments=comments, 
        current_time=datetime.now(timezone.utc), 
        user_agent=request.headers.get('User-Agent')
    )

# 列表内任意元素作为URL变量 http://127.0.0.1:5000/services/commissioning
@app.route('/services/<any(%s):service>' % str(services)[1:-1])
def theree_colors(service):
    return '<p> %s </p>' % service




######## 钩子函数 ########

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

# 一个在每个请求处理后执行的钩子Hook函数
@app.teardown_appcontext
def teardown_db(exception):
    # 例如：销毁数据库连接
    db.close()



if __name__ == '__main__':

    print('sqlite:///' + os.path.join(basedir, 'data.sqlite'))

    app.run(debug=True)
    #manager.run()