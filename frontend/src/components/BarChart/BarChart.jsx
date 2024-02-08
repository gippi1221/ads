import React from 'react'
import { Column } from '@ant-design/plots';

const BarChart = ({attribute, data, metric}) => {

  

  const config = {
    data: data.map(d => ({date: d.date, metric: d[metric], attribute: d[attribute] && (d[attribute]).toString()})),
    xField: 'date',
    yField: 'metric',
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