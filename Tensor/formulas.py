import math as mt

class Block:
    def __init__(self, width, depth, height, xpoz, ypoz, zpoz, wElements, dElements, hElements):
        self.smallBlocksStructure = []
        self.xpoz = xpoz
        self.ypoz = ypoz
        self.zpoz = zpoz

        self.width = width
        self.depth = depth
        self.height = height

        self.wElements = int(wElements)
        self.dElements = int(dElements)
        self.hElements = int(hElements)

        self.widthSmall = (self.width / self.wElements)
        self.depthSmall = (self.depth / self.dElements)
        self.heightSmall = (self.height / self.hElements)
        self.nElements = int(
            round((self.width * self.depth * self.height) / (self.widthSmall * self.depthSmall * self.heightSmall)))

    def isInStructure(self, xpoint, ypoint, zpoint):
        return True

    def createStructure(self):
        startw = (self.widthSmall / 2) + self.xpoz
        startd = (self.depthSmall / 2) + self.ypoz
        starth = (self.heightSmall / 2) + self.zpoz

        #print(startw, starth, startd, self.widthSmall, self.depthSmall, self.heightSmall)
        #print(self.width, self.depth, self.height)
        #print(self.wElements, self.dElements, self.hElements)

        for i in range(self.wElements):
            for j in range(self.dElements):
                for k in range(self.hElements):
                    if self.isInStructure(startw+self.widthSmall*i, startd+self.depthSmall*j, starth+self.heightSmall*k):
                        self.smallBlocksStructure.append([startw+self.widthSmall*i, startd+self.depthSmall*j, starth+self.heightSmall*k])
        self.nElements = len(self.smallBlocksStructure)

class Rectangle(Block):
    def __init__(self, width, depth, height, xpoz, ypoz, zpoz, wElements, dElements, hElements):
        super(Rectangle, self).__init__(width, depth, height, xpoz, ypoz, zpoz, wElements, dElements, hElements)

    # all objects from rectangle are inside of rectangular shape
    def isInStructure(self, xpoint, ypoint, zpoint):
        return True


class Ellipse(Block):
    def __init__(self, a, b, height, axis, xpoz, ypoz, zpoz, wElements, dElements, hElements):
        # axis is 0 for x,y; 1 for y,z; and 2 for x,z
        self.axis = axis
        #if self.axis == 0:
        super(Ellipse, self).__init__(a, b, height, xpoz, ypoz, zpoz, wElements, dElements, hElements)
        '''elif self.axis == 1:
            super(Ellipse, self).__init__(height, a, b, xpoz, ypoz, zpoz, hElements, wElements, dElements)
        else:
            super(Ellipse, self).__init__(a, height, b, xpoz, ypoz, zpoz, wElements, dElements, hElements)
        '''
    def isInStructure(self, xpoint, ypoint, zpoint):
        if self.axis == 0:
            if ((xpoint - self.width - self.xpoz) ** 2 / self.width ** 2) + ((ypoint - self.depth- self.ypoz) ** 2 /                                    self.depth ** 2) <= 1 and zpoint <= self.zpoz + self.height and zpoint >= self.zpoz:
                return True


        elif self.axis == 1:
            if ((ypoint - self.depth - self.ypoz) ** 2 / (self.depth ** 2)) + ((zpoint - self.height - self.zpoz) ** 2 / (self.height ** 2)) <= 1 and xpoint <= self.xpoz + self.width and xpoint >= self.xpoz:
                return True

        else:
            if ((xpoint - self.width - self.xpoz) ** 2 / self.width ** 2) + ((zpoint - self.height - self.zpoz) ** 2 / self.height ** 2) <= 1 and ypoint <= self.ypoz + self.height and ypoint >= self.ypoz:
                return True
            
        return False


def radius(x, y, z):
    return mt.sqrt(x ** 2 + y ** 2 + z ** 2)

def wspolczynnik(delx, dely, delz, x, y, z, emitter):
    xx = abs(x - delx) / (emitter.widthSmall)
    yy = abs(y - dely) / (emitter.heightSmall)
    zz = abs(z - delz) / (emitter.depthSmall)

    if int(xx + yy + zz + 0.5) == 0:
        return 8.0
    if int(xx + yy + zz + 0.5) == 1:
        return -4.0
    if int(xx + yy + zz + 0.5) == 2:
        return 2.0
    else:
        return -1.0

def f(x, y, z):
    R = radius(x, y, z)

    # solving 0 division problem here

    if x == 0 and z == 0 or y == 0:
        part1 = 0
    else:
        part1 = 0.5 * y * (z ** 2 - x ** 2) * mt.asinh(y / (mt.sqrt(x ** 2 + z ** 2)))

    if x == 0 and y == 0 or z == 0:
        part2 = 0
    else:
        part2 = 0.5 * z * (y ** 2 - x ** 2) * mt.asinh(z / (mt.sqrt(x ** 2 + y ** 2)))

    if x == 0 or y == 0 or z == 0:
        part3 = 0
    else:
        part3 = x * y * z * mt.atan((y * z) / (x * R))

    # solving 0 division problem here

    part4 = (1 / 6.0) * R * (2 * x ** 2 - y ** 2 - z ** 2)

    return part1 + part2 - part3 + part4

def g(x, y, z):
    R = radius(x, y, z)

    if x == 0 and y == 0:
        part1 = 0
    else:
        part1 = x * y * z * mt.asinh(z / (mt.sqrt(x ** 2 + y ** 2)))

    if y == 0 and z == 0:
        part2 = 0
    else:
        part2 = (1 / 6.0) * y * (3 * z ** 2 - y ** 2) * mt.asinh(x / (mt.sqrt(y ** 2 + z ** 2)))

    if x == 0 and z == 0:
        part3 = 0
    else:
        part3 = (1 / 6.0) * x * (3 * z ** 2 - x ** 2) * mt.asinh(y / (mt.sqrt(x ** 2 + z ** 2)))

    if y == 0:
        part4 = 0
    else:
        part4 = 0.5 * (y ** 2) * z * mt.atan((x * z) / (y * R))

    if x == 0:
        part5 = 0
    else:
        part5 = 0.5 * (x ** 2) * z * mt.atan((y * z) / (x * R))

    if z == 0:
        part6 = 0
    else:
        part6 = (1 / 6.0) * z ** 3 * mt.atan((x * y) / (z * R))

    part7 = (1 / 3.0) * x * y * R

    return part1 + part2 + part3 - part4 - part5 - part6 - part7

def calculateNxx(delx, dely, delz, dx, dy, dz, emitter):
    xran = [delx - dx, delx, delx + dx]
    yran = [dely - dy, dely, dely + dy]
    zran = [delz - dz, delz, delz + dz]

    Nxx = 0

    for x in xran:
        for y in yran:
            for z in zran:
                Nxx += wspolczynnik(delx, dely, delz, x, y, z, emitter) * f(x, y, z)

    return Nxx

def calculateNxy(delx, dely, delz, dx, dy, dz, emitter):
    xran = [delx - dx, delx, delx + dx]
    yran = [dely - dy, dely, dely + dy]
    zran = [delz - dz, delz, delz + dz]

    Nxy = 0

    for x in xran:
        for y in yran:
            for z in zran:
                Nxy += wspolczynnik(delx, dely, delz, x, y, z, emitter) * g(x, y, z)

    return Nxy

def calculateDistance(cell1, cell2):
    return abs(cell1[0]-cell2[0]), abs(cell1[1]-cell2[1]), abs(cell1[2]-cell2[2])
