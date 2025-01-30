import pygame
import sys
from pygame.locals import *

WINDOW_SIZE = 400
GRID_SIZE = 4
MARGIN = 20
CELL_SIZE = (WINDOW_SIZE - 2 * MARGIN) // GRID_SIZE
FONT_SIZE = 32

BG_COLOR = (255, 255, 255)
GRID_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 255)
HIGHLIGHT_COLOR = (200, 200, 200)
ERROR_COLOR = (255, 0, 0)

pygame.init()

DISPLAYSURF = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Sudoku Solver")

FONT = pygame.font.Font(None, FONT_SIZE)

SUDOKU_GRID = [
    [1, 0, 0, 4],
    [0, 0, 3, 0],
    [0, 4, 0, 0],
    [2, 0, 0, 3]
]

def draw_grid(grid, selected=None, error_message=None):
    DISPLAYSURF.fill(BG_COLOR)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(DISPLAYSURF, GRID_COLOR, rect, width=1)
            if (row, col) == selected:
                pygame.draw.rect(DISPLAYSURF, HIGHLIGHT_COLOR, rect)
            if grid[row][col] != 0:
                text_surface = FONT.render(str(grid[row][col]), True, TEXT_COLOR)
                text_rect = text_surface.get_rect(center=rect.center)
                DISPLAYSURF.blit(text_surface, text_rect)
        
        subgrid_size = int(GRID_SIZE ** 0.5)
        for row in range(1, GRID_SIZE):
            if row % subgrid_size == 0:
                pygame.draw.line(DISPLAYSURF, GRID_COLOR,
                                 (MARGIN, MARGIN + row * CELL_SIZE),
                                 (MARGIN + GRID_SIZE * CELL_SIZE, MARGIN + row * CELL_SIZE), width=4)
                pygame.draw.line(DISPLAYSURF, GRID_COLOR,
                                 (MARGIN + row * CELL_SIZE, MARGIN),
                                 (MARGIN + row * CELL_SIZE, MARGIN + GRID_SIZE * CELL_SIZE), width=8)
                
    if error_message:
        text_surface = FONT.render(error_message, True, ERROR_COLOR)
        text_rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, MARGIN // 2))
        DISPLAYSURF.blit(text_surface, text_rect)

def is_valid_move(grid, row, col, num):
    if num in grid[row]:
        return False
    if num in [grid[r][col] for r in range(GRID_SIZE)]:
        return False
    subgrid_size = int(GRID_SIZE ** 0.5)
    start_row, start_col = (row // subgrid_size) * subgrid_size, (col // subgrid_size) * subgrid_size
    for r in range(start_row, start_row + subgrid_size):
        for c in range(start_col, start_col + subgrid_size):
            if grid[r][c] == num:
                return False
    return True

def is_solved(grid):
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

def main():
    grid = [row[:] for row in SUDOKU_GRID]
    selected = None
    solved_message = None
    invalid_move_message = None
    
    while True:
        draw_grid(grid, selected, invalid_move_message)

        if solved_message:
            text_surface = FONT.render(solved_message, True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, MARGIN // 2))
            DISPLAYSURF.blit(text_surface, text_rect)

        if invalid_move_message:
            text_surface = FONT.render(invalid_move_message, True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center = (WINDOW_SIZE // 2, MARGIN // 2 - 20))
            DISPLAYSURF.blit(text_surface, text_rect)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                selected = y // CELL_SIZE, x // CELL_SIZE
            elif event.type == KEYDOWN and selected:
                row, col = selected
                if event.key == K_BACKSPACE or event.key == K_DELETE:
                    grid[row][col] = 0
                elif K_1 <= event.key <= K_9:
                    num = event.key - K_0
                    if is_valid_move(grid, row, col, num):
                        grid[row][col] = num
                        invalid_move_message = None
                    else:
                        invalid_move_message = "Invalid Move!"
                elif event.key == K_RETURN or event.key == K_KP_ENTER:
                    if is_solved(grid):
                        solved_message = "Sudoku Solved!"
                    else:
                        solved_message = None
                        invalid_move_message = None
        
        pygame.display.update()

if __name__ == "__main__":
    main()