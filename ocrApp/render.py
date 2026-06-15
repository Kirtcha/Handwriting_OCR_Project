import cv2
import numpy as np 
import appState
import os
import time
from PIL import ImageFont, ImageDraw, Image
import tkinter as tk
from tkinter import filedialog



def drawButtons(image, buttons):
    for button in buttons:
        
        #USLOVI ZA THICKNESS
        thickness=1
        if button.isButton:
          if button.pressed==True or button.toggle==True:
               thickness=2
        x1,y1,x2,y2=button.x1, button.y1, button.x2, button.y2
        
        #CRTANJE PRAVOUGAONIKA
        cv2.rectangle(image, (x1,y1), (x2,y2), (255,255,255),thickness)

        #ISPIS TEKSTA

        #hardkodovano reset dugme jer je vertikalno
        if button.action=="reset":
            cv2.putText(image, "r", (945, 715), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(image, "e", (945, 730), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(image, "s", (945, 745), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(image, "e", (945, 760), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(image, "t", (945, 775), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        #ispis save button-a
        elif button.action=="save":
             if len(appState.worker.contourData)==0:
               (textWidth,textHeight),_=cv2.getTextSize("No letters to save!", cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
               textX=x1+(x2-x1-textWidth)//2
               textY=y1+(y2-y1+textHeight)//2
               cv2.putText(image, "No letters to save!", (textX, textY), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
             else:
               (textWidth,textHeight),_=cv2.getTextSize(f"save {appState.worker.unselectedContours()} letters", cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
               textX=x1+(x2-x1-textWidth)//2
               textY=y1+(y2-y1+textHeight)//2
               cv2.putText(image, f"save {appState.worker.unselectedContours()} letters", (textX, textY), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

        #harkodujemo yes i no dugme jer imaju manju dimenziju teksta
        elif button.text in ("Yes","No"):
             cv2.putText(image, "Yes", (912, 370), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
             cv2.putText(image, "No", (915, 390), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        #ispis teksta koji unosimo
        elif button.action == "input":
             putTextPIL(image=image, text=appState.letterName+drawCursor(), position=(790, 365))

        #ispis informacija o konturama
        elif button.action=="info":
             cv2.putText(image, f"All contours:{len(appState.worker.contourData)}", (775, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
             cv2.putText(image, f"Selected contours:{appState.worker.selectedContours()}", (775, 338), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

        #pisanje informacija o samples za treniranje
        elif button.action=="sampleInfo":
             putTextPIL(image=image, text=f"Avarage: {getAverageSample()} letters", position=(775, 220),size=15)#775,260

        elif button.action=="totalSample":
             putTextPIL(image=image, text=f"Total: {getTotalLetters()} letters", position=(775, 270),size=15)#775,260

        #pisanje sort dugmeta
        elif button.action=="sort":
             if appState.displayState["name"]:
                  sortName="Name"
             elif appState.displayState["size"]:
                  sortName="Size"
             (textWidth,textHeight),_=cv2.getTextSize(f"Sort by: {sortName}", cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
             textX=x1+(x2-x1-textWidth)//2
             textY=y1+(y2-y1+textHeight)//2
             cv2.putText(image, f"Sort by: {sortName}", (textX, textY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
               
        #centriramo tekst pre pisanja 
        else:
             (textWidth,textHeight),_=cv2.getTextSize(button.text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
             textX=x1+(x2-x1-textWidth)//2
             textY=y1+(y2-y1+textHeight)//2
             cv2.putText(image, button.text, (textX, textY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

def drawSliders(image,sliders):
     for slider in sliders:
          x1,x2,y,percentage=slider.x1,slider.x2,slider.y,slider.percentage
          sliderValue = int(x1+(x2-x1)/100*percentage)
          cv2.rectangle(image, (x1, y-1), (x2, y+1), (255, 255, 255), -1)
          cv2.rectangle(image, (sliderValue-5, y-5), (sliderValue+5, y+5), (255, 255, 255), -1)
          (textWidth,_),_=cv2.getTextSize(slider.text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
          textX=x1+(x2-x1-textWidth)//2
          cv2.putText(image, slider.text, (textX, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

def drawCanvas():
        return np.zeros((800, 1000, 3), dtype=np.uint8)

def letterExtractorDisplay(canvas):
     imgPath=appState.loader.importImage("Images/notUsed")
     if imgPath is None:
          #canvas[0:800, 0:1000] = 0
          cv2.putText(canvas, "No more images!", (220, 353), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
          return
     img,thresh=appState.worker.processImage(imgPath)
     """Stanja u kojima ce se naci display"""

     #prikaz obicne slike
     if appState.displayState["image"]:
          displayImage=img

     #prikaz thresh slike
     if appState.displayState["thresh"]:
          displayImage=appState.worker.displayThreshImage(thresh)

     #prikaz kontura
     #pravljenje kontura pri toggle-u button-a
     if appState.displayState["contours"]:
          if not appState.worker.contourData:
               listOfContours=appState.worker.getContour(threshImage=thresh)
               appState.worker.makeContourList(listOfContours=listOfContours,threshImage=thresh)
          displayImage=appState.worker.drawContours(image=displayImage,contourData=appState.worker.contourData)
     #brisanje kontura pri toggle-u button-a
     elif not appState.displayState["contours"]:
          if  appState.worker.contourData:
               appState.worker.contourData.clear()
     
     #crtanje drag-a
     if appState.dragStart and appState.dragEnd:
          x1,y1=appState.dragStart
          x2,y2=appState.dragEnd
          cv2.rectangle(displayImage,(x1,y1),(x2,y2),(0,255,255),1)

     canvas[0:700, 0:700] = displayImage

def drawCursor():
     if time.time()-appState.cursorTime>0.5:
          appState.cursorFlag= not appState.cursorFlag
          appState.cursorTime=time.time()
     return "|" if appState.cursorFlag else ""

def putTextPIL(image, text, position, color=(255, 255, 255),size=16):
        img_pil = Image.fromarray(image)
        draw = ImageDraw.Draw(img_pil)
        draw.text(position, text, font=ImageFont.truetype("arial.ttf", size), fill=color)
        image[:] = np.array(img_pil)



def showSamplesByName(canvas):
     y=150
     x=250
     for sample in os.listdir("Letters"):
          sampleNumber=os.listdir(f"Letters/{sample}")
          putTextPIL(image=canvas, text=f"{sample}  {len(sampleNumber)}", position=(x, y))
          y+=20
          if y==690:
               x=400
               y=150
     return canvas



def showSamplesBySize(canvas):
    samples = [
        (sample, len(os.listdir(f"Letters/{sample}")))
        for sample in os.listdir("Letters")
        if os.path.isdir(f"Letters/{sample}")
    ]

    # sort po broju slika (opadajuće)
    samples.sort(key=lambda x: x[1], reverse=True)

    y = 150
    x=250
    for sample, count in samples:
        putTextPIL(image=canvas, text=f"{sample}  {count}", position=(x, y))
        y += 20
        if y==690:
               x=400
               y=150

    return canvas

def getAverageSample(folder="Letters"):
    counts = [
        len(os.listdir(os.path.join(folder, s)))
        for s in os.listdir(folder)
        if os.path.isdir(os.path.join(folder, s))
    ]
    return round(sum(counts) / len(counts), 1) if counts else 0



def getTotalLetters(folder="Letters"):
    counts = [
        len(os.listdir(os.path.join(folder, sample)))
        for sample in os.listdir(folder)
        if os.path.isdir(os.path.join(folder, sample))
    ]

    return sum(counts)



def dataInfoDisplay(canvas):
     if appState.displayState["name"]:
            canvas[0:700, 0:700] = appState.sortedByName
     if appState.displayState["size"]:
            canvas[0:700, 0:700] = appState.sortedBySize
     


def mainMenuDisplay(canvas):
     cv2.putText(canvas, "MAIN MENU", (343, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 1)
     #cv2.putText(canvas, "Feed an image and recognize it's content ---------->", (150, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
     cv2.putText(canvas, "---------->", (400, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
     cv2.putText(canvas, "Feed an image and", (120, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
     cv2.putText(canvas, "recognize it's content", (120, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
     #cv2.putText(canvas, "Extract letters and make datasets out of them for training---------->", (150, 375), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
     cv2.putText(canvas, "---------->", (400, 375), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
     cv2.putText(canvas, "Extract letters and make", (120, 355), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
     cv2.putText(canvas, "datasets for training", (120, 385), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
     
     
     
     
     #cv2.putText(canvas, "View datasets that are used to train the neural network---------->", (150, 500), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
     cv2.putText(canvas, "   -------->", (400, 500), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
     cv2.putText(canvas, "View datasets that are used", (120, 480), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
     cv2.putText(canvas, "to train the neural network", (120, 510), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)


def recognizeDisplay(canvas):
     """
     #ispis prepoznatog teksta
     cv2.putText(canvas, "Recognized letters:", (770, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
     cv2.putText(canvas, "--------------------------", (700, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
     cv2.putText(canvas, "--------------------------", (700, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
     if appState.selectedImagePath and appState.displayState["recognize"]:
          tekst=" ".join(appState.results)
          cv2.putText(canvas, tekst, (710, 445), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
          
          y=530
          for letter,percent in zip(appState.results,appState.confidence):
               cv2.putText(canvas, letter, (780, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
               cv2.putText(canvas, f"{percent:.1f}%", (880, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
               y+=15
     else:
          cv2.putText(canvas, f"Press recognize to see!", (760, 445), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

     #prikaz sigurnosti predikcije
     cv2.putText(canvas, "Confidence score:", (770, 480), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
     cv2.putText(canvas, "Letter", (760, 500), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
     cv2.putText(canvas, "[%]", (900, 500), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
     cv2.putText(canvas, "--------------------------", (700, 515), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
     """
     if appState.displayState["confidence"]:
          #prikaz sigurnosti predikcije
          cv2.putText(canvas, "Confidence score:", (780, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
          cv2.putText(canvas, "Letter", (760, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
          cv2.putText(canvas, "[%]", (900, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
          cv2.putText(canvas, "--------------------------", (700, 305), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
          #y=320
          y=320
          for letter,percent in zip(appState.results,appState.confidence):
               #cv2.putText(canvas, letter, (780, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
               putTextPIL(canvas,letter,(780, y-15),color=(255, 255, 255),size=16)

               cv2.putText(canvas, f"{percent:.1f}%", (880, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
               y+=15
          

     #Prikaz za ako nema slike
     if appState.selectedImage is None:
          #canvas[0:700, 0:700]
          cv2.putText(canvas, "Select an image to be", (150, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
          cv2.putText(canvas, "used for letter recognition", (150, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
          cv2.putText(canvas, "-------------------->", (150, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
          return
     
     if appState.selectedImage is not None and appState.displayState["image"]:
          displayImage=appState.selectedImage.copy()

     #prikaz thresh slike
     if appState.displayState["thresh"]:
          displayImage=appState.worker.displayThreshImage(appState.selectedImageThresh)

     #pravljenje kontura pri toggle-u button-a
     if appState.displayState["contours"]:
          if not appState.worker.contourData:
               #listOfContours=appState.worker.getContour(threshImage=appState.selectedImageThresh)
               #appState.worker.makeContourList(listOfContours=listOfContours,threshImage=appState.selectedImageThresh)
               listOfContours=appState.worker.getContour(threshImage=appState.ThreshCopyImg)
               appState.worker.makeContourList(listOfContours=listOfContours,threshImage=appState.ThreshCopyImg)
          displayImage=appState.worker.drawContours(image=displayImage,contourData=appState.worker.contourData)

     #brisanje kontura pri toggle-u button-a
     if not appState.displayState["contours"]:
          if  appState.worker.contourData:
               appState.worker.contourData.clear()

     canvas[0:700, 0:700]=displayImage
     





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


def refreshDataInfo():
     #radim preprocessing ve slike koje koristim za prikazivanje data info
     image=np.zeros((700, 700, 3), dtype=np.uint8)
     appState.sortedByName = showSamplesByName(canvas=image.copy())
     appState.sortedBySize = showSamplesBySize(canvas=image.copy())