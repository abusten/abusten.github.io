首先进入题目的是一个登录页面/login![](https://cdn.nlark.com/yuque/0/2025/png/43146588/1747471834575-28539e39-ff27-47dd-a07f-bb8985b77b80.png)

不过这个登录页面对后面的步骤没有任何关系，不存在什么admin账号能有更多权限和功能之类的，我记得我在比赛时是用sql万能密码登录的，不过如果复现时的源码和比赛时一模一样的话，应该输入什么都行

登录后是一个文件上传功能/upload

![](https://cdn.nlark.com/yuque/0/2025/png/43146588/1747472049331-b22405d5-c3b2-4beb-bcb5-c5466298e8ef.png)

这个功能我在比赛时试着传了半天php马，我也不知道当初怎么想的就认定是php了，可能是题目这种过于简洁的前端页面让我下意识的以为这一定是php题，最终当然是没有成功，不过上传过程中发现了一个读任意文件的漏洞

-------------------------------------------------------------------------------------------------------------------

好吧现在我已经确定复现题目和原来比赛环境不一样了

后面的复现不来我就在这里记录一下吧

在./upload/file_path=xxx这个地方有一个任意文件读取的漏洞，不过不知道flag文件的名称是利用不了的，这个时候要先读/proc/self/cmdline查看题目源代码的存储位置（比赛时就是忘了这一点才没打出来），定位到/app/app.py拿到源代码：

```javascript
import uuid
import os
import hashlib
import base64
from flask import Flask, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/')
def index():
    if session.get('username'):
        return redirect(url_for('upload'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin':
            if hashlib.sha256(password.encode()).hexdigest() == '32783cef30bc23d9549623aa48aa8556346d78bd3ca604f277d63d6e573e8ce0':
                session['username'] = username
                return redirect(url_for('index'))
            else:
                flash('Invalid password')
        else:
            session['username'] = username
            return redirect(url_for('index'))
    else:
        return '''
        <h1>Login</h1>
        <h2>No need to register.</h2>
        <form action="/login" method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
            <br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
            <br>
            <input type="submit" value="Login">
        </form>
        '''

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if not session.get('username'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        f = request.files['file']
        file_path = str(uuid.uuid4()) + '_' + f.filename
        f.save('./uploads/' + file_path)
        return redirect(f'/upload?file_path={file_path}')
    
    else:
        if not request.args.get('file_path'):
            return '''
            <h1>Upload Image</h1>
            
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file">
                <input type="submit" value="Upload">
            </form>
            '''
            
        else:
            file_path = './uploads/' + request.args.get('file_path')
            if session.get('username') != 'admin':
                with open(file_path, 'rb') as f:
                    content = f.read()
                    b64 = base64.b64encode(content)
                    return f'<img src="data:image/png;base64,{b64.decode()}" alt="Uploaded Image">'
            else:
                os.system(f'base64 {file_path} > /tmp/{file_path}.b64')
                # with open(f'/tmp/{file_path}.b64', 'r') as f:
                #     return f'<img src="data:image/png;base64,{f.read()}" alt="Uploaded Image">'
                return 'Sorry, but you are not allowed to view this image.'
                
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

看到源代码就知道需要获得admin权限才能接着往下做，根据`app.secret_key = os.getenv('SECRET_KEY')`可以先读/proc/self/environ拿到secret_key然后本地运行一下拿到admin的session,改包就能获取admin的权限

另一种方式是利用`32783cef30bc23d9549623aa48aa8556346d78bd3ca604f277d63d6e573e8ce0`硬编码直接在md5解密网站里查，得到密码backdoor，在/login用admin和backdoor进入同样可以获得admin权限

之后的rce就是利用`os.system(f'base64 {file_path} > /tmp/{file_path}.b64')`，通过构造文件名来进行命令注入，比如上传一个文件名为a || cat /Fl4g_is_H3r3 > test.txt;的文件就能让系统执行`os.system(f'base64 ./uploads/a || cat /Fl4g_is_H3r3 > test.txt; > /tmp/./uploads/a || cat /Fl4g_is_H3r3 > test.txt;.b64')`来将cat /Fl4g_is_H3r3写入test.txt，然后访问/upload?file_path=../../../app/test.txt获得flag，或者直接注入/upload?file_path=../$(cat+/Fl4g_is_H3r3>/tmp/111.txt)，由于shell中$(command)是命令替换，先执行括号里的内容，之后与上一种方法同理；还有一种方法是注入/upload?file_path=somefile.txt;cat /Fl4g_is_H3r3 > /tmp/pwned;进行命令拼接，之后与上面类似。

记录这道题的原因也是希望多学习一些在知道文件读取漏洞情况下RCE的方法，之后也是要系统学习一下linux基础和shell基础了

