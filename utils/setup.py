
#Run this only if you are not using a custom docker image
#To build a custom docker image for this project run commands like in build-engine.sh

##NOTE: You need a session with at least 8GB memory to run this

cd
#!hdfs dfs -mkdir /tmp/airline-sentiment

!mkdir /home/cdsw/R

!cp utils/cdsw-build.sh .

!chmod 755 cdsw-build.sh
!sh /home/cdsw/cdsw-build.sh

#!/usr/local/bin/Rscript install.R
