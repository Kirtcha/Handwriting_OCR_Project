from render import drawCanvas,drawButtons,drawSliders,letterExtractorDisplay,recognizeDisplay,dataInfoDisplay,mainMenuDisplay
from uiComponents import buttonsLE,slidersLE,buttonsRL,buttonsDT,buttonsMM
import cv2
from input import keyboardLE


#LETTER EXTRACT WINDOW
def runLetterExtractor():
    canvas = drawCanvas()
    letterExtractorDisplay(canvas)
    drawButtons(canvas, buttonsLE)
    drawSliders(canvas, slidersLE)
    cv2.imshow("Diplomski", canvas)
    key = cv2.waitKey(1) & 0xFF
    keyboardLE(key)


#LETTER RECOGNITION WINDOW
def runRecognize():
    canvas = drawCanvas()
    recognizeDisplay(canvas=canvas)
    drawButtons(canvas, buttonsRL)
    cv2.imshow("Diplomski", canvas)
    cv2.waitKey(1)


#DATA INFO WINDOW
def runDataInfo():
    canvas = drawCanvas()
    dataInfoDisplay(canvas)
    drawButtons(canvas, buttonsDT)
    cv2.imshow("Diplomski", canvas)
    cv2.waitKey(1)


#MAIN MENU DISPLAY
def runMainMenu():
    canvas = drawCanvas()
    mainMenuDisplay(canvas=canvas)
    drawButtons(canvas, buttonsMM)
    cv2.imshow("Diplomski", canvas)
    cv2.waitKey(1)
    




