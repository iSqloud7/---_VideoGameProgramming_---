import pygame  # Импортирање на Pygame за графички приказ
import sys  # Импортирање на sys за да можеме да излеземе од програмата
from pygame.locals import *  # Импортирање на сите Pygame константи

# Константи за играта
WINDOW_SIZE = 400  # Големина на прозорецот (ширина и висина)
GRID_SIZE = 4  # Големина на Sudoku мрежата (4x4)
MARGIN = 20 # 1.Define the margin space around the grid
# CELL_SIZE = WINDOW_SIZE // GRID_SIZE  # Големина на секоја ќелија во пиксели
CELL_SIZE = (WINDOW_SIZE - 2 * MARGIN) // GRID_SIZE # 1.Subtract margin space to calculate cell size
FONT_SIZE = 32  # Големина на фонтот за бројките

# Бои (RGB формат)
BG_COLOR = (255, 255, 255)  # Бело - позадина
GRID_COLOR = (0, 0, 0)  # Црно - линии на мрежата
TEXT_COLOR = (0, 0, 255)  # Сино - боја на броевите
HIGHLIGHT_COLOR = (200, 200, 200)  # Светло сиво - означена ќелија
ERROR_COLOR = (255, 0, 0)  # 4.Red - error color

pygame.init()  # Иницијализација на Pygame

# Креирање на прозорецот
DISPLAYSURF = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Sudoku Solver")  # Наслов на прозорецот

# Фонт за бројките во мрежата
FONT = pygame.font.Font(None, FONT_SIZE)  # Креирање на фонт со дефинирана големина

# Почетна 4x4 Sudoku мрежа (0 претставува празни ќелии)
SUDOKU_GRID = [
    [1, 0, 0, 4],
    [0, 0, 3, 0],
    [0, 4, 0, 0],
    [2, 0, 0, 3]
]

# Функција за цртање на Sudoku мрежата
def draw_grid(grid, selected=None, error_message=None): # 4.Add parameter
    # Функција за цртање на мрежата со броевите и опционално означување на ќелија.
    DISPLAYSURF.fill(BG_COLOR)  # Чистење на екранот со бела боја
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            # rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            rect = pygame.Rect(MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE, CELL_SIZE, CELL_SIZE) # 1.Adjust the position of the cells considering the margin
            pygame.draw.rect(DISPLAYSURF, GRID_COLOR, rect, width=1)  # Цртање на ќелиите
            
            # Ако ќелијата е селектирана, означи ја со сива боја
            if (row, col) == selected:
                pygame.draw.rect(DISPLAYSURF, HIGHLIGHT_COLOR, rect)
            
            # Прикажи број ако ќелијата не е празна
            if grid[row][col] != 0:
                text_surface = FONT.render(str(grid[row][col]), True, TEXT_COLOR)  # Креирање на бројка
                text_rect = text_surface.get_rect(center=rect.center)  # Центрирање на текстот
                DISPLAYSURF.blit(text_surface, text_rect)  # Прикажување на бројката на екранот

        # 3.Draw thicker lines between sub-grids (2x2 sub-grids in 4x4 grid)
        subgrid_size = int(GRID_SIZE ** 0.5) # GRID_SIZE = 4, pow(4, 0.5)=2
        for row in range(1, GRID_SIZE):
            if row % subgrid_size == 0:
                pygame.draw.line(DISPLAYSURF, GRID_COLOR, # width
                                 (MARGIN, MARGIN + row * CELL_SIZE),
                                 (MARGIN + GRID_SIZE * CELL_SIZE, MARGIN + row * CELL_SIZE), width=4)
                pygame.draw.line(DISPLAYSURF, GRID_COLOR, # height
                                 (MARGIN + row * CELL_SIZE, MARGIN),
                                 (MARGIN + row * CELL_SIZE, MARGIN + GRID_SIZE * CELL_SIZE), width=8)
                
    # 4.Display error message if exists
    if error_message:
        text_surface = FONT.render(error_message, True, ERROR_COLOR)
        text_rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, MARGIN // 2))
        DISPLAYSURF.blit(text_surface, text_rect)

