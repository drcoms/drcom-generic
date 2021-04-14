#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <string>

#include <string>

std::string SALT;

class MD5
{
#define S11 7
#define S12 12
#define S13 17
#define S14 22
#define S21 5
#define S22 9
#define S23 14
#define S24 20
#define S31 4
#define S32 11
#define S33 16
#define S34 23
#define S41 6
#define S42 10
#define S43 15
#define S44 21

public:
  typedef unsigned int size_type; // must be 32bit

  static std::string checkSum(std::string text)
  {
    MD5 pmd5(text);
    return pmd5.getstring();
  }

  MD5() { init(); }
  MD5(const std::string& text) {
    init();
    update((const unsigned char*)text.c_str(), text.length());
    finalize();
  }
  void update(const unsigned char input[], size_type length) {
    // compute number of bytes mod 64
    size_type index = count[0] / 8 % blocksize;

    // Update number of bits
    if ((count[0] += (length << 3)) < (length << 3))
      count[1]++;
    count[1] += (length >> 29);

    // number of bytes we need to fill in buffer
    size_type firstpart = 64 - index;

    size_type i;

    // transform as many times as possible.
    if (length >= firstpart)
    {
      // fill buffer first, transform
      memcpy(&buffer[index], input, firstpart);
      transform(buffer);

      // transform chunks of blocksize (64 bytes)
      for (i = firstpart; i + blocksize <= length; i += blocksize)
        transform(&input[i]);

      index = 0;
    }
    else
      i = 0;

    // buffer remaining input
    memcpy(&buffer[index], &input[i], length - i);
  }
  MD5& finalize() {
    static unsigned char padding[64] = {
      0x80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    };

    if (!finalized) {
      // Save number of bits
      unsigned char bits[8];
      encode(bits, count, 8);

      // pad out to 56 mod 64.
      size_type index = count[0] / 8 % 64;
      size_type padLen = (index < 56) ? (56 - index) : (120 - index);
      update(padding, padLen);

      // Append length (before padding)
      update(bits, 8);

      // Store state in digest
      encode(digest, state, 16);

      // Zeroize sensitive information.
      memset(buffer, 0, sizeof buffer);
      memset(count, 0, sizeof count);

      finalized = true;
    }

    return *this;
  }

  unsigned char* getResult() {
    return  (unsigned char*)this->digest;
  }
  std::string getstring() {
    return std::string((const char*)this->digest, (size_t)16);
  }
private:
  void init() {
    finalized = false;

    count[0] = 0;
    count[1] = 0;

    // load magic initialization constants.
    state[0] = 0x67452301;
    state[1] = 0xefcdab89;
    state[2] = 0x98badcfe;
    state[3] = 0x10325476;
  }
  typedef unsigned char uint1; //  8bit
  typedef unsigned int uint4;  // 32bit
  enum { blocksize = 64 }; // VC6 won't eat a const static int here

