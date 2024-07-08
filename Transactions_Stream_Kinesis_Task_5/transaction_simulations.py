import boto3
import random
import json
import time

stream_name = 'your-stream-name'
transaction_id = 1

# Initialize the Kinesis client
kinesis_client = boto3.client('kinesis', region_name='us-east-1')

def get_random_transaction():
    transaction = {
        'transaction_id': str(transaction_id),
        'customer_id': random.randint(1, 50),
        'amount': round(random.uniform(1.0, 1200.0), 2),
        'timestamp': time.time()
    }
    return transaction

records = []

def put_record(stream_name, data):
    global records
    records.append(data)

    if len(records) > 50:
        kinesis_client.put_records(
            Records=[{'Data': json.dumps(record), 'PartitionKey': str(record['customer_id'])} for record in records],
            StreamName=stream_name
        )
        print("Transactions processed")
        records = []


# Simulate sending transactions to the stream
end_time = time.time() + 60
while time.time() < end_time:
    transaction = get_random_transaction()
    put_record(stream_name, transaction)
    print(f"Queued transaction: {transaction}")
    transaction_id += 1
    time.sleep(0.1)

# Put remaining transactions
kinesis_client.put_records(
    Records=[{'Data': json.dumps(record), 'PartitionKey': str(record['customer_id'])} for record in records],
    StreamName=stream_name)
print("Remaining Transactions processed")