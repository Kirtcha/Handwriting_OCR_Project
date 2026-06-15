
import torch 
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from PIL import Image



dataTransform= transforms.Compose([
    transforms.ToTensor()
])


trainData=datasets.ImageFolder(
    root="Data/trainData",
    transform=dataTransform,)

trainDataLoader=DataLoader(dataset=trainData,
                           batch_size=32,
                           shuffle=True)


testData=datasets.ImageFolder(
    root="Data/testData",
    transform=dataTransform,)

testDataLoader=DataLoader(dataset=testData,
                          batch_size=32,
                          shuffle=False)


image,label=next(iter(trainDataLoader))

#radimo tiny vgg arhitekturu, idi na cnn explainer sajt

class tinyVGG(nn.Module):

    def __init__(self,inputShape:int,
                 hiddenUnits:int,
                 outputShape:int)->None:
        super().__init__()

        self.convBlock1=nn.Sequential(
            nn.Conv2d(in_channels=inputShape,
                      out_channels=hiddenUnits,
                      kernel_size=3,
                      stride=1,
                      padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=hiddenUnits,
                      out_channels=hiddenUnits,
                      kernel_size=3,
                      stride=1,
                      padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2,
                         stride=2)
        )

        self.convBlock2=nn.Sequential(
            nn.Conv2d(in_channels=hiddenUnits,
                      out_channels=hiddenUnits,
                      kernel_size=3,
                      stride=1,
                      padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=hiddenUnits,
                      out_channels=hiddenUnits,
                      kernel_size=3,
                      stride=1,
                      padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2,
                         stride=2)
        )

        self.classifier=nn.Sequential(
            nn.Flatten(),
            nn.Linear(in_features=hiddenUnits*7*7,
                      out_features=outputShape)
            
        )

    def forward(self,x):
        x=self.convBlock1(x)
        print(x.shape)
        x=self.convBlock2(x)
        print(x.shape)
        x=self.classifier(x)
        print(x.shape)
        return x
        #moze se i ovako napisati
        #return self.classifier(self.convBlock2(self.convBlock1(x)))

torch.manual_seed(42)
model_0=tinyVGG(inputShape=3,
               hiddenUnits=10,
               #na output stavljas da ima izlaza koliko imas i slova (classes)
               outputShape=3)

imageBatch,labelBatch=next(iter(trainDataLoader))
print(imageBatch.shape, labelBatch.shape)

model_0(imageBatch)
print(model_0)

#23:11 sam stao

#sada radimo trening

def trainStep(model: torch.nn.Module,
              dataLoader: torch.utils.data.DataLoader,
              lossFn:torch.nn.Module,
              optimizer:torch.optim.Optimizer):
    model.train()
    trainLoss,trainAcc=0,0
    for batch, (X,y) in enumerate(dataLoader):
        #forward pass
        yPred=model(X)
        #calculate the loss
        loss=lossFn(yPred,y)
        trainLoss+=loss.item()
        #optimizer zero grad
        optimizer.zero_grad()
        #loss backward
        loss.backward()
        #optimizer step
        optimizer.step()
        #calculate acc
        yPredClass=torch.argmax(torch.softmax(yPred,dim=1),dim=1)
        trainAcc+=(yPredClass==y).sum().item()/len(yPred)

    #adjust metrics to get the avarage loss and acc per batch
    trainLoss=trainLoss/len(dataLoader)
    trainAcc=trainAcc/len(dataLoader)
    return trainLoss,trainAcc

def testStep(model:torch.nn.Module,
             dataLoader:torch.utils.data.DataLoader,
             lossFn:torch.nn.Module):
    model.eval()
    testLoss,testAcc=0,0
    with torch.inference_mode():
        for batch,(X,y) in enumerate(dataLoader):
            testPredLogits=model(X)
            loss=lossFn(testPredLogits,y)
            testLoss+=loss.item()
            testPredLabels=testPredLogits.argmax(dim=1)
            testAcc+=((testPredLabels==y).sum().item()/len(testPredLabels))

        testLoss=testLoss/len(dataLoader)
        testAcc=testAcc/len(dataLoader)
        return testLoss,testAcc
    
    #pravimo fju koja kombinuje prethodne dve

def train(model:torch.nn.Module,
            trainDataLoader:torch.utils.data.DataLoader,
            testDataLoader:torch.utils.data.DataLoader,
            optimizer: torch.optim.Optimizer,
            lossFn:torch.nn.Module=nn.CrossEntropyLoss(),
            epochs:int=5):
        
    results={"Train loss":[],
                "Train acc":[],
                "Test loss":[],
                "Test acc":[]}
        
    for epoch in range(epochs):
        trainLoss,trainAcc=trainStep(model=model,
                                        dataLoader=trainDataLoader,
                                        lossFn=lossFn,
                                        optimizer=optimizer)
        testLoss,testAcc=testStep(model=model,
                                    dataLoader=testDataLoader,
                                    lossFn=lossFn)
        results["Train loss"].append(trainLoss)
        results["Train acc"].append(trainAcc)
        results["Test loss"].append(testLoss)
        results["Test acc"].append(testAcc)
    return results
    
#train and evaluate model

EPOCHS=5
model_0=tinyVGG(inputShape=3,
               hiddenUnits=10,
               #na output stavljas da ima izlaza koliko imas i slova (classes)
               outputShape=3)
#set up loss and optimizer
lossFn=nn.CrossEntropyLoss()
optimizer=torch.optim.Adam(params=model_0.parameters(),
                           lr=0.001)
model_0_results=train(model=model_0,
                      trainDataLoader=trainDataLoader,
                      testDataLoader=testDataLoader,
                      optimizer=optimizer,
                      lossFn=lossFn,
                      epochs=EPOCHS)
#sad rokaj sine

