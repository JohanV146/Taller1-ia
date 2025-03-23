import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

# Colores
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
BUTTON_COLOR = (73, 189, 176)
HOVER_COLOR = (52, 152, 139)
TEXT_COLOR = (255, 255, 255)
X_COLOR = (84, 84, 84)
O_COLOR = (242, 235, 211)

# Configuración de la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

# Fuentes
title_font = pygame.font.Font(None, 80)
button_font = pygame.font.Font(None, 40)
mode_font = pygame.font.Font(None, 30)

# Variables del juego
board = [[None]*3 for _ in range(3)]
player_turn = True
game_active = False
current_mode = ""
game_over = False
winner = None

def draw_menu():
    screen.fill(BG_COLOR)
    title_text = title_font.render("Tic Tac Toe", True, TEXT_COLOR)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 100))
    
    # Botones de dificultad
    button_y = 250
    modes = ["Principiante", "Intermedio", "Avanzado"]
    for i, mode in enumerate(modes):
        button_rect = pygame.Rect(WIDTH//2 - 100, button_y + i*100, 200, 50)
        color = HOVER_COLOR if button_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
        pygame.draw.rect(screen, color, button_rect, border_radius=10)
        text = button_font.render(mode, True, TEXT_COLOR)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, button_y + i*100 + 15))
    
    pygame.display.update()

def draw_board():
    # Líneas horizontales
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2*SQUARE_SIZE), (WIDTH, 2*SQUARE_SIZE), LINE_WIDTH)
    # Líneas verticales
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2*SQUARE_SIZE, 0), (2*SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                pygame.draw.line(screen, X_COLOR, 
                               (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                               (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), 
                               CROSS_WIDTH)
                pygame.draw.line(screen, X_COLOR, 
                               (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                               (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), 
                               CROSS_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, O_COLOR, 
                                 (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), 
                                  int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), 
                                 CIRCLE_RADIUS, CIRCLE_WIDTH)

def draw_game_info():
    # Modo de juego
    mode_text = mode_font.render(f"Modo: {current_mode}", True, TEXT_COLOR)
    screen.blit(mode_text, (20, 10))
    
    # Turno actual
    turn_text = mode_font.render(
        "Turno: Jugador" if player_turn else "Turno: IA", 
        True, 
        TEXT_COLOR
    )
    screen.blit(turn_text, (WIDTH - turn_text.get_width() - 20, 10))

def check_win():
    # Verificar filas y columnas
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]
    # Verificar diagonales
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None

def check_tie():
    return all(cell is not None for row in board for cell in row)

def get_empty_cells():
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] is None]

def ai_beginner():
    empty_cells = get_empty_cells()
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = 'O'
        return True
    return False

def ai_intermediate():
    move = get_best_move()
    if move:
        row, col = move
        board[row][col] = 'O'
        return True
    return False

def MiniMaxIntermedio(board, depth, isMax, alpha, beta):
    #comprueba si ya alguien ha ganado o si hay un empate
    if check_win() == 'O':
        return 1
    elif check_win() == 'X':
        return -1
    elif check_tie() or depth >= 3:
        return 0
    
    if isMax:
        best = -float('inf')
        for row, col in get_empty_cells():
            board[row][col] = 'O'
            value = MiniMaxIntermedio(board, depth+1, False, alpha, beta)
            board[row][col] = None
            best = max(value, best)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = float('inf')
        for row, col in get_empty_cells():
            board[row][col] = 'X'
            value = MiniMaxIntermedio(board, depth+1, True, alpha, beta)
            board[row][col] = None
            best = min(value, best)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best
    
def get_best_move():
    best = -float('inf')
    best_move = None
    alpha = -float('inf')
    beta = float('inf')
    for row, col in get_empty_cells():
        board[row][col] = 'O'
        value = MiniMaxIntermedio(board, 0, False, alpha, beta)
        board[row][col] = None
        if value > best:
            best = value
            best_move = (row, col)
        alpha = max(alpha, best)
    return best_move

def ai_advanced():
    move = get_best_moveAd()
    if move:
        row, col = move
        board[row][col] = 'O'
        return True
    return False

def MiniMaxAdvanced(board, depth, isMax, alpha, beta):
    #comprueba si ya alguien ha ganado o si hay un empate
    if check_win() == 'O': # ia gana
        return 1
    elif check_win() == 'X': # jugador gana
        return -1
    elif check_tie() or depth >= 6: # en esta linea es donde se limita la profundidad
        return 0
    
    if isMax:
        best = -float('inf')
        for row, col in get_empty_cells():
            board[row][col] = 'O'
            value = MiniMaxIntermedio(board, depth+1, False, alpha, beta)
            board[row][col] = None
            best = max(value, best)
            alpha = max(alpha, best) # implementa alpha beta pruning
            if beta <= alpha:
                break
        return best
    else:
        best = float('inf')
        for row, col in get_empty_cells():
            board[row][col] = 'X'
            value = MiniMaxIntermedio(board, depth+1, True, alpha, beta)
            board[row][col] = None
            best = min(value, best)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best
    
