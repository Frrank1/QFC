#!/usr/bin/env python
import unittest
import numpy as np
import matplotlib
matplotlib.use('AGG')
import matplotlib.mlab as ml
import pylab as pl
import time

from GaussianBeam import *
from gaussianoptics import *

LamdaRed = 633
LamdaInfra = 1064
SizeRed = 2.12
SizeInfra = 1.01

l = np.arange(0,150)
sizeL = np.size(l)

result_waist = np.ones(sizeL)
result_test = np.ones(sizeL)
result_NA = np.ones(sizeL)
result_product = np.ones(sizeL)
result_waist.fill(0.56)
result_NA.fill(0.02)


IL_f_637_array = np.array([18.40, 11.00, 15.15, 18.24, 11.00])
IL_f_1064_array = np.array([18.57, 11.18, 15.44, 18.58, 11.165])
print "Choose an incoupling lense:\n[0]\tC280TMD-C\n[1]\tC220TMD-C\n[2]\tA260TM-C\n[3]\tA280TM-C\n[4]\tA220(no C-coating)\n[5]\tChoose properties manually"
choice = input()
if (choice == 5):
    print "Give the focal length of the incoupling lens for 637 nm in mm"
    IL_f_637 = raw_input()
    print "Give the focal length of the incoupling lens for 1064 nm in mm"
    IL_f_1064 = raw_input()
else:
    IL_f_637 = IL_f_637_array[choice]
    IL_f_1064 = IL_f_1064_array[choice]
print "The properties of the incoupling lense are: \nFocal length red = " + str(IL_f_637) + " mm\nFocal length infrared = " + str(IL_f_1064) + " mm"
print "Give the distance between the first lense and the incoupling lens in mm (standard 375 mm)"
Total_L = input() + 10
print "Give the focal length of the first lense in mm"
f1 = input()

print "Give the focal length of the second lense in mm"
f2 = input()

print "Give an index number for the to be created contour_plots"
index = input()


print Total_L, f1, IL_f_1064, IL_f_637



           
for m in range(np.size(l)):
                result = testTelescope3( LamdaInfra, LamdaRed, SizeInfra, SizeRed, Total_L, Total_L-155, f1, f2, l[m], IL_f_637, IL_f_1064, index, 3)
                result_test[m] = result[0]*1000
                if (result[0]*1000 > 12):
                    result_waist[m] = 12                    
                    result_product[m] = 1.2
                else:
                    result_waist[m] = result[0]*1000
                    if (result[1] < 0.1):
                        result_product[m] = result_NA[m]*result_waist[m]
                    else:
                        result_product[m] = 1.2
                if (result[1] > 0.1):
                    result_NA[m] = 0.1
                else: 
                    result_NA[m] = result[1]

minresult = min(result_test)
l_0 = [i for i,x in enumerate(result_test) if x == minresult] 


pl.plot(l,result_test)
pl.title("Optimal Extra Length  "  + str(l_0))#"z(waist red) = " + str(z_0[0]*0.01+np.size(zred)) +)
pl.xlabel('Extra length(mu m)')
pl.ylabel('Beam Size(mm)')
pl.axis([0 , sizeL, np.amin(result_test)*0.9, np.amax(result_test)*1.1])
pl.savefig('optimal_extra_l' + str(index) + '.png')