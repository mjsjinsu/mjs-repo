#
# Cookbook Name:: mjsmount
# Recipe:: default
#
# Copyright 2013, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#
mount "/mjstest" do
	device "/dev/xvdb1"
	fstype "ext4"
	action [:umount, :disable]
end
