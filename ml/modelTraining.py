

import keras
import os

import tensorflow as tf
from sklearn.model_selection import train_test_split
import glob
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

from ml.modelArchitecture import UNet
from ml.preprocessing import processTrainPath, AUTOTUNE, configPerformance, getExpDF

DATA_PATH = os.path.join(os.getcwd(), 'data', 'training')

METRICS = {
    'clf': [keras.metrics.BinaryAccuracy(name='accuracy'), keras.metrics.Precision(name='precision'), keras.metrics.Recall(name='recall')],
    'seg': [keras.metrics.BinaryAccuracy(name='accuracy'), keras.metrics.Precision(name='precision'), keras.metrics.Recall(name='recall'), keras.metrics.MeanIoU(num_classes=2, name="iou")]
}

LOSSES = {
    'clf': keras.losses.BinaryCrossentropy(),  # Binary classification
    'seg': keras.losses.Dice()  # Segmentation
}

LOSS_WEIGHTS = {
    'clf': 1.0,
    'seg': 1.0
}

MONITOR = 'val_loss'
VERBOSE = True

# TRAIN_IMG_PATHS = [os.path.join(DATA_PATH,'images',className,imgName) for className in CLASS_NAMES for imgName in imgNames]


AUGMENTATION = {
    "brightness": lambda img: tf.image.adjust_brightness(img, delta=0.3),
    "contrast": lambda img: tf.image.adjust_contrast(img, 0.5),
    "flip_vertical": lambda img: tf.image.flip_left_right(img),
    "flip_horizontal": lambda img: tf.image.flip_up_down(img),
    "rotate90": lambda img: tf.image.rot90(img),
    "crop": lambda img: tf.image.resize_with_crop_or_pad(img, 2000, 1400),
    "crop_brightness": lambda img: tf.image.adjust_brightness(tf.image.resize_with_crop_or_pad(img, 2000, 1400), delta=0.3),
    "crop_contrast": lambda img: tf.image.adjust_contrast(tf.image.resize_with_crop_or_pad(img, 2000, 1400), 0.5),
    "crop_flip_vertical": lambda img: tf.image.flip_left_right(tf.image.resize_with_crop_or_pad(img, 2000, 1400)),
    "crop_flip_horizontal": lambda img: tf.image.flip_up_down(tf.image.resize_with_crop_or_pad(img, 2000, 1400)),
    "crop_rotate90": lambda img: tf.image.rot90(tf.image.resize_with_crop_or_pad(img, 2000, 1400)),
}

# ======== Model Initialization ========

def createSegModel(inputShape, par) -> keras.Model:
    return UNet.unet_seg_class(inputShape=inputShape)

def createEoTLModel():
    return

# ======== Model Training ========

def trainSegModel(wearTypes, nrImages, modelName, augmentationList, parDict):
    print([os.path.join(DATA_PATH, 'images', className) for className in wearTypes])
    # TRAIN_IMG_PATHS = [os.path.join(DATA_PATH, 'images', className, img_name) for className in wearTypes
    # for img_name in glob.glob(os.path.join(DATA_PATH, 'images', className, '*.jpg'))
    # ]
    TRAIN_IMG_PATHS = [
    img_path
    for className in wearTypes
    for img_path in glob.glob(os.path.join(DATA_PATH, 'images', className, '*.jpg'))
    ]
    print(DATA_PATH)
    print(TRAIN_IMG_PATHS)
    pathTrain, pathTemp = train_test_split(TRAIN_IMG_PATHS, test_size=0.3)
    pathTest, pathVal = train_test_split(pathTemp, test_size=0.5); del(pathTemp)

    orgTrainDS = tf.data.Dataset.from_tensor_slices(pathTrain)
    testDS = tf.data.Dataset.from_tensor_slices(pathTest)
    valDS = tf.data.Dataset.from_tensor_slices(pathVal)

    SIZE = (int(parDict['imageHeight']), int(parDict['imageWidth']))
    CHANNELS = int(parDict['nrChannels'])

    trainDS = orgTrainDS.map(lambda filePath: processTrainPath(filePath, size=SIZE, channels=CHANNELS,classNames=wearTypes), num_parallel_calls=AUTOTUNE)
    for AUG_NAME, transform in augmentationList.items(): 
        augmented = orgTrainDS.map(lambda filePath: processTrainPath(filePath, transform=transform, size=SIZE, channels=CHANNELS,classNames=wearTypes), num_parallel_calls=AUTOTUNE)
        trainDS = trainDS.concatenate(augmented)

    testDS = testDS.map(lambda filePath: processTrainPath(filePath, size=SIZE, channels=CHANNELS,classNames=wearTypes), num_parallel_calls=AUTOTUNE)
    valDS = valDS.map(lambda filePath: processTrainPath(filePath, size=SIZE, channels=CHANNELS,classNames=wearTypes), num_parallel_calls=AUTOTUNE)

    BATCH_SIZE = int(parDict['batchSize'])
    EPOCHS = int(parDict['nrEpochs'])
    PATIENCE = int(parDict['patience'])

    saveModel = os.path.join(os.getcwd(),'model', str(modelName))
    if not os.path.exists(saveModel): os.makedirs(saveModel)

    # Callbacks
    EARLYSTOP = keras.callbacks.EarlyStopping(monitor=MONITOR, patience=PATIENCE, restore_best_weights=True)
    CHECKPOINTS = keras.callbacks.ModelCheckpoint(filepath=os.path.join(saveModel,str(modelName)+'.keras'), monitor=MONITOR, verbose=VERBOSE, save_best_only=True, mode='auto', save_freq='epoch')
    CALLBACKS = [EARLYSTOP, CHECKPOINTS]

    model = UNet.unet_seg_class(imgShape=(512,512,1))
    model.compile(
        optimizer='adam',
        loss=LOSSES,
        loss_weights=LOSS_WEIGHTS,
        metrics=METRICS,
    )

    singleModelTrainDS = configPerformance(trainDS, BATCH_SIZE)
    singleModelTestDS = configPerformance(testDS, BATCH_SIZE)
    singelModelValDS = configPerformance(valDS, BATCH_SIZE)

    history = model.fit(
        x=singleModelTrainDS,
        epochs=EPOCHS,
        validation_data=singelModelValDS, 
        shuffle=True, 
        callbacks=CALLBACKS, 
        verbose=True
    )

    evaluation = model.evaluate(singleModelTestDS, return_dict=True)
    print(evaluation)
    return model, history, evaluation

def trainEoTLModel(expNames):
    dfX, dfY = getExpDF(expNames=expNames)
    xTrain, xTest, yTrain, yTest = train_test_split(dfX,dfY,test_size=0.25,random_state=42)
    scaler = StandardScaler()
    xTrain = scaler.fit_transform(xTrain)
    xTest = scaler.fit_transform(xTest)
    svr = SVR(kernel='rbf',C=300,gamma=0.1, epsilon=0.1)
    svr.fit(xTrain, yTrain)
    yPred = svr.predict(xTest)

    mse = mean_squared_error(yTest, yPred)
    r2 = r2_score(yTest, yPred)

    # # DISPLAY RESULT
    # plt.figure(figsize=(8, 6))
    # plt.scatter(yTest, yPred, color='blue', alpha=0.6)
    # plt.plot([min(yTest), max(yTest)], [min(yTest), max(yTest)], color='red', linestyle='--')  # Ideal Line
    # plt.xlabel("Actual Remaining Cuts")
    # plt.ylabel("Predicted Remaining Cuts")
    # plt.title("Actual vs Predicted Remaining Cuts")
    # plt.grid(True)
    # plt.show()

    return svr, (mse, r2)