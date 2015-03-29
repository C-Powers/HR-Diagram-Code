#calculate the ZP mag of calibration star SA 104 461

import numpy as np

def zero_point(cps, m_AB, S_err,):
	
	m_I =-2.5*np.log10(cps)
	m_ZP = m_AB - m_I
	
	cpsError = np.sqrt(cps)

	mI_error = -2.5/cpsError

	
	
	return m_ZP, cpsError
	
	
# equation: m_AB = M_I + m_ZP
#note that m_AB depends on the filter mag, 


# x = [B 3s, B 10s, V 3s, V 10s]

S = [150495, 490952, 310827, 1.044e6]
S_err = [383.168, 700.68, 557.519, 1021.99]
m_AB = [ 10.181, 10.181, 9.705, 9.705]
time = [3.0, 10.0, 3.0, 10.0]



m_ZP_arr = []
cps_error=[]

for i in range(0, len(S)):
	cps = S[i]/time[i]
	m_ZP,cpsError = zero_point(cps, m_AB[i], S_err[i])
	m_ZP_arr.append(m_ZP)
	cps_error.append(cpsError)
	
print "mZP", m_ZP_arr
print "error cps", cps_error




#=======calc mZP=============
mZP_blue = (m_ZP_arr[0] + m_ZP_arr[1])/2

print "mZP_blue", mZP_blue

mZP_vis = (m_ZP_arr[2] + m_ZP_arr[3])/2

print "mZP_vis", mZP_vis



