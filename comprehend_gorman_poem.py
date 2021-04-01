#!/usr/bin/env python3

# Purpose: Analyze text with Amazon Comprehend: sentiment, syntax, entities, topic modeling, key phrases
# Author:  Gary A. Stafford (April 2021)
# SDK Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html
# Sentiment analysis documents limited to 5,000 bytes for sync or async

import json
import logging

import Comprehend.analyze as comprehend

logging.basicConfig(format='[%(asctime)s] %(levelname)s - %(message)s', level=logging.INFO)

# *** CHANGE ME ***
aws_account = '111222333444'
s3_uri_in = f's3://comprehend-{aws_account}-us-east-1/input/the_hill_we_climb_amanda_gorman.txt'
s3_uri_out = f's3://comprehend-{aws_account}-us-east-1/output/'
data_access_role_arn = f'arn:aws:iam::{aws_account}:role/service-role/AmazonComprehendServiceRole-S3'
language = 'en'


def main():
    content = comprehend.get_content('content/the_hill_we_climb_amanda_gorman.txt', 0)

    sentiment, score = comprehend.detect_sentiment(content, language)
    logging.info(f'Prevailing Sentiment: {sentiment}')
    logging.info(f'Sentiment Score: {score}')

    entities = comprehend.detect_entities(content, language)
    logging.info(f'Named Entities (first 10): {json.dumps(entities[0:10], indent=4, sort_keys=True)}')

    syntax_tokens = comprehend.detect_syntax(content, language)
    logging.info(f'Syntax Tokens (first 10): {json.dumps(syntax_tokens[0:10], indent=4, sort_keys=True)}')

    key_phrases = comprehend.detect_key_phrases(content, language)
    logging.info(f'Key Phrases (top 10): {json.dumps(key_phrases[0:10], indent=4, sort_keys=True)}')

    comprehend.start_entities_detection_job('gorman_entities_detection', s3_uri_in, s3_uri_out,
                                            data_access_role_arn, language)
    comprehend.start_topics_detection_job('gorman_topic_detection', s3_uri_in, s3_uri_out,
                                          data_access_role_arn)
    comprehend.start_key_phrases_detection_job('gorman_key_phrases_detection', s3_uri_in, s3_uri_out,
                                               data_access_role_arn, language)
    comprehend.start_sentiment_detection_job('gorman_sentiment_detection', s3_uri_in, s3_uri_out,
                                             data_access_role_arn, language)


if __name__ == '__main__':
    main()
