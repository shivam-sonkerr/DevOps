import re

phoneNumRegex = re.compile(r'\d\d\d-\d\d\d-\d\d\d\d')

mo = phoneNumRegex.search('My number is 415-555-4242.')

print('Phone number found: ' + mo.group())


phoneNumRegexx = re.compile(r'(\d\d\d)-(\d\d\d-\d\d\d\d)')

m = phoneNumRegexx.search('My number is 415-555-4245.')

print('Phone number is: '+ m.group())
print('Phone number is: '+ m.group(0))
print('Phone number is: '+ m.group(1))
print('Phone number is: '+ m.group(2))
print(m.groups())

batRegex = re.compile(r'Bat(man)+')

# mo1 = batRegex.search('The Adventures of Batman')

# print(mo1.group())

# mo2 = batRegex.search('The Adventures of Batwoman and Batman')
# print(mo2.group())

print(batRegex.findall('The Adventures of Batwoman and Batman'))


vowelRegex = re.compile(r'[aeiouAEIOU]')

print(vowelRegex.findall('The'))