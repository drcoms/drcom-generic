这是windows下0.8 u64对应的DrCOMAuthSendNameAndPassword函数

```
//----- (00451FB7) --------------------------------------------------------
signed int __cdecl sub_451FB7()
{
  signed int result; // eax@2
  int v1; // eax@12
  int v2; // eax@39
  int v3; // eax@39
  size_t v4; // eax@42
  size_t v5; // eax@42
  signed int v6; // [sp+0h] [bp-7A4h]@33
  char *v7; // [sp+4h] [bp-7A0h]@32
  size_t v8; // [sp+8h] [bp-79Ch]@32
  signed int j; // [sp+Ch] [bp-798h]@35
  signed int v10; // [sp+10h] [bp-794h]@10
  char v11; // [sp+14h] [bp-790h]@3
  char v12; // [sp+15h] [bp-78Fh]@12
  char v13; // [sp+16h] [bp-78Eh]@12
  char v14; // [sp+17h] [bp-78Dh]@12
  char v15[16]; // [sp+18h] [bp-78Ch]@12
  char v16; // [sp+28h] [bp-77Ch]@12
  _BYTE v17[8]; // [sp+4Ch] [bp-758h]@12
  char v18; // [sp+54h] [bp-750h]@15
  char v19; // [sp+64h] [bp-740h]@15
  char v20; // [sp+65h] [bp-73Fh]@15
  char v21; // [sp+75h] [bp-72Fh]@15
  char v22; // [sp+76h] [bp-72Eh]@15
  char v23; // [sp+77h] [bp-72Dh]@15
  char v24; // [sp+78h] [bp-72Ch]@15
  char v25; // [sp+7Dh] [bp-727h]@17
  int v26; // [sp+7Eh] [bp-726h]@15
  char v27; // [sp+82h] [bp-722h]@15
  char v28; // [sp+14Ah] [bp-65Ah]@31
  char v29; // [sp+14Bh] [bp-659h]@23
  int len; // [sp+14Ch] [bp-658h]@1
  int v31; // [sp+150h] [bp-654h]@1
  int i; // [sp+154h] [bp-650h]@1
  char buf; // [sp+158h] [bp-64Ch]@10
  char v34; // [sp+159h] [bp-64Bh]@10
  char Dst; // [sp+15Ah] [bp-64Ah]@12
  char v36; // [sp+15Ch] [bp-648h]@42
  char v37; // [sp+15Eh] [bp-646h]@12
  char v38; // [sp+16Ch] [bp-638h]@42
  int v39; // [sp+798h] [bp-Ch]@1
  char *v40; // [sp+79Ch] [bp-8h]@39
  void *Src; // [sp+7A0h] [bp-4h]@1

  v39 = 541283667;
  i = 0;
  len = 0;
  Src = 0;
  LOBYTE(v31) = (unsigned __int8)byte_551164 % 155 + 100;
  if ( *((_DWORD *)dword_54903C + 3) < 203 )
  {
    sub_4412E2((unsigned int *)::Src + 9);
    sub_441098();
    sub_441860(7);
    memset(&v11, 0, 0x138u);
    for ( i = 1; i < *((_DWORD *)dword_54903C + 116); ++i )
    {
      if ( *((_DWORD *)dword_54903C + i + 117) == *((_DWORD *)dword_54903C + 51) )
      {
        *((_DWORD *)dword_54903C + i + 117) = *((_DWORD *)dword_54903C + 117);
        *((_DWORD *)dword_54903C + 117) = *((_DWORD *)dword_54903C + 51);
        break;
      }
    }
    if ( *((_DWORD *)dword_54903C + 117) != *((_DWORD *)dword_54903C + 51) )
      *((_DWORD *)dword_54903C + 117) = *((_DWORD *)dword_54903C + 51);
    *((_DWORD *)dword_54903C + 135) = GetTickCount();
    memset(&buf, 0, 0x640u);
    buf = 3;
    v34 = 1;
    v10 = strlen((const char *)::Src + 36);
    if ( v10 > 16 )
      v10 = 16;
    memcpy(&Dst, (char *)dword_54903C + 164, 4u);
    memcpy(&v37, (char *)::Src + 36, v10);
    len = v10 + 6;
    Src = sub_446840(&buf, v10 + 6);
    memcpy((char *)dword_54903C + 128, Src, 0x10u);
    v11 = 3;
    v12 = 1;
    v13 = 0;
    v14 = strlen((const char *)::Src) + 20;
    memcpy(v15, (char *)dword_54903C + 128, 0x10u);
    memcpy(&v16, ::Src, 0x24u);
    v17[0] = *((_BYTE *)dword_54903C + 562);
    v1 = sub_438787((int)dword_54903C);
    sub_438787(v1);
    sub_438787((int)dword_54903C);
    v17[1] = *((_BYTE *)dword_54903C + 161);
    for ( i = 0; i < 6; ++i )
      v17[i + 2] = *((_BYTE *)dword_54903C + i + 128) ^ *((_BYTE *)dword_54903C + i + 232);
    memset(&buf, 0, 0x640u);
    buf = 1;
    memcpy(&v34, (char *)::Src + 36, v10);
    memcpy(&v34 + v10, (char *)dword_54903C + 164, 4u);
    len = v10 + 9;
    Src = sub_446840(&buf, v10 + 9);
    memcpy(&v18, Src, 0x10u);
    v19 = *((_BYTE *)dword_54903C + 464);
    memcpy(&v20, (char *)dword_54903C + 468, 0x10u);
    v21 = 20;
    v22 = 0;
    v23 = 7;
    v24 = 11;
    len = 101;
    Src = sub_446840(&v11, 0x65u);
    memcpy(&v21, Src, 8u);
    v26 = 0;
    memcpy(&v27, (char *)dword_54903C + 264, 0xC8u);
    if ( *((_DWORD *)::Dst + 49) == 4 )
    {
      if ( sub_441860(7) == 541283667 )
      {
        v25 = 1;
        sub_438787(541283667);
      }
      else
      {
        LOBYTE(v31) = 2;
      }
    }
    if ( *((_DWORD *)::Dst + 49) == 1 || *((_DWORD *)::Dst + 49) == 8 || *((_DWORD *)::Dst + 49) == 2 )
    {
      if ( sub_4458F3() )
      {
        v25 = 1;
        v29 = 32 * (dword_549FA4 & 7) + ((dword_549FA4 >> 3) & 0x1F);
      }
      else
      {
        v25 = 0;
      }
    }
    if ( !*((_DWORD *)dword_54903C + 769) )
    {
      if ( *((_BYTE *)dword_54903C + 562) & 0x60 )
      {
        if ( sub_44133A(";chinanet_type;") )
        {
          byte_549FA0 = 0;
        }
        else
        {
          if ( sub_44133A(";double_ext;") )
            byte_549FA0 = 1;
        }
      }
    }
    v28 = (byte_549FA0 << 7) | v31;
    memset(&buf, 0, 0x640u);
    len = 312;
    memcpy(&buf, &v11, 0x138u);
    if ( *((_WORD *)dword_54903C + 126) )
    {
      v7 = &buf + len;
      v8 = strlen((const char *)::Src + 36);
      if ( (signed int)v8 <= 16 )
        v6 = v8;
      else
        v6 = 16;
      *v7 = 0;
      v7[1] = v6;
      for ( j = 0; j < v6; ++j )
      {
        v7[j + 2] = v15[j] ^ *((_BYTE *)::Src + j + 36);
        v7[j + 2] = ((signed int)(unsigned __int8)v7[j + 2] >> 5) + 8 * v7[j + 2];
      }
      len = len + 18 - (16 - v6);
    }
    v40 = &buf + len;
    *(&buf + len) = 2;
    v40[1] = 12;
    *(_DWORD *)(v40 + 2) = 285681153;
    *((_WORD *)v40 + 3) = byte_549FA8;
    memcpy(v40 + 8, (char *)dword_54903C + 232, 6u);
    len += 14;
    len = 4 * (len + 3) / 4;
    v2 = sub_439068(1234, (int)&buf, len);
    *(_DWORD *)(v40 + 2) = 1968 * v2;
    v3 = (int)sub_4397FF("发送帐号密码......\n");
    sub_438787(v3);
    *((_DWORD *)dword_54903C + 3) = 203;
    sub_44F640(16);
    dword_54F200 = *((_DWORD *)dword_54903C + 12);
    ::len = len;
    memcpy(byte_54F208, &buf, len);
    *((_DWORD *)dword_54903C + 135) = GetTickCount();
    if ( *((_DWORD *)::Dst + 49) == 4 )
      v39 = sub_441860(6);
    else
      v39 = sub_44084E(&buf, len);
    v4 = strlen((const char *)::Src + 36);
    memcpy(&v38, (char *)::Src + 36, v4);
    v5 = strlen((const char *)::Src + 36);
    Src = sub_446840(&v36, v5 + 16);
    memcpy((char *)dword_54903C + 144, Src, 0x10u);
    sub_44129D((int)((char *)::Src + 36));
    result = v39;
  }
  else
  {
    result = 541283667;
  }
  return result;
}
```