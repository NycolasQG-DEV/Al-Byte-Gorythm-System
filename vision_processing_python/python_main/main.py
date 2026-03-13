import threading
import asyncio
import config

from functions.robot import robot_face_update
from functions.audio import play_audio
from functions.send_message import send_message
from commands import * 

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
    await asyncio.sleep(10) #Esperar 10 segundos
    await wait_single_hand_ok(5) #Ler 5 dedos
    config.ROBOT_EXPRESSION_INDEX = 2 #Expressão entediado
    moveFwd(150,4) #Andar para frente
    await asyncio.sleep(4.5) #Esperar 4,5 segundos 
    config.ROBOT_EXPRESSION_INDEX = 5 #Olho esquerdo fechado e direito aberto
    play_audio('./main/audio_files/1.mp3')
    await asyncio.sleep(3) #Esperar 3 segundos
    servo(90) #Motor servo da camera em 90 graus
    turnRight(255, 2) #Girar para direita
    await asyncio.sleep(1) #Esperar 1 segundo
    stopMove() #Parar motores
    await asyncio.sleep(2) #Esperar 2 segundos
    turnLeft(255) #Girar para esquerda
    await asyncio.sleep(3) #Esperar 3 segundos
    return

#//==============================================================================================//
#// -- programação ATO 2 //
#//==============================================================================================//
async def ato_2():
    await wait_centralize_codey() #Centralizar com Codey
    stopMove() #Parar motores
    await asyncio.sleep(7) #Esperar 7 segundos
    config.ROBOT_EXPRESSION_INDEX = 3 #Expressão brava
    play_audio('./main/audio_files/2.mp3')
    moveBwd(130,2.5) #Andar para trás
    await asyncio.sleep(14) #Esperar 14 segundos
    config.ROBOT_EXPRESSION_INDEX = 4 # Olho esquerdo aberto e direito fechado
    turnRight(255,2) #Girar para a direita
    play_audio('./main/audio_files/3.mp3')
    await asyncio.sleep(3) #Esperar 3 segundos
    turnLeft(255) #Girar para a esquerda
    config.ROBOT_EXPRESSION_INDEX = 3 #Expressão brava
    await asyncio.sleep(1) #Esperar 1 segundo
    await wait_centralize_codey() #Centralizar com Codey
    await asyncio.sleep(16) #Esperar 16 segundos
    play_audio('./main/audio_files/4.mp3')
    await asyncio.sleep(5) #Esperar 5 segundos
    config.ROBOT_EXPRESSION_INDEX = 1 #Expressão neutra
    moveBwd(130,5) #Andar para trás
    await asyncio.sleep(8) #Esperar 8 segundos
    return

#//==============================================================================================//
#// -- programação ATO 3 //
#//==============================================================================================//
async def ato_3():
    config.ROBOT_EXPRESSION_INDEX = 3 #Expressão brava
    play_audio('./main/audio_files/5.mp3')
    await asyncio.sleep(8) #Esperar 8 segundos
    config.ROBOT_EXPRESSION_INDEX = 7 #Ponto e virgula
    config.TRACKING = True; #Iniciar perseguição
    await asyncio.sleep(3); #Esperar 3 segundos
    await wait_stop_tracking(); #Esperar o robô parar de seguir
    if config.FACE_CENTER_X < config.IMG_CENTER_X : #Verificar centralição do robô em relação ao Codey
        turnLeft(255); #Girar para a esquerda         
    elif config.FACE_CENTER_X > config.IMG_CENTER_X : #Verificar centralição do robô em relação ao Codey        
        turnRight(255); #Girar para a direita
    await wait_centralize_codey() #Centralizar com Codey
    stopMove(); #Parar motores
    await asyncio.sleep(2) #Esperar 2 segundos
    config.ROBOT_EXPRESSION_INDEX = 3 #Expressão brava
    play_audio('./main/audio_files/6.mp3')
    await asyncio.sleep(7) #Esperar 7 segundos
    config.ROBOT_EXPRESSION_INDEX = 5 # Olho esquerdo fechado e direito aberto
    play_audio('./main/audio_files/7.mp3')
    await asyncio.sleep(12) #Esperar 12 segundos
    moveBwd(150, 5) #Centralizar com Codey
    return

