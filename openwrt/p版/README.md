p版python使用教程；

1、
   将三个文件夹拉入root文件夹中，使用 'scp -r 文件夹 /' 命令将三个文件夹覆盖进去。
2、
   修改文件权限为777，右键属性修改。
3、
   拨号：在putty直接粘贴这几条命令：
   #!/bin/sh
   cp /lib/netifd/proto/ppp.sh /lib/netifd/proto/ppp.sh_bak
   sed -i '/proto_run_command/i username=`echo -e "$username"`' /lib/netifd/proto/ppp.sh
   sed -i '/proto_run_command/i password=`echo -e "$password"`' /lib/netifd/proto/ppp.sh
   拨号账号要加上\r\n
4、安装python：
闪存剩余大小低于7.5M，安以下方式安装

   opkg update

   opkg install python-light -d ram

   export PATH=$PATH:/tmp/usr/bin/

   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/tmp/usr/lib/


   将最后两行添加到/etc/profile中，重启路由器，再一次执行
   opkg update    
   opkg install python-lightd
   配置好之后如果drcom不能运行再重新执行  
   opkg update    
   opkg install python-lightd
5、 
   心跳包：wireshark抓包，去https://drcoms.github.io/drcom-generic/  生成心跳包，然后在luci界面填写即可。
6、
   /etc/rc.d/S90drocm是一个链接，可能需要重新建立，右键新建链接，链接到../init.d/drcom即可。
