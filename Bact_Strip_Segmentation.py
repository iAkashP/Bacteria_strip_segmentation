# @Author: Akash Pathak <akash>
# @Date:   2018-08-03T22:22:25+05:30
# @Last modified by:   akash
# @Last modified time: 2018-08-05T01:59:43+05:30


######################################################################
# DESCRIPTION: 1. Place all images to be automatically segmented in folder "Test_Images".
#              2. Run Me
#              3. Get Segmented images in folder "Results"
######################################################################


import cv2 as cv
import os
import numpy as np
cwd = os.getcwd()
der=cwd+"/Test_Images/"
directories=[]
files=[]
###################################################################
########## GET DIRECTORY LISTING FOR FILES ########################
for x in os.listdir(der):

    if os.path.isfile(x):
        print ('f-', x)
        files.append(x)

    elif os.path.isdir(x):
        print ('d-', x)
        directories.append(x)

    elif os.path.islink(x):
        print ('l-', x)

    else:
        print ('---', x)
        files.append(x)
#### Work on All FILES in FILES[] ####################################
for ty in range(0,len(files)):

    filename = der+files[ty]
   # ft=filename
    orig=cv.imread(filename)    #BGR image
    img=cv.imread(filename,0)   #Grayscale image
    # cv.imwrite(cwd+"/Results/testpattern.jpg",img)

   # Applying the bilateral filter
    img = cv.bilateralFilter(img, 11, 17, 17)

    #OTSU Threshold
    ret,thresh = cv.threshold(img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    cv.imwrite(cwd+"/Results/testpattern_thresholded.jpg",thresh)


    # MASK GENERATION
    kernel=(8,8)
    kernel = np.ones(kernel, np.uint8)
    #Open to erode small patches, remove the scratches
    thresh2 = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel)
    #Close little holes, close filter.
    thresh2 = cv.morphologyEx(thresh2, cv.MORPH_CLOSE,kernel, iterations=20)
    cv.imwrite(cwd+"/Results/testpattern_threshold_pure_filled.jpg",thresh2)


    #BOUNDING RECTANGLE
    image, contours, hierarchy = cv.findContours(thresh2, cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    # convert image back to BGR
    color_img = cv.cvtColor(thresh2, cv.COLOR_GRAY2BGR)
    # draw contours onto image
    cnt=contours[0]
    x,y,w,h = cv.boundingRect(cnt)
    # print ("the Bounding Box Corners:",x,y)

    # Perfect rect Corners
    ytop=0 # Y top
    ybot=0 # Y bottom

	#if strip is bent, check avg value is 255 or not
    for i in range(y,y+h):
        avg=np.mean(thresh2[i,x:x+w])
        if avg==255:
            ytop=i
            break;
    for i in range(y+h,y,-1):
        avg=np.mean(thresh2[i,x:x+w])
        if avg==255:
            ybot=i
            break;
    # print (ytop,ybot)
    # height=ybot-ytop


    #Extract image, CROP
    crop_img = orig[ytop:ybot,x:x+w]

    crop_name=files[ty][0:len(files[ty])-4]
    cv.imwrite(cwd+"/Results/"+crop_name+"_cropped.png",crop_img)

    print ("Working on Image ",files[ty])
    print ("Progress:"+str(ty+1)+"/"+str(len(files)))
print ("OPERATION COMPLETED.")
