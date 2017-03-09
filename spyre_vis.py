
from spyre import server
from pyspark.sql import SparkSession
import pandas as pd
import json

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()



class walmoney(server.App):
    title = "Valued items and their currency rates"

    inputs = [{     "type":'dropdown',
                    "label": 'Bestselling items and their Currency rates', 
                    "options" : [ {"label": "rates", "value":"valued items"}
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
        currency = spark.read.json("s3://walcurrency/2017/03/*/*/*/")
        currency_df = currency.select(currency['timestamp'],currency['quotes.USDAED'],currency['quotes.USDAUD'],currency['quotes.USDCAD'],currency['quotes.USDCHF'],currency['quotes.USDCNY'],currency['quotes.USDEUR'],currency['quotes.USDGBP'],currency['quotes.USDINR'],currency['quotes.USDJPY'],currency['quotes.USDZAR'])
        currency_pandas = currency_df.toPandas()
        vod = spark.read.json("s3://walvod/2017/03/*/*/*/")
        vod_df = vod.select(vod['timestamp'],vod['name'],vod['salePrice'])
        vod_pandas = vod_df.toPandas()
        item_rates = currency_pandas.set_index('timestamp').join(vod_pandas.set_index('timestamp'))
        item_rates_final = pd.DataFrame(item_rates['name'])
        item_rates_final['value_INR'] =  item_rates['USDINR'] * item_rates['salePrice']
        item_rates_final['value_EUR'] =  item_rates['USDEUR'] * item_rates['salePrice']
        item_rates_final['value_GBP'] =  item_rates['USDGBP'] * item_rates['salePrice']
        item_rates_final['value_JPY'] =  item_rates['USDJPY'] * item_rates['salePrice']
        item_rates_final['value_USD'] =  item_rates['salePrice'] 
        return item_rates_final

    def getPlot(self, params):
        df = self.getData(params)
        plt_obj = df.plot()
        plt_obj.set_ylabel("Price")
        plt_obj.set_title("currency rates")
        fig = plt_obj.get_figure()
        return fig

app = walmoney()
app.launch(host='0.0.0.0',port=5000)