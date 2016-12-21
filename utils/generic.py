USR = "root"
PWD = "sriganesha"
HOST = "localhost"
PYPATH = "/Users/arunrao/Home/Learnings/Spark-WorkBenck/spark-1.5.2-bin-hadoop2.6/python/"
PY4JPATH = "/Users/arunrao/Home/Learnings/Spark-WorkBenck/spark-1.5.2-bin-hadoop2.6/python/lib/py4j-0.8.2.1-src.zip"
SPARKHOME = "/Users/arunrao/Home/Learnings/Spark-WorkBenck/spark-1.5.2-bin-hadoop2.6"
time_series = ['year', 'quarter', 'month', 'week', 'day', 'daily']

container_st_tag = "<div class='container' id='main><div class='row'><div class='col-sm-6'>"
container_ed_tag = "</div></div></hr>"

class Static:
    @staticmethod
    def attribute_query(p_group_class):
        return "select lower(name) AS name, class, target_table, " \
                 "metric_flag, filter_flag, filter_value, column_name " \
                 "from analytical_dictionary " \
                 "where lower(group_class) = '"+p_group_class+"' order by orderby"
    @staticmethod
    def join_query(target_table_list):
        return "select source_f_key, target_p_key from metadata " \
               "where target_table in ('" + target_table_list.replace(', ',"','") + "');"

    @staticmethod
    def chart_id_query():
        return "select coalesce(max(id),1) from saved_queries"

    @staticmethod
    def get_chart_header(chart_title):
        return "<div class='div-header' id='chartContainer-title'>"\
                "<div style='float: left;'><span id='chart-title' class='chart-title'>"+chart_title+"</span></div>"\
                "<div class='dropdown' style='float:right'>"\
                "<div class='dropdown-toggle' type='button' id='menu' data-toggle='dropdown'><div class='chart-edit'></div></div>"\
                "<ul class='dropdown-menu dropdown-menu-right' role='menu' aria-labelledby='menu'>"\
                "<li role='presentation'><a id='rename-chart' role='menuitem' tabindex='-1'>Edit</a></li>"\
                "<li role='presentation' class='disabled'><a role='menuitem' tabindex='-1' href='#'>Save to Dashboard</a></li>"\
                "<li role='presentation'><a role='menuitem' tabindex='-1' href='#'>Email</a></li>"\
                "<li role='presentation' class='divider'></li>"\
                "<li role='presentation'><a role='menuitem' tabindex='-1' href='#'>Delete</a></li>"\
                "</ul>"\
                "</div>"\
                "</div>"\
                "<script>"\
                "$(function () {"\
                "$('#rename-chart').click(function () {"\
                "var span_val = document.getElementById('chart-title').value;"\
                "$('#chart-title').text(span_val);"\
                "$('#chart-title').replaceWith($('<textarea >').attr({ id: 'chart1-title', class: 'chart-title chart-title-edit'}));"\
                "$('#chart-title').css('cursor', 'text');"\
                "});"\
                "});"\
                "$('#chartContainer-title').keypress(function(event){"\
                "var keycode = (event.keyCode ? event.keyCode : event.which);"\
                "if(keycode == '13'){"\
                "var span_val = document.getElementById('chart-title').value;"\
                "$('#chart-title').replaceWith($('<snap>').attr({ id: 'chart-title', class: 'chart-title'}));"\
                "$('#chart-title').text(span_val);"\
                "}"\
                " event.stopPropagation();"\
                "});"\
                "</script>"

    @staticmethod
    def get_pie_chart(chart_data, y_axis_name, series_name):
        return "<div class='div-continer' style='height:400px;' id='chartContainer'>"\
                "<script>"\
                "$(function () {  $(document).ready(function () {  Highcharts.chart('chartContainer', {"\
                "	chart: { type: 'pie'},"\
                "	exporting: { enabled: false },"\
                "	credits: { enabled: false},"\
                "	title: { style: { display: 'none'}},"\
                "	tooltip: {"\
                "		pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b><br/>"+y_axis_name+": <b>${point.y}</b>'},"\
                "	plotOptions: {"\
                "		pie: { "\
                "			borderWidth: 0.1,"\
                "			allowPointSelect: true,"\
                "			cursor: 'pointer',"\
                "			dataLabels: {"\
                "				enabled: false"\
                "			},"\
                "			showInLegend: true"\
                "		}"\
                "	},"\
                "	legend: {"\
                "        align: 'right',"\
                "        verticalAlign: 'top'"\
                "	},"\
                "	series: [{"\
                "		name: '"+series_name+"',"\
                "		colorByPoint: true,"\
                "		data: "+chart_data+""\
                "		}]"\
                "		});"\
                "	});"\
                "}); "\
                "</script></div>"
