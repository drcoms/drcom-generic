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


PKT3包的构造：
```c
//----- (0805E52B) --------------------------------------------------------
int __usercall DrcomDialExtProtoSendLoginPacket<eax>(int a1<esi>)
{
  int v1; // edi@1
  int v2; // edi@1
  char v3; // dl@1
  int v4; // eax@1
  int v5; // eax@1
  int v6; // eax@1
  int v7; // eax@1
  int v8; // eax@3
  int v9; // edx@6
  int v10; // eax@6
  int v11; // edx@10
  int v12; // eax@12
  int v13; // eax@16
  int v14; // ebx@17
  int v15; // eax@17
  int v16; // edx@18
  int v17; // ebx@18
  int v18; // eax@18
  int v19; // eax@19
  char v21; // [sp+4h] [bp-244h]@19
  int v22; // [sp+18h] [bp-230h]@12
  char v23; // [sp+28h] [bp-220h]@1
  int v24; // [sp+48h] [bp-200h]@1
  int v25; // [sp+228h] [bp-20h]@1
  int *v26; // [sp+22Ch] [bp-1Ch]@1
  unsigned __int8 v27; // [sp+233h] [bp-15h]@1
  unsigned int i; // [sp+234h] [bp-14h]@21
  int *v29; // [sp+238h] [bp-10h]@21

  v25 = (int)&v23;
  v26 = &v24;
  v27 = DRCOM_CLIENT_KERNEL_VER;
  memset(&v23, 0, 0x200u); // 缓冲区 512 字节
  v1 = v25;
  memset((void *)v25, 0, 0x20u); // 先看前32个字节
  v2 = v1 + 32;
  // 正式开始
  *(_BYTE *)v25 = 7; // 07
  v3 = as[160];
  *(_BYTE *)(v25 + 1) = as[160]; // 心跳次数 对应 56 ，这里应是pkt1的序数+1 
  as[160] = v3 + 1;
  *(_BYTE *)(v25 + 4) = 3; // 对应 [+4]的 03
  v4 = v25 + 6; // v4 = [+6]
  *(_DWORD *)(v25 + 6) = 0; // 4个字节全0 [+6]
  *(_WORD *)(v4 + 4) = 0; //对应ac 15前的00 00
  *(_DWORD *)(v25 + 12) = *(_DWORD *)&as[204]; // as[204]内容见下面分析, ac 15 05  0f
  *(_DWORD *)(v25 + 16) = 512; //0x0200 -> 00 00 02 00 【后面会对这个内容修改】最终结果是00 62 00 14
  *(_DWORD *)(v25 + 20) = *(_DWORD *)&as[164]; //as[164]是上个包的[+8-+11]的部分即 cf 89 a8 03
  *(_DWORD *)(v25 + 24) = 20000711; //0x01312fc7   现在是 66 cc 58 2f，估计是对前32个字节做个CRC，然后再覆盖这段内容【后面会对这个内容修改】
  *(_DWORD *)(v25 + 28) = 126; // 0x7e （一会会变成一堆0）
  *(_BYTE *)(v25 + 5) = 0; // [+5] = 00
  *(_WORD *)(v25 + 2) = *(_BYTE *)(v25 + 5) + 96; // 前面为0所以是0x60 -> 60 00 ，这个就是 [+2][+3]的60 00，应该表示的是包的长度
  
  v5 = (int)((char *)v26 + *(_BYTE *)(v25 + 5)); //v5是地址计算，不管，是后面那一坨莫名其妙的东西
  // 上面是32个字节的验证信息
  // 下面是64个字节的某些玩意，个人认为可以全部设为0
  // 加起来正好96字节
  *(_DWORD *)v5 = *(_DWORD *)&as[576];
  *(_DWORD *)(v5 + 4) = *(_DWORD *)&as[580];
  *(_DWORD *)(v5 + 8) = *(_DWORD *)&as[584];
  *(_DWORD *)(v5 + 12) = *(_DWORD *)&as[588];
  *(_DWORD *)(v5 + 16) = *(_DWORD *)&as[592];
  *(_DWORD *)(v5 + 20) = *(_DWORD *)&as[596];
  *(_DWORD *)(v5 + 24) = *(_DWORD *)&as[600];
  *(_DWORD *)(v5 + 28) = *(_DWORD *)&as[604];
  *(_DWORD *)(v5 + 32) = *(_DWORD *)&as[608];
  *(_DWORD *)(v5 + 36) = *(_DWORD *)&as[612];
  *(_DWORD *)(v5 + 40) = *(_DWORD *)&as[616];
  *(_DWORD *)(v5 + 44) = *(_DWORD *)&as[620];
  *(_DWORD *)(v5 + 48) = *(_DWORD *)&as[624];
  *(_DWORD *)(v5 + 52) = *(_DWORD *)&as[628];
  *(_DWORD *)(v5 + 56) = *(_DWORD *)&as[632];
  *(_DWORD *)(v5 + 60) = *(_DWORD *)&as[636];
  
  
  // 一些配置信息，意义不大，__start__
  AntiProxyModule_Call(v2, a1, 9);
  v6 = *(_DWORD *)&drcfg[304];
  DebugMessage(
    (unsigned int)"IS_CONFIG_PPPOE_USE_DRCOM_966_SERVER=%d\nas.DrcomPPPoEAuthRetry966Kern=%d\nAntiProxyModule_Call(DRCOMDLL_CHECK_IS_LOADED)=%d\n",
    (v6 & 0x40000) != 0);
  v7 = *(_DWORD *)&drcfg[304];
  // 一些配置信息，意义不大，__end__
  
  
  if ( (v7 & 0x40000 || *(_DWORD *)&as[680]) && ((v8 = *(_DWORD *)&drcfg[304], !(v8 & 0x40000)) || !*(_DWORD *)&as[680])
    || AntiProxyModule_Call(v2, a1, 9) != 541283667 )
  {
    /*
      巴拉巴拉以后 512 += 24, v27 = DRCOM_CLIENT_KERNEL_VER;,这个版本号在log_version_info()找到，对固定版本是定值
    */
    *(_DWORD *)(v25 + 16) += v27 << 24;
  }
  else
  {
    // 样本对应的是这个分支
    v9 = *(_DWORD *)(v25 + 16);
    // v9 = 512
    BYTE1(v9) |= 0x62u; // 可能的意思是取第v9的第一个字节00 00 02 00的 00 00 然后这个字节或上0x0062
    *(_DWORD *)(v25 + 16) = v9;
    v10 = *(_DWORD *)&drcfg[304];
    if ( !(v10 & 0x80000) )
      *(_DWORD *)(v25 + 16) += v27 << 24;
  }
  // 反正结果是00 62 00 14
  
  if ( *(_DWORD *)&as[676] )
  {
    v11 = *(_DWORD *)(v25 + 16);
    BYTE1(v11) |= 0x80u;
    *(_DWORD *)(v25 + 16) = v11;
  }
  // 下面这段是报告
  if ( *(_DWORD *)&as[676] <= 5u )
  {
    DebugMessage((unsigned int)"as.IsDrcomDialConnectionFirstActive=%d\n", as[668]);
    if ( *(_DWORD *)&as[668] && *(_DWORD *)&as[672] )
    {
      if ( !*(_DWORD *)&as[552] )
      {
        v13 = drlang_get_lang((int)&unk_80FCFD4);
        SendMessageToUI(a1, (int)"STM ", v13);
      }
      v14 = *(_DWORD *)(v25 + 16);
      v15 = drlang_get_lang((int)"Dr.COM PPPoE start connect %08X.");
      DebugMessage(v15, v14);
    }
    else
    {
      v16 = *(_DWORD *)(v25 + 16);
      BYTE1(v16) |= 1u;
      *(_DWORD *)(v25 + 16) = v16;
      v17 = *(_DWORD *)(v25 + 16);
      v18 = drlang_get_lang((int)"Dr.COM PPPoE start onlineing %08X.");
      DebugMessage(v18, v17);
    }
    
    
    v19 = DrcomCRC32(0, v25, *(_WORD *)(v25 + 2)); //v25 + 2对应的是包的长度96字节,这里是对整个包做一次CRC
    *(_DWORD *)(v25 + 24) = 19680126 * v19; // 19680126*CRC替换掉[+24]的四个字节
    *(_DWORD *)(v25 + 28) = 0; // 就是那个0x7e变成一堆0的情况
    
    // 更新一些全局变量，无关痛痒
    *(_DWORD *)&as[656] = *(_DWORD *)(v25 + 24);
    if ( *(_DWORD *)&as[668] == 1 )
      *(_DWORD *)&as[660] = *(_DWORD *)(v25 + 24);
    i = 0;
    v29 = (int *)((char *)v26 + *(_BYTE *)(v25 + 5));
    
    //下面的东西不影响包的结构，是一些提示信息和日志的更新，没什么意义
    for ( i = 0; i <= 0x3F; ++i )
    {
      a1 = (int)((char *)v29 + i);
      v2 = *((_BYTE *)v29 + i) << (i & 7);
      *((_BYTE *)v29 + i) = v2 + ((signed int)*((_BYTE *)v29 + i) >> (8 - (i & 7)));
    }
    *(_DWORD *)&as[548] = 4;
    *(_DWORD *)&as[24] = 503;
    if ( GetUserStatus(2048) )
      SetUserStatus(512);
    DebugMessage((unsigned int)"Drcom  Dial Ext Proto plugin Send Login CMD.\n", v21);
    v22 = SendAuthCmd(v2, a1);
  }
  else
  {
    v12 = drlang_get_lang((int)&unk_80FCF6C);
    SendMessageToUI(a1, (int)"SYM ERR ", v12);
    v22 = 542265925;
  }
  return v22;
}
```

