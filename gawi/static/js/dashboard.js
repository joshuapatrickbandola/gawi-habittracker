/* ==================================
   Dashboard - Bar Graph
   ================================== */

document.addEventListener('DOMContentLoaded', () => {
  const weeklyData = JSON.parse(document.getElementById('weekly-data').textContent);
  const habitCount = JSON.parse(document.getElementById('habit-count').textContent);

  const labels = weeklyData.map((day) => day.day.slice(0, 3));
  const values = weeklyData.map((day) => day.completed);

  const ctx = document.getElementById('weeklyChart');
  new Chart(ctx, {
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
        },
      },
    },
  });
});

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
