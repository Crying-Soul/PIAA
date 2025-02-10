import  QuickChart  from 'quickchart-js';

export function createChart(results: any[]) {

    const chart = new QuickChart();
    chart.setConfig({
        type: 'line',
        data: {
            labels: results.map(r => r.n),
            datasets: [{
                label: 'Operations vs Start Square Size',
                data: results.map(r => r.operations),
                borderColor: 'blue',
                fill: false
            }]
        }
    });

    console.log(`\nChart URL: ${chart.getUrl()}\n`);
}
