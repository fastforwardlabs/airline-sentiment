# PROJECT: Sentiment Analysis Pilot 

The purpose of this project is to pilot development of customer sentiment analysis capabilities using an exemplary test-case based on publically available sentiment data.

## Details
1. Business Objective: Ready the team and process for deploying business-specific sentiment analysis capabilities using a pilot project to organize, exercise and document team workflow and skills required for future projects.   
2. LOB: **Marketing**
3. Data Source(s): airline-sentiment/data/Tweets.csv (airline sentiment csv files)
4. Dependent applications: TBD
...

## Team Members
- Project Manager: Bethann Noble
- Data Engineer: Michael Gregory
- Data Scientist: Jeff Fletcher
- Modeller: Shioulin Sam
- Dev Ops: Ayushmaan Kumar
- App Dev: Andre Loose

## Project Phases
- Phase 1: Basic end-to-end workflow set-up.
  -PM Signoff: June 24, 2019
- Phase 2: Set-up streaming ingest and nightly re-training.
- Phase 3: Automatic notification to LOB of sentiment change at threshold.


## Data Engineering
We will use a static dataset of Twitter feeds relating to airlines as a starting point for phase 1.

https://www.kaggle.com/crowdflower/twitter-airline-sentiment/downloads/Tweets.csv

Ingest: I've created an ingest.py as a placeholder for nightly batch ingest.  Currently it only pulls thes 
same static file but in phase 2 we will change it to a streaming pipeline with Cloudera Data Flow

Data Prep: I am using Spark to process the tweets and anonymize the username field.  Addiitonaly prep
can be added as needed by the DS team.

Data: hdfs:///tmp/airline-sentiment/Tweets.csv

## Data Scientist
This is the a more general data analysis of the data that's present.

It starts with showing a table of all tweets, then narrows it down to tweet types by airline 
(i.e. positive, netural, negative) and plot as a stacked bar chart. This is followed by tweets by
location which is also plotted using leaflet.

Finally the complete tweet corpus is analysed to show word frequency across all words. This is also 
plotted on a bar chart and finally a wordcloud (just for Michael)

For this project and to meet the business objectives, the data that is usefull is sentiment
per airline, therefore we only need the tweet text for positive and negative tweets by airline.

## Modeller
The goal is to build a business application to understand and monitor sentiment of the airline and its competitors.  

Model is based on a RNN and uses pretrained vectors. It takes in a tweet and performs a binary classification.

The output is the classifier and the vocabulary as pickle files. 

## Dev Ops

Used for prediction function of sentiment embeddings and actual value of the sentiment.