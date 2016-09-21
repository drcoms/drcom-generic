--[[
# Copyright (c) 2014-2016, latyas <latyas@gmail.com>
# Edit by Sui <sun521xiaolei@gmail.com>
]]--
require("luci.sys")
local fs = require "nixio.fs"
local nixio = require "nixio"

local drcom_running =(luci.sys.call("ps | grep drcom |egrep -v grep > /dev/null") == 0)
local client_status

if drcom_running then	
	client_status = "<font color=green>客户端运行中</font>"
else
	client_status = "<font color=red>客户端未运行</font>"
end

m = Map("drcom", translate("Dr.COM"), translate(client_status))

s = m:section(TypedSection, "drcom", translate("客户端配置"),
translate("LuCI版本的Dr.COM配置.")..
"<br />"
..[[<br /><strong>]]
..[[<a href="https://groups.google.com/d/forum/drcom-3rd-party-client" target="_blank">]]
..translate("欢迎加入本项目的讨论组(注意：需要FQ)。")
..[[</a>]]
..[[</strong><br />]]
..[[<br /><strong>]]
..[[<a href="http://shang.qq.com/wpa/qunwpa?idkey=9ebf4aff87c485f5368f17fd670076efe74c1e2e9cb436d02c62c6a017d71f52" target="_blank">]]
..translate("官方交流QQ群:318495368，欢迎加入。")
..[[</a>]]
..[[</strong><br />]]
..[[<br /><strong>]]
..[[<a href="https://github.com/drcoms" target="_blank">]]
..translate("本项目在GitHub的项目地址。")
..[[</a>]]
..[[</strong><br />]]
..[[<br /><strong>]]
..[[<a href="https://github.com/drcoms/drcom-generic/tree/master/openwrt" target="_blank">]]
..translate("查看本页面的相关自定义修改和配置说明。")
..[[</a>]]
..[[</strong><br />]]
)
s.anonymous = true

enable = s:option(Flag, "enable", translate("开启Dr.com"))

remote_server = s:option(Value, "server", translate("认证服务器地址"))
remote_server.datatype = "ip4addr"
remote_server.defaule = "192.168.1.1"

username = s:option(Value, "username", translate("用户名"))
username.default = "123"

password = s:option(Value, "password", translate("密码"))
password.datatype = "maxlength(16)"
password.password = true
password.default = "123"

host_name = s:option(Value, "host_name", translate("主机名称"))
host_name.datatype = "maxlength(32)"
host_name.default = "HP"

host_os = s:option(Value, "host_os", translate("主机操作系统"))
host_os.datatype = "maxlength(32)"
host_os.default = "DOS"

host_ip = s:option(Value, "host_ip", translate("主机IP"))
host_ip.datatype = "ip4addr"
host_ip.default = "0.0.0.0"

dhcp_server = s:option(Value, "dhcp_server", translate("DHCP服务器"))
dhcp_server.datatype = "ip4addr"
dhcp_server.default = "0.0.0.0"

mac = s:option(Value, "mac", translate("绑定MAC地址"))
mac.default = "0xaabbccddeeff"

PRIMARY_DNS = s:option(Value, "PRIMARY_DNS", translate("PRIMARY_DNS"))
PRIMARY_DNS.default = "114.114.114.114"

AUTH_VERSION = s:option(Value, "AUTH_VERSION", translate("AUTH_VERSION"))
AUTH_VERSION.default = "\x0a\x00"

KEEP_ALIVE_VERSION = s:option(Value, "KEEP_ALIVE_VERSION", translate("KEEP_ALIVE_VERSION"))
KEEP_ALIVE_VERSION.default = "\xdc\x02"

CONTROLCHECKSTATUS = s:option(Value, "CONTROLCHECKSTATUS", translate("CONTROLCHECKSTATUS"))
CONTROLCHECKSTATUS.default = "\x20"

ADAPTERNUM = s:option(Value, "ADAPTERNUM", translate("ADAPTERNUM"))
ADAPTERNUM.default = "\x01"

IPDOG = s:option(Value, "IPDOG", translate("IPDOG"))
IPDOG.default = "\x01"

local apply = luci.http.formvalue("cbi.apply")
if apply then
    io.popen("/etc/init.d/drcom restart")
end

return m
