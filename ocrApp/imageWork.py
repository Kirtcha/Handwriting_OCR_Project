import cv2
import numpy as np 
from torchvision import transforms
from PIL import Image as PILimage

class imageWork:
    def __init__(self):
        self.blurKernel=5#ide 1-31, uvek neparan
        self.sigma=0#od 0-10
        self.blockSize=21#od 3-51, uvek neparan
        self.c=5#od -20-20
        self.contourData=[]

    def processImage(self,imagePath):
        image=cv2.imread(imagePath)
        grayImg=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(grayImg, (self.blurKernel, self.blurKernel), self.sigma)
        thresh = cv2.adaptiveThreshold(blurred ,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,self.blockSize,self.c)

        img = cv2.resize(image, (700,700))#radimo resize slike za canvas
        thresh = cv2.resize(thresh, (700,700))#radimo resize slike za canvas
        return img,thresh
    

    def getContour(self,threshImage):
        contour,_=cv2.findContours(threshImage,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        listOfContours=[]#pravimo listu kontura sa njenim koordinatama    
        for cnt in contour:
            x,y,w,h=cv2.boundingRect(cnt)
            area=cv2.contourArea(cnt)
            if area<500 and area>5:
                listOfContours.append((x,y,w,h)) 
                #ovo je dodato za resavanje problema sa i i j
            mergedContours = self.mergeDotsWithLetters(listOfContours)   
        #return listOfContours
        return mergedContours
    
    """
    def mergeDotsWithLetters(self, rawContours):
        mergedContours = []
        used = set()
        for letterIndex, (letterX, letterY, letterW, letterH) in enumerate(rawContours):
            if letterIndex in used:
                continue
            merged = False
            for dotIndex, (dotX, dotY, dotW, dotH) in enumerate(rawContours):
                if letterIndex == dotIndex or dotIndex in used:
                    continue
                # da li je dotIndex mala kontura (potencijalna tacka)
                if dotW < 15 and dotH < 15:
                    # da li je tacka iznad slova
                    if dotY < letterY:
                        # centri kontura po x osi
                        letterCenterX = letterX + letterW // 2
                        dotCenterX = dotX + dotW // 2
                        # da li su centrirani po x osi
                        if abs(letterCenterX - dotCenterX) < 10:
                            # donji rub tacke
                            dotBottomY = dotY + dotH
                            # razmak izmedju tacke i slova
                            gapY = letterY - dotBottomY
                            # da li su dovoljno blizu po y osi
                            if gapY < 25:
                                # spajanje
                                mergedX = min(letterX, dotX)
                                mergedY = min(letterY, dotY)
                                mergedW = max(letterX + letterW, dotX + dotW) - mergedX
                                mergedH = max(letterY + letterH, dotY + dotH) - mergedY
                                mergedContours.append((mergedX, mergedY, mergedW, mergedH))
                                used.add(letterIndex)
                                used.add(dotIndex)
                                merged = True
                                break
            if not merged and letterIndex not in used:
                mergedContours.append((letterX, letterY, letterW, letterH))
        return mergedContours
        """
    


    def mergeDotsWithLetters(self, rawContours):
        mergedContours = []
        used = set()

        areas = [w * h for (x, y, w, h) in rawContours]
        if not areas:
            return []

        letterAreas = [w * h for (x, y, w, h) in rawContours if not (w < 9 and h < 9)]

        if letterAreas:
            medianArea = sorted(letterAreas)[len(letterAreas) // 2]
        else:
            medianArea = sorted(areas)[len(areas) // 2]

        # ← razdvajamo unapred umesto da proveravamo unutar petlje
        dots = [(i, x, y, w, h) for i, (x, y, w, h) in enumerate(rawContours) if w < 9 and h < 9]
        letters = [(i, x, y, w, h) for i, (x, y, w, h) in enumerate(rawContours) if not (w < 9 and h < 9)]
        print(f"dots: {[(x,y,w,h) for i,x,y,w,h in dots]}")
        print(f"letters: {[(x,y,w,h) for i,x,y,w,h in letters]}")

        for letterIndex, letterX, letterY, letterW, letterH in letters:
            if letterIndex in used:
                continue

            merged = False

            # ← iteriramo samo kroz tacke, ne kroz sve konture
            for dotIndex, dotX, dotY, dotW, dotH in dots:
                if dotIndex in used:
                    continue

                if dotY < letterY:
                    letterCenterX = letterX + letterW // 2
                    dotCenterX = dotX + dotW // 2
                    if abs(letterCenterX - dotCenterX) < 15:
                        dotBottomY = dotY + dotH
                        gapY = letterY - dotBottomY
                        horizontallyClose = (dotX + dotW) > (letterX - 10) and dotX < (letterX + letterW + 10)

                        mergedArea = (max(letterX + letterW, dotX + dotW) - min(letterX, dotX)) * \
                                    (max(letterY + letterH, dotY + dotH) - min(letterY, dotY))
                        areaOk = mergedArea < medianArea * 5
                        

                        if gapY < 35 and horizontallyClose and areaOk:
                            mergedX = min(letterX, dotX)
                            mergedY = min(letterY, dotY)
                            mergedW = max(letterX + letterW, dotX + dotW) - mergedX
                            mergedH = max(letterY + letterH, dotY + dotH) - mergedY
                            mergedContours.append((mergedX, mergedY, mergedW, mergedH))
                            used.add(letterIndex)
                            used.add(dotIndex)
                            merged = True
                            break

            if not merged and letterIndex not in used:
                mergedContours.append((letterX, letterY, letterW, letterH))

        return mergedContours


    def drawContours(self,image,contourData):
        for contour in contourData:
            x1,y1=contour["Start"]
            x2,y2=contour["End"]
            if contour["Flag"]==True:
                cv2.rectangle(image,(x1,y1),(x2,y2),(0,0,255),1)
            else:
                cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,255),1)
        return image
    

    #moramo prebaciti thresh u trodimenzionalnu sliku (iz (700,700) u (700,700,3)) da bi mogla da se stavi na canvas jer je canvas BGR a thresh je crno bela slika
    def displayThreshImage(self,threshImage):
        thresh=cv2.cvtColor(threshImage, cv2.COLOR_GRAY2BGR)
        return thresh
    

    def extractLetter(self,x,y,w,h,threshImage):
        x1,y1,x2,y2=x,y,x+w,y+h
        h_thresh,w_thresh=threshImage.shape
        x1=max(0,x1)
        y1=max(0,y1)
        x2=min(w_thresh,x2)
        y2=min(h_thresh,y2)
        letter=threshImage[y1:y2,x1:x2]
        return letter
    

    def makeContourList(self,listOfContours,threshImage):
        self.contourData.clear()
        for x,y,w,h in listOfContours:
            letter=self.extractLetter(x,y,w,h,threshImage)
            self.contourData.append({
                "Start": [x, y],
                "End": [x+w, y+h],
                "Letter": letter,
                "Flag": False})
            
    #helper funkcija koja vraca  selektovane konture     
    def selectedContours(self):
        return sum(1 for c in self.contourData if c["Flag"] is True)

    #helper funkcija koja vraca ne selektovane konture     
    def unselectedContours(self):
        return sum(1 for c in self.contourData if c["Flag"] is False)
            
    """
    def augmentLetters(self,letter):
        standardizeLetter=transforms.Compose([transforms.Resize((20,20)),
                                              transforms.Pad(4)])
        letterPIL=PILimage.fromarray(letter)
        augmentedLetter=standardizeLetter(letterPIL)
        augmentedLetter=np.array(augmentedLetter)
        return augmentedLetter
        """
    

    def augmentLetters(self, letter):

        h, w = letter.shape

        # maksimalna dimenzija postaje 20
        if h > w:
            new_h = 20
            #new_w = int((w / h) * 20)
            new_w = max(1, int((w / h) * 20))
        else:
            new_w = 20
            #new_h = int((h / w) * 20)
            new_h = max(1, int((h / w) * 20))

        # resize sa očuvanjem proporcija
        resized = cv2.resize(letter, (new_w, new_h))

        # pravimo 28x28 slovo
        augmentedLetter = np.zeros((28, 28), dtype=np.uint8)

        # centriranje
        x_offset = (28 - new_w) // 2
        y_offset = (28 - new_h) // 2

        augmentedLetter[y_offset:y_offset+new_h,
            x_offset:x_offset+new_w] = resized

        return augmentedLetter





