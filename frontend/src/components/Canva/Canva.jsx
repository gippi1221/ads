import React, { useContext, useEffect, useState } from 'react'
import { Context } from '../..'
import { observer } from 'mobx-react-lite';
import BarChart from '../BarChart/BarChart';
import { fetchEvents } from '../../api/general';

const Canva = observer(() => {

  const { general } = useContext(Context)
  const [data, setData] = useState([])

  useEffect(() => {
    if (!general.params.groupBy) return
    
    async function fetchData() {
      const data = await fetchEvents(general.params.groupBy, general.params.metrics, general.params.granularity, general.params.startDate, general.params.endDate, general.params.filters)
      setData(data.results)
    }

    fetchData()
  }, [general.params])

  if (!general.params.groupBy) {
    return (
      <div>fill the filters</div>
    )
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'row' }}>

      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        {
          general.params.groupBy.split(',').map(a => (
            <div key={a} style={{ width: '100%' }}>
              <div style={{ padding: 8 }}>% {general.params.metrics.split(',')[0]} by event date and {a}</div>
              <BarChart attribute={a} data={data} metric={general.params.metrics.split(',')[0]} />
            </div>
          ))
        }
      </div>
      
      {
        general.params.metrics.split(',').length > 1 &&
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          {
            general.params.groupBy.split(',').map(a => (
              <div key={a} style={{ width: '100%' }}>
                <div style={{ padding: 8 }}>% {general.params.metrics.split(',')[1]} by event date and {a}</div>
                <BarChart attribute={a} data={data} metric={general.params.metrics.split(',')[1]} />
              </div>
            ))
          }
        </div>
      }
    </div>
  )
})

export default Canva