from functions.send_message import send_message
import config




#função que gira o servo motor da camera
def servo(angle):
    s_correcao = -45
    if not config.DEBUG_MODE:
            send_message(config.SER, str('s ' + str(angle + s_correcao) + ' 0 0'))
            print('comando enviado com sucesso! : ' + str('s ' + str(angle + s_correcao) + ' 0 0'))

#função que liga/inicia um motor especifico 
def iniciar_motor(motor_index, speed_value):
    if not config.DEBUG_MODE:
        if motor_index == config.DIREITO:
            send_message(config.SER, str('d ' + str(speed_value) + ' 0 0'))
            print('comando enviado com sucesso! : ' + 'd ' + str(speed_value) + ' 0 0')
        elif motor_index == config.ESQUERDO:
            send_message(config.SER, str('e ' + str(speed_value) + ' 0 0'))
            print('comando enviado com sucesso! : ' + 'e ' + str(speed_value) + ' 0 0')

#função que liga/inicia 2 motores por tempo determinado
def mover_tanque(left_speed, right_speed, time_in_sec):
    if not config.DEBUG_MODE:
        send_message(config.SER, str('m ' + str(left_speed) + ' ' + str(right_speed) + ' ' + str(time_in_sec)))
        print('comando enviado com sucesso! : ' + 'm ' + str(left_speed) + ' ' + str(right_speed) + ' ' + str(time_in_sec))
        print('comando enviado com sucesso! : ' + 'm ' + str(left_speed * -1) + ' ' + str(right_speed) + ' ' + str(time_in_sec))

#função que move o robô para tras
def mover_para_tras(speed):
    if not config.DEBUG_MODE:
        send_message(config.SER, str('t ' + str(speed) + ' 0 0'))
        print(config.SER, str('t ' + str(speed) + ' 0 0'))

#para um motor especifico
def parar_motores():
    if not config.DEBUG_MODE:
        send_message(config.SER, str('p ' + str(config.ESQUERDO) + ' 0 0'))
        send_message(config.SER, str('p ' + str(config.DIREITO) + ' 0 0'))
        print('p ' + str(config.ESQUERDO) + ' 0 0')
        print('p ' + str(config.DIREITO) + ' 0 0')

#breca um motor especifico
def brecar_motores():
    if not config.DEBUG_MODE:
        send_message(config.SER, str('b ' + str(config.ESQUERDO) + ' 0 0'))
        send_message(config.SER, str('b ' + str(config.DIREITO) + ' 0 0'))
        print('b ' + str(config.ESQUERDO) + ' 0 0')
        print('b ' + str(config.DIREITO) + ' 0 0')

#função que gira o robô em graus ( DONT WORK )
def girar_graus(angle, left_speed, right_speed):
    if not config.DEBUG_MODE:
        send_message(config.SER, str('g ' + str(angle) + ' ' + str(left_speed) + ' ' + str(right_speed)))
        print('g ' + str(angle) + ' ' + str(left_speed) + ' ' + str(right_speed))


#para um motor especifico
def andar_frente(left_speed, right_speed):
    if not config.DEBUG_MODE:
        send_message(config.SER, str('f ' + str(left_speed) + ' ' + str(right_speed) + ' 0'))
        print(('f ' + str(left_speed) + ' ' + str(right_speed) + ' 0'))