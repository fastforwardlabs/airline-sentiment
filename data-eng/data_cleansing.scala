//Project: Airline Sentiment 
//Author: Michael Gregory
//Description: Nightly data processing to
// - read from downloaded, data-stamped raw files
// - anonymize the tweeter's name
// - output as csv for model fitting


val hdfsDataDir = "hdfs:///tmp/airline-sentiment/incoming/"

import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql._
import org.apache.spark.sql.functions._

import scala.util.{Try, Success, Failure}
import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.FileSystem
import org.apache.hadoop.fs.Path
import org.apache.hadoop.fs.FileUtil
import org.apache.hadoop.fs.FileAlreadyExistsException
import org.apache.hadoop.fs.FileStatus
import org.apache.spark.sql.{DataFrame, Column}

object Airline {
  Logger.getLogger("org").setLevel(Level.WARN)
  Logger.getLogger("akka").setLevel(Level.WARN)
  def main(args: Array[String]): Unit = {
    val isLocal = true
    val spark = if (isLocal) {
      SparkSession.builder
        .master("local")
        .appName("my-spark-app")
        .config("spark.some.config.option", "config-value")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.sql.parquet.compression.codec", "gzip")
        //.enableHiveSupport()
        .getOrCreate()
    } else {
      SparkSession.builder
        .appName("my-spark-app")
        .config("spark.some.config.option", "config-value")
        //.enableHiveSupport()
        .getOrCreate()
    }
      import spark.implicits._
    val conf = spark.sparkContext.hadoopConfiguration
    val landingDir = args(0) //<input_dir>
    val completeDir = args(1) //complete_dir>

    val df =spark.read.option("header", true).csv("input_folder")

    //using md5. md5 might too long
   /*
   val dfAnnomd5 =  df.withColumn("annonym",md5($"name")) //hashing the name
     .select("annonym", "tweet_id", "airline_sentiment","text")
*/
    //crc return bigint

    val dfAnnocrc =  df.withColumn("annonym",crc32($"name")) //hashing the name
      .select("annonym", "tweet_id", "airline_sentiment","text")
    dfAnnocrc.write.option("header", true).csv("data/csv1")

    println("=================move file into complete folder================")
    val src:Path = new org.apache.hadoop.fs.Path(landingDir)
    val fs = FileSystem.get(spark.sparkContext.hadoopConfiguration)
    if (!fs.exists(new Path(completeDir))) fs.mkdirs(new Path(completeDir))
    val dst:Path = new Path(completeDir)
    val dstFs =FileSystem.get(dst.toUri,conf)
    val srcFs =FileSystem.get(src.toUri,conf)
      val status:Array[FileStatus] = fs.listStatus(new Path(landingDir))
      if (status.length>0) {
        status.foreach(x => {
          FileUtil.copy(srcFs,
            x.getPath,
            dstFs,
            dst,
            true, conf)

        }
        )
        println("processed "+  status.length +" files")}
      else{
        println("No Files Found !!")
      }

  }

}