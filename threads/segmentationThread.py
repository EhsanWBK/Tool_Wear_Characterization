from threads.opcThread import *
from threads.headerThread import *
from web.segmentationWeb import *

import threads.opcThread as opc

from utensils.generalUtensils import reformatFrame, saveTrigger
from ml.segmentation import videoSegmentation, singleFramePred, stackPred

TRIGGER_MODE = False

# ======== segmentation.js ========

@eel.expose()
def videoFeed():
    ''' Enable Camera and stream image to Canvas 1. '''
    if baumerSegStart.set():baumerSegStart.clear()
    else: baumerSegStart.set()

@eel.expose()
def segmentVideo():
    ''' Enable Camera and stream wear segmentation to Canvas 2. '''
    if not segmentStop.is_set(): print('\nStarting Video Segmentation.'); segmentStop.set()  
    else: print('\nStopping Video Segmentation.'); segmentStop.clear()

@eel.expose()
def stopVideo():
    if baumerSegStart.is_set(): baumerSegStart.clear()
    if segmentStop.is_set(): segmentStop.clear()
    else: print('No Video Stream to be stopped.')

@eel.expose()
def setTrigger():
    global TRIGGER_MODE
    if TRIGGER_MODE: 
        print('Stopping Trigger'); opc.cameraClient.setTriggerMode(off=True); TRIGGER_MODE=False; segmentStop.clear()
    else: print('Start Trigger'); opc.cameraClient.setTriggerMode(on=True); TRIGGER_MODE=True; segmentStop.set()

@eel.expose()
def takePicture():
    baumerSegStart.clear(); print('Cleared Video Event.')
    Image.fromarray(opc.STREAM_FRAME).save(join(CWD,'tmp','curImgTmp.jpg'))
    blob = reformatFrame(frame=opc.STREAM_FRAME)
    eel.updateCanvas1(blob)()

@eel.expose()
def segmentImage():
    global SEG_TEMP
    CURRENT_IMAGE = array(Image.open(join(CWD,'tmp','curImgTmp.jpg')).convert('RGB'))
    print(CURRENT_IMAGE.shape)
    VB_MAX_TEMP, SEG_TEMP, CLF_TEMP = singleFramePred(frame=CURRENT_IMAGE, model=SEG_MODEL)
    saveForPIL = SEG_TEMP[0,:,:,0].astype(uint8)
    Image.fromarray(saveForPIL).save(join(CWD,'tmp','segResTmp.jpg'))
    wearPar = {'maxVB':VB_MAX_TEMP, 'wearType':WEAR_TYPE_LIST[int(CLF_TEMP)]}
    blob = reformatFrame(SEG_TEMP, wearPar=wearPar,orgImg=CURRENT_IMAGE)
    eel.updateCanvas2(blob)()

@eel.expose()
def segmentStack(pathProj, nrEdges):
    print('Segmenting Data Stack.')
    wearCurve = stackPred(path=pathProj, nrEdges=nrEdges, model=SEG_MODEL)
    wearCurve = array(Image.open(join(CWD,'tmp','wearCurveTmp.jpg')).convert('RGB'))
    blob = reformatFrame(wearCurve, wearCurve=True, wearFrame=False)
    eel.updateCanvas2(blob)()

# ======== Thread Execution ========

def baumerStreamStart(event, stopEvent):
    print('\t- Baumer Video Stream Thread Set Up.')
    while not stopEvent.is_set():
        event.wait()
        if stopEvent.is_set(): return
        while event.is_set() and not stopEvent.is_set(): # to stop stream: call videoEvent.clear() outside of this function
            blob = reformatFrame(frame=opc.STREAM_FRAME)
            eel.updateCanvas1(blob)()
        print('Stopped Streaming Data.')
        event.clear()

def segmentationStreamStart(event, stopEvent):
    print('\t- Segmentation Stream Thread Set Up.')
    while not stopEvent.is_set():
        event.wait()
        if stopEvent.is_set(): return
        while event.is_set() and not stopEvent.is_set(): # to stop stream: call videoEvent.clear() outside of this function
            if TRIGGER_MODE:
                try:
                    for buffer in opc.TRIGGER_TEMP:
                        print('TRIGGER BUFFER: ', len(opc.TRIGGER_TEMP))
                        VB_MAX_TEMP, mask, CLF_TEMP = singleFramePred(frame=buffer,model=SEG_MODEL)
                        wearPar = {'maxVB':VB_MAX_TEMP, 'wearType':WEAR_TYPE_LIST[int(CLF_TEMP)]}
                        blob = reformatFrame(mask,wearPar=wearPar,orgImg=buffer)
                        eel.updateCanvas2(blob)()
                except: pass
            else:
                print('Video Segmenting')
                frame = videoSegmentation(frame=opc.STREAM_FRAME, model=SEG_MODEL)
                blob = reformatFrame(frame=frame)
                eel.updateCanvas2(blob)()   
        
        print('Stopped Streaming Data.')
        event.clear()

# ======== Events ========

baumerSegStart = opc.Event()
segmentStop = opc.Event()
picture = opc.Event()

# ======== Threads ========

baumerStreamThread = opc.Thread(target=baumerStreamStart, args=(baumerSegStart, opc.stopEvent))
segmentStreamThread = opc.Thread(target=segmentationStreamStart, args=(segmentStop, opc.stopEvent))

def startSegThread():
    print('\t- Starting Segmentation Thread.')
    baumerStreamThread.start(); sleep(1)
    segmentStreamThread.start(); sleep(1)

def shutdownSegThread():
    print('\t- Shutting Down Segmentation Thread.')
    stopEvent.set()
    baumerSegStart.set(); baumerSegStart.clear()
    segmentStop.set(); segmentStop.clear()
    picture.set(); picture.clear()
    baumerStreamThread.join(timeout=1); segmentStreamThread.join(timeout=1)