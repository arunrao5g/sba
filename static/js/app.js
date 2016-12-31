'use strict';

angular.module('myApp', [])
  .controller('ReportControler', function($scope, $http, $sce){
    $scope.$watch('search', function() {
      fetch();
    });

    function fetch(){
      if($(search_concept).text() != 'Source'){
      $http.post("http://127.0.0.1:8001/searchanalytics", {
                searchQuery : $scope.search,
                chartType : 'graph',
                groupClass : $(search_concept).text()

            })
      .then(function(response){
            $scope.details = response;
            $scope.chart_tag = $sce.trustAsHtml(response.data.meta.html_tag);
          }
       );
       }
    }

    $scope.select = function(){
      this.setSelectionRange(0, this.value.length);
    }
  });

//  $scope.details =
