# 一个快速打开网盘链接的方法

## 说明

老师把课件放到百度网盘了, 又不想把网盘链接添加到浏览器书签.  

那么每次下课件都要找网盘链接, 还不如把链接写进html里面以后双击就打开了.

>对于网盘有验证码的情况, 一般输入一次就够了, 下次打开链接的时候百度网盘服务器根据cookies应该能认出你, 就可以免登了.

如果有不止一个网盘链接的话, 可以试试`muti_jump.html`, 丢失了自动跳转的遍历, 毕竟不知道你想跳到那个链接上面. 打开html文件后再单击超链接文本就可以跳转了.

## 配置

- `auto_jump.html`

编辑器打开文件, 将

```html
    <script language='javascript'>document.location = 'https://pan.baidu.com/s/url/of/your/lecture'</script>
```

这行里面的`https://pan.baidu.com/s/url/of/your/lecture`改成对应的网盘链接(不一定是百度网盘), 保存文件.

- `muti_jump.html`

```html
    <li><a href="https://www.baidu.com">第一个网盘链接</a></li>
    <li><a href="https://www.bing.com">百度网盘链接</a></li>
    <li><a href="https://www.google.com">腾讯微云链接</a></li>
```

将`href`后的网址改成想要的链接, 后面的文本是网页打开时显示的文字.

> <span color="blue">如果觉得有帮助就点个**star**呗</span>
