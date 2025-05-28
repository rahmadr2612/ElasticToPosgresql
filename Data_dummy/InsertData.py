import requests
import json
from faker import Faker

fake = Faker()
es_url = 'http://localhost:9200/products/_bulk'
batch_size = 1000
total_records = 1_000_000

def generate_bulk_data(start_id, batch_size):
    bulk_lines = []
    for i in range(start_id, start_id + batch_size):
        # Metadata action untuk bulk insert
        action = {"index": {"_index": "products", "_id": str(i)}}
        bulk_lines.append(json.dumps(action))
        
        # Data dummy
        data = {
            "id": i,
            "name": fake.word().title(),
            "category": fake.word(),
            "price": round(fake.random_number(digits=5) / 100, 2),
            "created_at": fake.iso8601()
        }
        bulk_lines.append(json.dumps(data))
    return "\n".join(bulk_lines) + "\n"

def main():
    for start_id in range(1, total_records + 1, batch_size):
        bulk_data = generate_bulk_data(start_id, batch_size)
        headers = {'Content-Type': 'application/x-ndjson'}
        response = requests.post(es_url, headers=headers, data=bulk_data)
        
        if response.status_code == 200:
            print(f"Inserted records {start_id} to {start_id + batch_size - 1}")
        else:
            print(f"Failed to insert records {start_id} to {start_id + batch_size - 1}")
            print(response.text)
            break

if __name__ == "__main__":
    main()
