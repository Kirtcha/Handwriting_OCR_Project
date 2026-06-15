import torch 
from torch import nn
from tqdm.auto import tqdm
import numpy as np

def trainStep(model: torch.nn.Module,dataLoader: torch.utils.data.DataLoader,lossFn:torch.nn.Module,optimizer:torch.optim.Optimizer):
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

def testStep(model:torch.nn.Module,dataLoader:torch.utils.data.DataLoader,lossFn:torch.nn.Module):
    model.eval()
    testLoss,testAcc=0,0
    allPreds=[]
    allLabels=[]#dodato za confusion matrix
    with torch.inference_mode():
        for batch,(X,y) in enumerate(dataLoader):
            testPredLogits=model(X)
            loss=lossFn(testPredLogits,y)
            testLoss+=loss.item()
            testPredLabels=testPredLogits.argmax(dim=1)
            testAcc+=((testPredLabels==y).sum().item()/len(testPredLabels))

            #dodato za confusion matrix
            allPreds.append(testPredLabels)
            allLabels.append(y)


        testLoss=testLoss/len(dataLoader)
        testAcc=testAcc/len(dataLoader)
        #dodato za confusion matrix
        allPreds=torch.cat(allPreds).numpy()
        allLabels=torch.cat(allLabels).numpy()
        return testLoss,testAcc,allPreds,allLabels
    
    #pravimo fju koja kombinuje prethodne dve

def train(model:torch.nn.Module,trainDataLoader:torch.utils.data.DataLoader,testDataLoader:torch.utils.data.DataLoader,optimizer: torch.optim.Optimizer,lossFn:torch.nn.Module=nn.CrossEntropyLoss(),epochs:int=5):
        
    results={"Train loss":[],"Train acc":[],"Test loss":[],"Test acc":[]}
        
    for epoch in tqdm(range(epochs)):
        trainLoss,trainAcc=trainStep(model=model,dataLoader=trainDataLoader,lossFn=lossFn,optimizer=optimizer)
        testLoss,testAcc,_,_=testStep(model=model,dataLoader=testDataLoader,lossFn=lossFn)#dodao _ , _ zbog matrice
        results["Train loss"].append(trainLoss)
        results["Train acc"].append(trainAcc)
        results["Test loss"].append(testLoss)
        results["Test acc"].append(testAcc)
    return results