心跳包
---------------

```c
//  <===
struct  _tagServerKeepAlive
{
    unsigned char Code;
    unsigned char SubCode;
    unsigned short PlusWord;
    unsigned char AllowMaxIPNum;
    unsigned char Data[13];
};
```

返回：
```c
//  ===>
struct  _tagHostReplayServerAlive
{
    unsigned char Code;
    unsigned char Digest;
    unsigned char HostIpNum;
    unsigned char KeepReplayMd5[MD5_LEN];
    unsigned char unknow3;
    struct _tagDrcomDogData DogData;
};
```
