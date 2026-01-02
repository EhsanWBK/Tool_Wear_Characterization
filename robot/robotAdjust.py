''' ## Position adjustment functions. '''

import robot.robotHeader as hd
from robot.robotMov import microMove

def turnJoint(jointIdx: int = 6, jointAngle: int = 90):
    ''' Swivel end effector in small turns.
    Small rotation around the x-axis.'''
    print('Rotating.')

def craterAdjust(curPos, nrPatch: int = 4):
    for patch in range(nrPatch):
        moved, newPos = microMove(curPos=curPos, curOrient=hd.TOOL_ORIENT_DOWN, distance=.5, axis=0)
        # take picture command
        curPos = newPos
    return True

def edgeAdjust(curPos, bladeAngle: int = 90, bladeNr: int = 4):
    ''' Rotate tool to the next cutting edge. '''
    JOINT = 6
    for bladeIdx in range(bladeNr):
        print('Rotating to Blade Nr.: ',bladeIdx)
        moved = turnJoint(jointIdx=JOINT, jointAngle=bladeAngle)
        # take flank picture
        moved, sidePos = microMove(curPos=curPos, curOrient=hd.TOOL_ORIENT_DOWN, distance=.2, axis=1)
        craterAdjusted = craterAdjust(curPos=sidePos)
        moved, curPos = microMove(curPos=sidePos, curOrient=hd.TOOL_ORIENT_DOWN, distance=.2, axis=1)
    print('All blades moved.')
