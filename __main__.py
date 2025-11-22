from . import vercel
from . import verapi

import argparse

parser = argparse.ArgumentParser(description="Start the Sercel server.")
parser.add_argument("-p", "--port", type=int, default=15444, help="Port number to run the server on (default: 15444)")
args = parser.parse_args()

if __name__ == "__main__":
    vercel.start(
        HandlerClass=verapi.handler,
        port=args.port
    )
