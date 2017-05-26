import socket, struct, time
from hashlib import md5
import sys
import urllib2

class ChallengeException (Exception):
  def __init__(self):
    pass

class LoginException (Exception):
  def __init__(self):
    pass
   
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("your own ip", 61440))

s.settimeout(3)
SALT = ''
UNLIMITED_RETRY = True
EXCEPTION = False
DEBUG = True
username = "your username"
password = "your password"
mac = 0x123456789011 #your own mac
server = "10.100.61.3" # "auth.jlu.edu.cn"
host_name = "LAPTOP-ABCDEFGH" #can be assigned whatever values
host_os = "DrCOM"

def init(host_name):
	tmp = 'ABCDEFGH'
	if len(host_name)>=8:
		host_name = 'LAPTOP-'+host_name[0:8]
	else:
		host_name = 'LAPTOP-'+host_name+tmp[0:8-len(host_name)]
	return host_name

def challenge(svr,ran):
    while True:
      t = struct.pack("<H", int(ran)%(0xFFFF))
      s.sendto("\x01\x02"+t+"\x6a"+"\x00"*15, (svr, 61440))
      try:
        data, address = s.recvfrom(1024)
      except:
        if DEBUG:
          print '[challenge] timeout, retrying...'
        continue
        
      if address == (svr, 61440):
        break;
      else:
        continue
    if DEBUG:
      print '[DEBUG] challenge'
    if data[0] != '\x02':
      raise ChallengeException
    print '[challenge] challenge packet sent.'
    #print 'salt:',data[2:6].encode('hex')
    #print 'addr:',address.encode('hex')
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
    if first :
      data += '\x0f\x27'
    else:
      data += '\xdc\02'
    data += random + '\x00' * 6
    data += tail
    data += '\x00' * 4
    #data += struct.pack("!H",0xdc02)
    if type == 3:
      foo = '\x31\x8c\x21\x3e' #CONSTANT
      #CRC
      crc = packet_CRC(data+foo)
      data += struct.pack("!I",crc) + foo + '\x00' * 8
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

def keep_alive2():
    #first keep_alive:
    #number = number (mod 7)
    #status = 1: first packet user sended
    #         2: first packet user recieved
    #         3: 2nd packet user sended
    #         4: 2nd packet user recieved
    #   Codes for test
    tail = ''
    packet = ''
    svr = server
    import random
    ran = random.randint(0,0xFFFF)
    ran += random.randint(1,10)   
    packet = keep_alive_package_builder(0,dump(ran),'\x00'*4,1,True)
    s.sendto(packet, (svr, 61440))
    data, address = s.recvfrom(1024)
    
    ran += random.randint(1,10)   
    packet = keep_alive_package_builder(1,dump(ran),'\x00'*4,1,False)
    s.sendto(packet, (svr, 61440))
    data, address = s.recvfrom(1024)
    tail = data[16:20]
    

    ran += random.randint(1,10)   
    packet = keep_alive_package_builder(2,dump(ran),tail,3,False)
    s.sendto(packet, (svr, 61440))
    data, address = s.recvfrom(1024)
    tail = data[16:20]
    print "[keep-alive2] keep-alive2 loop was in daemon."
    
    i = 1
    while True:
      try:
        time.sleep(25)
        ran += random.randint(1,10)   
        packet = keep_alive_package_builder(2,dump(ran),tail,1,False)
        #print 'DEBUG: keep_alive2,packet 4\n',packet.encode('hex')
        s.sendto(packet, (svr, 61440))
        data, address = s.recvfrom(1024)
        tail = data[16:20]
        #print 'DEBUG: keep_alive2,packet 4 return\n',data.encode('hex')
        
        ran += random.randint(1,10)   
        packet = keep_alive_package_builder(2,dump(ran),tail,3,False)
        #print 'DEBUG: keep_alive2,packet 5\n',packet.encode('hex')
        s.sendto(packet, (svr, 61440))
        data, address = s.recvfrom(1024)
        tail = data[16:20]
        #print 'DEBUG: keep_alive2,packet 5 return\n',data.encode('hex')
        i = i+1
        i = i % (0xFF)
        
        check_online = urllib2.urlopen('http://10.100.61.3')
        foo = check_online.read()
        if 'login.jlu.edu.cn' in foo:
          print '[keep_alive2] offline.relogin...'
          break;
        #MODIFIED END
        ''' 
        if i % 10 == 0:
          check_online = urllib2.urlopen('http://10.100.61.3')
          foo = check_online.read()
          if 'login.jlu.edu.cn' in foo:
            print '[keep_alive2] offline.relogin...'
            break;
        '''
      except:
        pass
        
    
