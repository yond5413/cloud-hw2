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
def lambda_handler(event, context):
    ## specified format of 'JSON for Opensearch'
    '''
        {
            “objectKey”: “my-photo.jpg”,
                “bucket”: “my-photo-bucket”,
                “createdTimestamp”: “2018-11-05T12:40:02”,
                “labels”: [
                “person”,
                “dog”,
                “ball”,
                “park”
            ]
        }

    '''
    s3_name =""
    obj = ''
    for record in event['Records']:
        s3_name = record['s3']['bucket']['name']
        obj = record['s3']['object']['key']
        time = record["eventTime"]
        #response = s3.head_object(Bucket=bucket, Key=key)
        print(f"buck: {s3_name}, key: {obj}, time: {time}")
    s3 = boto3.client('s3')
    response = s3.head_object(Bucket=s3_name, Key=obj)
    custom_labels = response.get('ResponseMetadata', {}).get('x-amz-meta-customlabels')
    #print(f"labels: {custom_labels}")
    #print(response.get('ResponseMetadata', {}).get('HTTPHeaders'))
    #print(response.get('ResponseMetadata', {}).get('HTTPHeaders').get('x-amz-meta-customlabels'))
    #print(type(response.get('ResponseMetadata', {}).get('HTTPHeaders').get('x-amz-meta-customlabels')))
    custom_labels = response.get('ResponseMetadata', {}).get('HTTPHeaders').get('x-amz-meta-customlabels')
    content_type = response.get('ResponseMetadata', {}).get('HTTPHeaders').get('content-type')
    rek_labels = rekognition_labels(bucket_name = s3_name,object_name = obj,content = content_type)
    pic_info = {}
    pic_info["objectKey"] = obj
    pic_info["Bucket"] = s3_name
    pic_info["createdTimestamp"] = time
    cus_list = my_list = ''.join(custom_labels.split()).split(',')#custom_labels.split(',')
    #print(cus_list)
    pic_info['labels'] =  rek_labels+cus_list#label_logic(rek_labels,custom_labels)#list(set(custom_labels+rek_labels))
    # , ,, ", *, \, <, |, ,, >, /, and ?. not valud for elastic-search index
    ret = str(pic_info)
    index(pic_info)
    return {
        'statusCode': 200,
        'body': json.dumps(ret)
    }
####### change to insert
def index(term):
    #q = {'size': 5, 'query': {'multi_match': {'query': term}}}
    client = OpenSearch(hosts=[{
        'host': HOST,
        'port': 443
    }],
        http_auth=get_awsauth(REGION, 'es'),
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection)
    ####index json based on each label in the term ->
    #print(term)
    labels = term['labels']
    #print(f"labels: {labels},type: {type(labels)}")
    # Note -> all indexes must be lower case
    for lab in labels:
        res = client.index(index=lab.lower(), body=term)
        #client.index(index=INDEX, body=q)
        #print(res)
    return res
#############################################
def get_awsauth(region, service):
    cred = boto3.Session().get_credentials()
    return AWS4Auth(cred.access_key,
        cred.secret_key,
        region,
        service,
        session_token=cred.token)
#############################################
##################H#######################
######### aws-rekognition-portion####
def rekognition_labels(bucket_name ,object_name,content = ""):
# official documentation below made some edtis as we are only interested in labels tbh
###https://docs.aws.amazon.com/rekognition/latest/dg/labels-detect-labels-image.html
# security info->
#https://docs.aws.amazon.com/rekognition/latest/dg/security_iam_id-based-policy-examples.html
    rekognition = boto3.client('rekognition')
    # Specify the S3 bucket and object (image) name
    # Call the detect_labels operation
    if content !="text/base64":
        response = rekognition.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': object_name
                }
            },
            MaxLabels=10,  # Number of labels to return (adjust as needed)
            MinConfidence=70  # Confidence threshold (adjust as needed)
        )
    else:
        s3 = boto3.client('s3')
        s3_rep = s3.get_object(Bucket=bucket_name, Key=object_name)
        #print(s3_rep)
        #print(s3_rep.keys())
        #print(s3_rep['Metadata'])
        base64_data = s3_rep['Body'].read()
        #print(base64_data)
        #print(f"type of bucket stuff: {type(base64_data)}")
        #image_data = base64.decodebytes(base64_data)#base64.b64decode(base64_data)
        #image_data = base64.b64decode(base64_data)
        #print(image_data)
        #print(type(image_data))
        print(f"bucket data: {base64_data}")
        str_data = base64_data.decode('utf-8')
        json_data = json.loads(str_data)
        file_data = json_data['file']
        print(f'file_data type-> {type(file_data)}')
        image_data = file_data.encode('utf-8')
        print(f'image datat type->{type(image_data)}')
        image_data = base64.b64decode(image_data)
        print(f'latest image datat type->{type(image_data)}')
        print(image_data)
        response = rekognition.detect_labels(
            Image={
                "Bytes": image_data#base64_data#image_data#base64_data#image_data
            },
            MaxLabels=10,  # Number of labels to return (adjust as needed)
            MinConfidence=70  # Confidence threshold (adjust as needed)
        )
    # Extract and print detected labels
    detected_labels = response['Labels']
    ret = []
    for label in detected_labels:
        ret.append(label['Name'])
    return ret