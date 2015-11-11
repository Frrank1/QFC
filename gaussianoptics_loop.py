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
fInfra = 18.58
fRed = 18.24

nr = 1
index = 8

maxL = 385
DM_IL = 155
L = np.arange(maxL,maxL+1)
#f1 = np.arange(50,51)
f1 = [10,12,15,20,25,30,35,40,50,60,75,85,100,125,150,175,200]
f2 = np.arange(1,200)
l = np.arange(0,150)
sizeF2 = np.size(f2)
sizeL = np.size(l)
result_waist = np.ones((sizeF2, sizeL))
result_NA = np.ones((sizeF2, sizeL))
result_product = np.ones((sizeF2, sizeL))
result_waist.fill(0.56)
result_NA.fill(0.02)
#L= np.arange(DM_IL,maxL+1)
#print L

X,Y = pl.meshgrid(f2, l)


for i in range(np.size(L)):
    DM = L[i] - 155
    #f1 = np.arange(5,min(101,L[i]),5)
    #f1 = np.arange(50,51)
    for j in range(np.size(f1)):
        #f2 = np.arange(5,L[i]-DM_IL-f1[j],5)
        index = j
        for k in range(np.size(f2)):
            #l=np.arange(0,L[i]+1-DM_IL-f1[j]-f2[k])
            for m in range(np.size(l)):
                result = testTelescope3( LamdaInfra, LamdaRed, SizeInfra, SizeRed, L[i], DM, f1[j], f2[k], l[m], fRed, fInfra, index, nr)
                if (result[0]*1000 > 30):
                    result_waist[k,m] = 30
                    if (result[1] > 0.1):
                        result_product[k,m] = result_NA[k,m]*result_waist[k,m]
                    else:
                        result_product[k,m] = 3
                else:
                    result_waist[k,m] = result[0]*1000
                    result_product[k,m] = 3
                if (result[1] > 0.1):
                    result_NA[k,m] = 0.1
                else: 
                    result_NA[k,m] = result[1]
                    # if (k == 150):
                    #     if (m == 36):
                    #         print result[1], LamdaInfra, LamdaRed, SizeInfra, SizeRed, L[i], DM, f1[j], f2[k], l[m], fRed, fInfra, index, nr

                # if (result_NA[k,m]*result_waist[k,m] > 30):
                #     result_product[k,m] = 30
                # else: result_product[k,m] = result_NA[k,m]*result_waist[k,m]

                #result_NA[k,m] = result[1]

                #result_NA[k,m] = result[1]
                # if (f2[k] < (L[i]-DM_IL-f1[j])):
                #     #print f2[k]
                #     if (l[m] < (L[i]+1-DM_IL-f1[j]-f2[k])):
                #         #print f2[k], l[m]
                #         result = testTelescope3( LamdaInfra, LamdaRed, SizeInfra, SizeRed, L[i], DM, f1[j], f2[k], l[m], fRed, fInfra, index, nr)
                #         result_waist[k,m] = result[0]
                #         result_NA[k,m] = result[1]
        
        Z = result_waist
        im = pl.imshow(Z,cmap=pl.cm.RdBu)
        pl.colorbar(im)
        pl.title('Optimal focal length and position for L2\n' + str(LamdaRed) + 'nm; ' + str(LamdaInfra) +'nm L=' + str(L[0]) + 'mm f1=' + str(f1[j]) + 'mm' )#$z=(1-x^2+y^3) e^{-(x^2+y^2)/2}$')
        pl.xlabel('l(mm)')
        pl.ylabel('f2(mm)')
        pl.savefig('Contour_beamsize' + str(index) + '.png')
        time.sleep(0.1)
        pl.close('all') 

        Z2 = result_NA
        im = pl.imshow(Z2,cmap=pl.cm.RdBu)
        pl.colorbar(im)
        pl.title('Optimal focal length and position for L2\n' + str(LamdaRed) + 'nm; ' + str(LamdaInfra) +'nm L=' + str(L[0]) + 'mm f1=' + str(f1[j]) + 'mm' )#$z=(1-x^2+y^3) e^{-(x^2+y^2)/2}$')
        pl.xlabel('l(mm)')
        pl.ylabel('f2(mm)')
        pl.savefig('Contour_NA' + str(index) + '.png')
        time.sleep(0.1)
        pl.close('all') 

        Z3 = result_product
        im = pl.imshow(Z3,cmap=pl.cm.RdBu)
        pl.colorbar(im) 
        pl.title('Optimal focal length and position for L2\n' + str(LamdaRed) + 'nm; ' + str(LamdaInfra) +'nm L=' + str(L[0]) + 'mm f1=' + str(f1[j]) + 'mm' )#$z=(1-x^2+y^3) e^{-(x^2+y^2)/2}$')
        pl.xlabel('l(mm)')
        pl.ylabel('f2(mm)')
        pl.savefig('Contour_NA_beamsize_combined' + str(index) + '.png')
        time.sleep(0.1)
        pl.close('all') 

