# -*- coding: utf-8 -*-
"""
Created on Wed Dec 03 23:45:49 2014

@author: latyas
"""

from binascii import hexlify
import re

def hexed(s):
    ret = ''
    for i in s:
        ret += '\\x' + hex(ord(i))[2:].rjust(2, '0')
    return ret

filename = 'dr.pcapng'
f = open(filename, 'rb')
text = f.read()
offset = re.search('\xf0\x00\xf0\x00....\x03\x01', text).start() + 8
#print hexlify(text[offset:offset+330])
print 'pcapng file:', filename
print 'copy following statements to drcom.conf or overwrite field between "# CONFIG" and "# CONFIG_END" in latest-wired.py'
print '\n'
username_len = ord(text[offset+3]) - 20
username = text[offset+20:offset+20+username_len]
print 'server = \'%s\'' % '.'.join([str(ord(i)) for i in text[offset-12:offset-8]])
print 'username=\'%s\'' % username
print 'password=\'\''
print 'CONTROLCHECKSTATUS = \'%s\'' % hexed(text[offset+56])
print 'ADAPTERNUM = \'%s\'' % hexed(text[offset+57])
print 'host_ip = \'%s\'' % '.'.join(map(lambda x: str(ord(x)), text[offset+81:offset+85]))
print 'IPDOG = \'%s\'' % hexed(text[offset+105])
print 'host_name = \'%s\'' % 'DRCOMFUCKER'
print 'PRIMARY_DNS = \'%s\'' % hexed(text[offset+142 :offset+146])
print 'dhcp_server = \'%s\'' % '.'.join(map(lambda x: str(ord(x)), text[offset+146:offset+150]))
print 'AUTH_VERSION = \'%s\'' % hexed(text[offset+310:offset+312])
print 'mac = 0x%s' % hexlify(text[offset+320:offset+326])
print 'host_os = \'%s\'' % 'WINDIAOS'

# now get the version field in heartbeat
KEEP_ALIVE_VERSION = re.search('\xf0\x00\xf0\x00....\x07.\x5c\x28\x00\x0b\x01(..)', text).group(1)
print 'KEEP_ALIVE_VERSION = \'%s\'' % hexed(KEEP_ALIVE_VERSION)
