from sercel import vercel
from sercel import decorators as dec

@vercel.register
@dec.hot_reload
def hello(response):
    response.send_code(200)
    response.send_text("Hello, world!")