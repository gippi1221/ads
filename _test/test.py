import aiohttp
import aiofiles
import asyncio
from datetime import datetime, timedelta
import random

url = 'http://88.99.188.179:8088/event/'

async def generate_random_date():
    start_date = datetime(datetime.now().year, 2, 1)
    end_date = datetime(datetime.now().year, 2, 8)
    random_days = random.randint(0, (end_date - start_date).days)
    random_hours = random.randint(0, 23)
    random_minutes = random.randint(0, 59)
    random_seconds = random.randint(0, 59)
    random_date = start_date + timedelta(days=random_days, hours=random_hours, minutes=random_minutes, seconds=random_seconds)
    return random_date.isoformat()

async def generate_random_data():
    return {
        "id": random.randint(1, 1000),
        "event_date": await generate_random_date(),
        "metric1": random.randint(100000, 999999),
        "metric2": round(random.uniform(0.1, 10.0), 2),
        "attribute1": random.choice([111, 222, 333, 444, 555, 666, 777, 888, 999, 1111, 2222, 3333, 4444, 5555, 6666, 7777, 8888, 9999]),
        "attribute2": random.choice([111, 222, 333, 444, 555, 666, 777, 888, 999, 1111, 2222, 3333, 4444, 5555, 6666, 7777, 8888, 9999]),
        "attribute3": random.choice([111, 222, 333, 444, 555, 666, 777, 888, 999, 1111, 2222, 3333, 4444, 5555, 6666, 7777, 8888, 9999]),
        "attribute4": random.choice(['aaa', 'sss', 'ddd', 'fff', 'ggg', 'hhh', 'jjj', 'kkk', 'qqq', 'www', 'eee', 'rrr', 'ttt', 'yyy', 'uuu', 'zzz', 'xxx', 'ccc']),
        "attribute5": random.choice(['111', '222', '333', '444', '555', '666', '777', '888', '999', '1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888', '9999']),
        "attribute6": random.choice([True, False])
    }

async def send_requests(session, url, data, retries=3):
    for _ in range(retries):
        try:
            response = await session.post(url, json=data)
            await response.release()
            return
        except aiohttp.ClientConnectorError as e:
            print(f"Connection failed. Retrying... ({e})")

async def main():
    for _ in range(1000):
        print(_)
        tasks = []
        async with aiohttp.ClientSession() as session:
            for _ in range(30):
                data = await generate_random_data()
                task = asyncio.create_task(send_requests(session, url, data))
                tasks.append(task)
            await asyncio.gather(*tasks)

asyncio.run(main())