as[204]
```
signed int __usercall DrcomDialExtProtoHandle_ChallengeRep<eax>(int a1<esi>, int a2, unsigned int a3)
{
  signed int v4; // [sp+14h] [bp-14h]@12

  if ( a3 <= 0xF || *(_BYTE *)a2 != 7 || *(_BYTE *)(a2 + 4) != 2 )
  {
    v4 = 542265925;
  }
  else
  {
    if ( *(_DWORD *)&as[24] == 501 )
    {
      *(_DWORD *)&as[24] = 502;
      *(_DWORD *)&as[204] = *(_DWORD *)(a2 + 12); //上个包[+12-+15] 这里是pkt2的ac 15 05 0f
      *(_DWORD *)&as[976] = 1;
      if ( !*(_DWORD *)&as[116] )
        *(_DWORD *)&as[116] = *(_DWORD *)&as[96];
      if ( !*(_DWORD *)&as[968] )
      {
        *(_DWORD *)&as[968] = *(_DWORD *)&as[116];
        SetServerIP(*(int *)&as[116]);
      }
      *(_DWORD *)&as[164] = *(_DWORD *)(a2 + 8);
      if ( !bAuthIPInfoSended )
      {
        SaveAuthServerIP(*(int *)&as[96]);
        GetHostInfo(a1, 135578028, 1);
        SendLoginStatus(0);
        bAuthIPInfoSended = 1;
      }
      *(_DWORD *)&as[552] = 0;
      DrcomDialExtProtoSendLoginPacket(a1);
    }
    v4 = 541283667;
  }
  return v4;
}
```
