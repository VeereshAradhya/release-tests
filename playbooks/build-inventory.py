import os
import re
import sys

host_type = sys.argv[1]

stream = os.popen("ansible-playbook get-vm.yml | grep accessIPv4")
output = stream.read()

#get IP of host
match = re.search(r"\d+\.\d+\.\d+\.\d+", output)
ip = match.group()

#Build inventory and config
with open('hosts', 'w') as f:
	f.write("[test-host]\n{}".format(ip))

#Build ansible.cfg
os_username = { "ubuntu": "ubuntu", "rhel": "cloud_user"}

config = '''[defaults]
remote_user={}
inventory=hosts'''.format(os_username[host_type])
with open('ansible.cfg', 'w') as f:
	f.write(config)