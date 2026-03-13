import threading
import asyncio
import config

from functions.robot import robot_face_update
from functions.audio import play_audio
from functions.send_message import send_message
from commands import iniciar_motor, mover_tanque, girar_graus, parar_motores, mover_para_tras, servo
from main import wait_single_hand_ok, wait_both_hand_ok, ato_1, ato_2, ato_3, ato_4, FINALROBOTTALK, wait_centralize_codey, wait_stop_tracking

#//==============================================================================================//
#//  Função MAIN( principal ) do robô
#//==============================================================================================//

async def main():
    # Inicia a thread do robô
    servo(120)
    threading.Thread(target=robot_face_update, daemon=True).start()
    print('// -- Program Started! -- < Hello AL_Gorithm!  -- >')
    config.ROBOT_EXPRESSION_INDEX = 1

    await wait_single_hand_ok(5)
    await ato_2() #executa o ato 2
    await ato_3() #executa o ato 3
    await ato_4() #executa o ato 4
    await FINALROBOTTALK() #executa a fala final
    
    print('codigo finalizado!')

if __name__ == "__main__":
    asyncio.run(main())

