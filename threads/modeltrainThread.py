from threads.headerThread import *

from ml.modelTraining import trainSegModel

WEAR_TYPES = ['crater', 'flank']

@eel.expose()
def trainModel(parDict):
    print('Extracted Parameter Dictionary:\n', parDict)
    wearTypes = getWearTypes(parDict=parDict)
    print('Wear Types :', wearTypes)
    nrImages = int(parDict['nrTrainImages'])
    modelName = str(parDict['modelName'])
    augmentationList = getAugList(parDict=parDict)
    if bool(parDict['unet_arch']):
        trainSegModel(wearTypes=wearTypes, nrImages=nrImages, modelName=modelName, augmentationList=augmentationList, parDict=parDict)


def getWearTypes(parDict):
    wearTypes = []
    if bool(parDict['crater']): wearTypes.append('crater')
    if bool(parDict['flank']): wearTypes.append('flank')
    return wearTypes

def getAugList(parDict):
    AUGMENTATIONS = ['flip_horizontal', 'flip_vertical', 'rotate90', 'brightness', 'contrast']; AUG_LIST = []
    for aug in AUGMENTATIONS:
        if bool(parDict[aug]): 
            if bool(parDict['cropping']): aug = 'crop_' + aug
            AUG_LIST.append(aug)
    return AUG_LIST