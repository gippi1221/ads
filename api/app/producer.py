import logging
from aiokafka import AIOKafkaProducer

logger = logging.getLogger(__name__)

class KafkaProducer:
  def __init__(self, bootstrap_servers='kafka:9092', topic='samples'):
    self.bootstrap_servers = bootstrap_servers
    self.topic = topic
    self.producer = None

  async def setup(self):
    self.producer = AIOKafkaProducer(
      bootstrap_servers=self.bootstrap_servers,
      value_serializer=lambda v: v.encode('utf-8')
    )
    await self.producer.start()

  async def close(self):
    await self.producer.stop()

  async def send_data_to_kafka(self, data):
    await self.producer.send_and_wait(self.topic, data)
