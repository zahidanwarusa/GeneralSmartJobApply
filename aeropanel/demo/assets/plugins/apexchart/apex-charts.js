// Helper functions (simulate your chartTheme.js)
     function getThemeMode() {
        return document.documentElement.getAttribute("data-bs-theme") === "dark"
          ? "dark"
          : "light";
      }

function getGridColor() {
      return "#e5e7eb";
    }
    function getThemeTextColor() {
      return "#374151";
    }
    function getTooltipTheme() {
      return "light";
    }

    // Chart 1: Donut
    const donutOptions = {
      chart: { type: "donut", height: 320 },
      labels: ["Website", "Mobile App", "Referral", "Social"],
      colors: ["#4f46e5", "#ef4444", "#f59e0b", "#22c55e"],
      legend: { position: "bottom", fontSize: "14px" },
      dataLabels: { style: { fontSize: "13px" } },
      tooltip: {
        theme: "dark",
        y: { formatter: (val) => val + "%" },
      },
      plotOptions: {
        pie: {
          donut: {
            labels: {
              show: true,
              total: { show: true, label: "Total", formatter: () => "100%" },
            },
          },
        },
      },
      series: [45, 25, 15, 15],
    };
    new ApexCharts(document.querySelector("#donutChart"), donutOptions).render();

    // Chart 2: Area
    const areaOptions = {
      chart: {
        type: "area",
        height: 350,
        toolbar: { show: false },
      },
      stroke: { curve: "smooth", width: 3 },
      dataLabels: { enabled: false },
      grid: { borderColor: getGridColor() },
      xaxis: {
        categories: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        labels: { style: { colors: getThemeTextColor(), fontSize: "12px" } },
      },
      yaxis: {
        labels: { style: { colors: getThemeTextColor(), fontSize: "12px" } },
      },
      tooltip: { theme: getTooltipTheme() },
      colors: ["#4f46e5", "#22c55e"],
      legend: { position: "top", horizontalAlign: "right" },
      series: [
        { name: "Users", data: [120, 200, 150, 300, 250, 400, 350] },
        { name: "Sessions", data: [80, 150, 100, 200, 180, 250, 220] },
      ],
    };
    new ApexCharts(document.querySelector("#areaChart"), areaOptions).render();

    // Chart 3: Line
    const lineOptions = {
      chart: {
        type: "line",
        height: 350,
        zoom: { enabled: false },
        toolbar: { show: false },
      },
      stroke: { curve: "smooth", width: 3 },
      grid: { borderColor: getGridColor() },
      xaxis: {
        categories: ["Jan", "Feb", "Mar", "Apr", "May"],
        labels: { style: { colors: getThemeTextColor(), fontSize: "12px" } },
      },
      yaxis: {
        labels: { style: { colors: getThemeTextColor(), fontSize: "12px" } },
      },
      tooltip: { theme: getTooltipTheme() },
      title: {
        text: "Monthly Revenue",
        align: "left",
        style: { fontSize: "16px", color: getThemeTextColor() },
      },
      colors: ["#4f46e5"],
      series: [{ name: "Revenue", data: [4500, 4700, 5200, 6100, 6900] }],
    };
    new ApexCharts(document.querySelector("#lineChart"), lineOptions).render();


     // Chart 4: Pie
    const Pieoptions = {
      chart: {
        type: "pie",
        height: 350,
      },
      labels: ["Desktop", "Tablet", "Mobile", "Others"],
      colors: ["#4f46e5", "#22c55e", "#f59e0b", "#ef4444"],
      legend: {
        position: "bottom",
        fontSize: "14px",
      },
      dataLabels: {
        style: {
          fontSize: "13px",
        },
      },
      tooltip: {
        theme: "dark",
        y: {
          formatter: function (val) {
            return val + "%";
          },
        },
      },
      series: [44, 33, 23, 12],
    };

    new ApexCharts(document.querySelector("#pieChart"), Pieoptions).render();



     // Chart 5: Bar chart
    const BarChartoptions = {
      chart: {
        type: "bar",
        height: 360,
        toolbar: { show: false },
        animations: {
          enabled: true,
          easing: "easeinout",
          speed: 800,
        },
      },
      plotOptions: {
        bar: {
          borderRadius: 6,
          columnWidth: "40%",
          endingShape: "rounded",
        },
      },
      dataLabels: { enabled: false },
      stroke: {
        show: true,
        width: 3,
        colors: ["transparent"],
      },
      grid: {
        borderColor: "#e5e7eb", // light gray grid
      },
      xaxis: {
        categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        labels: {
          style: {
            colors: "#374151",
            fontSize: "13px",
          },
        },
      },
      yaxis: {
        title: {
          text: "Orders",
          style: {
            color: "#374151",
            fontSize: "14px",
          },
        },
        labels: {
          style: {
            colors: "#374151",
            fontSize: "12px",
          },
        },
      },
      fill: {
        type: "gradient",
        gradient: {
          shade: "light",
          type: "vertical",
          shadeIntensity: 0.4,
          gradientToColors: ["#00C9A7", "#FF6B6B"],
          inverseColors: false,
          opacityFrom: 1,
          opacityTo: 1,
          stops: [0, 100],
        },
      },
      tooltip: {
        theme: "dark",
        y: {
          formatter: (val) => `${val} orders`,
        },
      },
      colors: ["#00BFFF", "#FF69B4"],
      legend: {
        position: "top",
        horizontalAlign: "center",
        fontSize: "14px",
        labels: {
          colors: "#374151",
        },
      },
      series: [
        {
          name: "Website",
          data: [440, 505, 414, 671, 520, 610],
        },
        {
          name: "Mobile App",
          data: [380, 420, 390, 450, 480, 500],
        },
      ],
    };

    new ApexCharts(document.querySelector("#barChart"), BarChartoptions).render();


    // Chart 6: Bar chart
    const MixedChartoptions = {
      chart: {
        type: "line",
        stacked: false,
        height: 360,
        toolbar: { show: false },
      },
      stroke: {
        width: [0, 2],
        curve: "smooth",
      },
      plotOptions: {
        bar: {
          columnWidth: "40%",
          borderRadius: 6,
        },
      },
      grid: {
        borderColor:
          document.documentElement.getAttribute("data-bs-theme") === "dark"
            ? "rgba(255,255,255,0.1)"
            : "rgba(0,0,0,0.1)",
      },
      xaxis: {
        categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        labels: {
          style: {
            colors: getThemeTextColor(),
            fontSize: "12px",
          },
        },
      },
      yaxis: [
        {
          title: {
            text: "Revenue (₹)",
            style: { color: getThemeTextColor(), fontSize: "13px" },
          },
          labels: {
            style: { colors: getThemeTextColor(), fontSize: "12px" },
          },
        },
        {
          opposite: true,
          title: {
            text: "Growth (%)",
            style: { color: getThemeTextColor(), fontSize: "13px" },
          },
          labels: {
            style: { colors: getThemeTextColor(), fontSize: "12px" },
          },
        },
      ],
      tooltip: {
        shared: true,
        intersect: false,
        theme: getTooltipTheme(),
      },
      colors: ["#00BFFF", "#FF6B6B"],
      legend: {
        position: "top",
        horizontalAlign: "center",
        labels: { colors: getThemeTextColor() },
      },
      series: [
        {
          name: "Revenue",
          type: "bar",
          data: [12000, 15000, 14000, 18000, 17000, 20000],
        },
        {
          name: "Growth Rate",
          type: "line",
          data: [5, 7, 6, 8, 7.5, 9],
        },
      ],
    };

    // Render Chart
    new ApexCharts(document.querySelector("#mixedChart"), MixedChartoptions).render();


   // chart 7 
    const RadialChartoptions = {
      chart: {
        type: "radialBar",
        height: 320,
      },
      plotOptions: {
        radialBar: {
          hollow: {
            margin: 15,
            size: "70%",
          },
          track: {
            background: "rgba(0, 0, 0, 0.1)",
            strokeWidth: "100%",
          },
          dataLabels: {
            name: {
              offsetY: -10,
              color: "#888",
              fontSize: "16px",
            },
            value: {
              color: "#111",
              fontSize: "22px",
              show: true,
            },
          },
        },
      },
      fill: {
        type: "gradient",
        gradient: {
          shade: "dark",
          type: "horizontal",
          gradientToColors: ["#4f46e5"],
          stops: [0, 100],
        },
      },
      colors: ["#00C9A7"],
      stroke: {
        lineCap: "round",
      },
      labels: ["Progress"],
      series: [76], // percentage value
    };

    new ApexCharts(document.querySelector("#radialChart"), RadialChartoptions).render();


   // chart 8
   const RadarChartoptions = {
      chart: {
        type: 'radar',
        height: 360,
        toolbar: { show: false },
      },
      xaxis: {
        categories: ['React', 'Bootstrap', 'Recharts', 'Routing', 'UX', 'Modularity'],
        labels: {
          style: {
            fontSize: '13px',
            colors: ['#333','#333','#333','#333','#333','#333']
          }
        }
      },
      stroke: {
        width: 2,
      },
      fill: {
        opacity: 0.3,
      },
      markers: {
        size: 4,
      },
      tooltip: {
        shared: true,
        intersect: false,
      },
      legend: {
        position: 'top',
      },
      colors: ['#4f46e5', '#22c55e'],
      series: [
        {
          name: 'Current Skill',
          data: [90, 85, 95, 80, 88, 92],
        },
        {
          name: 'Target Skill',
          data: [100, 90, 98, 90, 95, 95],
        },
      ],
    };

  new ApexCharts(document.querySelector("#radarChart"), RadarChartoptions).render();