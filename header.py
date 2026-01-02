# from os import getcwd, chdir, makedirs, listdir, remove, mkdir
from os import *
# from os.path import join, dirname, exists, isfile, isdir, splitext
from os.path import *
import sqlite3 as sql
from tkinter import Tk, filedialog

from numpy import *
from cv2 import imread, imwrite, imencode, resize, INTER_LINEAR, rectangle, line, putText, FONT_HERSHEY_SIMPLEX, LINE_AA
from datetime import datetime
from base64 import b64encode

from PIL import Image
from tqdm import tqdm

import eel



from time import sleep, time

import matplotlib.pyplot as plt

from keras import models
from ultralytics import YOLO
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split

chdir(dirname(getcwd())) # move out of 'code' directory

# ======== Path Constants ========

CWD = join(getcwd(),'06_Main_Code') # path to current directory
REFERENCE_FOLDER = 'img'
IMAGE_LOAD_PATH = join(CWD,'data','experiment') # source images
MASK_LOAD_PATH = 'masks' # source masks
SINGLE_DATA_PATH = join(CWD,'data','experiment')
EXP_DATA_PATH = join(CWD,'data','experiment') 
TRAIN_DATA_PATH = join(CWD, 'projects')
TRIGGER_PATH = join(CWD, join(getcwd(), 'projects','trigger'))
SAVE_MODEL_PATH = join(CWD, 'models','predictWear')
SAVE_RES_PATH = join(CWD, 'results')
QR_SAVE_PATH = join(CWD,'docs','qrcodes')
PRED_WEAR_MODEL_PATH = join(CWD, 'models', 'predictWear')
PRED_TL_MODEL_PATH = join(CWD, 'models', 'predictTL')

SEG_TEMP = join(CWD, 'tmp','segTmp.jpg')

ROB_IMG_TEMP = join(CWD,'tmp','robotImg')
ROB_SEG_IMG = join(CWD,'results','robotSeg')

# ======== Data Containers ========

IMG_DATA = []
MASK_DATA = []
VAL_DATA = []

# ======== Threading Setup ========

IMG_SHAPE = (2048, 2448, 3)
IMG_ARRAY = zeros(IMG_SHAPE, dtype=uint8)

WEBCAM_SHAPE = (480,640,3)
WEBCAM_ARRAY = zeros(WEBCAM_SHAPE, dtype=uint8)
 
# ======== Saving Settings ========

TIF_SUFFIX = '.tif'
PNG_SUFFIX = '.png'
MODEL_FORMAT = '.keras'
METRICS = ['loss', 'accuracy']
PROCESSES = ['milling', 'turning']


CAM_URL = 'opc.tcp://141.3.142.81:12345'
# CAM_URL = 'opc.tcp://172.22.192.120:12345'
# CAM_URL = 'opc.tcp://127.0.0.1:12345' # local


WEAR_TYPE_LIST = ['crater','flank']