

import paramiko
import os
path = './admin' #path to the admin's public keys
another_path = './new_user' #path to a new user's public keys
host = 'localhost'
user = 'root'
secret = 'root'
port = 1234 #22nd port in the container is binded to this host's port
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=secret, port=port)

files = []
stdin, stdout, stderr = client.exec_command('cd ~/.ssh/authorized_keys')
error_msg = stderr.read().decode("utf-8")

#Create folder with authorised keys
if "No such file or directory" in error_msg:
    client.exec_command('mkdir ~/.ssh')
    client.exec_command('chmod 700 ~/.ssh')
    client.exec_command('touch ~/.ssh/authorized_keys')
    client.exec_command('chmod 600 ~/.ssh/authorized_keys')

for r, d, f in os.walk(path):
    for file in f:
        if '.pub' in file:
            files.append(file)
#
for f in files:
    days_file = open(path + "/" + f, 'r')
    key = days_file.read().rstrip()
    print(key)
    command = f'echo "{key}">> ~/.ssh/authorized_keys'
    client.exec_command(command)



# Change config

#Turn off PAM
client.exec_command("sed -i 's/UsePAM yes"
                    "/UsePAM no/g' /etc/ssh/sshd_config")
client.exec_command("sed -i 's/#UsePAM no"
                    "/UsePAM no/g' /etc/ssh/sshd_config")
#Turn off password authentication
client.exec_command("sed -i 's/PasswordAuthentication yes"
                    "/PasswordAuthentication no/g' /etc/ssh/sshd_config")

client.exec_command("sed -i 's/#PasswordAuthentication no"
                    "/PasswordAuthentication no/g' /etc/ssh/sshd_config")

client.exec_command('/etc/init.d/ssh reload')
client.close()