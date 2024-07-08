import json
import boto3
import base64
from datetime import datetime

# Initialize S3 client
s3 = boto3.client('s3')

# Define the S3 bucket name
S3_BUCKET = 'your-bucket-name'

def lambda_handler(event, context):
    # Initialize variables to track transactions and statistics
    total_transaction_amount = 0
    total_transactions = 0
    transactions_per_customer = {}
    suspicious_transactions = []

    # Process each record from the batch
    for record in event['Records']:
        # Decode and parse the record
        payload = base64.b64decode(record['kinesis']['data'])
        transaction = json.loads(payload)

        customer_id = transaction['customer_id']
        amount = transaction['amount']
        timestamp = transaction['timestamp']

        # Detect and flag suspicious transactions
        if amount > 1000:  # Example condition for suspicious transaction
            suspicious_transactions.append(transaction)

        # Update statistics
        total_transaction_amount += amount
        total_transactions += 1

        if customer_id not in transactions_per_customer:
            transactions_per_customer[customer_id] = 0
        transactions_per_customer[customer_id] += 1

    # Calculate average transaction amount
    average_transaction_amount = total_transaction_amount / total_transactions if total_transactions else 0

    # Prepare data to write to S3
    result = {
        'average_transaction_amount': average_transaction_amount,
        'total_transactions': total_transactions,
        'transactions_per_customer': transactions_per_customer,
        'suspicious_transactions': suspicious_transactions,
        'processed_time': datetime.utcnow().isoformat()
    }

    # Generate S3 object key with timestamp
    s3_key = f'transactions/processed_data_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.json'

    # Write data to S3
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=s3_key,
        Body=json.dumps(result),
        ContentType='application/json'
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Data processed and stored in S3 successfully!')
    }
