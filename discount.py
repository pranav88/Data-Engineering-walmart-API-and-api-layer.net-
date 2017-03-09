

from spyre import server
from pyspark.sql import SparkSession
import pandas as pd
from pyspark.sql.functions import explode
import json

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()



class walmart(server.App):
    title = "Discounts"

    inputs = [{     "type":'dropdown',
                    "label": 'discount percentage for items', 
                    "options" : [ {"label": "rates", "value":"discounts"}
                                  ],
                    "key": 'ticker', 
                    "action_id": "update_data"}]

    controls = [{   "type" : "hidden",
                    "id" : "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [{ "type" : "plot",
                    "id" : "plot",
                    "control_id" : "update_data",
                    "tab" : "Plot"},
                { "type" : "table",
                    "id" : "table_id",
                    "control_id" : "update_data",
                    "tab" : "Table",
                    "on_page_load" : True }]

    def getData(self, params):
        ticker = params['ticker']
        trend_items = spark.read.json("s3://waltrend/2017/03/*/*/*/")
        trend_df = trend_items.select(explode(trend_items['items.name'])) 
        df1 = trend_items.select(explode(trend_items['items.msrp']))
        df2 = trend_items.select(explode(trend_items['items.salePrice']))
        df3 = trend_items.select(explode(trend_items['items.customerRating']))
        cost_df = trend_df.toPandas()
        cost_df['msrp'] = df1.toPandas()
        cost_df['salePrice'] = df2.toPandas()
        cost_df['customerRating'] = df3.toPandas()
        cost_df = cost_df.dropna()
        cost_df['discount'] = ((cost_df['msrp'] -  cost_df['salePrice'])/cost_df['msrp'])*100
        return cost_df

    def getPlot(self, params):
        df = self.getData(params)
        plt_obj = df.plot()
        plt_obj.set_ylabel("Price")
        plt_obj.set_title("discount percentage")
        fig = plt_obj.get_figure()
        return fig

app = walmart()
app.launch(host='0.0.0.0',port=5000)