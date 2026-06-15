import os
import shutil

class imageLoader:
    def __init__(self):
        self.imageIndex=0

    def importImage(self,path):
        imageList=os.listdir(path)
        if 0<=self.imageIndex<len(imageList):
            imagePath=os.path.join(path,imageList[self.imageIndex])
            return imagePath
        
    def moveImageToUsed(self,path):
        imageList=os.listdir(path)
        src=os.path.join("Images/notUsed",imageList[self.imageIndex])
        dst=os.path.join("Images/Used",imageList[self.imageIndex])
        shutil.move(src,dst)

