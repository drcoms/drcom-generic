有关PPPOE之后的扩展认证
----------------------
状态
 - [X] 完成分析
 - [ ] 验证正确性
 - [ ] 编写代码
 - [ ] 实际测试通过

心跳分两部分，一个是正常心跳（07心跳），和目前已有算法一样，一个是pppoe的心跳，两者独立运行，注意要去掉ff开头的那个心跳换成pppoe心跳<br>
pppoe心跳分析如下

pppoe心跳
正常心跳
（以上总共20s)

pppoe心跳
正常心跳

其中有关正常心跳的tail部分继承上一个正常心跳的，和pppoe心跳无关

[send]PKT1:<br>
```
0000   07 55 08 00 01 00 00 00
07心跳，登陆次数为55，类型为 08 00 01 00
```

[recv]PKT2:<br>
```
07 // header.code
55 // header.id
10 00 // header.length
02 // header.type
00 00 00 // other[3] other[0]确定加密方式，0为不加密
cf 89 a8 03 // ChallengeSeed[4]
ac 15 05 0f // ClientSouIp
a8 a4 00 00 3a ae 6f 3c 00 00 00 00 d8 02 00 00
```

[send]PKT3:<br>
```
07 //header.code
56 //header.id
60 00 //header.length
03 //header.type
00 //uid length (strlen(us.Account))
00 00 00 00 00 00 //mac
ac 15 05 0f // AuthHostIP
00 62 00 14 // option, 第一次发送是这个，第二次则是 00 63 00 14 (0x14006300)
/*
 校验位unsigned long pCrcBuff生成，不加密则是初始化为 [0]:DRCOM_DIAL_EXT_PROTO_CRC_INIT(0x01312fc7) 126(0x0000007e)
*/
cf 89 a8 03 66 cc 58 2f


00 00 00 00

//_tagDrcomDialExtProtoNetWorkInfo
//基本格式

00 00 00 00 00 00 // mac
00 //netmark
8b //type
ac 2a 14 78 //sip
ff ff ff ff //smask
//下同
00 a0 59 06 00 20 00 03 c0 51 25 08 ff ff ff 00 
00 a0 59 06 00 01 00 03 c0 51 2b 08 ff ff ff 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
```

[recv]PKT4:<br>
```
0000   07 56 30 00 04 00 20 00 19 33 d6 8b 00 00 00 00
0010   44 39 d8 ed ca c0 f7 46 a9 86 2b a2 50 78 04 d0
0020   b0 82 00 60 00 00 00 00 00 00 00 00 00 00 00 00
```


接下来正常心跳
先发
```
0000   07 00 28 00 0b 01 0f 27 1b 35 00 00 00 00 00 00
0010   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0020   00 00 00 00 00 00 00 00
```

pkt3 校验
旧版本仅做CRC32
新版本则
```c
for (int index = 0; index < pcrcLen; index++)
{
  pcrcstart[index] = (unsigned char)((pcrcstart[index] << (index & 0x07) + (pcrcstart[index] >> (8 - (index & 0x07))));
}
```
