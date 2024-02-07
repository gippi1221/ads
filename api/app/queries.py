from helpers import parse_filters

def build_stats_sql_query(groupBy: str, filters: str, metrics: str, granularity: str, startDate: str, endDate: str):
  """
  This function constructs the sql query with the details provided

  Returns:
    1) constructed sql query
    2) parameters
  """
  where_list = []
  params = {}

  #gather predicates and where clause
  if startDate:
    where_list.append("event_date >= {start_date:DateTime}")
    params['start_date'] = startDate

  if endDate:
    where_list.append("event_date < {end_date:DateTime}")
    params['end_date'] = endDate
  
  if filters:
    parsed_filters = parse_filters(filters)
    for f in parsed_filters:
      attribute = f['attribute']
      value = f['value']

      if attribute == 'attribute1':
        int_value = int(value)
        where_list.append("attribute1 = {attribute1:Int64}")
        params['attribute1'] = int_value
      elif attribute == 'attribute2':
        int_value = int(value)
        where_list.append("attribute2 = {attribute2:Int64}")
        params['attribute2'] = int_value
      elif attribute == 'attribute3':
        int_value = int(value)
        where_list.append("attribute3 = {attribute3:Int64}")
        params['attribute3'] = int_value
      elif attribute == 'attribute4':
        where_list.append("attribute4 = {attribute4:String}")
        params['attribute4'] = value
      elif attribute == 'attribute5':
        where_list.append("attribute5 = {attribute5:String}")
        params['attribute5'] = value
      elif attribute == 'attribute6':
        where_list.append("attribute6 = {attribute6:Bool}")
        params['attribute6'] = value == 'true'
      else:
        raise ValueError("Unknown filter parameter")

  #build db query
  query = f"select {groupBy},date_trunc('{'hour' if granularity == 'hourly' else 'day'}', event_date) as date"

  for m in metrics.split(','):
    query += f",sum({m}) as {m}"

  query += f"\nfrom events"

  if where_list:
    where_clause = " and ".join(where_list)
    query += f"\nwhere {where_clause}"

  query += f"\ngroup by date_trunc('{'hour' if granularity == 'hourly' else 'day'}', event_date),{groupBy}"

  return query, params
