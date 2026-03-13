import pygame
import cv2
from cvzone.HandTrackingModule import HandDetector
from global_defs import *
from draw_robot_face import drawExpression

# Inicializa o PyGame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hortobots")

# Inicializa a câmera e o detector de mãos
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Controle de FPS
clock = pygame.time.Clock()
running = True
expression = 1  # Começa na primeira expressão

while running:
    # Captura a imagem da câmera
    success, img = cap.read()
    if success:
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, draw=False)
        
        if hands:
            hand = hands[0]
            fingers = detector.fingersUp(hand)
            expression = sum(fingers)  # Conta quantos dedos estão levantados
    
    # Desenha o rosto na interface
    drawExpression(screen, expression, 10)
    
    # Processa eventos do Pygame para permitir fechar a janela
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    clock.tick(60)  # Mantém o FPS estável

# Libera recursos
cap.release()
cv2.destroyAllWindows()
pygame.quit()
