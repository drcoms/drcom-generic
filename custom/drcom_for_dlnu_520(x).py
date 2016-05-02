#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, struct, time
from hashlib import md5
import sys
import os
import random

# CONFIG
server = '172.16.192.111'
username=''
password=''
CONTROLCHECKSTATUS = '\x00'
ADAPTERNUM = '\x00'
host_ip = '0.210.30.0'
IPDOG = '\x00'
host_name = 'DRCOMFUCKER'
PRIMARY_DNS = '0.0.0.0'
dhcp_server = '0.0.0.0'
AUTH_VERSION = '\x20\x1a'
mac = 0xb888e3051680
host_os = 'WINDIAOS'
KEEP_ALIVE_VERSION = '\xdc\x02'
# CONFIG_END

nic_name = '' #Indicate your nic, e.g. 'eth0.2'.nic_name
bind_ip = '0.0.0.0'

class ChallengeException (Exception):
    def __init__(self):
        pass

class LoginException (Exception):
    def __init__(self):
        pass

def bind_nic():
    try:
        import fcntl
        def get_ip_address(ifname):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', ifname[:15])
            )[20:24])
        return get_ip_address(nic_name)
    except ImportError as e:
        print('Indicate nic feature need to be run under Unix based system.')
        return '0.0.0.0'
    except IOError as e:
        print(nic_name + 'is unacceptable !')
        return '0.0.0.0'
    finally:
        return '0.0.0.0'

if nic_name != '':
    bind_ip = bind_nic()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((bind_ip, 61440))

s.settimeout(3)
SALT = ''
IS_TEST = True
# specified fields based on version
CONF = "/etc/drcom.conf"
UNLIMITED_RETRY = True
EXCEPTION = False
DEBUG = False #log saves to file
LOG_PATH = '/var/log/drcom_client.log'
if IS_TEST:
    DEBUG = True
    LOG_PATH = 'drcom_client.log'


def log(*args, **kwargs):
    s = ' '.join(args)
    print s
    if DEBUG:
        with open(LOG_PATH,'a') as f:
            f.write(s + '\n')

def challenge(svr,ran):
    while True:
        t = struct.pack("<H", int(ran)%(0xFFFF))
        s.sendto("\x01\x02"+t+"\x09"+"\x00"*15, (svr, 61440))
        try:
            data, address = s.recvfrom(1024)
            log('[challenge] recv',data.encode('hex'))
        except:
            log('[challenge] timeout, retrying...')
            continue
        
        if address == (svr, 61440):
            break
        else:
            continue
    log('[DEBUG] challenge:\n' + data.encode('hex'))
    if data[0] != '\x02':
        raise ChallengeException
    log('[challenge] challenge packet sent.')
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

# def ror(md5, pwd):
#     ret = ''
#     for i in range(len(pwd)):
#         x = ord(md5[i]) ^ ord(pwd[i])
#         ret += chr(((x<<3)&0xFF) + (x>>5))
#     return ret

def keep_alive_package_builder(number,random,tail,type=1,first=False):
    data = '\x07'+ chr(number) + '\x28\x00\x0b' + chr(type)
    if first :
        data += '\x0f\x27'
    else:
        data += KEEP_ALIVE_VERSION
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

# def packet_CRC(s):
#     ret = 0
#     for i in re.findall('..', s):
#         ret ^= struct.unpack('>h', i)[0]
#         ret &= 0xFFFF
#     ret = ret * 0x2c7
#     return ret

def keep_alive2(*args):
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
    ran = random.randint(0,0xFFFF)
    ran += random.randint(1,10)   
    # 2014/10/15 add by latyas, maybe svr sends back a file packet
    svr_num = 0
    packet = keep_alive_package_builder(svr_num,dump(ran),'\x00'*4,1,True)
    while True:
        log('[keep-alive2] send1',packet.encode('hex'))
        s.sendto(packet, (svr, 61440))
        data, address = s.recvfrom(1024)
        log('[keep-alive2] recv1',data.encode('hex'))
        if data.startswith('\x07\x00\x28\x00') or data.startswith('\x07' + chr(svr_num)  + '\x28\x00'):
            break
        elif data[0] == '\x07' and data[2] == '\x10':
            log('[keep-alive2] recv file, resending..')
            svr_num = svr_num + 1
            packet = keep_alive_package_builder(svr_num,dump(ran),'\x00'*4,1, False)
        else:
            log('[keep-alive2] recv1/unexpected',data.encode('hex'))
    #log('[keep-alive2] recv1',data.encode('hex'))
    
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
            #log('DEBUG: keep_alive2,packet 4\n',packet.encode('hex'))
            log('[keep_alive2] send',str(i),packet.encode('hex'))
            s.sendto(packet, (svr, 61440))
            data, address = s.recvfrom(1024)
            log('[keep_alive2] recv',data.encode('hex'))
            tail = data[16:20]
            #log('DEBUG: keep_alive2,packet 4 return\n',data.encode('hex'))
        
            ran += random.randint(1,10)   
            packet = keep_alive_package_builder(i+1,dump(ran),tail,3,False)
            #log('DEBUG: keep_alive2,packet 5\n',packet.encode('hex'))
            s.sendto(packet, (svr, 61440))
            log('[keep_alive2] send',str(i+1),packet.encode('hex'))
            data, address = s.recvfrom(1024)
            log('[keep_alive2] recv',data.encode('hex'))
            tail = data[16:20]
            #log('DEBUG: keep_alive2,packet 5 return\n',data.encode('hex'))
            i = (i+2) % 0xFF
            time.sleep(20)
            keep_alive1(*args)
        except:
            pass

    
