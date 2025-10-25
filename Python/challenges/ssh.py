import paramiko


client = paramiko.SSHClient()

client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect(
    hostname = "37.27.30.5",
    username = "root",
    password = "hznibba123",
    look_for_keys= False,
    allow_agent=False,
)

commands = ["whoami","pwd","ls -l"]

for command in commands:
    stdin,stdout,stderr = client.exec_command(command)
    print(stdout.read().decode().strip())


sftp_client = client.open_sftp()
localFilePath = "/Users/shivam/nsswitch.conf"
remoteFilePath = "user.txt"

file_need = "nsswitch.conf"

sftp_client.chdir("/etc/")

sftp_client.get(file_need,localFilePath)

files = sftp_client.listdir("/var/log")
print(files)

sftp_client.close()
client.close()


