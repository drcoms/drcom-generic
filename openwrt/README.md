# OpenWrt-Dr.COM

> luci已无人维护，请谨慎使用

当前root文件夹下为D版本，将luci存储的参数实现转换为py文件可获取的格式(默认位置在/etc/config/drcoom.conf下)，增加判断开启与关闭drcom控制脚本，依赖环境依然是python-mini，若手动覆盖安装python-mini后，运行时出现提示libz.so文件确实，请自行寻找并添加到/usr/lib文件夹下，并建立相应的软连接。


这里提供一个NEWIFI-mini的固件，添加python-mini和drcom以及该目录下的LuCI界面(暂包括：K1、K2、niwifi-mini)

* 链接: https://pan.baidu.com/s/1qYaTTgC
* 密码:6sgp

其他版本如果要自行添加可以参照以下方法(以P版本作大体介绍)。


首先修改 `root/usr/lib/lua/luci/model/cbi/drcom.lua`，在末尾处添加

    pppoe_flag = s:option(Value, "pppoe_flag", translate("pppoe_flag"))
    keep_alive2_flag = s:option(Value, "keep_alive2_flag", translate("keep_alive2_flag"))

此处修改是添加必要的参数设置方式。


接下来修改 `root/etc/config/drcom`，在其末尾添加

	option pppoe_flag '\x2a'
	option keep_alive2_flag '\xdc'

此处参数可以不做修改，待调整后在luci图形界面再作相关修改；


接下来修改`root/bin/transdrcom`，在相应末尾部位添加

	tmp_pppoe_flag="pppoe_flag = '$(uci get drcom.@drcom[0].pppoe_flag)'"
	tmp_keep_alive2_flag="keep_alive2_flag = '$(uci get drcom.@drcom[0].keep_alive2_flag)'"
	echo "$tmp_pppoe_flag" >> "$curdir"
	echo "$tmp_keep_alive2_flag" >> "$curdir"

最后将P版本的`latest-wired-pppoe.py`文件移动到`root/bin`文件夹下，并重命名为drcom，修改赋予执行权限。

以上修改完成之后，windows下直接通过winscp上传root目录下文件到根目录覆盖即可；linux下使用scp命令上传覆盖。
