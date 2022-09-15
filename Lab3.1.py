from math import*
r=float(input("Radius "))
x=float(input("x "))
y=float(input("y "))
if x>=-2*r and x<=-r and y<=r and y>=-r or x>=-r and (pow(x-r,2)+y*y)<=r*r:
    print("Принадлежит")
elif x<=2*r and x>=r and y<=r and y>=-r or x<=r and (pow(x+r,2)+y*y)<=r*r:
    print("Принадлежит")
else:
    print("Не принадлежит")
