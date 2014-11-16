发第一个82bytes的包（drcom载荷为40bytes）服务器返回一个 File 的函数名
SendNextDownloadModuleFileCmd

```c
int __usercall SendNextDownloadModuleFileCmd<eax>(int a1<esi>, int a2)
{
  int v2; // eax@1
  int v3; // eax@1
  int v4; // eax@15
  int result; // eax@18
  char v6; // [sp+4h] [bp-224h]@14
  char v7; // [sp+20h] [bp-208h]@1
  char v8; // [sp+21h] [bp-207h]@1
  signed __int16 v9; // [sp+22h] [bp-206h]@1
  char v10; // [sp+24h] [bp-204h]@1
  signed __int16 v11; // [sp+26h] [bp-202h]@1
  int v12; // [sp+28h] [bp-200h]@1
  __int64 v13; // [sp+30h] [bp-1F8h]@1
  int v14; // [sp+48h] [bp-1E0h]@18
  char *v15; // [sp+220h] [bp-8h]@1

  v2 = time();
  srandom(v2);
  rand();
  g_RandomIndex = v3;
  memset(&v7, 0, 0x28u);
  v15 = &v7;
  v7 = 7;
  v8 = g_DownLoadReqPacketIndex;
  v12 = v3;
  v9 = 40; //0x0028   28 00
  v10 = 11;//0x0b
  v13 = TMPcode1recExtchalleng;
  v11 = 9999; //0x270f (大端序是 0f 27)
  /*
      举一个常见的例子是
      0f 27 和 dc 02，换成小端序就是 0x270f  0x02dc 27和02对应v15[6], 0f和dc对应v15[7]
  */
  if ( *(_WORD *)&DownloadModuleBuff[12] )
    *((_WORD *)v15 + 3) = *(_WORD *)&DownloadModuleBuff[12];
    //(_WORD *)v15 + 3 就是v15[6]
    //下面会替换
  if ( !a2 )
  {
    g_nStartUpdateCount = 0;
    v15[5] = 1; //0b 01中那个 01
  }
  if ( a2 == 1 )
  {
    *((_DWORD *)v15 + 7) = *(_DWORD *)&as[204];
    v15[5] = 3; //0b 03中那个03，现在分析的是03，所以知a2=1
  }
  /*
      没见过0b 05，忽略
  */
  if ( a2 == 2 )
    v15[5] = 5;
  
  //dc 02 XX XX <= DownloadModuleBuff[4]
  *((_DWORD *)v15 + 3) = *(_DWORD *)&DownloadModuleBuff[4];
  
  if ( a2 == 2 ) //a2=1
    *((_WORD *)v15 + 3) = *(_WORD *)&DownloadModuleBuff[12];
  
  //DownloadModuleBuff[12]非0就把DownloadModuleBuff[12]放到dc 02那个位置
  if ( *(_WORD *)&DownloadModuleBuff[12] )
    *((_WORD *)v15 + 3) = *(_WORD *)&DownloadModuleBuff[12];

  if ( v15[5] == 3 ) //=3则要做crc校验
  {
    //v15 + 6*4 = v15[24]正好对应校验段四个字节
    *((_DWORD *)v15 + 6) = MadeCmdPacketCRCSum((int)&v7, *((_WORD *)v15 + 1));
    //第二个参数正好是那个0x0028 就是 40, 就是说对现在的包做一次crc16 * 711 得到的值填充到校验段
    ++g_nStartUpdateCount;
    if ( (unsigned int)g_nStartUpdateCount > 3 )
    {
      v4 = drlang_get_lang((int)"客户端核心模块通信3重试超时，重置状态!!!");
      ErrorMessage(v4, v6);
      g_nStartUpdateCount = 0;
      AntiProxyModuleUpdateStatus = 0;
      g_DownLoadReqPacketIndex = 0;
    }
  }
  if ( g_nModuleOnlineCount == 10 )
  {
    *((_WORD *)v15 + 3) = *(_WORD *)&DownloadModuleBuff[12] - 1;
    g_nModuleOnlineCount = 0;
  }
  result = SendAuthCmd((int)&v14, a1);
  NextUpdateModuleCmdWaitTime = 2;
  return result;
}
```

```c
// PACKET_CRC_CONST = 711
//----- (0805D18C) --------------------------------------------------------
int __cdecl MadeCmdPacketCRCSum(int a1, int a2)
{
  int i; // [sp+0h] [bp-10h]@1
  int v4; // [sp+8h] [bp-8h]@1

  v4 = 0;
  *(_WORD *)(a1 + a2) = 0;
  for ( i = 0; i < (a2 + 1) / 2; ++i )
    v4 ^= *(_WORD *)(a1 + 2 * i);
  return (unsigned __int16)PACKET_CRC_CONST * (unsigned __int16)v4;
}
```
