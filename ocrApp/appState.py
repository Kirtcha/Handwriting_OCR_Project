"""Ovde importujemo worker-a i loader-a i odavde onda importujemo to gde treba
   To radim da bi imao "globalnog" worker-a i loader-a"""
from imageLoader import imageLoader
from imageWork import imageWork
loader = imageLoader()
worker = imageWork()
import os
import time

#dodajemo deo za selektovanje kontura 
dragging=False
dragStart = None
dragEnd = None

#dodajem display state flagove za menjaje stvari koje se prikazuju
displayState={"image":True,
              "thresh":False,
              "contours":False,
              "name":True,
              "size":False,
              "select":False,
              "recognize":False,
              "confidence":False}
#rad sa kursorom --> |
cursorTime = time.time()
cursorFlag = True

#ovde cuvamo ime slova
letterName=""

#Main menu flagovi,koristimo za menjanje prozora
runState={"menu":True,
          "letter": False,
          "data":False,
          "recognize":False}
#koristimo za cuvanje slika sortiranih listi training data
sortedByName = None
sortedBySize = None


#ovde cuvamo selektovanu sliku za recognize
selectedImage=None
selectedImageThresh=None
ThreshCopyImg=None
selectedImagePath=None



results=[]
confidence=[]
