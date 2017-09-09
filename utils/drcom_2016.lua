--Wireshark dr.com协议插件
--By Lixiang，douniwan5788
--Last Modify   2016/10/22

do --do...end是Lua语言的语句块关键字
	--创建一个Proto类的对象，表示一种协议
	local p_drcom = Proto("drcom","Dr.com V2016");

	--创建几个ProtoField对象，就是主界面中部Packet Details窗格中能显示的那些属性
	local pf = p_drcom.fields

	pf.f1_1dir =    ProtoField.uint8("drcom.times","Times of Dial",base.DEC)
	pf.f1_unkonw01 =    ProtoField.bytes("drcom.unkonwn","unkonwn01",base.NONE)
	pf.f1_unkonw02 =    ProtoField.bytes("drcom.fixed","Fixed ver? ",base.NONE)
	pf.f2_1dir =    ProtoField.bytes("drcom.challenge","Challenge")

	local t_code = {[0x01]="Start Request",
			[0x02]="Start Response",
			[0x03]="Login Auth",
			[0x04]="Success",
			[0x05]="Failure",
			[0x06]="Logout Auth",
			[0x07]="Misc",
			[0x08]="Unknown, Attention！！",
			[0x09]="New Password",
			[0x4d]="Message",
			[0xfe]="Alive 4 client",
			[0xff]="Alive, Client to Server per 20s"
			}
	pf.f_code = ProtoField.uint8("drcom.code","Code",base.HEX,t_code)
	pf.f_authtype = ProtoField.uint8("drcom.authtype","AuthType",base.HEX)
	pf.f_subcode = ProtoField.uint8("drcom.subcode","Subcode",base.HEX)
	pf.f_cmdlen = ProtoField.uint8("drcom.cmdlen","CMDLength",base.HEX)
	
	local t_type = {[0x25]="Out of money",  --0x4d25
			[0x26]="alive_4_server",    --ox4d26
			[0x38]="Server Infomation", --ox4d38
			[0x3a]="Notice"     --ox4d3a
			}
	pf.f_type =     ProtoField.uint8("drcom.type","Type",base.HEX,t_type)

	local t_07type ={   [0x0800]="0800",
			[0x1000]="Response for Alive",
			[0x1001]="File",
			[0x2800]="2800",
			[0x3000]="3000",
			[0xf400]="Info username,hostname",
			}
	pf.f_07type =   ProtoField.uint16("drcom.07type","Type",base.HEX,t_07type)

	local t_misctype ={ [0x00]="Misc Type 0,Response for Alive",
			[0x01]="Misc Type 1",
			[0x02]="Misc Type 2",
			[0x03]="Misc Type 3 (CRC included)",
			[0x04]="Misc Type 4",
			[0x06]="Misc Type 1,File",
			}
	pf.f_misctype = ProtoField.uint8("drcom.step","Step",base.HEX,t_misctype)

	pf.f_usernamelen = ProtoField.uint8("drcom.usernamelen","Username length",base.DEC)
	pf.f_md5a = ProtoField.bytes("drcom.md5a", "MD5A=md5(code +type +challenge +password)") --ubytes
	pf.f_username = ProtoField.string("drcom.username", "Username")
	pf.f_ControlCheckStatus = ProtoField.string("drcom.ControlCheckStatus", "ControlCheckStatus")
	pf.f_macflag =  ProtoField.bool("drcom.macflag", "AdapterNum")  --ubytes
	pf.f_macxor =   ProtoField.bytes("drcom.xormac", "MAC xor MD5A")    --ubytes
	pf.f7 =     ProtoField.bytes("drcom.md5b", "MD5B=md5(01 +password +challenge +00*4)") --ubytes
	pf.f_niccount = ProtoField.uint8("drcom.niccount", "NIC count")
	pf.nicips =     ProtoField.ipv4("drcom.nics","NIC's IPs")
	pf.nic1_ip =    ProtoField.ipv4("drcom.nic1","NIC1 IP")
	pf.nic2_ip =    ProtoField.ipv4("drcom.nic2","NIC2 IP")
	pf.nic3_ip =    ProtoField.ipv4("drcom.nic3","NIC3 IP")
	pf.nic4_ip =    ProtoField.ipv4("drcom.nic4","NIC4 IP")

	pf.f_checksum1 =ProtoField.bytes("drcom.checksum1","Checksum1") --ubytes
	pf.f11 =    ProtoField.bool("drcom.ipdog","IP dog")
	pf.f_zeros =    ProtoField.bytes("drcom.zeros","Zeros")
	pf.f_hostname = ProtoField.string("drcom.hostname","Hostname")
	pf.f14 =    ProtoField.ipv4("drcom.pdns","Primary Dns")
	pf.f15 =    ProtoField.ipv4("drcom.dhcp","DHCP Server")
	pf.f16 =    ProtoField.ipv4("drcom.sdns","Secondary Dns")
	pf.f16_1 =  ProtoField.uint32("drcom.WINSIP1","WINSIP1")
	pf.f16_2 =  ProtoField.uint32("drcom.WINSIP2","WINSIP2")
	pf.f17 =    ProtoField.uint32("drcom.OSVersionInfoSize","OSVersionInfoSize")
	pf.f19 =    ProtoField.uint32("drcom.major","OS major")
	pf.f20 =    ProtoField.uint32("drcom.minor","OS minor")
	pf.f21 =    ProtoField.uint32("drcom.build","OS build")
	pf.f22 =    ProtoField.uint32("drcom.PlatformID","PlatformID")
	pf.f_servicepack =  ProtoField.string("drcom.servicepack","servicepack" )
	pf.f25_1 = ProtoField.bytes("drcom.version", "ClientVerInfoAndInternetMode")
	pf.f25_2 = ProtoField.bytes("drcom.dogversion", "DogVersion")
	pf.len_passwd = ProtoField.bytes("drcom.len_passwd", "Password length") -- new
	pf.ror = ProtoField.bytes("drcom.rorversion", "ROR version") -- new
	pf.f25_3 = ProtoField.bytes("drcom.AuthExtDataCode", "AuthExtDataCode")
	pf.f25_4 = ProtoField.bytes("drcom.AuthExtDatalen", "AuthExtDataLength")
	pf.f26 =    ProtoField.uint32("drcom.checksum","CRC",base.HEX)  --ubytes
	pf.f27 =    ProtoField.uint16("drcom.AuthExtDataOption","AuthExtDataOption",base.HEX)
	pf.f28 =    ProtoField.ether("drcom.mac","MAC" )
	pf.f29 =    ProtoField.bool("drcom.autologout","Auto logout")
	pf.f30 =    ProtoField.bool("drcom.brcomcast","Brcomcast mode" )
	pf.f_info = ProtoField.string("drcom.info","Infomation")
	pf.f_serinfo_unknown = ProtoField.bytes("drcom.unknown","unknown checksum?")
	pf.f_EOF =  ProtoField.uint8("drcom.eof","EOF")
	pf.f_serverIP = ProtoField.ipv4("drcom.svrIP","Server IP")
	pf.f_clientIP = ProtoField.ipv4("drcom.cliIP","Client IP")
	pf.f_drco = ProtoField.string("drcom.drco","DrcomFlag(Drco)")
	pf.f_port = ProtoField.uint16("drcom.port","Port")
	pf.f_authinfo = ProtoField.bytes("drcom.authinfo","Auth Infomation")
	pf.f_uptime =   ProtoField.uint16("drcom.uptime","some time in Seconds",base.DEC)
	pf.f_alivefixed=ProtoField.uint32("drcom.unknown","Unknown 01/00")
	pf.f_unknownbyte =  ProtoField.bytes("drcom.unknownbyte","unknown")
	pf.f_fixedUnknown = ProtoField.bytes("f_fixedUnknown", "f_fixedUnknown")
	local t_failtype = {[0x01]="Already in use",
			[0x02]="server problem",
			[0x03]="Username or password error!",
	  [0x04]="Exceed the balance",
	  [0x05]="Account is unavailable",
			[0x07]="Wrong IP < Account not match 802.1X Account>",
			[0x0b]="Wrong MAC should be TODO:XXXX",
			[0x14]="To many IPs for the account",
			[0x15]="Wrong client version or account has been banned.",
			[0x16]="Specified ip and mac for the account",
			[0x17]="Server required DHCP mode instead of static mode",
			[0x18]="reserved",
			[0x19]="reserved",
			[0x1A]="reserved",
			[0x1B]="reserved",
			[0x1C]="reserved",
			}
	pf.f_failtype = ProtoField.uint8("drcom.failType","Type",base.HEX,t_failtype)
	pf.f_bindmac =  ProtoField.ether("drcom.bindmac","MAC should be")
	pf.f_misccount =    ProtoField.uint8("drcom.misccount","Count what?")
	pf.f_mm =   ProtoField.bytes("drcom.unknown","MM?")
	pf.f_responseunnkown =  ProtoField.bytes("drcom.unknown","uknown")
	pf.f_onlinetime =   ProtoField.uint32("drcom.onlinetime","Online Time in Seconds",base.DEC)
	pf.f_someflux = ProtoField.uint32("drcom.someflux","some flux?",base.DEC)
	pf.f_time2 =    ProtoField.uint32("drcom.time2","some time2 in seconds",base.DEC)
	pf.f_clientversion =  ProtoField.bytes("drcom.clientversion","Client Version")
	pf.f_1000 =     ProtoField.uint16("drcom.1000","Carry per 1000 setp ?",base.DEC)
	pf.f_file   =   ProtoField.bytes("drcom.file","File Content")
	pf.f_monthflux =    ProtoField.float("drcom.monthflux","Month used flux(MB)")
	pf.f_monthtime =    ProtoField.uint32("drcom.monthtime","Month used time(MIN)")
	pf.f_balance =  ProtoField.float("drcom.balance","Balance(yuan)",base.DEC)
	pf.f_timebalance =  ProtoField.float("drcom.timebalance","Time Balance(Minutes)",base.DEC)
	pf.f_milliseconds   =   ProtoField.uint16("drcom.milliseconds","Milliseconds")
	pf.f_internetaccessControl  =   ProtoField.uint32("drcom.InternetAccessControl","InternetAccessControl")

