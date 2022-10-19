import pickle
import socket
import threading
import typing

import pygame.display

import grid_client


class Client:
    """
    Client connects to a server and draws a game window. Then processes data from the server and reacts accordingly.
    """

    def __init__(self, addr: tuple[str, int]):
        self.addr = addr
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player: str | None = None
        self.on_turn = False
        self.grid = grid_client.Grid()
        self.running = True

    def start(self) -> None:
        """
        Connects the client to the server, starts to receive messages from it and starts the game window itself.
        :return:
        """
        self.sock.connect(self.addr)
        recv_data = threading.Thread(target=self._receive_data, daemon=True)
        recv_data.start()
        self._loop()

    def _process_data(self, data: dict) -> None:
        print(data)
        if "player_id" in data:
            if not self.player:
                self.player = data["player_id"]
        if "new_game" in data:
            self.grid.reset()
        if "on_turn" in data:
            self.on_turn = data["on_turn"] == self.player
        if "cell_filled" in data:
            self.grid.set_cell(*data["cell_filled"], data["player_id"])
        if "game_over" in data:
            self.grid.set_winner(data["winner"])
            result_quotes = {
                self.player: "You won!",
                3 - self.player: "You lose!",
                0: "It's a draw!"
            }
            print(result_quotes[data["winner"]])

    def send(self, message: typing.Any) -> None:
        """
        Sends a message to the server.
        :param message: Can be of any data type. Here it's using dictionary.
        :return:
        """
        self.sock.send(pickle.dumps(message))

    def _receive_data(self) -> None:
        while True:
            data = self.sock.recv(1024)
            print("Client: ", pickle.loads(data))
            self._process_data(pickle.loads(data))

    def _loop(self) -> None:
        surface = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Tic-Tac-Toe")
        while self.running:
            surface.fill((0, 0, 0))
            self.grid.draw(surface)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if not self.grid.game_over:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[0] and self.on_turn:
                            message = {
                                "cell_pressed": self.grid.get_cell_indexes(*pygame.mouse.get_pos()),
                                "player_id": self.player
                            }
                            self.send(message)
                            print(f"Client: sending {message}")
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                        if event.key == pygame.K_SPACE:
                            message = {
                                "reset": True,
                                "player_id": self.player
                            }
                            self.send(message)
            pygame.display.flip()

    def __str__(self):
        return f"{self.player=}, {self.on_turn=}"
