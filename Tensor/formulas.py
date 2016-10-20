import math as mt

def radius(x,y,z):
	return mt.sqrt(x**2 + y**2 + z**2)
	

def f(x,y,z):
	R = radius(x, y, z)
	return (
		0.5*y*(z**2 - x**2) * mt.asinh(y/(mt.sqrt(x**2 + z**2)))
		+ 0.5*z*(y**2 - x**2) * mt.asinh(z/(mt.sqrt(x**2 + y**2)))
		- x*y*z*((y*z)/(x*R))
		+ (1/6)*R*(2*x**2 - y**2 - z**2)
	)

def g(x,y,z):
	R = radius(x, y, z)
	
	return (
		x*y*z*mt.asinh(z/(mt.sqrt(x**2 + y**2)))
		+ (1/6)*y*(3*z**2 - y**2) * mt.asinh(x/(mt.sqrt(y**2 + z**2)))
		+ (1/6)*x*(3*z**2 - x**2) * mt.asinh(y/(mt.sqrt(x**2 + z**2)))
		- 0.5*y**2*z * mt.atan((x*z)/(y*R))
		- 0.5*x**2*z * mt.atan((y*z)/(x*R))
		- (1/6)*z**3 * mt.atan((x*y)/(z*R))
		- (1/3)*x*y*R
	)


def Nxx(delx, dely, delz, dx, dy, dz):
	#TODO SUMS
	return (
		(1/(4*mt.pi*dx*dy*dz))*(8*f(delx, dely, delz)-4*...)
	)

def Nxy(delx, dely, delz, dx, dy, dz):
	#TODO SUMS
	return (
		(1/(4*mt.pi*dx*dy*dz))*(8*f(delx, dely, delz)-4*...)
	)
	
#
#print(f(1,1,1))
#print(g(1,1,1))


