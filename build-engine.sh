#!/bin/sh

CDSW_HOST2=`hostname -s | sed 's/\-4/\-5/g'`
CDSW_HOST3=`hostname -s | sed 's/\-4/\-6/g'`

#sudo yum install -y git
#git clone https://github.com/fastforwardlabs/airline-sentiment
cd airline-sentiment
sudo docker build --network=host -t spacy:1 . -f Dockerfile
sudo docker image save -o ./spacy.tar spacy:1
sudo scp -o StrictHostKeyChecking=no spacy.tar $CDSW_HOST2:~
sudo scp -o StrictHostKeyChecking=no spacy.tar $CDSW_HOST3:~
ssh -o StrictHostKeyChecking=no $CDSW_HOST2 "sudo docker load --input ~/spacy.tar"
ssh -o StrictHostKeyChecking=no $CDSW_HOST3 "sudo docker load --input ~/spacy.tar"
