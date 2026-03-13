import threading
import asyncio
import config

import cv2
import pygame
from moviepy.editor import VideoFileClip

from functions.robot import robot_face_update
from functions.audio import play_audio
from functions.send_message import send_message
from commands import iniciar_motor, mover_tanque, girar_graus, parar_motores, mover_para_tras, servo
from main import wait_single_hand_ok, wait_both_hand_ok, ato_1, ato_2, ato_3, ato_4, FINALROBOTTALK, wait_centralize_codey, wait_stop_tracking

# Caminho do vídeo
video_path = 'video_files/entrevista.mp4'

def entrevista_video():
    # Carrega o vídeo usando moviepy
    video_clip = VideoFileClip(video_path)
    
    # Reproduz o vídeo (já sincronizado com o áudio)
    video_clip.preview()

async def entrevista_codigo():
    # Cria uma thread para executar o vídeo
        video_thread = threading.Thread(target=entrevista_video)
        video_thread.start()
        await asyncio.sleep(21)

        mover_tanque(140,150, 1.5)
        print('moveu para frente')
        await asyncio.sleep(3)
        mover_para_tras(150)
        print('moveu para tras')
        await asyncio.sleep(1.2)
        parar_motores()

        await asyncio.sleep(2)
        await asyncio.sleep(0.5)
        servo(120)
        print('servo para cima')
        await asyncio.sleep(0.5)
        servo(90)
        print('servo para baixo')
        await asyncio.sleep(0.5)
        servo(120)
        print('servo para cima')
        await asyncio.sleep(0.5)
        servo(90)
        print('servo para baixo')
        await asyncio.sleep(0.5)

        print('codigo finalizado!')

# Inicia o servo (ou outros processos do robô)
servo(90)
threading.Thread(target=robot_face_update, daemon=True).start()
config.ROBOT_EXPRESSION_INDEX = 0
print('// -- Program Started! -- < Hello AL_Gorithm! > --')

async def main():
    await wait_single_hand_ok(5)#faz a primeira detecção
    await asyncio.sleep(1)#espera um tempo
    if (config.FCOUNT[0] == 5):#verifica se o commando esta correto. se sim, ele inicia a apresentação. se não, ele volta o looping
        await entrevista_codigo()
    else:
         await main()

if __name__ == "__main__":
    asyncio.run(main())
