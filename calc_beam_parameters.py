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


#print "Give the distance between the incoupling lens and the waveguide in mm",
#distance_IL_WG = raw_input()
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
print "Give the extra distance in mm between the first and second lense without the sum of the two focal lengths (use 0 for a collimated beam)"
l = input()
print "Give an index number for the to be created png image"
index = input()


print Total_L, f1, IL_f_1064, IL_f_637

test = testTelescope2( 1064, 633, 1.01, 2.12, Total_L, Total_L-155, f1, f2, l, IL_f_637, IL_f_1064, index, 3)

