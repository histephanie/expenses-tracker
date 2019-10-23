var options = {
    chart: {
        width: 600,
        type: 'donut',
    },
    plotOptions: {
        pie: {
          donut: {
            labels: {
              show: true,
              name: {
                  show: true
              },
              value: {
                  show: true,
                  formatter: function (val) {
                    return val
                  }
              },
              total: {
                  show: true
              }
            }
          }
        }
    },
    labels: categories,
    series: spent,
    dataLabels: {
        enabled: true,
    },
    responsive: [{
        breakpoint: 480,
        options: {
            chart: {
                width: 200
            },
            legend: {
                position: 'bottom'
            }
        }
    }]
}

console.log(options);

var chart = new ApexCharts(
    document.querySelector("#chart"),
    options
);

chart.render();
