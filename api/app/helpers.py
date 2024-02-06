import json

def parse_filters(filters_str: str) -> list:
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
  
