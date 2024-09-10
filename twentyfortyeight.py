import random
import pygame

pygame.init()

WIDTH, HEIGHT = 400, 400
TILE_SIZE = WIDTH // 4

TILE_COLORS = {
    0: (204, 192, 179),  
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

def create_board():
    return [[0] * 4 for _ in range(4)]

def print_board(board):
    for row in board:
        print('\t'.join(map(str,row)))

def draw_board(board):
    for row in range(4):
        for col in range(4):
            value = board[row][col]
            color = TILE_COLORS.get(value, (0,0,0))
            pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if value != 0:
                font = pygame.font.Font(None, 36)
                text = font.render(str(value), True, (0,0,0))
                text_rect = text.get_rect(center=(col * TILE_SIZE + TILE_SIZE / 2, row * TILE_SIZE + TILE_SIZE / 2))
                screen.blit(text, text_rect)

def add_tile(board):
    empty_positions = [(i,j) for i in range(4) for j in range(4) if board[i][j]==0]
    if not empty_positions:
        # if board is full
        return board
    
    i,j = random.choice(empty_positions)
    board[i][j] = 2 if random.random() < 0.9 else 4
    return board

def check_win(board):
    for row in board:
        if 2048 in row:
            return True
    return False

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

board = create_board()
board = add_tile(board)
draw_board(board)
pygame.display.flip()

def get_move():
    return input("Enter move (w/a/s/d): ")

def move_left(board):
    return [slide_left(row) for row in board]

def slide_left(row):
    new_row = [i for i in row if i != 0]
    for i in range(len(new_row) - 1):
        if new_row[i] == new_row[i+1]:
            new_row[i] *= 2
            new_row[i+1] = 0
    new_row = [i for i in new_row if i != 0]
    new_row += [0] * (4 - len(new_row))
    return new_row

def move_right(board):
    return [slide_right(row) for row in board]

def slide_right(row):
    row_reversed = row[::-1]
    new_row = [i for i in row_reversed if i != 0]
    for i in range(len(new_row) - 1):
        if new_row[i] == new_row[i+1]:
            new_row[i] *= 2
            new_row[i+1] = 0
    new_row = [i for i in new_row if i != 0]
    new_row += [0] * (4 - len(new_row))
    
    return new_row[::-1]

def get_column(board, col_index):
    return [row[col_index] for row in board]

def set_column(board, col_index, new_col):
    for row_index in range(len(board)):
        board[row_index][col_index] = new_col[row_index]

def move_up(board):
    for col_index in range(len(board[0])):
        col = get_column(board, col_index)
        new_col = slide_vertical(col)
        set_column(board, col_index, new_col)
    return board

def slide_vertical(col):
    new_col = [i for i in col if i != 0]
    for i in range(len(new_col) - 1):
        if new_col[i] == new_col[i+1]:
            new_col[i] *= 2
            new_col[i+1] = 0
    new_col = [i for i in new_col if i != 0]
    new_col += [0] * (4 - len(new_col))

    return new_col

def move_down(board):
    for col_index in range(len(board[0])):
        col = get_column(board, col_index)
        reversed_col = col[::-1]
        new_col = slide_vertical(reversed_col)
        reversed_col = new_col [::-1]
        set_column(board, col_index, reversed_col)
    return board

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                board = move_left(board)
                add_tile(board)
            elif event.key == pygame.K_RIGHT:
                board = move_right(board)
                add_tile(board)
            elif event.key == pygame.K_UP:
                board = move_up(board)
                add_tile(board)
            elif event.key == pygame.K_DOWN:
                board = move_down(board)
                add_tile(board)
    
    screen.fill((187, 173, 160))
    draw_board(board)
    pygame.display.flip()

pygame.quit()