  void transform(const uint1 block[blocksize]) {
    uint4 a = state[0], b = state[1], c = state[2], d = state[3], x[16];
    decode(x, block, blocksize);

    /* Round 1 */
    FF(a, b, c, d, x[0], S11, 0xd76aa478); /* 1 */
    FF(d, a, b, c, x[1], S12, 0xe8c7b756); /* 2 */
    FF(c, d, a, b, x[2], S13, 0x242070db); /* 3 */
    FF(b, c, d, a, x[3], S14, 0xc1bdceee); /* 4 */
    FF(a, b, c, d, x[4], S11, 0xf57c0faf); /* 5 */
    FF(d, a, b, c, x[5], S12, 0x4787c62a); /* 6 */
    FF(c, d, a, b, x[6], S13, 0xa8304613); /* 7 */
    FF(b, c, d, a, x[7], S14, 0xfd469501); /* 8 */
    FF(a, b, c, d, x[8], S11, 0x698098d8); /* 9 */
    FF(d, a, b, c, x[9], S12, 0x8b44f7af); /* 10 */
    FF(c, d, a, b, x[10], S13, 0xffff5bb1); /* 11 */
    FF(b, c, d, a, x[11], S14, 0x895cd7be); /* 12 */
    FF(a, b, c, d, x[12], S11, 0x6b901122); /* 13 */
    FF(d, a, b, c, x[13], S12, 0xfd987193); /* 14 */
    FF(c, d, a, b, x[14], S13, 0xa679438e); /* 15 */
    FF(b, c, d, a, x[15], S14, 0x49b40821); /* 16 */

    /* Round 2 */
    GG(a, b, c, d, x[1], S21, 0xf61e2562); /* 17 */
    GG(d, a, b, c, x[6], S22, 0xc040b340); /* 18 */
    GG(c, d, a, b, x[11], S23, 0x265e5a51); /* 19 */
    GG(b, c, d, a, x[0], S24, 0xe9b6c7aa); /* 20 */
    GG(a, b, c, d, x[5], S21, 0xd62f105d); /* 21 */
    GG(d, a, b, c, x[10], S22, 0x2441453); /* 22 */
    GG(c, d, a, b, x[15], S23, 0xd8a1e681); /* 23 */
    GG(b, c, d, a, x[4], S24, 0xe7d3fbc8); /* 24 */
    GG(a, b, c, d, x[9], S21, 0x21e1cde6); /* 25 */
    GG(d, a, b, c, x[14], S22, 0xc33707d6); /* 26 */
    GG(c, d, a, b, x[3], S23, 0xf4d50d87); /* 27 */
    GG(b, c, d, a, x[8], S24, 0x455a14ed); /* 28 */
    GG(a, b, c, d, x[13], S21, 0xa9e3e905); /* 29 */
    GG(d, a, b, c, x[2], S22, 0xfcefa3f8); /* 30 */
    GG(c, d, a, b, x[7], S23, 0x676f02d9); /* 31 */
    GG(b, c, d, a, x[12], S24, 0x8d2a4c8a); /* 32 */

    /* Round 3 */
    HH(a, b, c, d, x[5], S31, 0xfffa3942); /* 33 */
    HH(d, a, b, c, x[8], S32, 0x8771f681); /* 34 */
    HH(c, d, a, b, x[11], S33, 0x6d9d6122); /* 35 */
    HH(b, c, d, a, x[14], S34, 0xfde5380c); /* 36 */
    HH(a, b, c, d, x[1], S31, 0xa4beea44); /* 37 */
    HH(d, a, b, c, x[4], S32, 0x4bdecfa9); /* 38 */
    HH(c, d, a, b, x[7], S33, 0xf6bb4b60); /* 39 */
    HH(b, c, d, a, x[10], S34, 0xbebfbc70); /* 40 */
    HH(a, b, c, d, x[13], S31, 0x289b7ec6); /* 41 */
    HH(d, a, b, c, x[0], S32, 0xeaa127fa); /* 42 */
    HH(c, d, a, b, x[3], S33, 0xd4ef3085); /* 43 */
    HH(b, c, d, a, x[6], S34, 0x4881d05); /* 44 */
    HH(a, b, c, d, x[9], S31, 0xd9d4d039); /* 45 */
    HH(d, a, b, c, x[12], S32, 0xe6db99e5); /* 46 */
    HH(c, d, a, b, x[15], S33, 0x1fa27cf8); /* 47 */
    HH(b, c, d, a, x[2], S34, 0xc4ac5665); /* 48 */

    /* Round 4 */
    II(a, b, c, d, x[0], S41, 0xf4292244); /* 49 */
    II(d, a, b, c, x[7], S42, 0x432aff97); /* 50 */
    II(c, d, a, b, x[14], S43, 0xab9423a7); /* 51 */
    II(b, c, d, a, x[5], S44, 0xfc93a039); /* 52 */
    II(a, b, c, d, x[12], S41, 0x655b59c3); /* 53 */
    II(d, a, b, c, x[3], S42, 0x8f0ccc92); /* 54 */
    II(c, d, a, b, x[10], S43, 0xffeff47d); /* 55 */
    II(b, c, d, a, x[1], S44, 0x85845dd1); /* 56 */
    II(a, b, c, d, x[8], S41, 0x6fa87e4f); /* 57 */
    II(d, a, b, c, x[15], S42, 0xfe2ce6e0); /* 58 */
    II(c, d, a, b, x[6], S43, 0xa3014314); /* 59 */
    II(b, c, d, a, x[13], S44, 0x4e0811a1); /* 60 */
    II(a, b, c, d, x[4], S41, 0xf7537e82); /* 61 */
    II(d, a, b, c, x[11], S42, 0xbd3af235); /* 62 */
    II(c, d, a, b, x[2], S43, 0x2ad7d2bb); /* 63 */
    II(b, c, d, a, x[9], S44, 0xeb86d391); /* 64 */

    state[0] += a;
    state[1] += b;
    state[2] += c;
    state[3] += d;

    // Zeroize sensitive information.
    memset(x, 0, sizeof x);
  }
  static void decode(uint4 output[], const uint1 input[], size_type len) {
    for (unsigned int i = 0, j = 0; j < len; i++, j += 4)
      output[i] = ((uint4)input[j]) | (((uint4)input[j + 1]) << 8) |
      (((uint4)input[j + 2]) << 16) | (((uint4)input[j + 3]) << 24);
  }
  static void encode(uint1 output[], const uint4 input[], size_type len) {
    for (size_type i = 0, j = 0; j < len; i++, j += 4) {
      output[j] = input[i] & 0xff;
      output[j + 1] = (input[i] >> 8) & 0xff;
      output[j + 2] = (input[i] >> 16) & 0xff;
      output[j + 3] = (input[i] >> 24) & 0xff;
    }
  }

