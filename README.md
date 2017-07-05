
# drcom-generic [![Join the chat at https://gitter.im/drcoms/drcom-generic](https://badges.gitter.im/drcoms/drcom-generic.svg)](https://gitter.im/drcoms/drcom-generic?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) <a href="https://t.me/dajiji"><img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg" align="right" height="48" width="48" ></a>

## 注意

本项目会随着 *DrCOM* 客户端更新而跟进，建议您直接 *Watch* 而不要 *fork*，除非您想提交代码，不然 *fork* 毫无意义。请可以折腾 *DrCOM* 的同学，请发邮件到 latyas@gmail.com, 让我把您加入开发者。

## 发起Issue（提问的要求）
[提问的智慧](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/master/README-zh_CN.md)

如果你不能登录，请发Issue的时候附上用哪个脚本文件，脚本的日志输出，正常客户端的抓包，并且附上你的学校的名称，最好可以提供相关的Windows和Linux下的客户端，提高沟通效率。

所有的 Issue 在 15 天内没有**任何更新的**或者**已经解决**的将做关闭处理，除非再提供更有帮助于解决问题的资料，否则Issue不会Reopen，并且同一个人同样的Issue请不要重复提交。

同一个学校的同学请先自行搜索是否有已经解决的方案，强烈建议线下交流讨论，传播相关的解决方案，不赞成同样的问题提问多次，被判断为同样的Issue时，会给出可能相关的Issue，并且关闭掉当前的，如确有不同请在该issue下提交comment说明不同的地方，包括但不限于版本升级，不同校区，多版本共存等等。

请勿发表和本repo无关的issue，无关的issue一般包含但不限于下列议题：

* 学校11点半断网怎么破？
* p版如何多播?
* 为什么不做一个GUI?
* 路由器怎么刷openwrt?

有些问题需要你提供更详细的说明，而不是纯粹的描述你所看到的现象，如：

* Windows下程序闪退 - 请给出具体的错误或者异常栈
* Address has already used (一般广泛见于windows) - 请检查官方客户端是否关闭

等等

使用问题 **不建议** 在 issue 中提问，因为wiki中已经描述的足够清晰，这类问题大致上会问：

* 脚本怎么启动啊？
* 怎么放到路由器里

提问的标题最好可以直击主题，诸如以下的标题是不礼貌的：

* 老掉线
* 5.2.1(p)用不了
* 无法登陆

等等，合适的标题参考

* 如果掉了不能自动重连，已添加hotplug但还是得重启路由器才能连上
* drcom版本 5.2.0d，使用路由器登陆，多台设备时掉线
* 5.20x版802.1x正常，心跳包执行不到几次后802.1x收到下线报文
* “禁止商业使用“不属 AGPL 范畴（x
* 关于测试latest-pppoe.py 文件出现socket.timeout: timed out
* 已经拨号成功了，运行latest-pppoe.py 报错：socket.error: [Errno 10013]
* 吉大定制版，无限 被服务器拒绝 ([login] server return exception.retry)
* 如果IP是自动获取，那个host_ip = 应该怎么填写啊？

等等

如果你在 linux 环境下做测试，请在发 issue 的时候将发行版和其对应的版本一并发上来（假设没有进行过部件的升级），如果你使用的是 openwrt 系统，请使用官方源代码编译出的固件或者使用官方提供的编译好的固件，并提供对应的版本号。**请不要使用其他第三方的基于openwrt修改的系统进行测试** 我们没有测试条件。

与协议无关的问题，请尽量到gitter上问。

## 说明
本页面仅供drcom客户端开发的童鞋有价值，需要有一些相关的知识。有关drcom所有项目仅供研究使用，由滥用造成的法律后果与作者无关。

建议有问题先读wiki，再发issue

* 在线配置器 http://drcoms.github.io/drcom-generic/ by NTR君
* 相关工具和验证用的代码在 *utils* 目录下
* 测试数据在 *tests* 目录下
* 某些学校的版本请在 *custom* 目录中寻找
* 所有说明已移动到 [wiki](https://github.com/drcoms/generic/wiki) 中

## 其他
#### 黑科技：drcom client on 8266
<http://obaka.moe/hei-ke-ji-esp8266rang-ni-bai-tuo-drcomke-hu-duan.html>

#### drcom_2016.lua
这是一个由 *googlecode* 上 *jdrcom* 项目中的 *wireshark* 插件 <br>
项目地址：(https://code.google.com/p/jdrcom/) <br>
使用(for windows):
> 将 *drcom_2016.lua* 放到 *Wireshark.exe* 所在的目录下， 打开 *init.lua* ，在 `dofile(DATA_DIR.."console.lua")` 之后添加 `dofile(DATA_DIR.."drcom_2016.lua")`.

之后就可以在过滤器中使用 *drcom* 协议了。

#### 其他最新客户端
HITwh的Shindo酱的项目也是非常优秀，适用x版，请参考 <br>
https://github.com/coverxit/EasyDrcom/

**NTR君的dogcom**
https://github.com/mchome/dogcom


#### 其他哦莫西罗伊的版本
PHP版: https://github.com/dantmnf/drcom-client

## 许可证

AGPLv3

特别指出禁止任何个人或者公司将 [drcoms](http://github.com/drcoms/) 的代码投入商业使用，由此造成的后果和法律责任均与本人无关。 
