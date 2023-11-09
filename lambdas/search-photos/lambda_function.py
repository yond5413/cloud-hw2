import json
import ast 
import os
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import base64
REGION = 'us-east-1'
HOST = 'search-photos-escniwfsrfppledgjhg4fvk37e.aos.us-east-1.on.aws'
INDEX = 'photos'

client = boto3.client('lexv2-runtime')

def lambda_handler(event, context):
    # TODO implement
    print('event: ', event)
    print(event)
    
    q=event["queryStringParameters"]['q']
    print(q)
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
