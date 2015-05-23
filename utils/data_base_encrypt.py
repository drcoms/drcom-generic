#Ice Weng@May 23
import string,sys
def get_string():
	s=map(ord,raw_input('input the code u want to encrpt:'))
	codearray=[28,57,86,19,47,76,9,38,66,95,28,57,86,18,47,76]
	print s
	lens=len(s)
	count=0
	while(count<lens):
		print chr(lim_126(s[count]+codearray[count])),
		count=count+1
	print 'a'

def lim_126(num):
	if(num>126):
		return num-126+31
	else:
		return num

get_string()
raw_input("\nany key to exit...") 
