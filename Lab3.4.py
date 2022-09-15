from math import*
r=float(input("Radius "))
x=float(input("x "))
y=float(input("y "))
x=abs(x)
y=abs(y)
if x>r and x<=2*r and y<=r:
    print("Попадает")
elif x<=r and (pow(x+r,2)+y*y)<=r*r:
    print("Попадает")
else:
    print("Не попадает")
