import threading
import asyncio
import config

from functions.robot import robot_face_update
from functions.audio import play_audio
from functions.send_message import send_message
from commands import * 

#//==============================================================================================//
#//  Al B. Gorithm -- code by Hortobots team 2024/2025
#// 
#//  * Nycolas Queiroz Gimenez     
#//  * Tiago Ferreira Gregório
#//  * Luiz Otavio Siqueira
#//  * Nicolas Paiva Medeiros                          
#//                         
#//==============================================================================================//
motor_direito, motor_esquerdo = config.DIREITO, config.ESQUERDO

#function to pause for 2-hand gesture detection
async def wait_both_hand_ok(finger_count_left_hand, finger_count_right_hand):
    while True:
        if len(config.FCOUNT) > 1:
            if config.FCOUNT[0] == finger_count_left_hand and config.FCOUNT[1] == finger_count_right_hand:
                return
        await asyncio.sleep(0.1)  # Non-blocking wait

#function to pause for 1-hand gesture detection
async def wait_single_hand_ok(finger_count):
    while True:
        if len(config.FCOUNT) > 0:
            if config.FCOUNT[0] == finger_count:
                return
        await asyncio.sleep(0.1)  # Non-blocking wait

#//==============================================================================================//
#//  Presentation script programming
#//==============================================================================================//

#// -- ACT 1 programming //
async def ato_1():
    await asyncio.sleep(10) 
    await wait_single_hand_ok(5) 
    config.ROBOT_EXPRESSION_INDEX = 2 
    moveFwd(150,4) 
    await asyncio.sleep(4.5) 
    config.ROBOT_EXPRESSION_INDEX = 5 
    play_audio('./main/audio_files/1.mp3')
    await asyncio.sleep(2.5) 
    servo(90) 
    config.ROBOT_EXPRESSION_INDEX = 3
    turnRight(255, 2) 
    await asyncio.sleep(2.5) 
    stopMove() 
    await asyncio.sleep(1.5) 
    config.ROBOT_EXPRESSION_INDEX = 2
    turnLeft(255) 
    await asyncio.sleep(1.5) 
    return

#// -- ACT 2 programming //
async def ato_2():
    await wait_centralize_codey() 
    stopMove() 
    await asyncio.sleep(7) 
    config.ROBOT_EXPRESSION_INDEX = 3 
    play_audio('./main/audio_files/2.mp3')
    moveBwd(140,2.5) 
    await asyncio.sleep(3)
    config.ROBOT_EXPRESSION_INDEX = 2
    await asyncio.sleep(11) 
    turnRight(255,2) 
    play_audio('./main/audio_files/3.mp3')
    config.ROBOT_EXPRESSION_INDEX = 4
    await asyncio.sleep(3)
    turnLeft(255) 
    await asyncio.sleep(2.5)
    await wait_centralize_codey()
    config.ROBOT_EXPRESSION_INDEX = 2
    await asyncio.sleep(3) 
    config.ROBOT_EXPRESSION_INDEX = 3
    await asyncio.sleep(10) 
    play_audio('./main/audio_files/4.mp3')
    await asyncio.sleep(5) 
    config.ROBOT_EXPRESSION_INDEX = 1 
    moveBwd(130,5) 
    await asyncio.sleep(8) 
    return

#// -- ACT 3 programming //
async def ato_3():
    config.ROBOT_EXPRESSION_INDEX = 3 
    play_audio('./main/audio_files/5.mp3')
    await asyncio.sleep(8) 
    config.ROBOT_EXPRESSION_INDEX = 7
    config.TRACKING = True; 
    await asyncio.sleep(3); 
    await wait_stop_tracking(); 
    if config.FACE_CENTER_X < config.IMG_CENTER_X :
        turnLeft(255);         
    elif config.FACE_CENTER_X > config.IMG_CENTER_X :      
        turnRight(255); 
    await asyncio.sleep(0.5)
    await wait_centralize_codey() 
    stopMove(); 
    await asyncio.sleep(3) 
    config.ROBOT_EXPRESSION_INDEX = 3 
    play_audio('./main/audio_files/6.mp3')
    await asyncio.sleep(8) 
    config.ROBOT_EXPRESSION_INDEX = 5 
    play_audio('./main/audio_files/7.mp3')
    await asyncio.sleep(1)
    config.ROBOT_EXPRESSION_INDEX = 2
    await asyncio.sleep(3)
    moveBwd(150, 5) 
    await asyncio.sleep(9) 
    return

