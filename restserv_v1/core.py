import json
import falcon
from database.db_core import SearchMain


def crossdomain(req, resp):
    resp.set_header('Access-Control-Allow-Origin', '*')
    resp.set_header('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    resp.set_header('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE')


class searchAnalytics(object):
    @staticmethod
    def on_post(req, resp):
        falcon.after(crossdomain(req, resp))
        result_dict = dict()
        try:
            resp.status = falcon.HTTP_200
            data = json.loads(req.stream.read().decode('utf-8'))
            searchQuery = data.get('searchQuery')
            chartType = data.get('chartType')
            groupClass = data.get('groupClass')
            result = SearchMain.get_chart(searchQuery, chartType, groupClass)
            resp.body = json.dumps(result)
            # resp.content_type = "application/json"
        except Exception as e:
            print(e)
            result_dict["meta"] = {
                    "html": "",
                    "lang": "en",
                    "report":"",
                    "kpi":"",
                    "kpi_name":"",
                    "etag": "timestamp",
                    "message": "OK"
                    # ToDo Append ETAG (r&d req)
            }
            resp.body = json.dumps(result_dict)

