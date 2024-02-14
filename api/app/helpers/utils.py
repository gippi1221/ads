import json
import re
from datetime import datetime


def parse_filters(filters_str: str) -> list:
  """
  Function is to validate incoming string is json array
  Returns the list of values
  """
  if filters_str is None:
    return []
  try:
    filters_list = json.loads(filters_str)
    if not isinstance(filters_list, list):
      raise ValueError("Invalid filters format. Expected a list.")
    for item in filters_list:
      if not isinstance(item, dict):
        raise ValueError("Invalid filter item format. Expected a dictionary.")
      if "attribute" not in item or "value" not in item:
        raise ValueError("Filter item must contain 'attribute' and 'value' keys.")
    return filters_list
  except json.JSONDecodeError:
      raise ValueError("Invalid JSON format for filters.")
  
def convert_data_to_output(result):
  """
  Function is to convert clickhouse output to desired requestor output
  """
  data = []
  for row in result.result_rows:
    obj = {}
    for idx, val in enumerate(result.column_names):
      if isinstance(row[idx], datetime):
        obj[val] = row[idx].isoformat()
      elif isinstance(row[idx], float):
        obj[val] = round(row[idx], 2)
      else:
        obj[val] = row[idx]
    data.append(obj)
  return data

def validate_iso_date(date_str):
  """
  Function is to validate incoming string is ISO date
  """
  try:
    datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
  except ValueError:
    raise ValueError("Invalid date format. Expected format: YYYY-MM-DDTHH:mm:ss")

def validate_params(groupBy: str, filters: str, metrics: str, granularity: str, startDate: str, endDate: str):
  """
  Function is to validate incoming query parameters
  """
  #mandatory parameters
  if not re.match(r'^\w+(,\s*\w+)*$', metrics):
    raise ValueError("Invalid metrics value, must be comma-separated names")
  
  if not re.match(r'^\w+(,\s*\w+)*$', groupBy):
    raise ValueError("Invalid metrics value, must comma separated names")
  
  #others
  if startDate:
    validate_iso_date(startDate)

  if endDate:
    validate_iso_date(endDate)

  if filters:
    parsed_filters = parse_filters(filters)
    for f in parsed_filters:
      attribute = f['attribute']
      value = f['value']

      if attribute == 'attribute1':
        try:
          int(value)
        except ValueError:
          raise ValueError("Invalid value for attribute1. Expected an int.")
      elif attribute == 'attribute2':
        try:
          int(value)
        except ValueError:
          raise ValueError("Invalid value for attribute2. Expected an int.")
      elif attribute == 'attribute3':
        try:
          int(value)
        except ValueError:
          raise ValueError("Invalid value for attribute3. Expected an int.")
      elif attribute == 'attribute4':
        if not isinstance(value, str):
          raise ValueError("Invalid type for attribute4. Expected str.")
      elif attribute == 'attribute5':
        if not isinstance(value, str):
          raise ValueError("Invalid type for attribute5. Expected str.")
      elif attribute == 'attribute6':
        if value not in ['true', 'false']:
          raise ValueError("Invalid type for attribute6. Expected bool.")
      else:
        raise ValueError("Unknown filter parameter")
