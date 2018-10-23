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
    itemName = response['Items'][0]
    dynamo_put(itemName)

def dynamo_put(itemName):
    client = boto3.client('dynamodb') 
    try:                              
        response = client.put_item(       
            TableName="test0",     
            Item=itemName
        )                             
    except:                           
        raise                         

if __name__ == "__main__":
    dynamo_scan("test0-recovery")

