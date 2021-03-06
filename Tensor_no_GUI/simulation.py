from formulas import *
import multiprocessing
from time import sleep
import mpmath as mp
import math as mt

#calculateNxxLookUp = mp.memoize(calculateNxx)
#calculateNxyLookUp = mp.memoize(calculateNxy)
#calculateDistanceLookUp = mp.memoize(calculateDistance) 

def saveToFile(data):
	f = open("out.txt", "w")
	temp = "["+str(data[0])+" "+str(data[1])+" "+str(data[2])+"]\n["+str(data[3])+" "+str(data[4])+" "+str(data[5])+"]\n["+str(data[6])+" "+str(data[7])+" "+str(data[8])+"]"
	f.write(temp)
	f.close()

def simulate(emi, rec, nThreads=0):
    mp.mp.dps = 64
    
    if emi.axis == '-1':
        emitter = Rectangle(emi.width, emi.depth, emi.height, emi.x, emi.y, emi.z, emi.widthEl, emi.depthEl,
                            emi.heightEl)
    else:
        emitter = Ellipse(emi.width, emi.depth, emi.height, emi.axis, emi.x, emi.y, emi.z, emi.widthEl, emi.depthEl,
                          emi.heightEl)
    if rec.axis == '-1':
        receiver = Rectangle(rec.width, rec.depth, rec.height, rec.x, rec.y, rec.z, rec.widthEl, rec.depthEl,
                             rec.heightEl)
    else:
        receiver = Ellipse(rec.width, rec.depth, rec.height, rec.axis, rec.x, rec.y, rec.z, rec.widthEl,
                           rec.depthEl, rec.heightEl)

    receiver.createStructure()
    emitter.createStructure()

    thread = []

    if nThreads < 1:
        nThreads = multiprocessing.cpu_count()
    print("Blocks in simulation: ", receiver.nElements*emitter.nElements)
    manager = multiprocessing.Manager()
    avgMatrix = manager.list()

    for i in range(nThreads):

        onThread = mp.floor(receiver.nElements / nThreads)
        thisThreadStart = onThread * (i + 0)
        
        if i == nThreads - 1:
            thisThreadEnd = receiver.nElements
        else:
            thisThreadEnd = onThread * (i + 1)
        process = multiprocessing.Process(target=calculateAllAverages, args=(
            thisThreadStart, thisThreadEnd, nThreads, receiver, emitter, avgMatrix))
        thread.append(process)
        thread[i].start()

    # starting calculations in main thread to send signals to GUI
    #calculateAllAverages(0, mt.floor(receiver.nElements / nThreads), nThreads, receiver, emitter,avgMatrix)
    for i in range(nThreads):
        thread[i].join()

    finalMatrix = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # create sum of all matrixes to calculate average
    for k, e in enumerate(avgMatrix):
        for i, e in enumerate(avgMatrix[0]):
            finalMatrix[i] += avgMatrix[k][i]

    # divide sum by all elements
    for k, e in enumerate(avgMatrix[0]):
        finalMatrix[k] /= len(avgMatrix)
        finalMatrix[k] *= (emitter.nElements / (4 * mp.pi * emitter.widthSmall * emitter.depthSmall * emitter.heightSmall))

    mp.mp.dps = 15
    #mp.mp.pretty = True
    avgMatrix = []
    print("[", finalMatrix[0], finalMatrix[1], finalMatrix[2], "]")
    print("[", finalMatrix[3], finalMatrix[4], finalMatrix[5], "]")
    print("[", finalMatrix[6], finalMatrix[7], finalMatrix[8], "]")
    saveToFile(finalMatrix)
    return finalMatrix




def calculateAllAverages(start, stop, nThreads, receiver, emitter, avgMatrix):
    calculateNxxLookUp = mp.memoize(calculateNxx)
    calculateNxyLookUp = mp.memoize(calculateNxy)
    fLookUP = mp.memoize(f)
    gLookUP = mp.memoize(g)
    
    start = int(float(mp.nstr(start)))
    stop = int(float(mp.nstr(stop)))
    
    for j in range(start, stop):
        if (start == 0):
            print(mp.nstr(((j * 100) / receiver.nElements) * nThreads, 4), "%")

        a11 = mp.mpf('0')
        a12 = mp.mpf('0')
        a13 = mp.mpf('0')
        a22 = mp.mpf('0')
        a23 = mp.mpf('0')
        a33 = mp.mpf('0')

        emEle = int(float(mp.nstr(emitter.nElements)))

        for i in range(emEle):
            delx, dely, delz = calculateDistance(emitter.smallBlocksStructure[i], receiver.smallBlocksStructure[j])
            dx = emitter.widthSmall
            dy = emitter.depthSmall
            dz = emitter.heightSmall



            a11 += calculateNxxLookUp(delx, dely, delz, dx, dy, dz, emitter, fLookUP)
            a12 += calculateNxyLookUp(delx, dely, delz, dx, dy, dz, emitter, gLookUP)
            a13 += calculateNxyLookUp(delx, delz, dely, dx, dz, dy, emitter, gLookUP)
            a22 += calculateNxxLookUp(dely, delx, delz, dy, dx, dz, emitter, fLookUP)
            a23 += calculateNxyLookUp(dely, delz, delx, dy, dz, dx, emitter, gLookUP)
            # a31 = a13
            # a32 = a23
            a33 += calculateNxxLookUp(delz, dely, delx, dz, dy, dx, emitter, fLookUP)

        a11 = a11 / emitter.nElements
        a12 = a12 / emitter.nElements
        a13 = a13 / emitter.nElements
        a22 = a22 / emitter.nElements
        a23 = a23 / emitter.nElements
        a33 = a33 / emitter.nElements


        avgMatrix.append([a11, a12, a13, a12, a22, a23, a13, a23, a33])
    return avgMatrix
