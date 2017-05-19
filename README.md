# Data-Engineering-walmart-API-and-api-layer.net-
Setting up a pipeline on Amazon Web Services to combine two api's and carry out analysis on the data obtained.
## Motivation
To build an end-to-end data engineering system that would use live streaming data and produce meaningful results on the same.

## Approach 
- Establish a clear architecture for the end-to-end system as shown in the png file
- Make use of API calls to access the live streaming data. In this case we make use of two data sources one from the Walmart Open API and the other from apilayer.net which has the currency exchange rates.
- Store all the data in s3 using the Amazon Kinesis Firehose and use boto to stream the data
- Next,we initialise our EMR on amazon to set up a Spark Cluster. After doing so we can use the spark Context or the Spark      Session to access the data that has been stored on s3.
- Then we make use of Spark dataframes , Spark Sequel ,pandas to process the data from s3 and obtain only the relavant information that is required.
- We would also carry out all the lazy Spark transformations that is necessary to obtain only the required information on the dataset
- Usage of two different approaches to show the results of our pipeline , the first being Flask and the second being Spyre both being web development frameworks.
- To display results through the Flask app , we add our required data in JSON format into mongoDB , a no SQL datastructure. We make use of pymongo to do so and then print the results out of mongoDB using the flask app again using pymongo.
- To display results through Spyre , we do all our processing using spark transformations and spark dataframes to output a final pandas dataframe. This dataframe can then be used to plot our data using the Spyre web development framework.The results from both the front-ends has been shown in the .png files.

## Architecture
- The architecture is as shown in the WALMART-Architecture.jpg. To summarize the architecture we have two live streaming API's that are streamed into s3 using the amazon kinesis firehose and the boto3 client. We use the spark context and the spark session to get the data from S3. From here we have two front ends setup , the first one is the flask App wherein we put the data in a NOSQL dataframe , mongoDB then using the flask app and pymongo we print the necessary data on the flask webpage. The second one is SPYRE wherein we use spark datafreame operations to get a table of only the required data and then we carry out visualisations on the same.This has been explained more in detail , further down in this file.

## Scalability and Latency 
- The data is highly scalable with the use of S3 , spark , AWS as a whole . By setting up the clusters the processing does not take a lot time. Data being updated everyday does not necessarily have a lot of volume. The system also requires minimal maintenance.

## Robustness and Fault Tolerance
- The whole system was fairly robust although there were issues at times with the EMR pipe beaking. The whole process of setting up the cluster and installing the dependencies everytime was not viable. json.loads() did throw a value error at times while loading the data from S3 , we made a workaround by putting the statement in a try and except clause where except just made a pass.

## currency_firehose.py
- This script is used to get the data using the currency api and then to put it into Amazon s3 using the amazon kinesis firehose with boto3 as the client.A timestamp is also added as the data is updated once every day.We use the put_record method to add the data to s3 using the boto client through the kinesis firehose. The data is of the json format and has the currency exchange rates with respect to us dollars for a select few countries.

## wal_trending.py and walvod.py
- These scripts are used to get the top trending items and the top item for each day respectively. The obtained data is then added to kinesis firehose similar to how the currency data was added using the boto3 client. A timestamp is added as well as the data is updated once everyday.
- The scripts add data to three different buckets in order to easily differentiate between them.

## The data_enginnering.ipynb notebook
- The entire architecture was set up on a Spark EMR cluster , the notebook was set up on this EMR similarly , the notebook has code that was tried and tested before making them into python scripts. The notebook has explanations for the blocks of code that were put together.It also contans code where the data has been put into mongoDB.

## mongo_flask.py
- The code to set up the front end , The Flask App. We use pymongo the mongoclient to get data from mongoDB(A no SQL database).The flask app has been setup on the EMR as well , we specify the host to be 0.0.0.0 to make the app accessible from the EMR.We have to specify our end point for the EMR as well while using the IP address.After running the script , we enter the URL on a new tab to find the top 25 items displayed over the course of a week through the FLASK app.A screenshot of what was displayed through the flask app can be seen in the flask_app.png

## discount.py and spyre_vis.py
- These two scripts are used to create visualisations of the data through the SPARK dataframes that were created. The front end used in this case is SPYRE. The tables that have the discount rates included for each of the items and a graph depicting the same can be seen in DISCOUNT.png and the DISCOUNT GRAPH.png. The line in red indiactes the discount rates , we were trying to see if higher discount rates made customers buy a project at walmart.
- The spyre_vis.py has the visualisations for prices in various currencies across the world taking into account the exchange rate for that particular day. The prices are for the bestselling item on that given day. Some currencies had a higher value and hence the graph did not come out perfectly.The screenshot for the graphs and the visualisations can be found in the CUURENCY TABLES.png and the popular graph.png.
