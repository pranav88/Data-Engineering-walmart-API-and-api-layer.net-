import os
import json
import requests
import datetime
import yaml
import boto3

def main(boto_client,cur_price):
	cur_dump = json.dumps(cur_price) + '\n'
	client.put_record(DeliveryStreamName='walmart', Record={'Data': cur_dump})



if __name__ == '__main__':
	currencylive = requests.get("http://apilayer.net/api/live?access_key=b13523155060ced40adabafd03e6edf8&currencies=AUD,EUR,GBP,INR,AED,JPY,CHF,ZAR,CNY,CAD")
	cur_price = json.loads(currencylive.content.decode('utf-8'))
	cur_price['timestamp'] = '{:%Y-%b-%d}'.format(datetime.datetime.now())
	client = boto3.client('firehose', region_name='us-east-1')
	main(client,cur_price)
