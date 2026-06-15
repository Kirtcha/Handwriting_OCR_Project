import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from PIL import Image


class dataHandler:
    def __init__(self,batch=32):
        self.batch=batch
        self.testPath="Data/testData"
        self.trainPath="Data/trainData"
        testData=self.dataToTensor(self.testPath)
        trainData=self.dataToTensor(self.trainPath)
        self.testDataLoader=self.tensorLoader(testData,shuffle=False)
        self.trainDataLoader=self.tensorLoader(trainData,shuffle=True)

    def dataToTensor(self,path):
        transformToTensor=transforms.Compose([transforms.Grayscale(num_output_channels=1),
                                              transforms.RandomRotation(degrees=10),
                                              transforms.RandomAffine(degrees=0,translate=(0.1,0.1)),
                                              transforms.ToTensor()])
        tensorData=datasets.ImageFolder(root=path,transform=transformToTensor)
        return tensorData
    
    def tensorLoader(self,data,shuffle):
        sampleLoader=DataLoader(dataset=data,batch_size=self.batch,shuffle=shuffle)
        return sampleLoader





"""
dataTransform= transforms.Compose([
    transforms.ToTensor()
])

img=Image.open("Data_Samples/Test_data/a_lower/a_0.png")

#print(dataTransform(img).shape)
#print(dataTransform(img).dtype)

trainData=datasets.ImageFolder(
    root="Data_Samples/Training_data",
    transform=dataTransform,
    #target_transform=None)
)

testData=datasets.ImageFolder(
    root="Data_Samples/Test_data",
    transform=dataTransform,
    #target_transform=None)
)

#print(trainData.samples)
#image=trainData[0][0]
#print(image.shape)
#img_per=image.permute(1,2,0)
#print(img_per.shape)

trainDataLoader=DataLoader(dataset=trainData,
                           batch_size=1,
                           shuffle=True)

testDataLoader=DataLoader(dataset=testData,
                          batch_size=1,
                          shuffle=False)

#print(len(trainDataLoader))
image,label=next(iter(trainDataLoader))
"""
#22:44:34 sam stao
#napravi klasu ili sta god za ovo sranje ovde i rokaj dalje