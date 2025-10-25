from copy import deepcopy

def fib_gen(stop):
    current_fib, next_fib = 0,1
    for _ in range(0,stop):
        fib_number = current_fib
        current_fib, next_fib = next_fib, current_fib+ next_fib
        yield fib_number


fib_gen(10)

print(list(fib_gen(10)))

t = [number**2 for number in range(1,11)]

print(t)

k = [z*90 for z in range(10,20)]

print(k)

letters = ["A","a","B","b","C","c","D","d"]

uppercase = letters[0::2]

lowercase = letters[1::2]


print(uppercase,lowercase)

print(uppercase)


digits = [0,1,2,3,4,5,6,7,8]

first_four = digits[:4]
print(first_four)

last_three = digits[-3:]
print(last_three)


countries = ["United States","Canada","India","Japan"]

print(countries)

nations = countries.copy()

print(nations)

national = deepcopy(countries)

print(national)

numbers = [1,5,6,7]
numbers[1:1] = [2,3,4]
print(numbers)

nums = [1,2,0,0,0,0,4,5,6,7]
nums[2:6] = [3]
print(nums)

nums.append(8)
print(nums)

nums.extend([9,10,11])
print(nums)

print(nums*2)

print(list(reversed(nums)))
print(nums[::-1])


usernames = ["john","jane","bob","david","eve"]

print("linda" in usernames)

print("linda" not in usernames)