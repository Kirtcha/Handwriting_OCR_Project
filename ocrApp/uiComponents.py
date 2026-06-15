import appState

class Button:
    def __init__(self,x1,x2,y1,y2,text,action,isButton=True):
        self.x1=x1
        self.x2=x2
        self.y1=y1
        self.y2=y2
        self.text=text
        self.action=action
        self.isButton=isButton

        self.pressed=False
        self.toggle=False

    #da li je mis na buttonu
    def isHovering(self,x,y):
        return self.x1<x<self.x2 and self.y1<y<self.y2
    
class Slider:
    def __init__(self,x1,x2,y,percentage,text,action):
        self.x1=x1
        self.x2=x2
        self.y=y
        self.text=text
        self.percentage=percentage
        self.action=action
        
        self.pressed=False

    def isHovering(self,x,y):
        return self.x1<x<self.x2 and self.y-5<y<self.y+5
     
        
    def update(self,x):
        x = max(self.x1, min(x, self.x2))
        self.percentage = int((x - self.x1) / (self.x2 - self.x1) * 100)
    

#LETTER EXTRACTOR KOMPONENTE   
#grupa button-a koji se odma crtaju
buttonsLE = [Button(x1=765, x2=935, y1=205, y2=245, text="black & white", action="thresh"),
            Button(x1=765, x2=935, y1=255, y2=295, text="contours", action="contours"),
            Button(x1=765, x2=935, y1=305, y2=345, text=None, action="info",isButton=False),
            Button(x1=765, x2=935, y1=355, y2=395, text=None, action="save"),
            Button(x1=765, x2=847, y1=405, y2=445, text="back", action="back"),
            Button(x1=853, x2=935, y1=405, y2=445, text="next", action="next"),
            Button(x1=765, x2=935, y1=455, y2=495, text="image done", action="move"),
            Button(x1=930, x2=970, y1=700, y2=785, text=None, action="reset"),
            Button(x1=765, x2=935, y1=105, y2=145, text="Main Menu", action="menu")]

#grupa button-a koji se crtaju pri odredjenim uslovima (prebacuju se u buttons)
buttonStorageLE=[Button(x1=910, x2=935, y1=355, y2=375, text="Yes", action="yes"),
               Button(x1=910, x2=935, y1=375, y2=395, text="No", action="no"),
               Button(x1=765,x2=910,y1=355,y2=395,text=None,action="input",isButton=False)]


slidersLE=[Slider(50, 450, 725, int(100*(appState.worker.blurKernel-1)/30), "Blur Amount",action="blur"),
        Slider(50, 450, 760, int(100*appState.worker.sigma/10), "Smoothness",action="sigma"),
        Slider(500, 900, 725, int(100*(appState.worker.blockSize-3)/48), "Detection Area",action="block"),
        Slider(500, 900, 760, int(100*(appState.worker.c+20)/40), "Contrast",action="c")]

#MAIN MENU KOMPONENTE
buttonsMM=[Button(x1=750, x2=950, y1=225, y2=275, text="Recognize Letters", action="recognize"),
           Button(x1=750, x2=950, y1=350, y2=400, text="Letter Extractor", action="extractor"),
           Button(x1=750, x2=950, y1=475, y2=525, text="Data info", action="data")]

#DATA KOMPONENTE
buttonsDT=[Button(x1=765, x2=935, y1=105, y2=145, text="Main Menu", action="menu"),
           Button(x1=765, x2=935, y1=155, y2=195, text=None, action="sort"),
           Button(x1=765, x2=935, y1=205, y2=245, text=None, action="sampleInfo",isButton=False),
           Button(x1=765, x2=935, y1=255, y2=295, text=None, action="totalSample",isButton=False)]

#RECOGNIZE  KOMPONENTE
buttonsRL=[Button(x1=765, x2=935, y1=105, y2=145, text="Main Menu", action="menu"),
           Button(x1=765, x2=935, y1=205, y2=245, text="black & white", action="thresh"),
           Button(x1=765, x2=935, y1=255, y2=295, text="contours", action="contours"),
           Button(x1=765, x2=935, y1=305, y2=345, text="Select an image", action="select"),
           Button(x1=765, x2=935, y1=355, y2=395, text="Recognize text", action="recognize"),
           Button(x1=765, x2=935, y1=405, y2=445, text="Confidence score", action="confidence")]

buttonStorageRL=[Button(x1=765, x2=935, y1=205, y2=245, text="Back", action="back"),]
