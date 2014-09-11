登陆过程
--------------
按顺序

challenge包：
```c
struct  _tagChallenge
{
    unsigned char code;
    unsigned char ChallengeID;      // ID 每发送一次，累加
    unsigned short ChallengeRandomID;   // 发送时的毫秒数，其实就是随机数
    unsigned char ClientVerno;
    unsigned char unused[15];
#ifdef DRCOM_ENCRYPT_PROTO
    unsigned char encrypt_info[32];
#endif
};
```

服务器返回包：
```c
struct  _tagReturnChallenge
{
    unsigned char code;
    unsigned char ChallengeID;      // 返回Challenge 发送的ID
    unsigned short ChallengeRandomID;   // 返回Challenge 发送的ID
    unsigned char ChallengeSeed[SEED_LEN];
    unsigned short AuthTypeSele; //WORD seleA;//authtypesele
    unsigned short DeviceVer;
    unsigned short DeviceKernelVer;
    unsigned short AdminTcpPort;
    unsigned int DhcpsServerIP;
    unsigned int HostIP;
    unsigned short HostPort;

    unsigned char MyDllHeader[16];
    unsigned short SystemAuthOption;//b(0-3)=systemInitPara.mainv6mode, b4-14 unuse, b(15)==1为4步心跳
    unsigned long MainServerV6IP[4];
    unsigned long HostV6IP[4];

#ifdef DRCOM_ENCRYPT_PROTO
    unsigned char unused[4];
    unsigned char encrypt_info[32];
#endif
};
```

登陆包：

```c
struct  _tagLoginPacket
{
    struct _tagDrCOMHeader Header;
    unsigned char PasswordMd5[MD5_LEN];
    char Account[ACCOUNT_MAX_LEN];
    unsigned char ControlCheckStatus;
    unsigned char AdapterNum;
    unsigned char MacAddrXORPasswordMD5[MAC_LEN];
    unsigned char PasswordMd5_2[MD5_LEN];
    unsigned char HostIpNum;
    unsigned int HostIPList[HOST_MAX_IP_NUM];
    unsigned char HalfMD5[8];
    unsigned char DogFlag;
    unsigned int unkown2;
    struct _tagHostInfo HostInfo;
    unsigned char ClientVerInfoAndInternetMode;
    unsigned char DogVersion;
};
```
