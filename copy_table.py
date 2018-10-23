#!/usr/bin/python3.6
import boto3
import botocore
import argparse
import sys

def dynamo_scan(restoreTableName, destinationTableName):
    client = boto3.client('dynamodb')
    print("Running initial data pull")
    try: 
        response = client.scan(
             TableName=restoreTableName,
             Limit=1
        )
        itemName = response['Items'][0]
    except:
        raise
    dynamo_put(itemName, destinationTableName)
    print("working through individual keys")
    while 'LastEvaluatedKey' in response:
        try: 
            # this print creates screen action
            #print(".", end=" ")
            sys.stdout.write('.')
            response = client.scan(
                 TableName=restoreTableName,
                 Limit=1,
                 ExclusiveStartKey=response['LastEvaluatedKey']
            )
            itemName = response['Items'][0]
        except IndexError:
            print("\nThat was the last key! Should be recovered")
            break
        except:
            raise
        dynamo_put(itemName, destinationTableName)

def dynamo_put(itemName, destinationTableName):
    # This section deletes the aws global table atrributes if they exist
    DeleteAttributeList = [ "aws:rep:deleting", "aws:rep:updatetime", "aws:rep:updateregion" ]
    for attribute in DeleteAttributeList:
        if attribute in itemName:
            del itemName[attribute]
        
    # Now start copying data to the newdb
    client = boto3.client('dynamodb') 
    try:                              
        response = client.put_item(       
            TableName=destinationTableName,
            Item=itemName
        )                             
    except:                           
        raise                         

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--restoretable", help="The source table to restore from", required=True)
    parser.add_argument("-d", "--destinationtable", help="The desination to restore to", required=True)
    args = parser.parse_args()
    dynamo_scan(args.restoretable, args.destinationtable)

