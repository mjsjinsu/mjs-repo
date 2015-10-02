#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pexpect
import sys, os, datetime

CONN_PASS='Password' # Switch telnet Connection Password
EN_PASS='EN_Password' # Switch Enable Connection Password
PROMPT = ['#', '>>>', '>','\$'] # List of expect Switch PROMPT

#telnet Connection function
def connect_telnet(username, password, host) :
	
	child = pexpect.spawn("telnet %s" % (host)) # use pexpect spawn class to generate child application object  
	i = child.expect([pexpect.TIMEOUT, "Username: ", "login: "]) # expect function return matched pattern List index

	if i == 0 : # index = 0, telnet timeout, default 30 sec
		print "ERROR : occuer timeout"
		print "print 'Telnet could not login. Here is what Telnet said:'"
		result = host + " : timeout"
		return result

	elif i in [1, 2] : # index = 1, 2 are Swtich login prompt (1:Cisco / 2: Arista)
		child.sendline(username) # send username
		i = child.expect([pexpect.TIMEOUT, 'Password:*'])
		if i == 0 :
			print "ERROR : Telnet could not login. Here is what Telnet said"
			print child.before, child,after
			return None

		child.sendline(password) # send CONN_PASS
		child.expect(PROMPT) # send PROMPT
		return child # return child object


# collect swtich Configuration(type1 : Cisco, Arista switch)
def collect_cfg_type1_switch(host, CONN_PASS, EN_PASS) :

	s = connect_telnet("admin", CONN_PASS, host) # connect_telnet object 's' generate
	s.sendline("en") # send enable command
	s.expect('Password: ') 
	s.sendline(EN_PASS) # send enable password
	s.expect("#")
	switch_hostname = s.before.strip() # get switch hostname
	switch_prompt = switch_hostname	+ "#" # set switch prompt
	s.sendline('terminal length 0')
	s.expect(switch_prompt)
	s.sendline('show run')
	s.expect(switch_prompt)
	return s.before

# collect switch Configuration(Juniper switch)
def collect_cfg_type2_switch(host, CONN_PASS) :

	s = connect_telnet("admin", CONN_PASS, host) # connect_telnet object 's' generate
	s.sendline('show configuration | display set | no-more')
	s.expect(pexpect.TIMEOUT, timeout=2)
	return s.before

# write file with filename, input parameter    
def write_to_file(filename, input) :

	try :
		cfg_file = open(filename, "w")
		
	except IOError as e :
		stdout_handler("Error meg : ", str(e))

	else :
		cfg_file.write(input)
		stdout_handler("Sucessfully write result", filename)

	finally :
		cfg_file.close()

def stdout_handler(*args) :

	msg = ""
	for i in args :
		msg += i
	print msg

if __name__ == "__main__" :

	work_directory = os.getcwd()
	date = str(datetime.date.today()).replace("-","")
	directory = work_directory + "/" + str(date)
	dict_sp_line = {}

	if not os.path.exists(directory) :
		os.mkdir(directory) # make directory to put switch config file
	
	try :
		switch_list = open(work_directory + "/" + "switch_list.txt", "rb") # list of switch that using collect_cfg_type1/2_switch function
		lines = switch_list.readlines() # read switch_list.txt file

		for line in lines :
			if line[0] != "#" :
				sp_line = line.strip().split("\t")
				dict_sp_line[sp_line[0]] = sp_line[1] # make dictionary : key(ip) = value(switch vendor)
		
	except :
		print "Occur Error"
		
	else :
		for ip in dict_sp_line :
			if dict_sp_line[ip] in ['CISCO', 'ARISTA'] :
				result = collect_cfg_type1_switch(ip, CONN_PASS, EN_PASS)

			elif dict_sp_line[ip] in ['JUNIPER'] :
				result = collect_cfg_type2_switch(ip, CONN_PASS)
			
			write_to_file(directory + "/" + date + "_" + ip, result)
			
	finally :
		switch_list.close()

