'''
Created on 2 Apr 2013

@author: samoleary
'''
#/usr/bin/env python
 
import cv2
import cv2.cv as cv

HAAR_CASCADE_PATH = "/Users/samoleary/Documents/opencv/data/haarcascades/haarcascade_frontalface_alt_tree.xml"
SCALE = 2

def detect_faces(image):
    faces = []
    # create temp storage, used during object detection
    storage = cv.CreateMemStorage()
    # create a face detector from the cascade file in the resources directory
    cascade = cv.Load(HAAR_CASCADE_PATH)
    print '\nDetecting faces'
    detected = cv.HaarDetectObjects(image, cascade, storage, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (100, 100))
    if detected:
            for (x,y,w,h),n in detected:
                faces.append((x,y,w,h))
    return faces


if __name__ == '__main__':
    print '\nPython: Running pyDetect'
    image = cv.LoadImage('/Users/samoleary/Documents/Images/Python/InputImages/wholeGROUP.jpg', cv.CV_LOAD_IMAGE_COLOR)

    #convert to grayscale
    grayImage = cv.CreateImage((image.width,image.height), cv.IPL_DEPTH_8U, 1)
    cv.CvtColor(image, grayImage, cv.CV_BGR2GRAY)
    
    # equalize the small grayscale (to speed up face detection)
    smallImage = cv.CreateImage((cv.Round(grayImage.width / SCALE), cv.Round(image.height / SCALE)), cv.IPL_DEPTH_8U, 1)
    cv.Resize(grayImage, smallImage, cv.CV_INTER_LINEAR)
    
    # equalize the small grayscale
    equImage = cv.CreateImage((smallImage.width, smallImage.height), cv.IPL_DEPTH_8U, 1)
    cv.EqualizeHist(smallImage, equImage)
    
    faces = []
    faceRectCollection = []
    faces = detect_faces(equImage)
    total = (len(faces))
    print '\nDetected ' + `total` + ' faces'
    for (x,y,w,h) in faces:
        cv.Rectangle(image, (x*SCALE, y*SCALE), ((x+w)*SCALE, (y+h)*SCALE), 255, 6, cv.CV_AA, 0)
        cv.Rectangle(equImage, (x, y), ((x+w), (y+h)), 255, 6, cv.CV_AA, 0)
        faceRect = cv.GetSubRect(equImage, (x, y, w, h))
        faceRectCollection.append(faceRect)
    
    cv.SaveImage('/Users/samoleary/Documents/Images/Python/OutputImages/out.jpg', image)
    cv.SaveImage('/Users/samoleary/Documents/Images/Python/OutputImages/equOut.jpg', equImage)
    
    total = len(faceRectCollection)
    for total in range(0, total):
        cv.SaveImage('/Users/samoleary/Documents/Images/Python/OutputImages/' + `total` +'.jpg', faceRectCollection[total])


    
