import cv2 as cv
import numpy as np
import pytesseract as pyt

def scan_Image(img)

    #to white text on black background
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    gray = cv.bitwise_not(gray)
    ret,thresh = cv.threshold(gray,0,255,cv.THRESH_BINARY)

    #text = pyt.image_to_string(img)
    #print(text)
    #cv.imshow("Thresh",thresh)
    #cv.waitKey(1000)
    #Find the rect that bounds the text
    coords = np.column_stack(np.where(thresh>0))
    rect = cv.minAreaRect(coords)
    angle = cv.minAreaRect(coords)[-1]
    #Determine angle of inclinatio
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    print ("Angle is : (:.3f)".format(angle)+"degrees")

    #Get the affine transform
    (h,w) = img.shape[:2]
    center = (w//2,h//2)
    M = cv.getRotationMatrix2D(center,angle,1.0)

    rotated = cv.warpAffine(img,M,(w,h),flags=cv.INTER_CUBIC,borderMode=cv.BORDER_REPLICATE)
    #cv.imshow("rot",rotated)
    #cv.waitKey(0)
    #cv.destroyAllWindows()
    text = pyt.image_to_string(rotated)
    return text