#// -- ACT 4 programming //
async def ato_4():
    turnRight(255, 2)
    config.ROBOT_EXPRESSION_INDEX = 3 
    play_audio('./main/audio_files/8.mp3')
    await asyncio.sleep(4)
    config.ROBOT_EXPRESSION_INDEX = 2
    await asyncio.sleep(11) 
    config.ROBOT_EXPRESSION_INDEX = 3
    play_audio('./main/audio_files/9.mp3')
    turnLeft(255) 
    await asyncio.sleep(1);
    await wait_centralize_codey() 
    await asyncio.sleep(4) 
    config.ROBOT_EXPRESSION_INDEX = 1 
    await asyncio.sleep(8) 
    config.ROBOT_EXPRESSION_INDEX = 6
    play_audio('./main/audio_files/10.mp3')
    await asyncio.sleep(1.8) 
    config.ROBOT_EXPRESSION_INDEX = 3 
    await asyncio.sleep(1.2) 
    config.ROBOT_EXPRESSION_INDEX = 7 
    moveFwd(150, 3) 
    await wait_both_hand_ok(5, 5) 
    turnRight(255, 2.6) 
    await asyncio.sleep(2) 
    play_audio('./main/audio_files/erro.mp3')
    config.ROBOT_EXPRESSION_INDEX = 8 
    await asyncio.sleep(65) 
    play_audio('./main/audio_files/start.mp3')
    await asyncio.sleep(5) 
    config.ROBOT_EXPRESSION_INDEX = 9 
    config.EYE_COLOR = (255, 255, 0) 
    turnLeft(255) 
    await asyncio.sleep(1);
    await wait_centralize_codey()
    await asyncio.sleep(2)
    config.ROBOT_EXPRESSION_INDEX = 1
    play_audio('./main/audio_files/11.mp3')
    await asyncio.sleep(1) 
    config.ROBOT_EXPRESSION_INDEX = 9
    await asyncio.sleep(19) 
    play_audio('./main/audio_files/12.mp3')
    turnRight(255, 2) 
    config.ROBOT_EXPRESSION_INDEX = 6
    await asyncio.sleep(2) 
    config.ROBOT_EXPRESSION_INDEX = 1 
    await asyncio.sleep(14) 
    play_audio('./main/audio_files/erro.mp3')
    config.ROBOT_EXPRESSION_INDEX = 3 
    config.EYE_COLOR = (255, 0, 255) 
    await asyncio.sleep(3) 
    config.ROBOT_EXPRESSION_INDEX = 1 
    config.EYE_COLOR = (255, 255, 0) 
    await asyncio.sleep(20) 
    print('The code is finished!')
    return

#//==============================================================================================//
#// -- extra functions //
#//==============================================================================================//
async def wait_stop_tracking():
     while config.TRACKING:  # Check if config.TRACKING is True
         await asyncio.sleep(0.1)  # Wait 100ms before checking again
     print("config.TRACKING is False!")

async def wait_centralize_codey():
    while not config.CENTRALIZE_CODEY:  # Check if config.CENTRALIZE_CODEY is False
        await asyncio.sleep(0.1)  # Wait 100ms before checking again
    stopMove(); 
    print("codey in the center!")



#//==============================================================================================//
#//  Robot MAIN function
#//==============================================================================================//

async def main():
    # Inicia a thread do robô
    adjustMotors(config.M1_ADJUST,config.M2_ADJUST,config.M3_ADJUST,config.M4_ADJUST) # Manual engine calibration
    servo(100)#camera start calibration
    threading.Thread(target=robot_face_update, daemon=True).start()
    print('// -- Program Started! -- < Hello AL_Gorithm!  > -- ')
    config.ROBOT_EXPRESSION_INDEX = 1 

    await ato_1() 
    await ato_2() 
    await ato_3() 
    await ato_4() 

if __name__ == "__main__":
    asyncio.run(main())
