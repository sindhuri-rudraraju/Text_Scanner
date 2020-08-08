from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .form import *
from .models import Scanner
import cv2 as cv
import numpy as np
import pytesseract as pyt
from matplotlib import image
import os
import cv2 as cv
import numpy as np
import pytesseract as pyt
#from myocr import *

  
# Create your views here. 
def take_image(request):     
    if request.method == 'POST': 
        if '_getscans' in request.POST:
            return redirect('All_images')
        if '_delscans' in request.POST:
            return redirect('deleted')
        form = ImageForm(request.POST, request.FILES) 
  
        if form.is_valid(): 
            form.save()
            obj=Scanner.objects.last()
            path = os.getcwd()
            parent = os.path.join(path, os.pardir) 
            print(parent)
            parent=parent.replace("..","")
            print(parent)
            #im=obj.input_Image.url.replace("/", "\\")
            img = parent + obj.input_Image.url
            print(img)

            text = scan_Image(img)
            obj.image_Text=text
            obj.save()
            return redirect('display') 
    else: 
        form = ImageForm() 
    return render(request, 'upload.html', {'form' : form})
    

def display_images(request): 
  
    if request.method == 'GET': 
  
        # getting all the objects of hotel. 
        Images = Scanner.objects.all()  
        return render(request, 'display.html', {'all_images' : Images})
def display_image(request):
    if request.method == 'GET': 
  
        # getting all the objects of hotel. 
        Image = Scanner.objects.last()  
        return render(request, 'display_single.html', {'image' : Image})
def delete_images(request):
    if request.method == 'GET': 
  
        # getting all the objects of hotel. 
        Image = Scanner.objects.all().delete()  
        return render(request, 'delete.html')
  
def success(request): 
    return HttpResponse('successfully uploaded') 


# Create your views here.
def scan_Image(img):
    print(img)
    img = cv.imread(img)
    print(img)
    #img = np.float32(img)
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
    print(text)
    return text
