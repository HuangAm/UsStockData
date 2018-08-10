import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
import datetime
import traceback
import json
import os
from tornado.options import define, options


define("port", default=8887, help="run on the given port", type=int)


class DataHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        print("set_header")
        self.set_header("Access-Control-Allow-Origin", "*")  # 这个地方可以写域名
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        print("hello")
        self.write("world")

    def post(self, *args, **kwargs):
        data1 = self.get_argument("welcome",None)
        print(data1)
        import json
        data2 = json.loads(data1)
        content = data2["content"]
        print(content)
        text = content.get("text",None)
        if text:
            print(text)
            # with open("xx","a",encoding="utf-8")as f:
            #     f.write(text)
            #     print("write")




class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/data", DataHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        super(Application, self).__init__(handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(),ssl_options={
           "certfile": os.path.join(os.path.dirname(__file__), "keys", "caimouse.crt"),
           "keyfile": os.path.join(os.path.dirname(__file__), "keys", "caimouse.key"),
    })
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()