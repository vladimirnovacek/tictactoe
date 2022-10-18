
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

    def push_turn(self):
        self.on_turn = 3 - self.on_turn

    def reset(self):
        self.grid = [[0 for _ in range(3)] for _ in range(3)]
        self.winner = 0
        self.game_over = False

    def grid_full(self):
        if all([i for col in self.grid for i in col]):
            return True
        return False

    def cell_selected(self, xx, yy, player):
        cell_value = self.get_cell_value(xx, yy)
        if cell_value == 0:
            self.set_cell(xx, yy, player)
            self.push_turn()
            if self.grid_full():
                self.game_over = True
            if self.check_grid(xx, yy, player):
                self.set_winner(player)
            return 3 - player
        return player

    def set_winner(self, player):
        self.winner = player
        self.game_over = True

    def get_cell_value(self, xx: int, yy: int) -> int:
        return self.grid[xx][yy]

    def set_cell(self, xx: int, yy: int, value: int) -> None:
        self.grid[xx][yy] = value

    @staticmethod
    def get_cell_indexes(x, y):
        return tuple(i // 200 for i in (x, y))

    @staticmethod
    def _is_in_bounds(xx, yy):
        return 0 <= xx < 3 and 0 <= yy < 3

    def check_grid(self, xx, yy, player):
        count = 1
        for direction in self.search_dirs:
            for multiplicator in (1, -1):
                xxx, yyy = xx, yy
                direction = tuple(d * multiplicator for d in direction)
                xxx += direction[0]
                yyy += direction[1]
                while self._is_in_bounds(xxx, yyy):
                    if self.get_cell_value(xxx, yyy) == player:
                        count += 1
                        xxx += direction[0]
                        yyy += direction[1]
                    else:
                        break
            if count >= 3:
                return player
            count = 1
        return 0
