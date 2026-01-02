from threads.segmentationThread import *
from threads.headerThread import *
import threads.opcThread as opc

import robot.robotHeader as hdRob
from robot.kinCalculations import convertCOS, calculateFocusPoint
from ml.segmentation import objectDetection

from header import ROB_SEG_IMG
from utensils.generalUtensils import getTimeStamp

BLOCK_COMM = False
SEQ_DONE = False

def horstCmd(cmd:str, val):
    global BLOCK_COMM
    timeout = time()+60
    while time()<timeout:
        if not BLOCK_COMM: opc.CUR_CMD = cmd; opc.CUR_VAL = val; BLOCK_COMM=True
        if opc.ROB_CALLBACK != None: callback = opc.ROB_CALLBACK; opc.ROB_CALLBACK = None; BLOCK_COMM=False; return callback
    print('horstCmd Terminated')

def moveLinear(point, orientation = hdRob.TOOL_ORIENT_DOWN, speed = hdRob.STANDARD_MOVE_SET['speed']):
    value = point+orientation+speed
    moved = horstCmd(cmd='moveLinear', val=value)
    return moved

def ptpMovement(endPoint, endOrientation = hdRob.TOOL_ORIENT_FORWARD):
    ''' Point-To-Point (PTP) movement. Takes in coordinate of initial point and end point.
    Coordinate system of points is tableCOS. Need to be converted before.
    Returns True if successful and End Pose in Table COS.'''
    endPointRobot, endPointRobotMatrix =convertCOS(points=endPoint, orientation=endOrientation, initCOS='tableCOS', targetCOS='robotCOS')
    print('\n==== PTP ROBOT MOVEMENT ====')
    print('Set Position (Robot COS):\t', endPointRobot)
    robotMoved = moveLinear(point=endPointRobot, orientation=endOrientation)
    print('Robot Moved:\t\t\t', robotMoved)
    return robotMoved, endPoint

def accessTool(curPos, pickUp = True, toolPos: str = '1L'):
    ''' Current Position Input in Table COS. Pick Up is True, when picking up tool and False, when placing down tool.'''
    # CALCULATE GRASPING POSE FROM TOOL HISTORY PARAMETER (tool length)
    hGrasp = hdRob.H_MAG + hdRob.toolMagazineProp[toolPos][2] - hdRob.H_GRASP
    gripPoint = copy(curPos)
    gripPoint[2] = hGrasp
    movedDown, holdPoint = ptpMovement(endPoint=gripPoint, endOrientation=hdRob.TOOL_ORIENT_DOWN)
    sleep(hdRob.STALL_TIME)
    if pickUp: gripON()
    else: gripOFF()
    sleep(hdRob.STALL_TIME )
    movedUp, endPoint = ptpMovement(endPoint=curPos, endOrientation=hdRob.TOOL_ORIENT_DOWN) if movedDown else False, curPos
    if movedUp: return True, endPoint
    else: return False, endPoint

def pictureRoutine(curPos):
    ''' Takes in Position where the turning operation should take place. Orientation is downwards. Speed capped to 0.5. '''
    baumerRobStart.clear()
    curPos, endPointRobotMatrix = convertCOS(points=curPos, orientation=hdRob.TOOL_ORIENT_DOWN, initCOS='tableCOS', targetCOS='robotCOS')
    for idx in range(len(hdRob.TOOL_ROTATION)): 
        moved = moveLinear(point=list(curPos), orientation=hdRob.TOOL_ROTATION[idx], speed = [1])
        curImg = copy(opc.STREAM_FRAME); saveForPIL = curImg[:,:,0].astype(uint8)
        Image.fromarray(saveForPIL).save(join(CWD,'tmp','robotImg',f'robotImg_{idx}.jpg'))
    baumerRobStart.set(); #segmentRobStart.set()
    return False

# ======== Eel Extension ========

@eel.expose()
def fullSeq():
    global SEQ_DONE, CUR_TOOL_POS
    print('Running Full Movement Sequence')
    toolPosList = ['1R', '1L', '2R', '2L', '3R', '3L']
    for pos in toolPosList:
        CUR_TOOL_POS = pos; SEQ_DONE = False
        routineStart.set()
        while not SEQ_DONE: pass
    print('Finished Full Movement Sequence')

@eel.expose()
def singleSeq(toolPos):
    global SEQ_DONE, CUR_TOOL_POS
    print('Running Single Movement Sequence')
    CUR_TOOL_POS = str(toolPos); SEQ_DONE = False
    routineStart.set()
    while not SEQ_DONE: pass
    print('Finished Single Movement Sequence')

