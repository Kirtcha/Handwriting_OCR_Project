import os 
import cv2
from imageWork import imageWork


def saveLetter(contourData,letterName):
    for item in contourData:
        if item["Flag"]==False:
        # Folder Letters u kome se nalaze folderi za svako slovo
            mainFolder = "Letters"
            if not os.path.exists(mainFolder):
                os.makedirs(mainFolder)
            #posto ne moze da postoje folderi a i A onda moram kopirati ime za folder i modifikovati ga tako da postoje veliko i malo a
            if letterName.isupper():
                letterFolderName=f"{letterName}_upper"
            else:
                letterFolderName=f"{letterName}_lower"
            letterFolder=os.path.join(mainFolder,letterFolderName)
            if not os.path.exists(letterFolder):
                os.makedirs(letterFolder)
            # Kreiramo naziv fajla koji se automatski povećava
            letterNumber = len(os.listdir(letterFolder))  # broj fajlova u folderu
            letterPath = os.path.join(letterFolder, f"{letterName}_{letterNumber}.png")
            #Augmentujemo slovo pre cuvanja
            worker=imageWork()
            augmentedLetter=worker.augmentLetters(item["Letter"])
            # Čuvamo slovo
            cv2.imencode('.png', augmentedLetter)[1].tofile(letterPath)#Uzeto sa Claude-a, obicna save linija ne radi zbog srpskih karaktera a ovako radi
            #cv2.imwrite(letterPath, letter["Letter"])