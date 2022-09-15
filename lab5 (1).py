from math import*
from random import*
from copy import*
def Matrix():
    A=[[randint(1,52) for i in range(4)] for j in range(13)]  
    return A
    for x in range(len(A)):
        num=random.randint(1,52)
        while num in result:
            num=random.randint(1,52)
        result.append(num)

def Vivod(A):
    print("Матрица:")
    for i in range(len(A)):
        for j in range(len(A[i])):
            print(A[i][j], end=' ')
        print()
result=[] 
A=Matrix()
Vivod(A)

