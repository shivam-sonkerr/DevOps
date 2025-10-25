import uuid
import time
import datetime

random_uuid = uuid.uuid4()
print(random_uuid)


timestamp = time.time()
print(timestamp)

bucket_name = str(random_uuid)+str(timestamp)

print(bucket_name)

time= datetime.datetime.now()
formatted_time = time.strftime("%Y-%m-%d")
print(time)
print(formatted_time)

final_name = "Bucket_"+formatted_time
print(final_name)