#!/usr/bin/env python

import sys, re, os, getopt, getpass
import pexpect

def exit_with_usage():
	print(globals()['__doc__'])
	os._exit(1)

def main(user, host, password, command):
	try:
		optlist, args = getopt.getopt(sys.argv[1:], 's:u:p:')
	except Exception as e:
		print (str(e))
		exit_with_usage()
	options = dict(optlist)

	if len(args) > 1:
		exit_with_usage()
	if '-s' in options:
		host = options["-s"]
	if '-u' in options:
        	user = options['-u']
	if '-p' in options:
        	password = options['-p']
	
	ssh_newkey = 'Are you sure you want to continue connecting'

	child = pexpect.spawn('ssh -l root %s %s'%(host, command))
	i = child.expect([ssh_newkey ,'[P|p]assword', pexpect.EOF])
	print i
	if i == 0: # Timeout
        	print('ERROR! could not login with SSH. Here is what SSH said:')
        	print(child.before, child.after)
        	print(str(child))
        	sys.exit (1)
	if i == 1:
		child.sendline(password)
		child.expect(pexpect.EOF)
	if i == 2:
		pass
    	if i == 3: # In this case SSH does not have the public key cached.
        	child.sendline ('yes')
        	child.expect ('(?i)password')
		child.sendline(password)
	print child.before

if __name__ == "__main__":
	user="root"
	host="10.13.31.222"
	password="wlstn0284"
	command="ifconfig"

	main(user,host,password,command)
