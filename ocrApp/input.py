import appState
import cv2
from actionHandler import buttonActionHandlerLE,sliderActionHandlerLE,selectContours,buttonActionHandlerMM,buttonActionHandlerDT,buttonActionHandlerRL
from uiComponents import buttonsLE,buttonStorageLE,slidersLE,buttonsMM,buttonsDT,buttonsRL
from imageSaver import saveLetter
from render import refreshDataInfo

#LETTER EXTRACTOR INPUTI

def mouseLE(event,x,y,flags,params):
    #KLIK DOLE
    if event==cv2.EVENT_LBUTTONDOWN:
        #za selekciju kontura
        if 0 <= x < 700 and 0 <= y < 700:
            appState.dragging=True
            appState.dragStart=(x,y)
            appState.dragEnd=(x,y)
        #za buttone
        for button in buttonsLE:
            if button.isHovering(x,y):
                button.pressed=True
                print(f"Clicked on {button.text}")
        #za slidere
        for slider in slidersLE:
            if slider.isHovering(x,y):
                slider.pressed=True
    #KLIK GORE
    elif event==cv2.EVENT_LBUTTONUP:
        #za selekciju kontura
        appState.dragging=False
        if appState.dragStart is not None and appState.dragEnd is not None:
            selectContours(appState.dragStart, appState.dragEnd)
            appState.dragging = False
            appState.dragStart = None
            appState.dragEnd = None
        #za buttone
        for button in buttonsLE:
            #if button.isHovering(x,y) and button.pressed:
            if button.pressed:
                buttonActionHandlerLE(button=button)
                button.pressed=False
                if button.action=="thresh" or button.action=="contours":
                    button.toggle=not button.toggle
        #za slidere
        for slider in slidersLE:
            if slider.pressed:
                slider.pressed=False
    #DRZANJE DUGMETA
    elif event == cv2.EVENT_MOUSEMOVE:
        #za selekciju kontura
        if appState.dragging==True:
            appState.dragEnd=(x,y)
        #za slidere
        for slider in slidersLE:
            if slider.pressed:
                slider.update(x)
                sliderActionHandlerLE(slider=slider)


def keyboardLE(key):
        srp_latin_map = {
            200: 'Č', 198: 'Ć', 208: 'Đ', 138: 'Š', 142: 'Ž',
            232: 'č', 230: 'ć', 240: 'đ', 154: 'š', 158: 'ž'}
        #ovaj deo je dodat da se ne bi ispisivala 3 slova odjednom (jer proveravamo 3 button-a)
        input_active = any(b.action in ("yes", "no", "input") for b in buttonsLE)
        if not input_active:
            return
        #normalna tastatura
        if 65 <= key <= 90 or 97 <= key <= 122:
            appState.letterName += chr(key)
        #srpska slova
        elif key in srp_latin_map:
            appState.letterName += srp_latin_map[key]
        #delete
        elif key == 8:
            appState.letterName = appState.letterName[:-1]
        #enter
        elif key == 13 and appState.letterName != "":
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
        #escape
        elif key == 27:
            for button in buttonsLE[:]:
                if button.action in ("yes", "no", "input"):
                    buttonStorageLE.append(button)
                    buttonsLE.remove(button)
            for button in buttonStorageLE[:]:
                if button.action == "save":
                    buttonsLE.append(button)
                    buttonStorageLE.remove(button)
            appState.letterName = ""


#MAIN MENU INPUTI
def mouseMM(event,x,y,flags,params):

    #KLIK DOLE
    if event==cv2.EVENT_LBUTTONDOWN:
        #za buttone
        for button in buttonsMM:
            if button.isHovering(x,y):
                button.pressed=True
                print(f"Clicked on {button.text}")

    #KLIK GORE
    elif event==cv2.EVENT_LBUTTONUP:
        #za buttone
        for button in buttonsMM:
            if button.pressed:
                buttonActionHandlerMM(button=button)
                button.pressed=False




#DATA  INPUTI
def mouseDT(event,x,y,flags,params):

    #KLIK DOLE
    if event==cv2.EVENT_LBUTTONDOWN:
        #za buttone
        for button in buttonsDT:
            if button.isHovering(x,y):
                button.pressed=True
                print(f"Clicked on {button.text}")

    #KLIK GORE
    elif event==cv2.EVENT_LBUTTONUP:
        #za buttone
        for button in buttonsDT:
            if button.pressed:
                buttonActionHandlerDT(button=button)
                button.pressed=False


            
#RECOGNIZE  INPUTI
def mouseRL(event,x,y,flags,params):

    #KLIK DOLE
    if event==cv2.EVENT_LBUTTONDOWN:
        #za buttone
        for button in buttonsRL:
            if button.isHovering(x,y):
                button.pressed=True
                print(f"Clicked on {button.text}")

    #KLIK GORE
    elif event==cv2.EVENT_LBUTTONUP:
        #za buttone
        for button in buttonsRL:
            if button.pressed:
                buttonActionHandlerRL(button=button)
                button.pressed=False
                if button.action=="thresh" or button.action=="contours":
                    button.toggle=not button.toggle
            
            
                