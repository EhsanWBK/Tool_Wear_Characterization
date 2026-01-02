''' ## Kinematic Calculations
Range of kinematic calculations suporting the robot model and movement functions. '''

import robot.robotHeader as hd
import spatialmath as sm

def convertToMatrix(point: tuple, orientation: tuple=(0,0,0)) -> sm.SE3:
    ''' Convert point to homogenous transformation matrix. Returns Transformation Matrix.'''
    X = sm.SE3.Tx(point[0])
    Y = sm.SE3.Ty(point[1])
    Z = sm.SE3.Tz(point[2])
    RX = sm.SE3.Rx(orientation[0],'deg')
    RY = sm.SE3.Ry(orientation[1],'deg')
    RZ = sm.SE3.Rz(orientation[2],'deg')
    return X*Y*Z*RX*RY*RZ

def convertCOS(points: tuple, orientation: tuple, display: bool = False, initCOS=None, targetCOS=None) -> sm.SE3:
    ''' Convert points from table COS to robot COS.
    Returns points for target COS. Abborts if unsuccessful. '''
    offset = hd.OFF_ROBOT
    POSE_IN = convertToMatrix(point=points, orientation=orientation)
    T_OFF = convertToMatrix(point=offset, orientation=orientation) 
    T_OFF = T_OFF.inv() 
    POSE_OUT = POSE_IN * T_OFF
    t = POSE_OUT.t
    POS_XYZ = [round(a,5) for a in t]
    return POS_XYZ, POSE_OUT

def calculateFocusPoint(toolRef: str):
    z_off = hd.toolMagazineProp[toolRef][3]-hd.toolMagazineProp[toolRef][2]
    DIAM = hd.toolMagazineProp[toolRef][1]
    FOCUS_POINT = [hd.OFF_ROBOT_X+500, hd.OFF_ROBOT_Y-9, hd.OFF_ROBOT_Z+147]
    print('Diam.: ', DIAM, 'zOff: ',z_off, ' FocusPoint: ', FOCUS_POINT)
    focus_new = (FOCUS_POINT[0]+DIAM//2, FOCUS_POINT[1], FOCUS_POINT[2]-z_off)
    print(focus_new)
    # focus_new = convertCOS(focus_new, hd.TOOL_ORIENT_DOWN)[0]
    print(focus_new)
    return focus_new