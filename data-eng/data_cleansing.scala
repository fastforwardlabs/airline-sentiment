//Nightly data processing to read from raw files make some simple transformations and output as csv for model fitting
import sys.process._

//download the data and put to HDFS
//"curl -o iris.txt https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data" !
//"hdfs dfs -put -f iris.txt" !
//"rm iris.txt" !

import org.apache.hadoop.fs.Path
import org.apache.spark.sql.{DataFrame, SparkSession}

val spark = SparkSession.builder().getOrCreate()
import spark.implicits._
    
val rawInput = "hdfs:///user/demo/iris.txt"
val csvInput = "hdfs:///user/demo/iris.csv"
    
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

"hdfs dfs -get -f iris.csv/*.txt iris.csv" !
"hdfs dfs -rmr -f iris.csv iris.txt" !

spark.stop()
