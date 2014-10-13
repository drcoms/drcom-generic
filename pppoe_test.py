#coding=utf8
from binascii import hexlify, crc32
import re
import struct

class PPPOEHeartbeat:
	def __init__(self, num):
		self.count = num # 计数器
	def _make_challenge(self):
		data = '\x07'
		data += chr(self.count)
		data += '\x08\x00\x01\x00'
		data+= '\x00\x00'
		return data

	def _DrcomCRC32(self, data, init = 0):
		ret = init
		for i in re.findall('....', data):
			ret ^= struct.unpack('!I', i)[0]
		return ret

	def _make_heartbeat(self, sip, challenge_seed, first=False):
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
		data += chr(self.count) # id
		data += '\x60\x00' # length
		data += '\x03' # type
		data += '\x00' # uid length
		data += '\x00\x00\x00\x00\x00\x00' # mac
		data += sip # AuthHostIP
		if first:
			data += struct.pack("I", 0x6200) # 非第一次则是 data += '\x00\x62\x00\x14' 
		else:
			data += struct.pack("I", 0x6300)
		data += challenge_seed # Challenge Seed
		# CRC
		data += struct.pack('I',20000711) # DRCOM_DIAL_EXT_PROTO_CRC_INIT
		# data += '\xc7\x2f\x31\x01'
		# data + '\x01\x31\x2f\xc7'
		data += struct.pack('I',126)
		# data += '\x7e\x00\x00\x00'
		#   data += '\x00\x00\x00\x7e'
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
		data += '\x00'*16 # ip1
	    	data += '\x00'*16 # ip2
	    	data += '\x00'*16 # ip3
	    	data += '\x00'*16 # ip4

		return data
	def send(self):
		# 20s 发一次
		# send challenge
		# recv auth_required
		# self.count = (self.count + 2) % 0xFF
		# send auth packet
		# self.count = (self.count + 2) % 0xFF
		# recv success packet

