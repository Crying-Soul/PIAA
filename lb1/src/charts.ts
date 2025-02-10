import QuickChart from 'quickchart-js';

export function createChart(results: any[]) {
  const chart = new QuickChart();

  chart.setConfig({
    type: 'line',
    data: {
      labels: results.map(r => r.n),
      datasets: [{
        label: 'Number of Operations',
        data: results.map(r => r.operations),
        borderColor: '#4A90E2',
        backgroundColor: 'rgba(74, 144, 226, 0.2)',
        borderWidth: 3,
        pointRadius: 4,
        pointBackgroundColor: '#4A90E2',
        pointBorderColor: '#FFFFFF',
        fill: true,
        tension: 0.4,
        cubicInterpolationMode: 'monotone'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: 'Backtracking Algorithm Complexity Analysis',
          font: { size: 20, family: 'Arial', weight: 'bold' },
          padding: { top: 20, bottom: 20 }
        },
        legend: {
          display: true,
          position: 'top',
          labels: {
            font: { size: 14 },
            usePointStyle: true,
            boxWidth: 10
          }
        },
        tooltip: {
          mode: 'index',
          intersect: false,
          backgroundColor: 'rgba(0, 0, 0, 0.75)',
          titleFont: { size: 16, family: 'Arial', weight: 'bold' },
          bodyFont: { size: 14, family: 'Arial' },
          padding: 12,
          callbacks: {
            label: function(context) {
              let label = context.dataset.label || '';
              if (label) {
                label += ': ';
              }
              if (context.parsed.y !== null) {
                label += context.parsed.y.toLocaleString();
              }
              return label;
            }
          }
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Grid Size (n)',
            font: { size: 16, weight: 'bold' }
          },
          grid: {
            display: true,
            color: 'rgba(0,0,0,0.1)'
          },
          ticks: {
            font: { size: 14 }
          }
        },
        y: {
          type: 'logarithmic',
          title: {
            display: true,
            text: 'Number of Operations',
            font: { size: 16, weight: 'bold' }
          },
          grid: {
            display: true,
            color: 'rgba(0,0,0,0.1)'
          },
          ticks: {
            font: { size: 14 },
            callback: function(value) {

              return Number(value).toLocaleString();
            }
          }
        }
      },
      elements: {
        line: {
          borderWidth: 2,
          borderCapStyle: 'round'
        },
        point: {
          hoverRadius: 6,
          hoverBorderWidth: 2
        }
      },
      layout: {
        padding: {
          left: 30,
          right: 30,
          top: 20,
          bottom: 20
        }
      },
      animation: {
        duration: 1500,
        easing: 'easeInOutQuad'
      }
    }
  });

  chart.setWidth(1200);
  chart.setHeight(600);
  chart.setBackgroundColor('#ffffff');

  console.log(`\nChart URL: ${chart.getUrl()}\n`);
}
