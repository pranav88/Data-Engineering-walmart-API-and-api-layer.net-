import os
import json
import requests
import datetime
import yaml
import boto3

def main(boto_client,cur_price):
	trending_dump = json.dumps(trending) + '\n'
	client.put_record(DeliveryStreamName='waltrend', Record={'Data': trending_dump})



if __name__ == '__main__':
	trends = requests.get("http://api.walmartlabs.com/v1/trends?format=json&apiKey=23tqstpv2srkvf6jvc44td74")
	trending = json.loads(trends.content.decode('utf-8'))
	trending['timestamp'] = '{:%Y-%b-%d}'.format(datetime.datetime.now())
	client = boto3.client('firehose', region_name='us-east-1')
	main(client,trending)