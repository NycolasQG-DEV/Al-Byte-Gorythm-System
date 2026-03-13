import threading
import cv2
import os
import time
from functions.camera import Camera
from functions.cv_detector import FaceDetectorWrapper, HandDetectorWrapper
from functions.eye_position import EyePosition, blink_eyes, animate_eyes
from commands import *
import functions.audio as audio
import config

def robot_face_update():
    camera = Camera()
    face_detector = FaceDetectorWrapper()
    hand_detector = HandDetectorWrapper()
    window_width = int(camera.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    window_height = int(camera.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    eye_position = EyePosition(window_width, window_height)

    # Iniciar threads para piscada e animação dos olhos
    threading.Thread(target=blink_eyes, args=(eye_position,)).start()
    threading.Thread(target=animate_eyes, args=(eye_position,)).start()

    # Variáveis de controle do servo
    last_servo_update = time.time()
    smoothed_error_y = 0  # Armazena erro suavizado

    def stop_all():
        if not audio.pygame.mixer.get_init():
            audio.pygame.mixer.init()
        audio.pygame.mixer.music.stop()
        stopMove();
        cv2.destroyAllWindows()
        os._exit(0)

    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            stop_all()

    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", click_event)

    while True:
        start_time = time.time()

        img = camera.get_frame()
        img, bboxs = face_detector.detect_faces(img)
        img, hands = hand_detector.detect_hands(img)

        if not config.SHOW_CAMERA:
            cv2.rectangle(img, (0, 0), (window_width, window_height), config.BACKGROUND_COLOR, cv2.FILLED)

        if bboxs:
            closest_face = min(bboxs, key=lambda b: b['bbox'][2] * b['bbox'][3])
            x, y, w, h = closest_face['bbox']
            face_center_x, face_center_y = x + w // 2, y + h // 2
            img_center_x, img_center_y = window_width // 2, window_height // 2

            config.FACE_CENTER_X = face_center_x
            config.FACE_CENTER_Y = face_center_y
            config.IMG_CENTER_X = img_center_x
            config.IMG_CENTER_Y = img_center_y

            # Parâmetros ajustados para mais velocidade e sensibilidade
            Kp_min = 0.05  # Aumentado
            Kp_max = 0.25  # Aumentado para resposta mais forte quando o rosto está próximo
            area_max = 10000
            servo_delay = 0.05  # Menor atraso para resposta mais rápida
            alpha = 0.5  # Suavização um pouco menor para responder mais rápido

            # Cálculo do erro
            error_y = face_center_y - img_center_y

            # Inicialize smoothed_error_y = 0 antes do loop principal
            smoothed_error_y = alpha * error_y + (1 - alpha) * smoothed_error_y

            # Cálculo do ganho proporcional com base na área
            area = w * h
            normalized_area = min(area / area_max, 1.0)
            Kp = Kp_min + (Kp_max - Kp_min) * normalized_area

            # Cálculo do ajuste do servo (delta)
            delta = int(Kp * smoothed_error_y)

            # Aumentar limite de delta para permitir movimentos maiores se necessário
            delta = max(-6, min(6, delta))

            # Menor zona morta (mais sensível ao centro)
            current_time = time.time()
            if abs(smoothed_error_y) > 5 and abs(delta) >= 1 and (current_time - last_servo_update) > servo_delay:
                config._SERVO = max(75, min(100, config._SERVO + delta))
                servo(config._SERVO)
                last_servo_update = current_time


            # Controle dos motores baseado na horizontal
            if abs(face_center_x - img_center_x) < 200 and w * h >= 2000:
                config.CENTRALIZE_CODEY = True
            else:
                config.CENTRALIZE_CODEY = False

            if config.TRACKING:
                                # Suavização horizontal
                error_x = face_center_x - img_center_x
                smoothed_error_x = 0.5 * error_x + 0.5 * getattr(config, "SMOOTHED_ERROR_X", 0)
                config.SMOOTHED_ERROR_X = smoothed_error_x  # salva no config para manter o histórico

                movement_delay = 0.15  # Delay maior para suavidade
                movement_last = getattr(config, "LAST_MOVEMENT_TIME", 0)

                if config.TRACKING and (time.time() - movement_last) > movement_delay:
                    moved = False
                    if smoothed_error_x < -60:
                        print('Rosto à esquerda - Movendo para direita suavemente')
                        moveRight(120)
                        moved = True
                    elif smoothed_error_x > 60:
                        print('Rosto à direita - Movendo para esquerda suavemente')
                        moveLeft(120)
                        moved = True
                    elif abs(smoothed_error_x) < 40:
                        print('Rosto centralizado - Movendo para frente suavemente')
                        moveFwd(150)
                        moved = True

                    if moved:
                        config.LAST_MOVEMENT_TIME = time.time()
                    else:
                        stopMove()

                # Quando muito próximo, parar com suavidade
                if w * h >= 12000:
                    print("Rosto muito próximo - parando com suavidade")
                    stopMove()
                    time.sleep(0.2)  # pequeno delay para evitar repetição
                    config.TRACKING = False


        eye_position.draw(img)

        if hands:
            fingers_count = [hand_detector.detector.fingersUp(hand).count(1) for hand in hands]
            distance, midpoint = hand_detector.measure_distance_between_index_fingers(hands)
            config.FCOUNT = fingers_count
            if distance is not None:
                config.IDISTANCE = distance

        cv2.imshow("Image", img)

        elapsed_time = time.time() - start_time
        if elapsed_time < 0.033:
            time.sleep(0.033 - elapsed_time)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_all()
            break

    camera.release()
