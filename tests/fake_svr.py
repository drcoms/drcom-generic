#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import re

# CONFIG
server = '192.168.1.14'
username = 'a'
password = 'a'
host_name = 'LIYUANYUAN'
host_os = '8089D'
host_ip = '10.30.22.17'
PRIMARY_DNS = '114.114.114.114'
dhcp_server = '0.0.0.0'
mac = 0xb888e3051680
CONTROLCHECKSTATUS = '\x20'
ADAPTERNUM = '\x01'
KEEP_ALIVE_VERSION = '\xDC\x02'
AUTH_VERSION = '\x0A\x00'
IPDOG = '\x01'
ror_version = False
# CONFIG_END

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('192.168.1.14', 61440))
s.settimeout(30)
test_svr = ('192.168.1.11', 61440)
print('##### Server is listening. #####')

def receive_challenge(challenge_seed, MM):
    data, addr = s.recvfrom(1024)
    if addr == test_svr:
        print('> Received: ' + data.encode('hex'))
        if (re.match('\x01\x02[\x00-\xFF]{3}[\x00]{15}', data)):
            print('>>> Challenge packet received.')
            seed = data[2:4]
            s.sendto('\x02\x01' + seed + challenge_seed + '\x00' * 12 + ''.join([chr(int(i)) for i in host_ip.split('.')]) + '\xF0\x00' + MM + '\x00' * 34, test_svr)
            return 1
        else:
            print('>>> Unknown packet in challenge.')
            return 0
    else:
        print('>>> Not match.')
        return 0

def receive_loginpkt(challenge_seed, Auth_Information):
    data, addr = s.recvfrom(1024)
    print('> Received: ' + data.encode('hex'))
    if (data.encode('hex') == '030100153821896b162d58752557b27a03d322ff610000000000000000000000000000000000000000000000000000000000000000000000200180a96a6e00adba973cf02d13d29a8eec6605e2e8d780010a1e1611000000000000000000000000486c558f1a339aa001000000004c495955414e5955414e000000000000000000000000000000000000000000007272727200000000000000000000000000000000940000000500000001000000280a00000200000038303839440000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a00020c803256d60000b888e30516800000e913'):
        print('>>> Login packet received.')
        s.sendto('\x04\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00' + Auth_Information + '\xB0\x05\x00\x03\x01\x00', test_svr)
        s.sendto('\x4D\x3A\x04\xD5\x68\x74\x74\x70\x3A\x2F\x2F\x35\x38\x2E\x32\x30\x2E\x31\x30\x38\x2E\x31\x30\x38\x3A\x31\x30\x30\x31\x30\x2F\x6C\x67\x64\x78\x2F', test_svr)
    else:
        print('>>> Wrong authentication.')

def receive_keepalive1(Auth_Information, MM):
    data, addr = s.recvfrom(1024)
    print('>>> Received: ' + data.encode('hex'))
    if (re.match('\xFF\x38\x21\x89\x6B\x16\x2D\x58\x75\x25\x57\xB2\x7A\x03\xD3\x22\xFF\x00\x00\x00' + Auth_Information + '[\x00-\xFF]{2}', data)):
        print('>>> Keepalive 1 received.')
        s.sendto('\x07\x01\x10\x00\x06\x00\x89\x45\x04\x38\xE2\x11\x6E\x35\xAA' + MM + '\x01\x00\x00\x00\x06' + '\x00' * 17 + '\xFF\xFF\xFF\xFF\x80\x3A\x09\x00\xFF\xFF\xFF\xFF', test_svr)

def receive_keepalive2(MM, someflux):
    data, addr = s.recvfrom(1024)
    print('>>> Received: ' + data.encode('hex'))
    if (re.match(r'\x07[\x00-\xFF]\x28\x00\x0B\x01\x0F\x27\x2F\x12[\x00]{30}', data)):
        print('>>> Keepalive 2 Misc_Type_1 partA received.')
        # send Misc_Type file
        s.sendto('\x07\x00\x10\x01\x0B\x06' + KEEP_ALIVE_VERSION + '\x00' * 8 + MM, test_svr)
        receive_keepalive2(MM, someflux)
    elif (re.match(r'\x07[\x00-\xFF]\x28\x00\x0B\x01' + KEEP_ALIVE_VERSION + r'\x2F\x12[\x00]{6}[\x00-\xFF]{4}[\x00]{20}', data)):
        print('>>> Keepalive 2 Misc_Type_1 partB received.')
        # send Misc_Type 2
        s.sendto('\x07\x00\x28\x00\x0B\x02' + KEEP_ALIVE_VERSION + '\x2F\x12' + '\x00' * 6 + someflux + '\x00' * 20, test_svr)
        data, addr = s.recvfrom(1024)
        print('>>> Received: ' + data.encode('hex'))
        foo = ''.join([chr(int(i)) for i in host_ip.split('.')])
        if (re.match(r'\x07[\x00-\xFF]\x28\x00\x0B\x03' + KEEP_ALIVE_VERSION + '\x2F\x12[\x00]{6}' + someflux + r'[\x00]{8}' + foo + '[\x00]{8}', data)):
            print('>>> Keepalive 2 Misc_Type_3 received.')
            # send Misc_Type 4
            s.sendto('\x07\x00\x28\x00\x0B\x04' + KEEP_ALIVE_VERSION + '\x2F\x12' + '\x00' * 6 + someflux + '\x00' * 20, test_svr)
            print('>>> Keepalive in loop. <<<')

def main():
    challenge_seed = '\x52\x6C\xE4\x00'
    MM = '\xA8\xA6\x00\x00\x70\xCD\xA0\xA3\x00\x00\x00\x00' + KEEP_ALIVE_VERSION + '\x00\x00'
    Auth_Information = '\x44\x72\x63\x6F\x77\x27\x20\xCA\xED\x05\x6E\x35\xAA\x8B\x01\xFB'
    val = receive_challenge(challenge_seed, MM)
    someflux = '\x13\x38\xE2\x11'
    if val:
        receive_loginpkt(challenge_seed, Auth_Information)
        while 1:
            receive_keepalive1(Auth_Information, MM)
            receive_keepalive2(MM, someflux)


if __name__ == '__main__':
    main()
