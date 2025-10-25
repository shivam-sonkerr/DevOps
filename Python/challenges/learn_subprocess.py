import subprocess


result = subprocess.run(["ls","-lrth"],capture_output = True,text = True)

print(result.stdout)
print(result.returncode)

print(subprocess.run("echo $HOME",shell= True))

print(subprocess.run("whoami",shell= True))

dire = subprocess.run(["ls","-lrth"],cwd="/etc",capture_output=True,text=True)

print(dire.stdout)
print(dire.stderr)

sudo = subprocess.run(["cat","/etc/sudoers"],capture_output=True,text=True)

print(sudo)

proc = subprocess.Popen(["ls","-lrth"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)

stdout,stderr = proc.communicate()

print(proc.returncode)
print("STDOUT: ",stdout)
print("STDERR: ",stderr)

proc = subprocess.Popen(["ping","-c","4","gmail.com"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)

for line in proc.stdout:
    print(line.strip())


p1 = subprocess.Popen(["ps","aux"],stdout=subprocess.PIPE)
p2 = subprocess.Popen(["grep","Applications"],stdin = p1.stdout,stdout=subprocess.PIPE)

p1.stdout.close()

output = p2.communicate()[0].decode()
print(output)

subprocess.run(["python","/Users/shivam/IdeaProjects/DevOps/Python/timer.py","5"],check=True)

subprocess.run(["open","-e"])