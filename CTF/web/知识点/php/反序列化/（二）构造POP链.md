**一、背景知识**

1.类的序列化与反序列化

类是一个定义事物的抽象概念，定义了事物的一些抽象的特点，类实例化后就是对象。

而序列化一个类的过程，就是将一个类的内容转化为特殊的字符串，例如：

```php
<?php
   error_reporting(0);
   class student{
       public $name;
       public $age;
       private $grade;
       function setName($name){
           $this->name=$name;
      }
       function setAge($age){
           $this->age=$age;
      }
       function setGrade($grade){
           $this->grade=$grade;
      }
  }
   $emp = new student();
   $emp->setName("Tom");
   $emp->setAge(20);
   $emp->setGrade(98);
   var_dump(serialize($emp));
```

		以上代码执行后会输出：

```php
"O:7:"student":3:{s:4:"name";s:3:"Tom";s:3:"age";i:20;s:14:"studentgrade";i:98;}"
```

		可以观察到类名、类的大小、变量名、变量类型、变量值、变量大小等信息都在字符串中，但类的方		 法却没有保存进序列化的字符串里。

          而反序列化就是将序列化后的字符串再转为原本的类 。

```php
PS C:\Users\86150> php "C:\Users\86150\AppData\Local\Temp\tempCodeRunnerFile.php"
object(__PHP_Incomplete_Class)#1 (4) {
  ["__PHP_Incomplete_Class_Name"]=>
  string(7) "student"
  ["name"]=>
  string(3) "Tom"
  ["age"]=>
  int(20)
  [" student grade"]=>
  int(98)
}
```

2.反序列化漏洞

反序列化漏洞就是将序列化后的字符串进行随意更改来控制输出敏感信息。

假设有这样一个环境:

存在url：

`127.0.0.1/ser.php`

其对应的后台代码如下:

```php
<?php
    class person {
        public $name="echo 'I am isee'";

        public function __wakeup(){
            eval ("$this->name;");
        }
    }


    if (isset($_GET['mid'])){
        $mid=$_GET['mid'];
        unserialize("$mid");
    }

    else{
        echo "<h1>hello!!!<h1/>";
    }
```

	这段代码定义了一个person类，person类里存在一个敏感函数eval()可以执行任意代码，当反序列化这个**person类形成的特殊字符串成功时会自动触发__wakeup()魔术方法，从而执行eval()函数(本例中，正常情况下，eval()触发会将$name的值当PHP代码解析，即输出I am isee** )，访问该页面，不传递参数时返回一个**hello！！！信息

