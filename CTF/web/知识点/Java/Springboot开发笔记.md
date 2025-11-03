# 父工程
在springboot[官方文档](https://docs.spring.io/spring-boot/docs/3.2.0-SNAPSHOT/maven-plugin/reference/htmlsingle/#using.parent-pom) 中亦有记载，是用Maven创建项目后需要在pom.xml添加的，父工程是一种依赖管理。比如说 A 依赖于其他库 B。如果，另外一个项目 C 想要使用 A ，那么 C 项目也需要使用库 B。而找出和管理项目之间的依赖就是依赖管理。官方文档里的父工程如下：
```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <!-- Import dependency management from Spring Boot -->
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>3.2.0-SNAPSHOT</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```
# 起步依赖
springboot的起步依赖包含tomcat、spring-webmvc等等依赖项。spring-boot-start-XXX就是spring-boot的场景启动器。我们还可以自己定义starter。官方文档里的起步依赖如下：
```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <!-- Import dependency management from Spring Boot -->
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>3.2.0-SNAPSHOT</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```
# 容器
容器是一种虚拟化技术，将应用程序和其依赖项打包到一起，使其可以脱离操作系统环境运行，你如一个容器封装起来可以让Centos正常运行应用程序从Centos移动到ubuntu上也能正常运行。Linux Container容器技术一种**内核轻量级的操作系统层**虚拟化技术，与硬件抽象层虚拟化hypervisor技术相比有三个特点：
- 极其轻量：只打包了必要的Bin/Lib；
- 秒级部署：根据镜像的不同，容器的部署大概在毫秒与秒之间（比虚拟机强很多）；
- 易于移植：一次构建，随处部署；
- 弹性伸缩：Kubernetes、[Swam](https://zhida.zhihu.com/search?content_id=7763038&content_type=Article&match_order=1&q=Swam&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NTIzMjg3MjEsInEiOiJTd2FtIiwiemhpZGFfc291cmNlIjoiZW50aXR5IiwiY29udGVudF9pZCI6Nzc2MzAzOCwiY29udGVudF90eXBlIjoiQXJ0aWNsZSIsIm1hdGNoX29yZGVyIjoxLCJ6ZF90b2tlbiI6bnVsbH0.gZx5Yj-2niOlgTonJSIzPEjRgIxr6oNqAiXdTyLHy9I&zhida_source=entity)、[Mesos](https://zhida.zhihu.com/search?content_id=7763038&content_type=Article&match_order=1&q=Mesos&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NTIzMjg3MjEsInEiOiJNZXNvcyIsInpoaWRhX3NvdXJjZSI6ImVudGl0eSIsImNvbnRlbnRfaWQiOjc3NjMwMzgsImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.ZaEJP3neWjpRZRjqZWgHLLFrsV_iBiCxliUbMHFWiRM&zhida_source=entity)这类开源、方便、好使的容器管理平台有着非常强大的弹性管理能力。
# springboot里的bean
spring里的bean本质上是指代**任何被Spring加载生成出来的对象**。pring Bean代表着Spring中最小的执行单位，其加载、作用域、生命周期的管理都由Spring操作。可见Spring Bean在整个Spring框架中的重要地位。当我们需要用容器内的对象时，只需要“告诉”Spring，Spring就能自动帮我们加载，我们则无需考虑这个Bean到底是如何加载的、什么时候回收等细节逻辑。我们只需要使用即可。由此一来，**降低了使用门槛，也减少了对于细节的一些管理**。

自动装配机制是SpringBoot的一大亮点之一，其**主要依赖于@SpringBootApplication下的@EnableAutoConfiguration注解**实现。简单来说，就是在该注解指定的目录下，通过使用@Component及其衍生注解如@Service、@Repository等，Spring就会默认将对应对象注册道容器中。具体例子如下：

```java
@Data
@AllArgsConstructor
@NoArgsConstructor
@Component
public class MyBean {
    Integer filedA;

    String fieldB;
}
```

```java
@SpringBootApplication
@ComponentScan(basePackages = {"com.example.demo.*", "com.alibaba"}) // 需要显示指明路径。
@Slf4j
public class DemoApplication {
    
	@SneakyThrows
    public static void main(String[] args) {
        ConfigurableApplicationContext run = SpringApplication.run(DemoApplication.class, args);
        Object myBean = run.getBean("myBean");
        System.out.println(myBean);
    }
}
```

自动装配的方案，**遵循了“约定大于配置”的设计理念**，通过约定俗成来极大减少了程序员开发的成本。在通常情况下，Spring只会默认扫描当前类路径下的组件，不会扫描其他第三方包组件。可以通过上文的@ComponentScan来扩充扫描的范围，当然也可以通过在类路径下修改_META-INF/spring.factories_文件，来指定对应的扫描路径。
# 自动配置原理
## pom.xml
- spring-boot-dependencies:核心依赖在父工程
- 引入springboot依赖不需要指定版本的原因：有版本仓库
## 启动器
```xml
<dependencies>  
    <dependency>        <groupId>org.springframework.boot</groupId>  
        <artifactId>spring-boot-starter-web</artifactId>  
    </dependency>  
    <dependency>        <groupId>org.springframework.boot</groupId>  
        <artifactId>spring-boot-starter-test</artifactId>  
        <scope>test</scope>  
    </dependency></dependencies>
```
启动器就是Springboot的启动场景。`spring-boot-starter-web`就是springboot在web环境下的启动器
## 主程序
```java
package com.johnsmith;  
  
import org.springframework.boot.SpringApplication;  
import org.springframework.boot.autoconfigure.SpringBootApplication;  
  
@SpringBootApplication  
public class SpringbootHelloworldApplication {  
  
    public static void main(String[] args) {  
        SpringApplication.run(SpringbootHelloworldApplication.class, args);  
    }  
  
}
```
其中`@SpringBootApplication`是一个注解，意思是这是一个springboot应用，只有加上这个注解程序才能正常运行。
`SpringApplication.run`是一个静态方法，通过反射调用class，它有多个注解组成，主要有：
- SpringBootConfiguration:SpringBoot配置
	 - @configuration：spring配置类
	    - @component：说明这也是一个spring组件
- EnableAutoConfiguration:自动配置导入包
    - AutoConfigurationPackage：自动导入包
	    - import(AutoConfigurationPackage.Register.class)：自动配置包
    - import(AutoConfigurationImportSelector.class)：自动导入类（自动导入包的核心）
	    - AutoConfigurationImportSelector()：选择了什么
		    - GetAutoConfigrationEntry():获得自动导入的实体
		    - CandidateConfigration():获得候选的配置
			    - ```protected Class getSpringFactoriesLoaderFactoryClass(){
					    return EnableAutoConfigration.class//标注了EnableAutoConfigration注解的类
				 }```
		    - public static List loadFactoryNames()：获取所有加载配置
		    - loadSpringFactories()
			    - 项目资源：classLoader.getResources(FACTORIES_RESOURCE_LOCATION):
				    - "META-INF/spring.factories":从这里获取配置
						- spring-boot-autoconfigure-3.5.3.RELEASE.jar
							- META-INF
								- spring.factories:所有自动配置类都在这里
									- 思考：为什么那么多自动配置的类没有生效，导入对应的starter才会生效？
										- 核心注解：@ConditionalOnXXX:如果这里面的条件都满足才会生效
				- 系统资源：ClassLoader.getSystemResources(FACTORIES_RESOURCE_LOCATION);
				- 从这些资源中便利了所有的nextElement(自动配置)，比那里完成之后，封装为Properties供我们使用
- ComponentScan：扫描当前主启动类同级的包
![[Pasted image 20250710213551.png]]
springboot中所有的自动配置都在启动时扫描并加载，自动配置类都在`spring.factories`里，不过不一定生效，只有经过相关方法的判断，也就是导入对应的start，就有对应的启动器，才能自动配置成功，具体步骤如下：
1. springboot启动时先从Maven的`/META-INF/spring.factories`类路径获取指定的值
2. 将这些自动配置的类导入容器，自动配置就会生效
3. SpringMVC需要自动配置的东西，springboot帮我们做了
4. 整合javaEE，解决方案和自动配置的东西都在
# yaml配置文件
springboot的`/src/main/resource`文件里有个application.properties配置文件，可以删掉换成application.yaml，yaml的优势是语法简单，除了可以储存普通键值以外还可以储存对象
`application.yaml`:
```yaml
#key: value
#对象
student:
	name: JohnSmith
	age: 18
#行内写法
student: {name: JohnSmith,age: 18}
#数组
pets:
	- cat
	- dog
#行内写法
pets: [cat,dog]
```
等价于：
`application.properties`:
```
#key=value
student.name=JohnSmith
student.age=18
```
yaml文件里的对象可以注入到配置类里。