import re
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
    data += CONTROLCHECKSTATUS
    data += ADAPTERNUM
    data += dump(int(data[4:10].encode('hex'),16)^mac).rjust(6,'\x00') #mac xor md51
    data += md5sum("\x01" + pwd + salt + '\x00'*4) #md52
    data += '\x01' # number of ip
    #data += '\x0a\x1e\x16\x11' #your ip address1, 10.30.22.17
    data += ''.join([chr(int(i)) for i in host_ip.split('.')]) #x.x.x.x -> 
    data += '\00'*4 #your ipaddress 2
    data += '\00'*4 #your ipaddress 3
    data += '\00'*4 #your ipaddress 4
    data += md5sum(data + '\x14\x00\x07\x0b')[:8] #md53
    data += IPDOG
    data += '\x00'*4 #delimeter
    data += host_name.ljust(32, '\x00')
    data += ''.join([chr(int(i)) for i in PRIMARY_DNS.split('.')]) #primary dns
    data += ''.join([chr(int(i)) for i in dhcp_server.split('.')]) #DHCP server
    data += '\x00\x00\x00\x00' #secondary dns:0.0.0.0
    data += '\x00' * 8 #delimeter
    data += '\x94\x00\x00\x00' # unknow
    data += '\x05\x00\x00\x00' # os major
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
    data += '\xe9\x13' #unknown, filled numbers randomly =w=
    
    log('[mkpkt]',data.encode('hex'))
    return data

def login(usr, pwd, svr):
    import random
    global SALT
 
    i = 0
    while True:
        salt = challenge(svr,time.time()+random.randint(0xF,0xFF))
        SALT = salt
        packet = mkpkt(salt, usr, pwd, mac)
        log('[login] send',packet.encode('hex'))
        s.sendto(packet, (svr, 61440))
        data, address = s.recvfrom(1024)
        log('[login] recv',data.encode('hex'))
        log('[login] packet sent.')
        if address == (svr, 61440):
            if data[0] == '\x04':
                log('[login] loged in')
                break
            else:
                log('[login] login failed.')
                if IS_TEST:
                    time.sleep(3)
                else:
                    time.sleep(30)
                continue
        else:
            if i >= 5 and UNLIMITED_RETRY == False :
                log('[login] exception occured.')
                sys.exit(1)
            else:
                continue
            
    log('[login] login sent')
    #0.8 changed:
    return data[23:39]
    #return data[-22:-6]

def keep_alive1(salt,tail,pwd,svr):
    foo = struct.pack('!H',int(time.time())%0xFFFF)
    data = '\xff' + md5sum('\x03\x01'+salt+pwd) + '\x00\x00\x00'
    data += tail
    data += foo + '\x00\x00\x00\x00'
    log('[keep_alive1] send',data.encode('hex'))

    s.sendto(data, (svr, 61440))
    while True:
        data, address = s.recvfrom(1024)
        if data[0] == '\x07':
            break
        else:
            log('[keep-alive1]recv/not expected',data.encode('hex'))
    log('[keep-alive1] recv',data.encode('hex'))

def empty_socket_buffer():
#empty buffer for some fucking schools
    log('starting to empty socket buffer')
    try:
        while True:
            data, address = s.recvfrom(1024)
            log('recived sth unexpected',data.encode('hex'))
            if s == '':
                break
    except:
        # get exception means it has done.
        log('exception in empty_socket_buffer')
        pass
    log('emptyed')
def daemon():
    with open('/var/run/jludrcom.pid','w') as f:
        f.write(str(os.getpid()))
        
def main():
    if not IS_TEST:
        daemon()
        execfile(CONF, globals())
    log("auth svr:"+server+"\nusername:"+username+"\npassword:"+password+"\nmac:"+str(hex(mac)))
    log(bind_ip)
    while True:
      try:
        package_tail = login(username, password, server)
      except LoginException:
        continue
      log('package_tail',package_tail.encode('hex'))
      #keep_alive1 is fucking bullshit!
      empty_socket_buffer()
      keep_alive1(SALT,package_tail,password,server)
      keep_alive2(SALT,package_tail,password,server)
if __name__ == "__main__":
    main()
