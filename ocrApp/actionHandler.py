import appState
import os 
from imageSaver import saveLetter
from uiComponents import buttonsLE,buttonStorageLE,slidersLE,buttonsDT,buttonsRL,buttonStorageRL
import tkinter as tk
from tkinter import filedialog
import cv2
from render import refreshDataInfo
from render import putTextPIL


import torch
import cv2

from ocrApp.imageLoader import imageLoader
from ocrApp.imageWork import imageWork
from neuralNetwork.models.model_1 import model_1

#AKCIJE ZA LETTER EXTRACTOR
def buttonActionHandlerLE(button):

    #thresh slika
    if button.action=="thresh":
        appState.displayState["image"]= not appState.displayState["image"]
        appState.displayState["thresh"]= not appState.displayState["thresh"]
    
    #prikaz kontura
    if button.action=="contours":
        appState.displayState["contours"]= not appState.displayState["contours"]

    #next dugme
    if button.action=="next":
        if appState.loader.imageIndex<len(os.listdir("Images/notUsed"))-1:
            appState.loader.imageIndex+=1
            appState.worker.contourData.clear()
        

    #back dugme
    if button.action=="back":
        if appState.loader.imageIndex>0:
            appState.loader.imageIndex-=1
            appState.worker.contourData.clear()
    
    #reset dugme
    if button.action=="reset":
        appState.worker.blurKernel=5
        appState.worker.sigma=0
        appState.worker.blockSize=21
        appState.worker.c=5
        resetSliders(sliders=slidersLE)
    
 
    #move dugme
    if button.action=="move":
        appState.loader.moveImageToUsed("Images/notUsed")
        appState.worker.contourData.clear()
        if appState.loader.imageIndex > 0:
            appState.loader.imageIndex -= 1

    #save dugme
    if button.action == "save" and len(appState.worker.contourData)!=0:
        for button in buttonsLE[:]:
            if button.action == "save":
                buttonStorageLE.append(button)
                buttonsLE.remove(button)
        for button in buttonStorageLE[:]:
            if button.action in ("yes", "no", "input"):
                buttonsLE.append(button)
                buttonStorageLE.remove(button)

    #yes dugme
    if button.action=="yes" and appState.letterName != "":
        for button in buttonsLE[:]:
            if button.action in ("yes", "no", "input"):
                buttonStorageLE.append(button)
                buttonsLE.remove(button)
        for button in buttonStorageLE[:]:
            if button.action == "save":
                buttonsLE.append(button)
                buttonStorageLE.remove(button)
        if appState.letterName != "":
            saveLetter(appState.worker.contourData, appState.letterName)
            refreshDataInfo()
        appState.letterName = ""

    #no dugme
    if button.action=="no":
        for button in buttonsLE[:]:
            if button.action in ("yes", "no", "input"):
                buttonStorageLE.append(button)
                buttonsLE.remove(button)
        for button in buttonStorageLE[:]:
            if button.action == "save":
                buttonsLE.append(button)
                buttonStorageLE.remove(button)
        appState.letterName = ""

    if button.action=="menu":
        appState.displayState={"image":True,
                                "thresh":False,
                                "contours":False,
                                "name":True,
                                "size":False,
                                "select":False,
                                "recognize":False,
                                "confidence":False}
        resetButtons(buttons=buttonsLE)
        appState.runState["menu"]=True
        appState.runState["letter"]=False


def sliderActionHandlerLE(slider):
    appState.worker.contourData.clear()

    if slider.action=="blur":
        appState.worker.blurKernel=int(30*slider.percentage/100)+1
        if appState.worker.blurKernel % 2 == 0:
            appState.worker.blurKernel += 1

    if slider.action=="sigma":
        appState.worker.sigma = int(10*slider.percentage/100)
    
    if slider.action=="block":
        appState.worker.blockSize = int(48*slider.percentage/100)+3
        if appState.worker.blockSize % 2 == 0:
            appState.worker.blockSize += 1
    
    if slider.action=="c":
        appState.worker.c = int(40*slider.percentage/100)-20


