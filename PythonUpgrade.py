import paramiko
import urllib.request
import os
import subprocess

# get the current and desired Python versions
current_version = subprocess.check_output('python --version', shell=True).decode('utf-8').strip()
desired_version = '3.10.0'

# get the remote system name and login credentials
remote_system = input("Enter remote system name or IP address: ")
remote_user = input("Enter remote username: ")
remote_password = input("Enter remote password: ")

# connect to the remote system using SSH
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(remote_system, username=remote_user, password=remote_password)

# download the latest Python installer based on the remote system
stdin, stdout, stderr = ssh_client.exec_command('uname')
system = stdout.read().decode('utf-8').strip().lower()
if system == 'windows':
    url = f'https://www.python.org/ftp/python/{desired_version}/python-{desired_version}-amd64.exe'
    filename = f'python-{desired_version}-amd64.exe'
    urllib.request.urlretrieve(url, filename)
    sftp_client = ssh_client.open_sftp()
    sftp_client.put(filename, filename)
    sftp_client.close()
elif system == 'darwin':
    url = f'https://www.python.org/ftp/python/{desired_version}/python-{desired_version}-macosx10.9.pkg'
    filename = f'python-{desired_version}-macosx10.9.pkg'
    urllib.request.urlretrieve(url, filename)
    sftp_client = ssh_client.open_sftp()
    sftp_client.put(filename, filename)
    sftp_client.close()
else:
    url = f'https://www.python.org/ftp/python/{desired_version}/Python-{desired_version}.tgz'
    filename = f'Python-{desired_version}.tgz'
    urllib.request.urlretrieve(url, filename)
    sftp_client = ssh_client.open_sftp()
    sftp_client.put(filename, filename)
    sftp_client.close()

# run the installer with command line arguments
if system == 'windows':
    stdin, stdout, stderr = ssh_client.exec_command(f'{filename} /quiet InstallAllUsers=1 PrependPath=1')
elif system == 'darwin':
    stdin, stdout, stderr = ssh_client.exec_command(f'sudo installer -pkg {filename} -target /')
else:
    stdin, stdout, stderr = ssh_client.exec_command(f'tar -zxvf {filename}')
    stdin, stdout, stderr = ssh_client.exec_command(f'cd Python-{desired_version} && ./configure && make && sudo make install')

# remove the installer file
stdin, stdout, stderr = ssh_client.exec_command(f'rm {filename}')

# close the SSH connection
ssh_client.close()

# verify the Python version
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(remote_system, username=remote_user, password=remote_password)
stdin, stdout, stderr = ssh_client.exec_command('python --version')
output = stdout.read().decode('utf-8').strip()
if output == f'Python {desired_version}':
    print(f'Successfully upgraded Python from {current_version} to {desired_version} on {remote_system}.')
else:
    print('Python upgrade failed.')
ssh_client.close()