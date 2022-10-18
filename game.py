
import pygame

import grid_client


surface = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Tic Tac Toe")
surface.fill((255, 0, 0))

grid = grid.Grid()

playing = 1  # 1 == X, 2 == O

running = True


def switch_player(player):
    return 3 - player


while running:
    surface.fill((0, 0, 0))
    grid.draw(surface)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not grid.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    playing = grid.on_mouse_pressed(*pygame.mouse.get_pos(), playing)
            if grid.winner:
                print(f"{grid.winner} wins.")
            elif grid.grid_full():
                print("It's a draw.")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.game_over:
                grid.reset()
            if event.key == pygame.K_ESCAPE:
                running = False

    pygame.display.flip()
