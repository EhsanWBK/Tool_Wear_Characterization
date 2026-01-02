from sklearn.preprocessing import normalize
from sklearn.svm import SVR
from ultralytics import YOLO

from cv2 import resize, rectangle, putText, addWeighted, cvtColor, COLOR_BGR2GRAY, FONT_HERSHEY_SIMPLEX
from ml.preprocessing import  processSingleImg, processStackPath
from ml.postprocessing import measurementVB, wearCurvePlot

from header import *
from numpy import uint8, ndarray, expand_dims, zeros_like
from keras import models


#  =========================================
#  	     Segmentation Functions		
#  =========================================

def singleFramePred(frame:ndarray, model:models.Model):
    seg, clf = model.predict(processSingleImg(frame=frame))
    maxVB = measurementVB(predMask=seg*255)
    return maxVB, seg, clf

def stackPred(path, nrEdges, model):
    imgDS, batches = processStackPath(path=path)
    wearList, wearMasks, classList = predictDS(ds=imgDS, batches=batches, model=model)
    _,_,wearCurve = wearCurvePlot(wearData=wearList, nrExp=1, trendDeg=10)
    return wearCurve[0]

#  =========================================
#  	     Supporting Functions		
#  =========================================

def predictDS(ds, batches, model:models.Model):
    classList = []; maxWearList = []; predMaskList = []
    for image in ds.take(batches):
        predMask, predClf = model.predict(image, verbose=False)
        maxVB = measurementVB(predMask=predMask*255)
        classList.append(int(predClf[0][0])); maxWearList.append(maxVB); predMaskList.append(predMask*255)
    return maxWearList, predMaskList, classList

def objectDetection(frame:ndarray, model:YOLO):
    results = model(frame)
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0].item()
            cls = int(box.cls[0])
            label = f"{model.names[cls]}: {conf:.2f}"
            
            # Draw rectangle
            rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            putText(frame, label, (x1, y1 - 10), FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame

def eotlPredict(frame:ndarray, thID:str, modelSeg:models.Model, modelEOTL:SVR):
    return

def videoSegmentation(frame:ndarray, model:models.Model):
    ''' Takes in single frame of video stream, model for prediction and desired aspect ratio (latter optional)
    Returns single frame overlayed with image prediction. '''
    frameGrayScaled = cvtColor(frame, COLOR_BGR2GRAY)
    frameDownsized = resize(frameGrayScaled, (512, 512)) # to fit model prediction
    frameNorm = expand_dims(normalize(frameDownsized), 2) # expected shape: (512, 512, 1)
    frameNormExpand = expand_dims(frameNorm, 0) # expected shape: (1, 512, 512, 1): format for model prediction
    predMask = (model.predict(frameNormExpand)[0,:,:,0]>0.2).astype(uint8) # expected shape: (512, 512)
    predMaskUpsize = resize(predMask, (frame.shape[1], frame.shape[0])) # expected shape: (frameHeight, frameWidth)
    redMask = zeros_like(frame) # expected shape: frame.shape
    redMask[predMaskUpsize==1]=[0,0,255]
    overlayFrame = addWeighted(frame, 1.0, redMask, 0.5, 0)
    return overlayFrame