import re
def checksum(s):
    ret = 1234
    for i in re.findall('....', s):
        ret ^= int(i[::-1].encode('hex'), 16)
    ret = (1968 * ret) & 0xffffffff
    return struct.pack('<I', ret)


def log(data):
    print data.encode('hex')
    print '====================================='


def mkpkt(salt, usr, pwd, mac):
    data = '\x03\01\x00'+chr(len(usr)+20)
    data += md5sum('\x03\x01'+salt+pwd)
    data += usr.ljust(36, '\x00')
    data += '\x00\x00'
    data += dump(int(data[4:10].encode('hex'),16)^mac).rjust(6,'\x00')
    data += md5sum("\x01" + pwd + salt + '\x00'*4)
    data += '\x01\x31\x8c\x31\x4e' + '\00'*12
    data += md5sum(data + '\x14\x00\x07\x0b')[:8] + '\x01'+'\x00'*4
    host_name = init(host_name)
    data += host_name
    data += '\x00'.ljust(17,'\x00')+'\x0a\x0a\x0a\x0a\x00\x00\x00\x00\xca\x62\x12\x03'
    data += '\x00'.ljust(7,'\x00')+'\x94\x00\x00\x00\x06\x00\x00\x00\x00\x02\x00\x00\x00'
    data += '\xf0\x23\x00\x00\x02\x00\x00\x00'
    data += host_os
    data += b'\x00\xcf\x07\x6a\x00'.ljust(59,'\x00')
    data += b'1c210c99585fd22ad03d35c956911aeec1eb449b'
    data += '\x00'.ljust(24,'\x00')
    data += '\x6d\x00\x00'+chr(len(pwd))
    data += ror(md5sum('\x03\x01'+salt+pwd), pwd)
    data += '\x02\x0c'
    data += checksum(data+'\x01\x26\x07\x11\x00\x00'+dump(mac))
    data += "\x00\x00" + dump(mac)
    data += '\x00\x00'+'\xa1\x19'
    return data

def login(usr, pwd, svr):
    import random
    global SALT
 
    i = 0
    while True:
        try:
            try:
              salt = challenge(svr,time.time()+random.randint(0xF,0xFF))
            except ChallengeException:
              if DEBUG:
                print 'challenge packet exception'
              continue
            SALT = salt
            packet = mkpkt(salt, usr, pwd, mac)
            s.sendto(packet, (svr, 61440))
            data, address = s.recvfrom(1024)
        except:
            print "[login] recvfrom timeout,retrying..."
            continue
        print '[login] packet sent.'
        if address == (svr, 61440):
            if data[0] == '\x05' and i >= 5 and UNLIMITED_RETRY == False:
              print '[login] wrong password, retried ' + str(i) +' times.'
              sys.exit(1)
            elif data[0] == '\x05':
              print "[login] wrong password."
              i = i + 1
              time.sleep(i*1.618)
            elif data[0] != '\x04':
              print "[login] server return exception.retry"
              if DEBUG:
                print '[login] last packet server returned:\n' + data.encode('hex')
              time.sleep(1)
              raise LoginException
              continue;
            break;
        else:
            if i >= 5 and UNLIMITED_RETRY == False :
              print '[login] packet received error, maybe you are under attacking'
              sys.exit(1)
            else:
              i = i + 1
              print '[login] package error, retrying...'
              
    print '[login] login sent'
    return data[-22:-6]

import httplib
def info(ip):
    c = httplib.HTTPConnection(ip, 80, timeout=10)
    c.request("GET", "")
    r = c.getresponse()
    if r.status != 200:
        return None
    s = r.read()
    data = dict()
    data["flux"] = int(s[s.index("flow='")+6:s.index("';fsele=")])
    data["time"] = int(s[s.index("time='")+6:s.index("';flow")])
    return data
def keep_alive1(salt,tail,pwd,svr):
    foo = struct.pack('!H',int(time.time())%0xFFFF)
    data = '\xff' + md5sum('\x03\x01'+salt+pwd) + '\x00\x00\x00'
    data += tail
    data += foo + '\x00\x00\x00\x00'
    print '[keep_alive1] keep_alive1,sent'
    s.sendto(data, (svr, 61440))
    try:
        data, address = s.recvfrom(1024)
        print '[keep_alive1] keep_alive1,server received'
    except:
        print '[keep_alive1] Timeout!'
        pass
    
def main():
    print "auth svr:"+server+"\nusername:"+username+"\npassword:"+"********"+"\nmac:"+str(hex(mac))
    print "os:MSDOS 8.0"+"\nhostname: localhost" 
    print "DrCOM Auth Router Ver 1.2"
    print "Version feature:\n[1] Auto Anti droping connection\n[2] Stronger exception handling."
    while True:
      try:
        package_tail = login(username, password, server)
      except LoginException:
        continue
      keep_alive2()
if __name__ == "__main__":
    main()
