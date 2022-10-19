
class Grid:

    def __init__(self):
        self.search_dirs = (
            # down  down-right right up-right
            (1, 0), (1, 1), (0, 1), (-1, 1)
        )
        self.grid = [[0 for _ in range(3)] for _ in range(3)]
        self.on_turn = 1
        self.winner = 0
        self.game_over = False

    def _push_turn(self):
        self.on_turn = 3 - self.on_turn

    def reset(self) -> None:
        """
        Prepares the grid for a new game.
        :return:
        """
        self.grid = [[0 for _ in range(3)] for _ in range(3)]
        self.winner = 0
        self.game_over = False

    def _grid_full(self) -> bool:
        return all([i for col in self.grid for i in col])

    def cell_selected(self, xx: int, yy: int, player: int) -> int:
        """
        Attepmts to place a symbol of the player to the given cell. If the game is over after this, it also sets
        the game_over and winner property.
        :param xx: Column
        :param yy: Row
        :param player: Player id
        :return: Id of a player who's on turn now.
        """
        cell_value = self._get_cell_value(xx, yy)
        if cell_value == 0:
            self._set_cell(xx, yy, player)
            self._push_turn()
            if self._grid_full():
                self.game_over = True
            if self._check_grid(xx, yy, player):
                self._set_winner(player)
        return self.on_turn

    def _set_winner(self, player:int) -> None:
        self.winner = player
        self.game_over = True

    def _get_cell_value(self, xx: int, yy: int) -> int:
        return self.grid[xx][yy]

    def _set_cell(self, xx: int, yy: int, value: int) -> None:
        self.grid[xx][yy] = value

    @staticmethod
    def _is_in_bounds(xx: int, yy: int) -> bool:
        return 0 <= xx < 3 and 0 <= yy < 3

    def _check_grid(self, xx: int, yy: int, player: int) -> int:
        """
        Checks if there are 3 in a row after placing a symbol to a given cell.
        :param xx: Column
        :param yy: Row
        :param player: Player id
        :return: Player id if he has 3 in a row, else 0.
        """
        count = 1
        for direction in self.search_dirs:
            for multiplicator in (1, -1):
                xxx, yyy = xx, yy
                direction = tuple(d * multiplicator for d in direction)
                xxx += direction[0]
                yyy += direction[1]
                while self._is_in_bounds(xxx, yyy):
                    if self._get_cell_value(xxx, yyy) == player:
                        count += 1
                        xxx += direction[0]
                        yyy += direction[1]
                    else:
                        break
            if count >= 3:
                return player
            count = 1
        return 0