![](https://cdn.nlark.com/yuque/0/2024/jpeg/43146588/1712311605461-bacfaa67-70a1-49bc-bdfd-33e03c6a9b1d.jpeg)

如果带上?mid参数服务器后端对应的PHP代码将会反序列化这个用户传参，此时如果我们在本地正常序列化这个**pesong类并拼接到?mid的结果是这样的:

本地正常序列化**person类：

```php
<?php
class person
{
    public $name = "echo 'I am isee'";

    public function __wakeup()
    {
        eval ("$this->name;");
    }
}
$person1=new person();
$mid=serialize($person1);
var_dump($mid);
//序列化后的字符串
//O:6:"person":1:{s:4:"name";s:16:"echo 'I am isee'";}
```

	url拼接mid参数后访问服务器：

![](https://cdn.nlark.com/yuque/0/2024/jpeg/43146588/1712311734648-9cf70e24-0b39-4c8c-8582-becd2b271977.jpeg)

可以清楚的看到，传递序列化后的字符串成功的被后台的unserialize()还原成了原本的person类，从而触发了__wakeup魔术方法，最终eval()成功的将$name的值 echo 'I am isee'将PHP代码解析，输出了I am isee字样



如果我们自定义这个序列化后的特殊字符串，会怎样?

![](https://cdn.nlark.com/yuque/0/2024/jpeg/43146588/1712311780122-8684e85c-3de2-43a0-846b-bd7874db2a07.jpeg)

![](https://cdn.nlark.com/yuque/0/2024/jpeg/43146588/1712311791589-69567487-39c0-41aa-b319-5a1bfc0be0c8.jpeg)

可以看到，ping命令被成功的执行，这也说明，其他的任意命令也可以执行了。

因此，简单小结一下PHP序列化与反序列化漏洞的成因：

序列化的字符串可以保存类的基本信息，反序列化的过程可以将这个特殊的字符串重新还原成类,虽然在整个序列化与反序列化的过程中我们无法控制类方法的改变(这个主要指后台的自定义函数)，但是我们却可以通过复写变量并借用类中自定义好的方法(服务器上的)或魔术方法(服务器存在的或本地自定义的)，并借用敏感函数来达到恶意效果。

关键点就在于PHP序列化与反序列化的过程用户可控。

3.魔术方法

```php
/**
 * __construct()//创建对象时触发
 * __destruct() //对象被销毁时触发
 * __call() //在对象上下文中调用不可访问的方法时触发
 * __callStatic() //在静态上下文中调用不可访问的方法时触发
 * __get() //用于从不可访问的属性读取数据
 * __set() //用于将数据写入不可访问的属性
 * __isset() //在不可访问的属性上调用isset()或empty()触发
 * __unset() //在不可访问的属性上使用unset()时触发
 * __invoke() //当脚本尝试将对象调用为函数时触发
 */
```

通过借助官网的例子进一步加深理解:

```php
class Ljie{

    // 被重载的数据
    private $data=array();
    // 重载不能用在已经被定义的属性
    public $declared=1;
    // 只有从类的外部访问这个属性时，重载才会发生
    private $hidden=2;

    // __set是给不可访问属性赋值时会被调用
    public function __set($name, $value)
    {
        // TODO: Implement __set() method.
        echo "Setting '$name' to '$value'\n";
        $this->data[$name]=$value;
    }

    // __get是读取不可访问的属性时会被调用
    public function __get($name)
    {
        // TODO: Implement __get() method.
        echo "Getting '$name'\n";
        if(array_key_exists($name,$this->data)){
            return $this->data[$name];
        }
        $trace=debug_backtrace();
        trigger_error(
            'Undefined property via __get(): ' . $name .
            ' in ' . $trace[0]['file'] .
            ' on line ' . $trace[0]['line'],
            E_USER_NOTICE
        );
        return null;
    }

    // 当对不可访问的属性调用isset()或者empty()时__isset()会被调用
    public function __isset($name)
    {
        // TODO: Implement __isset() method.
        echo "Is '$name' set?\n";
        return isset($this->data[$name]);
    }

    // 当对不可访问的属性调用unset()时__unset()会被调用
    public function __unset($name)
    {
        // TODO: Implement __unset() method.
        echo "Unsetting '$name'\n";
        unset($this->data[$name]);
    }

    public function getHidden(){
        return $this->hidden;
    }
}
```

通过上面的类创建一个实例，并对他没有的元素进行赋值，触发set方法，通过访问定义的不可访问的元素触发get方法，相应的触发其他的方法如下：

```php
echo "<pre>\n";
$obj=new Ljie;
// 触发__set(),(key,value)<-->(a,1)
$obj->a=1;
// 触发__get(),(key,value)<-->(a,1)
echo $obj->a."\n\n";
// 触发__isset()
var_dump(isset($obj->a));
// 触发__unset()
unset($obj->a);
var_dump(isset($obj->a));
echo "\n";
echo $obj->declared . "\n\n";
echo "Let's experiment with the private property named 'hidden':\n";
echo "Privates are visible inside the class, so __get() not used...\n";
echo $obj->getHidden() . "\n";
echo "Privates not visible outside of class, so __get() is used...\n";
// 会触发__get()函数，但是会发出警告
echo $obj->hidden . "\n";
相应的结果如下：
Setting 'a' to '1'
Getting 'a'
1

Is 'a' set?
bool(true)
Unsetting 'a'
Is 'a' set?
bool(false)

1

Let's experiment with the private property named 'hidden':
Privates are visible inside the class, so __get() not used...
2
Privates not visible outside of class, so __get() is used...
Getting 'hidden'

Notice:  Undefined property via __get(): hidden in
call方法和callStatic方法的调用例子:
class LjieTest{
    public function __call($name, $arguments)
    {
        // TODO: Implement __call() method.
        echo $name."\n";
        echo "Calling object method '$name'".implode(',',$arguments)."\n";
    }

    // php 5.0.3之后的版本
    public static function __callStatic($name, $arguments)
    {
        // TODO: Implement __callStatic() method.
        echo "Calling static method '$name'".implode(',',$arguments)."\n";
    }
}
$obj=new LjieTest;
$obj->runTest('Ljie');
LjieTest::runTest('Ljie');
```



