# createTask
import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Tasks')

def lambda_handler(event, context):
    try:
        
        table.put_item(
            Item={
                'taskID': event['taskId'],
                'taskName': event['taskName'],
                'taskDescription': event['taskDescription']
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Task created successfully!')
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
    
# updateTask
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Tasks')

def lambda_handler(event, context):
    try:
        task_id = event['pathParameters']['taskID']
        body = json.loads(event['body'])
        
        update_expression = "SET "
        expression_attribute_values = {}
        if 'taskName' in body:
            update_expression += "taskName = :taskName, "
            expression_attribute_values[':taskName'] = body['taskName']
        if 'taskDescription' in body:
            update_expression += "taskDescription = :taskDescription, "
            expression_attribute_values[':taskDescription'] = body['taskDescription']
        
        # Remove the trailing comma and space
        update_expression = update_expression.rstrip(', ')
        
        response = table.update_item(
            Key={
                'taskID': task_id
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Task updated successfully!')
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }

# deleteTask
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Tasks')

def lambda_handler(event, context):
    try:
        task_id = event['pathParameters']['taskID']
        
        response = table.delete_item(
            Key={
                'taskID': task_id
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Task deleted successfully!')
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }


# getTasks
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Tasks')

def lambda_handler(event, context):
    try:
        # Example: Fetch all items from DynamoDB table
        response = table.scan()
        tasks = response.get('Items', [])

        # Prepare tasks as JSON response
        return {
            'statusCode': 200,
            'body': json.dumps(tasks)
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
