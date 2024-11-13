from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, when, col, from_json
from pyspark.sql.types import (
    FloatType,
    StructType,
    StructField,
    StringType,
)
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE = os.getenv("DATABASE")
COLLECTION = os.getenv("COLLECTION")

# Download NLTK resources
nltk.download("vader_lexicon")

# Define the schema of the JSON data
schema = StructType(
    [
        StructField("author", StringType(), True),
        StructField("comment", StringType(), True),
        StructField("profile_image", StringType(), True),
    ]
)

# Initialize Spark Session
spark = (
    SparkSession.builder.master("local")
    .appName("SparkStructuredStream")
    .config("spark.streaming.stopGracefullyOnShutdown", "true")
    .config("spark.mongodb.read.connection.uri", MONGODB_URI)
    .config("spark.mongodb.write.connection.uri", MONGODB_URI)
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,org.mongodb.spark:mongo-spark-connector_2.12:10.4.0",
    )
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

# Initialize the Sentiment Analyzer
sia = SentimentIntensityAnalyzer()


# Define function to get sentiment score
def get_sentiment_score(text):
    sentiment = sia.polarity_scores(text)
    return sentiment["compound"]


# Register UDF
sentiment_udf = udf(get_sentiment_score, FloatType())

# Load comments data from Kafka and parse JSON
comments_df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "127.0.0.1:9092")
    .option("subscribe", "RAW_DATA")
    .option("startingOffsets", "latest")
    .load()
    .selectExpr("CAST(value AS STRING) as json_value")
)

# Parse the JSON data and select columns with timestamp parsing
parsed_comments_df = comments_df.withColumn(
    "data", from_json("json_value", schema)
).select(
    col("data.author"),
    col("data.comment"),
    col("data.profile_image"),
)

# Apply sentiment analysis
comments_with_sentiment = parsed_comments_df.withColumn(
    "sentiment_score", sentiment_udf(col("comment"))
)

# Classify sentiments
comments_with_sentiment = comments_with_sentiment.withColumn(
    "sentiment",
    when(comments_with_sentiment["sentiment_score"] >= 0.05, "positive")
    .when(comments_with_sentiment["sentiment_score"] <= -0.05, "negative")
    .otherwise("neutral"),
)

# Define the foreachBatch function to write each batch to MongoDB
def write_to_mongodb(batch_df, batch_id):
    batch_df.write.format("mongodb").mode("append").option("uri", MONGODB_URI).option(
        "database", DATABASE
    ).option("collection", COLLECTION).save()


# Write the stream to MongoDB
query = (
    comments_with_sentiment.writeStream.outputMode("append")
    .foreachBatch(write_to_mongodb)
    .trigger(processingTime="1 seconds")
    .start()
)

# Await termination of the stream
query.awaitTermination()