# Функција за проверка дали е валиден потег
def is_valid_move(grid, row, col, num):
    # Проверува дали бројот 'num' може да се постави во grid[row][col].
    # Проверка во редот
    if num in grid[row]:
        return False
    
    # Проверка во колоната
    if num in [grid[r][col] for r in range(GRID_SIZE)]:
        return False
    
    # Проверка во подмрежата (2x2 во 4x4 мрежа)
    subgrid_size = int(GRID_SIZE ** 0.5)  # За 4x4, subgrid_size = 2
    start_row, start_col = (row // subgrid_size) * subgrid_size, (col // subgrid_size) * subgrid_size
    for r in range(start_row, start_row + subgrid_size):
        for c in range(start_col, start_col + subgrid_size):
            if grid[r][c] == num:
                return False
    return True

# Функција за проверка дали Sudoku е решен
# def is_solved(grid):
    # Проверува дали целата Sudoku мрежа е пополнета правилно.
    # for row in range(GRID_SIZE):
        # for col in range(GRID_SIZE):
            # if grid[row][col] == 0 or not is_valid_move(grid, row, col, grid[row][col]):
                # print("Invalid move at", row, col)
                # return False
    # return True

def is_solved(grid):
    # 2.Checks that the entire Sudoku grid is filled in correctly.
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 0:
                return False
            if grid[row].count(grid[row][col]) > 1:
                return False
            column = [grid[r][col] for r in range(GRID_SIZE)]
            if column.count(grid[row][col]) > 1:
                return False

    return True

# Главна функција
def main():
    grid = [row[:] for row in SUDOKU_GRID]  # Копирање на почетната мрежа
    selected = None  # Почетно нема селектирана ќелија
    solved_message = None # 2.Sudoku solved message
    invalid_move_message = None # 4.Invalid move message
    
    while True:
        draw_grid(grid, selected, invalid_move_message)  # Исцртување на мрежата # 4. Add parameter to draw function

        # 2.Display message if Sudoku is solve
        if solved_message:
            text_surface = FONT.render(solved_message, True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, MARGIN // 2))
            DISPLAYSURF.blit(text_surface, text_rect)

        if invalid_move_message:
            text_surface = FONT.render(invalid_move_message, True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center = (WINDOW_SIZE // 2, MARGIN // 2 - 20)) # 3.Above the grid
            DISPLAYSURF.blit(text_surface, text_rect)
        
        for event in pygame.event.get():  # Чекање на настани (inputs)
            if event.type == QUIT:  # Ако корисникот затвори прозорецот
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:  # Ако кликне со глушец
                x, y = event.pos
                selected = y // CELL_SIZE, x // CELL_SIZE  # Селектирај ќелија
            elif event.type == KEYDOWN and selected:  # Ако корисникот притисне тастер
                row, col = selected
                if event.key == K_BACKSPACE or event.key == K_DELETE:  # Бришење на бројка
                    grid[row][col] = 0
                elif K_1 <= event.key <= K_9:  # Ако притисне бројка 1-9
                    num = event.key - K_0
                    if is_valid_move(grid, row, col, num):  # Проверка дали потегот е валиден
                        grid[row][col] = num
                        invalid_move_message = None # 4.If the move is valid, delete message
                    else:
                        invalid_move_message = "Invalid Move!" # 4.Set invalid move message
                # elif event.key == K_RETURN and is_solved(grid):  # Ако е решено
                    # print("Sudoku Solved!")
                elif event.key == K_RETURN:  # 2.If the user presses Enter
                    if is_solved(grid):  # 2.Check if Sudoku is solved
                        solved_message = "Sudoku Solved!"  # 2.Display success message
                    else:
                        solved_message = None  # 2.Clear message if the grid is not solved
                        invalid_move_message = None  # Clear error message when checking solution
        
        pygame.display.update()  # Ажурирање на екранот

# Извршување на програмата ако е директно стартувана
if __name__ == "__main__":
    main()
