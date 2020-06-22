import time
import os
import re
import sys
import string
import random
import subprocess
import json
import codecs

os_type = sys.argv[1]

expected_os = ['windows', 'rhel', 'ubuntu']

if os_type not in expected_os:
	raise Exception('os type {} is not in expected list {}'.format(os_type, expected_os))

# Flavor and image id combination for the VM creation
flavor_image_combination = {
	"windows": {
		"flavor": "f47e69d4-edd4-4da0-b4cc-aff9febfb289",
		"image" : "d6b1fad4-f7ee-452b-9813-c43e76592d9b"
	},
	"rhel": {
		"flavor": "a9acc2de-39d7-4148-8d16-413c3b696e9d",
		"image": "9d6cb476-c374-4daf-bceb-f0a1e6ae0cfc"
	}
}
rand_string = ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k = 6))


# Setting VM name and Keypair name which are required for creation of VM
vm_name = 'test-tkn-{}-{}'.format(os_type, rand_string)
keypair_name = 'test-keypair-{}'.format(rand_string)


# Exporting the VM name, Keypair name, flavor id and image id as environment variables
os.environ['VM_NAME'] = vm_name
os.environ['KEYPAIR_NAME'] = keypair_name
os.environ["IMAGE_ID"] = flavor_image_combination[os_type]['image']
os.environ["FLAVOR_ID"] = flavor_image_combination[os_type]['flavor']


# Generate new Keypair
print('******************************** Generating keypair {} *************************************'.format(keypair_name), flush=True)
output = subprocess.run('openstack keypair create {}'.format(keypair_name).split(), stdout=subprocess.PIPE, text=True)

# Checking if keypair got generated or not
if output.returncode != 0:
	raise Exception('Generating keypair failed with error {}'.format(output.stderr))

with open('id_rsa', 'w') as f:
	f.write(output.stdout)
print('******************************** Generated keypair {} successfully *************************************'.format(keypair_name), flush=True)

# Reduce permission to id_rsa
output = subprocess.run('chmod 400 id_rsa'.split(), stdout=subprocess.PIPE, text=True)




# Create VM
print('******************************** Creating {} VM with name {}*************************************'.format(os_type, vm_name), flush=True)
output = subprocess.run('ansible-playbook create-vm.yml -vvvv'.split(), stdout=subprocess.PIPE, text=True)

if output.returncode != 0:
	print('******************************** Deleting keypair {}*************************************'.format(keypair_name), flush=True)
	subprocess.run('openstack keypair delete {}'.format(keypair_name).split(), stdout=subprocess.PIPE, text=True)
	raise Exception('Creation of VM failed with error {}'.format(output.stderr))

print('sleeping for 2 minute')
time.sleep(120)


output = subprocess.run('openstack server list --name {} -f json'.format(vm_name).split(), stdout=subprocess.PIPE, text=True)
vm_info = eval(output.stdout)[0]
vm_id = vm_info['ID']

match = re.search(r"\d+\.\d+\.\d+\.\d+", vm_info['Networks'])
vm_ip = match.group(0)



# Build inventory file
os_username = { 'ubuntu': 'ubuntu', 'rhel': 'cloud-user', 'windows': "Admin"}


if os_type == 'windows':
	output = subprocess.run('nova get-password {} id_rsa'.format(vm_id).split(), stdout=subprocess.PIPE, text=True)
	win_password = output.stdout

	inventory_content = '''
[test-host]
{}

[test-host:vars]
ansible_user={}
ansible_password={}
ansible_connection=winrm
ansible_winrm_server_cert_validation=ignore
'''.format(vm_ip, os_username[os_type], win_password)
else:
	inventory_content = '''
[test-host]
{}

[test-host:vars]
ansible_user={}
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
'''.format(vm_ip, os_username[os_type])
with open('hosts', 'w') as f:
	f.write(inventory_content)

# Install tkn on remote machine
print('******************************** Install tkn on machine {} *************************************'.format(vm_name), flush=True)
output = subprocess.run('ansible-playbook install-tkn-{}.yml -v -i hosts --private-key id_rsa'.format(os_type).split(), stdout=subprocess.PIPE, text=True)
print('installation tkn was successful', flush=True)
print(output.stdout)

if output.returncode == 0:
	print('******************************** running cli tests on  {} *************************************'.format(vm_name), flush=True)
	output = subprocess.run('ansible-playbook run-cli-tests-{}.yml -i hosts'.format(os_type).split(), stdout=subprocess.PIPE, text=True)
	match = re.search(r'"msg": "(.*)"', output.stdout)
	output = match.group(1)
	output = output.split("\\n")
	for i in output:
		i = i.strip('-')
		print(codecs.getdecoder("unicode_escape")(i)[0])

# Delete created VM
print('******************************** Delete created VM {} *************************************'.format(vm_name))
output = subprocess.run('nova delete {}'.format(vm_id).split(), stdout=subprocess.PIPE, text=True)


# Delete keypair
print('******************************** Delete Keypair {} *************************************'.format(keypair_name))
output = subprocess.run('openstack keypair delete {}'.format(keypair_name).split(), stdout=subprocess.PIPE, text=True)