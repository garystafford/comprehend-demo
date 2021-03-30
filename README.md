# Amazon Comprehend Analyses Demo

Example of several types of [Amazon Comprehend](https://aws.amazon.com/comprehend/) analyses: Sentiment, Syntax, Entity
detection, Topic modeling (arbitrary 25 topics), and Key phrases detection. Performed using the `boto3` SDK. Analyses performed on the March
25,
2021 [U.S. Economic Outlook and Monetary Policy](https://www.federalreserve.gov/newsevents/speech/clarida20210325a.htm)
speech, given at the 2021 Institute of International Finance Washington Policy Summit, Washington, D.C. (_via webcast_).

## Content

See the [content](./content) directory for text content used for the analysis. Note Sentiment analysis with Amazon
Comprehend is limited to only 5,000 bytes. Thus, the speech had to be split into two halves for only the Sentiment
analysis

## Script

The [comprehend.py](./comprehend.py) script was used to perform all analyses.

## Results

See the [results](./results) directory for Amazon Comprehend results. All results are in JSON,
except [topic modeling](./results/topic_modeling), which is in CSV.