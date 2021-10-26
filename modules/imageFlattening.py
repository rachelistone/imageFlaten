import cv2 as cv
import os
import numpy as np
import imutils

def flattening(imgPath, destination):

    pi = 3.141592
    img = cv.imread(imgPath)
    # cv.imshow("source", img)
    
    width, height, c = img.shape
    print(width,height)
    x = int(width/2 + width/5)
    y = int(height/4)
    r = int(width/2.5)
    
    # add rect on the letters
    image = cv.rectangle(img, (90,20), (height-110, 70), (255, 255, 255), -1)
    color = (255, 255, 255)
    image = cv.circle(img, (x,y), r, color, -1)
    
    # can be removed by replacing the letters rectangle with area merged color pixels
    # lettersHeight = int(height/9)
    # cropedLetters = img[lettersHeight:width, 0:height]
    
    # cv.imshow("before", image)
    
    # only for the case of letters above as above
    # cv.imshow("croped", image)
    # cv.imwrite(f"picture analyse/{imgPath}", cropedLetters)
    
    firstRotate = imutils.rotate_bound(image, 90)
    width, height, _ = firstRotate.shape

    squareImg = np.zeros((width,width,3),np.uint8)
    squareImg[0:firstRotate.shape[0],0:firstRotate.shape[1]]=firstRotate
    startAngle = imutils.rotate(squareImg, -15)
    # cv.imshow("start rotation", squareImg)
    
    trapezHeight = 110
    SQRwidth, SQRheight, _ = squareImg.shape
    centerX = round(SQRwidth/2)
    topY = round(SQRheight- trapezHeight)
    topXstart = round(centerX - 60)
    topXend = round(centerX + 60)
    downXstart = round(centerX - 100)
    downXend = round(centerX + 100)
    reqXstart = topXstart - round((topXstart - downXstart)/2)
    reqXend = topXend + round((downXend - topXend)/2)
    reqXSize = reqXend - reqXstart
    
    # loop over the rotation angles
    for angle in np.arange(0, 220, 15):
        rotated = imutils.rotate(startAngle, angle)
        scaledSlices = np.zeros((trapezHeight,reqXSize,3),np.uint8)
        for y in range(topY, SQRheight,2):
            currentXStart = round(topXstart-(y-topY)/2)
            halfX = centerX-currentXStart
            currentXEnd = centerX + halfX
            # cv.rectangle(rotated, (currentXStart,y), (currentXEnd,y+2),(0,0,0))
            # cv.imshow("Rotated", rotated)
            # cv.waitKey(0)
            sliced = rotated[y:y+2,currentXStart:currentXEnd]
            scaled = cv.resize(sliced, (reqXSize,2), interpolation = cv.INTER_AREA)
            # cv.imshow("scaled", scaled)
            # cv.waitKey(0)
            scaledSlices[y-topY:y-topY+2,0:reqXSize]= scaled
            # cv.imshow("scaledSlices", scaledSlices)
            # cv.waitKey(0)
            
        if angle != 0: 
            currentOutWidth += reqXSize
            temp = np.zeros((trapezHeight,currentOutWidth, 3),np.uint8)
            temp[0:trapezHeight,0:reqXSize]= scaledSlices
            temp[0:trapezHeight,reqXSize:currentOutWidth]=outputTrack
            outputTrack = temp
        else:
            outputTrack = np.zeros((trapezHeight, reqXSize, 3),np.uint8)
            outputTrack[0:trapezHeight,0:reqXSize]= scaledSlices
            currentOutWidth = reqXSize
            
        #cv.imshow("outputTrack", outputTrack)
        #cv.waitKey(0)
        
    filename = os.path.splitext(os.path.basename(imgPath))[0]    
    cv.imwrite(f"{destination}/{filename}.jpg",outputTrack)
    return trapezHeight

    
    