#pomocna funkcija koju koristim za reset UI dela slidera
def resetSliders(sliders):
    appState.worker.contourData.clear()
    for slider in sliders:
        if slider.action=="blur":
            slider.percentage = int(100*(appState.worker.blurKernel-1)/30)
        if slider.action=="sigma":
            slider.percentage = int(100*appState.worker.sigma/10)
        if slider.action=="block":
            slider.percentage = int(100*(appState.worker.blockSize-3)/48)
        if slider.action=="c":
            slider.percentage = int(100*(appState.worker.c+20)/40)


#selekcija kontura
def selectContours(dragStart,dragEnd):
    x1,y1=dragStart
    x2,y2=dragEnd
    xmin, xmax = min(x1,x2), max(x1,x2)
    ymin, ymax = min(y1,y2), max(y1,y2)
    for contour in appState.worker.contourData:
        c_x1,c_y1=contour["Start"]
        c_x2,c_y2=contour["End"]
        overlap= not (c_x2<xmin or c_x1>xmax or c_y2<ymin or c_y1>ymax)
        if overlap:
            contour["Flag"]=not contour["Flag"]

#AKCIJE ZA MAIN MENU
def buttonActionHandlerMM(button):
    if button.action=="extractor":
        appState.runState["letter"]=True
        appState.runState["menu"]=False
    if button.action=="data":
        appState.runState["data"]=True
        appState.runState["menu"]=False
    if button.action=="network":
        appState.runState["network"]=True
        appState.runState["menu"]=False
    if button.action=="recognize":
        appState.runState["recognize"]=True
        appState.runState["menu"]=False




#AKCIJE ZA DATA
def buttonActionHandlerDT(button):
    if button.action=="menu":
        appState.displayState={"image":True,
                                "thresh":False,
                                "contours":False,
                                "name":True,
                                "size":False,
                                "select":False,
                                "recognize":False,
                                "confidence":False}
        resetButtons(buttons=buttonsDT)
        appState.runState["menu"]=True
        appState.runState["data"]=False
    
    if button.action=="sort":
        appState.displayState["name"]= not appState.displayState["name"]
        appState.displayState["size"]= not appState.displayState["size"]


#AKCIJE ZA RECOGNIZE
def buttonActionHandlerRL(button):
    #meni
    if button.action=="menu":
        appState.displayState={"image":True,
                                "thresh":False,
                                "contours":False,
                                "name":True,
                                "size":False,
                                "select":False,
                                "recognize":False,
                                "confidence":False}
        resetButtons(buttons=buttonsRL)
        appState.runState["menu"]=True
        appState.runState["recognize"]=False

    #biranje slike
    if button.action=="select":
        path=imageSelectFolder()
        #image=cv2.imread(path)
        appState.selectedImage,appState.selectedImageThresh=appState.worker.processImage(path)
        appState.ThreshCopyImg=appState.selectedImageThresh.copy()
        appState.selectedImagePath=path
        appState.results.clear()
        appState.worker.contourData.clear()
        appState.displayState["recognize"]=False

    #thresh slika
    if button.action=="thresh":
        appState.displayState["image"]= not appState.displayState["image"]
        appState.displayState["thresh"]= not appState.displayState["thresh"]
    
    #prikaz kontura
    if button.action=="contours":
        appState.displayState["contours"]= not appState.displayState["contours"]

    if button.action=="recognize":
        runRecognition()
        appState.displayState["recognize"]=True

    if button.action=="confidence":
        appState.displayState["confidence"]=True
        for button in buttonsRL[:]:
            if button.action not in ("menu"):
                buttonStorageRL.append(button)
                buttonsRL.remove(button)
        for button in buttonStorageRL[:]:
            if button.action in ("back"):
                buttonsRL.append(button)
                buttonStorageRL.remove(button)

    if button.action=="back":
        appState.displayState["confidence"]=False
        for button in buttonsRL[:]:
            if button.action in ("back"):
                buttonStorageRL.append(button)
                buttonsRL.remove(button)
        for button in buttonStorageRL[:]:
            if button.action not in ("back"):
                buttonsRL.append(button)
                buttonStorageRL.remove(button)



#Helper funkcija za otvaranje foldera za selekciju slike
def imageSelectFolder():
    root = tk.Tk()
    root.withdraw()

    path = filedialog.askopenfilename(
        title="Select image",
        filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")]
    )

    root.destroy()
    return path


