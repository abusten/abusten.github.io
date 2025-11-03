 >**官方文档地址**：[https://docs.oracle.com/javase/tutorial/jndi/overview/index.html](https://docs.oracle.com/javase/tutorial/jndi/overview/index.html)
# 什么是JNDI
根据官方文档，JNDI 全称为 **Java Naming and Directory Interface**，即 Java 名称与目录接口。也就是一个名字对应一个 Java 对象。

也就是一个字符串对应一个对象。

jndi 在 jdk 里面支持以下四种服务
![[jndiarch.gif]]
- LDAP：轻量级目录访问协议
- 通用对象请求代理架构(CORBA)；通用对象服务(COS)名称服务
- Java 远程方法调用(RMI) 注册表
- DNS 服务

前三种都是字符串对应对象，DNS 是 IP 对应域名。
