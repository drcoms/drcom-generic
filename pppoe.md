PPPOE
------------------
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
