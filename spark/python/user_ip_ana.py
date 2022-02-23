import sys
from random import random
from operator import add
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json, window, date_format
from pyspark.sql.types import BinaryType, StructType, StringType, IntegerType, StructField, Row, TimestampType
from pyspark.sql.functions import from_json
import json
import requests

FUNCTION_MAP = {
    "textlist": "文章列表",
    "freqdist": "聲量趨勢",
    "datadist": "資料分佈 - 資料分佈",
    "datasource": "資料分佈 - 資料來源",
    "hotchnl": "熱門頻道",
    "sndist": "社群活躍度",
    "opleader": "意見領袖",
    "hotrank": "熱門排行榜",
    "hotkw": "熱門關鍵字",
    "maintext": "即時大數據",
    "smint": "社群指數",
    "conexplr": "概念探索",
    "sprdtrnd": "傳播趨勢",
    "cadatadist": "競品比較-資料分佈",
    "casentidist": "競品比較-網路好感度",
    "casndist": "CASNDist",
    "cafreqcorr": "競品比較-趨勢相關",
    "kwstorm": "關鍵字風暴",
    "sentidist": "網路好感度"
}

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("tts") \
        .getOrCreate()

    lines = spark \
        .read \
        .format("kafka") \
        .option("kafka.bootstrap.servers", '34.80.54.94:9094') \
        .option("subscribe", 'keypo-log') \
        .option("failOnDataLoss", "false") \
        .option("startingOffsets", "earliest") \
        .load() \
        .selectExpr("CAST(value AS STRING) as json")

    # define json schema
    schema = StructType([
        StructField("LOG_TIME", TimestampType(), True),
        StructField("USERNAME", StringType(), True),
        StructField("IP", StringType(), True),
        StructField("API_METHOD", StringType(), True),
        StructField("ACTION", StringType(), True),
        StructField("VERSION", StringType(), True),
        StructField("AGENT", StringType(), True),
        StructField("PARAMS", StructType([
            StructField("realname", StringType(), True),
            StructField("username", StringType(), True)
        ]), True),
        StructField("RESPONSE_CODE", IntegerType(), True),
        StructField("RESPONSE_TEXT", StringType(), True),
    ])


    def api_format(x):
        return FUNCTION_MAP.get(x, x)


    api_format_udf = udf(
        lambda z: api_format(z),
        StringType()
    )

    fun = lines.select(from_json("json", schema).alias("jsonp")).select("jsonp.*")
    fun = fun.where("LOG_TIME BETWEEN '2019-11-07' AND '2019-11-08'")

    fun = fun.groupBy(
        'IP'
        'USERNAME',
        'PARAMS.realname',
    ).count()
    fun = fun.groupBy(
        'USERNAME',
        'realname',
    ).count().sort('count')
    fun = fun.select(
        'USERNAME',
        'realname',
        'count'
    )
    fun \
        .coalesce(1) \
        .write.format("com.databricks.spark.csv") \
        .option("header", "true") \
        .save("user_ip_ana.csv")
