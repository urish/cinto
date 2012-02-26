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

class PawnListHandler(web.RequestHandler):
    def get(self):
        result = []
        for i in range(1, cinto.numTracks() + 1):
            x, y = cinto.getTrack(int(i))
            result.append({"id": i, "x": x, "y": y})
        self.write({"pawns": result});

class PawnHandler(web.RequestHandler):
    def get(self, pawnId):
        id = int(pawnId)
        x, y = cinto.getTrack(id)
        self.write({"id": id, "x": x, "y": y})
    
    def post(self, pawnId):
        x = float(self.get_argument("x"))
        y = float(self.get_argument("y"))
        norm = lambda x: min(max(x, 0), 1)
        cinto.updateTrack(int(pawnId), norm(x), norm(y))
        
def synthTimer():
    if cinto.running:
        cinto.nextMeasure()

settings = {
    "static_path": os.path.abspath(os.path.join(os.path.dirname(__file__), "../web")),
}

application = web.Application([
    (r"/start", StartHandler),
    (r"/stop", StopHandler),
    (r"/pawns", PawnListHandler),
    (r"/pawns/([\d+])", PawnHandler),
    (r"/", web.RedirectHandler, {"url": "/index.html"}),
    (r"/(.*)", web.StaticFileHandler, dict(path=settings['static_path'])),
])

if __name__ == "__main__":
    application.listen(8888)
    autoreload.start()
    ioloop.PeriodicCallback(synthTimer, 1000).start()
    ioloop.IOLoop.instance().start()
