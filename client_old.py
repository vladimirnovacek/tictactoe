import pickle
import socket
import threading

import pygame

import grid_client


HOST = "127.0.0.1"
PORT = 65432

sock = socket.socket()
sock.connect((HOST, PORT))


def create_thread(target):
    thread = threading.Thread(target=target, daemon=True)
    thread.start()


def receive_data():
    global on_turn
    while True:
        cell_pressed = pickle.loads(sock.recv(1024))
        print(cell_pressed)
        if not on_turn:
            grid.cell_selected(*cell_pressed, 1)
            on_turn = True
            if grid.winner:
                print(f"{grid.winner} wins.")
            elif grid.grid_full():
                print("It's a draw.")


create_thread(receive_data)

surface = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Tic Tac Toe")

grid = grid.Grid()

player_id = 2  # 1 == X, 2 == O

on_turn = False

running = True


while running:
    surface.fill((0, 0, 0))
    grid.draw(surface)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not grid.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] and on_turn:
                    grid.on_mouse_pressed(*pygame.mouse.get_pos(), player_id)
                    cell_pressed = grid.get_cell_indexes(*pygame.mouse.get_pos())
                    sock.send(pickle.dumps(cell_pressed))
                    on_turn = False
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