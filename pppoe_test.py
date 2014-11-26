#coding=utf-8
import socket, struct, time
from hashlib import md5
from binascii import hexlify
import sys
import random
import os

# First step: use builtin pppoe client of your OS
# 	      then use this script
server = '61.142.108.96' # Edit this
host_ip = server
DEBUG = True #log saves to file
LOG_PATH = 'drcom_client.log'

def log(*args, **kwargs):
    s = ' '.join(args)
    print '[*] ', s
    if DEBUG:
      with open(LOG_PATH,'a') as f:
          f.write(s + '\n')

def dump(n):
    s = '%x' % n
    if len(s) & 1:
        s = '0' + s
    return s.decode('hex')

class Socket:

    def __init__(self, server, port=61440):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(("0.0.0.0", 61440))
        log("open local port:" + str(port))
        self.server = server
        self.port = port

    def send(self, data):
        self.s.sendto(data, (self.server, self.port))

    def recv(self):
        while True:
            data, address = self.s.recvfrom(1024)
            if data[0] == '\x4d':
                log('received message packet, dropped')
                continue
            break
        return data, address

    def get_socket(self):
        return self.s

    def sendto(self, data, *args):
        self.send(data)

    def recvfrom(self, *args):
        return self.recv()



class PPPOEHeartbeat:

    def __init__(self, num=1):
        self.count = num # 计数器
    def _make_challenge(self):
        data = '\x07'
        data += chr(self.count)
        data += '\x08\x00\x01\x00'
        data+= '\x00\x00'
        return data

    def _DrcomCRC32(self, data, init = 0):
      ret = init
      for i in range(len(data))[::4]:
          ret ^= struct.unpack('I', data[i:i+4])[0]
          ret &= 0xFFFFFFFF
      return ret

    def _make_heartbeat(self, sip, challenge_seed, first=True):
        # DrcomDialExtProtoHeader - 5 bytes
        data = '\x07' # code
        data += chr(self.count) # id
        data += '\x60\x00' # length
        data += '\x03' # type
        data += '\x00' # uid length
        data += '\x00\x00\x00\x00\x00\x00' # mac
        data += sip # AuthHostIP
        if first:
            data += '\x00\x62\x00\xd8' # 非第一次则是 data += '\x00\x62\x00\x14' 
        else:
            data += '\x00\x62\x00\xd8'
        data += challenge_seed # Challenge Seed
        data += struct.pack('I',20000711) # DRCOM_DIAL_EXT_PROTO_CRC_INIT
        data += struct.pack('I',126)
        crc = (self._DrcomCRC32(data) * 19680126) & 0xFFFFFFFF
        data = data[:-8] + struct.pack("I", crc) + '\x00\x00\x00\x00'
        # data += '\x7e\x00\x00\x00'
        #   data += '\x00\x00\x00\x7e'
        # - DrcomDialExtProtoHeader end -
        data += '\x00'*16 # ip1
        data += '\x00'*16 # ip2
        data += '\x00'*16 # ip3
        data += '\x00'*16 # ip4
        return data

    def send(self, s):
        socket.setdefaulttimeout(1)
        while True:
            #1. challenge
            data = self._make_challenge()
            print '[*] challenge request:', hexlify(data)
            s.send(data)
            data, address = s.recv()
            print '[*] challenge response:', hexlify(data)

            self.count += 1

            #2. heartbeat
            seed = data[8:12]
            sip = data[12:16]
            data = self._make_heartbeat(sip=sip, challenge_seed=seed)
            print '[*] heartbeat request:', hexlify(data)
            s.send(data)
            try:
                data, address = s.recv()
                print '[*] heartbeat response:', hexlify(data)
                break
            except:
                print '[*] failed'
                continue

            self.count += 1
        socket.setdefaulttimeout(3)


