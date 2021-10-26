from modules.imageFlattening import flattening
import os
import numpy as np
import cv2 as cv

def main():

    flatenSource = 'frames'
    flatenDestination = 'slices'
    numOfFrames = len([name for name in os.listdir(flatenSource)])
    
    def absoluteFilePaths(directory):
        for dirpath,_,filenames in os.walk(directory):
            for f in filenames:
                yield os.path.abspath(os.path.join(dirpath, f))
    
    for i in absoluteFilePaths(flatenSource):
        flattening(i, flatenDestination)
    
    slices = absoluteFilePaths(flatenDestination)
    oneslice = cv.imread(next(slices))
    w, h, _ = oneslice.shape
    outputTrack = np.zeros((w, h*numOfFrames, 3),np.uint8)
    outputTrack[h*numOfFrames-h:h*numOfFrames,:] = oneslice[:,:]
    
    for i in range(numOfFrames-1):
        oneslice = cv.imread(next(slices))
        outputTrack[h*numOfFrames-(i+2)*h:h*numOfFrames-(i+1)*h,:] = oneslice
        
    cv.imwrite(f"{os.getcwd()}/oneImage.jpg",outputTrack)
main()