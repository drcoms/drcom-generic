var app = new Vue({
  el: '#app',
  data: {
    versions: ['5.2.x Version D', '5.2.x Version P', '6.0.x Version D', '6.0.x Version P'],
    version_selected: '5.2.x Version D',
    result: ''
  },
  methods: {
    parseConfig: function () {
      function fileupload(callback, accept) {
        var fileSelector = document.createElement('input');
        fileSelector.setAttribute('type', 'file');
        fileSelector.setAttribute('accept', '.pcapng');
        fileSelector.addEventListener('change', function () {
          var files = fileSelector.files;
          if (files.length) {
            callback(files[0]);
          } else {
            callback(null);
          }
        });
        fileSelector.click();
      }

      function hexEncode(array) {
        return array.map(function (byte) {
          return ('0' + (byte & 0xFF).toString(16)).slice(-2);
        }).join('')
      }
      String.prototype.hex2a = function () {
        var str = '';
        for (var i = 0; i < this.length; i += 2)
          str += String.fromCharCode(parseInt(this.substr(i, 2), 16));
        return str
      }
      String.prototype.hex2o = function () {
        var str = '';
        for (var i = 0; i < this.length; i += 2)
          str += (parseInt(this.substr(i, 2), 16) + '.');
        return str
      }

      function re_5d(text) {
        var int8array = new Uint8Array(text);
        var textarray = Array.from(int8array);
        text = hexEncode(textarray);
        var re1 = /f000f000[00-ff]{8}0[37]01/;
        var r1 = text.match(re1);
        var offset = text.indexOf(r1) + 16;
        var re2 = /0000[00-ff]{4}/;
        var r2 = text.substring(offset + 668, offset + 676).match(re2);
        if (r2 !== null) {
          var ror_version = true;
        } else {
          var ror_version = false;
        }
        var username_len = (parseInt(text.substring(offset + 6, offset + 8), 16) - 20) * 2;
        var username = text.substring(offset + 40, offset + 40 + username_len).hex2a();
        var server = text.substring(offset - 24, offset - 16).hex2o().slice(0, -1);
        var password = '';
        var CONTROLCHECKSTATUS = '\\x' + text.substring(offset + 112, offset + 114);
        var ADAPTERNUM = '\\x' + text.substring(offset + 114, offset + 116);
        var host_ip = text.substring(offset + 162, offset + 170).hex2o().slice(0, -1);
        var IPDOG = '\\x' + text.substring(offset + 210, offset + 212);
        var host_name = 'fuyumi';
        var PRIMARY_DNS = text.substring(offset + 284, offset + 292).hex2o().slice(0, -1);
        var dhcp_server = text.substring(offset + 292, offset + 300).hex2o().slice(0, -1);
        var AUTH_VERSION = '\\x' + text.substring(offset + 620, offset + 622) + '\\x' + text.substring(offset + 622, offset + 624);
        if (ror_version) {
          var mac = '0x' + text.substring(offset + 656, offset + 668);
        } else {
          var mac = '0x' + text.substring(offset + 640, offset + 652);
        }
        var host_os = 'Windows 10';
        var re3 = /f000f000.{8}07..28000b01..../g;
        var r3 = text.match(re3);
        for (var i = r3.length - 1; i >= 0; i--) {
          if (r3[i].slice(-4) != '0f27')
            var KEEP_ALIVE_VERSION = r3[i].slice(-4).replace(/../ig, function (s) {
              return '\\x' + s
            });
        };
        var params1 = ['server', 'username', 'password', 'CONTROLCHECKSTATUS', 'ADAPTERNUM', 'host_ip', 'IPDOG', 'host_name', 'PRIMARY_DNS', 'dhcp_server', 'AUTH_VERSION', 'mac', 'host_os', 'KEEP_ALIVE_VERSION', 'ror_version']
        var params2 = [server, username, password, CONTROLCHECKSTATUS, ADAPTERNUM, host_ip, IPDOG, host_name, PRIMARY_DNS, dhcp_server, AUTH_VERSION, mac, host_os, KEEP_ALIVE_VERSION, String(ror_version).charAt(0).toUpperCase() + String(ror_version).slice(1)]
        var result = '';
        for (var i = 0; i <= params1.length - 1; i++) {
          if (params1[i] == 'mac' || params1[i] == 'ror_version') {
            result += (params1[i] + ' = ' + params2[i] + '\n');
          } else {
            result += (params1[i] + ' = \'' + params2[i] + '\'\n');
          }
        };
        return result.slice(0, -1);
      }
      function re_5p(text) {
        var int8array = new Uint8Array(text);
        var textarray = Array.from(int8array);
        text = hexEncode(textarray);
        var re1 = /07[00-ff]{2}60000300/;
        var r1 = text.match(re1);
        var offset = text.indexOf(r1);
        var server = text.substring(offset - 24, offset - 16).hex2o().slice(0, -1);
        var pppoe_flag = '\\x' + text.substring(offset + 38, offset + 40);
        var re2 = /07.{2}28000b..(..)02/;
        var keep_alive2_flag = '\\x' + text.match(re2)[1];
        var params1 = ['server', 'pppoe_flag', 'keep_alive2_flag'];
        var params2 = [server, pppoe_flag, keep_alive2_flag];
        var result = '';
        for (var i = 0; i <= params1.length - 1; i++) {
          if (params1[i] == 'mac' || params1[i] == 'ror_version') {
            result += (params1[i] + ' = ' + params2[i] + '\n');
          } else {
            result += (params1[i] + ' = \'' + params2[i] + '\'\n');
          }
        };
        return result.slice(0, -1);
      }

      function re_6d(text) {
        var int8array = new Uint8Array(text);
        var textarray = Array.from(int8array);
        text = hexEncode(textarray);
        var re1 = /f000f000[00-ff]{8}0[37]01/;
        var r1 = text.match(re1);
        var offset = text.indexOf(r1) + 16;
        var re2 = /0000[00-ff]{4}/;
        var r2 = text.substring(offset + 668, offset + 676).match(re2);
        var ror_version = true;
        var username_len = (parseInt(text.substring(offset + 6, offset + 8), 16) - 20) * 2;
        var username = text.substring(offset + 40, offset + 40 + username_len).hex2a();
        var server = text.substring(offset - 24, offset - 16).hex2o().slice(0, -1);
        var password = '';
        var CONTROLCHECKSTATUS = '\\x' + text.substring(offset + 112, offset + 114);
        var ADAPTERNUM = '\\x' + text.substring(offset + 114, offset + 116);
        var host_ip = text.substring(offset + 162, offset + 170).hex2o().slice(0, -1);
        var IPDOG = '\\x' + text.substring(offset + 210, offset + 212);
        var host_name = 'fuyumi';
        var PRIMARY_DNS = text.substring(offset + 284, offset + 292).hex2o().slice(0, -1);
        var dhcp_server = text.substring(offset + 292, offset + 300).hex2o().slice(0, -1);
        var AUTH_VERSION = '\\x' + text.substring(offset + 620, offset + 622) + '\\x' + text.substring(offset + 622, offset + 624);
        var mac = '0x' + text.substring(offset + 660, offset + 672);
        var host_os = 'Windows 10';
        var re3 = /f000f000.{8}07..28000b01..../g;
        var r3 = text.match(re3);
        for (var i = r3.length - 1; i >= 0; i--) {
          if (r3[i].slice(-4) != '0f27')
            var KEEP_ALIVE_VERSION = r3[i].slice(-4).replace(/../ig, function (s) {
              return '\\x' + s
            });
        };
        var params1 = ['server', 'username', 'password', 'CONTROLCHECKSTATUS', 'ADAPTERNUM', 'host_ip', 'IPDOG', 'host_name', 'PRIMARY_DNS', 'dhcp_server', 'AUTH_VERSION', 'mac', 'host_os', 'KEEP_ALIVE_VERSION', 'ror_version']
        var params2 = [server, username, password, CONTROLCHECKSTATUS, ADAPTERNUM, host_ip, IPDOG, host_name, PRIMARY_DNS, dhcp_server, AUTH_VERSION, mac, host_os, KEEP_ALIVE_VERSION, String(ror_version).charAt(0).toUpperCase() + String(ror_version).slice(1)]
        var result = '';
        for (var i = 0; i <= params1.length - 1; i++) {
          result += (params1[i] + ' = \'' + params2[i] + '\'\n');
        };
        return result.slice(0, -1);
      }
      function re_6p(text) {
        var int8array = new Uint8Array(text);
        var textarray = Array.from(int8array);
        text = hexEncode(textarray);
        var re1 = /07[00-ff]{2}28010300/;
        var r1 = text.match(re1);
        var offset = text.indexOf(r1);
        var server = text.substring(offset - 24, offset - 16).hex2o().slice(0, -1);
        var pppoe_flag = '\\x' + text.substring(offset + 38, offset + 40);
        var re2 = /07.{2}28000b..(..)02/;
        var keep_alive2_flag = '\\x' + text.match(re2)[1];
        var params1 = ['server', 'pppoe_flag', 'keep_alive2_flag'];
        var params2 = [server, pppoe_flag, keep_alive2_flag];
        var result = '';
        for (var i = 0; i <= params1.length - 1; i++) {
          result += (params1[i] + ' = \'' + params2[i] + '\'\n');
        };
        return result.slice(0, -1);
      }

      fileupload(function (file) {
        if (file) {
          var reader = new FileReader();
          reader.onload = function (e) {
            var data = e.target.result;
            if (app.$data.version_selected === '5.2.x Version D') {
              app.$data.result = re_5d(data);
            } else if (app.$data.version_selected === '5.2.x Version P') {
              app.$data.result = re_5p(data);
            } else if (app.$data.version_selected === '6.0.x Version D') {
              app.$data.result = re_6d(data);
            } else if (app.$data.version_selected === '6.0.x Version P') {
              app.$data.result = re_6p(data);
            }
          }
          reader.readAsArrayBuffer(file);
        }
      })
    },
    saveConfig: function () {
      var blob = new Blob([app.$data.result], {
        type: "text/plain;charset=utf-8"
      });
      saveAs(blob, 'drcom.conf', true);
    }
  }
});
