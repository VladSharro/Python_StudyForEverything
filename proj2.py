from math import*
a=float(input("Input number: "))
check = True
while check:
    if a<-6 or a>5:
      print("Вышли за ОДЗ")
      a=float(input("Input number: "))
    else:
        check = False
if a>=-6 and a<-5:
    y=2
elif a>=-5 and a<=-1: 
    b=4-pow(a+3, 2)
    y=2-(pow(b, 1/2))
elif a>-1 and a<1:
    y=cosh(2*a)
elif a>=1 and a<2 or a>4:
    y=0
elif a>=2 and a<=4:
    b=pow(a-3, 2)
    y=1-(pow(b, 1/2))
print("y= ","%.5f" % (y))
