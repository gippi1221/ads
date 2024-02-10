import React from 'react'
import { Column } from '@ant-design/plots';

const BarChart = ({attribute, data, metric}) => {

  const result = data.reduce((acc, d) => {
    const key = `${d.dataset}_${d.date}_${d[attribute]}`;
    if (!acc[key]) {
      acc[key] = {
        dataset: d.dataset,
        date: d.date,
        attribute: d[attribute] && (d[attribute]).toString(),
        total: 0
      };
    }
    acc[key].total += d[metric];
    return acc;
  }, {});

  console.log(Object.values(result))

  const config = {
    data: Object.values(result),
    xField: 'date',
    yField: 'total',
    stack: true,
    colorField: 'attribute',
    legend: false,
    percent: true,
    interaction: {
      tooltip: {
        shared: true,
      },
    },
    tooltip: { channel: 'y0', valueFormatter: (d) => `${(d * 100).toFixed(2)}%` },
  };

  return <Column {...config} />;
}

export default BarChart