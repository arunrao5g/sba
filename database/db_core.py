from database.db_mysql_conmngr import CreateSession
from utils.generic import Static, container_st_tag, container_ed_tag


class Search(object):
    # initialize all the attribute to default
    def __init__(self, p_search_query, p_chart_type, p_group_class):
        self.search_query = p_search_query.lower()
        self.chart_type = p_chart_type.lower()
        self.group_class = p_group_class.lower()
        self.d_metric = dict()
        self.d_dimension = dict()
        self.d_filters = dict()
        self.tag = ""
        self.result_dict = dict()

    # Generic static method to create a database cursor for a query string
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

    # Method to populate metric, dimension & filters from the search query
    def generate_mdf(self):
        qry_string = Static.attribute_query(self.group_class)
        cur = self.generate_query_object(qry_string)

        for row in cur:
            if row[0] in self.search_query and row[3] == "Y":
                self.d_metric[row[0]] = {
                    "column_alias": row[0].title().replace(" ", ""),
                    "class": row[1],
                    "target_table": row[2],
                    "column_name": row[6]
                }
            if row[0] in self.search_query and row[3] == "N" and row[4] == "N":
                self.d_dimension[row[0]] = {
                    "column_alias": row[0].title().replace(" ", ""),
                    "class": row[1],
                    "target_table": row[2],
                    "column_name": row[6]
                }
            if row[0] in self.search_query and row[3] == "N" and row[4] == "Y":
                self.d_filters[row[0]] = {
                    "column_alias": row[0].title().replace(" ", ""),
                    "class": row[1],
                    "target_table": row[2],
                    "filter_value": row[5],
                    "column_name": row[6]
                }

    def generate_sql_query(self, display_type):
        if display_type == 'report':
            # populate all the columns in a set
            col_query = ""
            # noinspection PyTypeChecker
            select_list = set([d["class"] + " as " + d["column_alias"] for d in self.d_dimension.values()])
            # noinspection PyTypeChecker
            select_list.update([m["class"] + " as " + m["column_alias"] for m in self.d_metric.values()])
            for columns in select_list:
                col_query = columns + ", " + col_query

            # populate all the tables in a set
            tab_query = ""
            # noinspection PyTypeChecker
            from_list = set([d["target_table"] for d in self.d_dimension.values()])
            # noinspection PyTypeChecker
            from_list.update([m["target_table"] for m in self.d_metric.values()])
            for columns in from_list:
                tab_query = columns + ", " + tab_query

            # populate all the joins in a set
            join_query = ""
            jcur = self.generate_query_object(Static.join_query(tab_query.strip(", ")))
            join_set = set([j[0] + " = " + j[1] for j in jcur])
            for joins in join_set:
                join_query = join_query + joins + " and "

            # populate group by columns in a set
            group_by_query = ""
            # noinspection PyTypeChecker
            group_by_list = set([d["class"] for d in self.d_dimension.values()])
            for gb_columns in group_by_list:
                group_by_query = gb_columns + ", " + group_by_query

            return "select " + col_query.strip(", ") + " from " + tab_query.strip(", ") \
                   + " where " + join_query.strip(" and ") + " group by " + group_by_query.strip(", ")

    def get_report(self):
        report_cur = self.generate_query_object(self.generate_sql_query('report'))

        field_names = [i[0] for i in report_cur.description]

        report_tag = "<table id='reportTable' class='report_table' align='left' " \
                     "style='padding:20px;box-shadow: 2px 2px 5px #888888;background-color:white'><thead><tr>"

        for i in field_names:
            report_tag += "<th>" + i + "</th>"

        report_tag += "</tr></thead><tbody>"

        record = dict()
        word_list = list()

        for row in report_cur:
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

    @staticmethod
    def get_graph():
        return "graph-tag"

    # main method to get the result
    def get_chart(self):
        self.generate_mdf()
        chart_header = Static.get_chart_header(self.search_query)

        if self.chart_type == 'report':
            chart_body = self.get_report()
        else:
            chart_body = self.get_graph()

        self.tag = container_st_tag + chart_header + chart_body + container_ed_tag

        self.result_dict["meta"] = {
            "html_tag": self.tag,
            "lang": "en",
            "etag": "timestamp",
            "message": "OK"
        }

        return self.result_dict
