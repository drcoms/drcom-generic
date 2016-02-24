#!/usr/bin/env python
# -*- coding: utf-8 -*-

#history:
# 1.Please edit this file in editors which supports UNIX files if you are using Windows OS
# 2.tests passed on v0.8 u62R0
# 3.edit basic configuration first.
# 4.Code adapted for ChongQing University Dr.com Client && Server
# 						--By GY
#Date: 2015.07.01  
#Author:       cquhsk
#Chongqing University
#test passed in win7/RHEL6
'''
Add notes
Increase hide login password
Modify socket reuse mode
Repair:closed socket when process ended 
Increase the logging can be configured
'''

#Version:      v2b
# 2015.11.11


import socket, struct, time
from hashlib import md5
import sys
import urllib2
import re

import gc
import pdb

#Hide input password 
import getpass

class ChallengeException (Exception):
    def __init__(self):
        pass

class LoginException (Exception):
    def __init__(self):
        pass
#if you don't want to input the usrname and password
#Please comment out the two lines,replease them with fixed value
username = raw_input("Your login ID:")
password=getpass.getpass(prompt='Password: ',stream=None)
#Example:
#username = "Your login ID"
#password = "your password here"

#create a UDPsocket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port=61440
#socket option：
#Reusable:SO_REUSEADDR=1,the port will be release when socket is closed
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

s.settimeout(3)
SALT = '' #It is a random number,server return it to client when challenge(function) run end
UNLIMITED_RETRY = True
EXCEPTION = False
DEBUG = True# false:print and log nothing
LOGHISTORY = False#log all history
LOGFILE='drcom_client.log'

    
s.bind(("0.0.0.0", port))
#linux:
#find the port：lsof -i:61440
#kill pid

#windows：netstat -ano
#Task Manager:kill
#or:taskkill /pid 1988 /f 

#basic configuration
host_name = "test"
host_os = "8089D"
host_ip = "172.25.173.65"#you don't need to edit
server = "202.202.0.163"  # Auth server ip
dhcp_server = "202.202.0.50"
mac_flag = "\x02"  # \x01 for no binding \x02 for mac-ip binding
mac = 0x123456789ABC

#*args不定参数，放在tuple中
#log the history
def log(*args, **kwargs):
    if DEBUG:
        s = ' '.join(args)
        print s #don't print in stdout
        with open(LOGFILE,'a') as f:
            f.write(s + '\n')


        
#Keep trying to connect the server, until success
#Signed in,and return a string from the response packet frame tail
def login(usr, pwd, svr):
    import random    
    i = 0
    while True:
        salt = challenge(svr,time.time()+random.randint(0xF,0xFF))#尝试通信成功
        SALT = salt
        packet = mkpkt(salt, usr, pwd, mac)#用户信息生成数据包
        if LOGHISTORY:
            log('[login] send',packet.encode('hex'))
        s.sendto(packet, (svr, port))#发送用户信息到认证服务器
        data, address = s.recvfrom(1024)#接收认证服务器的响应包
        if LOGHISTORY:
            log('[login] recv',data.encode('hex'))
            log('[login] packet sent.')
        if address == (svr, port):#正确收包
            if data[0] == '\x04':#标志正确,登入成功
              log('[login] loged in')
              break
            else:
              continue#登入失败，重复尝试
        else:
            if i >= 5 and UNLIMITED_RETRY == False :#尝试次数限制
              log('[login] exception occured.')
              sys.exit(1)#退出程序
            else:
              continue
            
    if LOGHISTORY:
        log('[login] login sent')
    #0.8 changed:
    return data[23:39]#返回认证服务器的响应包的一部分数据，（理解为密钥）


#不断尝试通信，直到成功
#发送随机数，接收数据包，返回接收数据包的帧尾
def challenge(svr,ran):#服务器地址，随机数
    while True:
        #H:unsigned short, <:小端对齐
        #把数据封装成字符串
        t = struct.pack("<H", int(ran)%(0xFFFF))
        #发送到svr
        #数据帧结构：
        #"\x01\x02"+t+"\x09"+"\x00"*15
        s.sendto("\x01\x02"+t+"\x09"+"\x00"*15, (svr, port))
        if LOGHISTORY:
            log('[challenge] send: ',"\x01\x02"+t+"\x09"+"\x00"*15)
        try:#接收，正确收包则返回data[4:8]
            data, address = s.recvfrom(1024)
            if LOGHISTORY:
                log('[challenge] recv:',data.encode('hex'))
        except:
            log('[challenge] timeout, retrying...')
            continue
        
        if address == (svr, port):#正常接收
            break
        else:#通信失败，再次尝试
            continue
        
    if LOGHISTORY:
        log('[DEBUG] challenge:' + data.encode('hex'))
    if data[0] != '\x02':
        raise ChallengeException
    if LOGHISTORY:
        log('[challenge] challenge packet sent.')
    return data[4:8]

