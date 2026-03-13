import pygame
import copy
import config

# Posições das barras (atuais e anteriores)
bar_positions = {
    "left_upper": [120, 50],
    "left_lower": [120, 525],
    "right_upper": [755, 50],
    "right_lower": [755, 525]
}

# Deep copy para evitar referências entre listas aninhadas
last_bar_positions = copy.deepcopy(bar_positions)

def doExpressionTransition(delay):
    """ Move as barras suavemente até as novas posições """
    global last_bar_positions, bar_positions

    for key in bar_positions:
        target_x, target_y = bar_positions[key]
        last_x, last_y = last_bar_positions[key]

        # Ajuste no eixo X
        if last_x < target_x:
            last_bar_positions[key][0] += min(delay, target_x - last_x)
        elif last_x > target_x:
            last_bar_positions[key][0] -= min(delay, last_x - target_x)

        # Ajuste no eixo Y
        if last_y < target_y:
            last_bar_positions[key][1] += min(delay, target_y - last_y)
        elif last_y > target_y:
            last_bar_positions[key][1] -= min(delay, last_y - target_y)

def drawExpression(screen, expression, delay):
    """ Desenha a expressão no Pygame """
    global bar_positions

    expressions = {
        # Neutra
        1: {"left_upper": [120, 50], "left_lower": [120, 525],
            "right_upper": [755, 50], "right_lower": [755, 525]},
        # Olhos fechados
        2: {"left_upper": [120, 175], "left_lower": [120, 350],
            "right_upper": [755, 175], "right_lower": [755, 350]},
        # Olhos sérios
        3: {"left_upper": [120, 175], "left_lower": [120, 525],
            "right_upper": [755, 175], "right_lower": [755, 525]},
        # Olho esquerdo sério e o direito normal
        4: {"left_upper": [120, 175], "left_lower": [120, 525],
            "right_upper": [755, 50], "right_lower": [755, 525]},
        # Olho direito sério e o esquerdo normal
        5: {"left_upper": [120, 50], "left_lower": [120, 525],
            "right_upper": [755, 175], "right_lower": [755, 525]}
    }

    if expression not in expressions:
        #print("\033[91mErro na função drawExpression! Defina uma expressão válida!!!\033[0m")
        return

    # Atualiza as posições desejadas das barras sem modificar o dicionário original
    bar_positions = copy.deepcopy(expressions[expression])

    #faz a transição das expressões naturalmente
    doExpressionTransition(delay)

    # Desenha os olhos e as barras
    pygame.draw.circle(screen, config.PINK, (config.SCREEN_WIDTH//4, config.SCREEN_HEIGHT//2), 150)  # Olho esquerdo
    pygame.draw.rect(screen, config.BLACK, (*last_bar_positions["left_upper"], 400, 160))
    pygame.draw.rect(screen, config.BLACK, (*last_bar_positions["left_lower"], 400, 160))

    pygame.draw.circle(screen, config.PINK, ((config.SCREEN_WIDTH//4)*3, config.SCREEN_HEIGHT//2), 150)  # Olho direito
    pygame.draw.rect(screen, config.BLACK, (*last_bar_positions["right_upper"], 400, 160))
    pygame.draw.rect(screen, config.BLACK, (*last_bar_positions["right_lower"], 400, 160))

    pygame.display.update()
