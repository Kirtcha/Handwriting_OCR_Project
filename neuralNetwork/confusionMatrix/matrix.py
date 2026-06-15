from torchmetrics import ConfusionMatrix
from mlxtend.plotting import plot_confusion_matrix
from mlxtend.evaluate import confusion_matrix
from neuralNetwork.training.trainingCode import testStep
import torch
import matplotlib.pyplot as plt

"modifikovane su mi linije trainingCode: 63, 50,44,33"
def evaluate(model, dataLoader, lossFn, classNames):
    testLoss, testAcc, allPreds, allLabels = testStep(model, dataLoader, lossFn)
    cm = confusion_matrix(y_target=allLabels, y_predicted=allPreds)
    return testLoss, testAcc, cm


def plotConfusionMatrix(cm, classNames):
    fig, ax = plot_confusion_matrix(
        conf_mat=cm,
        class_names=classNames,
        show_normed=True,
        colorbar=True
    )
    plt.title("Confusion Matrix")
    plt.savefig("confusion_matrix.png")
    plt.show()