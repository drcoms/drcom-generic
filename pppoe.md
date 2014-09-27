PPPOE
------------------
先给出反编译出来的结果
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

再给出某代码:
```c
/*
 * 第3步,发送认证数据
 */
int DrppoePlugin::DrcomDialExtProtoSendLoginPacket() {
	showLog("jni.DrppoePlugin::DrcomDialExtProtoSendChallenge", "第3步,发送认证数据命令...");
	m_SetpCurrent = SetpSendLogin;
    char drcom_dial_ext_login_buff[512];
    unsigned char aChallenge[SEED_LEN];
    bool bIsCrcCheckHandle = false;

    struct _tagDrcomDialExtProtoLoginPacket* drcom_dial_ext_login
        = (struct _tagDrcomDialExtProtoLoginPacket *)drcom_dial_ext_login_buff;

    unsigned char* ptrExtInfoStart = (unsigned char*)(drcom_dial_ext_login_buff + sizeof(struct _tagDrcomDialExtProtoLoginPacket));
    unsigned char ClientCurrVer = m_sDRCOM_CLIENT_KERNEL_VER;

    bzero(drcom_dial_ext_login_buff, sizeof(drcom_dial_ext_login_buff));

    drcom_dial_ext_login->hcode = AUTH_CODE_PPPOE;
    drcom_dial_ext_login->hid =  m_iChallengeID++;
    drcom_dial_ext_login->htype = AUTH_CODE_TYPE_PPPOE_LOGIN;
    memset(drcom_dial_ext_login->mac, 0, 6);
    drcom_dial_ext_login->sip = m_AuthHostIP;
    drcom_dial_ext_login->option = DRCOM_DIAL_PROTO_OPT_DEFAULT;     //2006-9-1      //0;

    // fgx 2013-03-29 修改第三步的校验方式
    memcpy(drcom_dial_ext_login->ChallengeSeed, m_sChallengeSeed, SEED_LEN);
    bIsCrcCheckHandle = GetCrcCheckField(m_sChallengeSeed, SEED_LEN, m_cEncryptionMode, drcom_dial_ext_login->crc, NULL);

    //us.Accout[0] = 0x00;
    drcom_dial_ext_login->uidlength = 0;//strlen(us.Account);
    drcom_dial_ext_login->hlength = sizeof(struct _tagDrcomDialExtProtoLoginPacket)
                                    + drcom_dial_ext_login->uidlength
                                    + sizeof(struct _tagDrcom8021XExtProtoNetWorkInfo) * MAX_DRCOM_8021X_EXT_PROTO_NET_NUM;

    // add by fgx 2012-07-20
    // 修复上传了 169.254 IP段的问题
    void *temp = NULL;
    {

        struct _tagDrcom8021XExtProtoNetWorkInfo* pNewWorkInfo
            = (struct _tagDrcom8021XExtProtoNetWorkInfo*)ptrExtInfoStart + drcom_dial_ext_login->uidlength;
        showLog("qqqq", "pNewWorkInfo1:%p", pNewWorkInfo);
        for (int index = 0; index < MAX_DRCOM_DIAL_EXT_PROTO_NET_NUM; index++)
        {
            if (!is_dhcp_169_ip_addr(m_DrcomDialExtProtoNetInfo[index].sip))
            {
                memcpy(pNewWorkInfo, m_DrcomDialExtProtoNetInfo + index, sizeof(struct _tagDrcomDialExtProtoNetWorkInfo));
                pNewWorkInfo++;
            }
            if(index == 0) {
            	temp = (void *)pNewWorkInfo;
            	temp = temp + 6;
            	showLog("qqqq", "pNewWorkInfo2:%p temp:%p", pNewWorkInfo, temp);
            }
        }

    }

    if(1) {
    	drcom_dial_ext_login->option = drcom_dial_ext_login->option | DRCOM_DIAL_PROTO_OPT_DRCOMDLL_CHECK;
    	if(1) {
    		// 大部分内核版本需要上传版本号，只有少数不需要
    		drcom_dial_ext_login->option = drcom_dial_ext_login->option
    	                                           + (DRCOM_DIAL_PROTO_OPT_ANTI_CLIENT_VER * ClientCurrVer);
    	}
    }
    else {
        drcom_dial_ext_login->option = drcom_dial_ext_login->option
                                       + (DRCOM_DIAL_PROTO_OPT_ANTI_CLIENT_VER * ClientCurrVer);
    }

    if (m_uiAntiProxyResault != 0x00) //2007-11-22
    {
        // pppoe发现代理网关将其踢下线
        drcom_dial_ext_login->option = drcom_dial_ext_login->option | DRCOM_DIAL_PROTO_OPT_ANTI_PROXY_OFFLINE;
    }

    if (m_uiAntiProxyResault > 5)
    {
    	// 请停止使用路由器或代理软件上网,并重新登录，谢谢合作!!!
        return DRCOM_ERR;
    }

    if (m_bIsFirstTimeConnect) {
    	drcom_dial_ext_login->option = drcom_dial_ext_login->option | DRCOM_DIAL_PROTO_OPT_CONNECTION_START;
    	drcom_dial_ext_login->option = 0x1d006200;
    }
    else {
    	drcom_dial_ext_login->option = drcom_dial_ext_login->option | DRCOM_DIAL_PROTO_OPT_CONNECTION_ONLINEING;
    	drcom_dial_ext_login->option = 0x1d006300;
    }

    if (!bIsCrcCheckHandle){
        // 旧版本
        drcom_dial_ext_login->hlength = ((drcom_dial_ext_login->hlength + 3) / 4) * 4;
        drcom_dial_ext_login->crc[0] = DRCOM_DIAL_EXT_PROTO_CRC_CONST *
                                       DrcomCRC32(0, (unsigned char*)drcom_dial_ext_login, drcom_dial_ext_login->hlength);
        drcom_dial_ext_login->crc[1] = 0;
    }

    m_ulDrcomDialExtProtoAuthLastCRC = drcom_dial_ext_login->crc[0];

    if (m_iIsDrcomDialConnectionFirstActive == 0x01) {
    	m_iDrcomDialExtProtoActiveCRC = drcom_dial_ext_login->crc[0];
    }

	int index = 0;
	unsigned char* pcrcstart = (unsigned char*)(ptrExtInfoStart + drcom_dial_ext_login->uidlength); //&drcom_dial_ext_login->netinfo;

	int pcrcLen = (sizeof(struct _tagDrcomDialExtProtoNetWorkInfo) * MAX_DRCOM_DIAL_EXT_PROTO_NET_NUM);
	string log = Arithmetic::AsciiToHexWithSep((const char*)pcrcstart, pcrcLen);
	showLog("jni.DrppoePlugin::DrcomDialExtProtoSendChallenge", "pcrcstart:(%d)加密前 Hex编码:\n%s", pcrcLen, log.c_str());


	for (index = 0; index < pcrcLen; index++)
	{
		pcrcstart[index] =
			(unsigned char)((pcrcstart[index] << (index & 0x07))
							+ (pcrcstart[index] >> (8 - (index & 0x07))));
	}

	log = Arithmetic::AsciiToHexWithSep((const char*)pcrcstart, pcrcLen);
	showLog("jni.DrppoePlugin::DrcomDialExtProtoSendChallenge", "pcrcstart:(%d)加密后 Hex编码:\n%s", pcrcLen, log.c_str());

	if(NULL !=  temp) {
	    char a = 0x40;
	    memcpy((void *)temp, &a, sizeof(a));
	}

	// 正在向服务器确认IP地址,请稍后.....
    return SendAuthCmd((char *)drcom_dial_ext_login, drcom_dial_ext_login->hlength);
}
```

