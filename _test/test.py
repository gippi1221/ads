import aiohttp
import aiofiles
import asyncio
from datetime import datetime, timedelta
import random

url = 'http://88.99.188.179:8000/event/'

async def generate_random_date():
    start_date = datetime(datetime.now().year, 1, 1)
    end_date = datetime(datetime.now().year, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    return (start_date + timedelta(days=random_days)).isoformat()

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

async def write_log(filename, content):
    async with aiofiles.open(filename, 'a') as f:
        await f.write(content + '\n')

async def send_requests(session, url, data, log_filename):
    start_time = datetime.now()
    async with session.post(url, json=data) as response:
        end_time = datetime.now()
        response_time = end_time - start_time
        log_message = f"Request: {data['id']}, Status Code: {response.status}, Response Time: {response_time}"
        await write_log(log_filename, log_message)

async def main():
    for _ in range(1000):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for _ in range(1000):
                data = await generate_random_data()
                task = asyncio.create_task(send_requests(session, url, data, 'request_log.txt'))
                tasks.append(task)
            await asyncio.gather(*tasks)

asyncio.run(main())
