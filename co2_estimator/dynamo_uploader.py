import boto3
import json

def upload_to_dynamodb(report_dict, table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    table.put_item(Item=report_dict)
