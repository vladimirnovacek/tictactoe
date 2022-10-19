
import sys

import client
import server


usage = "Usage: {} --host=IPADDR --port=PORT [--server]"


def parse_cl_arguments(argv: list[str]) -> dict:
    """
    Parses command line arguments and returns a dictionary
    :param argv: arguments passed to the command line
    :return: Dictionary containing 3 keys:
        - "filename" name of an executed script
        - "arguments" dictionary or argument names as keys and their values a values
        - "options" list of options
    """
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


def process_arguments(args: dict) -> None:
    """
    Run apropriate functions acording to the given arguments.
    :param args: return value of parse_cl_arguments()
    :return:
    """
    if "server" in args["options"]:
        try:
            run_server((args["arguments"]["host"], int(args["arguments"]["port"])))
        except KeyError or TypeError:
            raise SystemExit(usage.format(args["filename"]))

    try:
        run_client((args["arguments"]["host"], int(args["arguments"]["port"])))
    except KeyError or TypeError:
        raise SystemExit(usage.format(args["filename"]))


def run_server(addr: tuple[str, int]) -> None:
    """
    Starts a game server listening for connections on a given address.
    :param addr: tuple of a host IP address and a port
    :return:
    """
    s = server.Server(addr)
    s.start()


def run_client(addr: tuple[str, int]) -> None:
    """
    Starts a client that tries to connect to server on a given address.
    :param addr: tuple of a host IP address and a port
    :return:
    """
    c = client.Client(addr)
    c.start()


if __name__ == '__main__':
    process_arguments(parse_cl_arguments(sys.argv))
