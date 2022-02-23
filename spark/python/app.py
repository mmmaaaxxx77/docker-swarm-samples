import sys
from random import random
from operator import add
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json
from pyspark.sql.types import BinaryType, StructType, StringType, IntegerType, StructField, Row
from pyspark.sql.functions import from_json
import json
import requests


class DF:
    import requests
    def __init__(self):
        print("--- init ---")

    def printt2(x):
        import requests
        print(f"-------------------{x['msg']}-----------------------")
        r = requests.get('http://jsonip.com')
        ip = r.json()['ip']
        print(f"{ip}")
        print(f"{sys.version}")
        return x


if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("tts") \
        .getOrCreate()

    lines = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", '104.199.243.52:9094') \
        .option("subscribe", 'topic') \
        .option("failOnDataLoss", "false") \
        .option("startingOffsets", "earliest") \
        .load() \
        .selectExpr("CAST(value AS STRING) as json")

    # define json schema
    schema = StructType([StructField("number", StringType(), True),
                         StructField("msg", StringType(), True),
                         StructField("fdg", StringType(), True)])


    # custom function
    def printt(x):
        print(f"-------------------{x['number']}-----------------------")
        # if x == "1":
        #     return x
        dic = x.asDict()
        dic['fdg'] = 1
        return Row(**dic)


    def printt2(x):
        import requests
        print(f"-------------------{x['msg']}-----------------------")
        # if x == "1":
        #     return x
        r = requests.get('http://jsonip.com')
        ip = r.json()['ip']
        print(f"{ip}")
        print(f"{sys.version}")
        return x


    # define a custom function and return type
    print_udf = udf(
        lambda z: printt(z),
        schema
    )
    print_udf2 = udf(
        DF.printt2,
        schema
    )

    fun = lines.select(from_json("json", schema).alias("jsonp"))  # .select("jsonp.*")
    fun = fun.select(print_udf('jsonp').alias("cus")).dropna()
    fun = fun.select(print_udf2('cus').alias("cus2")).dropna().select("cus2.*")
    query = fun \
        .writeStream \
        .outputMode('update') \
        .format('console') \
        .trigger(continuous="5 second") \
        .start()

    query.awaitTermination()
