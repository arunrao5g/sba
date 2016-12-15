import json
import falcon
from database.db_dashboards import Dashboard


def crossdomain(req, resp):
    resp.set_header('Access-Control-Allow-Origin', '*')
    resp.set_header('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    resp.set_header('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE')


class listDashboards(object):
    @staticmethod
    def on_post(req, resp):
        falcon.after(crossdomain(req, resp))
        result_dict = dict()
        try:
            resp.status = falcon.HTTP_200
            data = json.loads(req.stream.read().decode('utf-8'))
            groupClass = data.get('groupClass')
            lexString = data.get('lexString')
            result = Dashboard.get_dashboard_list(groupClass, lexString)
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


class createDashboards(object):
    @staticmethod
    def on_post(req, resp):
        falcon.after(crossdomain(req, resp))
        result_dict = dict()
        try:
            resp.status = falcon.HTTP_200
            data = json.loads(req.stream.read().decode('utf-8'))
            groupClass = data.get('groupClass')
            dashboardName = data.get('dashboardName')
            result = Dashboard.create_dashboard(groupClass, dashboardName)
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


class saveChart(object):
    @staticmethod
    def on_post(req, resp):
        falcon.after(crossdomain(req, resp))
        result_dict = dict()
        try:
            resp.status = falcon.HTTP_200
            data = json.loads(req.stream.read().decode('utf-8'))
            chartName = data.get('chartName')
            dashboardName = data.get('dashboardName')
            groupClass = data.get('groupClass')
            result = Dashboard.save_chart(chartName, dashboardName, groupClass)
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

