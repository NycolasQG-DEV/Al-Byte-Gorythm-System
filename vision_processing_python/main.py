import threading
import asyncio
import config

from functions.robot import robot_face_update
from functions.audio import play_audio
from functions.send_message import send_message
from commands import iniciar_motor, mover_tanque, girar_graus, parar_motores, mover_para_tras, servo, brecar_motores, andar_frente

#//==============================================================================================//
#//  Al B. Gorithm -- code by Hortobots team 2024 
#// 
#//  * Nycolas Queiroz Gimenez     
#//  * Tiago Ferreira Gregório
#//  * Luiz Otavio Siqueira
#//  * Nicolas Paiva Medeiros                          
#//                         
#//==============================================================================================//
motor_direito, motor_esquerdo = config.DIREITO, config.ESQUERDO

#função para fazer a pausa para detecção de gestos com 2 mãos
async def wait_both_hand_ok(finger_count_left_hand, finger_count_right_hand):
    while True:
        if len(config.FCOUNT) > 1:
            if config.FCOUNT[0] == finger_count_left_hand and config.FCOUNT[1] == finger_count_right_hand:
                return
        await asyncio.sleep(0.1)  # Espera não bloqueante

#função para fazer a pausa para detecção de gestos com 1 mão
async def wait_single_hand_ok(finger_count):
    while True:
        if len(config.FCOUNT) > 0:
            if config.FCOUNT[0] == finger_count:
                return
        await asyncio.sleep(0.1)  # Espera não bloqueante

#//==============================================================================================//
#//  Programação do script da apresentação
#//==============================================================================================//

#// -- programação ATO 1 //
async def ato_1():
    await asyncio.sleep(10)
    await wait_single_hand_ok(5)
    config.ROBOT_EXPRESSION_INDEX = 2
    mover_tanque(150,150, 3)
    await asyncio.sleep(4.5)
    config.ROBOT_EXPRESSION_INDEX = 5
    play_audio('audio_files/1.mp3')
    await asyncio.sleep(3)
    iniciar_motor(motor_esquerdo,255)
    await asyncio.sleep(1)
    brecar_motores()
    await asyncio.sleep(2)
    iniciar_motor(motor_direito,255)
    await asyncio.sleep(1)
    await wait_centralize_codey()
    await asyncio.sleep(6)
    config.ROBOT_EXPRESSION_INDEX = 3
    return    
    

#// -- programação ATO 2 //
async def ato_2():
    parar_motores()
    mover_para_tras(180)
    await asyncio.sleep(2)
    play_audio('audio_files/2.mp3')
    await asyncio.sleep(0.5)
    parar_motores()
    await asyncio.sleep(13)
    config.ROBOT_EXPRESSION_INDEX = 5
    iniciar_motor(motor_esquerdo,255)
    await asyncio.sleep(1)
    brecar_motores()
    play_audio('audio_files/3.mp3')
    await asyncio.sleep(2)
    config.ROBOT_EXPRESSION_INDEX = 6
    await asyncio.sleep(1)
    config.ROBOT_EXPRESSION_INDEX = 3
    iniciar_motor(motor_direito, 255)
    await asyncio.sleep(1.2)
    await wait_centralize_codey()
    await asyncio.sleep(1)
    config.ROBOT_EXPRESSION_INDEX = 5
    await asyncio.sleep(9)
    config.ROBOT_EXPRESSION_INDEX = 2
    play_audio('audio_files/4.mp3')
    await asyncio.sleep(5.5)
    config.ROBOT_EXPRESSION_INDEX = 1
    mover_para_tras(160)
    await asyncio.sleep(2)
    parar_motores()
    await asyncio.sleep(3.5)
    play_audio('audio_files/5.mp3')
    config.ROBOT_EXPRESSION_INDEX = 3
    await asyncio.sleep(4)
    return 

