import os
from . import vercel


def main(handler = vercel.API, port = 8000):
    vercel.start(
        HandlerClass = handler,
        port = port
    )

class handler(vercel.API):
    def vercel(self, url, data, headers):
        if(os.path.isdir(url)):
            self.send_code(200)
            for home in ['index.html','index.htm']:
                if(os.path.isfile(url + home)):
                    self.send_file(url + home)
                    return
            self.send_text( '\n'.join(os.listdir(url)) )
            return

        if(os.path.isfile(url)):
            if(os.path.splitext(url)[1]=='.py'):
                return vercel.ErrorStatu(self, 403)
            self.send_code(200)
            self.send_file(url)
            return

        if(os.path.isfile(url + '.py')):
            mod_handler = vercel.load_handler(url, url + '.py')
            if mod_handler:
                vercel_func = getattr(mod_handler, 'vercel', None)
                if vercel_func is None:
                    return vercel.ErrorStatu(self, 503, 'Handler has no vercel method')
                try:
                    vercel_func(self, url, data, headers)
                except Exception as e:
                    vercel.verlog.name("router")(f"Error in handler {url + '.py'}")
                    vercel.verlog.name("router")(f"  {e}")
                    return vercel.ErrorStatu(self, 503, str(e))
                return

        vercel.ErrorStatu(self, 404)


if(__name__=='__main__'):
    main( handler )
