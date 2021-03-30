# Amazon Comprehend demo using `boto3` SDK

Analysis performed on the March 25, 2021 [U.S. Economic Outlook and Monetary Policy](https://www.federalreserve.gov/newsevents/speech/clarida20210325a.htm) speech, given at the 2021 Institute of International Finance Washington Policy Summit, Washington, D.C. (_via webcast_).

## Content
See the [content](./content) directory for text content used for the analysis. Note since sentiment analysis with Amazon Comprehend is limited to 5000 bytes, so speech had to be split into two halves.

## Script
The [comprehend.py](./comprehend.py) script was used to perform all analyses.

## Results
See the [results](./results) directory for Amazon Comprehend results, in JSON. Note since sentiment analysis with Amazon Comprehend is limited to 5000 bytes, so speech had to be split into two halves.