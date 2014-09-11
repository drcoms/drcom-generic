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

	def _make_heartbeat(self, sip, challenge_seed):
		# DrcomDialExtProtoHeader - 5 bytes
		data = '\x07' # code
		data += chr(self.count + 1) # id
		data += struct.pack('I',0x60) # length
		data += '\x03' # type

		data += '\x00' # uid length
		data += '\x00\x00\x00\x00\x00\x00' # mac
		data += sip # AuthHostIP
		#data += '\x00\x62\x00\x14' # 非第一次则是 data += '\x00\x62\x00\x14' 
		data += struct.pack('I',0x14006200)
		data += challenge_seed # Challenge Seed
		# CRC
		data += struct.pack('I',20000711) # DRCOM_DIAL_EXT_PROTO_CRC_INIT
		data += struct.pack('I',126)
		# - DrcomDialExtProtoHeader end -
		data += '\x00\x00\x00\x00\x00\x00\x00\x8b\xac\x2a\x14\x78\xff\xff\xff\xff'
		data += '\x00\xa0\x59\x06\x00\x20\x00\x03\xc0\x51\x25\x08\xff\xff\xff\x00'
		data += '\x00\xa0\x59\x06\x00\x01\x00\x03\xc0\x51\x2b\x08\xff\xff\xff\x00'
		data += '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

		 
		return data
	def send(self):
		pass

a = PPPOEHeartbeat(0x55)
c = a._make_heartbeat('\xac\x15\x05\x0f','\xcf\x89\xa8\x03')
print hexlify(c)
print hex(a._DrcomCRC32(c))
print hex(a._DrcomCRC32(c)*19680126)
