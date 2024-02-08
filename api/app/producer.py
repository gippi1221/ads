import logging
from aiokafka import AIOKafkaProducer

logger = logging.getLogger(__name__)

class KafkaProducer:
  """
  Represents a connection and methods to work with Kafka cluster.
  """
  def __init__(self, bootstrap_servers='kafka:9092', topic='samples'):
    """
    Initializes a Producer object with the given connection parameters.
    """
    self.bootstrap_servers = bootstrap_servers
    self.topic = topic
    self.producer = None

  async def setup(self):
    """
    This method is used to setup connection on app start
    """
    self.producer = AIOKafkaProducer(
      bootstrap_servers=self.bootstrap_servers,
      value_serializer=lambda v: v.encode('utf-8')
    )
    await self.producer.start()

  async def close(self):
    """
    This method is used to close connection on app start
    """
    await self.producer.stop()

  async def send_data_to_kafka(self, data):
    """
    This method is used to publish json message to kafka
    """
    await self.producer.send_and_wait(self.topic, data)
