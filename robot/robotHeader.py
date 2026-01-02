''' ## Header for HORST600 part
Pre-defines constants for the robotic part. '''

from math import pi


# -------------------------------------------
#           DIGITAL TWIN
# -------------------------------------------

# ======== CONFIGURATION ========

CONFIG_INIT             = [(0, pi/4, 0, 0, 0, 0), (406.04, 0, 324.96)]
CONFIG_X_ALIGN          = [(0, pi/2, -pi/2, 0, 0, 0), (588.1, 0, 340.23)]
CONFIG_X_ALIGN_TCP_DOWN = [(0, pi/2, -pi/2, 0, pi/2, 0), (526.1, 0, 278.23)]
CONFIG_Z_MAX            = [(0, 0, -pi/2, 0, 0, 0), (-33.5, 0, 961.83)]

# ======== MOVEMENT SETTINGS ========

STANDARD_MOVE_SET = {
    'speed': [1.0]
} 

# ======== COMMUNICATION ========

# Program variables (named in horstFX)
GRIP_OPEN  = 'TOOL_OUTPUT_1'
GRIP_CLOSE = 'TOOL_OUTPUT_2'

# ======== TABLE PROPERTIES ========
# UNIT: [mm]

TABLE_X = 1195
TABLE_Y = 595

# ======== MAGAZINE PROPERTIES ========
# UNIT: [mm]

STALL_TIME = .25

H_MAG = 48
X_OFF = 25
X_D = 45
Y_OFF = 25
Y_D = 45

H_GRASP = 16.5
TOOL_HEIGHT = 30

# ======== COORDINATES ========
# UNIT: [mm]

# Offsets

OFF_MAG_X = 396-75
OFF_MAG_Y = 27.5
OFF_MAG_Z = 0
OFF_MAG = (OFF_MAG_X, OFF_MAG_Y, OFF_MAG_Z)

OFF_ROBOT_X = 100 
OFF_ROBOT_Y = 297.5 
OFF_ROBOT_Z = 12 # CONSIDER JAW!!!!
OFF_ROBOT = (OFF_ROBOT_X, OFF_ROBOT_Y, OFF_ROBOT_Z)

OFF_CAMERA_X = 0
OFF_CAMERA_Y = 0
OFF_CAMERA_Z = 0

# Points definition (in tableCOS)
# CALIBRATE
INITIAL_POINT_X = 406.04
INITIAL_POINT_Y = 297.5
INITIAL_POINT_Z = 424.96
INITIAL_POINT = (INITIAL_POINT_X, INITIAL_POINT_Y, INITIAL_POINT_Z)

# REMOVE MAGAZINE POINT AND INSTEAD USE TOOL POSITION WITH OFFSET
MAGAZINE_POINT_X = OFF_MAG_X # aligned with magazine offset
MAGAZINE_POINT_Y = OFF_MAG_Y # aligned with magazine offset
MAGAZINE_POINT_Z = 300 # realtive value
MAGAZINE_POINT = (MAGAZINE_POINT_X, MAGAZINE_POINT_Y, MAGAZINE_POINT_Z)
# CALCULATE
FOCUS_POINT_X = 600
FOCUS_POINT_Y = 297.5
FOCUS_POINT_Z = 68

PRESENTATION_TOOL = (603,285,58)

CAMERA_POINT_X = 606.5
CAMERA_POINT_Y = 286
CAMERA_POINT_Z = 112.5 # EXCHANGE TOOL HEIGHT PARAMETER
CAMERA_POINT = (CAMERA_POINT_X, CAMERA_POINT_Y, CAMERA_POINT_Z)

QR_POINT_X = OFF_MAG_X
QR_POINT_Y = TABLE_Y-50
QR_POINT_Z = 200
QR_POINT = (QR_POINT_X, QR_POINT_Y, QR_POINT_Z)

# -------------------------------------------
# Denavit-Hartenberg Parameters
# -------------------------------------------

# alpha: rotation about z; angle between z_(i-1) and z_i
# a: distance between O_i and O_i'
# d: coordinate of O_i' along z_(i-1)

# According to "Siciliano et. al.: Robotics - Modelling, Planning and Control"

ALPHA_1 = pi/2  
ALPHA_2 = 0     
ALPHA_3 = pi/2  
ALPHA_4 = -pi/2  
ALPHA_5 = pi/2 
ALPHA_6 = 0

A_1 = -33.5     
A_2 = 300       
A_3 = 0         
A_4 = 0   
A_5 = 0
A_6 = 0 

D_1 = 340.18    
D_2 = 0         
D_3 = 0         
D_4 = 259.6     
D_5 = 0         
D_6 = 62

THETA_1 = 0     
THETA_2 = pi/2   
THETA_3 = 0     
THETA_4 = 0    
THETA_5 = 0
THETA_6 = 0

# -------------------------------------------
#           ROBOT CONFIGURATIONS
# -------------------------------------------

# ======== TOOL ========
 
TOOL_RZ = pi/4 # TOOL INITIALIZATION
TOOL_TZ = 100 # TOOL INITILAIZATION

TOOL_ORIENT_DOWN = [-180, 0, -135]
TOOL_ORIENT_CAM = [-180,0,45]
TOOL_ORIENT_FORWARD = [-90, 45, -90]

# in RPY (RX, RY, RZ)
TOOL_ROTATION = [
    [-180,0,45],
    [-180,0,-45],
    [-180,0,-225],
    [-180,0,-135]
]

# ======== MAGAZINE ========
# CHANGE FROM DICTIONARY TO FORMULA

toolMagazineProp ={
    # tool plate properties: [center point, diameter(mm)]
    # INCLUDE TOOL HEIGHT

    '1R': [(X_OFF,Y_OFF,H_MAG+TOOL_HEIGHT), 5, 32, 57],
    '1L': [(X_OFF, Y_OFF+Y_D, H_MAG+TOOL_HEIGHT), 5, 32, 57],

    '2R': [(X_OFF+X_D, Y_OFF, H_MAG+TOOL_HEIGHT), 8, 32, 63],
    '2L': [(X_OFF+X_D, Y_OFF+Y_D, H_MAG+TOOL_HEIGHT), 8, 32, 63],
    
    '3R': [(X_OFF+(X_D*2.0), Y_OFF, H_MAG+TOOL_HEIGHT), 12, 40, 83],
    '3L': [(X_OFF+(X_D*2.0), Y_OFF+Y_D, H_MAG+TOOL_HEIGHT), 12, 40, 83],
    
    '4R': [(X_OFF+(X_D*3.0), Y_OFF, H_MAG+TOOL_HEIGHT), 16, 57, 92],
    '4L': [(X_OFF+(X_D*3.0), Y_OFF+Y_D, H_MAG+TOOL_HEIGHT), 16, 57, 92],
}

# ======== POSES ========
 
POSE_DICT = {
    'init': [INITIAL_POINT, TOOL_ORIENT_DOWN],
    'cam' : [CAMERA_POINT, TOOL_ORIENT_DOWN],
    'qr': [QR_POINT, TOOL_ORIENT_DOWN]
}