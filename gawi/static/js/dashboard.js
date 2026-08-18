/* ==================================
   Dashboard - Bar Graph
   ================================== */

let weeklyChart;

document.addEventListener('DOMContentLoaded', () => {
  const weeklyData = JSON.parse(document.getElementById('weekly-data').textContent);
  const habitCount = JSON.parse(document.getElementById('habit-count').textContent);

  const axisColor = getComputedStyle(document.documentElement)
    .getPropertyValue('--chart-axis-color')
    .trim();

  const gridColor = getComputedStyle(document.documentElement)
    .getPropertyValue('--chart-grid-color')
    .trim();

  const labels = weeklyData.map((day) => day.day.slice(0, 3));
  const values = weeklyData.map((day) => day.completed);

  const ctx = document.getElementById('weeklyChart');
  weeklyChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Habits Completed',
          data: values,
          backgroundColor: '#79AE6F',
          borderRadius: 8,
          borderSkipped: false,
          barThickness: 20,
        },
      ],
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          enabled: true,

          backgroundColor: '#494949',

          displayColors: false,

          callbacks: {
            title: function (context) {
              return context[0].label; // e.g. Monday
            },

            label: function (context) {
              return `${context.raw} habits completed`;
            },
          },

          titleFont: {
            family: 'LT Saeada',
            size: 14,
            weight: 'bold',
          },

          bodyFont: {
            family: 'LT Saeada',
            size: 12,
          },

          padding: 12,

          cornerRadius: 8,
        },
      },
      scales: {
        x: {
          beginAtZero: true,
          max: habitCount,
          ticks: {
            stepSize: 1,
            precision: 0,
            font: {
              family: 'LT Saeada',
              weight: 200,
            },
          },
          grid: {
            drawBorder: false,
            color: gridColor,
          },
          border: {
            color: axisColor,
          },
        },
        y: {
          ticks: {
            font: {
              family: 'LT Saeada',
              weight: 200,
            },
          },
          grid: {
            display: false,
          },
          border: {
            color: axisColor,
          },
        },
      },
    },
  });
});

function updateChartTheme() {
  if (!weeklyChart) return;

  const axisColor = getComputedStyle(document.documentElement)
    .getPropertyValue('--chart-axis-color')
    .trim();

  const gridColor = getComputedStyle(document.documentElement)
    .getPropertyValue('--chart-grid-color')
    .trim();

  weeklyChart.options.scales.x.border.color = axisColor;
  weeklyChart.options.scales.y.border.color = axisColor;

  weeklyChart.options.scales.x.grid.color = gridColor;
  weeklyChart.options.scales.y.grid.color = gridColor;

  weeklyChart.update();
}

/* ==================================
   Dashboard - Heatmap Tooltip
   ================================== */

document.addEventListener('DOMContentLoaded', () => {
  const cells = document.querySelectorAll('.heatmap-cell');
  const tooltip = document.getElementById('heatmapTooltip');

  console.log('Heatmap cells:', cells.length);
  console.log('Heatmap tooltip:', tooltip);

  if (!tooltip || cells.length === 0) {
    return;
  }

  cells.forEach((cell) => {
    cell.addEventListener('mouseenter', () => {
      const date = cell.dataset.date;
      const count = cell.dataset.count;

      // Don't show tooltip for padding cells
      if (!date) {
        return;
      }

      tooltip.innerHTML = `
                <strong>${date}</strong>
                <br>
                ${count} habit${count == 1 ? '' : 's'} completed
            `;

      tooltip.style.display = 'block';
    });

    cell.addEventListener('mousemove', (event) => {
      tooltip.style.left = `${event.clientX + 12}px`;
      tooltip.style.top = `${event.clientY + 12}px`;
    });

    cell.addEventListener('mouseleave', () => {
      tooltip.style.display = 'none';
    });
  });
});
