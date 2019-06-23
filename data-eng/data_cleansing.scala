//Project: Airline Sentiment 
//Author: Michael Gregory
//Description: Nightly data processing to
// - read from downloaded, data-stamped raw files
// - anonymize the tweeter's name
// - output as csv for model fitting

import sys.process._

val hdfsDataDir = "hdfs:///tmp/airline-sentiment/incoming/"

import org.apache.hadoop.fs.Path
import org.apache.spark.sql.{DataFrame, SparkSession}

val spark = SparkSession.builder().getOrCreate()
import spark.implicits._
    
val rawInput = "hdfs:///tmp/airline-sentiment/incoming/*"
val csvInput = "hdfs:///tmp/airline-sentiment/Tweets.csv"
    
spark.read.textFile(rawInput).
  map { line =>
    if (line.startsWith("\"date\"")) {
      line
      } else {
      line.substring(line.indexOf(',') + 1)
      }
    }.
  repartition(1).
  write.text(csvInput)

spark.stop()
