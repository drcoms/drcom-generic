#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
I want to express my great thanks to the following friends
they brought me hope of this version (in QQ Group 318495368)

@Countdown to Heaven
@djj
"""
import socket
import struct
import time
import sys
import random
import platform
import os

# CONFIG
server = '61.142.108.96'
pppoe_flag = '\x00'
keep_alive2_flag = '\xdc'
# CONFIG_END

host_ip = server
IS_TEST = True
CONF = "/etc/drcom.conf"
DEBUG = False #log saves to file
if IS_TEST:
    CONF = ''
    DEBUG = True
    LOG_PATH = 'drcom_client.log'

def log(*args, **kwargs):
    s = ' '.join(args)
    if 'pkt' in kwargs and DEBUG == True:
        s += '\n\tpacket:' + kwargs['pkt'].encode('hex')
    print '[*] ', s
    if DEBUG:
        with open(LOG_PATH,'ab') as f:
            try:
                f.write(s)
                f.write('\n')
            except:
                f.write('FUCK WINDOWS' + '\n')

def dump(n):
    s = '%x' % n
    if len(s) & 1:
        s = '0' + s
    return s.decode('hex')

def gbk2utf8(string):
    try:
        if platform.uname()[0] != 'Windows':
            return string.decode('gb2312').encode().decode()
        else:
            return string.decode('gb2312')
    except Exception, e:
        return 'error for decoding'

class Socket:
    def __init__(self, server, port=61440):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(("0.0.0.0", 61440))
        log("open local port:" + str(port))
        log("DEBUG MODE:"+ str(DEBUG))
        self.server = server
        self.port = port
        self.s.settimeout(3)

    def send(self, data):
        self.s.sendto(data, (self.server, self.port))

    def recv(self):
        while True:
            data, address = self.s.recvfrom(1024)
            if data[0] == '\x4d':
                log('received message packet, dropped. message: ' + gbk2utf8(data[4:]))
                continue
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
          ret ^= struct.unpack('<I', data[i:i+4])[0]
          ret &= 0xFFFFFFFF
      return ret

    def _make_heartbeat(self, sip, challenge_seed, first=False):
        # DrcomDialExtProtoHeader - 5 bytes
        data = '\x07' # code
        data += chr(self.count) # id
        data += '\x60\x00' # length
        data += '\x03' # type
        data += '\x00' # uid length
        data += '\x00\x00\x00\x00\x00\x00' # mac
        data += sip # AuthHostIP
        if first:
            data += '\x00\x62\x00' + pppoe_flag # 非第一次则是 data += '\x00\x62\x00\x14' 
        else:
            data += '\x00\x63\x00' + pppoe_flag
        data += challenge_seed # Challenge Seed
        data += struct.pack('<I',20000711) # DRCOM_DIAL_EXT_PROTO_CRC_INIT
        data += struct.pack('<I',126)
        crc = (self._DrcomCRC32(data) * 19680126) & 0xFFFFFFFF
        data = data[:-8] + struct.pack('<I', crc) + '\x00\x00\x00\x00'
        # data += '\x7e\x00\x00\x00'
        #   data += '\x00\x00\x00\x7e'
        # - DrcomDialExtProtoHeader end -
        data += '\x00'*16 # ip1
        data += '\x00'*16 # ip2
        data += '\x00'*16 # ip3
        data += '\x00'*16 # ip4
        return data

    def send(self, s):
        while True:
            #1. challenge
            data = self._make_challenge()
            log('pppoe: send challenge request', pkt=data)
            s.send(data)
            data, address = s.recv()
            log('pppoe: received challenge response', pkt=data)

            self.count += 1
            self.count %= 0xFF
            
            #2. heartbeat
            seed = data[8:12]
            sip = data[12:16]
            if self.count != 2 and self.count != 1:
                data = self._make_heartbeat(sip=sip, challenge_seed=seed)
            else:
                data = self._make_heartbeat(sip=sip, challenge_seed=seed, first=True)
            log('pppoe: send heartbeat request', pkt=data)
            s.send(data)
            try:
                data, address = s.recv()
                log('pppoe: received heartbeat response', pkt=data)
                break
            except:
                log('pppoe: heartbeat response failed, retry')
                log('pppoe: reset idx to 0x01')
                self.count = 1
                continue

            self.count += 1
            self.count %= 0xFF


def keep_alive_package_builder(number,random,tail,type=1,first=False):
    data = '\x07'+ chr(number) + '\x28\x00\x0b' + chr(type)
    if first :
        data += '\x0f\x27'
    else:
        data += keep_alive2_flag + '\x02'
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
        log('[keep-alive2] send1', pkt=packet)
        s.sendto(packet, (svr, 61440))
        data, address = s.recvfrom(1024)
        if data[0] == '\x07' and data[2] == '\x28':
            break
        elif data[0] == '\x07' and data[2] == '\x10':
            log('[keep-alive2] recv file, resending..')
            svr_num = svr_num + 1
            packet = keep_alive_package_builder(svr_num,dump(ran),'\x00'*4,svr_num,False)
        else:
            log('[keep-alive2] recv1/unexpected', pkt=data)
    log('[keep-alive2] recv1', pkt=data)
    
    ran += random.randint(1,10)   
    packet = keep_alive_package_builder(svr_num, dump(ran),'\x00'*4,1,False)
    log('[keep-alive2] send2', pkt=packet)
    s.sendto(packet, (svr, 61440))
    while True:
        data, address = s.recvfrom(1024)
        if data[0] == '\x07':
            svr_num = svr_num + 1
            break
        else:
            log('[keep-alive2] recv2/unexpected', pkt=data)
    log('[keep-alive2] recv2', pkt=data)
    tail = data[16:20]
    

    ran += random.randint(1,10)   
    packet = keep_alive_package_builder(svr_num,dump(ran),tail,3,False)
    log('[keep-alive2] send3', pkt=packet)
    s.sendto(packet, (svr, 61440))
    while True:
        data, address = s.recvfrom(1024)
        if data[0] == '\x07':
            svr_num = svr_num + 1
            break
        else:
            log('[keep-alive2] recv3/unexpected', pkt=data)
    log('[keep-alive2] recv3', pkt=data)
    tail = data[16:20]
    log("[keep-alive2] keep-alive2 loop was in daemon.")
    
    i = svr_num
    while True:
        try:
            ran += random.randint(1,10)   
            packet = keep_alive_package_builder(i,dump(ran),tail,1,False)
            log('[keep_alive2] send',str(i), pkt=packet)
            s.sendto(packet, (svr, 61440))
            data, address = s.recvfrom(1024)
            log('[keep_alive2] recv', pkt=data)
            tail = data[16:20]
        
            ran += random.randint(1,10)   
            packet = keep_alive_package_builder(i+1,dump(ran),tail,3,False)
            s.sendto(packet, (svr, 61440))
            log('[keep_alive2] send',str(i+1), pkt=packet)
            data, address = s.recvfrom(1024)
            log('[keep_alive2] recv', pkt=data)
            tail = data[16:20]
            i = (i+2) % 0xFF
            time.sleep(10)
            #send pppoe heartbeat once
            pppoe.send(s)
        except:
            pass

def daemon():
    with open('/var/run/drcom_p.pid','w') as f:
        f.write(str(os.getpid()))

def main():
    if not IS_TEST:
        daemon()
        execfile(CONF, globals())
    log('auth svr:' + server + '\npppoe_flag:' + pppoe_flag.encode('hex') + '\nkeep_alive2_flag:' + keep_alive2_flag.encode('hex'))
    while True:
        s = Socket(server)
        pppoe = PPPOEHeartbeat(1)
        pppoe.send(s)
        keep_alive2(s, pppoe)

if __name__ == '__main__':
    main()
