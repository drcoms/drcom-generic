本页面仅供drcom客户端开发的童鞋有价值，需要有一些相关的知识。有关drcom所有项目仅供研究使用，由滥用造成的法律后果与作者无关。

*如果你愿意捐助作者这个穷屌, 支付宝: latyas@live.com*

建议有问题先读wiki，再发issue

* 相关工具和验证用的代码在 *utils* 目录下
* 测试数据在 *tests* 目录下
* 所有说明已移动到 [wiki](https://github.com/drcoms/generic/wiki) 中

其他
-------------------
#### 黑科技：drcom client on 8266
<http://blog.lyj.me/hei-ke-ji-esp8266-drcom-client/>

#### drcom_2011.lua
这是一个由 *googlecode* 上 *jdrcom* 项目中的 *wireshark* 插件 <br>
项目地址：(https://code.google.com/p/jdrcom/) <br>
使用(for windows):

将 *drcom_2011.lua* 放到 *Wireshark.exe* 所在的目录下， 打开 *init.lua* ，在 `dofile(DATA_DIR.."console.lua")` 之后添加 `dofile(DATA_DIR.."drcom_2011.lua")`.

之后就可以在过滤器中使用 *drcom* 协议了。

#### 其他最新客户端
HITwh的Shindo酱的项目也是非常优秀，适用x版，请参考 <br>
https://github.com/coverxit/EasyDrcom/

# 许可证

GPLv2

特别指出禁止任何个人或者公司将 [drcoms](http://github.com/drcoms/) 的代码投入商业使用，由此造成的后果和法律责任均与本人无关。 

