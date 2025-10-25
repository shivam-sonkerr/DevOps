import random
class Sample:
    def __init__(self):
        pass
    def gennum(self):
        return random.randint(1,99)


s1 = Sample()
print(s1.gennum())