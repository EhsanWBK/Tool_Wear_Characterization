from threads.headerThread import *

from com.baumerCom import CamClient
from com.robotCom import HorstClient

from header import CAM_URL

# ======== Thread Execution ========
TRIGGER_TEMP = []

def opcCamConn(sharedArray, webcamArray, stopEvent:Event, triggerMode:Event):
    global STREAM_FRAME, TRIGGER_TEMP, cameraClient; 
    # global WEBCAM_FRAME
    print('\t- OPC Client Thread Set Up.')
    try:
        cameraClient = CamClient(url=CAM_URL)
        while not stopEvent.is_set():
            sharedArray[:] = cameraClient.getBaumer(); STREAM_FRAME = sharedArray
            # try: webcamArray[:] = cameraClient.getWebcam(); WEBCAM_FRAME = webcamArray
            # finally: WEBCAME_STATUS = False
            # try: triggerSet = cameraClient.getTrigger()
            # finally: triggerSet = False
            if cameraClient.getTrigger(): 
                triggerTemp = cameraClient.receivedTrigger(); TRIGGER_TEMP.append((triggerTemp)); print('Received Trigger')
                if len(TRIGGER_TEMP)>4:TRIGGER_TEMP=[]; TRIGGER_TEMP.append((triggerTemp)); print('RESET TRIGGER TEMP. NEW LEN ',len(TRIGGER_TEMP))
    except: print('CANNOT START CAM CONN'); return
    finally: cameraClient.stopClient()

def opcRobConn(stopEvent:Event):
    ''' Send Command to Horst Fx. Commands available:
    - *getInput( inputName )*: 
    - *getOutput( outputName )*:
    - *setOutput( outputName, state )*: 
    - *getCurrentRobotPosition( )*: 
    - *getCurrentRobotJoints( )*: 
    - *moveJoint( [xyz, q, velocity] )*: 
    - *moveLinear( [xyz, q, velocity] )*: 
    - *setTool*: 
    - *getToolOff*: 
    - *getNextJoint*: 
    - *setNextJoint*: 
    - *getNextPose*: 
    - *setNextPose*: 
    - *getGlobalSpeed*: 
    - *setGlobalSpeed*: 
    - *initRobot*: 
    '''
    global CUR_CMD, CUR_VAL, ROB_CALLBACK
    try:
        client = HorstClient(); RUN=False; ROB_CALLBACK=None; CUR_CMD=''; CUR_VAL=None
        while not stopEvent.is_set():
            if not RUN and CUR_CMD != '':
                client.sendCmd(cmd=CUR_CMD, val=CUR_VAL)
                print('Sending Command to HORST: ',CUR_CMD)
                RUN = True; resultSet = False
                while RUN: RUN=client.isRunning()
                while not resultSet: resultSet, callback = client.readResult()
                RUN = False; ROB_CALLBACK = callback; CUR_CMD = ''; CUR_VAL = []
    except: print('Problem in Execution')
    finally: 
        client.stopClient()

# ======== Events ========

opcCamStart = Event()
triggerMode = Event()
opcRobStart = Event()
stopEvent = Event(); stopEvent.clear()

# ======== Threads ========

opcCamThread = Thread(target=opcCamConn, args=(IMG_ARRAY, WEBCAM_ARRAY,stopEvent, triggerMode))
opcRobThread = Thread(target=opcRobConn, args=(stopEvent,))

def startOPCThread():
    print('\t- Starting OPC Thread.')
    opcCamThread.start(); sleep(1)
    opcRobThread.start()

def shutdownOPCThread():
    print('\t- Shutting Down OPC Thread.')
    stopEvent.set()
    opcCamStart.set(); opcCamStart.clear()
    triggerMode.set(); triggerMode.clear()
    opcRobStart.set(); opcRobStart.clear()
    opcCamThread.join(timeout=1)