--    local addr = Field.new("ip.addr")

	--为Proto对象添加一个名为dissector的函数，
	--Wireshark会对每个“相关”数据包调用这个函数
	function p_drcom.dissector(buf,pkt,root)
	pkt.cols.protocol= p_drcom.name     --覆盖协议栏为DRCOM

	local subtree   = root:add(p_drcom,buf())   --子节点开始
	subtree:append_text(", "..buf():len().." bytes ")

	--这句是将数据的第一个字节转换成无符号整数
	local code_id = buf(0,1):uint()
	-- DrCOMHeader
	subtree:add(pf.f_code,buf(0,1))
  subtree:add(pf.f_authtype,buf(1,1))
  subtree:add(pf.f_subcode,buf(2,1))
  subtree:add(pf.f_cmdlen,buf(3,1))
	pkt.cols.info=t_code[code_id] or "Unknown"

-------------------------------------------------------------------------------------------
	if code_id == 0x01  then    --complite
	  -- Challenge
		subtree:add(pf.f1_1dir,buf(1,1))
		subtree:add_le(pf.f_uptime,buf(2,2))
		subtree:add(pf.f1_unkonw02,buf(4,1))
		subtree:add(pf.f_zeros,buf(5,15))
	elseif code_id == 0x02  then
	  -- Challenge return
		subtree:add(pf.f1_1dir,buf(1,1))
		subtree:add_le(pf.f_uptime,buf(2,2))
		subtree:add(pf.f2_1dir,buf(4,4))

		subtree:add(pf.f_clientIP,buf(20,4))
		subtree:add(pf.f_responseunnkown,buf(24,2))
		subtree:add(pf.f_mm,buf(26,16))
		subtree:add(pf.f_zeros,buf(42,34))
	elseif code_id == 0x03  then    --complite
	  -- 用户登录
		pkt.cols.info:append(" (Username=\""..buf(20,36):stringz().."\")")
		subtree:add(pf.f_type,buf(1,1))
		subtree:add(pf.f_usernamelen,buf(3,1),buf(3,1):uint()-20)  --usernamelen
		subtree:add(pf.f_md5a,buf(4,16))
		subtree:add(pf.f_username,buf(20,36))
		subtree:add(pf.f_ControlCheckStatus,buf(56,1))
		subtree:add(pf.f_macflag,buf(57,1))
		subtree:add(pf.f_macxor,buf(58,6))
		subtree:add(pf.f7,buf(64,16))
		subtree:add(pf.f_niccount,buf(80,1))

		local nic_ip = subtree:add(pf.nicips,buf(81,16),buf(81,4):ipv4())   --TODO:what type should be?
		nic_ip:add(pf.nic1_ip,buf(81,4))
		nic_ip:add(pf.nic2_ip,buf(85,4))
		nic_ip:add(pf.nic3_ip,buf(89,4))
		nic_ip:add(pf.nic4_ip,buf(93,4))

		local md5c = subtree:add(pf.f_checksum1,buf(97,8)) --md5(front + 1400070b)[0:8]    --checksum1-md5c TODO:verify
		subtree:add(pf.f11,buf(105,1))
		subtree:add(pf.f_zeros,buf(106,4))
		subtree:add(pf.f_hostname,buf(110,32))
		subtree:add(pf.f14,buf(142,4))
		subtree:add(pf.f15,buf(146,4))
		subtree:add(pf.f16,buf(150,4))
		subtree:add(pf.f16_1,buf(154,4))
		subtree:add(pf.f16_2,buf(158,4))
		subtree:add(pf.f17,buf(162,4))
		subtree:add(pf.f19,buf(166,4))
		subtree:add(pf.f20,buf(170,4))
		subtree:add(pf.f21,buf(174,4))
		subtree:add(pf.f22,buf(178,4))
		subtree:add(pf.f_servicepack,buf(182,128))
		subtree:add(pf.f25_1,buf(310,1))
		subtree:add(pf.f25_2,buf(311,1))
		if buf():len()>=338 then
			subtree:add(pf.len_passwd,buf(312,2))
			subtree:add(pf.ror,buf(314,6))
			subtree:add(pf.f25_3,buf(320,1))
			subtree:add(pf.f25_4,buf(321,1))
			subtree:add(pf.f26,buf(322,4))
			subtree:add(pf.f27,buf(326,2))
			subtree:add(pf.f28,buf(328,6))
			subtree:add(pf.f29,buf(334,1))
			subtree:add(pf.f30,buf(335,1))
			if buf():len()>=338 then
				subtree:add(pf.f_unknownbyte,buf(336,2))
			end
		else
			subtree:add(pf.f25_3,buf(312,1))
			subtree:add(pf.f25_4,buf(313,1))
			subtree:add(pf.f26,buf(314,4))
			subtree:add(pf.f27,buf(318,2))
			subtree:add(pf.f28,buf(320,6))
			subtree:add(pf.f29,buf(326,1))
			subtree:add(pf.f30,buf(327,1))
			if buf():len()>=330 then
				subtree:add(pf.f_unknownbyte,buf(328,2))
			end
		end
		
	elseif code_id == 0x04  then
	-- Login return
		if buf():len()>=37 then
      subtree:add(pf.f_fixedUnknown,buf(1,22))
      subtree:add_le(pf.f_monthtime,buf(5,4))
      subtree:add_le(pf.f_monthflux,buf(9,4),buf(9,4):le_uint()/1024)
      subtree:add_le(pf.f_balance,buf(13,4),buf(13,4):le_uint()/100)
      local authinfo = subtree:add(pf.f_authinfo,buf(23,16))
      authinfo:add(pf.f_drco,buf(23,4))
      authinfo:add(pf.f_serverIP,buf(27,4))
      authinfo:add(pf.f_port,buf(31,2))
      authinfo:add(pf.f_clientIP,buf(33,4))
      authinfo:add(pf.f_port,buf(37,2))
      subtree:add(pf.f_milliseconds,buf(39,2))
      subtree:add(pf.f_internetaccessControl,buf(41,4))
      -- subtree:add(pf.f_fixedUnknown,buf(39,6))
		end
	elseif code_id == 0x05  then
		subtree:add(pf.f_failtype,buf(4,1))
		pkt.cols.info:append(" ("..(t_failtype[buf(4,1):uint()] or "Unknown")..")")
		if buf(4,1):uint()==0x0b then
		subtree:add(pf.f_bindmac,buf(5,6))
		else

		end

	elseif code_id == 0x06  then
		subtree:add(pf.f_type,buf(1,1))
		subtree:add(pf.f_EOF,buf(2,1))
		subtree:add(pf.f_usernamelen,buf(3,1),buf(3,1):uint()-20)  --usernamelen
		subtree:add(pf.f_md5a,buf(4,16))
		subtree:add(pf.f_username,buf(20,36))
		subtree:add(pf.f_fixedUnknown,buf(56,1))
		subtree:add(pf.f_macflag,buf(57,1))
		subtree:add(pf.f_macxor,buf(58,6))
		local authinfo = subtree:add(pf.f_authinfo,buf(64,16))
		authinfo:add(pf.f_drco,buf(64,4))
		authinfo:add(pf.f_serverIP,buf(68,4))
		authinfo:add(pf.f_unknown,buf(72,2))
		authinfo:add(pf.f_clientIP,buf(74,4))
		authinfo:add(pf.f_unknown,buf(78,2))
	elseif code_id == 0x07  then
		subtree:add(pf.f_misccount,buf(1,1))
		subtree:add(pf.f_07type,buf(2,2))
		pkt.cols.info:append(", "..(t_07type[buf(2,2):uint()] or "Unknown type"))
		if buf(2,2):uint() == 0x2800 then
		pkt.cols.info:append(", "..t_misctype[buf(5,1):uint()])
		subtree:add(pf.f_misctype,buf(5,1))
		subtree:add(pf.f_clientversion,buf(6,2))
		subtree:add_le(pf.f_1000,buf(8,2))
		subtree:add_le(pf.f_time2,buf(10,4))
		subtree:add_le(pf.f_someflux,buf(16,4))
		subtree:add(pf.f_clientIP,buf(28,4))

		elseif buf(2,2):uint() == 0x1000 then   --Response for Alive

		subtree:add_le(pf.f_uptime,buf(6,2))
		subtree:add_le(pf.f_someflux,buf(8,4))
		subtree:add(pf.f_clientIP,buf(12,4))
		subtree:add(pf.f_mm,buf(16,16))
		-- subtree:add_le(pf.f_onlinetime,buf(32,4))
		-- subtree:add_le(pf.f_monthtime,buf(44,4))
		-- subtree:add_le(pf.f_monthflux,buf(48,4),buf(48,4):le_uint()/1024)
		-- subtree:add_le(pf.f_balance,buf(52,4),buf(52,4):le_uint()/10000)
		-- subtree:add_le(pf.f_timebalance,buf(56,4),buf(56,4):le_uint()/60)
		elseif buf(2,2):uint() == 0x1001 then   --File
		subtree:add_le(pf.f_1000,buf(8,2))
		subtree:add_le(pf.f_time2,buf(10,4))
		subtree:add(pf.f_clientversion,buf(6,2))
		subtree:add(pf.f_mm,buf(16,16))
		subtree:add_le(pf.f_file,buf(32,buf():len()-32))
		elseif buf(2,2):uint() == 0xf400 then

		subtree:add(pf.f_username,buf(32,9))    --FIXME:changeable length
		subtree:add(pf.f_hostname,buf(41,48))   --FIXME:changeable length

		end
	elseif code_id == 0x4d  then

		subtree:add(pf.f_type,buf(1,1))
		pkt.cols.info:append(","..t_type[buf(1,1):uint()])
		if buf(1,1):uint() == 0x38 then
		subtree:add(pf.f_serinfo_unknown,buf(2,2))
		subtree:add(pf.f_info,buf(4))
		elseif false then

		end
	elseif code_id == 0xff  then
	  -- Ping server
		subtree:add(pf.f_md5a,buf(1,16))
		subtree:add(pf.f_zeros,buf(17,3))
		local authinfo = subtree:add(pf.f_authinfo,buf(20,16))
		authinfo:add(pf.f_drco,buf(20,4))
		authinfo:add(pf.f_serverIP,buf(24,4))
		authinfo:add(pf.f_port,buf(28,2))
		authinfo:add(pf.f_clientIP,buf(30,4))
		authinfo:add(pf.f_port,buf(34,2))
	  subtree:add(pf.f_milliseconds,buf(36,2))
	  -- subtree:add(pf.f_internetaccessControl,buf(38,2))
	end

	--local dissector   = protos[0]
 
	--if dissector ~=   nil then
	----  dissector:call(buf(2):tvb(),pkt,root)
	--elseif code_id    < 2 then
	----  subtree:add(pf.f_text,buf(2))
	---- pkt.cols.info:set(buf(2,buf:len() - 3):string())
	--else
	----调用另外一个dissector
	----  data_dis:call(buf(2):tvb(),pkt,root)  --  如果还有剩余数据，作为一般的Data段进行解析
	--end
	end

	--所有的dissector都是以“table”的形式组织的，table表示上级协议
	local wtap_encap_table = DissectorTable.get("wtap_encap")

	--这个是获得udp协议的DissectorTable，并且以端口号排列
	local udp_encap_table = DissectorTable.get("udp.port")

	wtap_encap_table:add(wtap.USER15,p_drcom)
	wtap_encap_table:add(wtap.USER12,p_drcom)
	--为UDP的61440端口注册这个Proto对象，
	--当遇到源或目的为UDP61440的数据包，就会调用上面的p_drcom.dissector函数
	udp_encap_table:add(61440,p_drcom)
end
