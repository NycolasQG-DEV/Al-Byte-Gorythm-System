import threading
import cv2
import os
import time
from functions.camera import Camera
from functions.cv_detector import FaceDetectorWrapper, HandDetectorWrapper
from functions.eye_position import EyePosition, blink_eyes, animate_eyes
from commands import parar_motores, iniciar_motor, servo, andar_frente
import functions.audio as audio
import config

def robot_face_update():
    camera = Camera()
    face_detector = FaceDetectorWrapper()
    hand_detector = HandDetectorWrapper()  # Inicializar o HandDetectorWrapper
    window_width = int(camera.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    window_height = int(camera.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    eye_position = EyePosition(window_width, window_height)

    # Iniciar threads para piscada e animação dos olhos
    threading.Thread(target=blink_eyes, args=(eye_position,)).start()
    threading.Thread(target=animate_eyes, args=(eye_position,)).start()

    def stop_all():
        if not audio.pygame.mixer.get_init():  # Evita reinicialização desnecessária
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
        start_time = time.time()

        img = camera.get_frame()  # Captura cada frame
        img, bboxs = face_detector.detect_faces(img)  # Detectar rostos
        img, hands = hand_detector.detect_hands(img)  # Detectar mãos

        # Mostrar fundo apenas se a câmera estiver desativada
        if not config.SHOW_CAMERA:
            cv2.rectangle(img, (0, 0), (window_width, window_height), config.BACKGROUND_COLOR, cv2.FILLED)

        if bboxs:  # Se rostos forem detectados
            closest_face = min(bboxs, key=lambda b: b['bbox'][2] * b['bbox'][3])  # Encontra a face mais próxima
            x, y, w, h = closest_face['bbox']
            face_center_x, face_center_y = x + w // 2, y + h // 2
            img_center_x, img_center_y = window_width // 2, window_height // 2

            config.FACE_CENTER_X = face_center_x
            config.FACE_CENTER_Y = face_center_y
            config.IMG_CENTER_X = img_center_x
            config.IMG_CENTER_Y = img_center_y

            # Controle do servo com base na posição do rosto
            if abs(face_center_y - img_center_y) > 25:
                config._SERVO = max(75, min(135, config._SERVO + (5 if face_center_y < img_center_y else -5)))
                servo(config._SERVO)

            # Centralizar e parar motores se o rosto estiver próximo
            if abs(face_center_x - img_center_x) < 200 and w * h >= 2000:
                config.CENTRALIZE_CODEY = True
            else:
                config.CENTRALIZE_CODEY = False

            if config.TRACKING:
                if face_center_x < img_center_x - 50:
                    print('rosto a esquerda!')
                    iniciar_motor(config.ESQUERDO, -250)
                    

                    
                elif face_center_x > img_center_x + 50:
                    print('rosto a direita!')
                    iniciar_motor(config.DIREITO, -250)
                    

                    
                elif face_center_x > img_center_x - 50 and face_center_x < img_center_x + 50:
                    andar_frente(160, 160)
                    print('frente')


                if w * h >= 6000:
                    parar_motores()
                    config.TRACKING = False

        # Desenhar os olhos independentemente de detectar rostos
        eye_position.draw(img)

        # Processar detecção de mãos, apenas se detectadas
        if hands:
            fingers_count = [hand_detector.detector.fingersUp(hand).count(1) for hand in hands]
            distance, midpoint = hand_detector.measure_distance_between_index_fingers(hands)
            config.FCOUNT = fingers_count
            if distance is not None:
                config.IDISTANCE = distance

        # Mostrar imagem na janela
        cv2.imshow("Image", img)

        # Controle de FPS para garantir performance
        elapsed_time = time.time() - start_time
        if elapsed_time < 0.033:  # Aproximadamente 30 FPS
            time.sleep(0.033 - elapsed_time)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_all()
            break

    camera.release()
