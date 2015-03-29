def getDataFunc(fileVis, fileBlue):
	import numpy as np
	import matplotlib.pyplot as plt
	import pdb
	import math
	#tmp115.dat is c0 image, visual filter, 6s
	#tmp116.dat is c0 image, blue filter, 6s
	 
	#---------------- Read in data ----------------------------------------------------------#
	#exp time 6s
	tmpV_array = np.genfromtxt(fileVis, comments="#") #Visual
	tmpB_array = np.genfromtxt(fileBlue, comments="#") #Blue 
 
	tmpVx_array = tmpV_array[:,0]
	tmpVy_array = tmpV_array[:,1]
	tmpBx_array = tmpB_array[:,0]
	tmpBy_array = tmpB_array[:,1]
 
	#------------ Remove bad rows from V ----------------------------------------------------#
	bad_col1 = 1002
	bad_Vrows1 = np.array(np.where(np.abs((tmpVx_array - bad_col1)) < 1.))
 
	bad_col2 = 255
	bad_Vrows2 = np.array(np.where(np.abs((tmpVx_array - bad_col2)) < 1.))
 
	bad_Vrows = np.append(bad_Vrows1, bad_Vrows2)
 
	tmpVx_array_clipped = np.delete(tmpVx_array, bad_Vrows)
	tmpVy_array_clipped = np.delete(tmpVy_array, bad_Vrows)
 
	#------ For every row of V, find matching x and y values in B ---------------------------#
 
	#Create list to store matching rows
	Vlist = np.array(np.int_([]))
	Blist = np.array(np.int_([]))
 
	#Pixel value must be within n for a match
	n = 5
	#Offset is the row where values start in tmp.dat file after comments.
	#offset = 18 ######SET TO ZERO
	offset = 0
 
	for i in range(0, tmpVx_array_clipped.size-1):
		Vx = tmpVx_array_clipped[i]
		Vy = tmpVy_array_clipped[i]
	 
		Vxmax = Vx + n
		Vxmin = Vx - n
		Vymax = Vy + n
		Vymin= Vy - n
 
		#-- Create new arrays where matching x and y values in B are within n of V. Else 0. -#
		tmpBx_array_copy = np.copy(tmpBx_array)
		tmpBx_array_copy[tmpBx_array_copy[:] > Vxmax] = 0
		tmpBx_array_copy[tmpBx_array_copy[:] < Vxmin] = 0
	 
		tmpBy_array_copy = np.copy(tmpBy_array)
		tmpBy_array_copy[tmpBy_array_copy[:] > Vymax] = 0
		tmpBy_array_copy[tmpBy_array_copy[:] < Vymin] = 0
	 
		#------  Find the rows of the matching x and y values in B --------------------------#
		Bx = np.array(np.where(tmpBx_array_copy[:] != 0))
		By = np.array(np.where(tmpBy_array_copy[:] != 0))
 
		#-- If there is an intersection of rows in B, save Vrow and Brow as a a match -------#
		if (np.intersect1d(Bx, By).size != 0):
			Vrow = i + offset
			Brow = np.intersect1d(Bx, By)[0]+offset 
			Vlist = np.append(Vlist, Vrow)
			Blist = np.append(Blist, Brow)
			print 'Matching Bx rows:', Bx + offset
			print 'Matching By rows:', By + offset
			print 'Object in row', Vrow, 'of V and', Brow, 'of B \n'
 
	 
	print "Vlist"
	print Vlist
	print "======="
	print "Blist"
	print Blist

	#convert lists from floats to integers
	#listVis=[]
	#listBlue=[]

	#def integer(listIndex):
	#	listIndex = int(listIndex)
	#	return listIndex

	#for i in range(0, len(Vlist)):
	#	listIndexVis = integer(Vlist[i])
	#	listVis.append(listIndexVis)
	
	#for i in range(0, len(Blist)):
	#	listIndexBlue = integer(Blist[i])
	#	listBlue.append(listIndexBlue)
	

	#=====================================================================
	#Start Get Data
	#=====================================================================

	#+++++++++++++++++++++++++++++++++++
	#Get Magnitudes
	#+++++++++++++++++++++++++++++++++++

	#array[ROW, COLUMN]
	#Mag col = 3

	#tmpV_array = np.genfromtxt("tmp115.dat", comments="#") #Visual
	#tmpB_array = np.genfromtxt("tmp118.dat", comments="#") #Blue 


	#visData= tmpV_array[listVis]
	#blueData = tmpB_array[listBlue]
	#magVis = visData[:,3]
	#magBlue = blueData[:,3]


	#isophotal magnitude is the 5th index
	magVis = tmpV_array[Vlist, 5]
	magBlue = tmpV_array[Blist, 5]

	print magVis
	print magBlue

	#+++++++++++++++++++++++++++++++++++
	#Get Luminosity
	#+++++++++++++++++++++++++++++++++++



	def luminosVis(mI, mZP, dist):
		#if isophotal magnitude, from sextractor, is mAB rather than mI
		#mAB = mI + mZP
		mAB = mI
		print "mAB", mAB
		flux = math.pow(10, -.4*(mAB + 48.6))
		#flux = 10**[-.4*(mAB + 48.6)]
		print "flux", flux
		lumin = 4*np.pi*(np.power(dist,2))*flux
		return lumin
		
	def luminosFilter(mI, mZP, dist):
		mAB = mI + mZP
		print "mAB", mAB
		flux = math.pow(10, -.4*(mAB + 48.6))
		#flux = 10**[-.4*(mAB + 48.6)]
		print "flux", flux
		lumin = 4*np.pi*(np.power(dist,2))*flux
		return lumin
	
	
	distPc = 908 #parsecs 
	distCm = (908)*(3.085e18) #cm
	distM = (908)*(3.085e16)

	mZP_vis = 24.12846
	mZP_blue = 23.792045

	mZP_vis_test= 22.34
	mZP_blue_test = 21.99

	luminosityVis = []
	luminosityBlue=[]


	#Visual Luminosity
	print "============Visual Luminosity==========="
	for i in range(0, len(magVis)):
		luminVis = luminosVis(magVis[i], mZP_vis_test, distCm)
		luminosityVis.append(luminVis)
	
	#Blue Luminosity
	print "=======Blue Luminosity============"
	for i in range(0, len(magBlue)):
		luminBlue = luminosFilter(magBlue[i], mZP_blue_test, distCm)
		luminosityBlue.append(luminBlue)
	

	
	print "luminosityVis", luminosityVis
	print "luminosityBlue", luminosityBlue
	
	V_B = magVis-magBlue
	
	return luminosityVis, luminosityBlue, V_B


	#plt.plot((magVis-magBlue), luminosityVis, 'x')
	#plt.title("Color Index")
	#plt.xlabel("V-B")
	#plt.ylabel("Luminosity")
	#plt.savefig("color_index.eps")
	#plt.show()




