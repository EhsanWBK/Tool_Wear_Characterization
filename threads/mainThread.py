from header import *

from web import server
from web.segmentationWeb import loadImage, loadModel

from threads.robotThread import *
from threads.opcThread import *
from threads.modeltrainThread import *
from threads.segmentationThread import *

# ======== all.js ========

@eel.expose()
def getFile(elementID):
    # HTML Extraction
    path = CWD
    if elementID == 'imageInput': path=SINGLE_DATA_PATH
    if elementID == 'modelDirPath': path=SAVE_MODEL_PATH
    # Tkinter Interface
    root = Tk()
    root.attributes("-topmost", True)
    filename = filedialog.askopenfilename(initialdir=path) # CHANGE TO DATA FILE
    root.destroy()
    # HTML Update
    eel.updateDirectoryName(filename,elementID)()
    if elementID == 'imageInput': loadImage(filename)
    elif elementID == 'modelDirPath': loadModel(filename)
    else: print('Error Loading File.')

@eel.expose()
def getDirectory(elementID):
    path = CWD
    if elementID == 'imageInput' or elementID == 'dataDirectory' or elementID == 'trainingImgDir': path = TRAIN_DATA_PATH
    # if elementID == 'stackData': path = EXP_DATA_PATH
    if elementID =='SaveResultDir': path = SAVE_RES_PATH
    if elementID == 'modelSavingDir': path = SAVE_MODEL_PATH
    root = Tk()
    root.attributes("-topmost", True)
    directory = filedialog.askdirectory(initialdir=path)
    root.destroy()
    eel.updateDirectoryName(directory,elementID)()

@eel.expose()
def windowClosed():
    print('\n----------------------- CLOSING HTML WINDOW -----------------------')
    print('\t- Set HMTL Close Event'); htmlStop.set(); print('\t- HTML can be closed now.')

# ======== Thread Execution ========

def setupThreads():
    print('\n----------------------- STARTING THREADS -----------------------')
    startOPCThread(); sleep(1)
    startSegThread(); sleep(1)
    startRobThread(); sleep(1)
    htmlThread.start(); sleep(1)


def shutdownThreads():
    print('\n----------------------- SHUTTING DOWN PROGRAM -----------------------')
    stopEvent.set()
    shutdownOPCThread()
    shutdownSegThread()
    shutdownRobThread()
    print('\t- Stopped all Threads.')

# ======== HTML Thread ========

htmlStop = Event()
htmlThread = Thread(target=server.startHTML)
