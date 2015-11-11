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

f2 = np.arange(1,200)
l = np.arange(0,150)
sizeF2 = np.size(f2)
sizeL = np.size(l)
result_waist = np.ones((sizeF2, sizeL))
result_test = np.ones((sizeF2, sizeL))
result_NA = np.ones((sizeF2, sizeL))
result_product = np.ones((sizeF2, sizeL))
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

print "Give an index number for the to be created contour_plots"
index = input()


print Total_L, f1, IL_f_1064, IL_f_637


for k in range(np.size(f2)):
            #l=np.arange(0,L[i]+1-DM_IL-f1[j]-f2[k])
            for m in range(np.size(l)):
                result = testTelescope3( LamdaInfra, LamdaRed, SizeInfra, SizeRed, Total_L, Total_L-155, f1, f2[k], l[m], IL_f_637, IL_f_1064, index, 3)
                result_test = result[0]*1000
                if (result[0]*1000 > 12):
                    result_waist[k,m] = 12                    
                    result_product[k,m] = 1.2
                else:
                    result_waist[k,m] = result[0]*1000
                    if (result[1] < 0.1):
                        result_product[k,m] = result_NA[k,m]*result_waist[k,m]
                    else:
                        result_product[k,m] = 1.2
                if (result[1] > 0.1):
                    result_NA[k,m] = 0.1
                else: 
                    result_NA[k,m] = result[1]

#p.savetxt('test.out', result_test, fmt='%.1f', delimiter=' , ', newline='\n')
#np.savetxt('test2.out', result_waist, fmt='%.1f', delimiter=' , ', newline='\n')
        
Z = result_waist
im = pl.imshow(Z,cmap=pl.cm.RdBu)
pl.colorbar(im)
pl.title('Beam size of the infrared at the waist of the red beam\n' + str(LamdaRed) + 'nm; ' + str(LamdaInfra) +'nm L=' + str(Total_L) + 'mm f1=' + str(f1) + 'mm' )#$z=(1-x^2+y^3) e^{-(x^2+y^2)/2}$')
pl.xlabel('l(mm)')
pl.ylabel('f2(mm)')
pl.savefig('Contour_beamsize' + str(index) + '.png')
time.sleep(0.1)
pl.close('all') 

Z2 = result_NA
im = pl.imshow(Z2,cmap=pl.cm.RdBu)
pl.colorbar(im)
pl.title('Numerical aperture of the infrared at the waist of the red beam\n' + str(LamdaRed) + 'nm; ' + str(LamdaInfra) +'nm L=' + str(Total_L) + 'mm f1=' + str(f1) + 'mm' )#$z=(1-x^2+y^3) e^{-(x^2+y^2)/2}$')
pl.xlabel('l(mm)')
pl.ylabel('f2(mm)')
pl.savefig('Contour_NA' + str(index) + '.png')
time.sleep(0.1)
pl.close('all') 

Z3 = result_product
im = pl.imshow(Z3,cmap=pl.cm.RdBu)
pl.colorbar(im) 
pl.title('Optimal focal length and position for L2\n' + str(LamdaRed) + 'nm; ' + str(LamdaInfra) +'nm L=' + str(Total_L) + 'mm f1=' + str(f1) + 'mm' )#$z=(1-x^2+y^3) e^{-(x^2+y^2)/2}$')
pl.xlabel('l(mm)')
pl.ylabel('f2(mm)')
pl.savefig('Contour_NA_beamsize_combined' + str(index) + '.png')
time.sleep(0.1)
pl.close('all') 