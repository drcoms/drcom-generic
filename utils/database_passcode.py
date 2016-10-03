#!/usr/bin/python
# Copyright (c) 2015 Ice Weng   # May 23
# Copyright (c) 2016 Artoria2e5 # refactor, changes released under CC0
"""DRCOM db passcode obfuscation utils."""
import sys

try:
    raw_input
except:
    raw_input = input  # py3

codearray = [28, 57, 86, 19, 47, 76, 9, 38, 66, 95, 28, 57, 86, 18, 47, 76]

def decode(s, clean=True):
    if s[-1] == 'a' and not clean:
        s = s[:-1]
    return ''.join(chr(_lim32(ord(c) - codearray[i])) for i, c in enumerate(s))

def encode(s, clean=False):
    return ''.join(chr(_lim126(ord(c) + codearray[i]))
                   for i, c in enumerate(s)) + 'a' if not clean else ''

def _lim32(num):
    return num if (num >= 32) else num + 126 - 31

def _lim126(num):
    return num if (num <= 126) else num - 126 + 31

if __name__ == '__main__':
    prompt = 'input the code you want to %s: '
    argv, argc = sys.argv, len(sys.argv)
    if argc == 1:
        action = ''
        while action not in ['encode', 'decode']:
            action = raw_input('encode/decode? ')
        print(locals()[action](raw_input(prompt % action)))
    if argc == 2:
        if argc in ['encode', 'decode']:
            print(locals()[argv[1]](raw_input(prompt % argv[1])))
        else:
            print('decode(-a$): ' + decode(argv[1]))
            print('encode(+a$): ' + encode(argv[1]))
    elif argc >= 3:
        if argc in ['encode', 'decode']:
            print('\n'.join(map(locals()[argv[1]](argv[2:]))))
        else:
            raise ValueError('bad action: not encode/decode')
