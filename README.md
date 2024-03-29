# Amazon Comprehend Samples/Demonstration

Example of several types of [Amazon Comprehend](https://aws.amazon.com/comprehend/) analyses: Sentiment, Syntax, Entity
detection, Topic modeling (arbitrary 5 topics), and Key phrases detection. Analyses performed using the `boto3` Python SDK for Comprehend.

## Analysis Sources
 - The [U.S. Economic Outlook and Monetary Policy](https://www.federalreserve.gov/newsevents/speech/clarida20210325a.htm) speech, given at the 2021 Institute of International Finance Washington Policy Summit, Washington, D.C., on March 25, 2021.

- Amanda Gorman's poem, [The Hill We Climb](https://www.rev.com/blog/transcripts/amanda-gorman-inauguration-poem-transcript-the-hill-we-climb), read at Joe Biden’s January 20, 2021 Presidential Inauguration.

## Textual Content

See the [content](./content) directory for text content used for the analysis. Note Sentiment analysis with Amazon Comprehend is limited to only 5,000 bytes. Thus, the Monetary Policy speech had to be split into two halves for only the Sentiment
analysis.

## Python Scripts

- The [comprehend_monetary_policy.py](comprehend_monetary_policy.py) Python 3 script was used to perform all analyses for the longer Monetary Policy speech.

- The [comprehend_gorman_poem.py](comprehend_gorman_poem.py) Python 3 script was used to perform all analyses for the shorter Amanda Gorman poem.


## Analysis Results

See the [results](./results) directory for Amazon Comprehend results. All results are in JSON format, except [topic modeling](results/us_economic_outlook_monetary_policy/topic_modeling), which is in CSV format.
