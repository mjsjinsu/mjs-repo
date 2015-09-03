has_multinic = false

node['network']['interfaces'].each do |i,s|
	if ["eth1","eth2","eth3"].include?(i)
		if ["UP"].include?(s['flags'])
			has_multinic = false
		else
			has_multinic = true
		end
	end

if has_multinic == true
	if node['platform']=='centos'
		template "/etc/sysconfig/network-scripts/ifcfg-#{i}" do
		source "network-interface.erb"
		mode "644"
		variables ({
		:ethx => i
		})
		action :create
		notifies :restart, 'service[network]', :delayed
		end
	Chef::Log.info "Network interface ifcfg-#{i} setting complete"
	end
end
has_multinic = false
end
service "network" do
	supports :restart => true, :reload => true
end