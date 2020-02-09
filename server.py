import web
import sigsrc
from siggen import siggen
import json

urls = (
    '/', 'index',
    '/api', 'api'
)
app = web.application(urls, globals())

class index:
    def GET(self):
        web.header('Content-Type', 'text/html')

        f = open('index.html','rb')
        ret = f.read()
        f.close()
        
        return ret

class api:
    def GET(self):
        srcex = {}

        try:
            web.input().src
            web.input().id
            getattr(sigsrc,web.input().src)
        except AttributeError:
            source = 'hello'
        else:
            web.header('Content-Type', 'image/png')
            source = web.input().src
            try:
                web.input().srcex
            except AttributeError:
                pass
            else:
                srcex = json.loads(web.input().srcex)
            srcex['id'] = web.input().id

        data = getattr(sigsrc, source).data(srcex)
        return siggen(data)

if __name__ == '__main__':
    app.run()
