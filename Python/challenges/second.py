import subprocess

p1 = subprocess.run(["ls"],text=True,stdout=subprocess.PIPE)

print(p1)

print(p1.stdout)


p2 = subprocess.Popen(["ls","-lrth","/Users/shivam/Downloads"], text=True,stderr=subprocess.PIPE)


print(p2.communicate())

print(p2.returncode)

if p2.returncode == 0:
    print("Command Succeeded")
else:
    print("Command Failed")



p3 = subprocess.run(["date"])

print(p3.returncode)

if p3.returncode ==0:
    p4 = subprocess.Popen(["uptime"])
    print(p4.communicate(timeout=5))

    p5 = subprocess.Popen(["uptime"])

    print(p5.communicate())



file = open("disk_usage.txt",'w')
p6 = subprocess.Popen(["df","-h"],text=True,stdout=subprocess.PIPE)

stdout,stderr = p6.communicate()

if p6.returncode ==0 :
    file.write(stdout)



# print(p6)


p7 = subprocess.Popen(["ps","aux"],text=True,stdout=subprocess.PIPE)
p8 = subprocess.Popen(["grep","Python"],text=True,stdin = p7.stdout,stdout=subprocess.PIPE)
p9 = subprocess.Popen(["sort"],stdin=p8.stdout,text=True,stdout=subprocess.PIPE)

print(p9.communicate())


text = "Hello from stdin"

p10 = subprocess.Popen(["echo",text])
p11 = subprocess.Popen(["cat"],stdin = p10.stdout,text=True,stdout=subprocess.PIPE)

# print(p11.communicate())

# p12 = subprocess.Popen(["sleep","10"])
# exit_code = p12.wait(3)
# print(exit_code)


p13 = subprocess.Popen(["mkdir -p test_folder && cd test_folder && touch file.txt"],shell=True)

p14 = subprocess.Popen(["curl https://api.github.com"],text=True,shell=True,stdout=subprocess.PIPE)
p15 = subprocess.Popen(["grep","-i","current_user_url"],stdin = p14.stdout)

print(p15.communicate())

try:
    p16 = subprocess.Popen(["wrongcommand"],text=True,stdout= subprocess.PIPE)
except FileNotFoundError:
    print("Command given is wrong")