import React from 'react'
import { Column } from '@ant-design/plots';

const BarChart = ({attribute, data, metric}) => {

  console.log(data.filter(d => d.attribute1 === 111))

  const config = {
    data,//: data.filter(d => [111, 222, 333, 444, 555, 666, 777, 888, 999, 1111, 2222, 3333, 4444, 5555, 6666, 7777, 8888, 9999].includes(d.attribute1)),
    xField: 'date',
    yField: metric,
    stack: true,
    colorField: attribute,
    tooltip: false,
  };

  return <Column {...config} />;
}

export default BarChart