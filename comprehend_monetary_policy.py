#!/usr/bin/env python3

# Purpose: Analyze text with Amazon Comprehend: sentiment, syntax, entities, topic modeling, key phrases
# Author:  Gary A. Stafford (April 2021)
# SDK Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html
# Sentiment analysis documents limited to 5,000 bytes for sync or async - this example is split into two parts

import json
import logging

import Comprehend.analyze as comprehend

logging.basicConfig(format='[%(asctime)s] %(levelname)s - %(message)s', level=logging.INFO)

# *** CHANGE ME ***
aws_account = '111222333444'
s3_uri_in_full = f's3://comprehend-{aws_account}-us-east-1/input/us_economic_outlook_monetary_policy_full.txt'
s3_uri_in_5k_p1 = f's3://comprehend-{aws_account}-us-east-1/input/us_economic_outlook_monetary_policy_5k_p1.txt'
s3_uri_in_5k_p2 = f's3://comprehend-{aws_account}-us-east-1/input/us_economic_outlook_monetary_policy_5k_p2.txt'
s3_uri_out = f's3://comprehend-{aws_account}-us-east-1/output/'
data_access_role_arn = f'arn:aws:iam::{aws_account}:role/service-role/AmazonComprehendServiceRole-S3'
language = 'en'


def main():
    content = comprehend.get_content('content/us_economic_outlook_monetary_policy_full.txt', 4986)
    sentiment, score = comprehend.detect_sentiment(content, language)
    logging.info(f'Prevailing Sentiment (part 1): {sentiment}')
    logging.info(f'Sentiment Score (part 1): {score}')

    content = comprehend.get_content('content/us_economic_outlook_monetary_policy_full.txt', -4978)
    sentiment, score = comprehend.detect_sentiment(content, language)
    logging.info(f'Prevailing Sentiment (part 2): {sentiment}')
    logging.info(f'Sentiment Score (part 2): {score}')

    content = comprehend.get_content('content/us_economic_outlook_monetary_policy_full.txt', 4986)

    entities = comprehend.detect_entities(content, language)
    logging.info(f'Named Entities (first 10): {json.dumps(entities[0:10], indent=4, sort_keys=True)}')

    syntax_tokens = comprehend.detect_syntax(content, language)
    logging.info(f'Syntax Tokens (first 10): {json.dumps(syntax_tokens[0:10], indent=4, sort_keys=True)}')

    key_phrases = comprehend.detect_key_phrases(content, language)
    logging.info(f'Key Phrases (top 10): {json.dumps(key_phrases[0:10], indent=4, sort_keys=True)}')

    comprehend.start_entities_detection_job('monetary_policy_entities_detection', s3_uri_in_full, s3_uri_out,
                                            data_access_role_arn, language)
    comprehend.start_topics_detection_job('monetary_policy_topic_detection', s3_uri_in_full, s3_uri_out,
                                          data_access_role_arn)
    comprehend.start_key_phrases_detection_job('monetary_policy_key_phrases_detection', s3_uri_in_full, s3_uri_out,
                                               data_access_role_arn, language)
    comprehend.start_sentiment_detection_job('monetary_policy_sentiment_detection_p1', s3_uri_in_5k_p1, s3_uri_out,
                                             data_access_role_arn, language)
    comprehend.start_sentiment_detection_job('monetary_policy_sentiment_detection_p2', s3_uri_in_5k_p2, s3_uri_out,
                                             data_access_role_arn, language)


if __name__ == '__main__':
    main()
