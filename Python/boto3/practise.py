countries ={'USA':'Washington','India':'New Delhi','Australia':'Canberra'}

print(countries)

print(countries.values())

print(countries['India'])

countries['Japan'] = 'Tokyo'

print(countries)

countries['USA'] = 'Washington DC'

print(countries)
print("\n")

for text in countries.keys():
    if text=='France':
        print("France exists")
        break
else:
        print("Does not exist")


hex = {'red':'#ff0000','green':'#3cb371','yellow':'#ffa500'}

print(hex)
print("\n")


for key in hex.keys():
    print(key)

print("\n")

for codes in hex.values():
    print(codes)

animal = {'Horse':'neigh','dog':'bark','cat':'meow'}

print(animal['dog'])

del (animal['cat'])

print(animal)

print(animal.get('cow'))

random = {}

random['name'] = 'john'
random['age'] = '21'
random['city'] = 'Arizona'

print(random,"\n")

for counting in random.keys():
    print(counting)
