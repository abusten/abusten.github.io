# Java代理模式
首先介绍什么是代理，打个比方下面的中介就是代理
![[Pasted image 20251101110610.png]]
## 静态代理
### 简单理解静态代理
- 以租客找**中介**向房东租房子为例
想要实现**租客找中介租房东**，在 Java 中就需要4个文件，分别是房源、房东、中介、租客，其中房源应该是接口，其余三项为类。
- `Rent.java`：这是一个接口，可以抽象的理解为房源，作为房源，它有一个方法`rent()`为**租房**
**Rent.java**
```java
package src.JdkProxy.StaticProxy;

// 租房的接口
public interface Rent {

    public void rent();
}
```

- `Host.java`：这是一个类，这个类就是房东，作为房东，他需要实现`Rent.java`这一个接口，并且要实现接口的`rent()`方法
**Host.java**
```java
package src.JdkProxy.StaticProxy;

public class Host implements Rent {

    public void rent(){
        System.out.println("房东要出租房子");
 }
}
```
- `Client.java`：这是一个启动类，这个类其实就是租客，租客的想法也很简单，就是找到中介，然后租房（为什么不直接找房东呢？因为房东通常不想管那么多事，而且房源基本被中介垄断）
因为租客是要去找中介看房的，而不是去找房东看房的，所以我们这里先把 Proxy.java 实现一下，也就是把中介相关的功能先实现一下。
- `Proxy.java`：这是一个类，这个类是中介，也就是代理，他需要有房东的房源，然而我们通常不会继承房东，而会将房东作为一个私有的属性`host`，我们通过`host.rent()`来实现租房的方法。  
**Proxy.java**
```java
package src.JdkProxy.StaticProxy;

// 中介
public class Proxy {

    private Host host;

 public Proxy(){}
    public Proxy(Host host){
        this.host = host;
 }

    public void rent(){
        host.rent();
 }
}
```
**Client.java**租客去找中介看房
```java
package src.JdkProxy.StaticProxy;

// 启动器
public class Client {
    public static void main(String[] args) {
        Host host = new Host();
 Proxy proxy = new Proxy(host);
 proxy.rent();
 }
}
```
这样子，基本的看房就完成了
**优点：**
- 可以使得我们的真实角色更加纯粹 . 不再去关注一些公共的事情 .
- 公共的业务由代理来完成 . 实现了业务的分工 ,
- 公共业务发生扩展时变得更加集中和方便 .

**缺点 :**
- 一个真实类对应一个代理角色，代码量翻倍，开发效率降低 .
我们想要静态代理的好处，又不想要静态代理的缺点，所以 , 就有了动态代理 !

### 深入理解静态代理
深入到实际业务当中，比如我们平常做的最多的 CRUD
- `UserService.java`，这是一个接口，我们定义四个抽象方法。
```java
package src.JdkProxy.MoreStaticProxy;

// 深入理解静态代理
public interface UserService {
 public void add();
 public void delete();
 public void update();
 public void query();
}
```
我们需要一个真实对象来完成这些增删改查操作  
**UserServiceImpl.java**
```java
package src.JdkProxy.MoreStaticProxy;

public class UserServiceImpl implements UserService{

    @Override
 public void add() {
        System.out.println("增加了一个用户");
 }

    @Override
 public void delete() {
        System.out.println("删除了一个用户");
 }

    @Override
 public void update() {
        System.out.println("更新了一个用户");
 }

    @Override
 public void query() {
        System.out.println("查询了一个用户");
 }
}
```

需求来了，现在我们需要增加一个日志功能，怎么实现！

- 思路1 ：在实现类上增加代码 【麻烦！】
- 思路2：使用代理来做，能够不改变原来的业务情况下，实现此功能就是最好的了！

> 处理手段：增加一个代理类来处理日志~

**UserServiceProxy.java**

```
package src.JdkProxy.MoreStaticProxy;

// 代理
public class UserServiceProxy implements UserService{
    private UserServiceImpl userService;

 public void setUserService(UserServiceImpl userService) {
        this.userService = userService;
 }

    public void add() {
        log("add");
 userService.add();
 }

    public void delete() {
        log("delete");
 userService.delete();
 }

    public void update() {
        log("update");
 userService.update();
 }

    public void query() {
        log("query");
 userService.query();
 }

    // 增加日志方法
 public void log(String msg){
        System.out.println("[Debug]使用了 " + msg +"方法");
 }
}
```

修改启动器 **Client.java**

```
package src.JdkProxy.MoreStaticProxy;

public class Client {
    public static void main(String[] args) {
        UserServiceImpl userService = new UserServiceImpl();

 UserServiceProxy proxy = new UserServiceProxy();
 proxy.setUserService(userService);
 proxy.add();

 }
}
```
如此一来，增加业务点的日志便成功了
## 动态代理

- 前文我们说到静态代理的问题，还记得吗？
    

每多一个房东就需要多一个中介，这显然不符合生活认知（对于租客来说，如果是用静态代理模式，每当想要换一个房东，那就必须要再换一个中介，在开发中，如果有多个中介代码量就更大了）

动态代理的出现就是为了解决上面静态代理的缺点。

### 动态代理的一些基础知识

> 下面讲的主要是一些源码的东西吧，不看也可。我是不建议看的，但是为了文章内容的完整性，我还是贴上来吧。

- 动态代理的角色和静态代理的一样。需要一个实体类，一个代理类，一个启动器。
- 动态代理的代理类是动态生成的，静态代理的代理类是我们提前写好的。

**JDK的动态代理需要了解两个类**

