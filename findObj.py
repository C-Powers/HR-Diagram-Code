import numpy as np

#tmp115.dat is c0 image, visual filter, 6s
#tmp116.dat is c0 image, blue filter, 6s
 
#---------------- Read in data ----------------------------------------------------------#
#exp time 6s
tmpV_array = np.genfromtxt("tmp115.dat", comments="#") #Visual
tmpB_array = np.genfromtxt("tmp118.dat", comments="#") #Blue 
 
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
Vlist = np.array([])
Blist = ([])
 
#Pixel value must be within n for a match
n = 5
#Offset is the row where values start in tmp.dat file after comments.
offset = 18
 
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




#=====================================================================
#Start Get Data
#=====================================================================






