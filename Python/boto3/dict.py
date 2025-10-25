from collections import Counter
import copy
from operator import itemgetter

def main():
    person = {"name":"Jack","Age":"38","city":"Dallas"}

    print("initial",person,"\n")

    print("name:",person["name"])

    person["Age"] = '28'

    person["email"] = "Jack@example.com"

    del person["city"]

    print("\n")
    print("after changes",person)



if __name__ == "__main__":
    main()

print("\n")

def play():
    box = {"match":"5","apple":"7","banana":"10"}
    print("Boxes are: ",box)

    box["mango"] = "11"

    print("Latest boxes are: ",box)


play()

print("\n")
print("\n")

people = {
    1:{'name':'John','age':'64'},
    2:{'name':'Marie','age':'62'}
}




for person_id,person_details in people.items():
    print("Person ID: ",person_id)

    for key,value in person_details.items():
        print(f" {key} : {value}")



def season():
    stuff = {
        'summer' :{'upper':'t-shirt','lower':'shorts'},
        'winter' :{'upper':'sweater','lower':'woolen pants'}
    }

    for weather,cloth in stuff.items():
        print(weather)

        for key,value in cloth.items():
            print(f" {key}: {value}")
season()

def learnget():

    d = {"a":10,"b":25,"c":30,"d":40,"e":50}
    print(d.get("a"))
    print(d.get("b"))
    print("\n")
    print(d.keys())
    print(d.values())
    print(d.items())
    print("\n")


    for k in d.values():
        if k % 2 == 0:
            print(k)
    result = d.popitem()
    print(result)
    print(d)
    element = d.pop("b")
    print(element)
    print(d)

learnget()


def make():
    cube = {}

    for n in range(1,16):
        cube[n] = n*n*n
    print(cube)
    print("\n")
    print(cube.keys())
    print(cube.values())
    print(cube.items())



    cubes = {n:n*n*n for n in range(1,16)}
    print("cubes",cubes)

    even_cubes = {p: p*p*p for p in range(1,26) if p%2 == 0}
    print("Even Cubes are: ",even_cubes)


make()


def counting():
    text = "mississippi"
    c = Counter(text)
    print("Counter: ", c)
    print(c.most_common(2))

counting()

def copying():
    a = {"x":{"y":1}}
    b = a.copy()
    print("b before the copy",b)

    b["x"]["y"] = 2
    print("After shallow change, a:",a)
    print(b)

    c = copy.deepcopy(a)
    c["x"]["y"] = 99
    print("After deep change,a : ",a)
    print("deep copy c: ",c)
copying()


def sorting():
    peoples= {3:"Jim",2:"Jack",4:"Jane",1:"Jill"}
    print(peoples.items())
    print(peoples.keys())
    print(peoples.values())
    print(sorted(peoples.items()))
    print("\n")

sorting()

def get_name(item):
    return item[1]

def get_key(item):
    return item[0]


peoples= {3:"Jim",2:"Jack",4:"Jane",1:"Jill"}

sorted_by_name = sorted(peoples.items(), key = get_name)
sorted_by_key = sorted(peoples.items(),key = get_key)

print(sorted_by_name)
print(sorted_by_key)


sorted_people = sorted(peoples.items(),key = lambda item:item[1] )

sorted_people_dict = {}

for key, value in sorted_people:
    sorted_people_dict[key] = value

print("Sorted Dictionary is: ",sorted_people_dict)

t = lambda x,y: x*y*90

r = t(55,66)
print(r)


fruit_inventory = [("banana",5),("orange",15),("apple",3),("kiwi",0)]


print(sorted(fruit_inventory,key = itemgetter(0)))

print(sorted(fruit_inventory,key=itemgetter(1)))










