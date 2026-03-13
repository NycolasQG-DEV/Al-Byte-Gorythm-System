import serial


#//==============================================================================================//
#//  Script de configuração de variaveis e definições globais.
#//==============================================================================================//

#//Config da camera 
SHOW_CAMERA = False #padrão False

#//Resto das configs
DEBUG_MODE = False #padrão False

PORT = "COM3"
DETECTION_CONFIDENCE_THRESHOLD = 0.2
PROXIMITY_THRESHOLD = 2000
FULLSCREEN_WINDOW = True

#definição de variaveis gerais
EYE_COLOR = (255,0,255)
BACKGROUND_COLOR = (0,0,0)
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

#posição inicial do servo
_SERVO = 120

if not DEBUG_MODE:
    SER = serial.Serial(PORT, 9600, timeout=2)