@eel.expose()
def moveToPosXYZ(x,y,z,speed):
    point = [float(x),float(y),float(z)]
    moved = moveLinear(point=point, speed=[float(speed)/100])
    return moved

@eel.expose()
def moveToPosDict(key, speed):
    point, orientation = hdRob.POSE_DICT[key]
    moved, endPoint = ptpMovement(endPoint=point, endOrientation=orientation)
    return moved

@eel.expose()
def moveToCalibrate(CUR_TOOL_POS:str = '3R'):
    noError = True
    while noError:
        noError, curPos = ptpMovement(endPoint=hdRob.INITIAL_POINT, endOrientation=hdRob.TOOL_ORIENT_DOWN) # 1: initialize
        noError, curPos = moveToToolPos(toolPos=CUR_TOOL_POS)  # 2: approach tool magazine
        noError, curPos = accessTool(curPos=curPos, pickUp=True, toolPos=CUR_TOOL_POS) # 3: pick up tool
        noError, curPos = ptpMovement(endPoint=calculateFocusPoint(CUR_TOOL_POS), endOrientation=hdRob.TOOL_ORIENT_DOWN)
        blob = reformatFrame(frame=opc.STREAM_FRAME); break
    eel.updateRobCanvas2(blob)()

@eel.expose()
def moveToToolPos(toolPos: str = '1L'):
    ''' Approach a tool on the tool plate.
    Needs grasping taxonomy: predifined grasps; all tools have same geometry for base
    Just different diameters. Assumption: diameters are predefined for each position.
    
    Initial situation: TCP at point close to tool plate. Point far enough away from plate to allow rotation. '''
    toolBasePos, toolDiam, _, _ = hdRob.toolMagazineProp[toolPos]
    toolConfig = [a+b for a,b in zip(toolBasePos,hdRob.MAGAZINE_POINT)] # coordinate transform mag cos to table cos
    print('TOOL CONFIG: ',toolConfig)
    print('\nMOVING TO TOOL POSITION:\nSet Position (Table COS):\t', toolConfig, '\nDiameter:\t\t\t',toolDiam,'\n')
    moved, endPoint = ptpMovement(endPoint=toolConfig, endOrientation=hdRob.TOOL_ORIENT_DOWN)
    sleep(hdRob.STALL_TIME)
    if moved: return True, endPoint 
    else: return False, endPoint

@eel.expose()
def gripON():
    horstCmd(cmd='setOutput', val=[1.0,hdRob.GRIP_CLOSE])
    horstCmd(cmd='setOutput', val=[0.0,hdRob.GRIP_CLOSE])

@eel.expose()
def gripOFF():
    horstCmd(cmd='setOutput', val=[1.0,hdRob.GRIP_OPEN])
    horstCmd(cmd='setOutput', val=[0.0,hdRob.GRIP_OPEN])

# ======== Thread Execution ========

def robotRoutine(event:Event, stopEvent:Event):
    print('\t- Robot Routine Thread Set Up.')
    global SEQ_DONE
    noError = True
    while not stopEvent.is_set():
        event.wait(); webcamStart.set()
        if stopEvent.is_set(): return
        while event.is_set() and not stopEvent.is_set():
            while noError: 
                noError, curPos = ptpMovement(endPoint=hdRob.INITIAL_POINT, endOrientation=hdRob.TOOL_ORIENT_DOWN) # 1: initialize
                noError, curPos = moveToToolPos(toolPos=CUR_TOOL_POS)  # 2: approach tool magazine
                noError, curPos = accessTool(curPos=curPos, pickUp=True, toolPos=CUR_TOOL_POS) # 3: pick up tool
                # noError, curPos = ptpMovement(endPoint=hdRob.QR_POINT, endOrientation=hdRob.TOOL_ORIENT_DOWN) # 4: to qr Scan
                # display qr scan # set result # 4.1 scan qr
                # noError, curPos = adjustToolCamera(curPos=hdRob.PRESENTATION_TOOL,curOrient=hdRob.TOOL_ROTATION[0], toolPos=curToolPos)
                noError, curPos = ptpMovement(endPoint=calculateFocusPoint(CUR_TOOL_POS), endOrientation=hdRob.TOOL_ORIENT_DOWN) # 5: to camera
                segmentRobStart.set() # Start Segmentation
                noError = pictureRoutine(curPos=curPos); # 5.1: display wear results
                noError, curPos = moveToToolPos(toolPos=CUR_TOOL_POS) # 6: approach tool magazine
                noError, curPos = accessTool(curPos=curPos, pickUp=False, toolPos=CUR_TOOL_POS) # 7: place down tool
                SEQ_DONE = True; 
                break
            webcamStart.clear(); event.clear()

