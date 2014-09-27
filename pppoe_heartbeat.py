#coding=utf8
from binascii import hexlify, crc32
import re
import struct
import md4

class PPPOEHeartbeat:
	def __init__(self, num):
		self.count = num # 计数器
	def _make_challenge(self):
		data = '\x07'
		data += chr(self.count)
		data += '\x08\x00\x01\x00'
		data+= '\x00\x00'
		return data
	
	def _encrypt_md4(self, data):
		pass
	def _encrypt_md5(self, data):
		pass

	def _encrypt_sha1(self, data):
		pass

		def _netinfo_encrypt(self, data):
			s = ''
			for index, c in enumerate(data):
				foo = ord(c) << index & 0x07
				foo &= 0xFF # 去掉多余位
				bar = ord(c) >> (8 - (index & 0x07))
				bar &= 0xFF
				s += chr((foo + bar) & 0xFF)
			return s

	def _DrcomCRC32(self, data, init = 0):
		ret = init
		for i in re.findall('....', data):
			ret ^= struct.unpack('!I', i)[0]
		return ret
	def _gen_crc(self, data, encrypt_type):
		DRCOM_DIAL_EXT_PROTO_CRC_INIT = 20000711
		ret = ''
		if encrypt_type == 0:
			# 加密方式无
			return struct.pack('!I',DRCOM_DIAL_EXT_PROTO_CRC_INIT) + struct.pack('!I',126)
		elif encrypt_type == 1:
			# 加密方式为 md5
			foo = hashlib.md5(data).digest()
			ret += foo[2]
			ret += foo[3]
			ret += foo[8]
			ret += foo[9]
			ret += foo[5]
			ret += foo[6]
			ret += foo[13]
			ret += foo[14]
			return ret
		elif encrypt_type == 2:
			# md4
			foo = md4(data)
			ret += foo[1]
			ret += foo[2]
			ret += foo[8]
			ret += foo[9]
			ret += foo[4]
			ret += foo[5]
			ret += foo[11]
			ret += foo[12]
			return ret
		elif encrypt_type == 3:
			# sha1
			foo = hashlib.sha1(data).digest()	
			ret += foo[2]
			ret += foo[3]
			ret += foo[9]
			ret += foo[10]
			ret += foo[5]
			ret += foo[6]
			ret += foo[15]
			ret += foo[16]	
			return ret

	def _make_heartbeat(self, sip, challenge_seed):
		# DrcomDialExtProtoHeader - 5 bytes
		"""
		typedef struct _tagDrcomDialExtProtoHeader
		{
		    unsigned char code;
		    unsigned char id;
		    unsigned short length;
		    unsigned char type;
		} PPPOEHEADER;
		"""
		data = '\x07' # code
		data += chr(self.count + 1) # id
		data += '\x60\x00' # length
		data += '\x03' # type
		"""
		struct _tagDrcomDialExtProtoLoginPacket {
		    PPPOEHEADER header; // 5 byte

		#define hcode   header.code     // PPPoE ext = 0x07
		#define hid     header.id       // 自定义，每次不同就可以
		#define hlength header.length   // 发送数据包的长度
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
		"""
		data += '\x00' # uid length
		data += '\x00\x00\x00\x00\x00\x00' # mac
		data += sip # AuthHostIP
		data += '\x00\x62\x00\x14' # 非第一次则是 data += '\x00\x62\x00\x14' 
		#data += struct.pack('I',0x14006200)
		data += challenge_seed # Challenge Seed
		# CRC
		# data += struct.pack('I',20000711) # DRCOM_DIAL_EXT_PROTO_CRC_INIT
		# data += '\xc7\x2f\x31\x01'
		data + '\x01\x31\x2f\xc7'
		#data += struct.pack('I',126)
		# data += '\x7e\x00\x00\x00'
		data += '\x00\x00\x00\x7e'
		# - DrcomDialExtProtoHeader end -
		"""
		struct _tagDrcomDialExtProtoNetWorkInfo
		{
		    unsigned char mac[6];
		    unsigned char netmark;      //dhcp mark
		    unsigned char type;     //interface type(ether,ppp)
		    unsigned long sip;
		    unsigned long smask;
		    //ULONG gateway1;
		};
		"""
		data += '\x00\x00\x00\x00\x00\x00'
		data += '\x00'
		data += '\x8b'
		data += '\xac\x2a\x14\x78'
		data += '\xff\xff\xff\xff'

		data += '\x00\xa0\x59\x06\x00\x20'
		data += '\x00'
		data += '\x03'
		data += '\xc0\x51\x25\x08'
		data += '\xff\xff\xff\x00'

		data += '\x00\xa0\x59\x06\x00\x01'
		data += '\x00'
		data += '\x03'
		data += '\xc0\x51\x2b\x08'
		data += '\xff\xff\xff\x00'

		data += '\x00\x00\x00\x00\x00\x00'
		data += '\x00'
		data += '\x00'
		data += '\x00\x00\x00\x00'
		data += '\x00\x00\x00\x00'

		 
		return data
	def send(self):
		pass

a = PPPOEHeartbeat(0x55)
c = a._make_heartbeat('\xac\x15\x05\x0f','\xcf\x89\xa8\x03')
print hexlify(c)
print hex(a._DrcomCRC32(c))
print hex((a._DrcomCRC32(c)*19680126))
print hex((a._DrcomCRC32(c)*19680126) & 0xFFFFFFFF)
