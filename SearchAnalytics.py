import falcon
import webbrowser
from wsgiref import simple_server
from restserv_v1.core import searchAnalytics
from restserv_v1.dashboard import listDashboards, createDashboards, saveChart


ALLOWED_ORIGINS = ['http://127.0.0.1:8001']  # Or load this from a config file


class CorsMiddleware(object):

    def process_request(self, response):
        response.set_header('Access-Control-Allow-Origin', '*')
        response.set_header('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.set_header('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE')


app = falcon.API(middleware=[CorsMiddleware()])

# Register API view
searchanalytics = searchAnalytics()
listdashboards = listDashboards()
createdashboards = createDashboards()
savechart = saveChart()

# Resgister API endpoits
app.add_route('/searchanalytics', searchanalytics)
app.add_route('/listdashboards', listdashboards)
app.add_route('/createdashboards', createdashboards)
app.add_route('/savechart', savechart)

if __name__ == '__main__':
    host = "127.0.0.1"
    port = 8001
    httpd = simple_server.make_server(host, port, app)
    try:
        webbrowser.open('http://localhost:63342/sba/static/index.html')
        print("Serving on %s:%s" % (host, port))
        httpd.serve_forever()
    except Exception as e:
        print(e)
