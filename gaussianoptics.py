#!/usr/bin/env python
import unittest
import numpy as np
import matplotlib
matplotlib.use('AGG')
import matplotlib.mlab as ml
import pylab as pl
import time 

from GaussianBeam import *

def add_lens(z, f, diam, L, lbl, size):
    ww, tw, rad = diam / 3.0, diam/0.25, diam / size
    pl.plot([z, z],    [-rad, rad],                'k', linewidth=2)
    pl.plot([z, z+tw], [-rad, -rad+np.sign(f)*ww], 'k', linewidth=2)
    pl.plot([z, z-tw], [-rad, -rad+np.sign(f)*ww], 'k', linewidth=2)
    pl.plot([z, z+tw], [ rad,  rad-np.sign(f)*ww], 'k', linewidth=2)
    pl.plot([z, z-tw], [ rad,  rad-np.sign(f)*ww], 'k', linewidth=2)
    #pl.plot([z+f, z+f], [-ww,ww], 'k', linewidth=2)
    #pl.plot([z-f, z-f], [-ww,ww], 'k', linewidth=2)
    pl.text(z - L*0.01,rad+0.8, lbl, fontsize=10)
    if (f == float("inf")):     pl.text(z-L*0.01,rad+0.5, 'mirror', fontsize=7)  
    else:           pl.text(z-L*0.01,rad+0.5, 'f='+str(int(f))+' mm', fontsize=7)

def testTelescope2( lamda, lamdared, d, dred, L, DM, f1, f2, l, fred, finfra, index, nr):
    # import matplotlib
        # matplotlib.use('AGG')
        # import matplotlib.mlab as ml
        # import pylab as pl
        # import time        
    w0 = d/2
    w0_red = dred/2
    k = 1000000*2*np.pi/lamda
    kred = 1000000*2*np.pi/lamdared
    gb = GaussianBeam(w0, k)
    gbred = GaussianBeam(w0_red, kred)
    lens = ThinLens(f1, 10)
    gb2 = lens*gb
    #self.assertAlmostEqual(gb2._z0, gb._z0 + 2*151.0)
    lens2 = ThinLens(f2, f1+f2+l+10)
    gb3 = lens2*gb2
    #self.assertAlmostEqual(gb3._z0, gb2._z0 + 2*300.0)
    #self.assertAlmostEqual(gb._w0, gb3._w0/2.0)
    lens3 = ThinLens(finfra, L)
    lensred = ThinLens(fred,L)
    gb4 = lens3*gb3
    gbred2 = lensred*gbred
    z = np.arange(0, 10)
    z2 = np.arange(10, f1+f2+l+10)
    z3 = np.arange(f1+f2+l+10, L)
    z4 = np.arange(L, L*1.2,0.01)
    zred = np.arange(0,L,)
    zred2 = np.arange(L,L*1.2,0.01)

    
    zl = np.array([10, f1+f2+l+10, DM, L])
    ffinfrared = np.array([f1, f2, float("inf"), finfra])

    names = ["L1", "L2", "DM", "IL"]
    for i in range(np.size(zl)): add_lens(zl[i], ffinfrared[i], w0_red*1.1, L, names[i], 0.4)#"L"+str(i))

    for i in range(nr+1):
        factor = i*1.0/nr
        pl.plot(z, gb.w(z, k)*factor, 'g', z2, gb2.w(z2, k)*factor, 'g',  z3, gb3.w(z3, k)*factor, 'g',  z4, gb4.w(z4, k)*factor, 'g')
        pl.plot(z, -gb.w(z, k)*factor, 'g', z2, -gb2.w(z2, k)*factor, 'g',  z3, -gb3.w(z3, k)*factor, 'g',  z4, -gb4.w(z4, k)*factor, 'g')
        pl.plot(zred, gbred.w(zred, kred)*factor, 'r', zred2, gbred2.w(zred2, kred)*factor, 'r')
        pl.plot(zred, -gbred.w(zred, kred)*factor, 'r', zred2, -gbred2.w(zred2, kred)*factor, 'r')

    # pl.plot(z, gb.w(z, k), 'g', z2, gb2.w(z2, k), 'g',  z3, gb3.w(z3, k), 'g',  z4, gb4.w(z4, k), 'g')
    # pl.plot(z, -gb.w(z, k), 'g', z2, -gb2.w(z2, k), 'g',  z3, -gb3.w(z3, k), 'g',  z4, -gb4.w(z4, k), 'g')
    # pl.plot(zred, gbred.w(zred, kred), 'r', zred2, gbred2.w(zred2, kred), 'r')
    # pl.plot(zred, -gbred.w(zred, kred), 'r', zred2, -gbred2.w(zred2, kred), 'r')
    #pl.grid()
    w_0 = min(gb4.w(z4,k))
    z_0 = [i for i,x in enumerate(gb4.w(z4,k)) if x == w_0] 
    w_0red = min(gbred2.w(zred2,kred))
    z_0red = [i for i,x in enumerate(gbred2.w(zred2,kred)) if x == w_0red] 

    if (z_0[0]*0.01+np.size(zred) < z_0red[0]*0.01+np.size(zred)):
        NA = (gb4.w(np.size(zred),k) + gb4.w(z_0red[0]*0.01+np.size(zred),k))/(z_0red[0]*0.01)
    else:
        NA = (gb4.w(np.size(zred),k) - gb4.w(z_0red[0]*0.01+np.size(zred),k))/(z_0red[0]*0.01)
    if (z_0[0] == 0):
        NA = 1000
    else:
        NA = gb4.w(np.size(zred),k)/(z_0[0]*0.01)


    pl.title("$w_0^{red}$ = " + str(w_0red*2000) + "$\mu m \quad z_0^{red}$ = " + str(z_0red[0]*0.01+np.size(zred)) +"$\ z_0$ = " + str(z_0[0]*0.01+np.size(zred)) + "\nbeamsize($z_0^{red}$) = " + str(gb4.w(z_0red[0]*0.01+np.size(zred),k)*2000) + "$\mu m$ NA = " + str(NA) )#"z(waist red) = " + str(z_0[0]*0.01+np.size(zred)) +)
    pl.xlabel('z')
    pl.ylabel('w')
    pl.axis([0 , L+finfra*1.5, -w0_red*4, w0_red*4])
    

    
    pl.savefig('testTelescope' + str(index) + '.png')

    add_lens(z_0red[0]*0.01+np.size(zred), float("inf"), gb4.w(z_0red[0]*0.01+np.size(zred),k), L,  "", 1.0)

    pl.axis([L+finfra*0.8, L+finfra*1.3, -0.2, 0.2])
    pl.savefig('testTelescope_zoom' + str(index) + '.png')
    time.sleep(0.1)
    pl.close('all') 
    #result = [2*w_0,z_0[0], 2*w_0red,z_0red[0], 2*gb4.w(z_0red[0],k), abs(z_0[0] - z_0red[0]), 2*gb4.w(z_0red[0]*0.01+np.size(zred),k)]
    result = [abs(2*gb4.w(z_0red[0]*0.01+np.size(zred),k) - 2*w_0red), (gb4.w(np.size(zred),k) - gb4.w(z_0red[0]*0.01+np.size(zred),k))/(z_0red[0]*0.01), w0_red/(z_0red[0]*0.01) ]
    #result = gb4.w
    return result