  bool finalized;
  uint1 buffer[blocksize]; // bytes that didn't fit in last 64 byte chunk
  uint4 count[2];   // 64bit counter for number of bits (lo, hi)
  uint4 state[4];   // digest so far
  uint1 digest[16]; // the result

  // low level logic operations
  static inline uint4 Fl(uint4 x, uint4 y, uint4 z) {
    return x & y | ~x & z;
  }
  static inline uint4 G(uint4 x, uint4 y, uint4 z) {
    return x & z | y & ~z;
  }
  static inline uint4 H(uint4 x, uint4 y, uint4 z) {
    return x ^ y ^ z;
  }
  static inline uint4 I(uint4 x, uint4 y, uint4 z) {
    return y ^ (x | ~z);
  }
  static inline uint4 rotate_left(uint4 x, int n) {
    return (x << n) | (x >> (32 - n));
  }
  static inline void FF(uint4& a, uint4 b, uint4 c, uint4 d, uint4 x, uint4 s, uint4 ac) {
    a = rotate_left(a + Fl(b, c, d) + x + ac, s) + b;
  }
  static inline void GG(uint4& a, uint4 b, uint4 c, uint4 d, uint4 x, uint4 s, uint4 ac) {
    a = rotate_left(a + G(b, c, d) + x + ac, s) + b;
  }
  static inline void HH(uint4& a, uint4 b, uint4 c, uint4 d, uint4 x, uint4 s, uint4 ac) {
    a = rotate_left(a + H(b, c, d) + x + ac, s) + b;
  }
  static inline void II(uint4& a, uint4 b, uint4 c, uint4 d, uint4 x, uint4 s, uint4 ac) {
    a = rotate_left(a + I(b, c, d) + x + ac, s) + b;
  }

};

std::string hexToString(std::string hexStr)
{
  char hexTabel[] = { '0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f' };
  std::string ret;
  for (auto& e : hexStr)
  {
    ret += hexTabel[((unsigned char)e) / 0x10];
    ret += hexTabel[((unsigned char)e) % 0x10];
  }
  return ret;
}

std::string stringToHex(std::string hexstring)
{
  auto getInt = [](char c)
  {
    char hexTabel[] = { '0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f' };
    for (int i = 0; i < 16; i++)
    {
      if (c == hexTabel[i])
        return i;
    }
  };
  std::string ret;
  for (int i = 0, a; i < hexstring.size(); i += 2)
  {
    a = getInt(hexstring[i]) << 4;
    a += getInt(hexstring[i + 1]);
    ret.append(1, (unsigned char)a);
  }
  return ret;
}

int hexToInt(std::string hexstr)
{
  auto getInt = [](char c)
  {
    char hexTabel[] = { '0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f' };
    for (int i = 0; i < 16; i++)
    {
      if (c == hexTabel[i])
        return i;
    }
  };
  int ret = 0;
  for (int i = 0; i < 4; i++)
    ret += getInt(hexstr[i]) << (28 - (i * 4));
  return ret;
}

