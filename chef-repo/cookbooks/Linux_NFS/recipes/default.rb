#
# Cookbook Name:: auto_NFS
# Recipe:: default
#
# Copyright 2014, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#
node['nfs']['packages'].each do |nfspkg|
  package nfspkg do
    action :install
  end
end

# Start NFS client components
service "portmap" do
  service_name node['nfs']['service']['portmap']
  action [ :start, :enable ]
end

service "nfslock" do
  service_name node['nfs']['service']['lock']
  action [ :start, :enable ]
end

# Configure NFS client components
#node['nfs']['config']['client_templates'].each do |client_template|
#  template client_template do
#    mode 0644
#    notifies :restart, "service[portmap]", :delayed
#    notifies :restart, "service[nfslock]", :delayed
#  end
#end
