import threading
import cv2
import time
from functions.camera import Camera
from functions.cv_detector import FaceDetectorWrapper, HandDetectorWrapper
from functions.eye_position import EyePosition, blink_eyes, animate_eyes
from commands import parar_motores, iniciar_motor, mover_tanque, girar_graus, mover_para_tras,  servo
#from send_message import send_message
import os
import functions.audio as audio
import config

#atualiza e deixa o rosto do robô funcionando
def robot_face_update():
    camera = Camera()
    face_detector = FaceDetectorWrapper()
    hand_detector = HandDetectorWrapper()  # Inicializar o HandDetectorWrapper
    window_width = int(camera.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    window_height = int(camera.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    eye_position = EyePosition(window_width, window_height)

    threading.Thread(target=blink_eyes, args=(eye_position,)).start()
    threading.Thread(target=animate_eyes, args=(eye_position,)).start()

    def stop_all():
        audio.pygame.mixer.init()
        audio.pygame.mixer.music.stop()
        parar_motores()
        cv2.destroyAllWindows()
        os._exit(0)

    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            stop_all()

    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", click_event)

    while True:
        img = camera.get_frame()
        img, bboxs = face_detector.detect_faces(img)
        img, hands = hand_detector.detect_hands(img)  # Detectar as mãos

        # Limpar a tela do robô
        cv2.rectangle(img, (0, 0), (window_width, window_height), config.BACKGROUND_COLOR, cv2.FILLED)

        if bboxs:
            closest_face = None
            min_distance = float('inf')

            for bbox in bboxs:
                x, y, w, h = bbox['bbox']
                distance = w * h

                if distance < min_distance:
                    min_distance = distance
                    config.CODEY_DISTANCE = min_distance
                    closest_face = bbox

                if closest_face:
                    x, y, w, h = closest_face['bbox']
                    face_center_x = x + w // 2
                    face_center_y = y + h // 2
                    img_center_x = window_width // 2
                    img_center_y = window_height // 2

                    config.FACE_CENTER_X = face_center_x
                    config.FACE_CENTER_Y = face_center_y
                    config.IMG_CENTER_X = img_center_x
                    config.IMG_CENTER_Y = img_center_y

                if face_center_y < img_center_y - 25:
                    #print("Rosto está à cima")
                    if config._SERVO <= 130:
                        config._SERVO+=5
                    else:
                        config._SERVO = 135
                elif face_center_y > img_center_y + 25:
                    #print("Rosto está à baixo")
                    if config._SERVO >= 80:
                        config._SERVO-=5
                    else:
                        config._SERVO = 75



                if config._SERVO >= 75:
                    time.sleep(0.1)
                    servo(config._SERVO)

                if face_center_x > img_center_x - 200 and face_center_x < img_center_x + 200 and min_distance >=2000:
                    config.CENTRALIZE_CODEY = True
                    #print('codey no centro')
                else:
                    config.CENTRALIZE_CODEY = False

                

                if config.TRACKING:

                    if face_center_x < img_center_x :
                        print("Rosto está à esquerda")
                        
                        iniciar_motor(config.DIREITO, 250)
                        
                        
                    elif face_center_x > img_center_x :
                        print("Rosto está à direita")
                        
                        iniciar_motor(config.ESQUERDO, 250)
                        
                    if min_distance >= 4000:
                        parar_motores()    
                        config.TRACKING = False
                  
            eye_position.draw(img)
        else:
            eye_position.draw(img)

        # Processar detecção de mãos
        if hands:
            fingers_count = []
            for hand in hands:
                fingers = hand_detector.detector.fingersUp(hand)
                fingers_count.append(fingers.count(1))

            distance, midpoint = hand_detector.measure_distance_between_index_fingers(hands)
            if distance is not None:
                config.FCOUNT = fingers_count
                config.IDISTANCE = distance
            else:
                config.FCOUNT = fingers_count


        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_all()
            break

    camera.release()
