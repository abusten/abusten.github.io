**Cross-Site Scripting**
- XSS是一种发生在Web前端的漏洞，所以其危害的对象主要是前端用户。
- XSS漏洞可以用来进行钓鱼攻击，前端js挖矿，获取用户cookie，甚至可以结合浏览器自身的漏洞对用户主机进行远程控制等
# 跨站脚本漏洞常见类型
## - 反射型  
交互的数据一般不会被存在数据库里面，一次性，一般出现在查询类等页面。
### 什么是反射型xss
反射型 XSS，也叫非持久型 XSS，转瞬即逝。
最简单的xss payload如下：
```javascript
<script>alert(1)</script>
```
不过这种标签大多会被过滤，所以重点是绕过手段
#### 当大多数标签被禁止
[Lab: Reflected XSS into HTML context with most tags and attributes blocked](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-html-context-with-most-tags-and-attributes-blocked)
fuzz测试内容：[Cross-site scripting (XSS) cheat sheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)
大多数标签都被过滤了，不过依然可以通过`<body>`和`onresize`绕过
onresize 属性在调整窗口大小时触发。语法：`<_element_ onresize="_script_">`
支持onresize事件的属性：
```html
<a>, <address>, <b>, <big>, <blockquote>, <body>, <button>, <cite>, <code>, <dd>, <dfn>, <div>, <dl>, <dt>, <em>, <fieldset>, <form>, <frame>, <h1> to <h6>, <hr>, <i>, <img>, <input>, <kbd>, <label>, <legend>, <li>, <object>, <ol>, <p>, <pre>, <samp>, <select>, <small>, <span>, <strong>, <sub>, <sup>, <table>, <textarea>, <tt>, <ul>, <var>
```
#### 当事件处理器与 href 被禁用时的绕过
[Lab: Reflected XSS with event handlers and href attributes blocked](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-event-handlers-and-href-attributes-blocked)
老样子还是需要 Fuzz 的。如果渗透测试真正遇到这种情况的话，`svg` 标签的绕过方式还是主流。
Payload
```html
<svg>
	<a>
	<animate attributeName=href
     values=javascript:alert(1) />
		<text x=20 y=20>Click me</text>
    </a>
```
还有一些 `svg` 标签的绕过手段
```javascript
<svg><animatetransform onbegin=alert(1)>
```

## - 存储型  
交互的数据被存储在数据库里，永久性存储，一般出现在留言板，注册类等页面。
## - DOM型  
不与后台服务器产生数据交互，通过DOM操作前端代码 输出的时候产生的问题，一次性，也属于反射型。
# XSS漏洞成因
主要是对用户输入和输出控制不够严格，也有浏览器无法正确区分html元素是开发者设置的还是用户设置的原因。
# XSS危害
xss本质上是一种钓鱼攻击，所以危害角度上也是以钓鱼造成的危害相同。
# 跨站脚本漏洞测试流程

1. 在目标站点找到输入点，比如查询接口，留言板等；
2. 输入一组“特殊字符+唯一识别字符”，点击提交后，查看返回的源码，是否有做对应的处理。
3. 通过搜索定位到唯一字符，结合唯一字符前后语法确认是否可以构造执行JS代码的条件（构造闭合）；
4. 提交payload，成功执行则存在xss漏洞。
# tips
1. 一般查询接口易出现反射型xss，留言板易出现存储型xss。
2. 后台可能存在过滤措施，构造的script可能会被过滤掉，从而无法生效。
3. 通过变化不同的script，尝试绕过后台过滤机制。
4. xss漏洞一般影响并不大，因为利用条件比较苛刻，因为只有受害者点击相关链接才有可能进行利用，而且大多也就是盗取cookie，如果网站登录验证做得严格一些拿了cookie也登不上，影响最大的存储型xss因为写入后端看到的用户比较多，受害者范围比较广一般也就是中危，像反射型如果是xss注入点在GET参数里好歹能外带到链接里进行短域名生成之后让受害人点击触发，运气好厂商可能算个低危；如果是POST参数就利用不了了。
