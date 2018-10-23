#!/usr/bin/python
import boto3
import botocore

def dynamo_scan(tableName):
    client = boto3.client('dynamodb')
    print "Running initial data pull"
    try: 
        response = client.scan(
             TableName=tableName,
             Limit=1
        )
        itemName = response['Items'][0]
    except:
        raise
    dynamo_put(itemName)
    print "working through individual keys"
    while 'LastEvaluatedKey' in response:
        print('.'),
        try: 
            response = client.scan(
                 TableName=tableName,
                 Limit=1,
                 ExclusiveStartKey=response['LastEvaluatedKey']
            )
            itemName = response['Items'][0]
        except IndexError:
            print "\nThat was the last key! Should be recovered"
            break
        except:
            raise
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

