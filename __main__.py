from . import vercel
from . import verapi

if __name__ == "__main__":
    vercel.start(
        HandlerClass=verapi.handler,
        port=15444
    )
