from math import*
from random import*
from copy import*
for x in range(1,10):
    num=random.randint(1,10)
    while num in result:
        num=random.randint(1,10)
    result.append(num)
print (result)
