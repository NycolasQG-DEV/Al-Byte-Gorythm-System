import time
import cv2
import numpy as np
import config

#instancia dos olhos do robô
class EyePosition:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.left_eye_x = window_width // 2 - 100
        self.right_eye_x = window_width // 2 + 100
        self.circle_y = window_height // 2
        self.blink_state = False  # Estado dos olhos (abertos ou fechados)
        self.min_eye_distance = 200  # Distância mínima entre os olhos
        self.movement_offset = 0
        self.movement_direction = 1

    def draw(self, img):
        circle_radius = 60
        _state = config.ROBOT_EXPRESSION_INDEX

        if self.blink_state and _state != 6 and _state != 7 and _state != 0:
            config.BACKGROUND_COLOR = (0,0,0)
            # Olho fechado
            cv2.rectangle(img, (int(self.left_eye_x - circle_radius), int(self.circle_y - 5)),
                          (int(self.left_eye_x + circle_radius), int(self.circle_y + 5)), config.EYE_COLOR, cv2.FILLED)
            cv2.rectangle(img, (int(self.right_eye_x - circle_radius), int(self.circle_y - 5)),
                          (int(self.right_eye_x + circle_radius), int(self.circle_y + 5)), config.EYE_COLOR, cv2.FILLED)
        else:
            # Olho padrão NEUTRO
            if _state == 1:  
                config.BACKGROUND_COLOR = (0,0,0)
                cv2.circle(img, (int(self.left_eye_x), int(self.circle_y)), circle_radius, config.EYE_COLOR, cv2.FILLED)
                cv2.circle(img, (int(self.right_eye_x), int(self.circle_y)), circle_radius, config.EYE_COLOR, cv2.FILLED)
            
            # Olho padrão ENTEDIADO
            elif _state == 2:  
                config.BACKGROUND_COLOR = (0,0,0)
                cv2.circle(img, (int(self.left_eye_x), int(self.circle_y)), circle_radius, config.EYE_COLOR, cv2.FILLED)
                cv2.circle(img, (int(self.right_eye_x), int(self.circle_y)), circle_radius, config.EYE_COLOR, cv2.FILLED)
                cv2.rectangle(img, (0, int(self.circle_y-100)), (800, int(self.circle_y - 20)), config.BACKGROUND_COLOR, cv2.FILLED)
            
            # Expressão de Raiva
            elif _state == 3:  
                config.BACKGROUND_COLOR = (0,0,0)
                cv2.circle(img, (int(self.left_eye_x), int(self.circle_y)), circle_radius, config.EYE_COLOR, cv2.FILLED)
                cv2.circle(img, (int(self.right_eye_x), int(self.circle_y)), circle_radius, config.EYE_COLOR, cv2.FILLED)
                triangle_points = np.array([
                    [int(self.left_eye_x + circle_radius-90), int(self.circle_y) - 60],
                    [int(self.right_eye_x - circle_radius+90), int(self.circle_y) - 60],
                    [int((self.left_eye_x + self.right_eye_x) // 2), int(self.circle_y + circle_radius -20)] 
                ])
                cv2.fillPoly(img, [triangle_points], config.BACKGROUND_COLOR)

            # Olho esquerdo aberto e direito fechado
            elif _state == 4:  
                config.BACKGROUND_COLOR = (0,0,0)
                cv2.circle(img, (int(self.left_eye_x), int(self.circle_y)), circle_radius, config.EYE_COLOR, cv2.FILLED)
                cv2.circle(img, (int(self.right_eye_x), int(self.circle_y)), circle_radius, config.EYE_COLOR, cv2.FILLED)
                cv2.rectangle(img, (int(self.left_eye_x + 100), int(self.circle_y-100)), (800, int(self.circle_y - 20)), config.BACKGROUND_COLOR, cv2.FILLED)

            # Olho esquerdo fechado e direito aberto
            elif _state == 5:  
                config.BACKGROUND_COLOR = (0,0,0)
                cv2.circle(img, (int(self.left_eye_x), int(self.circle_y)), circle_radius, config.EYE_COLOR, cv2.FILLED)
                cv2.circle(img, (int(self.right_eye_x), int(self.circle_y)), circle_radius, config.EYE_COLOR, cv2.FILLED)
                cv2.rectangle(img, (0, int(self.circle_y-100)), (int(self.right_eye_x - 100), int(self.circle_y - 20)), config.BACKGROUND_COLOR, cv2.FILLED)
            
            # Olho rindo
            elif _state == 6:
                config.BACKGROUND_COLOR = (0,0,0)
                
                # Olho esquerdo
                cv2.line(img, (int(self.left_eye_x) - 40, int(self.circle_y + self.movement_offset) - 40), 
                        (int(self.left_eye_x) + 40, int(self.circle_y + self.movement_offset)), config.EYE_COLOR, thickness=8)
                cv2.line(img, (int(self.left_eye_x) - 40, int(self.circle_y + self.movement_offset) + 40), 
                        (int(self.left_eye_x) + 40, int(self.circle_y + self.movement_offset)), config.EYE_COLOR, thickness=8)
                
                # Olho direito
                cv2.line(img, (int(self.right_eye_x) - 40, int(self.circle_y + self.movement_offset)), 
                        (int(self.right_eye_x) + 40, int(self.circle_y + self.movement_offset) - 40), config.EYE_COLOR, thickness=8)
                cv2.line(img, (int(self.right_eye_x) - 40, int(self.circle_y + self.movement_offset)), 
                        (int(self.right_eye_x) + 40, int(self.circle_y + self.movement_offset) + 40), config.EYE_COLOR, thickness=8)
                
            # PONTO E VÍRGULA
            elif _state == 7:
                 config.BACKGROUND_COLOR = (255,255,255)
                 cv2.putText(img,";", (self.window_width // 2 - 50, self.window_height // 2 + 50),cv2.FONT_HERSHEY_SIMPLEX, 10, (0,0,0), 40, cv2.LINE_AA)
            
            # TELA AZUL ( ERROR SIMULAÇÃO )
            elif _state == 8 :
                config.BACKGROUND_COLOR = (255, 50, 50)
            
            # Olho Triste
            elif _state == 9:  
                config.BACKGROUND_COLOR = (0, 0, 0)

                cv2.circle(img, (int(self.left_eye_x), int(self.circle_y)), circle_radius, config.EYE_COLOR, cv2.FILLED)
                cv2.circle(img, (int(self.right_eye_x), int(self.circle_y)), circle_radius, config.EYE_COLOR, cv2.FILLED)

                cv2.circle(img, (int(self.left_eye_x), int(self.circle_y) - 80) , circle_radius, (0,0,0), cv2.FILLED)
                cv2.circle(img, (int(self.right_eye_x), int(self.circle_y) - 80) , circle_radius, (0,0,0), cv2.FILLED)

    def update_position(self):
        # Atualiza a posição vertical para simular movimento para cima e para baixo
        if self.movement_offset > 20 or self.movement_offset < -20:
            self.movement_direction *= -1
        self.movement_offset += self.movement_direction * 10  # Ajuste a velocidade aqui

    def blink(self):
        # Piscar só se o estado não for 6
        if config.ROBOT_EXPRESSION_INDEX != 6 and config.ROBOT_EXPRESSION_INDEX != 7 and config.ROBOT_EXPRESSION_INDEX != 8:
            self.blink_state = True
            time.sleep(0.1)
            self.blink_state = False

def blink_eyes(eye_position):
    while True:
        time.sleep(5)
        eye_position.blink()

def animate_eyes(eye_position):
    while True:
        time.sleep(0.05)
        eye_position.update_position()


