import serial
#//==============================================================================================//
#//  Variable configuration script and global definitions.
#//==============================================================================================//

#// Motor calibration parameters
M1_ADJUST = -55
M2_ADJUST = -65
M3_ADJUST = -80
M4_ADJUST = 0

#// Camera configuration
SHOW_CAMERA = False  # default is False

#// Other settings
DEBUG_MODE = True   # default is False



# //=================================================================
# IF YOU WANT TO SWITCH THE CAMERA, go to :
# "/functions/camera.py" and switch de var CAMERA to 0, 1, ...
# //=================================================================



PORT = "COM20"
DETECTION_CONFIDENCE_THRESHOLD = 0.2
PROXIMITY_THRESHOLD = 2000
FULLSCREEN_WINDOW = True

# General variable definitions
EYE_COLOR = (255, 0, 255)
BACKGROUND_COLOR = (0, 0, 0)
ROBOT_EXPRESSION_INDEX = 1

DIREITO = 1
ESQUERDO = 0
FRENTE = 1
TRAS = 0

FCOUNT = []
IDISTANCE = 0

TRACKING = False
CENTRALIZE_CODEY = False
CODEY_DISTANCE = 0

FACE_CENTER_X = 0
FACE_CENTER_Y = 0
IMG_CENTER_X = 0
IMG_CENTER_Y = 0

# Initial servo position
_SERVO = 120

if not DEBUG_MODE:
    SER = serial.Serial(PORT, 9600, timeout=2)
