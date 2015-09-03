case node['platform']
when 'redhat','centos','scientific','amazon'
  if node['platform_version'].to_i >= 6
    # RHEL/CentOS 6 portmap/rpcbind edge case, thanks BryanWB!
    default['nfs']['packages'] = [ 'nfs-utils', 'rpcbind' ]
    default['nfs']['service']['portmap'] = 'rpcbind'
  else
    # RHEL/CentOS <= 5 portmap/packages
    default['nfs']['packages'] = [ 'nfs-utils', 'portmap' ]
    default['nfs']['service']['portmap'] = 'portmap'
  end
  # General RHEL/Centos options
default['nfs']['service']['lock'] = 'nfslock'
default['nfs']['service']['server'] = 'nfs'
end
default['nfs']['config']['nfs_network'] = false
default['nfs']['shares']['/data']['server'] = '172.27.242.210'
default['nfs']['shares']['/data']['remote_folder'] = '/home/nas'
default['nfs']['shares']['/data']['nfs_options'] = 'rw'
