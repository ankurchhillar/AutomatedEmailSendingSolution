import json
import boto3
import csv
import io

s3Client = boto3.client('s3')
sesClient = boto3.client('ses')

def lambda_handler(event, context):
    #Bucket and File Name
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    print(bucket)
    print(key)

    #Get Our Object
    response = s3Client.get_object(Bucket=bucket,Key=key)

    #Get Object Content
    data = response['Body'].read().decode('utf-8')
    reader = csv.reader(io.StringIO(data))
    next(reader)
    for row in reader:
        print(str.format("Name:- {}, Email:- {} ",row[0],row[1]))

    #SendEmail
    emailAddress = "ankurchhillar001@gmail.com"
    emailResponse = sesClient.send_email(
        Destination = {
            "ToAddresses": [
                row[1]
            ],
        },
        Message = {
            "Body": {
                "Text": {
                    "Data": "Hello, " + row[0] + " Welcome to AWS!"
                }
            },
            "Subject": {
                "Data": "Ankur Welcomes You to AWS"
            }
        },
        Source = emailAddress
    )
