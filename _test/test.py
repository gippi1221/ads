import requests
from datetime import datetime, timedelta
import random

url = 'http://localhost:8000/event/'

def generate_random_date():
    start_date = datetime(datetime.now().year, 1, 1)
    end_date = datetime(datetime.now().year, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    return (start_date + timedelta(days=random_days)).isoformat()

def generate_random_data():
    return {
        "id": random.randint(1, 1000),
        "event_date": generate_random_date(),
        "metric1": random.randint(100000, 999999),
        "metric2": round(random.uniform(0.1, 10.0), 2),
        "attribute1": random.choice([111, 222, 333, 444, 555, 666, 777, 888, 999, 1111, 2222, 3333, 4444, 5555, 6666, 7777, 8888, 9999]),
        "attribute2": random.choice([111, 222, 333, 444, 555, 666, 777, 888, 999, 1111, 2222, 3333, 4444, 5555, 6666, 7777, 8888, 9999]),
        "attribute3": random.choice([111, 222, 333, 444, 555, 666, 777, 888, 999, 1111, 2222, 3333, 4444, 5555, 6666, 7777, 8888, 9999]),
        "attribute4": random.choice(['aaa', 'sss', 'ddd', 'fff', 'ggg', 'hhh', 'jjj', 'kkk', 'qqq', 'www', 'eee', 'rrr', 'ttt', 'yyy', 'uuu', 'zzz', 'xxx', 'ccc']),
        "attribute5": random.choice(['111', '222', '333', '444', '555', '666', '777', '888', '999', '1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888', '9999']),
        "attribute6": random.choice([True, False])
    }

def write_log(filename, content):
    with open(filename, 'a') as f:
        f.write(content + '\n')

log_buffer = []
log_filename = 'request_log.txt'
for i in range(100000):
    start_time = datetime.now()
    data = generate_random_data()
    response = requests.post(url, json=data)
    end_time = datetime.now()
    if response.status_code == 200:
        log_message = f"Request {i+1}: Successful, Response Time: {end_time - start_time}"
    else:
        log_message = f"Request {i+1}: Failed with status code {response.status_code}, Response Time: {end_time - start_time}"
    log_buffer.append(log_message)
    
    if len(log_buffer) >= 1000:
        print(len(log_buffer))
        write_log(log_filename, '\n'.join(log_buffer))
        log_buffer = []

if log_buffer:
    write_log(log_filename, '\n'.join(log_buffer))
