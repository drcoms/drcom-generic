#coding=UTF-8

#适用于衡水学院校园网，已通过测试
#在下面需要输入帐号信息的地方输入账号等信息
#有问题请联系littledongdong@foxmail.com
#最后编辑时间：2017-2-22 10:14:51
#by Dong

import socket, struct, time,random,re
from hashlib import md5

#config
server = '192.168.114.11'
username=''#引号内输入校园网账号（学号）
password=''#引号内输入校园网密码
CONTROLCHECKSTATUS = '\x20'
ADAPTERNUM = '\x04'
host_ip = ''#引号内输入本机IP地址（可在Dr.COM客户端查看）
IPDOG = '\x01'
host_name = 'DRCOMFUCKER'
PRIMARY_DNS = '222.222.222.222'
dhcp_server = '192.168.103.254'
AUTH_VERSION = '\x21\x00'
mac = 0x001c4209e63c
host_os = 'WINDIAOS'
KEEP_ALIVE_VERSION = '\xdc\x02'
#config_end

class ChallengeException (Exception):
  def __init__(self):
    pass

class loginException (Exception):
  def __init__(self):
    pass
	
def try_socket():
#sometimes cannot get the port
	global s,salt
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.bind(("0.0.0.0", 61440))
		s.settimeout(3)
	except:
		print ("."),
		time.sleep(0.5)
		print ("."),
		time.sleep(0.5)
		print (".")
		time.sleep(0.5)
		print ("...reopen")
		time.sleep(10)
		main()
	else:
		SALT= ''

UNLIMITED_RETRY = True
EXCEPTION = False
	
def get_randmac():
	mac = [ 0x00, 0x16, 0x3e,random.randint(0x00, 0x7f),random.randint(0x00, 0xff),random.randint(0x00, 0xff) ]
	return ''.join(map(lambda x: "%02x" % x, mac))
	#print randomMAC()
	
def version():
	print ("DrCOM Auth Router for GDUFE") 
	
	
def challenge(svr,ran):
    while True:
      t = struct.pack("<H", int(ran)%(0xFFFF))
      s.sendto("\x01\x02"+t+"\x09"+"\x00"*15, (svr, 61440))
      try:
        data, address = s.recvfrom(1024)
        #print('[challenge] recv',data.encode('hex'))
      except:
        print('[challenge] timeout, retrying...')
        continue
        
      if address == (svr, 61440):
        break
      else:
        continue
    #print('[DEBUG] challenge:\n' + data.encode('hex'))
    if data[0] != '\x02':
      raise ChallengeException
    print('[challenge] challenge packet sent.')
    return data[4:8]

def md5sum(s):
    m = md5()
    m.update(s)
    return m.digest()

def dump(n):
    s = '%x' % n
    if len(s) & 1:
        s = '0' + s
    return s.decode('hex')

def ror(md5, pwd):
    ret = ''
    for i in range(len(pwd)):
        x = ord(md5[i]) ^ ord(pwd[i])
        ret += chr(((x<<3)&0xFF) + (x>>5))
    return ret

def keep_alive_package_builder(number,random,tail,type=1,first=False):
    data = '\x07'+ chr(number) + '\x28\x00\x0b' + chr(type)
    data += KEEP_ALIVE_VERSION+'\x2f\x12' + '\x00' * 6
    data += tail
    data += '\x00' * 4
    #data += struct.pack("!H",0xdc02)
    if type == 3:
      foo = ''.join([chr(int(i)) for i in host_ip.split('.')]) # host_ip
	#use double keep in main to keep online .Ice
      crc = '\x00' * 4
      #data += struct.pack("!I",crc) + foo + '\x00' * 8
      data += crc + foo + '\x00' * 8
    else: #packet type = 1
      data += '\x00' * 16
    return data

def packet_CRC(s):
    ret = 0
    for i in re.findall('..', s):
        ret ^= struct.unpack('>h', i)[0]
        ret &= 0xFFFF
    ret = ret * 0x2c7
    return ret



