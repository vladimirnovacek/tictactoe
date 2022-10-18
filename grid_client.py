import os

import pygame.draw


class Grid:
    """
    Grid holds informations of a current state of a game grid and draws it to a surface.
    """

    def __init__(self):
        self._resources_folder: str = "resources"

        self._image_x: pygame.Surface = pygame.image.load(os.path.join(self._resources_folder, "x.png"))
        self._image_o: pygame.Surface = pygame.image.load(os.path.join(self._resources_folder, "o.png"))

        self._lines: tuple[tuple[tuple[int, int], ...], ...] = (
            ((200, 0), (200, 600)),
            ((400, 0), (400, 600)),
            ((0, 200), (600, 200)),
            ((0, 400), (600, 400))
        )
        self._grid: list[list[int, ...], ...] = [[0 for _ in range(3)] for _ in range(3)]

        self.winner: int = 0
        self.game_over: bool = False

    def reset(self) -> None:
        """
        Prepares the grid for a new game.
        :return:
        """
        self._grid = [[0 for _ in range(3)] for _ in range(3)]
        self.winner = 0
        self.game_over = False

    def set_winner(self, player: int) -> None:
        """
        Sets a winner.
        :param player: 0 for empty, 1 for "X", 2 for "O"
        :return:
        """
        if player == 1:
            self.winner = "X"
        elif player == 2:
            self.winner = "O"
        self.game_over = True

    def set_cell(self, xx: int, yy: int, value: int) -> None:
        """
        Puts a symbol by the given value to the given cell.
        :param xx: Column
        :param yy: Row
        :param value: 0 for empty, 1 for "X", 2 for "O"
        :return:
        """
        self._grid[xx][yy] = value

    @staticmethod
    def _get_cell_coords(xx: int, yy: int):
        return xx * 200, yy * 200

    @staticmethod
    def get_cell_indexes(x: int, y: int) -> tuple[int, ...]:
        """
        Transfers mouse coorditates to cell coordinates.
        :param x: Width
        :param y: Height
        :return: Cell coordinates (column, row)
        """
        return tuple(i // 200 for i in (x, y))

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws grid lines and symbols to the surface.
        :param surface: Surface to draw
        :return:
        """
        for column in self._lines:
            pygame.draw.line(surface, (200, 200, 200), column[0], column[1], 2)
        for xx, column in enumerate(self._grid):
            for yy, cell in enumerate(column):
                if cell == 1:
                    self._draw_to_cell(xx, yy, surface, self._image_x)
                elif cell == 2:
                    self._draw_to_cell(xx, yy, surface, self._image_o)

    def _draw_to_cell(self, xx: int, yy: int, surface: pygame.Surface, image: pygame.Surface):
        surface.blit(image, self._get_cell_coords(xx, yy))
