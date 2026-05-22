import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('Feedback-Table')

def lambda_handler(event, context):

    http_method = 'POST'

    if 'requestContext' in event:
        http_method = event['requestContext']['http']['method']

    if http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'message': 'CORS preflight successful'
            })
        }

    body = json.loads(event['body'])

    item = {
        'id': str(uuid.uuid4()),
        'name': body['name'],
        'message': body['message']
    }

    table.put_item(Item=item)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'message': 'Feedback stored successfully!'
        })
    }
