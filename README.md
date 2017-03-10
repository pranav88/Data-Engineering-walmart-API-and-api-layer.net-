# Data-Engineering-walmart-API-and-api-layer.net-
Setting up a pipeline to combine two api's and analysis on the same
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

## Scalability and Latency 
- The data is highly scalable with the use of S3 , spark , AWS as a whole . By setting up the clusters the processing does not take a lot time. Data being updated everyday does not necessarily have a lot of volume. The system also requires minimal maintenance.

## Robustness and Fault Tolerance
- The whole system was fairly robust although there were issues at times with the EMR pipe beaking. The whole process of setting up the cluster and installing the dependencies everytime was not viable. json.loads() did throw a value error at times while loading the data from S3 , we made a workaround by putting the statement in a try and except clause where except just made a pass.
