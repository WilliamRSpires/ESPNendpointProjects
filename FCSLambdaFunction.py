import json
import requests
import boto3
from bs4 import BeautifulSoup
"""Creating an S3 client"""
s3_client = boto3.client('s3')
bucket_name = 'alexa-project-bucket'

def lambda_handler(event, context):
    """First we pull the data from ESPN"""
    ESPN = "http://site.api.espn.com/apis/site/v2/sports/football/college-football/rankings"
    """Next we turn this data into json, making it easier to parse"""
    Rankings = requests.get(ESPN)
    NewRank = Rankings.json()
    """Defining FCSRank by indexing to where this ranking is located"""
    FCSRank = NewRank['rankings'][3]['ranks']
    """Creating a blank list and a for loop that will populate the list with the FCS ranked team in order"""
    FCSteams = [ ]
    for num in range(25):
        FCSteams.append(FCSRank[num]['team']['nickname'])
    f= open("/tmp/FCSFile.txt","w+")
    for item in FCSteams:
        f.write("%s\n" % item)
    f.close()
    s3_client.upload_file("/tmp/FCSFile.txt", bucket_name, 'fcsfile')
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
