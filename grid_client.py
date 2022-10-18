import os

import pygame.draw


class Grid:

    def __init__(self):
        self.resources_folder = "resources"

        self.image_x = pygame.image.load(os.path.join(self.resources_folder, "x.png"))
        self.image_o = pygame.image.load(os.path.join(self.resources_folder, "o.png"))
        self.lines = (
            ((200, 0), (200, 600)),
            ((400, 0), (400, 600)),
            ((0, 200), (600, 200)),
            ((0, 400), (600, 400))
        )
        self.grid = [[0 for _ in range(3)] for _ in range(3)]
        self.winner = 0
        self.game_over = False

    def reset(self):
        self.grid = [[0 for _ in range(3)] for _ in range(3)]
        self.winner = 0
        self.game_over = False

    def set_winner(self, player):
        if player == 1:
            self.winner = "X"
        elif player == 2:
            self.winner = "O"
        self.game_over = True

    def set_cell(self, xx: int, yy: int, value: int) -> None:
        self.grid[xx][yy] = value

    @staticmethod
    def get_cell_coords(xx, yy):
        return xx * 200, yy * 200

    @staticmethod
    def get_cell_indexes(x, y):
        return tuple(i // 200 for i in (x, y))

    def draw(self, surface):
        for column in self.lines:
            pygame.draw.line(surface, (200, 200, 200), column[0], column[1], 2)
        for xx, column in enumerate(self.grid):
            for yy, cell in enumerate(column):
                if cell == 1:
                    self.draw_to_cell(xx, yy, surface, self.image_x)
                elif cell == 2:
                    self.draw_to_cell(xx, yy, surface, self.image_o)

    def draw_to_cell(self, xx, yy, surface: pygame.Surface, image: pygame.Surface):
        surface.blit(image, self.get_cell_coords(xx, yy))
