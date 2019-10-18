var options = {
    chart: {
        width: 480,
        type: 'pie',
    },
    labels: categories,
    series: spent,
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
