import boto3
source_ddb = boto3.resource('dynamodb', 'us-east-1')
dest_ddb = boto3.client('dynamodb', 'us-west-2')

def sync(source_ddb, dest_ddb):
    table = source_ddb.Table("<FMI1>")
    scan_kwargs = {
        'ProjectionExpression': "Key1, Key2"
    }
    done = False
    start_key = None
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)
        for item in response['Items']:
            newItem = { 'Key1': {}, 'Key2': {} }
            newItem['Key1']['S'] = item['Key1']
            newItem['Key2']['S'] = item['Key2']
            dest_ddb.put_item(TableName="<FMI2>", Item=newItem)
            print(item)
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None


sync(source_ddb, dest_ddb)