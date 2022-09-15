from math import*
r=float(input("Radius "))
x=float(input("x "))
y=float(input("y "))
if x>=-2*r and y>=-r and y<=r or (pow(x-r,2)+y*y)<=r*r and x<=2*r:
    print("Принадлежит")
elif x<=2*r and y<=r and y>=-r or (pow(x+r,2)+y*y)<=r*r and x>=-2*r:
    print("Принадлежит")
else:
    print("Не принадлежит")
