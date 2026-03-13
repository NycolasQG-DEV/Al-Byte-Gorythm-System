from functions.send_message import send_message
import config

# Function that defines the individual calibration parameters for each motor
def adjustMotors(m1, m2, m3, m4):
    print('Parametros de definição dos motores definidos para :', m1, m2, m3, m4)
    if not config.DEBUG_MODE:
            send_message(config.SER, 'adjustMotors ' + str(m1) + ' ' + str(m2) + ' ' + str(m3) + ' ' + str(m4))

# Function that rotates the camera servo motor
def servo(angle):
    s_correcao = -45
    print('servo ' + str(angle + s_correcao))
    if not config.DEBUG_MODE:
            send_message(config.SER, str('servo ' + str(angle + s_correcao)))

# Function that moves the robot forward for a defined amount of time
def moveFwd(speed_value, time_in_sec = 0):
    print(str('move_Fwd ' + str(speed_value) + ' ' + str(time_in_sec)))
    if not config.DEBUG_MODE:
        send_message(config.SER, str('move_Fwd ' + str(speed_value) + ' ' + str(time_in_sec)))

# Function that moves the robot backward for a defined amount of time
def moveBwd(speed_value, time_in_sec = 0):
    print(str('move_Bwd ' + str(speed_value) + ' ' + str(time_in_sec)))
    if not config.DEBUG_MODE:
        send_message(config.SER, str('move_Bwd ' + str(speed_value) + ' ' + str(time_in_sec)))

# Function that moves the robot to the right for a defined amount of time
def moveRight(speed_value, time_in_sec = 0):
    print(str('move_Right ' + str(speed_value) + ' ' + str(time_in_sec)))
    if not config.DEBUG_MODE:
        send_message(config.SER, str('move_Right ' + str(speed_value) + ' ' + str(time_in_sec)))

# Function that moves the robot to the left for a defined amount of time
def moveLeft(speed_value, time_in_sec = 0):
    print(str('move_Left ' + str(speed_value) + ' ' + str(time_in_sec)))
    if not config.DEBUG_MODE:
        send_message(config.SER, str('move_Left ' + str(speed_value) + ' ' + str(time_in_sec)))

# Function that rotates the robot to the right for a defined amount of time
def turnRight(speed_value, time_in_sec = 0):
    print(str('turn_Right ' + str(speed_value) + ' ' + str(time_in_sec)))
    if not config.DEBUG_MODE:
        send_message(config.SER, str('turn_Right ' + str(speed_value) + ' ' + str(time_in_sec)))

# Function that rotates the robot to the left for a defined amount of time
def turnLeft(speed_value, time_in_sec = 0):
    print(str('turn_Left ' + str(speed_value) + ' ' + str(time_in_sec)))
    if not config.DEBUG_MODE:
        send_message(config.SER, str('turn_Left ' + str(speed_value) + ' ' + str(time_in_sec)))

# Function that stops the movement
def stopMove():
     print("movement stoped!")
     if not config.DEBUG_MODE:
        send_message(config.SER, "stop")
