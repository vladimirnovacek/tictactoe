import pickle
import socket
import threading

import grid_server


class Server:

    def __init__(self, addr: tuple[str, int]):
        self.addr: tuple[str, int] = addr
        self.sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected: dict[int, None | socket.socket] = {1: None, 2: None}
        self.connection_established = False
        self.grid = grid_server.Grid()
        self.reset_request = 0

    def start(self):
        self.sock.bind(self.addr)
        self.sock.listen(2)
        waiting_for_connection = threading.Thread(target=self._waiting_for_connection, daemon=True)
        waiting_for_connection.start()

    def send(self, message, client: int):
        self.connected[client].send(pickle.dumps(message))

    def broadcast(self, message):
        for c in self.connected:
            self.send(message, c)

    def process_data(self, data: dict):
        message = dict()
        if not self.connection_established:
            return
        if "reset" in data:
            if self.reset_request == 3 - data["player_id"]:
                self.grid.reset()
                self.reset_request = 0
                message.update({
                    "new_game": True,
                    "on_turn": self.grid.on_turn
                })
            else:
                self.reset_request = data["player_id"]
        if "cell_pressed" in data:
            if not self.grid.game_over:
                cell = data["cell_pressed"]
                player_id = data["player_id"]
                result = self.grid.cell_selected(*cell, player_id)
                if result != player_id:
                    message.update({
                        "cell_filled": cell,
                        "player_id": player_id,
                        "on_turn": result
                    })
            if self.grid.game_over:
                message.update({
                    "game_over": True,
                    "winner": self.grid.winner
                })
        if message:
            self.broadcast(message)

    def _waiting_for_connection(self):
        recv_data = set()
        while not self.connection_established:
            conn, addr = self.sock.accept()
            self._add_client(conn)
            t = threading.Thread(target=self._receive_data, args=(conn,), daemon=True)
            t.start()
            recv_data.add(t)

    def _receive_data(self, conn):
        while True:
            data = pickle.loads(conn.recv(1024))
            self.process_data(data)

    def _add_client(self, conn):
        message = {}
        if not self.connected[1]:
            self.connected[1] = conn
            player = 1
        elif not self.connected[2]:
            self.connected[2] = conn
            player = 2
            self.connection_established = True
        else:
            return
        message["player_id"] = player
        message["on_turn"] = self.grid.on_turn
        self.send(message, player)
