# drcom-generic [![Join the chat at https://gitter.im/drcoms/drcom-generic](https://badges.gitter.im/drcoms/drcom-generic.svg)](https://gitter.im/drcoms/drcom-generic?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

## 注意

本项目会随着 *DrCOM* 客户端更新而跟进，建议您使用 *Watch* 而不是 *fork* 功能，因为 *fork* 具有时效性，您 *fork* 的代码可能不是最新的。项目不会关闭，所以请放心使用。跪求折腾 *DrCOM* 的同学，请发邮件到 *latyas at gmail.com*, 让我把您加入开发者。

## 发起Issue
如果你不能登录，请发Issue的时候附上用哪个脚本文件，脚本的日志输出，正常客户端的抓包，并且附上你的学校的名称，最好可以提供相关的Windows和Linux下的客户端，提高沟通效率。

## 说明
本页面仅供drcom客户端开发的童鞋有价值，需要有一些相关的知识。有关drcom所有项目仅供研究使用，由滥用造成的法律后果与作者无关。

建议有问题先读wiki，再发issue

* 在线配置器 http://drcoms.github.io/drcom-generic/ by NTR君 (Firefox有秘制bug，请用Chrome或IE)
* 相关工具和验证用的代码在 *utils* 目录下
* 测试数据在 *tests* 目录下
* 某些学校的版本请在 *custom* 目录中寻找
* 所有说明已移动到 [wiki](https://github.com/drcoms/generic/wiki) 中

## 其他
#### 黑科技：drcom client on 8266
<http://obaka.moe/hei-ke-ji-esp8266rang-ni-bai-tuo-drcomke-hu-duan.html>

#### drcom_2011.lua
这是一个由 *googlecode* 上 *jdrcom* 项目中的 *wireshark* 插件 <br>
项目地址：(https://code.google.com/p/jdrcom/) <br>
使用(for windows):
> 将 *drcom_2011.lua* 放到 *Wireshark.exe* 所在的目录下， 打开 *init.lua* ，在 `dofile(DATA_DIR.."console.lua")` 之后添加 `dofile(DATA_DIR.."drcom_2011.lua")`.

之后就可以在过滤器中使用 *drcom* 协议了。

#### 其他最新客户端
HITwh的Shindo酱的项目也是非常优秀，适用x版，请参考 <br>
https://github.com/coverxit/EasyDrcom/

## 许可证

AGPLv3

特别指出禁止任何个人或者公司将 [drcoms](http://github.com/drcoms/) 的代码投入商业使用，由此造成的后果和法律责任均与本人无关。 