#用户信息生成数据包
#\x03\x01\x00+用户名长度+密码加密+用户名+客户端版本+是否绑定mac
def mkpkt(salt, usr, pwd, mac):
    data = '\x03\x01\x00'+chr(len(usr)+20)#用户名长度+20
    data += md5sum('\x03\x01'+salt+pwd)#密码加密
    data += usr.ljust(36, '\x00')#用户名后面补0
    #ljust() 方法返回一个原字符串左对齐,并使用空格填充至指定长度的新字符串。
    #如果指定的长度小于原字符串的长度则返回原字符
    
    data += '\x20' #client version: \x20 for U62, \x0c for U60
    data += '\x02' #mac flag: 1 for no any binding, 2 for mac-ip binding
    data += dump(int(data[4:10].encode('hex'),16)^mac).rjust(6,'\x00') #mac xor md51
    data += md5sum("\x01" + pwd + salt + '\x00'*4) #md52#再次加密？
    data += '\x01' # number of ip
    data += ''.join([chr(int(i)) for i in host_ip.split('.')]) #x.x.x.x -> IP地址
    data += '\00'*4 #your ipaddress 2
    data += '\00'*4 #your ipaddress 3
    data += '\00'*4 #your ipaddress 4
    data += md5sum(data + '\x14\x00\x07\x0b')[:8] #md53
    data += '\x01' #ipdog
    data += '\x00'*4 #delimeter
    data += host_name.ljust(32, '\x00')
    data += '\x08\x08\x08\x08' #primary dns: 8.8.8.8
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
    data += '\x0a\x00' # for u64, \x1a\x00
    data += '\x02\x0c'
    data += checksum(data+'\x01\x26\x07\x11\x00\x00'+dump(mac))
    data += '\x00\x00' #delimeter
    data += dump(mac)
    data += '\x00' # auto logout / default: False
    data += '\x00' # broadcast mode / default : False
    data += '\xe9\x13' #unknown, filled numbers randomly =w=
    
    if LOGHISTORY:
        log('[mkpkt]',data.encode('hex'))
    return data

"""\
注意，传入 hashlib.md5()的应该是文件内容而不是文件名,这样才是对文件内容产生md5校验码；
调用了hashlib.md5()后返回的是一个对象，
想要获得linux下md5sum同样的效果，还要调用一下hexdigest()方法。
如果要对一个比较大的文件进行校验，将会把文件内容一次读入内存，造成性能上的缺陷。
个人比较推荐从http://ryan-liu.iteye.com/blog/1530029提供的代码：
"""
def md5sum(str_content):
    m = md5()#获取加密对象
    m.update(str_content)#指定需要加密的字符串
    return m.digest()#返回加密后的字符串


def dump(n):
    s = '%x' % n
    if len(s) & 1:
        s = '0' + s
    return s.decode('hex')

def ror(md5, pwd):
    ret = ''
    for i in range(len(pwd)):
        #密码与md5异或
        x = ord(md5[i]) ^ ord(pwd[i])#ord()将字符转换成ASCII码
        ret += chr(((x<<3)&0xFF) + (x>>5))#chr()将ASCII码转换成字符
    return ret

#根据参数进行封装数据
#对number,type,tail进行封装；根据type的值决定是否加入主机IP
#data='07'+number+'28000b'+type+'d8022f12000000000000'+tail+'00000000'
#+host_ip_part(if type=3)+'\x00' * 16
#first,random参数未使用
def keep_alive_package_builder(number,tail,type=1):
    data = '\x07'+ chr(number) + '\x28\x00\x0b' + chr(type)
    data += '\xd8\x02'
    data += '\x2f\x12' + '\x00' * 6
    data += tail
    data += '\x00' * 4
    if type == 3:#尾部加上主机ip
        foo = ''.join([chr(int(i)) for i in host_ip.split('.')]) # host_ip
        crc = '\x00' * 4 #没有进行crc
        data += crc + foo + '\x00' * 8 #crc:4字节，foo：4字节，\x00:8字节；共16字节
    else: #packet type = 1
        data += '\x00' * 16 #16字节全零
    return data

#对数据进行crc，这个函数没有被调用
def packet_CRC(content):
    ret = 0
    for i in re.findall('..', content):
        ret ^= struct.unpack('>h', i)[0]
        ret &= 0xFFFF
    ret = ret * 0x2c7
    return ret#返回检验码

def keep_alive1(salt,tail,pwd,svr):#发送带认证信息和密码的数据包，接收服务器响应
    foo = struct.pack('!H',int(time.time())%0xFFFF)#随时间变化的数
    data = '\xff' + md5sum('\x03\x01'+salt+pwd) + '\x00\x00\x00'#密码加密
    data += tail+foo + '\x00\x00\x00\x00'#封装随机数据包
    #log('[keep_alive1] send',data.encode('hex'))
    s.sendto(data, (svr, port))#发送带认证信息和密码的数据包
    while True:
        data, address = s.recvfrom(1024)
        if data[0] == '\x07':#正常响应，则退出函数
            break
        else:#响应数据包异常，重新接收
            log('[keep-alive1]recv/not expected',data.encode('hex'))
    #log('[keep-alive1] recv',data.encode('hex'))

            
