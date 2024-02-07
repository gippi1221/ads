import clickhouse_connect
from clickhouse_connect import common
from models import Event
from helpers import parse_filters

class Database:
  def __init__(self, host: str, port: int, database: str):
    common.set_setting('autogenerate_session_id', False)
    self.client = clickhouse_connect.get_client(host=host, port=port, database=database)

  def insert_event(self, table: str, event_data: Event):
    column_names = list(event_data.model_fields.keys())
    values = [event_data.model_dump()[field] for field in event_data.model_fields.keys()]
    self.client.insert(table, [values], column_names=column_names)

  def query(self, query_string: str, parameters: dict = None):
    return self.client.query(query_string, parameters=parameters)
