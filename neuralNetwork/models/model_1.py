import torch
from torch import nn



class model_1(nn.Module):

    def __init__(self,inputShape:int,
                 hiddenUnits:int,
                 outputShape:int):
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
      #  x=self.convBlock1(x)
      #  print(x.shape)
       # x=self.convBlock2(x)
       # print(x.shape)
        #x=self.classifier(x)
        #print(x.shape)
        #return x
        #moze se i ovako napisati
        return self.classifier(self.convBlock2(self.convBlock1(x)))