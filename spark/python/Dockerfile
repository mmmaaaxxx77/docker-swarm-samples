FROM bde2020/spark-submit:2.4.4-hadoop2.7

MAINTAINER Cecile Tonglet <cecile.tonglet@tenforce.com>

COPY template.sh /

# Copy the requirements.txt first, for separate dependency resolving and downloading
RUN mkdir /app
COPY requirements.txt /app/
RUN cd /app \
      && pip3 install -r requirements.txt

# Copy the source code
COPY . /app

ENV SPARK_SUBMIT_ARGS="--conf spark.driver.extraJavaOptions=-Dlog4j.configuration=file:/app/log4j.properties --conf spark.executor.extraJavaOptions=-Dlog4j.configuration=file:/app/log4j.properties --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.4"

CMD ["/bin/bash", "/template.sh"]