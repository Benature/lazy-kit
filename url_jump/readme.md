# 一个快速打开网盘链接的方法

## 说明

老师把课件放到百度网盘了, 又不想把网盘链接添加到浏览器书签.  

那么每次下课件都要找网盘链接, 还不如把链接写进html里面以后双击就打开了.

>对于网盘有验证码的情况, 一般输入一次就够了, 下次打开链接的时候百度网盘服务器根据cookies应该能认出你, 就可以免登了.

## 配置

用编辑器打开`jump2pan.html`, 将

```html
    <script language='javascript'>document.location = 'https://pan.baidu.com/s/url/of/your/lecture'</script>
```

这行里面的`https://pan.baidu.com/s/url/of/your/lecture`改成对应的网盘链接(不一定是百度网盘), 保存文件.

<!-- <div style="margin-bottom: 20px;padding: 15px;position: relative;border: 1px solid #eee;border-left-width: 5px;border-radius: 3px;border-left-color: #428bca"><p>如果觉得有帮助就点个**star**呗</p></div> -->
> <span color="blue">如果觉得有帮助就点个**star**呗</span>
