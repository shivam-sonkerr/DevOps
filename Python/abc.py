import learn_csv
import pprint




# print("What is your name")
# myname = input()
# print(myname)
# print(len(myname))


number = 7

if number<8:
    print('less')
else:
    print('greater')


spam =0

while spam< 6:
    print("Hello")
    spam = spam+1
    print(type(spam))


for i in range(9):
    print("YES/NO")


grand_total = 1000
for number in range(1000):
    grand_total = grand_total + number
print(grand_total)


grand_tot = 1000
for number in range(1,5):
    grand_tot = grand_tot * number
print(grand_tot)



def hello():
    print('Hello there!')

hello()




def testing(n):
    n = n*108
    return n

result = testing(5000)
print(result)


num = [1,3,5,7,9,11]

print(num[-1])

print(num[1:5])


num.append(13)
print(num)

num.insert(1,15)
print(num)

for i in num:
    print(num[2]*5)

num.sort(reverse=True)
print(num)

num.reverse()
print(num)

spam = {'color':'green','name':'John'}

for y in spam.keys():
    print(y)

for z in spam.items():
    print(z)

spam.setdefault('colour', 'pink')
print(spam)


allGuests = {'Alice': {'apples':5,'pretzels':12},
             'Bob':{'sandwiches':5,'apples':2},
             'Carol':{'cups': 3,'apple pies':7}}

for k in allGuests:
    print(allGuests.keys())
    print(allGuests.values())


def totalBrought(guests,item):
    numBrought=0
    for j,k in guests.items():
        numBrought = numBrought + k.get(item,0)
    return numBrought

abc = totalBrought(allGuests,'apples')
print(abc)
