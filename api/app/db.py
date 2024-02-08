import clickhouse_connect
from clickhouse_connect import common
from models import Event

class Database:
  """
  Represents a connection to a ClickHouse database.
  """
  
  def __init__(self, host: str, port: int, database: str):
    """
    Initializes a Database object with the given connection parameters.
    """
    common.set_setting('autogenerate_session_id', False)
    self.client = clickhouse_connect.get_client(host=host, port=port, database=database)

  def query(self, query_string: str, parameters: dict = None):
    """
    Executes a query on the database.
    """
    return self.client.query(query_string, parameters=parameters)
