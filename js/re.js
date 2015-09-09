'use strict';

var params;

$(document).ready(function (){
	$('#file-upload').click(function(){
		fileupload(function(file) {
		if (file) {
			var reader = new FileReader();
			reader.onload = function(e) {
				var data = e.target.result;
				// alert(data);
				// document.getElementById('test').innerHTML = data;
				// params = re_d(data);
				if ($('.table-responsive').is('#panel1')) {
					params = re_d(data);
				} else{
					params = re_p(data);
				};
			}
			reader.readAsText(file, 'utf-16be');
		}
	}, '.pcapng');
	});
	$('#config-generate').click(function(){
		var gen = '';
		for (var i = 0; i < params[0].length; i++) {
			if (params[0][i] == 'mac'){
				gen += (params[0][i] + ' = ' + params[1][i] + '\n');
			} else {
				gen += (params[0][i] + ' = \'' + params[1][i] + '\'\n');
			}
		};
		gen = gen.slice(0, -1);
		var blob = new Blob([gen], {type: "text/plain;charset=utf-8"});
		saveAs(blob, 'drcom.conf');
	});
	$('#edit').click(function(){
		params[1][2] = $('#password').val();
	});
	// $('#v_d').click(function(){
	// 	$('#panel1').load('index.html' + ' #panel1');
	// });
	// $('#v_p').click(function(){
	// 	$('#panel2').load('config_p.html' + ' #panel2');
	// });
});

function fileupload (callback, accept) {
	var fileSelector = $('<input type="file">');
	if (accept) fileSelector.attr('accept', accept);
	fileSelector.change(function() {
		var files = fileSelector[0].files;
		if (files.length) {
			callback(files[0]);
		} else {
			callback(null);
		}
	});
	fileSelector.click();
}

String.prototype.hexEncode = function(){
	var hex, i;
	var result = "";
	for (i=0; i<this.length; i++) {
		hex = this.charCodeAt(i).toString(16);
		result += ("000"+hex).slice(-4);
	}
	return result
}

String.prototype.hex2a = function(){
	var str = '';
	for (var i = 0; i < this.length; i += 2)
		str += String.fromCharCode(parseInt(this.substr(i, 2), 16));
	return str;
}

String.prototype.hex2o = function(){
    var str = '';
    for (var i = 0; i < this.length; i += 2)
        str += (parseInt(this.substr(i, 2), 16) + '.');
    return str;
}

function re_d (text) {
	text = text.hexEncode();
	var re1 = /f000f000[00-ff]{8}0301/;
	var r1 = text.match(re1);
	var offset = text.indexOf(r1) + 16;
	// document.getElementById('test').innerHTML = offset;
	// ra = text.substring(offset, offset + 660);
	// document.getElementById('test').innerHTML = ra;
	var username_len = (parseInt(text.substring(offset + 6, offset + 8), 16) - 20)*2;
	var username = text.substring(offset + 40, offset + 40 + username_len).hex2a();
	var server = text.substring(offset - 24, offset -16);
	var password = '';
	var CONTROLCHECKSTATUS = '\\x' + text.substring(offset + 112, offset + 114);
	var ADAPTERNUM = '\\x' + text.substring(offset + 114, offset + 116);
	var host_ip = text.substring(offset + 162, offset + 170).replace(/../ig, function (s,t) {return '\\x' + s});
	var IPDOG = '\\x' + text.substring(offset + 210, offset + 212);
	var host_name = 'fuyumi';
	var PRIMARY_DNS = text.substring(offset + 284, offset + 292).replace(/../ig, function (s,t) {return '\\x' + s});
	var dhcp_server = text.substring(offset + 292, offset + 300).replace(/../ig, function (s,t) {return '\\x' + s});
	var AUTH_VERSION = '\\x' + text.substring(offset + 620, offset + 622) + '\\x' + text.substring(offset + 622, offset + 624);
	var mac = '0x' + text.substring(offset + 640, offset + 652);
	var host_os = 'Windows 8.1';
	var re2 = /f000f000.{8}07..28000b01..../g;
	var r2 = text.match(re2);
	// var KEEP_ALIVE_VERSION = r2[1];
	for (var i = r2.length - 1; i >= 0; i--) {
		if(r2[i].slice(-4)!='0f27')
			var KEEP_ALIVE_VERSION = r2[i].slice(-4).replace(/../ig, function (s,t) {return '\\x' + s});
	};
	var params1 = ['server','username','password','CONTROLCHECKSTATUS','ADAPTERNUM','host_ip','IPDOG','host_name','PRIMARY_DNS','dhcp_server','AUTH_VERSION','mac','host_os','KEEP_ALIVE_VERSION']
	var params2 = [server,username,password,CONTROLCHECKSTATUS,ADAPTERNUM,host_ip,IPDOG,host_name,PRIMARY_DNS,dhcp_server,AUTH_VERSION,mac,host_os,KEEP_ALIVE_VERSION]
	for (var i = params1.length - 1; i >= 0; i--) {
		document.getElementById(params1[i]).innerHTML = params2[i];
	};
	return [params1,params2];
	// document.getElementById('test').innerHTML = KEEP_ALIVE_VERSION;
}

function re_p (text) {
	text = text.hexEncode();
	var re1 = /07[00-ff]{2}60000300/;
	var r1 = text.match(re1);
	var offset = text.indexOf(r1);
	var server = text.substring(offset - 24, offset -16).hex2o().slice(0, -1);
	var pppoe_flag = '\\x' + text.substring(offset + 38, offset + 40);
	var re2 = /07.{4}28000b..(..)02/;
	var keep_alive2_flag = '\\x' + text.match(re2)[1];
	var params1 = ['server','pppoe_flag','keep_alive2_flag'];
	var params2 = [server,pppoe_flag,keep_alive2_flag]
	for (var i = params1.length - 1; i >= 0; i--) {
		document.getElementById(params1[i]).innerHTML = params2[i];
	};
	return [params1,params2];
}
