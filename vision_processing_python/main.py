import pygame
import cv2
import multiprocessing
import asyncio
import atexit
import sys
from cvzone.HandTrackingModule import HandDetector
import config
from draw_robot_face import drawExpression

# Função para rodar o loop principal do Pygame e OpenCV
def main_loop(window_ready, stop_event):
    try:
        pygame.init()
        screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Hortobots")
        
        cap = cv2.VideoCapture(config.CAMERA)
        detector = HandDetector(detectionCon=0.8, maxHands=1)
        
        clock = pygame.time.Clock()
        
        # Confirma que a janela foi aberta
        window_ready.set()
        
        running = True
        while running:
            success, img = cap.read()
            if success:
                img = cv2.flip(img, 1)
                hands, img = detector.findHands(img, draw=False)
                
                if hands:
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    config.EXPRESSION = sum(fingers)
            
            # Desenha o rosto do robô
            drawExpression(screen, config.EXPRESSION, 20)
            
            # Para fechar a janela ao apertar no "X" ou clicar na tela
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.mouse.get_pressed()[0]:
                    running = False
                    stop_event.set()  # Sinaliza para o processo principal encerrar
                    break
            
            clock.tick(60)
    except Exception as e:
        print(f"Erro no loop da câmera: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        pygame.quit()

def start_multi_process():
    manager = multiprocessing.Manager()
    window_ready = manager.Event()
    stop_event = manager.Event()  # Evento para sinalizar encerramento
    process = multiprocessing.Process(target=main_loop, args=(window_ready, stop_event))
    process.start()
    return process, window_ready, stop_event  # Retorna o processo, evento de janela e evento de parada

def terminate_processes(processes):
    """
    Encerra todos os processos em execução.
    
    :param processes: Lista de processos a serem encerrados
    """
    for process in processes:
        if process.is_alive():
            process.terminate()
            process.join()

async def setup(window_ready, stop_event):
    print("Aguardando janela abrir...")
    window_ready.wait()  # Aguarda até que a janela do Pygame esteja pronta
    print("Janela aberta! Iniciando sequência...")
    
    for char in "abcd":
        if stop_event.is_set():  # Interrompe se o evento de parada for acionado
            print("Encerrando setup...")
            return
        print(char)
        await asyncio.sleep(3)
    
if __name__ == "__main__":
    try:
        process, window_ready, stop_event = start_multi_process()
        atexit.register(lambda: terminate_processes([process]))  # Garante finalização ao sair
        asyncio.run(setup(window_ready, stop_event))
    except KeyboardInterrupt:
        print("Encerrando o programa...")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        terminate_processes([process])
        print("Processo finalizado com sucesso!")
        sys.exit(0)
