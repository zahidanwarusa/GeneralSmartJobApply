$(function () {
    "use strict";

// Revenue Line Chart
const revenueChartOptions = {
  chart: { type: "line", sparkline: { enabled: true }, height:"80" },
  stroke: { curve: "smooth", width: 2 },
  colors: ["#4f46e5"],
  tooltip: { enabled: false },
};
const revenueChartSeries = [{ name: "Revenue", data: [45, 52, 48, 56, 43, 59, 51] }];
new ApexCharts(document.querySelector("#revenueChart"), {
  ...revenueChartOptions,
  series: revenueChartSeries
}).render();


// Orders Bar Chart
const ordersChartOptions = {
  chart: { type: "bar", sparkline: { enabled: true }, height:"80" },
  plotOptions: { bar: { borderRadius: 4, columnWidth: "60%" } },
  stroke: { width: 0 },
  colors: ["#4f46e5"],
  tooltip: { enabled: false },
};
const ordersChartSeries = [{ name: "Orders", data: [180, 220, 260, 310, 340, 370] }];
new ApexCharts(document.querySelector("#ordersChart"), {
  ...ordersChartOptions,
  series: ordersChartSeries
}).render();


// Visitor Line Chart
const visitorChartOptions = {
  chart: { type: "area", sparkline: { enabled: true }, height:"80"  },
  stroke: { curve: "smooth", width: 2 },
  markers: {
    size: 0,
    strokeWidth: 2,
    strokeColors: "#4f46e5",
    fillOpacity: 1,
    colors: ["#ffffff"],
  },
  fill: {
    type: "gradient",
    gradient: { shadeIntensity: 1, opacityFrom: 0.4, opacityTo: 0, stops: [0, 100] },
  },
  colors: ["#4f46e5"],
  tooltip: { enabled: false },
};
const visitorChartSeries = [{ name: "Revenue", data: [47, 50, 46, 58, 41, 63, 49] }];
new ApexCharts(document.querySelector("#visitorChart"), {
  ...visitorChartOptions,
  series: visitorChartSeries
}).render();


// Conversion Bar Chart
const conversionChartOptions = {
  chart: { type: "bar", sparkline: { enabled: true }, height:"80" },
  plotOptions: { bar: { borderRadius: 4, columnWidth: "60%" } },
  stroke: { width: 0 },
  colors: ["#4f46e5"],
  tooltip: { enabled: false },
};
const conversionChartSeries = [{ name: "Conversion Rate", data: [180, 240, 210, 295, 330, 310] }];
new ApexCharts(document.querySelector("#conversionChart"), {
  ...conversionChartOptions,
  series: conversionChartSeries
}).render();


// Traffic Pie Chart
const trafficPiechartOptions = {
  chart: { type: "donut", },
  labels: ["Facebook", "Instagram", "Other"],
  colors: ["#4f46e5", "#b3b3ff", "#dcdcff"],
  legend: { show: false },
  dataLabels: { enabled: false },
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
};
const trafficPiechartSeries = [100.6, 33.8, 20.6];
new ApexCharts(document.querySelector("#trafficPieChart"), {
  ...trafficPiechartOptions,
  series: trafficPiechartSeries
}).render();


// Sales Line Chart
const salesChartOptions = {
  chart: {
    type: "area",
    height: "380",
    sparkline: { enabled: false },
    toolbar: { show: false },
    zoom: { enabled: false },
  },
  stroke: { curve: "smooth", width: 3 },
  markers: {
    size: 0,
    strokeWidth: 2,
    strokeColors: "#4f46e5",
    fillOpacity: 1,
    colors: ["#ffffff"],
    hover: { size: 8 },
  },
  fill: {
    type: "gradient",
    gradient: { shadeIntensity: 1, opacityFrom: 0.7, opacityTo: 0, stops: [0, 100] },
  },
  colors: ["#4f46e5"],
  tooltip: { theme: "light", enabled: true },
  dataLabels: { enabled: false },
  grid: {
    borderColor:
      document.documentElement.getAttribute("data-bs-theme") === "dark"
        ? "rgba(255,255,255,0.1)"
        : "rgba(0,0,0,0.1)",
  },
  xaxis: {
    categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
    labels: { style: { colors: "#6b7280", fontSize: "12px" } },
    axisBorder: { color: "#6b7280" },
    axisTicks: { color: "#6b7280" },
  },
  yaxis: {
    labels: { style: { colors: "#6b7280", fontSize: "12px" } },
  },
};
const salesChartSeries = [{ name: "Revenue", data: [42, 50, 47, 53, 46, 61, 55] }];
new ApexCharts(document.querySelector("#salesAnalysisChart"), {
  ...salesChartOptions,
  series: salesChartSeries
}).render();

    
});