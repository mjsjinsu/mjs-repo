# -*- coding: utf-8 -*-

if __name__ == "__main__":
	import os, commands

	ifg_info = dict()
	gateway = ''
	
	fail, output = commands.getstatusoutput("ifconfig -a | grep eth1 -A1 | grep inet")
	
	try:
		res = output.strip().split()[1].split(":")
		ifg_info[res[0]] = res[1]
		res = output.strip().split()[3].split(":")
		ifg_info[res[0]] = res[1]

		gw = ifg_info['addr'].split('.')

		for i in range(3):
			gateway += gw[i] + '.'
		gateway += '1'
		os.system("echo GATEWAY=%s >> /etc/sysconfig/network" % gateway)
	except IndexError:
		print "Exception is occured! you have to check MultiNIC interface eth1 state"
else:
	print "imported not support"