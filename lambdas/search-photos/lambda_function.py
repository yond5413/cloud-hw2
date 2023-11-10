import json
import ast 
import os
import boto3
import urllib.parse
from requests_aws4auth import AWS4Auth
#from opensearchpy import Opensearch, RequestsHttpConnection
#from elasticsearch import Elasticsearch, RequestsHttpConnection
#import base64
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import base64
REGION = 'us-east-1'
HOST = 'search-photos-escniwfsrfppledgjhg4fvk37e.aos.us-east-1.on.aws'
INDEX = 'photos'
SERVICE='es'
#### checking to see if pipeline works 
# from local to git
client = boto3.client('lexv2-runtime')

def lambda_handler(event, context):
    # TODO implement
    print('event: ', event)
    print(event)
    
    q = event["queryStringParameters"]['q']
    print(q)
    #configure test event based off lex output?
    # right now it is basically dummy data
    #now to get the labels from lex
    response = client.post_text(
        botName='MCTHXSG0MW',
        botAlias='TSTALIASID',
        userId="user",
        inputText=q
    )
    
    print("Lex Response: ", response)
    
    #getting labels
    labels = []
    if 'slots' in response:
        slot_val = response['slots']
        for key, val in slot_val.items():
            if val is not None:
                labels.append(val)
    else:
        print("No matches for this query.")
        
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, REGION, SERVICE, session_token=credentials.token)
    if len(labels) > 0:
        #make an opensearch instance
        ### try changing to opensearch like in demo ig?
        es = Elasticsearch(
            hosts=[{'host': HOST, 'port':443}],
            http_auth=awsauth,
            use_ssl = True,
            verify_certs= True,
            connection_class = RequestsHttpConnection
        )
        
        q = ''.join(labels)
        responses = []
        for l in labels:
            if (l!=None) and (l!=''):
                search_response = es.search({"query": {"match": {'title': q}}})
                responses.append(search_response)
        print(responses)
        
        return{
            'statusCode':200,
            'body': json.dumps(opensearch_response['hits']['hits'])
        }
    else:
        return{
            'StatusCode':200,
            'body':json.dumps([])
        }
## Opensearch demo just for reference        
'''
def query(term):
    q = {'size': 5, 'query': {'multi_match': {'query': term}}}
    
    client = OpenSearch(hosts=[{
        'host': HOST,
        'port': 443
    }],
        http_auth=get_awsauth(REGION, 'es'),
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection)
    res = client.search(index=INDEX, body=q)
    print(res)
    hits = res['hits']['hits']
    results = []
    for hit in hits:
        results.append(hit['_source'])
    return results
def get_awsauth(region, service):
    cred = boto3.Session().get_credentials()
    return AWS4Auth(cred.access_key,
        cred.secret_key,
        region,
        service,
        session_token=cred.token)
'''
    