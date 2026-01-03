// Chart 1 - Area Chart
const areaChart = new ApexCharts(document.querySelector("#netIncomeChart"), {
    chart: {
        width: 180,
        height: 60,
        type: "area",
        sparkline: { enabled: true },
    },
    stroke: {
        curve: "smooth",
        width: 2,
    },
    fill: {
        type: "gradient",
        gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.4,
            opacityTo: 0,
            stops: [0, 100],
        },
    },
    colors: ["#28a745"],
    tooltip: {
        enabled: false,
    },
    series: [{
        data: [45, 52, 48, 56, 43, 59, 51]
    }]
});
areaChart.render();

// Chart 2 - Line Chart
const lineChart = new ApexCharts(document.querySelector("#totalSalesChart"), {
    chart: {
        width: 180,
        height: 60,
        type: "line",
        sparkline: { enabled: true },
    },
    stroke: {
        curve: "straight",
        width: 2,
    },
    colors: ["#f15406"],
    tooltip: {
        enabled: false,
    },
    series: [{
        name: "Income",
        data: [45, 52, 48, 56, 43, 59, 51]
    }]
});
lineChart.render();


// Chart 3 - Bar Chart
const barChart = new ApexCharts(document.querySelector("#newOffersChart"), {
    chart: {
        width: 180,
        height: 60,
         type: "area",
        sparkline: { enabled: true },
    },
    plotOptions: {
        bar: {
            borderRadius: 6,
            columnWidth: "60%",
        },
    },
    stroke: {
        curve: "smooth",
        width: 2,
    },
    fill: {
        type: "gradient",
        gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.4,
            opacityTo: 0,
            stops: [0, 100],
        },
    },
    colors: ["#4f46e5"],
    tooltip: {
        enabled: false,
    },
    series: [{
        name: "Income",
         data: [45, 52, 48, 56, 43, 59, 51]
    }]
});
barChart.render();


// Chart 4 - Traffic Donut Chart
const trafficDonutChart = new ApexCharts(document.querySelector("#trafficDonutChart"), {
    chart: {
        height: 300,
        type: "donut",
    },
    labels: ["Facebook", "Instagram", "Other"],
    colors: ["#4f46e5", "#b3b3ff", "#dcdcff"],
    legend: { show: false },
    dataLabels: {
        enabled: false,
    },
    plotOptions: {
        pie: {
            donut: {
                size: "80%",
                labels: {
                    show: true,
                    name: { show: false },
                    value: { show: false },
                    total: {
                        show: true,
                        label: "FACEBOOK",
                        fontSize: "14px",
                        color: "#4f46e5",
                    },
                },
            },
        },
    },
    tooltip: { enabled: false },
    series: [100.6, 33.8, 20.6]
});
trafficDonutChart.render();

// Chart 5 - Sales Mixed Chart
const salesChart = new ApexCharts(document.querySelector("#salesLineChart"), {
    chart: {
        height: 220,
        type: "line",
        sparkline: { enabled: true },
    },
    stroke: {
        width: [0, 3],
        curve: "smooth",
    },
    markers: {
        size: 7,
        strokeWidth: 2,
        strokeColors: "#22c55e",
        fillOpacity: 1,
        colors: ["#ffffff"],
    },
    plotOptions: {
        bar: {
            borderRadius: 6,
            columnWidth: "40%",
        },
    },
    fill: {
        opacity: [1, 1],
    },
    colors: ["#4f46e5", "#22c55e"],
    tooltip: {
        enabled: false,
    },
    series: [
        {
            name: "Clients",
            type: "bar",
            data: [8, 14, 20, 28, 32, 36, 42]
        },
        {
            name: "Engagement",
            type: "line",
            data: [18, 24, 45, 38, 60, 46, 52]
        }
    ]
});
salesChart.render();

// Chart 6 - Radial Chart
const radialChart = new ApexCharts(document.querySelector("#expenseRadialChart"), {
    chart: {
        width: 140,
        height: 140,
        type: "radialBar",
        sparkline: { enabled: true },
    },
    plotOptions: {
        radialBar: {
            hollow: {
                size: "55%",
            },
            track: {
                background: "#f1f5f9",
            },
            dataLabels: {
                name: {
                    show: false,
                },
                value: {
                    offsetY: 5,
                    fontSize: "18px",
                    color: "#16a34a",
                    formatter: () => "68%",
                },
            },
        },
    },
    colors: ["#16a34a"],
    stroke: {
        lineCap: "round",
    },
    series: [68]
});
radialChart.render();

// Chart 7 - Bar Chart
const sixMonthRevenubarChart = new ApexCharts(document.querySelector("#sixMonthRevenubarChart"), {
  chart: {
    //width: 200,
    height: 160,
    type: "bar",
    sparkline: { enabled: true },
  },
  plotOptions: {
    bar: {
      borderRadius: 6,
      columnWidth: "60%",
    },
  },
  stroke: {
    width: 0,
  },
  colors: ["#4f46e5"],
  tooltip: {
    enabled: false,
  },
  series: [
    {
      name: "Income",
      data: [32, 38, 44, 51, 58, 65, 72],
    },
  ],
});
sixMonthRevenubarChart.render();