核心 : InvocationHandler 调用处理程序类和 Proxy 代理类

**InvocationHandler：调用处理程序**

```
public interface InvocationHandler
```

InvocationHandler是由代理实例的调用处理程序实现的接口

每个代理实例都有一个关联的调用处理程序。

```
Object invoke(Object proxy, 方法 method, Object[] args)；
```

当在代理实例上调用方法的时候，方法调用将被编码并分派到其调用处理程序的`invoke()`方法。

**参数**：

- `proxy`– 调用该方法的代理实例
- `method`-所述方法对应于调用代理实例上的接口方法的实例。方法对象的声明类将是该方法声明的接口，它可以是代理类继承该方法的代理接口的超级接口。
- `args`-包含的方法调用传递代理实例的参数值的对象的阵列，或null如果接口方法没有参数。原始类型的参数包含在适当的原始包装器类的实例中，例如`java.lang.Integer`或`java.lang.Boolean`。
    

**Proxy : 代理**

```
public class Proxy extends Object implements Serializable
```

`Proxy`提供了创建动态代理类和实例的静态方法，它也是由这些方法创建的所有动态代理类的超类。

动态代理类 （以下简称为代理类 ）是一个实现在类创建时在运行时指定的接口列表的类，具有如下所述的行为。 代理接口是由代理类实现的接口。 代理实例是代理类的一个实例。

```
public static Object newProxyInstance(ClassLoader loader, 类<?>[] interfaces, InvocationHandler h) throws IllegalArgumentException
```

返回指定接口的代理类的实例，该接口将方法调用分派给指定的调用处理程序。

**参数**

- `loader`– 类加载器来定义代理类
    
- `interfaces`– 代理类实现的接口列表
    
- `h`– 调度方法调用的调用处理函数
    

### 动态代理的代码实现

- 要写动态代理的代码，需要抓牢两个要点

①：我们代理的是接口，而不是单个用户。  
②：代理类是动态生成的，而非静态定死。

我只能说这种编程思想是真的牛逼，其实我们还可以实现任意接口的动态代理实现，在这里就不贴出来了。

首先是我们的接口类  
**UserService.java**

```
package src.JdkProxy.DynamicProxy;


public interface UserService {
    public void add();
 public void delete();
 public void update();
 public void query();
}
```

接着，我们需要用实体类去实现这个抽象类

**UserServiceImpl.java**

```
package src.JdkProxy.DynamicProxy;

public class UserServiceImpl implements UserService{
    @Override
 public void add() {
        System.out.println("增加了一个用户");
 }

    @Override
 public void delete() {
        System.out.println("删除了一个用户");
 }

    @Override
 public void update() {
        System.out.println("更新了一个用户");
 }

    @Override
 public void query() {
        System.out.println("查询了一个用户");
 }
}
```

接着，是动态代理的实现类

```
package src.JdkProxy.DynamicProxy;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;

public class UserProxyInvocationHandler implements InvocationHandler {

    // 被代理的接口
 private UserService userService;

 public void setUserService(UserService userService) {
        this.userService = userService;
 }

    // 动态生成代理类实例
 public Object getProxy(){
        Object obj = Proxy.newProxyInstance(this.getClass().getClassLoader(), userService.getClass().getInterfaces(), this);
 return obj;
 }

    // 处理代理类实例，并返回结果
 @Override
 public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        log(method);
 Object obj = method.invoke(userService, args);
 return obj;
 }

    //业务自定义需求
 public void log(Method method){
        System.out.println("[Info] " + method.getName() + "方法被调用");
 }
}
```

- 最后编写我们的 Client，也就是启动器
    

**Client.java**

```
package src.JdkProxy.DynamicProxy;

import src.JdkProxy.DynamicProxy.UserServiceImpl;

public class Client {
    public static void main(String[] args) {
        // 真实角色
 UserServiceImpl userServiceImpl = new UserServiceImpl();
 // 代理角色，不存在
 UserProxyInvocationHandler userProxyInvocationHandler = new UserProxyInvocationHandler();
 userProxyInvocationHandler.setUserService((UserService) userServiceImpl); // 设置要代理的对象

 // 动态生成代理类
 UserService proxy = (UserService) userProxyInvocationHandler.getProxy();

 proxy.add();
 proxy.delete();
 proxy.update();
 proxy.query();
 }
}
```
- 上述，我们的动态代理便完成了。
#  在反序列化中动态代理的作用

- 如果只是纯讲开发，没什么意义，我们重点来了，动态代理是如何参与反序列化攻击的。

回到之前文章的内容，我们之前说要利用反序列化的漏洞，我们是需要一个入口类的。

我们先假设存在一个能够漏洞利用的类为`B.f`，比如`Runtime.exec`这种。  
我们将入口类定义为`A`，我们最理想的情况是 A[O] -> O.f，那么我们将传进去的参数`O`替换为`B`即可。但是在实战的情况下这种情况是极少的。

回到实战情况，比如我们的入口类`A`存在`O.abc`这个方法，也就是 A[O] -> O.abc；而 O 呢，如果是一个动态代理类，`O`的`invoke`方法里存在`.f`的方法，便可以漏洞利用了，我们还是展示一下。

```
A[O] -> O.abc
O[O2] invoke -> O2.f // 此时将 B 去替换 O2
最后  ---->
O[B] invoke -> B.f // 达到漏洞利用效果
```

动态代理在反序列化当中的利用和`readObject`是异曲同工的。

`readObject`方法在反序列化当中会被自动执行。  
而`invoke`方法在动态代理当中会自动执行。