#这个函数很长
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
    svr = server#svr认证服务器地址
    
    #receive file
    #0---------------------------------------------------------------------
    #number=0,tail='\x00'*4,type=1
    packet = keep_alive_package_builder(0,'\x00'*4,1)#生成包
    log('[keep-alive2] send 1',packet.encode('hex'))
    while True:
        s.sendto(packet, (svr, port))#发送包
        data, address = s.recvfrom(1024)
        if data.startswith('\x07'):#开始标志正确，跳出循环
            break
        else:#开始标志错误，循环发送
            log('[keep-alive2] recv/unexpected',data.encode('hex'))
    #log('[keep-alive2] recv 1',data.encode('hex'))
    #1---------------------------------------------------------------------
    #number=1,tail='\x00'*4,type=1
    packet = keep_alive_package_builder(1,'\x00'*4,1)
    log('[keep-alive2] send 2',packet.encode('hex'))
    s.sendto(packet, (svr, port))#发送随机包
    while True:
        data, address = s.recvfrom(1024)#接收
        if data[0] == '\x07':#接收数据开始标志正确，跳出循环
            break
    #log('[keep-alive2] recv 2',data.encode('hex'))
    tail = data[16:20]#截取尾部
    #2---------------------------------------------------------------------
    #number=2,tail,type=3
    packet = keep_alive_package_builder(2,tail,3)
    log('[keep-alive2] send 3',packet.encode('hex'))
    s.sendto(packet, (svr, port))#发送随机包
    while True:
        data, address = s.recvfrom(1024)
        if data[0] == '\x07':#接收数据开始标志正确，跳出循环
            break
    #log('[keep-alive2] recv 3',data.encode('hex'))
    tail = data[16:20]#截取尾部
    #log("[keep-alive2] keep-alive2 loop was in daemon.")
    #3---------------------------------------------------------------------
    i = 3
    log('while True:...')
    while True:
      try:
        #3---------------------------------------------------------------------
        #number=3,tail,type=1
        packet = keep_alive_package_builder(i,tail,1)
        #log('DEBUG: keep_alive2,packet 4\n',packet.encode('hex'))
        if LOGHISTORY:
            log('[keep_alive2] send',str(i),packet.encode('hex'))
        s.sendto(packet, (svr, port))#发送随机包
        data, address = s.recvfrom(1024)#接收响应包
        if LOGHISTORY:
            log('[keep_alive2] recv',data.encode('hex'))
        tail = data[16:20]#截取尾部
        #log('DEBUG: keep_alive2,packet 4 return\n',data.encode('hex'))
        #4---------------------------------------------------------------------
        #number=4,tail,type=3
        packet = keep_alive_package_builder(i+1,tail,3)
        #log('DEBUG: keep_alive2,packet 5\n',packet.encode('hex'))
        s.sendto(packet, (svr, port))
        if LOGHISTORY:
            log('[keep_alive2] send',str(i+1),packet.encode('hex'))
        data, address = s.recvfrom(1024)
        if LOGHISTORY:
            log('[keep_alive2] recv',data.encode('hex'))
        tail = data[16:20]
        #log('DEBUG: keep_alive2,packet 5 return\n',data.encode('hex'))
        i = (i+2) % 0xFF#i=5
        log('sleep 20s...')
        time.sleep(20)#进入睡眠
        log('keep_alive1 ...')
        keep_alive1(*args)#调用函数keep_alive1
        log('keep_alive2 ...')
      except:#异常-->继续
        pass



def checksum(s):#检测校验码
    ret = 1234
    for i in re.findall('....', s):
        ret ^= int(i[::-1].encode('hex'), 16)
    ret = (1968 * ret) & 0xffffffff
    return struct.pack('<I', ret)

def empty_socket_buffer():
    log('starting to empty socket buffer')
    try:
        while True:
            data, address = s.recvfrom(1024)
            log('recived sth unexcepted',data.encode('hex'))
            if s == '':
                break
    except: #get exception means it has done.
        log('exception in empty_socket_buffer')
    log('emptyed')

def running():
    log("auth svr:"+server+"\nusername:"+username+"\nmac:"+str(hex(mac)))
    while True:
        try:
            package_tail = login(username, password, server)#登入，返回服务器响应数据帧的一部分数据
        except LoginException:#异常，不断尝试登入
            continue
        log('package_tail',package_tail.encode('hex'))
        #keep_alive1 is fucking bullshit!
        empty_socket_buffer()#清空socket buffer

        #发送带认证信息和密码的数据包，接收服务器响应
        log('run keep_alive1...')
        keep_alive1(SALT,package_tail,password,server)
        #empty_socket_buffer()
        log('run keep_alive2...')
        keep_alive2(SALT,package_tail,password,server)
    #close the socket,release the port
    s.close()
      
if __name__ == "__main__":
    running()
    

