import threading
import asyncio
import config

import cv2
import pygame
from moviepy.editor import VideoFileClip

from functions.robot import robot_face_update
from commands import * 
from main import wait_single_hand_ok
# video path
video_path = 'main/video_files/interview.mp4'

def video_interview():
    # Load the video using moviepy
    video_clip = VideoFileClip(video_path)
    
    # Play the video (already synchronized with the audio)
    video_clip.preview()

async def code_interview():
    # Create a thread to play the video
        video_thread = threading.Thread(target=video_interview)
        video_thread.start()
        await asyncio.sleep(21)


        print('The code is finished!')

servo(100)
threading.Thread(target=robot_face_update, daemon=True).start()
config.ROBOT_EXPRESSION_INDEX = 0
print('// -- Program Started! -- < Hello AL_Gorithm! > --')

async def main():
    await wait_single_hand_ok(5)#do the first detection
    await asyncio.sleep(1)
    if (config.FCOUNT[0] == 5):#check if the command is correct. If yes, it starts a presentation. If not, it resumes the looping.
        await code_interview()
    else:
         await main()

if __name__ == "__main__":
    asyncio.run(main())
