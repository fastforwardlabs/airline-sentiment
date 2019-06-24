//Project: Airline Sentiment 
//Author: Michael Gregory
//Description: Nightly data processing to
// - read from downloaded, data-stamped raw files
// - anonymize the tweeter's name
// - output as csv for model fitting

import sys.process._
import java.io.File
import org.apache.hadoop.fs.FileSystem
import org.apache.hadoop.fs.Path
import org.apache.spark.sql.{DataFrame, SparkSession}


val hdfsDataDir = "hdfs:///tmp/airline-sentiment/incoming/"

val spark = SparkSession.builder().getOrCreate()
import spark.implicits._

//def getListOfFiles(dir: File):List[File] = dir.listFiles.filter(_.isFile).toList
//def getListOfFiles(dir: String):List[File] = {
//    val d = new File(dir)
//    if (d.exists && d.isDirectory) {
//        d.listFiles.filter(_.isFile).toList
//    } else {
//        List[File]()
//    }
//}
//val files = getListOfFiles(hdfsDataDir)
    
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
