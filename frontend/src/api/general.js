import $host from "./index"

//data
export const fetchEvents = async (groupBy, metrics, granularity, startDate, endDate, filters) => {
  let str = `/analytics/query?groupBy=${groupBy}&metrics=${metrics}&granularity=${granularity}`
  if (startDate) {
    str = str + `&startDate=${startDate}`
  }
  if (endDate) {
    str = str + `&endDate=${endDate}`
  }
  if (filters) {
    str = str + `&filters=${filters}`
  }

  const {data} = await $host.get(str)
  return data
}
