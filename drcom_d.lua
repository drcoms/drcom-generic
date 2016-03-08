#!/usr/bin/env lua

-- drcom lua version with dhcp
-- depend lua with double int32, luasocket, lua-md5
-- author: fuyumi
-- dirty and unfinished

local socket = require('socket')
local md5 = require('md5')
local udp = socket.udp()
local server = '119.39.30.18'
local port = 61440
udp:settimeout(5)
udp:setsockname('*', port)
udp:setpeername(server, port)

-- server = '119.39.30.18'
username = 'abc@defg'
password = 'hijk'
CONTROLCHECKSTATUS = '20'
ADAPTERNUM = '01'
host_ip = '6e35d852'
IPDOG = '01'
host_name = 'fuyumi'
-- PRIMARY_DNS = '58.20.127.238'
-- dhcp_server = '110.53.216.1'
AUTH_VERSION = '2600'
mac = '1c872c478e3b'
host_os = 'Windows 10'
KEEP_ALIVE_VERSION = 'd802'

function bin_xor(x, y)
    local z = 0
    for i = 0, 63 do
        if (x % 2 == 0) then
            if ( y % 2 == 1) then
                y = y - 1
                z = z + 2 ^ i
            end
        else
            x = x - 1
            if (y % 2 == 0) then
                z = z + 2 ^ i
            else
                y = y - 1
            end
        end
        y = y / 2
        x = x / 2
    end
    return z
end

function num2hex(num)
    local hexstr = '0123456789abcdef'
    local s = ''
    while num > 0 do
        local mod = math.fmod(num, 16)
        s = string.sub(hexstr, mod+1, mod+1) .. s
        num = math.floor(num / 16)
    end
    if s == '' then s = '0' end
    return s
end

function random(a, b)
    math.randomseed(tostring(os.time()):reverse():sub(1, 6))
    return math.random(a, b)
end

function dump()
    -- body
end

function challenge()
    ran = random(1, 255)
    udp:send(string.char(01,02,ran,09,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00))
    data = udp:receive(1024)
    if string.byte(data) == 02 then
        return string.sub(data, 5, 8)
    else
        assert(print(), 'error for receiving')
    end
end

function mkptk(salt, usr, pwd, mac)
    data1 = string.char(03,01,00) .. string.char(string.len(usr) + 20)
    data2 = md5.sum(string.char(03,01) .. salt .. pwd)
    data3 = string.sub(usr .. string.rep(string.char(0), 36), 1, 36)
    data4 = string.char(('0x' .. CONTROLCHECKSTATUS) + 0) .. string.char(('0x' .. ADAPTERNUM) + 0)
    f1 = num2hex(string.byte(data2,1))..num2hex(string.byte(data2,2))..num2hex(string.byte(data2,3))..num2hex(string.byte(data2,4))..num2hex(string.byte(data2,5))..num2hex(string.byte(data2,6))
    f2 = bin_xor((('0x'..f1) + 0), (('0x'..mac) + 0))
    f3 = string.sub(('000000' .. num2hex(f2)), -12)
    f4 = string.char(('0x'..(string.sub(f3,1,2)))+0)..string.char(('0x'..(string.sub(f3,3,4)))+0)..string.char(('0x'..(string.sub(f3,5,6)))+0)..string.char(('0x'..(string.sub(f3,7,8)))+0)..string.char(('0x'..(string.sub(f3,9,10)))+0)..string.char(('0x'..(string.sub(f3,11,12)))+0)
    data5 = f4
    data6 = md5.sum(string.char(01) .. pwd .. salt .. string.char(0,0,0,0))
    data7 = string.char(01) .. string.char(8,8,8,8) --issue
    data8 = string.rep(string.char(0), 12)
    data9 = string.sub(md5.sum((data1 .. data2 .. data3 .. data4 .. data5 .. data6 .. data7 .. data8) .. string.char(20, 00, 07, 11)), 1, 8)
    data10 = string.char(('0x' .. IPDOG) + 0) .. string.char(0,0,0,0)
    data11 = string.sub(host_name .. string.rep(string.char(0), 32), 1, 32)
    data12 = string.char(8,8,8,8) .. string.char(8,8,8,8)
    data13 = string.char(0,0,0,0,0,148,0,0,0,96,0,0,0,1,0,0,0,177,29,0,0,2,0,0,0)
    data14 = string.sub(host_os .. string.rep(string.char(0), 32), 1, 32)
    data15 = string.rep(string.char(0), 96)
    data16 = string.char(('0x' .. string.sub(AUTH_VERSION, 1, 2)) + 0) ..string.char(('0x' .. string.sub(AUTH_VERSION, 3, 4)) + 0)
    data17 = string.char(2,12)
    data18 = nil --checksum
    data19 = string.char(0,0)
    data20 = dump()
    data21 = string.char(0,0,0,0)
    data = data1 .. data2 .. data3 .. data4 .. data5 .. data6 .. data7 .. data8 .. data9 .. data10
    data = data .. data11 .. data11 .. data12 .. data13 ..data14 .. data15 .. data16 .. data17
    data = data .. data18 .. data19 .. data20 .. data21
    udp:send(data)
end

salt = challenge()
-- print(string.byte(salt),1,100)
-- udp:send(salt)
mkptk(salt, username, password, mac)
