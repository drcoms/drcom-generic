有关PPPOE之后的扩展认证
----------------------
[send]PKT1:<br>
```
0000   07 01 08 00 01 00 00 00
07心跳，登陆次数为1，类型为 08 00 01 00
```

[recv]PKT2:<br>
```
0000   07 55 10 00 02 00 00 00 cf 89 a8 03 ac 15 05 0f
0010   a8 a4 00 00 3a ae 6f 3c 00 00 00 00 d8 02 00 00
```

[send]PKT3:<br>
```
0000   07 56 60 00 03 00 00 00 00 00 00 00 ac 15 05 0f
0010   00 62 00 14 cf 89 a8 03 66 cc 58 2f 00 00 00 00
0020   00 00 00 00 00 00 00 8b ac 2a 14 78 ff ff ff ff
0030   00 a0 59 06 00 20 00 03 c0 51 25 08 ff ff ff 00
0040   00 a0 59 06 00 01 00 03 c0 51 2b 08 ff ff ff 00
0050   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

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
  memset(&v23, 0, 0x200u);
  v1 = v25;
  memset((void *)v25, 0, 0x20u);
  v2 = v1 + 32;
  *(_BYTE *)v25 = 7;
  v3 = as[160];
  *(_BYTE *)(v25 + 1) = as[160];
  as[160] = v3 + 1;
  *(_BYTE *)(v25 + 4) = 3;
  v4 = v25 + 6;
  *(_DWORD *)(v25 + 6) = 0;
  *(_WORD *)(v4 + 4) = 0;
  *(_DWORD *)(v25 + 12) = *(_DWORD *)&as[204];
  *(_DWORD *)(v25 + 16) = 512;
  *(_DWORD *)(v25 + 20) = *(_DWORD *)&as[164];
  *(_DWORD *)(v25 + 24) = 20000711;
  *(_DWORD *)(v25 + 28) = 126;
  *(_BYTE *)(v25 + 5) = 0;
  *(_WORD *)(v25 + 2) = *(_BYTE *)(v25 + 5) + 96;
  v5 = (int)((char *)v26 + *(_BYTE *)(v25 + 5));
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
  AntiProxyModule_Call(v2, a1, 9);
  v6 = *(_DWORD *)&drcfg[304];
  DebugMessage(
    (unsigned int)"IS_CONFIG_PPPOE_USE_DRCOM_966_SERVER=%d\nas.DrcomPPPoEAuthRetry966Kern=%d\nAntiProxyModule_Call(DRCOMDLL_CHECK_IS_LOADED)=%d\n",
    (v6 & 0x40000) != 0);
  v7 = *(_DWORD *)&drcfg[304];
  if ( (v7 & 0x40000 || *(_DWORD *)&as[680]) && ((v8 = *(_DWORD *)&drcfg[304], !(v8 & 0x40000)) || !*(_DWORD *)&as[680])
    || AntiProxyModule_Call(v2, a1, 9) != 541283667 )
  {
    *(_DWORD *)(v25 + 16) += v27 << 24;
  }
  else
  {
    v9 = *(_DWORD *)(v25 + 16);
    BYTE1(v9) |= 0x62u;
    *(_DWORD *)(v25 + 16) = v9;
    v10 = *(_DWORD *)&drcfg[304];
    if ( !(v10 & 0x80000) )
      *(_DWORD *)(v25 + 16) += v27 << 24;
  }
  if ( *(_DWORD *)&as[676] )
  {
    v11 = *(_DWORD *)(v25 + 16);
    BYTE1(v11) |= 0x80u;
    *(_DWORD *)(v25 + 16) = v11;
  }
  if ( *(_DWORD *)&as[676] <= 5u )
  {
    DebugMessage((unsigned int)"as.IsDrcomDialConnectionFirstActive=%d\n", as[668]);
    if ( *(_DWORD *)&as[668] && *(_DWORD *)&as[672] )
    {
      *(_DWORD *)(v25 + 16) = *(_DWORD *)(v25 + 16);
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
    *(_WORD *)(v25 + 2) = 4 * (*(_WORD *)(v25 + 2) + 3) / 4;
    v19 = DrcomCRC32(0, v25, *(_WORD *)(v25 + 2));
    *(_DWORD *)(v25 + 24) = 19680126 * v19;
    *(_DWORD *)(v25 + 28) = 0;
    *(_DWORD *)&as[656] = *(_DWORD *)(v25 + 24);
    if ( *(_DWORD *)&as[668] == 1 )
      *(_DWORD *)&as[660] = *(_DWORD *)(v25 + 24);
    i = 0;
    v29 = (int *)((char *)v26 + *(_BYTE *)(v25 + 5));
    // 下面一段是CRC
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