def runRecognition():
    if not appState.displayState["recognize"]:

        
        #prvi model
        classes = [
            'A','B','C','D','E','F','G','H','I','J',
            'K','L','M','N','O','P','R','S','T','U',
            'V','Z','Ć','Č','Đ','Š','Ž']
        

        

        """
        #drugi model
        classes = ['A', 'B', 'C', 'D', 'E', 'F',
                    'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'R', 'S',
                    'T', 'U', 'V', 'Z',
                    'a', 'b', 'd', 'e', 'f', 'g',
                    'h', 'i', 'l', 'n', 'r', 't',
                    'Ć', 'Č', 'Đ',
                    'đ', 'Š', 'Ž']"""
        

        model = model_1(inputShape=1, hiddenUnits=10, outputShape=27)
        model.load_state_dict(torch.load("neuralNetwork/savedModels/model_5.pth"))
        model.eval()

        contours = appState.worker.getContour(threshImage=appState.selectedImageThresh)
        contours = sortContours(contours)
        #contours = sorted(contours, key=lambda x: x[0])


        for x, y, w, h in contours:
            letter = appState.worker.extractLetter(x, y, w, h, appState.selectedImageThresh)
            letter = appState.worker.augmentLetters(letter)

            tensor = torch.tensor(letter).float().unsqueeze(0).unsqueeze(0)/255.0
            prediction = model(tensor)

            """
            #PRVA ITERACIJA

            label = prediction.argmax(dim=1).item()
            predictedChar = classes[label]
            appState.results.append(predictedChar)
            """


            
            #DRUGA ITERACIJA
            #print(prediction)
            probs = torch.softmax(prediction, dim=1)
            #print(probs)
            label = probs.argmax(dim=1).item()
            confidence = probs[0][label].item() * 100
            predictedChar = classes[label]
            appState.results.append(predictedChar)
            appState.confidence.append(confidence)
            



            """
            #TRECA ITERACIJA
            probs = torch.softmax(prediction, dim=1)

            topProbs, topLabels = torch.topk(probs, k=2, dim=1)

            # prvi guess
            label1 = topLabels[0][0].item()
            confidence1 = topProbs[0][0].item() * 100
            predictedChar1 = classes[label1]
            appState.results1.append(predictedChar1)
            appState.confidence1.append(confidence1)

            # drugi guess
            label2 = topLabels[0][1].item()
            confidence2 = topProbs[0][1].item() * 100
            predictedChar2 = classes[label2]
            appState.results2.append(predictedChar2)
            appState.confidence2.append(confidence2)
            """


            putTextPIL(appState.selectedImage, predictedChar, (x, y - 15), color=(0, 0, 0), size=16)
            putTextPIL(appState.selectedImageThresh, predictedChar, (x, y - 15), color=255, size=16)#ovde je color samo 255 a ne (255,255,255) jer thresh ima samo jedan kanal
            #cv2.putText(appState.selectedImage, predictedChar, (x, y-5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            #cv2.putText(appState.selectedImageThresh, predictedChar, (x, y-5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)


#sortiranje kontura tako da su poredjane tako kao da se citaju
def sortContours(contours, lineThreshold=25):

    # sortiraj prvo po y
    contours = sorted(contours, key=lambda c: c[1])

    rows = []
    currentRow = []

    currentY = contours[0][1]

    for contour in contours:

        x, y, w, h = contour

        # isto tekstualno "vrsta"
        if abs(y - currentY) < lineThreshold:
            currentRow.append(contour)

        else:
            # sortiraj red po x
            currentRow = sorted(currentRow, key=lambda c: c[0])

            rows.append(currentRow)

            currentRow = [contour]
            currentY = y

    # poslednji red
    currentRow = sorted(currentRow, key=lambda c: c[0])
    rows.append(currentRow)

    # flatten
    sortedContours = []

    for row in rows:
        for contour in row:
            sortedContours.append(contour)

    return sortedContours



#helper funkcija za reset buttona pri izlazu u meni
def resetButtons(buttons):
    for button in buttons:
        button.pressed = False
        button.toggle = False