def testTelescope3( lamda, lamdared, d, dred, L, DM, f1, f2, l, fred, finfra, index, nr):      
    w0 = d/2
    w0_red = dred/2
    k = 1000000*2*np.pi/lamda
    kred = 1000000*2*np.pi/lamdared
    gb = GaussianBeam(w0, k)
    gbred = GaussianBeam(w0_red, kred)

    lens = ThinLens(f1, 10)
    gb2 = lens*gb

    lens2 = ThinLens(f2, f1+f2+l+10)
    gb3 = lens2*gb2

    lens3 = ThinLens(finfra, L)
    lensred = ThinLens(fred,L)
    gb4 = lens3*gb3
    gbred2 = lensred*gbred

    z = np.arange(0, 10)
    z2 = np.arange(10, f1+f2+l + 10)
    z3 = np.arange(f1+f2+l+10, L)
    z4 = np.arange(L, L*1.2,0.01)
    zred = np.arange(0,L,)
    zred2 = np.arange(L,L*1.2,0.01)

    w_0 = min(gb4.w(z4,k))
    z_0 = [i for i,x in enumerate(gb4.w(z4,k)) if x == w_0] 
    w_0red = min(gbred2.w(zred2,kred))
    z_0red = [i for i,x in enumerate(gbred2.w(zred2,kred)) if x == w_0red] 

    if (z_0[0] == 0):
        NA = 2
    else:
        if (z_0[0]*0.01+np.size(zred) < z_0red[0]*0.01+np.size(zred)):
            NA = (gb4.w(np.size(zred),k) + gb4.w(z_0red[0]*0.01+np.size(zred),k))/(z_0red[0]*0.01)
        else:
            NA = (gb4.w(np.size(zred),k) - gb4.w(z_0red[0]*0.01+np.size(zred),k))/(z_0red[0]*0.01)
        NA = gb4.w(np.size(zred),k)/(z_0[0]*0.01)

    result = [2*gb4.w(z_0red[0]*0.01+np.size(zred),k) , NA]
    return result

test = testTelescope2( 1064, 633, 1.01, 2.12, 385, 280, 100, 175, 30, 18.24, 18.58, 05, 3)
#print test

# for i in range(50):
#     test = testTelescope3( 1064, 633, 1.01, 2.12, 385, 280, 25, 50 + i, 100, 18.24, 18.58, 2, 1)
#     print test[1], i+50


