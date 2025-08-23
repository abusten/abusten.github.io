> *学到哪记哪* 
## 接口
- 普通类：只有具体实现
- 抽象类：具体实现和规范（抽象方法）都有
- 接口：只有规范（抽象方法）无法写方法。约束和实现分离：面向接口编程
接口是一组规范，定义一组规则，体现了“如果...必须...”的思想。
接口里的方法默认是public abstract的，不可修改
举个例子：
UserService:
```
public interface UserService{
	void read(string name);
	void write(string name);
}
```
UserServiceImpl:
```
public class UserServiseImpl implement UserServise{
	@Override
	public void read(string name){
	}
	@Override
	public void write(string name){
	}
}
```
接口可以实现多继承（例如UserServiceImpl类还能实现其他接口的抽象方法而不报错）
## 注解
注解是JDK1.5版本开始引入的一个特性，用于对代码进行说明，可以对包、类、接口、字段、方法参数、局部变量等进行注解。它主要的作用有以下四方面：

- 生成文档，通过代码里标识的元数据生成javadoc文档。
- 编译检查，通过代码里标识的元数据让编译器在编译期间进行检查验证。
- 编译时动态处理，编译时通过代码里标识的元数据动态处理，例如动态生成代码。
- 运行时动态处理，运行时通过代码里标识的元数据动态处理，例如使用反射注入实例。

这么来说是比较抽象的，我们具体看下注解的常见分类：

- **Java自带的标准注解**，包括`@Override`、`@Deprecated`和`@SuppressWarnings`，分别用于标明重写某个方法、标明某个类或方法过时、标明要忽略的警告，用这些注解标明后编译器就会进行检查。
- **元注解**，元注解是用于定义注解的注解，包括`@Retention`、`@Target`、`@Inherited`、`@Documented`，`@Retention`用于标明注解被保留的阶段，`@Target`用于标明注解使用的范围，`@Inherited`用于标明注解可继承，`@Documented`用于标明是否生成javadoc文档。
- **自定义注解**，可以根据自己的需求定义注解，并可用元注解对自定义注解进行注解。

接下来我们通过这个分类角度来理解注解。
### Java内置注解

我们从最为常见的Java内置的注解开始说起，先看下下面的代码：

```
class A{
    public void test() {
        
    }
}

class B extends A{

    /**
        * 重载父类的test方法
        */
    @Override
    public void test() {
    }

    /**
        * 被弃用的方法
        */
    @Deprecated
    public void oldMethod() {
    }

    /**
        * 忽略告警
        * 
        * @return
        */
    @SuppressWarnings("rawtypes")
    public List processList() {
        List list = new ArrayList();
        return list;
    }
}
```
#### 内置注解 - @Override

我们先来看一下这个注解类型的定义：

```
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.SOURCE)
public @interface Override {
}
```

从它的定义我们可以看到，这个注解可以被用来修饰方法，并且它只在编译时有效，在编译后的class文件中便不再存在。这个注解的作用我们大家都不陌生，那就是告诉编译器被修饰的方法是重写的父类的中的相同签名的方法，编译器会对此做出检查，若发现父类中不存在这个方法或是存在的方法签名不同，则会报错。

## Runtime类
Java Runtime类是与Java程序与Java运行底层环境虚拟机JVM沟通的重要途径。
Runtime类提供了许多的API 来与`java runtime environment`进行交互，如：
- 执行一个进程。
- 调用垃圾回收。
- 查看总内存和剩余内存。
Runtime是单例的，可以通过`Runtime.getRuntime()`得到这个单例。
### API列表

|public static Runtime getRuntime()|返回单例的Runtime实例|
|---|---|
|public void exit(int status)|终止当前的虚拟机|
|public void addShutdownHook(Thread hook)|增加一个JVM关闭后的钩子|
|public Process exec(String command)throws IOException|执行command指令，启动一个新的进程|
|public int availableProcessors()|获得JVM可用的处理器数量（一般为CPU核心数）|
|public long freeMemory()|获得JVM已经从系统中获取到的总共的内存数【byte】|
|public long totalMemory()|获得JVM中剩余的内存数【byte】|
|public long maxMemory()|获得JVM中可以从系统中获取的最大的内存数【byte】|

注：以上为列举的比较常见的一些方法，不完全。