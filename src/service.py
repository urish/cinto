import os
from tornado import (web, ioloop, autoreload)
from cinto import CintoEngine

cinto = CintoEngine()

class StartHandler(web.RequestHandler):
    def get(self):
        cinto.start()

class StopHandler(web.RequestHandler):
    def get(self):
        cinto.stop()

class MoveHandler(web.RequestHandler):
    def post(self, pawnId):
        x = float(self.get_argument("x"))
        y = float(self.get_argument("y"))
        cinto.updateTrack(int(pawnId), x, y)
        
        
def synthTimer():
    if cinto.running:
        cinto.nextMeasure()

settings = {
    "static_path": os.path.abspath(os.path.join(os.path.dirname(__file__), "../web")),
}

application = web.Application([
    (r"/start", StartHandler),
    (r"/stop", StopHandler),
    (r"/pawn/([0-4])", MoveHandler),
    (r"/", web.RedirectHandler, {"url": "/index.html"}),
    (r"/(.*)", web.StaticFileHandler, dict(path=settings['static_path'])),
])

if __name__ == "__main__":
    application.listen(8888)
    autoreload.start()
    ioloop.PeriodicCallback(synthTimer, 1000).start()
    ioloop.IOLoop.instance().start()
