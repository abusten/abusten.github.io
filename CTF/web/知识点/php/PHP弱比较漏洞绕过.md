_原理：PHP是弱类型语言，不需要明确的定义变量的类型，变量的类型根据使用时的上下文所决定，也就是变量会根据不同表达式所需要的类型自动转换，比如求和，PHP会将两个相加的值转为long、double再进行加和。每种类型转为另外一种类型都有固定的规则，当某个操作发现类型不符时就会按照这个规则进行转换，这个规则正是弱类型实现的基础。_

**一.字符数字绕过**

例题：

```plain
<?php
if(is_numeric($_GET['1']) && $_GET['1']=="255"){
    if(strstr($_GET['1'],"255")==False){
            $flag;
    }
}
show_source(__FILE__);
```

	题目要求1的值为数字且等于255，是1中不能存在255这个字符串。

解决方式：用八进制或十六进制，这里用?1=0xff

另外还有一个技巧：<font style="color:rgb(77, 77, 77);">字符串以数字开头时，以开头数字（到字母出现截止）作为转换结果；开头不是数字的字符串或空（null），则转换为0。</font>

```plain
'12'==12    //true
'12abc'==12 //true
'adm2n'==0  //true
```

**二.sha1绕过**

例题：

```plain
<?php
error_reporting(0);
if (isset($_GET['name']) and isset($_GET['password'])) {
    sha1($_GET['name']) . "</br>";
    sha1($_GET['password']) . "</br>";

    if ($_GET['name'] == $_GET['password'])
        '<p>Your password can not be your name!</p>';

    else if (sha1($_GET['name']) == sha1($_GET['password']))
         $flag;
}
highlight_file(__FILE__);
?>
```

需要满足name和password的值不同但是sha1值相同

解决方法：数组绕过，?name[]=1&&password[]=2

解法2：弱比较可以用0e绕过

sha1

```plain
10932435112: 0e07766915004133176347055865026311692244
aaroZmOk: 0e66507019969427134894567494305185566735
aaK1STfY: 0e76658526655756207688271159624026011393
aaO8zKZF: 0e89257456677279068558073954252716165668
aa3OFF9m: 0e36977786278517984959260394024281014729
0e1290633704: 0e19985187802402577070739524195726831799
```

**三.md5**

与sha1相似

0e绕过：

```plain
240610708:0e462097431906509019562988736854
QLTHNDT:0e405967825401955372549139051580
QNKCDZO:0e830400451993494058024219903391
PJNPDWY:0e291529052894702774557631701704
NWWKITQ:0e763082070976038347657360817689
NOOPCJF:0e818888003657176127862245791911
MMHUWUV:0e701732711630150438129209816536
MAUXXQC:0e478478466848439040434801845361
```

**四.session**

**session:**

例题：

```plain
 <?php
session_start();
if (isset ($_POST['pwd'])){
        if ($_POST['pwd'] == $_SESSION['pwd'])
                die('Flag:'.$flag);
        else{
                print '<p>不对哦，再猜.</p>';
                $_SESSION['pwd']=time().time();
        }
}else{
    $_SESSION['pwd']=time().time();
}
?>
```

> _**SESSION是什么：**_
>
> _Session是服务器为了记录用户状态而创建的一个特殊的对象。不同的是Cookie保存在客户端浏览器中，而Session保存在服务器上。_
>
> _客户端浏览器访问服务器的时候，服务器把客户端信息以某种形式记录在服务器上，这就是Session。客户端浏览器再次访问时，只需要从该Session中查找该客户的状态就可以了。_
>
> _当多个客户端执行程序时，服务器会保存多个客户端的Session。_
>
> _获取Session的时候也不需要声明获取谁的Session。_
>
> _Session机制决定了当前客户只会获取到自己的Session，而不会获取到别人的Session。各客户的Session也彼此独立，互不可见。_
>
> _**Session的作用**_
>
> _1、当浏览器第一次访问服务器时，服务器创建一个session对象（该对象有一个唯一的id，一般称之为sessionId）。_
>
> _2、服务器会将sessionId以cookie的方式发送给浏览器。_
>
> _3、当浏览器再次访问服务器时，会将sessionId发送给服务器。_
>
> _4、服务器依据sessionId就可以找到对应的session对象。_
>
> _**Session的内部细节**_
>
> _Session对应的类为javax.servlet.http.HttpSession类。_
>
> __
>
> _每个来访者对应一个Session对象，所有该客户的状态信息都保存在这个Session对象里。_
>
> _Session对象是在客户端第一次请求服务器的时候创建的，Session也是一种key-value的属性对。_
>
> _通过getAttribute(Stringkey)和setAttribute(String key,Objectvalue)方法读写客户状态信息。_
>
> _Servlet里通过request.getSession()方法获取该客户的Session。_
>
> _request还可以使用getSession(boolean create)来获取Session。区别是如果该客户的Session不存在，request.getSession()方法会返回null，而getSession(true)会先创建Session再将Session返回。_
>
> _Servlet中必须使用request来编程式获取HttpSession对象，而JSP中内置了Session隐藏对象，可以直接使用。_
>

解决方法：用burpsuit将phpsession改为空

**五.strcmp**

例题：

```plain
<?php
error_reporting(0);
$password="***************";
if(isset($_POST['password'])) {
    if (strcmp($_POST['password'], $password) == 0) {
        $flag;
    } else {
        "Wrong password..";
    }
}
highlight_file(__FILE__);
?>
```

	_strcmp_函数是string compare(字符串比较)的缩写，用于比较两个字符串并根据比较结果返回整数。基本形式为_strcmp_(str1,str2)，若str1=str2，则返回零；若str1>str2，则返回正数。

根据代码逻辑，需要比较$_POST[‘password’]和$password的值，而$password的值无从得知。但由于php代码在比较时使用了弱比较，并且strcmp传入的期望类型是字符串类型的数据，但是如果传入非字符串类型的数据的时候，这个函数将发生错误但却判定其相等

解题方法：POST:password[]=1



