from imageLoader import imageLoader
from imageWork import imageWork
from ui import userInterface

loader = imageLoader()
worker = imageWork()
ui = userInterface(loader, worker)

ui.display()