long long strToLong(std::string hexstr)
{
  unsigned long long ret = 0;
  int size = hexstr.size() - 1;
  for (int i = 0; i < hexstr.size(); i ++)
  {
    unsigned long long num = (unsigned long long)((unsigned char)hexstr[i]);
    ret += (num) << ((size - i) * 8);
  }
  return ret;
}

class UDPSocket
{
public:
  UDPSocket()
  {
        Udp.begin(61440);
  }
  ~UDPSocket()
  {
  }

  void SendTo(const std::string& address, unsigned short port, const char* buffer, int len)
  {
    Udp.beginPacket(address.c_str(), port);
    Udp.write(buffer, len);
    Udp.endPacket();
  }
  
  bool RecvFrom(char* buffer, int len, int flags = 0)
  {
    long long frq = 0;
    while (frq < 8342363)
    {
      int packetSize = Udp.parsePacket();
      if(packetSize > 0)
      {
        int n = Udp.read(buffer, len);
        buffer[n] = 0;
        return true;
      }
      frq++;
    }
    return false;
  }
private:
  WiFiUDP Udp;
};

struct expand_type {
  template<typename... T>
  expand_type(T&&...) {}
};

template<typename... ArgTypes>
void log(ArgTypes... args)
{
  expand_type{ (  Serial.print(args.c_str()), 0)... };
  Serial.printf("\n");
}


UDPSocket s;

std::string challenge(std::string svr, int ran)
{
    while (1)
    {
      std::string ret;
      std::string send;

      int randNum = ran % 0xffff;
      send.append("\01\02");

      send.append(1, (unsigned char)((randNum << 24) >> 24));
      send.append(1, (unsigned char)(randNum >> 8));

      send.append("\x09");
      send.append(15, (char)0x0);
      s.SendTo(svr, 61440, send.c_str(), send.size());
    
        ret.resize(1024);
        s.RecvFrom((char*)ret.c_str(), ret.length());
        log(std::string("[challenge] recv "), hexToString(ret));
        return ret.substr(4, 4);
    }
    return std::string();
}

std::string dump(long long n)
{
  std::string ret;
  bool start = 0;
  for (int i = 0; i < 8; i++)
  {
    char ad = (n << (i * 8)) >> 56;
    if (ad != 0)
      start = 1;
    if (start)
      ret += ad;
  }
  return ret;
}

std::string mkpkt(std::string salt, std::string usr, std::string pwd, long long mac)
{

  std::string data = "\x03\x01";
  data.append(1, (char)0x0);
  data += (char)(usr.size() + 20);

  data.append(MD5::checkSum(std::string("\3\1") + salt + pwd));
  data.append(usr);
  data.append(36 - usr.size(), (char)0x0);
  data.append("\x20");// CONTROLCHECKSTATUS
  data.append("\1");// adpter num

  std::string dumpstr = dump(strToLong(data.substr(4, 6)) ^ mac);
  data += dumpstr.substr(dumpstr.size() - 6);

  std::string checkStr = std::string("\x01") + pwd + salt;
  checkStr.append(4, (char)0x0);
  data += MD5::checkSum(checkStr);

  data += "\x01";
  data += "\xa\x1e\x16\x11"; // host_ip
  
  data.append(12, (char)0x0);

  checkStr = data + std::string("\x14");
  checkStr.append(1, (char)0x0);
  checkStr += "\x07\x0B";
  data += MD5::checkSum(checkStr).substr(0, 8);

  data += "\x01"; //IPDOG
  data.append(4, (char)0x0);

  std::string host_name = "LIYUANYUAN";
  data.append(host_name);
  data.append(32 - host_name.size(), 0x0);
  data.append(4, (char)114);// dns
  data.append(4, (char)0);// _tagHostInfo.DHCPServerIP
  data.append(12, (char)0);
  data += "\x94";
  data.append(3, (char)0);
  data += "\x05";   // _tagHostInfo.OSVersion.MajorVersion
  data.append(3, (char)0);
  data += "\x01";   // _tagHostInfo.OSVersion.MinorVersion
  data.append(3, (char)0);
  data += "\x28\x0A";   // _tagHostInfo.OSVersion.BuildNumber
  data.append(2, (char)0);
  data += "\x02";   // _tagHostInfo.OSVersion.PlatformID
  data.append(3, (char)0);

  std::string host_os = "8089DA";
  data.append(host_os);
  data.append(32 - host_os.size(), 0x0);
  data.append(96, (char)0);

  data += "\x0a"; // AUTH_VERSION
  data.append(1, (char)0);

  //data += ror(MD5::checkSum(std::string("\x03\x01") + salt + pwd), pwd);
  
  auto checksum = [](std::string st) -> std::string
  {
    int ret = 1234;
    int i = 0;
    st.append(4, (char)0);
    for (; i < st.length() - 4; i += 4)
    {
      std::string bf = st.substr(i, 4);
      int num = (int)((unsigned char)bf[3] << 24);
      num += (int)(((unsigned char)bf[2]) << 16 );
      num += (int)(((unsigned char)bf[1]) << 8);
      num += (int)(((unsigned char)bf[0]));
      ret ^= num;
    }
    ret = (1968 * ret) & 0xffffffff;
    std::string r;
    r += ((unsigned char)ret) >> 24;
    r += (((unsigned char)ret) << 24) >> 24;
    r += (((unsigned char)ret) << 16) >> 24;
    r += (((unsigned char)ret) << 8) >> 24;
    return r;
  };
  data += "\x02";
  data += "\x0c";

  std::string sumStr;
  sumStr = data + std::string("\x01\x26\x07\x11");
  sumStr.append(2, (char)0x0);
  sumStr += dump(mac);
  data += checksum(sumStr);

  data.append(2, (char)0);
  data += dump(mac);
  data.append(2, (char)0);

  data += "\xE9\x13";
  return data;
}

