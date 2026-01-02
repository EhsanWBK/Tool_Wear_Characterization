import eel
from numpy import zeros, uint8
from threading import Event, Thread
from time import sleep

CLASSES = ['crater', 'flank']

IMG_SHAPE = (2048, 2448, 3)
IMG_ARRAY = zeros(IMG_SHAPE, dtype=uint8)

WEBCAM_SHAPE = (480,640,3)
WEBCAM_ARRAY = zeros(WEBCAM_SHAPE, dtype=uint8)