#!/bin/sh

CDSW_HOST2=`hostname -s | sed 's/\-4/\-5/g'`
CDSW_HOST3=`hostname -s | sed 's/\-4/\-6/g'`

#sudo yum install -y git
#git clone https://github.com/fastforwardlabs/airline-sentiment
#cd airline-sentiment
sudo docker build --network=host -t spacy:1 . -f Dockerfile
sudo docker image save -o ./spacy.tar spacy:1
sudo chmod 755 ./spacy.tar
scp -i ~/.ssh/id_rsa -o StrictHostKeyChecking=no spacy.tar $CDSW_HOST2:~
scp -i ~/.ssh/id_rsa -o StrictHostKeyChecking=no spacy.tar $CDSW_HOST3:~
ssh -i ~/.ssh/id_rsa -o StrictHostKeyChecking=no $CDSW_HOST2 "sudo docker load --input ~/spacy.tar"
ssh -i ~/.ssh/id_rsa -o StrictHostKeyChecking=no $CDSW_HOST3 "sudo docker load --input ~/spacy.tar"

#Jupyter : /usr/local/bin/jupyter notebook --no-browser --port=$CDSW_APP_PORT --ip=127.0.0.1 --NotebookApp.token='' --NotebookApp.allow_remote_access=True

#Rstudio : /usr/sbin/rstudio-server start
