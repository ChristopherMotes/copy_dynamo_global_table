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
        itemName = response['Items'][0]
    except:
        raise
    print response['LastEvaluatedKey']
#    dynamo_put(itemName)
    while 'LastEvaluatedKey' in response:
        print "in loop"
        try: 
            response = client.scan(
                 TableName=tableName,
                 Limit=1,
                 ExclusiveStartKey=response['LastEvaluatedKey']
            )
#            itemName = response['Items'][0]
        except:
            raise

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

