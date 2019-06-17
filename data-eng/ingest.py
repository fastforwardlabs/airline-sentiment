#curl -u username:password sftp://hostname/path/to/file.txt | hdfs dfs -put - file.txt

!curl https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data | hdfs dfs -put - iris-`date-I`.txt