def webcamStreamStart(event:Event, stopEvent:Event):
    ''' Stream Overhead Webcam on Robot Canvas 1.'''
    print('\t- Webcam Video Stream Thread Set Up.')
    while not stopEvent.is_set():
        event.wait(); print('RUNNING WEBCAM NOW.')
        OBJ_DET_MODEL = YOLO(join(CWD,'models','objectDet','yolov8_nohands.pt'))
        if stopEvent.is_set(): return
        while event.is_set() and not stopEvent.is_set(): # to stop stream: call videoEvent.clear() outside of this function
            frame = copy(opc.WEBCAM_FRAME)
            OBJ_DET_FRAME = objectDetection(frame=frame,model=OBJ_DET_MODEL)
            blob = reformatFrame(frame=OBJ_DET_FRAME)
            eel.updateRobCanvas1(blob)()
            print('Object Detection')
        print('Stopped Streaming Data.')
    print('Stream Segementation to be terminated.')

def robotBaumerStreamStart(event:Event, stopEvent:Event):
    print('\t- Baumer Video Stream Thread Set Up.')
    while not stopEvent.is_set():
        event.wait()
        if stopEvent.is_set(): return
        while event.is_set() and not stopEvent.is_set(): # to stop stream: call videoEvent.clear() outside of this function
            blob = reformatFrame(frame=opc.STREAM_FRAME)
            eel.updateRobCanvas2(blob)()
        print('Stopped Streaming Data.')
        event.clear()

def segmentRobImages(event:Event, stopEvent:Event):
    print('\t- Robot Image Segmentation Thread Set Up.')
    while not stopEvent.is_set():
        event.wait()
        if stopEvent.is_set(): return
        while event.is_set() and not stopEvent.is_set():
            print('Starting Segementation')
            RESULT_FOLDER = ROB_SEG_IMG+'_'+getTimeStamp()
            if not exists(RESULT_FOLDER): makedirs(RESULT_FOLDER)
            for idx in range(len(listdir(ROB_IMG_TEMP))):
                print('SEGMENTING IMAGE')
                try:
                    imgTmp = array(Image.open(join(ROB_IMG_TEMP,f'robotImg_{idx}.jpg')).convert('RGB'))
                    VB_MAX_TEMP, SEG_TEMP, CLF_TEMP = singleFramePred(frame=imgTmp, model=SEG_MODEL); SEG_TEMP=SEG_TEMP[0]
                    saveForPIL = SEG_TEMP[0,:,:,0].astype(uint8)
                    Image.fromarray(saveForPIL).save(join(RESULT_FOLDER, f'robotSegMask_{idx}.jpg'))
                    wearPar = {'maxVB':VB_MAX_TEMP[0], 'wearType':WEAR_TYPE_LIST[CLF_TEMP[0]]}
                    eel.updateWearValues(VB_MAX_TEMP, CLASSES[CLF_TEMP])()
                    blob = reformatFrame(SEG_TEMP, wearPar=wearPar,orgImg=opc.STREAM_FRAME)
                    eel.updateRobCanvas2(blob)(); print('Displayed Image to Canvas')
                except: None
            event.clear()
            
# ======== Events ========

routineStart = Event()
baumerRobStart = Event()
webcamStart = Event()
segmentRobStart = Event()

# ======== Threads ========

robotRoutineStart = Thread(target=robotRoutine, args=(routineStart, opc.stopEvent))
baumerRobThread = Thread(target=robotBaumerStreamStart, args=(baumerRobStart, opc.stopEvent))
webcamStreamThread = Thread(target=webcamStreamStart, args=(webcamStart, opc.stopEvent))
segmentRobThread = Thread(target=segmentRobImages, args=(segmentRobStart, opc.stopEvent))

def startRobThread():
    print('\t- Starting Robot Thread.')
    robotRoutineStart.start(); sleep(1)
    baumerRobThread.start(); sleep(1)
    webcamStreamThread.start(); sleep(1)
    segmentRobThread.start(); sleep(1)

def shutdownRobThread():
    print('\t- Shutting Down Robot Thread.')
    stopEvent.set()
    routineStart.set(); routineStart.clear()
    baumerRobStart.set(); baumerRobStart.clear()
    webcamStart.set(); webcamStart.clear()
    segmentRobStart.set(); segmentRobStart.clear()
    robotRoutineStart.join(timeout=1); sleep(1);baumerRobThread.join(timeout=1);sleep(1); 
    webcamStreamThread.join(timeout=1);sleep(1); 
    segmentRobThread.join(timeout=1)