import json
import os
import time
import boto3


def handler_result_aggregator(event, context):
    table_name = os.environ['DDB_TABLE_NAME']
    hash_key = os.environ['DDB_HASH_KEY']

    dynamo_db = boto3.resource('dynamodb')
    table = dynamo_db.Table(table_name)

    test_ids = []

    print('Event: {}'.format(str(event)))

    expiration_time = int(time.time()) + 86400

    for record in event['Records']:
        payload = json.loads(record['body'])
        print('Body: {}'.format(str(payload)))

        test_id = payload[hash_key]
        test_ids.append(test_id)

        table.put_item(
            Item={
                hash_key: test_id,
                'result': payload,
                'ttl': expiration_time
            }
        )

    response = {
        "requestId": context.aws_request_id,
        "testIds": test_ids
    }
    print(json.dumps(response))

    return response
