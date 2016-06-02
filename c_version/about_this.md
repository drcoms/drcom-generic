#dr.com 5.20d for cust/genenal_d
##test v1.3.7
### 作者 qoddi hnczp#icloud.com
这是一个MOD的版本，也就是参考了以下 Latyas latyas#gmail.com 的两部分共同完成的一个版本

派森客户端 https://github.com/drcoms/drcom-generic
jlu-drcom-clienthttps://github.com/drcoms/jlu-drcom-client/

感谢dixyes <dixyes@gmail.com>提供的帮助以及dogecom源码
这个版本理论上适用于绝大多数D版，修改d_generic＝1再改下方配置,当d_general =0时为cust专用

修正LOGIN包对齐问题，修正KL2计数问题,离线测试参数offlinetest，在线使用请置0

整体框架移植包含了KEEP ALIVE 2部分，但是我们学校并不对其进行校验，所以具体工作与否暂未验证,所以目前已经测试的模块包括CLALLANGE SOCKET LOGIN KEEPALIVE1部分

凑合看求别吐槽渣水平

``gcc main.c md5.c -o drcom``