def get_best_moveAd():
    best = -float('inf')
    best_move = None
    alpha = -float('inf')
    beta = float('inf')
    for row, col in get_empty_cells():
        board[row][col] = 'O'
        value = MiniMaxAdvanced(board, 0, False, alpha, beta)
        board[row][col] = None
        if value > best:
            best = value
            best_move = (row, col)
        alpha = max(alpha, best)
    return best_move

def draw_game_over():
    if winner:
        text = f"¡{'Jugador' if winner == 'X' else 'IA'} ha ganado!"
    else:
        text = "¡Empate!"
    
    # Fondo del mensaje
    pygame.draw.rect(screen, BUTTON_COLOR, (50, HEIGHT//2 - 70, WIDTH-100, 140), border_radius=10)
    
    # Texto principal
    game_over_text = button_font.render(text, True, TEXT_COLOR)
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 40))
    
    # Botón de reinicio (a la izquierda)
    restart_rect = pygame.Rect(WIDTH//2 - 160, HEIGHT//2 + 20, 150, 40)
    pygame.draw.rect(screen, HOVER_COLOR, restart_rect, border_radius=5)
    restart_text = mode_font.render("Reiniciar", True, TEXT_COLOR)
    screen.blit(restart_text, (WIDTH//2 - 160 + 75 - restart_text.get_width()//2, HEIGHT//2 + 30))

    # Botón de menú (a la derecha)
    restart_menu = pygame.Rect(WIDTH//2 + 10, HEIGHT//2 + 20, 150, 40)
    pygame.draw.rect(screen, HOVER_COLOR, restart_menu, border_radius=5)
    restart_textmenu = mode_font.render("Menu", True, TEXT_COLOR)
    screen.blit(restart_textmenu, (WIDTH//2 + 10 + 75 - restart_textmenu.get_width()//2, HEIGHT//2 + 30))

def reset_game():
    global board, player_turn, game_active, game_over, winner
    board = [[None]*3 for _ in range(3)]
    player_turn = random.choice([True, False])
    game_active = True
    game_over = False
    winner = None
    screen.fill(BG_COLOR)
    draw_board()
    draw_game_info()
    
    # Si la IA empieza primero
    if not player_turn:
        pygame.time.wait(300)
        # Llamar a la IA correspondiente según el modo
        if current_mode == "Principiante":
            ai_beginner()
        elif current_mode == "Intermedio":
            ai_intermediate()
        elif current_mode == "Avanzado":
            ai_advanced()
        player_turn = True

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if not game_active:
                if 150 <= mouse_pos[0] <= 350:
                    if 250 <= mouse_pos[1] <= 300:
                        current_mode = "Principiante"
                        reset_game()
                    elif 350 <= mouse_pos[1] <= 400:
                        current_mode = "Intermedio"
                        reset_game()
                    elif 450 <= mouse_pos[1] <= 500:
                        current_mode = "Avanzado"
                        reset_game()
            
            else:
                if game_over:
                    if WIDTH//2 - 160 <= mouse_pos[0] <= WIDTH//2 - 10 and HEIGHT//2 + 20 <= mouse_pos[1] <= HEIGHT//2 + 60:
                        # Botón de Reiniciar
                        reset_game()
                    elif WIDTH//2 + 10 <= mouse_pos[0] <= WIDTH//2 + 160 and HEIGHT//2 + 20 <= mouse_pos[1] <= HEIGHT//2 + 60:
                        # Botón de Menú
                        game_active = False
                        game_over = False
                    continue
                
                if player_turn and not game_over:
                    mouseX, mouseY = mouse_pos
                    clicked_row = mouseY // SQUARE_SIZE
                    clicked_col = mouseX // SQUARE_SIZE
                    
                    if 0 <= clicked_row < 3 and 0 <= clicked_col < 3:
                        if board[clicked_row][clicked_col] is None:
                            board[clicked_row][clicked_col] = 'X'
                            player_turn = False
                            
                            winner = check_win()
                            if winner:
                                game_over = True
                            elif check_tie():
                                game_over = True
                                winner = None

    if game_active and not game_over:
        if not player_turn:
            success = False
            if current_mode == "Principiante":
                success = ai_beginner()
            elif current_mode == "Intermedio":
                success = ai_intermediate()
            elif current_mode == "Avanzado":
                success = ai_advanced()
            
            if success:
                winner = check_win()
                if winner:
                    game_over = True
                elif check_tie():
                    game_over = True
                    winner = None
                player_turn = True
            
            pygame.time.wait(300)

    # Actualizar pantalla
    if game_active:
        screen.fill(BG_COLOR)
        draw_board()
        draw_figures()
        draw_game_info()
        
        if game_over:
            draw_game_over()
        
        pygame.display.update()
    else:
        draw_menu()
        pygame.display.update()
