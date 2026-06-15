import cv2
import numpy as np
import os
import time
from PIL import ImageFont, ImageDraw, Image
from imageLoader import imageLoader
from imageWork import imageWork
from imageSaver import saveLetter


class userInterface():

    def __init__(self, loader: imageLoader, worker: imageWork):
        self.loader = loader
        self.worker = worker
        self.letterName = ""
        self.threshFlag = False
        self.contourButtonFlag = False
        self.selectedContours = 0
        self.slider1Percentage = int(100*(self.worker.blurKernel-1)/30)
        self.slider1Flag = False
        self.slider2Percentage = int(100*self.worker.sigma/10)
        self.slider2Flag = False
        self.slider3Percentage = int(100*(self.worker.blockSize-3)/48)
        self.slider3Flag = False
        self.slider4Percentage = int(100*(self.worker.c+20)/40)
        self.slider4Flag = False
        self.moveToUsedImagesFlag = False
        self.saveButtonFlag = False
        self.lastImageFlag = False
        self.threshButtonStateFlag = False
        self.contourButtonStateFlag = False
        self.clearButtonStateFlag = False
        self.saveButtonStateFlag = False
        self.yesButtonStateFlag = False
        self.noButtonStateFlag = False
        self.backButtonStateFlag = False
        self.nextButtonStateFlag = False
        self.moveButtonStateFlag = False
        self.resetButtonStateFlag = False
        self.cursorTime = time.time()
        self.cursorFlag = True
        self.font = ImageFont.truetype("arial.ttf", 16)

    def refreshContours(self):
        imgPath = self.loader.importImage("Images/notUsed")
        if imgPath is None:
            return
        _, thresh = self.worker.processImage(imgPath)
        listOfContours = self.worker.getContour(thresh)
        self.worker.makeContourList(listOfContours, thresh)
        self.selectedContours = 0

    def createCanvas(self):
        return np.zeros((800, 1000, 3), dtype=np.uint8)

    def display(self):
        cv2.namedWindow("Letter Extractor")
        cv2.setMouseCallback("Letter Extractor", self.mouseCallback)
        imgPath = self.loader.importImage("Images/notUsed")
        if imgPath is None:
            self.lastImageFlag = True
        else:
            self.refreshContours()
        while True:
            canvas = self.createCanvas()
            if self.lastImageFlag == False:
                self.createButtons(canvas)
                self.createTrackbars(canvas)
            self.updateCanvasImage(canvas)
            cv2.imshow("Letter Extractor", canvas)
            key = cv2.waitKey(1) & 0xFF
            self.keyboard(key)
            if cv2.getWindowProperty("Letter Extractor", cv2.WND_PROP_VISIBLE) < 1:
                break

    def createButtons(self, canvas):
        cv2.rectangle(canvas, (765, 205), (935, 245), (255, 255, 255), 1)
        if self.threshButtonStateFlag:
            cv2.rectangle(canvas, (765, 205), (935, 245), (255, 255, 255), 2)
        cv2.putText(canvas, "black&white", (790, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.rectangle(canvas, (765, 255), (935, 295), (255, 255, 255), 1)
        if self.contourButtonStateFlag:
            cv2.rectangle(canvas, (765, 255), (935, 295), (255, 255, 255), 2)
        cv2.putText(canvas, "contours", (825, 275), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.rectangle(canvas, (765, 305), (935, 345), (255, 255, 255), 1)
        if self.clearButtonStateFlag:
            cv2.rectangle(canvas, (765, 305), (935, 345), (255, 255, 255), 2)
        if self.selectedContours == 0:
            cv2.putText(canvas, "No letters selected", (770, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        else:
            cv2.putText(canvas, "Deselect", (785, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(canvas, str(self.selectedContours), (855, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(canvas, "letters", (875, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        if self.saveButtonFlag == False:
            cv2.rectangle(canvas, (765, 355), (935, 395), (255, 255, 255), 1)
            if self.saveButtonStateFlag:
                cv2.rectangle(canvas, (765, 355), (935, 395), (255, 255, 255), 2)
            cv2.putText(canvas, "save", (790, 380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(canvas, str(len(self.worker.contourData)-self.selectedContours), (845, 380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(canvas, "letters", (870, 380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        else:
            if time.time()-self.cursorTime > 0.5:
                self.cursorFlag = not self.cursorFlag
                self.cursorTime = time.time()
            cursor = "|" if self.cursorFlag else ""
            cv2.rectangle(canvas, (765, 355), (910, 395), (255, 255, 255), 1)
            self.putTextPIL(canvas, self.letterName+cursor, (790, 365))
            cv2.rectangle(canvas, (910, 355), (935, 375), (255, 255, 255), 1)
            if self.yesButtonStateFlag:
                cv2.rectangle(canvas, (910, 355), (935, 375), (255, 255, 255), 2)
            cv2.putText(canvas, "Yes", (912, 370), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            cv2.rectangle(canvas, (910, 375), (935, 395), (255, 255, 255), 1)
            if self.noButtonStateFlag:
                cv2.rectangle(canvas, (910, 375), (935, 395), (255, 255, 255), 2)
            cv2.putText(canvas, "No", (915, 390), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        cv2.rectangle(canvas, (765, 405), (847, 445), (255, 255, 255), 1)
        if self.backButtonStateFlag:
            cv2.rectangle(canvas, (765, 405), (847, 445), (255, 255, 255), 2)
        cv2.putText(canvas, "back", (790, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.rectangle(canvas, (853, 405), (935, 445), (255, 255, 255), 1)
        if self.nextButtonStateFlag:
            cv2.rectangle(canvas, (853, 405), (935, 445), (255, 255, 255), 2)
        cv2.putText(canvas, "next", (880, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.rectangle(canvas, (765, 455), (935, 495), (255, 255, 255), 1)
        if self.moveButtonStateFlag:
            cv2.rectangle(canvas, (765, 455), (935, 495), (255, 255, 255), 2)
        cv2.putText(canvas, "Move to used images", (780, 475), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        if self.moveToUsedImagesFlag:
            cv2.rectangle(canvas, (765, 455), (935, 495), (255, 255, 255), 2)

        cv2.rectangle(canvas, (930, 700), (970, 785), (255, 255, 255), 1)
        if self.resetButtonStateFlag:
            cv2.rectangle(canvas, (930, 700), (970, 785), (255, 255, 255), 2)
        cv2.putText(canvas, "r", (945, 715), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(canvas, "e", (945, 730), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(canvas, "s", (945, 745), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(canvas, "e", (945, 760), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(canvas, "t", (945, 775), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    def createTrackbars(self, canvas):
        x1_start, x1_end, y1 = 50, 450, 725
        x1 = int(x1_start+(x1_end-x1_start)/100*self.slider1Percentage)
        cv2.putText(canvas, "Blur Amount", (int((x1_start+x1_end)/2)-60, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.rectangle(canvas, (x1_start, y1-1), (x1_end, y1+1), (255, 255, 255), -1)
        cv2.rectangle(canvas, (x1-5, y1-5), (x1+5, y1+5), (255, 255, 255), -1)

        x2_start, x2_end, y2 = 50, 450, 760
        x2 = int(x2_start+(x2_end-x2_start)/100*self.slider2Percentage)
        cv2.putText(canvas, "Smoothness", (int((x2_start+x2_end)/2)-55, y2-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.rectangle(canvas, (x2_start, y2-1), (x2_end, y2+1), (255, 255, 255), -1)
        cv2.rectangle(canvas, (x2-5, y2-5), (x2+5, y2+5), (255, 255, 255), -1)

        x3_start, x3_end, y3 = 500, 900, 725
        x3 = int(x3_start+(x3_end-x3_start)/100*self.slider3Percentage)
        cv2.putText(canvas, "Detection Area", (int((x3_start+x3_end)/2)-70, y3-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.rectangle(canvas, (x3_start, y3-1), (x3_end, y3+1), (255, 255, 255), -1)
        cv2.rectangle(canvas, (x3-5, y3-5), (x3+5, y3+5), (255, 255, 255), -1)

        x4_start, x4_end, y4 = 500, 900, 760
        x4 = int(x4_start+(x4_end-x4_start)/100*self.slider4Percentage)
        cv2.putText(canvas, "Contrast", (int((x4_start+x4_end)/2)-80, y4-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.rectangle(canvas, (x4_start, y4-1), (x4_end, y4+1), (255, 255, 255), -1)
        cv2.rectangle(canvas, (x4-5, y4-5), (x4+5, y4+5), (255, 255, 255), -1)

    def updateCanvasImage(self, canvas):
        if self.lastImageFlag:
            canvas[0:700, 0:700] = 0
            cv2.putText(canvas, "No more images!", (356, 411), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            return

        imgPath = self.loader.importImage("Images/notUsed")
        img, thresh = self.worker.processImage(imgPath)
        thresh_bgr = self.worker.displayThreshImage(thresh)

        if self.threshFlag:
            canvas[0:700, 0:700] = thresh_bgr
            cv2.rectangle(canvas, (765, 205), (935, 245), (255, 255, 255), 2)
        else:
            canvas[0:700, 0:700] = img

        if self.contourButtonFlag:
            cv2.rectangle(canvas, (765, 255), (935, 295), (255, 255, 255), 2)
            listOfContours = self.worker.getContour(thresh)
            if self.threshFlag:
                contourImage = self.worker.drawContours(thresh_bgr, listOfContours)
            else:
                contourImage = self.worker.drawContours(img, listOfContours)
            canvas[0:700, 0:700] = contourImage

        for contour in self.worker.contourData:
            if contour["Flag"] and self.contourButtonFlag:
                cv2.rectangle(canvas, contour["Start"], contour["End"], (0, 0, 255), 1)

    def resetTrackbars(self):
        self.worker.blurKernel = 5
        self.slider1Percentage = int(100*(self.worker.blurKernel-1)/30)
        self.worker.sigma = 0
        self.slider2Percentage = int(100*self.worker.sigma/10)
        self.worker.blockSize = 21
        self.slider3Percentage = int(100*(self.worker.blockSize-3)/48)
        self.worker.c = 5
        self.slider4Percentage = int(100*(self.worker.c+20)/40)
        self.selectedContours = 0
        self.worker.contourData.clear()
        self.refreshContours()

    def keyboard(self, key):
        srp_latin_map = {
            200: 'Č', 198: 'Ć', 208: 'Đ', 138: 'Š', 142: 'Ž',
            232: 'č', 230: 'ć', 240: 'đ', 154: 'š', 158: 'ž'}
        if self.saveButtonFlag:
            if 65 <= key <= 90 or 97 <= key <= 122:
                self.letterName += chr(key)
            elif key in srp_latin_map:
                self.letterName += srp_latin_map[key]
            elif key == 8:
                self.letterName = self.letterName[:-1]
            elif key == 13 and self.letterName != "":
                self.saveButtonFlag = False
                saveLetter(self.worker.contourData, self.letterName)
                self.letterName = ""
            elif key == 27:
                self.saveButtonFlag = False
                self.letterName = ""

    def putTextPIL(self, canvas, text, position, color=(255, 255, 255)):
        img_pil = Image.fromarray(canvas)
        draw = ImageDraw.Draw(img_pil)
        draw.text(position, text, font=self.font, fill=color)
        canvas[:] = np.array(img_pil)

    def mouseCallback(self, event, x, y, flags, param):
        self.threshButton(event, x, y, flags, param)
        self.contourButton(event, x, y, flags, param)
        self.contourInteraction(event, x, y, flags, param)
        self.clearButton(event, x, y, flags, param)
        self.sliderInteraction(event, x, y, flags, param)
        self.saveButton(event, x, y, flags, param)
        self.resetTrackbarsButton(event, x, y, flags, param)
        self.nextImageButton(event, x, y, flags, param)
        self.backImageButton(event, x, y, flags, param)
        self.moveToUsedImagesButton(event, x, y, flags, param)

    def threshButton(self, event, x, y, flags, param):
        buttonStart = (765, 205)
        buttonEnd = (935, 245)
        if event == cv2.EVENT_LBUTTONDOWN:
            if buttonStart[0]<=x<=buttonEnd[0] and buttonStart[1]<=y<=buttonEnd[1] and not self.lastImageFlag:
                self.threshButtonStateFlag = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.threshButtonStateFlag = False
            if buttonStart[0]<=x<=buttonEnd[0] and buttonStart[1]<=y<=buttonEnd[1] and not self.lastImageFlag:
                self.threshFlag = not self.threshFlag

    def contourButton(self, event, x, y, flags, param):
        buttonStart = (765, 255)
        buttonEnd = (935, 295)
        if event == cv2.EVENT_LBUTTONDOWN:
            if buttonStart[0]<=x<=buttonEnd[0] and buttonStart[1]<=y<=buttonEnd[1] and not self.lastImageFlag:
                self.contourButtonStateFlag = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.contourButtonStateFlag = False
            if buttonStart[0]<=x<=buttonEnd[0] and buttonStart[1]<=y<=buttonEnd[1] and not self.lastImageFlag and len(self.worker.contourData) != 0:
                self.contourButtonFlag = not self.contourButtonFlag

    def contourInteraction(self, event, x, y, flags, param):
        for contour in self.worker.contourData:
            contourStart = contour["Start"]
            contourEnd = contour["End"]
            if event == cv2.EVENT_LBUTTONDOWN:
                if contourStart[0]<=x<=contourEnd[0] and contourStart[1]<=y<=contourEnd[1] and self.contourButtonFlag:
                    if contour["Flag"] == False:
                        self.selectedContours += 1
                        contour["Flag"] = True
                    else:
                        self.selectedContours -= 1
                        contour["Flag"] = False

    def clearButton(self, event, x, y, flags, param):
        buttonStart = (765, 305)
        buttonEnd = (935, 345)
        if event == cv2.EVENT_LBUTTONDOWN:
            if buttonStart[0]<=x<=buttonEnd[0] and buttonStart[1]<=y<=buttonEnd[1] and self.selectedContours != 0 and not self.lastImageFlag:
                self.clearButtonStateFlag = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.clearButtonStateFlag = False
            if buttonStart[0]<=x<=buttonEnd[0] and buttonStart[1]<=y<=buttonEnd[1] and not self.lastImageFlag:
                for contour in self.worker.contourData:
                    contour["Flag"] = False
                self.selectedContours = 0

    def saveButton(self, event, x, y, flags, param):
        buttonStart = (765, 355)
        buttonEnd = (935, 395)
        if event == cv2.EVENT_LBUTTONDOWN:
            if buttonStart[0]<=x<=buttonEnd[0] and buttonStart[1]<=y<=buttonEnd[1] and not self.saveButtonFlag and not self.lastImageFlag:
                self.saveButtonStateFlag = True
            elif buttonStart[0]+145<=x<=buttonEnd[0]+20 and buttonStart[1]<=y<=buttonEnd[1]-20 and self.saveButtonFlag and self.letterName != "":
                self.yesButtonStateFlag = True
            elif buttonStart[0]+145<=x<=buttonEnd[0]+20 and buttonStart[1]+20<=y<=buttonEnd[1] and self.saveButtonFlag:
                self.noButtonStateFlag = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.saveButtonStateFlag = False
            self.yesButtonStateFlag = False
            self.noButtonStateFlag = False
            if buttonStart[0]<=x<=buttonEnd[0] and buttonStart[1]<=y<=buttonEnd[1] and len(self.worker.contourData) != 0 and not self.saveButtonFlag and not self.lastImageFlag:
                self.saveButtonFlag = True
            elif buttonStart[0]+145<=x<=buttonEnd[0]+20 and buttonStart[1]<=y<=buttonEnd[1]-20 and self.saveButtonFlag and self.letterName != "":
                self.saveButtonFlag = False
                saveLetter(self.worker.contourData, self.letterName)
                self.letterName = ""
            elif buttonStart[0]+145<=x<=buttonEnd[0]+20 and buttonStart[1]+20<=y<=buttonEnd[1] and self.saveButtonFlag:
                self.saveButtonFlag = False
                self.letterName = ""

    def resetTrackbarsButton(self, event, x, y, flags, param):
        buttonStart = (930, 700)
        buttonEnd = (970, 785)
        if event == cv2.EVENT_LBUTTONDOWN:
            if buttonStart[0]<=x<=buttonEnd[0] and buttonStart[1]<=y<=buttonEnd[1] and not self.lastImageFlag:
                self.resetButtonStateFlag = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.resetButtonStateFlag = False
            if buttonStart[0]<=x<=buttonEnd[0] and buttonStart[1]<=y<=buttonEnd[1] and not self.lastImageFlag:
                self.resetTrackbars()

    def nextImageButton(self, event, x, y, flags, param):
        buttonStart = (853, 405)
        buttonEnd = (935, 445)
        if event == cv2.EVENT_LBUTTONDOWN:
            if buttonStart[0]<=x<=buttonEnd[0] and buttonStart[1]<=y<=buttonEnd[1] and not self.lastImageFlag and self.loader.imageIndex!=len(os.listdir("Images/notUsed"))-1:
                self.nextButtonStateFlag = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.nextButtonStateFlag = False
            if buttonStart[0]<=x<=buttonEnd[0] and buttonStart[1]<=y<=buttonEnd[1] and not self.lastImageFlag:
                imageList = os.listdir("Images/notUsed")
                if self.loader.imageIndex < len(imageList)-1:
                    if self.moveToUsedImagesFlag:
                        self.loader.moveImageToUsed("Images/notUsed")
                        self.loader.imageIndex = 0
                    else:
                        self.loader.imageIndex += 1
                    self.resetTrackbars()
                elif self.loader.imageIndex == len(imageList)-1 and self.moveToUsedImagesFlag:
                    self.loader.moveImageToUsed("Images/notUsed")
                    self.loader.imageIndex = 0
                    self.lastImageFlag = True

    def backImageButton(self, event, x, y, flags, param):
        buttonStart = (765, 405)
        buttonEnd = (847, 445)
        if event == cv2.EVENT_LBUTTONDOWN:
            if buttonStart[0]<=x<=buttonEnd[0] and buttonStart[1]<=y<=buttonEnd[1] and self.loader.imageIndex != 0 and not self.lastImageFlag:
                self.backButtonStateFlag = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.backButtonStateFlag = False
            if buttonStart[0]<=x<=buttonEnd[0] and buttonStart[1]<=y<=buttonEnd[1] and not self.lastImageFlag:
                if self.loader.imageIndex > 0:
                    self.loader.imageIndex -= 1
                    self.resetTrackbars()

    def moveToUsedImagesButton(self, event, x, y, flags, param):
        buttonStart = (765, 455)
        buttonEnd = (935, 495)
        if event == cv2.EVENT_LBUTTONDOWN:
            if buttonStart[0]<=x<=buttonEnd[0] and buttonStart[1]<=y<=buttonEnd[1] and not self.lastImageFlag:
                self.moveButtonStateFlag = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.moveButtonStateFlag = False
            if buttonStart[0]<=x<=buttonEnd[0] and buttonStart[1]<=y<=buttonEnd[1] and not self.lastImageFlag:
                self.moveToUsedImagesFlag = not self.moveToUsedImagesFlag

    def sliderInteraction(self, event, x, y, flags, param):
        x1_start, x1_end, y1_start, y1_end = 50, 450, 720, 730
        x2_start, x2_end, y2_start, y2_end = 50, 450, 755, 765
        x3_start, x3_end, y3_start, y3_end = 500, 900, 720, 730
        x4_start, x4_end, y4_start, y4_end = 500, 900, 755, 765

        if event == cv2.EVENT_LBUTTONDOWN:
            if x1_start<=x<=x1_end and y1_start<=y<=y1_end and not self.lastImageFlag:
                self.slider1Flag = True
            elif x2_start<=x<=x2_end and y2_start<=y<=y2_end and not self.lastImageFlag:
                self.slider2Flag = True
            elif x3_start<=x<=x3_end and y3_start<=y<=y3_end and not self.lastImageFlag:
                self.slider3Flag = True
            elif x4_start<=x<=x4_end and y4_start<=y<=y4_end and not self.lastImageFlag:
                self.slider4Flag = True

        elif event == cv2.EVENT_LBUTTONUP and (self.slider1Flag or self.slider2Flag or self.slider3Flag or self.slider4Flag):
            self.slider1Flag = False
            self.slider2Flag = False
            self.slider3Flag = False
            self.slider4Flag = False
            self.worker.contourData.clear()
            self.refreshContours()

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.slider1Flag:
                x = max(x1_start, min(x, x1_end))
                self.slider1Percentage = int((x-x1_start)/(x1_end-x1_start)*100)
                self.worker.blurKernel = int(30*self.slider1Percentage/100)+1
                if self.worker.blurKernel % 2 == 0:
                    self.worker.blurKernel += 1
            elif self.slider2Flag:
                x = max(x2_start, min(x, x2_end))
                self.slider2Percentage = int((x-x2_start)/(x2_end-x2_start)*100)
                self.worker.sigma = int(10*self.slider2Percentage/100)
            elif self.slider3Flag:
                x = max(x3_start, min(x, x3_end))
                self.slider3Percentage = int((x-x3_start)/(x3_end-x3_start)*100)
                self.worker.blockSize = int(48*self.slider3Percentage/100)+3
                if self.worker.blockSize % 2 == 0:
                    self.worker.blockSize += 1
            elif self.slider4Flag:
                x = max(x4_start, min(x, x4_end))
                self.slider4Percentage = int((x-x4_start)/(x4_end-x4_start)*100)
                self.worker.c = int(40*self.slider4Percentage/100)-20