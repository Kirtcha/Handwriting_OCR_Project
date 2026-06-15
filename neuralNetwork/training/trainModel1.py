import torch
from torch import nn
from neuralNetwork.models.model_1 import model_1
from neuralNetwork.dataSet.dataSplit import dataSplitter
from neuralNetwork.dataSet.dataLoader import dataHandler
from neuralNetwork.training.trainingCode import train
from neuralNetwork.confusionMatrix.matrix import evaluate,plotConfusionMatrix




#cepamo data na training i test skupove
dataSplit=dataSplitter(dataSplitPercent=0.2)
dataSplit.run()
print("Splitovali smo slova")

#unosimo data
data=dataHandler(batch=32)
trainLoader=data.trainDataLoader
testLoader=data.testDataLoader
classNames = testLoader.dataset.classes
print("Ucitali smo slova")


classNames = testLoader.dataset.classes
print("KLASE:", classNames)
print("BROJ KLASA:", len(classNames))


#unosimo model
#model 1 ima output shape 27
#model 2 ima output shape 40 (Test Loss: 0.0717 | Test Acc: 0.9811)
#model 3 output shape 27    Test Loss: 0.0794 | Test Acc: 0.9761
#model 4 Test Loss: 0.1333 | Test Acc: 0.9585
#model 5 Test Loss: 0.0868 | Test Acc: 0.9741
model=model_1(inputShape=1,hiddenUnits=10,outputShape=27)
print("Uneli smo model")



#loss i optimizer
lossFn=torch.nn.CrossEntropyLoss()
optimizer=torch.optim.Adam(model.parameters(),lr=0.001)
print("Uneli smo loss i optimizer")

#treniramo model 
results=train(model=model,trainDataLoader=trainLoader,testDataLoader=testLoader,optimizer=optimizer,lossFn=lossFn,epochs=15)
print(results)

testLoss, testAcc, cm = evaluate(
    model=model,
    dataLoader=testLoader,
    lossFn=lossFn,
    classNames=classNames
)

print(f"Test Loss: {testLoss:.4f} | Test Acc: {testAcc:.4f}")
plotConfusionMatrix(cm, classNames)

#Cuvamo model
torch.save(model.state_dict(),"neuralNetwork/savedModels/model_5.pth")
print("Model je sacuvan!")