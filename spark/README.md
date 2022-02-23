# Deploy Spark in Docker Swarm

1. Using Docker Swarm to deploy spark cluster.
2. Easily to scale out Spark node.
3. One Spark master node and Three Spark slaves in Demo Setting.
4. Spark version 2.4.4

## Start Spark Clsuter
```shell script
$ docker stack deploy -c docker-compose.yml spark
```

## Submit Spark App
```shell script
docker ps | awk '{print $NF}' | grep -w master | docker run --rm --name my-spark-app -e ENABLE_INIT_DAEMON=false --link - --net demo-net 10.140.15.238:5000/spark-app
```

## Others

```shell script
$ SPARK_HOME/bin/spark-submit --conf "spark.driver.extraJavaOptions=-Dlog4j.configuration=file:/Users/johnny/spark-2.4.4-bin-hadoop2.7/log4j.properties" --conf "spark.executor.extraJavaOptions=-Dlog4j.configuration=file:/Users/johnny/spark-2.4.4-bin-hadoop2.7/log4j.properties" --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.4 test_spark_kafka.py
```

## Run Submit 
```shell script
$ docker build --rm -t 10.140.15.238:5000/spark-app .
$ docker ps | awk '{print $NF}' | grep -w master |docker run --rm --name my-spark-app -e ENABLE_INIT_DAEMON=false --link - --net demo-net 10.140.15.238:5000/spark-app
```

## Reference
https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html
https://spark.apache.org/docs/2.4.4/api/python/pyspark.sql.html