std::string DRlogin(std::string username, std::string password, std::string server)
{
  std::string ret;
  ret.resize(1024);
  for (int i = 0; i < 5; i++)
  {
    //SALT = challenge(server, GetSystemTimeAsUnixTime() + ((rand() % 0xf0) + 0xf));
    SALT = challenge(server, (rand() % 0xffff));

    std::string packet = mkpkt(SALT, username, password, 0x54e1ad1af086);
    log(std::string("[login] send "), hexToString(packet));
    s.SendTo(server, 61440, packet.c_str(), packet.size());
    s.RecvFrom((char*)ret.c_str(), ret.length());
    log(std::string("[login] recv "), hexToString(ret));
    log(std::string("[login] packet sent."));
    if (ret[0] == *"\x04")
    {
      log(std::string("[login] loged in"));
      break;
    }
    else
      delay(2000);
  }
  return ret.substr(23, 16);
}

std::string keep_alive_package_builder(int number, std::string tail, int type = 1, bool first = false)
{
  std::string data = "\x07";
  data.append(1, (char)number);
  data += "\x28";
  data.append(1, (char)0x0);
  data += "\x0B";
  data.append(1, (char)type);

  if (first)
    data += "\x0F\x27";
  else
    data += "\xdc\x02"; // KEEP_ALIVE_VERSION
  data += "\x2F\x12";
  data.append(6, (char)0x0);
  data += tail;
  data.append(4, (char)0x0);
  if (type == 3)
  {
    data.append(4, (char)0x0);
    data += "\x10\x30\x22\x17";
    data.append(8, (char)0x0);
  }
  else
    data.append(16, (char)0x0);
  return data;
}

bool keep_alive1(std::string salt, std::string tail, std::string pwd, std::string svr) 
{
  std::string data = "\xff" + MD5::checkSum("\x03\x01" + salt + pwd);
  data.append(3, (char)0x0);
  data += tail;
  unsigned int randNum = (rand()) % 0xffff;

  data.append(1, (char)((randNum) >> 8));
  data.append(1, (char)(((randNum) << 24) >> 24));
  

  data.append(4, (char)0x0);

  log(std::string("[keep_alive1] send "), hexToString(data));

  s.SendTo(svr, 61440, data.data(), data.size());

  while (1)
  {
    std::string ret;
    ret.resize(1024);
    if (!s.RecvFrom((char*)ret.c_str(), ret.length()))
      return false;
    if (ret[0] == *"\x07")
    {
      log(std::string("[keep_alive1] recv "), hexToString(ret));
      break;
    }
  }
  
}

