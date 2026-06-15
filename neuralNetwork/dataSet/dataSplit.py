import os
import random
import shutil



class dataSplitter:
    def  __init__(self,dataSplitPercent=0.2):
       self.dataSplitPercent=dataSplitPercent#20% svih slika idu u test folder, ostatak u training
       random.seed(42)

    def createFolders(self,letterFolderName):
        testPath=os.path.join("Data","testData",letterFolderName)
        trainPath=os.path.join("Data","trainData",letterFolderName)
        if not os.path.exists(testPath):
            os.makedirs(testPath)
        if not os.path.exists(trainPath):
            os.makedirs(trainPath)
        return testPath,trainPath

    def dataSplit(self,LettersInFolder):
        testSample=random.sample(LettersInFolder,int(self.dataSplitPercent*len(LettersInFolder)))
        trainingSample =list(set(LettersInFolder)-set(testSample))
        return testSample,trainingSample
    
    def dataCopy(self,sampleSet,srcPath,dstPath):
        for i,letterName in enumerate(sampleSet):
            name,_=os.path.splitext(letterName)
            letter,_=name.split("_")
            newLetterName=f"{letter}_{i}.png"
            src=os.path.join(srcPath,letterName)
            dst=os.path.join(dstPath,newLetterName)
            shutil.copy(src,dst)

    def clearFolders(self):
        for folder in ["Data/testData","Data/trainData"]:
            if os.path.exists(folder):
                shutil.rmtree(folder)

    def run(self):
        self.clearFolders()
        for letterFolderName in os.listdir("Letters"):
            srcPath=os.path.join("Letters",letterFolderName)
            lettersInFolder=os.listdir(srcPath)
            testSample,trainSample=self.dataSplit(lettersInFolder)
            testPath,trainPath=self.createFolders(letterFolderName)
            self.dataCopy(sampleSet=testSample,
                          srcPath=srcPath,
                          dstPath=testPath)
            self.dataCopy(sampleSet=trainSample,
                          srcPath=srcPath,
                          dstPath=trainPath)



datamaker=dataSplitter(dataSplitPercent=0.2)
datamaker.run()