#//==============================================================================================//
#// -- programação ATO 4 //
#//==============================================================================================//
async def ato_4():
    config.ROBOT_EXPRESSION_INDEX = 3 #Expressão brava
    play_audio('./main/audio_files/8.mp3')
    await asyncio.sleep(15) #Esperar 15 segundos
    play_audio('./main/audio_files/9.mp3')
    await asyncio.sleep(4) #Esperar 4 segundos
    config.ROBOT_EXPRESSION_INDEX = 1 #Expressão neutra
    await asyncio.sleep(14) #Esperar 14 segundos
    config.ROBOT_EXPRESSION_INDEX = 3 #Expressão brava
    play_audio('./main/audio_files/10.mp3')
    await asyncio.sleep(3) #Esperar 3 segundos
    config.ROBOT_EXPRESSION_INDEX = 7 #Ponto e virgula
    moveFwd(150, 3) #Andar para frente
    await asyncio.sleep(5) #Esperar 5 segundos
    await wait_both_hand_ok(5, 5) #Ler 5 dedos de ambas as mãos
    play_audio('./main/audio_files/erro.mp3')
    config.ROBOT_EXPRESSION_INDEX = 8 #Tela azul
    await asyncio.sleep(70) #Esperar 70 segundos = 1 minuto e 10 segundos
    play_audio('./main/audio_files/start.mp3')
    await asyncio.sleep(5) #Esperar 5 segundos
    config.ROBOT_EXPRESSION_INDEX = 9 #Expressão Triste
    config.EYE_COLOR = (255, 150, 150) #Olho ciano
    turnRight(255, 2) #Girar para a direira
    play_audio('./main/audio_files/11.mp3')
    await asyncio.sleep(20) #Esperar 20 segundos
    config.ROBOT_EXPRESSION_INDEX = 6 #Expressão Rindo
    play_audio('./main/audio_files/12.mp3')
    await asyncio.sleep(1) #Esperar 1 segundo
    config.ROBOT_EXPRESSION_INDEX = 1 #Expressão neutra
    await asyncio.sleep(14) #Esperar 14 segundos
    play_audio('./main/audio_files/erro.mp3')
    config.ROBOT_EXPRESSION_INDEX = 3 #Expressão brava
    config.EYE_COLOR = (255, 0, 255) #Olho roxo
    await asyncio.sleep(3) #Esperar 3 segundos
    config.ROBOT_EXPRESSION_INDEX = 1 #Expressão neutra
    config.EYE_COLOR = (255, 150, 150) #Olho ciano
    await asyncio.sleep(20) #Esperar 20 segundos
    print('codigo finalizado!')
    return

#//==============================================================================================//
#// -- funções extras //
#//==============================================================================================//
async def wait_stop_tracking():
     while config.TRACKING:  # Verifica se config.TRACKING é True
         await asyncio.sleep(0.1)  # Espera 100ms antes de verificar novamente
     print("config.TRACKING mudou para False!")

async def wait_centralize_codey():
    while not config.CENTRALIZE_CODEY:  # Verifica se config.CENTRALIZE_CODEY é False
        await asyncio.sleep(0.1)  # Espera 100ms antes de verificar novamente
    stopMove(); #Parar motores
    print("codey centralizado!")



#//==============================================================================================//
#//  Função MAIN( principal ) do robô
#//==============================================================================================//

async def main():
    # Inicia a thread do robô
    servo(90)
    threading.Thread(target=robot_face_update, daemon=True).start()
    print('// -- Program Started! -- < Hello AL_Gorithm!  > -- ')
    config.ROBOT_EXPRESSION_INDEX = 1 #Expressão neutra

    #await test()

    await ato_1() #executa o ato 1
    await ato_2() #executa o ato 2
    await ato_3() #executa o ato 3
    await ato_4() #executa o ato 4

if __name__ == "__main__":
    asyncio.run(main())
