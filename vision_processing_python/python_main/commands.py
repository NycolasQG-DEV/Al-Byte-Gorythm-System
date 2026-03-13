from functions.send_message import send_message
import config




#função que gira o servo motor da camera
def servo(angle):
    s_correcao = -45
    print('servo ' + str(angle + s_correcao))
    if not config.DEBUG_MODE:
            send_message(config.SER, str('servo ' + str(angle + s_correcao)))

#função que move o robô para frente por uma quantidade definida de tempo
def moveFwd(speed_value, time_in_sec = 0):
    print(str('move_Fwd ' + str(speed_value) + ' ' + str(time_in_sec)))
    if not config.DEBUG_MODE:
        send_message(config.SER, str('move_Fwd ' + str(speed_value) + ' ' + str(time_in_sec)))

#função que move o robô para trás por uma quantidade definida de tempo
def moveBwd(speed_value, time_in_sec = 0):
    print(str('move_Bwd ' + str(speed_value) + ' ' + str(time_in_sec)))
    if not config.DEBUG_MODE:
        send_message(config.SER, str('move_Bwd ' + str(speed_value) + ' ' + str(time_in_sec)))

#função que move o robô para direita por uma quantidade definida de tempo
def moveRight(speed_value, time_in_sec = 0):
    print(str('move_Right ' + str(speed_value) + ' ' + str(time_in_sec)))
    if not config.DEBUG_MODE:
        send_message(config.SER, str('move_Right ' + str(speed_value) + ' ' + str(time_in_sec)))

#função que move o robô para esquerda por uma quantidade definida de tempo
def moveLeft(speed_value, time_in_sec = 0):
    print(str('move_Left ' + str(speed_value) + ' ' + str(time_in_sec)))
    if not config.DEBUG_MODE:
        send_message(config.SER, str('move_Left ' + str(speed_value) + ' ' + str(time_in_sec)))

#função que gira o robô para direita por uma quantidade definida de tempo
def turnRight(speed_value, time_in_sec = 0):
    print(str('turn_Right ' + str(speed_value) + ' ' + str(time_in_sec)))
    if not config.DEBUG_MODE:
        send_message(config.SER, str('turn_Right ' + str(speed_value) + ' ' + str(time_in_sec)))

#função que gira o robô para esquerda por uma quantidade definida de tempo
def turnLeft(speed_value, time_in_sec = 0):
    print(str('turn_Left ' + str(speed_value) + ' ' + str(time_in_sec)))
    if not config.DEBUG_MODE:
        send_message(config.SER, str('turn_Left ' + str(speed_value) + ' ' + str(time_in_sec)))


#função que para o movimento
def stopMove():
     print("movement stoped!")
     if not config.DEBUG_MODE:
        send_message(config.SER, "stop")
        
        
