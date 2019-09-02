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

#Switch to an alternate port
client.exec_command("sed -i 's/#Port 22"
                    "/Port 1234/g' /etc/ssh/sshd_config")
#Disable ipv6
client.exec_command("sed -i 's/ListenAddress ::"
                    "//g' /etc/ssh/sshd_config")
#Disable X11 forwarding
client.exec_command("sed -i 's/X11Forwarding yes"
                    "/X11Forwarding no/g' /etc/ssh/sshd_config")

#Check if strict modes is the default
client.exec_command("sed -i 's/#StrictModes yes"
                    "/StrictModes yes/g' /etc/ssh/sshd_config")
# Allow only a specific system group to use the service (e.g. root or wheel)
client.exec_command("echo 'AllowGroups root' >> /etc/ssh/sshd_config")

#Enable logs
client.exec_command("sed -i 's/#LogLevel INFO"
                    "/LogLevel VERBOSE/g' /etc/ssh/sshd_config")
client.exec_command("sed -i 's/#SyslogFacility AUTH"
                    "/SyslogFacility AUTHPRIV/g' /etc/ssh/sshd_config")

# Create an account for a teammate and allow him to SSH into your server as user. Show your system logs as acceptance test, once your teammate reached his account.


client.exec_command("mkdir -p /home/mynewuser/.ssh")
client.exec_command("touch /home/mynewuser/.ssh/authorized_keys")
client.exec_command("useradd -d /home/mynewuser mynewuser")
client.exec_command("gpasswd -a mynewuser su")
client.exec_command("usermod -aG root mynewuser")
client.exec_command("chown -Rfv mynewuser:mynewuser /home/mynewuser/.ssh/")
client.exec_command("chmod 700 /home/mynewuser/.ssh")
client.exec_command("chmod 600 /home/mynewuser/.ssh/authorized_keys")


files = []
for r, d, f in os.walk(another_path):
    for file in f:
        if '.pub' in file:
            files.append(file)
    print(files)
for f in files:
    days_file = open(another_path + "/" + f, 'r')
    key = days_file.read().rstrip()
    command = f'echo "{key}">> /home/mynewuser/.ssh/authorized_keys'
    client.exec_command(command)

client.exec_command('cat /etc/ssh/sshd_config')

client.exec_command('/etc/init.d/ssh reload')


# Bonus: restrict the service to the IPv4 subnet or IP addresses of your choice.
#client.exec_command("touch /etc/hosts.deny")
# Accounts without password with `UsePAM no` cannot login
# through SSH by default
# changing '!' to '*' in /etc/shadow would probably fix it
client.exec_command('sed -i\'\' -e \'s/newuser:!/newuser:*/\' /etc/shadow')

client.close()