def keep_alive_package_builder(number,random,tail,type=1,first=False):
    data = '\x07'+ chr(number) + '\x28\x00\x0b' + chr(type)
    if first :
      data += '\x0f\x27'
    else:
      data += '\xd8\x02'
    data += '\x2f\x12' + '\x00' * 6
    data += tail
    data += '\x00' * 4
    #data += struct.pack("!H",0xdc02)
    if type == 3:
      foo = ''.join([chr(int(i)) for i in host_ip.split('.')]) # host_ip
      #CRC
      # edited on 2014/5/12, filled zeros to checksum
      # crc = packet_CRC(data+foo)
      crc = '\x00' * 4
      #data += struct.pack("!I",crc) + foo + '\x00' * 8
      data += crc + foo + '\x00' * 8
    else: #packet type = 1
      data += '\x00' * 16
    return data

def keep_alive2(s, pppoe):
    tail = ''
    packet = ''
    svr = server
    
    ran = random.randint(0,0xFFFF)
    ran += random.randint(1,10)   
    # 2014/10/15 add by latyas, maybe svr sends back a file packet
    svr_num = 0
    packet = keep_alive_package_builder(svr_num,dump(ran),'\x00'*4,1,True)
    while True:
        log('[keep-alive2] send1',packet.encode('hex'))
        s.sendto(packet, (svr, 61440))
        data, address = s.recvfrom(1024)
        if data[0] == '\x07' and data[2] == '\x28':
            break
        elif data[0] == '\x07' and data[2] == '\x10':
            log('[keep-alive2] recv file, resending..')
            svr_num = svr_num + 1
            packet = keep_alive_package_builder(svr_num,dump(ran),'\x00'*4,svr_num,False)
        else:
            log('[keep-alive2] recv1/unexpected',data.encode('hex'))
    log('[keep-alive2] recv1',data.encode('hex'))
    
    ran += random.randint(1,10)   
    packet = keep_alive_package_builder(svr_num, dump(ran),'\x00'*4,1,False)
    log('[keep-alive2] send2',packet.encode('hex'))
    s.sendto(packet, (svr, 61440))
    while True:
        data, address = s.recvfrom(1024)
        if data[0] == '\x07':
            svr_num = svr_num + 1
            break
        else:
            log('[keep-alive2] recv2/unexpected',data.encode('hex'))
    log('[keep-alive2] recv2',data.encode('hex'))
    tail = data[16:20]
    

    ran += random.randint(1,10)   
    packet = keep_alive_package_builder(svr_num,dump(ran),tail,3,False)
    log('[keep-alive2] send3',packet.encode('hex'))
    s.sendto(packet, (svr, 61440))
    while True:
        data, address = s.recvfrom(1024)
        if data[0] == '\x07':
            svr_num = svr_num + 1
            break
        else:
            log('[keep-alive2] recv3/unexpected',data.encode('hex'))
    log('[keep-alive2] recv3',data.encode('hex'))
    tail = data[16:20]
    log("[keep-alive2] keep-alive2 loop was in daemon.")
    
    i = svr_num
    while True:
      try:
        ran += random.randint(1,10)   
        packet = keep_alive_package_builder(i,dump(ran),tail,1,False)
        log('[keep_alive2] send',str(i),packet.encode('hex'))
        s.sendto(packet, (svr, 61440))
        data, address = s.recvfrom(1024)
        log('[keep_alive2] recv',data.encode('hex'))
        tail = data[16:20]
        
        ran += random.randint(1,10)   
        packet = keep_alive_package_builder(i+1,dump(ran),tail,3,False)
        s.sendto(packet, (svr, 61440))
        log('[keep_alive2] send',str(i+1),packet.encode('hex'))
        data, address = s.recvfrom(1024)
        log('[keep_alive2] recv',data.encode('hex'))
        tail = data[16:20]
        i = (i+2) % 0xFF
        time.sleep(10)
      except:
        pass


def main():
    while True:
        s = Socket(server)
        #1 pppoe heartbeat
        pppoe = PPPOEHeartbeat(1)
        pppoe.send(s)
        #2 empty notification packets
        keep_alive2(s, pppoe)

main()
