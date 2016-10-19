import math as mt

class block:
	def __init__(self, xpoz=0, ypoz=0, zpoz=0, width=50, height=10, depth=10, nElements = 1000):
		#define central cordinates of block
		self.xpoz = xpoz
		self.ypoz = ypoz
		self.zpoz = zpoz

		#define size of block in nm.
		self.width = width
		self.height = height
		self.depth = depth

		#how many pieces to consider
		self.nElements = nElements
		self.calcSmallSize()
		
		
		
	def calcSmallSize(self):
		ratio = self.nElements**(1/3)
	
		self.widthSmall = self.width/ratio;
		self.heightSmall = self.height/ratio;
		self.depthSmall = self.depth/ratio;
	
	#returns size of small blocks created from origin block
	def getSmallSize(self):
		return self.widthSmall, self.depthSmall, self.heightSmall
		
	'''
		return x,y,z cordinates for small block with given number, numbers goes from bottom-front-left corner to top-back-right (from 0 to (n-1)) it can be understood as 2-dimensional arrays stacked level by level
	'''
	def smallPoz(self, number):
		if self.width==0:
			raise NameError("Probably block smallSize was not called")
		
		#calculate position of block in my cordinates height, depth, width
		blocksPerLevel = round(self.width/self.widthSmall * self.depth/self.depthSmall)
		blocksPerWidth = round(self.width/self.widthSmall)
		blocksPerDepth = round(self.depth/self.depthSmall)
		

		level = mt.floor(number/blocksPerLevel)
		number = number - level*blocksPerLevel
		
		depthLevel = mt.floor(number/blocksPerWidth)
		number = number - depthLevel*blocksPerWidth
		
		widthLevel = number
		number = number - widthLevel
		
		if(number!=0): #it should never be true otherwise better to raise exception cause weird things may happen
			raise NameError("Error while calculating poz of element")

		xpozSmall = self.xpoz+widthLevel*self.widthSmall + 0.5*self.widthSmall
		ypozSmall = self.zpoz+depthLevel*self.depthSmall + 0.5*self.depthSmall
		zpozSmall = self.ypoz+level*self.heightSmall + 0.5*self.heightSmall
				
		return xpozSmall, ypozSmall, zpozSmall



class smallBlock:
	def __init__(self, xpoz, ypoz, zpoz, width, depth, height):
		#define central cordinates of block
		self.xpoz = xpoz
		self.ypoz = ypoz
		self.zpoz = zpoz

		#define size of block in nm.
		self.width = width
		self.height = height
		self.depth = depth
	
	def getCoordinates(self):
		return self.xpoz, self.ypoz, self. zpoz




#define big structure that is goind to be cut
source = block()


#for each small part create object
sourceDevided = []
for i in range(source.nElements):
	x, y, z = source.smallPoz(i)
	w, h, d = source.getSmallSize()
	sourceDevided.append(smallBlock(x,y,z, w,h,d))

print(sourceDevided[10].xpoz, sourceDevided[10].ypoz, sourceDevided[10].zpoz)



