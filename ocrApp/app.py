#ovaj deo koristim da mi mogao da pokrecem aplikaciju, jer su importi postali problem, bez ovoga ce bacati error da ne moze da nadje folder neuralNetwork
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from runWindows import runLetterExtractor,runMainMenu,runRecognize,runDataInfo
from input import mouseMM,mouseLE,mouseDT,mouseRL
import appState
import cv2
from render import refreshDataInfo



#inicijalizujemo data info da bi mogao odma da display-ujem
refreshDataInfo()

#inicijalizujem mouse input
mouseInput=mouseMM
cv2.namedWindow("Diplomski")
while True:
    cv2.setMouseCallback("Diplomski", mouseInput)
    if appState.runState["menu"]:
        mouseInput=mouseMM
        runMainMenu()
        
    elif appState.runState["letter"]:
        mouseInput=mouseLE
        runLetterExtractor()

    elif appState.runState["data"]:
        mouseInput=mouseDT
        runDataInfo()

    elif appState.runState["recognize"]:
        mouseInput=mouseRL
        runRecognize()
    
    
  
   
