#!/usr/bin/python
import boto3
import botocore
import json

def dynamo_scan(tableName):
    client = boto3.client('dynamodb')
    try: 
        response = client.scan(
             TableName=tableName,
             Limit=1
        )
    except:
        raise
    print response['Items']

if __name__ == "__main__":
    dynamo_scan("test0-recovery")

