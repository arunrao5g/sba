from database.db_mysql_conmngr import CreateSession
from utils.generic import Static, container_st_tag, container_ed_tag
import re
from collections import defaultdict


class Search(object):
    def __init__(self, p_search_query, p_chart_type, p_group_class):
        self.chart_title = p_search_query
        self.search_query = p_search_query.lower()
        self.chart_type = p_chart_type.lower()
        self.group_class = p_group_class.lower()
        self.d_metric = dict()
        self.d_dimension = dict()
        self.d_filters = dict()
        self.tag, self.query_string, self.table_cur = "", "", ""
        self.result_dict = dict()
        self.metric_count, self.dimension_count = 0, 0
        self.group_by_query, self.order_by_query, self.tab_query, \
        self.col_query, self.filter_query, self.join_query = "", "", "", "", "", ""

    @staticmethod
    def generate_query_object(p_query):
        try:
            db = CreateSession.connect('sba_analytics')
            cur = db.cursor()
            cur.execute(p_query)
            return cur
        except Exception as e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error: %s" % str(e)

    def generate_mdf(self):
        qry_string = Static.attribute_query(self.group_class)
        cur = self.generate_query_object(qry_string)
        for row in cur:
            if row[0] in self.search_query and row[3] == "Y":
                self.d_metric[row[0]] = {
                    "column_alias": row[0].title().replace(" ", ""),
                    "class": row[1],
                    "target_table": row[2],
                    "column_name": row[6],
                    "prefix": row[9]
                }
            if row[0] in self.search_query and row[3] == "N" and row[4] == "N":
                self.d_dimension[row[0]] = {
                    "column_alias": row[0].title().replace(" ", ""),
                    "class": row[1],
                    "target_table": row[2],
                    "column_name": row[6],
                    "time_series": row[7],
                    "drill_down": row[8]
                }
            if row[0] in self.search_query and row[3] == "N" and row[4] == "Y":
                self.d_filters[row[0]] = {
                    "column_alias": row[0].title().replace(" ", ""),
                    "class": row[1],
                    "target_table": row[2],
                    "filter_value": row[5],
                    "column_name": row[6]
                }
        self.metric_count = len(self.d_metric.keys())
        self.dimension_count = len(self.d_dimension.keys())

    def generate_sql_query(self):
        select_list = set([d["class"] + " as " + d["column_alias"] for d in self.d_dimension.values()])
        for columns in select_list:
            self.col_query = self.col_query + columns + ", "
        select_list = set([m["class"] + " as " + m["column_alias"] for m in self.d_metric.values()])
        for columns in select_list:
            self.col_query = self.col_query + columns + ", "

        from_list = set([d["target_table"] for d in self.d_dimension.values()])
        from_list.update([m["target_table"] for m in self.d_metric.values()])
        from_list.update([f["target_table"] for f in self.d_filters.values()])
        source_tbl_query = Static.get_source_table(self.group_class)
        source_tbl_cur = self.generate_query_object(source_tbl_query)
        for row in source_tbl_cur:
            from_list.update([tab for tab in row])
        for columns in from_list:
            self.tab_query = columns + ", " + self.tab_query

        jcur = self.generate_query_object(Static.join_query(self.tab_query.strip(", ")))
        join_set = set([j[0] + " = " + j[1] for j in jcur])
        for joins in join_set:
            self.join_query = self.join_query + joins + " and "

        filter_query = ""
        filter_set = set([f["class"] + " = " + f["filter_value"] for f in self.d_filters.values()])
        for filters in filter_set:
            self.filter_query = self.filter_query + filters + " and "


        group_by_list = set([d["class"] for d in self.d_dimension.values()])
        for gb_columns in group_by_list:
            self.group_by_query = gb_columns + ", " + self.group_by_query
            if gb_columns in ('d_calendar_date.week_name', 'd_calendar_date.month_name',
                              'd_calendar_date.quarter_name','d_calendar_date.year_name'):
                self.group_by_query = gb_columns.replace("_name","_id") + ", " + self.group_by_query
                self.order_by_query = gb_columns.replace("_name","_id") + ", " + self.order_by_query

        self.query_string = "select " + self.col_query.rstrip(", ") + " from " + self.tab_query.rstrip(", ")
        if len(join_set) > 0:
            self.query_string = self.query_string + " where " + self.join_query.rstrip(" and ")
        if len(filter_set) > 0:
            self.query_string = self.query_string + " and " + self.filter_query.rstrip(" and ")
        if len(group_by_list) > 0:
            self.query_string = self.query_string + " group by " + self.group_by_query.rstrip(", ")
        if self.order_by_query != "":
            self.query_string = self.query_string + " order by " + self.order_by_query.rstrip(", ")

        print self.query_string

    def get_report(self):
        try:
            field_names = [i[0] for i in self.table_cur.description]
            report_tag = "<table id='reportTable' class='report_table' align='left' " \
                         "style='padding:20px;box-shadow: 2px 2px 5px #888888;background-color:white'><thead><tr>"
            for i in field_names:
                report_tag += "<th>" + i + "</th>"
            report_tag += "</tr></thead><tbody>"
            record = dict()
            word_list = list()
            for row in self.table_cur:
                report_tag += "<tr>"
                j = 0
                for i in field_names:
                    record[str(i)] = str(row[j])
                    report_tag += "<td>" + str(row[j]) + "</td>"
                    j += 1
                word_list.append(record)
                record = dict()
                report_tag += "</tr>"
            report_tag += "</tbody></table></div>"
            return report_tag
        except Exception as e:
            try:
                print "Error @ get_report() [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                print "Error @ get_report(): %s" % str(e)

    def get_graph(self):
        prefix, metric_value = "", 0
        if self.metric_count == 1 and self.dimension_count == 0:
            try:

                metric_name = re.sub("([a-z])([A-Z])","\g<1> \g<2>", [i[0] for i in self.table_cur.description][0])
                if self.d_metric[metric_name.lower()]["prefix"] is not None:
                    prefix = self.d_metric[metric_name.lower()]["prefix"]
                    print prefix

                for cur in self.table_cur:
                    metric_value = cur[0]
                self.tag = Static.get_kpi(metric_name, metric_value, prefix)
                return ""
            except Exception as e:
                print e.args[0]
                return ""
        elif self.metric_count == 1 and self.dimension_count == 1:
            try:
                dimension =  self.d_dimension.keys()[0]
                if self.d_dimension[dimension]["time_series"] != "Y" and self.d_dimension[dimension]["drill_down"] is None:
                    y_axis_name = self.d_metric.keys()[0]
                    if self.d_metric[y_axis_name]["prefix"] is not None:
                        prefix = self.d_metric[y_axis_name]["prefix"]
                    field_names = [i[0] for i in self.table_cur.description]
                    chart_data, name, y = "[", "", ""
                    for cur in self.table_cur:
                        j = 0
                        for i in field_names:
                            if str(i).replace(" ","").lower() == dimension.replace(" ","").lower():
                                name = "name: '"+ str(cur[j]) + "'"
                            elif str(i).replace(" ","").lower() == y_axis_name.replace(" ","").lower():
                                y = "y: " + str(cur[j])
                            j += + 1
                        chart_data = chart_data + "{" + y + ", " + name + "},"
                    chart_data = chart_data.rstrip(",") + "]"
                    return Static.get_pie_chart(chart_data, y_axis_name.title(), dimension.title(), prefix)
                elif self.d_dimension[dimension]["time_series"] == "Y" and self.d_dimension[dimension]["drill_down"] is None:
                    y_axis_name = self.d_metric.keys()[0]
                    if self.d_metric[y_axis_name]["prefix"] is not None:
                        prefix = self.d_metric[y_axis_name]["prefix"]
                    field_names = [i[0] for i in self.table_cur.description]
                    category, data = "", ""
                    for cur in self.table_cur:
                        j = 0
                        for i in field_names:
                            if str(i).replace(" ","").lower() == dimension.replace(" ","").lower():
                                category = category + "'" + str(cur[j]) + "'" + ","
                            elif str(i).replace(" ","").lower() == y_axis_name.replace(" ","").lower():
                                data = data + str(cur[j]) + ","
                            j += + 1
                    category = category.rstrip(",")
                    data = data.rstrip(",")
                    return Static.get_column_chart(data, category, prefix)
                elif self.d_dimension[dimension]["time_series"] != "Y" and self.d_dimension[dimension]["drill_down"] is not None:
                    drill_array = self.d_dimension[dimension]["drill_down"].split(",")
                    drill_col = drill_array.pop()
                    drill_join = drill_array.pop()
                    drill_tab = drill_array.pop()
                    drill_query = "select "+ self.col_query + drill_col+ " from " + self.tab_query.rstrip(", ")\
                          + ", " + drill_tab + " where " + self.join_query + drill_join + " group by " \
                          + self.group_by_query + drill_col
                    y_axis_name = self.d_metric.keys()[0]
                    if self.d_metric[y_axis_name]["prefix"] is not None:
                        prefix = self.d_metric[y_axis_name]["prefix"]
                    field_names = [i[0] for i in self.table_cur.description]
                    chart_data, name, drill_down, y = "[", "", "", ""
                    for cur in self.table_cur:
                        j = 0
                        for i in field_names:
                            if str(i).replace(" ","").lower() == dimension.replace(" ","").lower():
                                name = "name: '"+ str(cur[j]) + "'"
                                drill_down = "drilldown: '"+ str(cur[j]) + "'"
                            elif str(i).replace(" ","").lower() == y_axis_name.replace(" ","").lower():
                                y = "y: " + str(cur[j])
                            j += + 1
                        chart_data = chart_data + "{" + y + ", " + name + ", " + drill_down + "},"
                    chart_data = chart_data.rstrip(",") + "]"

                    drill_cur = self.generate_query_object(drill_query)
                    d_field_names = [a[0] for a in drill_cur.description]
                    name, value, drill_down = "", "", ""
                    temp_drill_dict = defaultdict(list)
                    for rec in drill_cur:
                        j = 0
                        for i in d_field_names:
                            if str(i).replace(" ","").lower() == dimension.replace(" ","").lower():
                                name = str(rec[j])
                            elif str(i).replace(" ","").lower() == y_axis_name.replace(" ","").lower():
                                value = str(rec[j])
                                temp_drill_dict[name].append(value)
                            else:
                                drill_down = str(rec[j])
                                temp_drill_dict[name].append("'" + drill_down + "'")
                            j += + 1
                    series = "["
                    for keys in temp_drill_dict.keys():
                        series_data, series_value = "", ""
                        for data in temp_drill_dict[keys][1::2]:
                            series_data = series_data + data + ","
                        for data in temp_drill_dict[keys][0::2]:
                            series_value = series_value + data + ","
                        sd_list = list(series_data.rstrip(",").split(","))
                        sv_list = list(series_value.rstrip(",").split(","))
                        data = "data:["
                        for a in range(0,len(sd_list)):
                            data = data + "["+ sd_list[a] + "," + sv_list[a] + "],"
                        series = series + "{name:'"+keys + "', id:'"+ keys+"', "+ data.rstrip(",") + "]},"
                    series = series.rstrip(",") + "]"
                    return Static.get_drill_down_chart(chart_data, series, dimension.title(), y_axis_name.title())
                else:
                    return ""
            except Exception as e:
                print e.args[0]
                return ""
        else:
            return ""

    def get_chart(self):
        self.generate_mdf()
        chart_header = Static.get_chart_header(self.chart_title)
        chart_body = ""
        self.generate_sql_query()
        self.table_cur = self.generate_query_object(self.query_string)
        if self.chart_type == 'report':
            chart_body = self.get_report()
        if self.chart_type == 'graph':
            chart_body = self.get_graph()

        if chart_body != "":
            self.tag = container_st_tag + chart_header + chart_body + container_ed_tag

        self.result_dict["meta"] = {
            "html_tag": self.tag,
            "lang": "en",
            "etag": "timestamp",
            "message": "OK"
        }
        return self.result_dict


# ToDo Delete below line
#result = Search('Total Sales by owner', 'graph', 'sales')
#print result.get_chart()
