from math import*
r=float(input("Radius "))
x=float(input("x "))
y=float(input("y "))
okr=abs((pow(x+r,2)+y*y))
if abs(x>=r) and abs(x<=2*r):
    if abs(x<=2*r) and abs(y<=r):
        print("Принадлежит")
    else:
        if okr<=r*r:
          print("Пинаджежит")
        else:
          print("Не принадлежитъ")
else:
    print("Не принадлежит")
