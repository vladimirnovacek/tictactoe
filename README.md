# tictactoe

Initially I made a game by [this YouTube tutorial](https://www.youtube.com/playlist?list=PL1P11yPQAo7pJT26yr1_cmfS1g_RX7b4d), but I wasn't satisfied with the architecture with a lot of repeating code, where files server.py and client.py were basically the same, and with a class Grid, which contained both the game logic and methods for drawing on screen. Plus I wanted something reusable, where I could have more than two players or run the server separately from the clients. So I took that project and refactored it to this shape.

Usage: `python3 tictactoe.py --host=HOST --port=PORT (--server|--client)`

For example run `python3 tictactoe.py --host=127.0.0.1 --port=65432 --server` which starts a server and a client that connects to that server and `python3 tictactoe.py --host=127.0.0.1 --port=65432 --client` which creates the second client and then the game is on.