以下是某代码的头文件

```c
typedef struct _tagDrcomDialExtProtoHeader
{
    unsigned char code;
    unsigned char id;
    unsigned short length;
    unsigned char type;
} PPPOEHEADER;
```

发起认证请求：

```c
typedef struct _tagDrcomDialExtProtoChallenge {
    PPPOEHEADER header;
    unsigned char other[3];

#define hcode   header.code     //=7
#define hid     header.id
#define hlength header.length
#define htype   header.type     //=1

#ifdef DRCOM_ENCRYPT_PROTO
    unsigned char unused[12];
    unsigned char encrypt_info[32];
#endif
} PPPOECHALLENGE;
#define _tagDrcom8021XExtProtoChallenge _tagDrcomDialExtProtoChallenge
```

回应请求:
```c
struct _tagDrcomDialExtProtoReturnChallenge {
    PPPOEHEADER header;

#define hcode   header.code     //=7
#define hid     header.id
#define hlength header.length
#define htype   header.type     //=2
    unsigned char other[3];
    unsigned char challenge[SEED_LEN];

#ifdef DRCOM_ENCRYPT_PROTO
unsigned char unused[20+48];
unsigned char encrypt_info[32];
#endif
};

```

附加网络信息部分：
```c
#define  _tagDrcom8021XExtProtoReturnChallenge _tagDrcomDialExtProtoReturnChallenge
#define MAX_DRCOM_DIAL_EXT_PROTO_NET_NUM 4
#define MAX_DRCOM_8021X_EXT_PROTO_NET_NUM MAX_DRCOM_DIAL_EXT_PROTO_NET_NUM
#define USE_LIMIT_IP (unsigned long)(169+254*256)

struct _tagDrcomDialExtProtoNetWorkInfo
{
    unsigned char mac[6];
    unsigned char netmark;      //dhcp mark
    unsigned char type;     //interface type(ether,ppp)
    unsigned long sip;
    unsigned long smask;
    //ULONG gateway1;
};

#define _tagDrcom8021XExtProtoNetWorkInfo _tagDrcomDialExtProtoNetWorkInfo
```


发起认证：
```c
struct _tagDrcomDialExtProtoLoginPacket {
    PPPOEHEADER header; // 5 byte

#define hcode   header.code     // PPPoE ext = 0x07
#define hid     header.id		// 自定义，每次不同就可以
#define hlength header.length	// 发送数据包的长度
#define htype   header.type     // PPPoE = 0x03

    unsigned char uidlength;
    unsigned char mac[6];
    unsigned long sip;
    unsigned long option;   //bit0=dhcp, bit1=请求封装, bit2-7(verno)
    //b8=(no first),b9=有tcpipdog.dll, b10-12 选择出口线路 2006-12-18
    //b13(mydll mark2007-2-28), bit14-31 unuse
    //b14(mydll mark b15=find proxy cut line (pppoe模式2007-11-22)
    //bit16-31 unuse

    unsigned char ChallengeSeed[SEED_LEN];
    unsigned long crc[2];

    //account ,len 0
    //struct _tagDrcomDialExtProtoNetWorkInfo netinfo[MAX_DRCOM_DIAL_EXT_PROTO_NET_NUM];
    //unsigned char unused[4];
};

#define _tagDrcom8021XExtProtoLoginPacket _tagDrcomDialExtProtoLoginPacket
```


认证结果
```c
struct _tagDrcomDialExtProtoLoginResult {
    PPPOEHEADER header;

#define hcode   header.code     //=7
#define hid     header.id
#define hlength header.length
#define htype   header.type     //4=dvpntable, 6=ping return

    unsigned char   pingsec;
    unsigned short  infolength;
    unsigned long   crc[2];  //type==4 crc[1]=0x01,允许代理 ，kernel
};

```
