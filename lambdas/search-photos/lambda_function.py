import json
import ast 
import os
import boto3
import uuid
import urllib.parse
from requests_aws4auth import AWS4Auth
#from opensearchpy import Opensearch, RequestsHttpConnection
#from elasticsearch import Elasticsearch, RequestsHttpConnection
#import base64
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import base64
import inflection

REGION = 'us-east-1'
HOST = 'search-photos-escniwfsrfppledgjhg4fvk37e.aos.us-east-1.on.aws'
INDEX = 'photos'
SERVICE='es'
#### checking to see if pipeline works 
# from local to git
client = boto3.client('lexv2-runtime')

def lambda_handler(event, context):
    # TODO implement
    print(context)
    print('event: ', event)
    print('event:', json.dumps(event))

    print(event)
    
    q = event["inputTranscript"]
    print(q)
    #configure test event based off lex output?
    # right now it is basically dummy data
    #now to get the labels from lex
    response = client.recognize_text(
        botId='MCTHXSG0MW',
        botAliasId='TSTALIASID',
        localeId='en_US',
        sessionId=str(uuid.uuid4()),

        text=q
    )
    
    print("Lex Response: ", response)
    #getting labels
    labels = []
    if 'sessionState' in response:
        print("hi")
        slot_values = response['sessionState']['intent']['slots']
    
        slot_one_value = None
        slot_two_value = None
        
        if 'slotOne' in slot_values and 'value' in slot_values['slotOne']:
            slot_one_value = slot_values['slotOne']['value']['originalValue']
            print("slot val ", slot_one_value)
            labels.append(inflection.singularize(slot_one_value))
        
        if 'slotTwo' in slot_values:
            print("ye")
            if slot_values['slotTwo'] is not None:
                slot_two_value = slot_values['slotTwo']['value']['originalValue']
                labels.append(inflection.singularize(slot_two_value))
        
    else:
        print("No matches for this query.")
    
    print(labels)
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, REGION, SERVICE, session_token=credentials.token)
    if len(labels) > 0:
        #make an opensearch instance
        ### try changing to opensearch like in demo ig?
        
        opensearch = OpenSearch(
            hosts=[{'host': HOST, 'port':443}],
            http_auth=awsauth,
            use_ssl = True,
            verify_certs= True,
            connection_class = RequestsHttpConnection
        )
        
        q = ''.join(labels)
        print(f"what are you passing into the function: {INDEX}")
        print(q)
        opensearch_response = opensearch.search(
            index = q
            #index=INDEX,
            #body={"query": {"match": {'name': q}}}
        )
        print(f'here is the opensearch_resp: {opensearch_response}')
        hits = opensearch_response['hits']['hits']
        results = []
        for hit in hits:
            results.append(hit['_source'])
        print(results)
        s3 = boto3.client('s3')
        ret = []
        print(type(results))
        print(len(results))

        for i in range(0,min(5,len(results))):
            print(results[i])
            object_name = results[i]['objectKey']
            bucket_name = results[i]['Bucket']
            s3_rep = s3.get_object(Bucket=bucket_name, Key=object_name)
            base64_data = s3_rep['Body'].read()
            str_data = base64_data.decode('utf-8')
            json_data = json.loads(str_data)
            file_data = json_data['file']
            print(f'file_data type-> {type(file_data)}')
            print(file_data[:20])
            #image_data = file_data.encode('utf-8')
            #print(f'image datat type->{type(image_data)}')
            #image_data = base64.b64decode(image_data)
            image_data = file_data
            ret.append({"file":image_data})
        #responses = []
        #for l in labels:
        #    if (l!=None) and (l!=''):
        #        search_response = es.search({"query": {"match": {'title': q}}})
        #        responses.append(search_response)
        #print(responses)
        
        return{
            'statusCode':200,
            'body': json.dumps(ret)#opensearch_response['hits']['hits'])
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
    