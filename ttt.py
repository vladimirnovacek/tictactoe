
import sys

import client
import server


def parse_cl_arguments(argv: list[str]) -> dict:
    script_name = argv[0]
    arguments = {}
    options = []
    for arg in argv[1:]:
        if arg.startswith("--"):
            if "=" in arg:
                arg = arg.lstrip("-").split("=", 1)
                arguments[arg[0]] = arg[1]
            else:
                options.append(arg.lstrip("-"))
    return {"filename": script_name, "arguments": arguments, "options": options}


def process_arguments(args: dict):
    if "server" in args["options"]:
        try:
            run_server((args["arguments"]["host"], int(args["arguments"]["port"])))
        except KeyError or TypeError:
            SystemExit("Usage: ttt --host=IPADDR --port=PORT (--server|--client)")
    elif "client" in args["options"]:
        try:
            run_client((args["arguments"]["host"], int(args["arguments"]["port"])))
        except KeyError or TypeError:
            SystemExit("Usage: ttt --host=IPADDR --port=PORT (--server|--client)")


def run_server(addr: tuple[str, int]):
    s = server.Server(addr)
    s.start()
    run_client(addr)


def run_client(addr: tuple[str, int]):
    c = client.Client(addr)
    c.start()


if __name__ == '__main__':
    process_arguments(parse_cl_arguments(sys.argv))
