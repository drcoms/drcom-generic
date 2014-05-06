login包服务器返回错误类型 (发送序号为03的包后）<br>
> 05000005XX00...
> v33 = \*(_BYTE \*)(v46 + 4);
v46是服务器传回来的包的地址，（由之前函数得出），看出来v33对应 Dst[4] 即XX的位置<br>


XX是错误编号，对应下面的a2

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
* 其他都会提示账号密码错误

来源 0.8 u64的客户端

```

//----- (0043FB47) --------------------------------------------------------
int __cdecl sub_43FB47(int a1, signed int a2)
{
  int v2; // eax@2
  char *v3; // eax@3
  char *v4; // eax@4
  char *v5; // eax@6
  char *v6; // eax@7
  char *v7; // eax@10
  char *v8; // eax@11
  char *v9; // eax@14
  char *v10; // ST20_4@15
  char *v11; // eax@15
  char *v12; // eax@18
  int v13; // ST20_4@19
  int v14; // ST1C_4@19
  int v15; // ST18_4@19
  int v16; // ST14_4@19
  int v17; // ST10_4@19
  int v18; // ST0C_4@19
  char *v19; // eax@19
  char *v20; // eax@21
  char *v21; // eax@23
  char *v22; // ST20_4@27
  char *v23; // eax@27
  char *v24; // eax@28
  char *v25; // eax@33
  char *v26; // eax@35
  char *v27; // eax@36
  int v28; // ST20_4@37
  char *v29; // eax@37
  char *v30; // eax@38
  char *v31; // eax@39
  int v33; // [sp+4h] [bp-E9Ch]@1
  const char *v34; // [sp+8h] [bp-E98h]@29
  char Dst; // [sp+10h] [bp-E90h]@26
  char v36; // [sp+11h] [bp-E8Fh]@26
  __int16 v37; // [sp+20Dh] [bp-C93h]@26
  char v38; // [sp+20Fh] [bp-C91h]@26
  int i; // [sp+210h] [bp-C90h]@21
  int v40; // [sp+214h] [bp-C8Ch]@1
  char v41; // [sp+218h] [bp-C88h]@1
  char v42; // [sp+219h] [bp-C87h]@1
  __int16 v43; // [sp+855h] [bp-64Bh]@1
  char v44; // [sp+857h] [bp-649h]@1
  int v45; // [sp+858h] [bp-648h]@1
  int v46; // [sp+85Ch] [bp-644h]@1
  char Dest; // [sp+860h] [bp-640h]@1
  char v48; // [sp+861h] [bp-63Fh]@1
  __int16 v49; // [sp+E9Dh] [bp-3h]@1
  char v50; // [sp+E9Fh] [bp-1h]@1

  v45 = 541283667;
  v46 = a1;
  Dest = 0;
  memset(&v48, 0, 0x63Cu);
  v49 = 0;
  v50 = 0;
  v41 = 0;
  memset(&v42, 0, 0x63Cu);
  v43 = 0;
  v44 = 0;
  v40 = 0;
  sub_438787(0);
  memset(&Dest, 0, 0x640u);
  v33 = *(_BYTE *)(v46 + 4);
  switch ( v33 )
  {
    case 1:
      v2 = sub_43F9A2(v46);
      _snprintf(&Dest, 0x63Fu, "%s", v2);
      break;
    case 2:
      v3 = sub_4397FF("服务器繁忙，请稍候重新登录！！！");
      _snprintf(&Dest, 0x63Fu, v3);
      break;
    case 3:
      v4 = sub_4397FF("帐号或密码错误，请检查后重新登录！！！");
      _snprintf(&Dest, 0x63Fu, v4);
      break;
    case 4:
      if ( a2 >= 10 )
      {
        v6 = sub_4397FF("费用已超支，不能使用需要收费的网络资源！！！");
        _snprintf(&Dest, 0x63Fu, v6);
      }
      else
      {
        v5 = sub_4397FF("本帐号的累计时间或流量已超出限制，不能使用！！！");
        _snprintf(&Dest, 0x63Fu, v5);
      }
      v40 = 1;
      break;
    case 5:
      if ( a2 >= 6 )
      {
        v8 = sub_4397FF("本帐号的期限已到，不能使用！！！");
        _snprintf(&Dest, 0x63Fu, v8);
      }
      else
      {
        v7 = sub_4397FF("本帐号暂停使用");
        _snprintf(&Dest, 0x63Fu, v7);
      }
      break;
    case 7:
      if ( a2 >= 9 )
      {
        v10 = sub_445FF7(*(struct in_addr *)(v46 + 5));
        v11 = sub_4397FF("IP地址不匹配，本帐号只能在指定IP地址(%s)上使用！！！");
        _snprintf(&Dest, 0x63Fu, v11, v10);
      }
      else
      {
        v9 = sub_4397FF("IP地址不匹配，本帐号只能在指定IP地址上使用！！！");
        _snprintf(&Dest, 0x63Fu, v9);
      }
      break;
    case 11:
      if ( a2 >= 11 )
      {
        v13 = *(_BYTE *)(v46 + 10);
        v14 = *(_BYTE *)(v46 + 9);
        v15 = *(_BYTE *)(v46 + 8);
        v16 = *(_BYTE *)(v46 + 7);
        v17 = *(_BYTE *)(v46 + 6);
        v18 = *(_BYTE *)(v46 + 5);
        v19 = sub_4397FF("MAC(物理)地址不匹配，本帐号只能在指定的IP和MAC(物理)地址(%02X-%02X-%02X-%02X-%02X-%02X)上使用！！！");
        _snprintf(&Dest, 0x63Fu, v19, v18, v17, v16, v15, v14, v13);
      }
      else
      {
        v12 = sub_4397FF("MAC(物理)地址不匹配，本帐号只能在指定的IP和MAC(物理)地址上使用！！！");
        _snprintf(&Dest, 0x63Fu, v12);
      }
      break;
    case 20:
      v20 = sub_4397FF("本帐IP地址太多！！！");
      _snprintf(&Dest, 0x63Fu, v20);
      for ( i = 0; i < *((_DWORD *)dword_54903C + 116); ++i )
      {
        v21 = sub_445FF7(*((struct in_addr *)dword_54903C + i + 117));
        strcat(&Dest, v21);
        strcat(&Dest, L"#");
      }
      break;
    case 21:
      if ( a2 <= 20 )
      {
        v25 = sub_4397FF("客户端版本不正确，请下载升级包升级客户端！！！");
        _snprintf(&Dest, 0x63Fu, v25);
      }
      else
      {
        Dst = 0;
        memset(&v36, 0, 0x1FCu);
        v37 = 0;
        v38 = 0;
        memcpy(&Dst, (const void *)(a1 + 20), a2 - 20);
        if ( strlen(&Dst) )
        {
          v22 = sub_4397FF(&Dst);
          v23 = sub_4397FF("客户端认证失败 : %s");
          _snprintf(&Dest, 0x63Fu, v23, v22);
        }
        else
        {
          v24 = sub_4397FF("客户端版本不正确，请下载升级包升级客户端！！！");
          _snprintf(&Dest, 0x63Fu, v24);
        }
        v34 = (const char *)(strlen(&Dst) + 21 + a1);
        if ( strlen(v34) > 4 )
        {
          if ( strlen(v34) < 0xB4 )
          {
            memset(&v41, 0, 0x640u);
            _snprintf(&v41, 0x63Fu, "%s", v34);
          }
        }
      }
      break;
    case 22:
      v26 = sub_4397FF("本帐号只能在指定的Mac和IP上使用！！！");
      _snprintf(&Dest, 0x63Fu, v26);
      break;
    case 23:
      v27 = sub_4397FF("你的PC设置了静态IP,请改为动态获取方式(DHCP),然后重新登录！！！");
      _snprintf(&Dest, 0x63Fu, v27);
      break;
    case 24:
    case 25:
    case 26:
    case 27:
    case 28:
      v28 = *(_BYTE *)(v46 + 4);
      v29 = sub_4397FF("LOGIN ERROR Error code(%02X).");
      sub_43830C(v29, v28);
      break;
    default:
      sub_438787(v33 - 1);
      v30 = sub_4397FF("帐号或密码错误，请检查后重新登录！！！");
      _snprintf(&Dest, 0x63Fu, v30);
      break;
  }
  v31 = sub_4397FF("LOGIN ERROR: %s");
  sub_43830C(v31, &Dest);
  sub_43D739(0, (int)&Dest);
  if ( strlen(&v41) )
    v45 = sub_43B1AF((int)"SYM URL ", (int)&v41);
  if ( (*((_DWORD *)::Dst + 50) & 0x10) != 0 )
    sub_44F484();
  return v45;
}

```
