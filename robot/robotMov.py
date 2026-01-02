''' ## Coordination of HORST600 movement '''
from robot.kinCalculations import convertCOS, convertToMatrix
from com.robotCom import horstCmd
# from imageRecognition.imageQR import scanQR
import robot.robotHeader as hd
from time import sleep
from copy import copy

#  =========================================
#  	         Movement Routines
#  =========================================

def moveToToolPos(toolPos: str = '1L'):
    ''' Approach a tool on the tool plate.
    Needs grasping taxonomy: predifined grasps; all tools have same geometry for base
    Just different diameters. Assumption: diameters are predefined for each position.
    
    Initial situation: TCP at point close to tool plate. Point far enough away from plate to allow rotation. '''
    toolBasePos, toolDiam, _, _ = hd.toolMagazineProp[toolPos]
    toolConfig = [a+b for a,b in zip(toolBasePos,hd.MAGAZINE_POINT)] # coordinate transform mag cos to table cos
    print('TOOL CONFIG: ',toolConfig)
    print('\nMOVING TO TOOL POSITION:\nSet Position (Table COS):\t', toolConfig, '\nDiameter:\t\t\t',toolDiam,'\n')
    moved, endPoint = ptpMovement(endPoint=toolConfig, endOrientation=hd.TOOL_ORIENT_DOWN)
    sleep(hd.STALL_TIME)
    if moved: return True, endPoint 
    else: return False, endPoint

def accessTool(curPos, pickUp = True, toolPos: str = '1L'):
    ''' Current Position Input in Table COS. Pick Up is True, when picking up tool and False, when placing down tool.'''
    # CALCULATE GRASPING POSE FROM TOOL HISTORY PARAMETER (tool length)
    hGrasp = hd.H_MAG + hd.toolMagazineProp[toolPos][2] - hd.H_GRASP
    gripPoint = copy(curPos)
    gripPoint[2] = hGrasp
    movedDown, holdPoint = ptpMovement(endPoint=gripPoint, endOrientation=hd.TOOL_ORIENT_DOWN)
    sleep(hd.STALL_TIME)
    if pickUp: gripON()
    else: gripOFF()
    sleep(hd.STALL_TIME )
    movedUp, endPoint = ptpMovement(endPoint=curPos, endOrientation=hd.TOOL_ORIENT_DOWN) if movedDown else False, curPos
    if movedUp: return True, endPoint
    else: return False, endPoint

#  =========================================
#  	         Supportive Functions
#  =========================================

def move(point, orientation = hd.TOOL_ORIENT_DOWN, speed = hd.STANDARD_MOVE_SET['speed']):
    ''' Linear Movement. Points not converted. Orientation in RPY (deg). Speed in range between 0 and 1 [%]. Conversion on Robot.'''
    value = point+orientation+speed
    moved = horstCmd(cmd='moveLinear', val=value)
    return moved

def gripON():
    horstCmd(cmd='setOutput', val=[1.0,hd.GRIP_CLOSE])
    horstCmd(cmd='setOutput', val=[0.0,hd.GRIP_CLOSE])

def gripOFF():
    horstCmd(cmd='setOutput', val=[1.0,hd.GRIP_OPEN])
    horstCmd(cmd='setOutput', val=[0.0,hd.GRIP_OPEN])
    
def ptpMovement(endPoint, endOrientation = hd.TOOL_ORIENT_FORWARD):
    ''' Point-To-Point (PTP) movement. Takes in coordinate of initial point and end point.
    Coordinate system of points is tableCOS. Need to be converted before.
    Returns True if successful and End Pose in Table COS.'''
    endPointRobot, endPointRobotMatrix =convertCOS(points=endPoint, orientation=endOrientation, initCOS='tableCOS', targetCOS='robotCOS')
    # VALIDATE POSITION ACCORDING TO DIGITAL TWIN
    print('\n==== PTP ROBOT MOVEMENT ====')
    print('Set Position (Robot COS):\t', endPointRobot)
    robotMoved = move(point=endPointRobot, orientation=endOrientation)
    print('Robot Moved:\t\t\t', robotMoved)
    return robotMoved, endPoint

def microMoveCalc(curPos, distance, axis): 
    posTmp = list(copy(curPos))
    posTmp[axis] += distance
    print(posTmp[axis])
    posTmp = tuple(posTmp)
    print('PosTmp: ', posTmp, type(posTmp))
    return posTmp  

def microMove(curPos, curOrient, distance, axis):
    ''' Micro Movement of TCP. Takes in current pose, current orientation, and distance. Sign of distance determins direction. ''' 
    print('CurPos: ', curPos, type(curPos))
    posTmp = microMoveCalc(curPos=curPos, distance=distance, axis=axis)
    moved, endPoint = ptpMovement(endPoint=posTmp, endOrientation=curOrient)
    return moved, endPoint

def pictureRoutine(curPos):
    ''' Takes in Position where the turning operation should take place. Orientation is downwards. Speed capped to 0.5. '''
    curPos, endPointRobotMatrix = convertCOS(points=curPos, orientation=hd.TOOL_ORIENT_DOWN, initCOS='tableCOS', targetCOS='robotCOS')
    for orientation in hd.TOOL_ROTATION: move(point=list(curPos), orientation=orientation, speed = [1])
    return False

def adjustToolCamera(curPos, curOrient, toolPos):
    xNew = (hd.toolMagazineProp[toolPos][1])/2
    xNewPos = microMoveCalc(curPos=curPos, distance=xNew, axis=0)
    zNew = (hd.toolMagazineProp[toolPos][2]+hd.toolMagazineProp[toolPos][3])
    zNewPos = microMoveCalc(curPos=xNewPos, distance=zNew ,axis=2)
    moved, endPoint = ptpMovement(endPoint=zNewPos, endOrientation=curOrient)
    return moved, endPoint
