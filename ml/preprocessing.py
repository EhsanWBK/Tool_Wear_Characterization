from numpy import ndarray
from cv2 import imread

import os
import tensorflow as tf
import numpy as np
import sqlite3 as sql
import pandas as pd
import glob
from keras import models
from ml.postprocessing import measurementVB
from data.dbCon import returnRange
from data.dbHeader import CONN_IMG_DB, CONN_TH

BEST_MODEL_PATH = ''
IMG_HEIGHT = 2448
IMG_WIDTH = 2048
AUTOTUNE = tf.data.AUTOTUNE

#  =========================================
#  	     Pipeline Pre-Processing 		
#  =========================================

def processTrainPath(directory, filePath, size: tuple = (512, 512), transform = None, classNames: list = ['crater', 'flank'], channels: int = 1):
    # Load the raw data from the file as a string
    normPath = tf.strings.regex_replace(filePath, r"\\", "/")
    imgName = tf.strings.split(
        tf.strings.split(normPath, sep="/")[-1],
        ".")[0]
    label = tf.strings.split(normPath, sep="/")[-2]
    maskPath = os.path.join(directory, 'masks', label, imgName+'.tif')

    img = tf.io.read_file(normPath)
    img = tf.io.decode_jpeg(img, channels=channels) # channels
    if transform: img = transform(img)
    img = tf.image.resize(img, size); img = img / 255.0

    mask = tf.numpy_function(parseWithCV2, [maskPath], Tout=tf.float32)
    mask.set_shape([IMG_HEIGHT, IMG_WIDTH, 1])
    if transform: mask = transform(mask)
    mask = tf.image.resize(mask, size); mask = mask / 255.0
    mask = tf.cast(mask > 0.5, dtype=tf.dtypes.uint8)

    one_hot = label == classNames; labelID = tf.argmax(one_hot)
    return img, (mask, labelID)

def processSingleImg(frame: ndarray, imgSize = (512,512)):
    imgTensor = tf.convert_to_tensor(frame, dtype=tf.float32)
    imgTensor = tf.image.resize(imgTensor, imgSize)
    imgTensor = imgTensor/255.0
    imgTensor = tf.expand_dims(imgTensor, axis=0)
    return imgTensor

def processStackPath(path):
    pathList = []
    imgPaths = [path for path in glob.glob(f"{path}/**/*", recursive=True)]
    pathList.extend(imgPaths)
    testDS, batches = processImgStack(filePath=pathList)
    return testDS, batches

#  =========================================
#  	     Supporting Functions		
#  =========================================

def parseWithCV2(imgPath):
    mask = imread(imgPath.decode('UTF-8'), -1)
    mask = np.expand_dims(mask,2)
    mask = mask.astype(np.dtypes.Float32DType)
    return mask

def configPerformance(ds, batchSize:int  = 1):
    ds = ds.cache()
    # ds = ds.shuffle(buffer_size=1000)
    ds = ds.batch(batchSize)
    ds = ds.prefetch(buffer_size=AUTOTUNE)
    return ds

def processPath(filePath, size: tuple = (512, 512), transform = None, classNames: list = ['crater', 'flank'], channels: int = 3):
    # Load the raw data from the file as a string
    img = tf.io.read_file(filePath)
    img = tf.io.decode_jpeg(img)
    img = tf.image.resize(img, size)
    img = img /255.0
    return img

def processImgStack(filePath, size: tuple = (512, 512), transform = None, classNames: list = ['crater', 'flank'], channels: int = 1):
    normPath = tf.strings.regex_replace(filePath, r"\\", "/")
    test_ds = tf.data.Dataset.from_tensor_slices(normPath)
    test_ds = test_ds.map(lambda file_path: processPath(file_path), num_parallel_calls=AUTOTUNE)
    test_ds = configPerformance(test_ds)
    num_batches = test_ds.cardinality().numpy()
    return test_ds, num_batches

#  =========================================
#  	     EoTL Pre-Processing Steps		
#  =========================================

def prepareEoTL(model, expFolder: str = os.path.join(os.getcwd(),'data','experiment'), dbName: str = 'imageDatabase.db', expName: str = 'WKZ1', df=None):
    conn = sql.connect(dbName); cursor = conn.cursor()
    cursor.execute('''
        SELECT imgName, nrCuts FROM segExperiment WHERE expName = ? ORDER BY nrCuts
    ''', (expName,))
    targetFolder = os.path.join(expFolder, expName)
    records = cursor.fetchall(); conn.close()
    print(records)
    test_img_paths = [path for path in glob.glob(f"{targetFolder}/**/*", recursive=True)]
    test_ds = tf.data.Dataset.from_tensor_slices(test_img_paths)
    test_ds = test_ds.map(lambda file_path: processPath(file_path), num_parallel_calls=AUTOTUNE)
    test_ds = configPerformance(test_ds)
    num_batches = test_ds.cardinality().numpy()
    cuts_numbers = []; maxWearList = []; classList = []
    for image in test_ds.take(num_batches):
        pred_mask, pred_cls = model.predict(image, verbose=False)
        maxVB = measurementVB(frame=pred_mask*255) #if pred_cls == 1 else 0
        classList.append(int(pred_cls[0][0]))
        maxWearList.append(maxVB)
    df = pd.DataFrame({'wearType':classList, 'wearMax': maxWearList})

def getExpDF(expNames, model = None):
    if model == None: model = models.load_model(BEST_MODEL_PATH)
    dfConnectList, dfDiffList = [], []
    for name in expNames:
        df = returnRange(conn=CONN_IMG_DB, tableName='segExperiment',key='expName', values=[name])
        dfNew = prepareEoTL(model=model, expName=name)
        dfConnect = pd.concat([df,dfNew],axis=1)
        dfSelect = dfConnect[['nrCuts', 'nrCutsTot']]
        dfConnect.drop(columns=['nrCuts', 'nrCutsTot'], inplace=True)
        dfDiff = pd.DataFrame({'cutRemain': dfSelect['nrCutsTot'] - dfSelect['nrCuts']})
        dfDiffList.append(dfDiff)

        # Connect to TH
        dfExp = returnRange(conn=CONN_TH, tableName='experiment',key='nameExp',values=[name])
        toolVal = str(dfExp['toolID'][0]); wpVal = str(dfExp['workpieceID'][0]); procVal = str(dfExp['processID'][0])
        dfTool = returnRange(conn=CONN_TH, tableName='tool',key='refNr',values=[toolVal])
        # dfWP = returnRange(conn=connTH, tableName='workpiece',key='refNr',values=[wpVal])
        dfProc = returnRange(conn=CONN_TH, tableName='process',key='refNr',values=['2'])

        # Data Cleaning
        dfTool.drop(columns=['toolName'], inplace=True)
        dfTool.drop(columns=['coatMat'], inplace=True)
        dfTool.drop(columns=['toolMat'], inplace=True)

        dfProc.drop(columns=['refNr'], inplace=True)

        for col in dfTool.columns: dfConnect[col] = dfTool[col][0]
        for col in dfProc.columns: dfConnect[col] = dfProc[col][0]

        # Data Cleaning
        dfConnect.drop(columns=['imgName'], inplace=True)
        dfConnect.drop(columns=['expDate'], inplace=True)
        dfConnect.drop(columns=['expName'], inplace=True)
        dfConnectList.append(dfConnect)
    return dfConnectList, dfDiffList

def prepareSingelEOTL():
    return