import random
import pprint
"""Вариант 3:
Вывести получившийся словарь на экран. (Словарь №1)
Создать еще два пустых словаря (№2 и №3) и тоже вывести их на экран.
В бесконечном цикле предлагать пользователю ввести номер словаря и ключ, который
затем нужно переместить (вместе со значением) в один из двух других словарей
выбирая его случайно. При каждом перемещении все словари нужно выводить заново
"""
def vibor(rand1, b, c, d):
    cc = input("Введите ключ который окажется в одном из 2 словарей: ")
    if rand1 == 0:
        c[cc] = b[cc]
        del b[cc]
    elif rand1 == 1:

        d[cc] = b[cc]
        del b[cc]

def slov():
    d = {}

    with open("text.txt") as f:
        for line in f:
            if line != "\n":
                key, *value = line.split()
                d[key] = value
    return d
a=1

b=slov()

c={}

d={}

pp = pprint.PrettyPrinter(indent=1)
print("Cловарь 1")
pp.pprint(b)
print("Cловарь 2")
pp.pprint(c)
print("Cловарь 3")
pp.pprint(d)
while a>0:
    aa=int(input("Номер словаря: "))
    if aa==1:
        vibor(random.randint(0, 1),b,c,d)
    elif aa==2:

        vibor(random.randint(0, 1),c,b,d)

    elif aa==3:

        vibor(random.randint(0, 1),d,c,b)

    else:
        print ("Такого словаря нет")
    print("Cловарь 1")

    pp.pprint(b)
    print("Cловарь 2")
    pp.pprint(c)
    print("Cловарь 3")
    pp.pprint(d)


    a=int(input("Если хотите продолжить напишите положительое число"))