def keep_alive2(*args):
    tail = ''
    packet = ''
    svr = server
    ran = random.randint(0,0xFFFF)
    ran += random.randint(1,10)   
    
    packet = keep_alive_package_builder(0,dump(ran),'\x00'*4,1,True)
    #packet = keep_alive_package_builder(0,dump(ran),dump(ran)+'\x22\x06',1,True)
    print ('[keep-alive2] send1')#packet.encode('hex')
    while True:
        s.sendto(packet, (svr, 61440))
        data, address = s.recvfrom(1024)
        if data.startswith('\x07'):
            break
        else:
			print ('[keep-alive2] recv/unexpected',data.encode('hex'))
			continue
    ran += random.randint(1,10)   
    packet = keep_alive_package_builder(1,dump(ran),'\x00'*4,1,False)
    #print '[keep-alive2] send2',packet.encode('hex')
    s.sendto(packet, (svr, 61440))
    while True:
        data, address = s.recvfrom(1024)
        if data[0] == '\x07':
            break
    #print '[keep-alive2] recv2',data.encode('hex')
    tail = data[16:20]
    

    ran += random.randint(1,10)   
    packet = keep_alive_package_builder(2,dump(ran),tail,3,False)
    #print '[keep-alive2] send3',packet.encode('hex')
    s.sendto(packet, (svr, 61440))
    while True:
        data, address = s.recvfrom(1024)
        if data[0] == '\x07':
            break
    #print '[keep-alive2] recv3',data.encode('hex')
    tail = data[16:20]
    print ("[keep-alive] keep-alive loop was in daemon.")
    i = 3

    while True:
      try:
		keep_alive1(SALT,package_tail,password,server)
		print '[keep-alive2] send'
		ran += random.randint(1,10)   
		packet = keep_alive_package_builder(i,dump(ran),tail,1,False)
		#print('DEBUG: keep_alive2,packet 4\n',packet.encode('hex'))
		#print '[keep_alive2] send',str(i),packet.encode('hex')
		s.sendto(packet, (svr, 61440))
		data, address = s.recvfrom(1024)
		#print '[keep_alive2] recv',data.encode('hex')
		tail = data[16:20]
		#print('DEBUG: keep_alive2,packet 4 return\n',data.encode('hex'))
        
		ran += random.randint(1,10)   
		packet = keep_alive_package_builder(i+1,dump(ran),tail,3,False)
		#print('DEBUG: keep_alive2,packet 5\n',packet.encode('hex'))
		s.sendto(packet, (svr, 61440))
		#print('[keep_alive2] send',str(i+1),packet.encode('hex'))
		data, address = s.recvfrom(1024)
		#print('[keep_alive2] recv',data.encode('hex'))
		tail = data[16:20]
		#print('DEBUG: keep_alive2,packet 5 return\n',data.encode('hex'))
		i = (i+2) % 0xFF
		time.sleep(20)
      except:
        pass

def checksum(s):
    ret = 1234
    for i in re.findall('....', s):
        ret ^= int(i[::-1].encode('hex'), 16)
    ret = (1968 * ret) & 0xffffffff
    return struct.pack('<I', ret)