#print result_waist[3,5], result_NA[10,4] 
#print f2
#print l
#print result_waist

# X,Y = pl.meshgrid(f2, l)
# Z = result_waist
# im = pl.imshow(Z,cmap=pl.cm.RdBu)#,extent=(0,sizeL, 200, 50)) # drawing the function
# # adding the Contour lines with labels
# #cset = pl.contour(Z,np.arange(-1,1.5,0.2),linewidths=2,cmap=pl.cm.Set2)
# #pl.clabel(cset,inline=True,fmt='%1.1f',fontsize=10)
# pl.colorbar(im) # adding the colobar on the right
# # latex fashion title
# #pl.axis([0,sizeL, 0, sizeF2*5])
# pl.title('Optimal focal length and position for L2\n' + str(LamdaRed) + 'nm; ' + str(LamdaInfra) +'nm L=' + str(L[0]) + 'mm f1=' + str(f1[0]) + 'mm' )#$z=(1-x^2+y^3) e^{-(x^2+y^2)/2}$')
# pl.xlabel('l(mm)')
# pl.ylabel('f2(mm)')
# #pl.show()
# pl.savefig('Contour_beamsize' + str(index) + '.png')
# time.sleep(0.1)
# pl.close('all') 

# Z2 = result_NA
# im = pl.imshow(Z2,cmap=pl.cm.RdBu)#,extent=(0,sizeL, 200, 50)) # drawing the function
# # adding the Contour lines with labels
# #cset = pl.contour(Z2,np.arange(0.1,0.3,0.1),linewidths=2,cmap=pl.cm.Set2)#, extent=(sizeL, 0, 50, 200))
# #pl.clabel(cset,inline=True,fmt='%1.1f',fontsize=10)
# pl.colorbar(im) # adding the colobar on the right
# # latex fashion title
# #pl.axis([0,sizeL, 0, sizeF2*5])
# pl.title('Optimal focal length and position for L2\n' + str(LamdaRed) + 'nm; ' + str(LamdaInfra) +'nm L=' + str(L[0]) + 'mm f1=' + str(f1[0]) + 'mm' )#$z=(1-x^2+y^3) e^{-(x^2+y^2)/2}$')
# pl.xlabel('l(mm)')
# pl.ylabel('f2(mm)')
# #pl.show()
# pl.savefig('Contour_NA' + str(index) + '.png')
# time.sleep(0.1)


# pl.close('all') 

# Z3 = result_product
# im = pl.imshow(Z3,cmap=pl.cm.RdBu)#,extent=(0,sizeL, 200, 50)) # drawing the function
# # adding the Contour lines with labels
# #cset = pl.contour(Z3,np.arange(0.1,0.3,0.1),linewidths=2,cmap=pl.cm.Set2)#, extent=(sizeL, 0, 50, 200))
# #pl.clabel(cset,inline=True,fmt='%1.1f',fontsize=10)
# pl.colorbar(im) # adding the colobar on the right
# # latex fashion title
# #pl.axis([0,sizeL, 0, sizeF2*5])
# pl.title('Optimal focal length and position for L2\n' + str(LamdaRed) + 'nm; ' + str(LamdaInfra) +'nm L=' + str(L[0]) + 'mm f1=' + str(f1[0]) + 'mm' )#$z=(1-x^2+y^3) e^{-(x^2+y^2)/2}$')
# pl.xlabel('l(mm)')
# pl.ylabel('f2(mm)')
# #pl.show()
# pl.savefig('Contour_NA_beamsize_combined' + str(index) + '.png')
# time.sleep(0.1)


# pl.close('all') 

#pylab.imshow(SLP,aspect='auto',origin='lower',extent=(ff.min(),ff.max(),AA.min(),AA.max()))