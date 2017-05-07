# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 17:21:18 2015

@author: ferenc
"""

from os import listdir
from os.path import isfile, join
from subprocess import call
import numpy as np
import cv2

import os
import struct

EXT_MASK="_mask.png"
EXT_DEPTH="_depthcrop.png"
EXT_LOC="_loc.txt"


def format(value):
    return "%.9f" % value

def genPCD(rgbFile,maskFile,depthFile,locFile, scale =False):

    rgbImg = cv2.imread(rgbFile,1)
    maskImg = cv2.imread(maskFile,-1)
    depthImg = cv2.imread(depthFile,-1)
    padding = (rgbImg.shape[0] - maskImg.shape[0])/2
    if padding <> 0:
        print 'MASK AND RGB ARE NOT THE SAME SIZE. ABORTING: ',file[:-9]
        return
    
    loc = open(locFile,'r');
    clusterLocation = [int (e) for e in loc.read().split(',')]
    print clusterLocation
    CX=320
    CY=240
    FX=1/540.3422 
    FY=1/540.3422
    if scale:
        clusterLocation =[ l/2 for l in clusterLocation]
	print clusterLocation
        rgbImg = cv2.resize(rgbImg,None,fx=0.5,fy=0.5,interpolation = cv2.INTER_NEAREST)
        depthImg = cv2.resize(depthImg,None,fx=0.5,fy=0.5,interpolation = cv2.INTER_NEAREST)
        maskImg = cv2.resize(maskImg,None,fx=0.5,fy=0.5,interpolation = cv2.INTER_NEAREST)
        
    print CX,' ',CY,' ',FX
    print 'Padding is: ', padding
    print 'RGB is: ' ,rgbFile
    print 'Depth is: ',depthFile
    height, width ,depth= rgbImg.shape
    print "Height: ",height," Width:",width
    points = []
    for r in range(0,height):
        y = (r+clusterLocation[1]-CY)*FY
        for c in range(0,width):
            if maskImg[r,c] != 0:
                depthValue = depthImg[r,c]/1000.0
                if depthValue == 0.0:
                    continue
                x =(c+clusterLocation[0]-CX)*FX
                # create a 4 byte long string
                packed = struct.pack('I', rgbImg[r,c][2] << 16 | rgbImg[r,c][1] << 8 | rgbImg[r,c][0])
                # interpret it as a float
                colorValue = struct.unpack('f', packed)[0]
                tuple = (x*depthValue,y*depthValue,depthValue,colorValue)
                points.append(tuple)

    f = open(file[:-9]+'.pcd', 'w')
    f.write('# .PCD v0.7 - Point Cloud Data file format\n')
    f.write('VERSION 0.7\n')
    f.write('FIELDS x y z rgba\n')
    f.write('SIZE 4 4 4 4\n')
    f.write('TYPE F F F F\n')
    f.write('COUNT 1 1 1 1\n')
    f.write('WIDTH '+str(len(points))+'\n')
    f.write('HEIGHT 1\n')
    f.write('VIEWPOINT 0 0 0 1 0 0 0\n')
    f.write('POINTS '+str(len(points))+'\n')
    f.write('DATA ascii\n')
    for p in points:
        f.write(str(p[0])+' '+str(p[1])+' '+str(p[2])+' '+str(p[3])+'\n')



if __name__ == "__main__":

    currentPath = os.getcwd()
    allFiles = [ f for f in listdir(currentPath) if isfile(join(currentPath,f)) ]
    i=0
    scale = True
    if currentPath.endswith('_lr'):
	scale=False
    for file in allFiles:
        if file.endswith('_crop.png'):
            genPCD(file, file[:-9] + EXT_MASK, file[:-9]+EXT_DEPTH, file[:-9]+EXT_LOC,scale)
	    call(["pcl_convert_pcd_ascii_binary",file[:-9]+'.pcd',file[:-9]+'.pcd','2'])

