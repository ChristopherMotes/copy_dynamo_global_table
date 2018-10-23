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
    # This section deletes the aws global table atrributes if they exist
    DeleteAttributeList = [ "aws:rep:deleting", "aws:rep:updatetime", "aws:rep:updateregion" ]
    for attribute in DeleteAttributeList:
        if attribute in itemName:
            del itemName[attribute]
        
    # Now start copying data to the newdb
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

