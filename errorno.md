登陆错误信息
---------------------
```c
#define AUTH_ERR_CODE_CHECK_MAC         0x01
#define AUTH_ERR_CODE_SERVER_BUSY       0x02
#define AUTH_ERR_CODE_WRONG_PASS        0x03
#define AUTH_ERR_CODE_NOT_ENOUGH        0x04
#define AUTH_ERR_CODE_FREEZE_UP         0x05
#define AUTH_ERR_CODE_NOT_ON_THIS_IP    0x07
#define AUTH_ERR_CODE_NOT_ON_THIS_MAC   0x0B
#define AUTH_ERR_CODE_TOO_MUCH_IP       0x14
#define AUTH_ERR_CODE_UPDATE_CLIENT     0x15
#define AUTH_ERR_CODE_NOT_ON_THIS_IP_MAC    0x16
#define AUTH_ERR_CODE_MUST_USE_DHCP     0x17
#define AUTH_ERR_CODE_24                0x18
#define AUTH_ERR_CODE_25                0x19
#define AUTH_ERR_CODE_26                0x1A
#define AUTH_ERR_CODE_27                0x1B
#define AUTH_ERR_CODE_28                0x1C
```

对应客户端中文提示
* 0x01 有人正在使用这个账号，且是有线的方式
* 0x02 服务器繁忙，请稍候重新登录
* 0x03 帐号或密码错误
* 0x04 本帐号的累计时间或流量已超出限制
* 0x05 本帐号暂停使用
* 0x07 IP地址不匹配，本帐号只能在指定IP地址上使用
* 0x0b MAC(物理)地址不匹配，本帐号只能在指定的IP和MAC(物理)地址上使用
* 0x14 本帐IP地址太多
* 0x15 客户端版本不正确
* 0x16 本帐号只能在指定的Mac和IP上使用
* 0x17 你的PC设置了静态IP,请改为动态获取方式(DHCP),然后重新登录
* 0x18 - 0x1c 保留错误信息
