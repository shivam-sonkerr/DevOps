import csv
import json
import time
import threading


start = time.time()
print(start)
print('\n')
file = open('/Users/shivam/Downloads/Automate_the_Boring_Stuff_3e_onlinematerials/exampleWithHeader3.csv',encoding = 'utf-8')

filereader = csv.reader(file)

# filedata = list(filereader)
#
# print(filedata)

for row in filereader:


    # print('\n')
    print('Row#' +str(filereader.line_num)+''+str(row))




stringOfJsonData = '{"name": "Sophie", "isCat": true, "miceCaught": 0,"felineIQ": null}'

pythonValue = {'isCat': True, 'miceCaught': 0, 'name': 'Sophie','felineIQ': None}

data = json.loads(stringOfJsonData)

dumps = json.dumps(pythonValue)

print(data)
print(dumps)
print('\n')

end= time.time()

totalTimeTaken = end - start

print(totalTimeTaken)

print(round(totalTimeTaken,7))



