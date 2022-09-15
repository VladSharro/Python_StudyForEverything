lst = []
dct = {}
def make_list():
    from random import random
    lst=[[randint(-100, 100) for i in range(4)] for j in range(13)]
    return A
def analysis():
    for i in lst:
        if i in dct:
            dct[i] += 1
        else:
            dct[i] = 1  
 
make_list()
analysis()
for i in sorted(dct):
    print("'%d':%d" % (i,dct[i])
