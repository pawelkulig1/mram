
import math as mt

xmax=1e-08
xmin=0
ymax=2e-10
ymin=0
zmax=2e-10
zmin=0




def dist0(x,y,z):
	w = mt.sqrt(x**2+y**2+z**2)
	#print(w)
	if w==1:
		return 1
	if w>1 and w<mt.sqrt(3):
		return 2
	else:
		return 3
	
S1 = []
S2 = []
S3 = []



#def generateGrid(delx, dely, delz, dx, dy, dz, emitter):
#DANE WEJSCIOWE DO FUNKCJI
dx=1e-10
dy=1e-10
dz=1e-10

delx = 1e-10
dely = 1e-10
delz = 1e-10

#DANE WEJSCIOWE DO FUNKCJI
emiterdx = 1e-10
emiterdy = 1e-10
emiterdz = 1e-10 



for x in range(-1,2,1):
	for y in range(-1,2,1):
		for z in range(-1,2,1):
			if x==0 and y==0 and z==0:
				continue

			if x*emiterdx<=xmax and emiterdx - emiterdx*x>=xmin and emiterdy+emiterdy*y<=ymax and emiterdy-emiterdy*y>=ymin and emiterdz+emiterdz*z<=zmax and emiterdz-emiterdz*z>=zmin:
				print(x*emiterdx+emiterdx,y,z)
				if dist0(x,y,z)==1:
					S1.append([x,y,z])
					continue
			
				if dist0(x,y,z)==2:
					S2.append([x,y,z])
					continue
		
				if dist0(x,y,z)==3:
					S3.append([x,y,z])
		
'''for i in range(len(S1)):
	S1[i][0] = S1[i][0]*dx + delx
	S1[i][1] = S1[i][1]*dy + dely
	S1[i][2] = S1[i][2]*dz + delz
	
for i in range(len(S2)):
	S2[i][0] = S2[i][0]*dx + delz
	S2[i][1] = S2[i][1]*dy + dely
	S2[i][2] = S2[i][2]*dz + delz
	
for i in range(len(S3)):
	S3[i][0] = S3[i][0]*dx + delx
	S3[i][1] = S3[i][1]*dy + dely
	S3[i][2] = S3[i][2]*dz + delz
	

'''

print(S1, S2, S3)