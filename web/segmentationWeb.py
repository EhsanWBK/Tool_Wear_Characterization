from header import *
from utensils.generalUtensils import loadCurModel, imageReader, reformatFrame
# SEG_MODEL = models.load_model(join(CWD,'models','predictWear','DanTrainV1.hdf5'))
# EOTL_MODEL = models.load_model()

# ======== segmentation.js ========

@eel.expose()
def loadImage(path: str):
    CURRENT_IMAGE, _ = imageReader(targetPath=path, segment=True) # single file
    saveForPIL = CURRENT_IMAGE[0,:,:,0].astype(uint8)
    print('Loading image from directory (with shape): ', CURRENT_IMAGE.shape, saveForPIL.shape)
    Image.fromarray(saveForPIL).save(join(CWD,'tmp','curImgTmp.jpg'))
    blob = reformatFrame(CURRENT_IMAGE[0])
    eel.updateCanvas1(blob)() # expose picture to HTML interface

@eel.expose()
def saveSegResult(path: str):
    curTimeStr = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    filename = join(path, curTimeStr) + '.jpg'
    frame = imread(SEG_TEMP)
    imwrite(filename, frame)

@eel.expose()
def loadModel(path: str):
    global SEG_MODEL
    SEG_MODEL = loadCurModel(path=path) # expose current model to other functions