void keep_alive2(std::string salt, std::string tail, std::string pwd, std::string svr)
{
  auto compareStr = [](const char* str1, const char* str2, int size) -> bool
  {
    for (int i = 0; i < size; i++)
    {
      if (str1[i] != str2[i])
        return false;
    }
    return true;
  };
  std::string ttail;
  ttail.append(4, (char)0x0);

  std::string otail = tail;

  std::string data;
  data.resize(1024);

  int svr_num = 0;
  std::string packet = keep_alive_package_builder(svr_num, ttail, 1, true);

  while (1)
  {
    log(std::string("[keep-alive2] send1 "), hexToString(packet));
    s.SendTo(svr, 61440, packet.data(), packet.size());

  
    s.RecvFrom((char*)data.c_str(), data.length());
    log(std::string("[keep-alive2] recv1 "), hexToString(data));

    if (compareStr(data.c_str(), "\x07\x00\x28\x00", 4))
    {
      std::string cstr = "\x07";
      for (int i = 0; i < svr_num; i++)
        cstr.append(1, (char)0x0);
      cstr += "\x28";
      cstr.append(1, (char)0x0);
      if (compareStr(data.c_str(), cstr.c_str(), svr_num + 3))
        break;
    }
    else if (data[0] == 0x7 && data[2] == 0x10)
    {
      log(std::string("[keep-alive2] recv file, resending.."));
      svr_num = svr_num + 1;
      break;
    }
    else
    {
      log(std::string("[keep-alive2] recv1/unexpected"), hexToString(data));
    }
  }

  packet = keep_alive_package_builder(svr_num, ttail, 1, false);
  log(std::string("[keep-alive2] send2"), hexToString(packet));
  s.SendTo(svr, 61440, packet.data(), packet.size());
  while (1)
  {
    s.RecvFrom((char*)data.c_str(), data.length());
    if (data[0] == 0x7)
    {
      svr_num = svr_num + 1;
      tail = data.substr(16, 4);
      log(std::string("[keep-alive2] recv2"), hexToString(data));
      break;
    }
    else
      log(std::string("[keep-alive2] recv2/unexpected"), hexToString(data));
  }

  packet = keep_alive_package_builder(svr_num, tail, 3, false);
  s.SendTo(svr, 61440, packet.data(), packet.size());
  while (1)
  {
    s.RecvFrom((char*)data.c_str(), data.length());
    if (data[0] == 0x7)
    {
      svr_num = svr_num + 1;
      tail = data.substr(16, 4);
      log(std::string("[keep-alive2] recv3"), hexToString(data));
      log(std::string("[keep-alive2] keep-alive2 loop was in daemon."));
      break;
    }
  }
  while (1)
  {
    
      delay(20000);
      if (!keep_alive1(salt, otail, pwd, svr))
        return;
      packet = keep_alive_package_builder(svr_num, tail, 1, false);
      log(std::string("[keep_alive2] send "), hexToString(packet));
      s.SendTo(svr, 61440, packet.data(), packet.size());
      
      s.RecvFrom((char*)data.c_str(), data.length());
      log(std::string("[keep_alive2] recv "), hexToString(data));

      tail = data.substr(16, 4);

      packet = keep_alive_package_builder(svr_num + 1, tail, 3, false);
      s.SendTo(svr, 61440, packet.data(), packet.size());
      log(std::string("[keep_alive2] send "), hexToString(packet));

      s.RecvFrom((char*)data.c_str(), data.length());
      tail = data.substr(16, 4);
      log(std::string("[keep_alive2] recv "), hexToString(data));

      if (tail == "")
        return;
      svr_num = (svr_num + 2) % 127;
    
  
  }


}

  char server[] = "192.168.211.3";
  char username[] = "账号"; // 这里登录账号
  char password[] = "密码"; // 这里登录密码
  
void setup() {
  Serial.begin(115200);
  
  Serial.print("start connect");
  WiFi.mode(WIFI_STA);
  WiFi.begin(" 账号 ", " 密码 "); // 这里wifi账号密码
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(500);
  }
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());
  Serial.printf("UDP server on port %d\n", 8880);


  log(std::string("auth svr: "), std::string(server), std::string("\nusername: "), std::string(username), std::string("\npassword: "), std::string(password), std::string("\nmac: "));
  log(std::string("bind ip: "), std::string("0.0.0.0"));
}


void loop() {

    std::string package_tail = DRlogin(username, password, server);
    if(keep_alive1(SALT, package_tail, password, server))
       keep_alive2(SALT, package_tail, password, server);
}
