import subprocess

p1 = subprocess.Popen(["ls"])

f = open("user.txt","w")

p2 = subprocess.Popen(["whoami"],text=True,stdout = f)



p3 = subprocess.Popen(["ps","aux"],text=True,stdout=subprocess.PIPE)
p4 = subprocess.Popen(["grep","python"],stdin = p3.stdout,stdout=subprocess.PIPE)

p3.stdout.close()

output = p4.communicate()[0].decode()
print(output)


p5 = subprocess.Popen(["ping","-c","3","google.com"],text=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)

for line in p5.stdout:
    print(line)


print("Please enter the text")
text = input()

p6 = subprocess.Popen(["echo",text],text=True)

