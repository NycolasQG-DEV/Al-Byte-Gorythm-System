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

    # Start threads for blinking and eye animation
    threading.Thread(target=blink_eyes, args=(eye_position,), daemon=True).start()
    threading.Thread(target=animate_eyes, args=(eye_position,), daemon=True).start()

    # Servo control variables
    last_servo_update = time.time()
    smoothed_error_y = 0  # Stores smoothed error
    last_servo_value = None  # Last value sent to the servo

    def stop_all():
        if not audio.pygame.mixer.get_init():
            audio.pygame.mixer.init()
        audio.pygame.mixer.music.stop()
        stopMove()
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

            # Parameters adjusted for more speed and sensitivity
            Kp_min = 0.05
            Kp_max = 0.25
            area_max = 10000
            servo_delay = 0.05
            alpha = 0.5

            # Error calculation
            error_y = face_center_y - img_center_y
            smoothed_error_y = alpha * error_y + (1 - alpha) * smoothed_error_y

            area = w * h
            normalized_area = min(area / area_max, 1.0)
            Kp = Kp_min + (Kp_max - Kp_min) * normalized_area

            delta = int(Kp * smoothed_error_y)
            delta = max(-6, min(6, delta))

            current_time = time.time()
            if abs(smoothed_error_y) > 5 and abs(delta) >= 1 and (current_time - last_servo_update) > servo_delay:
                new_servo_value = max(85, min(110, config._SERVO + delta))
                if new_servo_value != last_servo_value:
                    config._SERVO = new_servo_value
                    servo(config._SERVO)
                    last_servo_value = config._SERVO
                    last_servo_update = current_time

            # Motor control based on horizontal position
            if abs(face_center_x - img_center_x) < 200 and w * h >= 2000:
                config.CENTRALIZE_CODEY = True
            else:
                config.CENTRALIZE_CODEY = False

            if config.TRACKING:
                error_x = face_center_x - img_center_x
                smoothed_error_x = 0.5 * error_x + 0.5 * getattr(config, "SMOOTHED_ERROR_X", 0)
                config.SMOOTHED_ERROR_X = smoothed_error_x

                movement_delay = 0.15
                movement_last = getattr(config, "LAST_MOVEMENT_TIME", 0)

                if (time.time() - movement_last) > movement_delay:
                    moved = False
                    abs_error = abs(smoothed_error_x)

                    def dynamic_speed(error, max_speed=150, min_speed=80, max_error=150):
                        error = abs(error)
                        if error > max_error:
                            return max_speed
                        speed = int(min_speed + (max_speed - min_speed) * (error / max_error))
                        return min(speed, max_speed)

                    speed = dynamic_speed(smoothed_error_x)

                    if smoothed_error_x < -120:
                        print(f'Large error to the left - Turning right (turnRight)')
                        turnLeft(240)
                        moved = True
                    elif smoothed_error_x > 120:
                        print(f'Large error to the right - Turning left (turnLeft)')
                        turnRight(240)
                        moved = True
                    elif smoothed_error_x < -70:
                        print(f'Medium error to the left - Moving right (moveRight) with speed {speed}')
                        moveRight(speed)
                        moved = True
                    elif smoothed_error_x > 70:
                        print(f'Medium error to the right - Moving left (moveLeft) with speed {speed}')
                        moveLeft(speed)
                        moved = True
                    elif abs_error < 80:
                        forward_speed = 140
                        print(f'Face centered - Moving forward with speed {forward_speed}')
                        moveFwd(forward_speed)
                        moved = True

                    if moved:
                        config.LAST_MOVEMENT_TIME = time.time()
                    else:
                        stopMove()

                if w * h >= 12000:
                    print("Face too close - Stopping smoothly")
                    stopMove()
                    time.sleep(0.2)
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
