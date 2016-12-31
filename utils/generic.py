import re

USR = "root"
PWD = "sriganesha"
HOST = "localhost"
PYPATH = "/Users/arunrao/Home/Learnings/Spark-WorkBenck/spark-1.5.2-bin-hadoop2.6/python/"
PY4JPATH = "/Users/arunrao/Home/Learnings/Spark-WorkBenck/spark-1.5.2-bin-hadoop2.6/python/lib/py4j-0.8.2.1-src.zip"
SPARKHOME = "/Users/arunrao/Home/Learnings/Spark-WorkBenck/spark-1.5.2-bin-hadoop2.6"
time_series = ['year', 'quarter', 'month', 'week', 'day', 'daily']

container_st_tag = "<div class='container' id='main'><div class='row'><div class='col-sm-8'>"
container_ed_tag = "</div></div></hr>"

class Static:
    @staticmethod
    def attribute_query(p_group_class):
        return "select lower(name) AS name, class, target_table, " \
                 "metric_flag, filter_flag, filter_value, column_name, time_series, drill_down, metric_prefix " \
                 "from analytical_dictionary " \
                 "where lower(group_class) = '"+p_group_class+"' order by orderby"

    @staticmethod
    def get_source_table(p_group_class):
        return "select source_table from source where group_class = '"+p_group_class+"'"

    @staticmethod
    def join_query(target_table_list):
        return "select source_f_key, target_p_key from metadata " \
               "where target_table in ('" + target_table_list.replace(', ',"','") + "');"

    @staticmethod
    def chart_id_query():
        return "select coalesce(max(id),1) from saved_queries"

    @staticmethod
    def get_kpi(metric_name, metric_value, prefix):
        return "<div id='kpitag' class='kpi_box'><div style='font-size:23px;'>" \
                "<div class='dropdown-toggle' type='button' id='menu' data-toggle='dropdown'><div class='chart-edit'></div></div>"\
                "<ul class='dropdown-menu dropdown-menu-right' role='menu' aria-labelledby='menu'>"\
                "<li role='presentation' class='disabled'><a role='menuitem' tabindex='-1' href='#'>Save to Dashboard</a></li>"\
                "<li role='presentation'><a role='menuitem' tabindex='-1' href='#'>Email</a></li>"\
                "<li role='presentation' class='divider'></li>"\
                "<li role='presentation'><a role='menuitem' tabindex='-1' href='#'>Delete</a></li>"\
                "</ul>"\
                + re.sub("([a-z])([A-Z])","\g<1> \g<2>",metric_name) + "</div> " + prefix +'{:20,.2f}'.format(metric_value) + "</div>"\
                "</div>"\
                "</div>"\
                "<script>"\
                "$(function () {"\
                "$('#rename-chart').click(function () {"\
                "var span_val = document.getElementById('chart-title').value;"\
                "$('#chart-title').text(span_val);"\
                "$('#chart-title').replaceWith($('<textarea >').attr({ id: 'chart-title', class: 'chart-title chart-title-edit'}));"\
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
                "$('#chart-title').replaceWith($('<textarea >').attr({ id: 'chart-title', class: 'chart-title chart-title-edit'}));"\
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
    def get_pie_chart(chart_data, y_axis_name, series_name, prefix):
        return "<div class='div-continer' style='height:400px;' id='chartContainer'>"\
                "<script>"\
                "$(function () {  $(document).ready(function () {" \
                    "Highcharts.setOptions({"\
	                    "colors: ['#2BAFDE','#FFAC37','#D95B90','#CAD144','#FA6931','#FFD33B','#2A5D9C','#80B94A']"\
	                "});"\
                    "Highcharts.chart('chartContainer', {"\
                    "chart: { type: 'pie'},"\
                    "exporting: { enabled: false },"\
                    "credits: { enabled: false},"\
                    "title: { style: { display: 'none'}},"\
                    "tooltip: {"\
                        "pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b><br/>"+y_axis_name+"<b>: "+prefix+"{point.y}</b>'"\
                    "},"\
                    "plotOptions: {"\
                        "pie: { "\
                            "borderWidth: 0.1,"\
                            "allowPointSelect: true,"\
                            "cursor: 'pointer',"\
                            "dataLabels: {"\
                                "enabled: true"\
                            "},"\
                            "showInLegend: true"\
                        "}"\
                    "},"\
                    "legend: {"\
                        "align: 'right',"\
                        "verticalAlign: 'top'"\
                    "},"\
                    "series: [{"\
                        "name: '"+series_name+"',"\
                        "colorByPoint: true,"\
                        "data: "+chart_data+""\
                        "}]"\
                    "});});"\
                "});"\
                "</script></div>"

    @staticmethod
    def get_column_chart(chart_data, categories, prefix):
        return "<div class='div-continer' style='height:400px;' id='chartContainer'>"\
                "<script>"\
                "$(function () {  $(document).ready(function () {" \
                    "Highcharts.setOptions({"\
	                    "colors: ['#2BAFDE','#FFAC37','#D95B90','#CAD144','#FA6931','#FFD33B','#2A5D9C','#80B94A']"\
	                "});"\
                    "Highcharts.chart('chartContainer', {"\
                    "exporting: { enabled: false },"\
                    "credits: { enabled: false},"\
                    "title: { style: { display: 'none'}},"\
                    "tooltip: {"\
			            "formatter: function () {"\
            	            "return this.series.xAxis.categories[this.point.x]+" \
                                    "'<b>: "+prefix+"'+this.point.y+'</b>'"\
			            "}"\
                    "},"\
                    "xAxis: {"\
                        "categories:[" + categories + "]" \
                    "},"\
                    "series: [{"\
                        "type: 'column',"\
                        "colorByPoint: true,"\
                        "data: ["+ chart_data +"],"\
                        "showInLegend: false"\
                        "}]"\
                    "});});"\
                "});"\
                "</script></div>"

    @staticmethod
    def get_drill_down_chart(chart_data, series, series_name, y_axis_name):
        return "<div class='div-continer' style='height:400px;' id='chartContainer'>"\
                "<script>"\
                "$(function () {  $(document).ready(function () {" \
                    "Highcharts.setOptions({"\
	                    "colors: ['#2BAFDE','#FFAC37','#D95B90','#CAD144','#FA6931','#FFD33B','#2A5D9C','#80B94A']"\
	                "});"\
                    "Highcharts.chart('chartContainer', {"\
                    "chart: {type: 'column'},"\
                    "exporting: { enabled: false },"\
                    "credits: { enabled: false},"\
                    "subtitle: {text: 'Click on individual "+series_name+" to view details'},"\
                    "title: { style: { display: 'none'}},"\
                    "tooltip: {"\
			            "headerFormat: '<span style=\"font-size:11px\">{series.name}</span><br>',"\
                        "pointFormat: '<span style=\"color:{point.color}\">{point.name}</span> "+y_axis_name+": <b>{point.y}</b><br/>'"\
                    "},"\
                    "xAxis: {"\
                        "type: 'category'" \
                    "},"\
                    "plotOptions: {"\
                        "series: {"\
                        "borderWidth: 0,"\
                        "dataLabels: {"\
                            "enabled: true,"\
                            "format: '{point.y}'"\
                            "}" \
                        "}"\
                    "},"\
                    "series: [{"\
                        "name: '"+series_name+"',"\
                        "colorByPoint: true,"\
                        "data:"+ chart_data + "}],"\
                    "drilldown: {"\
                        "series: "+ series +\
                    "}" \
                    "});});"\
                "});"\
                "</script></div>"