#// -- programação ATO 3 //
async def ato_3():
    brecar_motores()
    config.ROBOT_EXPRESSION_INDEX = 7
    await asyncio.sleep(2)
    config.TRACKING = True
    #andar_frente(120, 120)
    await wait_stop_tracking()
    await asyncio.sleep(2)
    brecar_motores()
    if config.FACE_CENTER_X < config.IMG_CENTER_X -5:
        iniciar_motor(config.DIREITO, 220)             
    elif config.FACE_CENTER_X > config.IMG_CENTER_X -5:         
        iniciar_motor(config.ESQUERDO, 220)
          
        
    play_audio('audio_files/6.mp3')
    await wait_centralize_codey()
    iniciar_motor(motor_esquerdo,255)
    await asyncio.sleep(2)
    parar_motores()
    await asyncio.sleep(3)
    iniciar_motor(motor_direito, 255)
    await wait_centralize_codey()
    await asyncio.sleep(1)
    config.ROBOT_EXPRESSION_INDEX = 3
    play_audio('audio_files/7.mp3')
    await asyncio.sleep(5)
    mover_para_tras(180)
    await asyncio.sleep(2)
    parar_motores()
    await asyncio.sleep(1.5)
    return

#// -- programação ATO 4 //
async def ato_4():
    play_audio('audio_files/10.mp3')
    config.ROBOT_EXPRESSION_INDEX = 5
    await asyncio.sleep(15)
    play_audio('audio_files/11.mp3')
    config.ROBOT_EXPRESSION_INDEX = 3
    await asyncio.sleep(4)
    config.ROBOT_EXPRESSION_INDEX = 1
    await asyncio.sleep(8)
    play_audio('audio_files/12.mp3')
    config.ROBOT_EXPRESSION_INDEX = 6
    await asyncio.sleep(1)
    config.ROBOT_EXPRESSION_INDEX = 7
    mover_tanque(140, 140, 2)
    await wait_both_hand_ok(5, 5)
    parar_motores()
    play_audio('audio_files/erro.mp3')
    config.ROBOT_EXPRESSION_INDEX = 8
    await asyncio.sleep(1)
    config.BACKGROUND_COLOR = (255,50,50)
    await asyncio.sleep(50)
    play_audio('audio_files/start.mp3')
    await asyncio.sleep(5)
    return

#// -- programação fala final //
async def FINALROBOTTALK():
    config.ROBOT_EXPRESSION_INDEX = 9
    config.EYE_COLOR = (255,255,0)
    iniciar_motor(motor_esquerdo,250)
    await asyncio.sleep(0.8)
    parar_motores()
    play_audio('audio_files/13.mp3')
    await asyncio.sleep(3)
    iniciar_motor(motor_esquerdo, 250)
    await asyncio.sleep(0.5)
    parar_motores()
    await asyncio.sleep(12)
    config.ROBOT_EXPRESSION_INDEX = 1
    play_audio('audio_files/14.mp3')
    await asyncio.sleep(15)
    play_audio('audio_files/erro.mp3')
    config.ROBOT_EXPRESSION_INDEX = 3
    config.EYE_COLOR = (255,0,255)
    await asyncio.sleep(3)
    config.ROBOT_EXPRESSION_INDEX = 1
    config.EYE_COLOR = (255,255,0)
    await asyncio.sleep(30)
    return 


async def wait_stop_tracking():
    while config.TRACKING:  # Verifica se config.TRACKING é True
        await asyncio.sleep(0.1)  # Espera 100ms antes de verificar novamente
    print("config.TRACKING mudou para False!")

async def wait_centralize_codey():
    while not config.CENTRALIZE_CODEY:  # Verifica se config.CENTRALIZE_CODEY é False
        await asyncio.sleep(0.1)  # Espera 100ms antes de verificar novamente
    parar_motores()
    print("codey centralizado!")
    return


async def test():
    mover_tanque(150, 150, 5)
    await asyncio.sleep(20)
    return

#//==============================================================================================//
#//  Função MAIN( principal ) do robô
#//==============================================================================================//

async def main():
    # Inicia a thread do robô
    servo(120)
    threading.Thread(target=robot_face_update, daemon=True).start()
    print('// -- Program Started! -- < Hello AL_Gorithm!  > -- ')
    config.ROBOT_EXPRESSION_INDEX = 1

    #await test()

    await ato_1() #executa o ato 1
    await ato_2() #executa o ato 2
    await ato_3() #executa o ato 3
    await ato_4() #executa o ato 4
    await FINALROBOTTALK() #executa a fala final
    
    print('codigo finalizado!')

if __name__ == "__main__":
    asyncio.run(main())
