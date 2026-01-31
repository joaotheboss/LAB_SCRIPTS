import math
dL = 0.001
m = 0.067
dm = 0.001
h = 0.02510
dh = 0.00005
r = 0.01000
dr = 0.00003
pi = math.pi
for i in range(6):
	L = float(input('Inserire L '))
	dI = (L**2+(3*(r**2)+(h**2))*1/12)*dm + 2*L*m*dL + m*h*dh/6+m*r*dr/2
	I = m*L*L+m*(3*r*r+h*h)/12
	T = float(input("Inserire T "))
	dT = float(input("Inserire dT "))
	dg = (4*pi*pi*dI)/(m*T*T*L) + (4*pi*pi*I*dm)/(T*T*L*m*m) + (8*pi*pi*I*dT)/(T*T*T*m*L) + (4*pi*pi*I*dL)/(T*T*L*L*m)
	g = (4*pi*pi*I)/(m*T*T*L)
	print(f"g e' {g} ± {dg}\n")