def mkpkt(salt, usr, pwd, mac):
    data = '\x03\x01\x00'+chr(len(usr)+20)
    data += md5sum('\x03\x01'+salt+pwd)
    data += usr.ljust(36, '\x00')
    data += '\x20' #fixed unknow 1
    data += '\x02' #unknow 2
    data += dump(int(data[4:10].encode('hex'),16)^mac).rjust(6,'\x00') #mac xor md51
    data += md5sum("\x01" + pwd + salt + '\x00'*4) #md52
    data += '\x01' #NIC count
    data += hexip #your ip address1 
    data += '\00'*4 #your ipaddress 2
    data += '\00'*4 #your ipaddress 3
    data += '\00'*4 #your ipaddress 4
    data += md5sum(data + '\x14\x00\x07\x0b')[:8] #md53
    data += '\x01' #ipdog
    data += '\x00'*4 #delimeter
    data += host_name.ljust(32, '\x00')
    data += '\x72\x72\x72\x72' #primary dns: 114.114.114.114
    data += '\x0a\xff\x00\xc5' #DHCP server
    data += '\x08\x08\x08\x08' #secondary dns:8.8.8.8
    data += '\x00' * 8 #delimeter
    data += '\x94\x00\x00\x00' # unknow
    data += '\x05\x00\x00\x00' #os major
    data += '\x01\x00\x00\x00' # os minor
    data += '\x28\x0a\x00\x00' # OS build
    data += '\x02\x00\x00\x00' #os unknown
    data += host_os.ljust(32,'\x00')
    data += '\x00' * 96
    #data += '\x01' + host_os.ljust(128, '\x00')
    #data += '\x0a\x00\x00'+chr(len(pwd)) # \0x0a represents version of client, algorithm: DRCOM_VER + 100
    #data += ror(md5sum('\x03\x01'+salt+pwd), pwd)
    data += AUTH_VERSION
    data += '\x02\x0c'
    data += checksum(data+'\x01\x26\x07\x11\x00\x00'+dump(mac))
    data += '\x00\x00' #delimeter
    data += dump(mac)
    data += '\x00' # auto logout / default: False
    data += '\x00' # broadcast mode / default : False
    data += '\xc2\x66' #unknown
    
    
    return data

def login(usr, pwd, svr):
    global SALT
 
    i = 0
    while True:
        salt = challenge(svr,time.time()+random.randint(0xF,0xFF))
        SALT = salt
        packet = mkpkt(salt, usr, pwd, mac)
        #print('[login] send',packet.encode('hex'))
        s.sendto(packet, (svr, 61440))
        data, address = s.recvfrom(1024)
        #print('[login] recv',data.encode('hex'))
        print('[login] packet sent.')
        if address == (svr, 61440):
            if data[0] == '\x04':
              print('[login] login in')
              break
            else:
              continue
        else:
            if i >= 5 and UNLIMITED_RETRY == False :
              print('[login] exception occured.')
              sys.exit(1)
            else:
              continue
            
    print('[login] login Success')
    return data[23:39]
    #return data[-22:-6]

def keep_alive1(salt,tail,pwd,svr):
    foo = struct.pack('!H',int(time.time())%0xFFFF)
    data = '\xff' + md5sum('\x03\x01'+salt+pwd) + '\x00\x00\x00'
    data += tail
    data += foo + '\x00\x00\x00\x00'
    print '[keep_alive1] send'#data.encode('hex'))

    s.sendto(data, (svr, 61440))
    while True:
        data, address = s.recvfrom(1024)
        if data[0] == '\x07':
            break
        else:
            print '[keep-alive1]recv/not expected'#data.encode('hex')
    #print('[keep-alive1] recv',data.encode('hex'))

def empty_socket_buffer():
#empty buffer
    print('starting to empty socket buffer')
    try:
        while True:
            data, address = s.recvfrom(1024)
            #print 'recived sth unexcepted',data.encode('hex')
            if s == '':
                break
    except:
        # get exception means it has done.
        print('exception in empty_socket_buffer')
        pass
    print('emptyed')


		
def main():
	global server,username,password,host_name,host_os,dhcp_server,mac,hexip,host_ip
	hexip=socket.inet_aton(host_ip)
	#host_ip=ip
	host_name = "est-pc"
	host_os = "8089D"   #default is 8089D
	dhcp_server = "0.0.0.0"
	#mac = 0xE0DB55BAE012 
	#it is a mac in programme and it may crush with other users so I use randMAC to avoid it
	loginpart()
	
def loginpart():
	global package_tail
	while True:
		try:
			package_tail = login(username, password, server)
		except loginException:
			continue
		#print('package_tail',package_tail.encode('hex'))
		keeppart()
		
def keeppart():
	#empty_socket_buffer()
	#empty_socket_buffer()
	keep_alive2(SALT,package_tail,password,server)

		
if __name__ == "__main__":
	try_socket()
	version()
	#get_conf()
	main()


