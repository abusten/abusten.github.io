# Spring简介
## 关于Spring
Spring 理念 : 使现有技术更加实用 . 本身就是一个大杂烩 , 整合现有的框架技术

- SSH：Struct2 + Spring + Hibernate
- SSM: SpringMVC + Spring + Mybatis

Spring 的一些特点：

轻量级框架，特点 IoC：控制反转；AOP：切面编程。
### 组成

Spring 毕竟也是一个框架，所以框架肯定是支持很多功能的，我们要实现功能，或者说要通过框架来完成业务，只需要打配置即可。Spring 框架支持的一些功能如下图所示。
![[SpringWork.png]]
这里可以简单解释一下几点东西：

- 最底下一定是我们的 Core，也就是所谓的 “核”
- 往上走支持一些编程思想：IOC，AOP
- 还支持 ORM（也就是处理数据库等语句，可以类比为 Mybatis）
- 还支持很多 Web，比如 Web Application，Servlet 等

之前学习有个误区，觉得应该先学 SpringBoot 再去看其他的，其实正常的学习路线应该是：Spring —-> SpringBoot —-> SpringCloud 这个样子；

在 Spring 的官网上，Spring.io 有一条这样的学习路线：
![[SpringRoute.png]]
为什么 Spring 之后是 SpringBoot，然后是 SpringCloud 呢？因为 Spring 的配置非常繁琐，有时候我们不得不配置一些与我们本身的 Web 应用关系不大的东西。所以 SpringBoot 顺势而生。
# Spring核心之一：IoC
## IoC
先新建一个项目，并创建 Module，导入 Maven 的 jar 包。
导入的jar包如下：
```xml
<dependency>  
 <groupId>org.springframework</groupId>  
 <artifactId>spring-webmvc</artifactId>  
 <version>5.3.16</version>  
</dependency>  
  
<dependency>  
 <groupId>org.springframework</groupId>  
 <artifactId>spring-jdbc</artifactId>  
 <version>5.3.16</version>  
</dependency>
```
### IoC介绍
IoC （Inversion of Control ）即控制反转/反转控制。它是一种思想不是一个技术实现。描述的是：Java 开发领域对象的创建以及管理的问题。

例如：现有类 A 依赖于类 B

- **传统的开发方式** ：往往是在类 A 中手动通过 new 关键字来 new 一个 B 的对象出来
- **使用 IoC 思想的开发方式** ：不通过 new 关键字来创建对象，而是通过 IoC 容器(Spring 框架) 来帮助我们实例化对象。我们需要哪个对象，直接从 IoC 容器里面去取即可。

从以上两种开发方式的对比来看：我们 “丧失了一个权力” (创建、管理对象的权力)，从而也得到了一个好处（不用再考虑对象的创建、管理等一系列的事情）

**为什么叫控制反转?**

- **控制** ：指的是对象创建（实例化、管理）的权力
- **反转** ：控制权交给外部环境（IoC 容器）
![[IoC&Aop-ioc-illustration.png]]

我们用代码来实现一下，看一看为什么要用到 IOC 的这种编程思维。
## 传统的业务实现
在看 IOC 的编程思想之前，我们可以先看一看传统的编程思想：

传统的编程思想：`Controller` 层写接口，去调用 `Service` 层，`Service` 层里面有一个 `Service` 接口，还有一个 `ServiceImpl` 的实现类，具体的业务是写在 ServiceImpl 里面的。

`Service` 层去调用 `Dao` 层，也就是我们的实体类，我们的 `Dao` 层有一个 `Dao` 的抽象接口，还有一个 `DaoImpl` 的实现类。

- 大致的流程就是 `Controller` 调 `Service` 调 `Dao`
e.g.
**UserDAO.java**
```JAVA
package DAO;  
  
public interface UserDAO {  
    public void getUser();  
}
```
UserDAO 的实现类 ———— **UserDAOImpl.java**

```java
package DAO;  
  
import DAO.UserDAO;  
  
public class UserDAOImpl implements UserDAO {  
    @Override  
 public void getUser() {  
        System.out.println("输出获取用户数据");  
 }  
}
```
**UserService.java** Service 业务层
```java
package Service;  
  
public interface UserService {  
    public void getUser();  
}
```

**UserServiceImpl.java** Service 业务实现类
```java
package Service;  
  
import DAO.UserDAO;  
import DAO.UserDAOImpl;  
  
public class UserServiceImpl implements UserService{  
  
    private UserDAO userDAO = new UserDAOImpl();  
  
 @Override  
 public void getUser() {  
        userDAO.getUser();  
 }  
}
```
这个地方需要提一嘴，我们的 UserService 全程都是在调用 DAO 层的，很有趣。

最后编写一个测试的启动类。

**TestApplication.java**
```java
import Service.UserService;  
import Service.UserServiceImpl;  
  
public class TestApplication {  
    public static void main(String[] args) {  
        UserService userService = new UserServiceImpl();  
 userService.getUser();  
 }  
}
```
![[Pasted image 20250905214537.png]]
