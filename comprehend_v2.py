#!/usr/bin/env python3

# Purpose: Analyze text with Amazon Comprehend: sentiment, syntax, entities, topic modeling, key phrases
# Author:  Gary A. Stafford (March 2021)
# SDK Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html
# Sentiment analysis documents limited to 5,000 bytes for sync or async

import json
import logging

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(format='[%(asctime)s] %(levelname)s - %(message)s', level=logging.INFO)

client = boto3.client('comprehend')

# *** CHANGE ME ***
AWS_ACCOUNT = '676164205626'
S3_URI_IN = f's3://comprehend-{AWS_ACCOUNT}-us-east-1/input/the_hill_we_climb_amanda_gorman.txt'
S3_URI_OUT = f's3://comprehend-{AWS_ACCOUNT}-us-east-1/output/'
DATA_ACCESS_ROLE_ARN = f'arn:aws:iam::{AWS_ACCOUNT}:role/service-role/AmazonComprehendServiceRole-S3'
LANGUAGE = 'en'


def main():
    # Available Methods
    content = get_content('content/the_hill_we_climb_amanda_gorman.txt', 0)

    sentiment, score = detect_sentiment(content)
    logging.info(f'Prevailing Sentiment: {sentiment}')
    logging.info(f'Sentiment Score: {score}')

    entities = detect_entities(content)
    logging.info(f'Named Entities (first 10): {json.dumps(entities[0:10], indent=4, sort_keys=True)}')

    syntax_tokens = detect_syntax(content)
    logging.info(f'Syntax Tokens (first 10): {json.dumps(syntax_tokens[0:10], indent=4, sort_keys=True)}')

    key_phrases = detect_key_phrases(content)
    logging.info(f'Key Phrases (top 10): {json.dumps(key_phrases[0:10], indent=4, sort_keys=True)}')

    start_entities_detection_job('fed_speech_entities_detection', S3_URI_IN)
    start_topics_detection_job('fed_speech_topic_detection', S3_URI_IN)
    start_key_phrases_detection_job('key_phrases_detection', S3_URI_IN)
    start_sentiment_detection_job('fed_speech_sentiment_detection', S3_URI_IN)


def get_content(file_path, length):
    """Read in text file, trim, and return string"""

    f = open(file_path, "r")
    content = f.read()
    if length > 0:
        content = content[:length]
    if length < 0:
        content = content[length:]
    return content


def detect_entities(content):
    """Inspects text for named entities, and returns information about them."""

    try:
        response = client.detect_entities(
            Text=content,
            LanguageCode=LANGUAGE
        )
        logging.info(json.dumps(response, indent=4, sort_keys=True))
        return response['Entities']
    except ClientError as e:
        logging.error(e)
        exit(1)


def detect_key_phrases(content):
    """Detects the key noun phrases found in the text."""

    try:
        response = client.detect_key_phrases(
            Text=content,
            LanguageCode=LANGUAGE
        )
        logging.info(json.dumps(response, indent=4, sort_keys=True))
        return response['KeyPhrases']
    except ClientError as e:
        logging.error(e)
        exit(1)


def detect_syntax(content):
    """Inspects text for syntax and the part of speech of words in the document."""

    try:
        response = client.detect_syntax(
            Text=content,
            LanguageCode=LANGUAGE
        )
        logging.info(json.dumps(response, indent=4, sort_keys=True))
        return response['SyntaxTokens']
    except ClientError as e:
        logging.error(e)
        exit(1)


def detect_sentiment(content):
    """Inspects text and returns an inference of the prevailing sentiment."""

    try:
        response = client.detect_sentiment(
            Text=content,
            LanguageCode=LANGUAGE
        )
        logging.info(json.dumps(response, indent=4, sort_keys=True))
        return response['Sentiment'], response['SentimentScore']
    except ClientError as e:
        logging.error(e)
        exit(1)


def start_topics_detection_job(job_name, s3_uri_in):
    """Starts an asynchronous topic detection job."""

    try:
        response = client.start_topics_detection_job(
            InputDataConfig={
                'S3Uri': s3_uri_in,
                'InputFormat': 'ONE_DOC_PER_FILE'
            },
            OutputDataConfig={
                'S3Uri': S3_URI_OUT
            },
            DataAccessRoleArn=DATA_ACCESS_ROLE_ARN,
            JobName=job_name,
            NumberOfTopics=25
        )
        logging.info(f'Topic Detection Job Id: {response}')
    except ClientError as e:
        logging.error(e)
        exit(1)


def start_entities_detection_job(job_name, s3_uri_in):
    """Starts an asynchronous entity detection job for a collection of documents."""

    try:
        response = client.start_entities_detection_job(
            InputDataConfig={
                'S3Uri': s3_uri_in,
                'InputFormat': 'ONE_DOC_PER_FILE'
            },
            OutputDataConfig={
                'S3Uri': S3_URI_OUT
            },
            DataAccessRoleArn=DATA_ACCESS_ROLE_ARN,
            JobName=job_name,
            LanguageCode=LANGUAGE
        )
        logging.info(f'Entities Detection Job Id: {response["JobId"]}')
    except ClientError as e:
        logging.error(e)
        exit(1)


def start_key_phrases_detection_job(job_name, s3_uri_in):
    """Starts an asynchronous key phrase detection job for a collection of documents."""

    try:
        response = client.start_key_phrases_detection_job(
            InputDataConfig={
                'S3Uri': s3_uri_in,
                'InputFormat': 'ONE_DOC_PER_FILE'
            },
            OutputDataConfig={
                'S3Uri': S3_URI_OUT
            },
            DataAccessRoleArn=DATA_ACCESS_ROLE_ARN,
            JobName=job_name,
            LanguageCode=LANGUAGE
        )
        logging.info(f'Key Phrase Detection Job Id: {response["JobId"]}')
    except ClientError as e:
        logging.error(e)
        exit(1)


def start_sentiment_detection_job(job_name, s3_uri_in):
    """Starts an asynchronous sentiment detection job for a collection of documents."""

    try:
        response = client.start_sentiment_detection_job(
            InputDataConfig={
                'S3Uri': s3_uri_in,
                'InputFormat': 'ONE_DOC_PER_FILE'
            },
            OutputDataConfig={
                'S3Uri': S3_URI_OUT
            },
            DataAccessRoleArn=DATA_ACCESS_ROLE_ARN,
            JobName=job_name,
            LanguageCode=LANGUAGE
        )
        logging.info(f'Sentiment Detection Job Id: {response["JobId"]}')
    except ClientError as e:
        logging.error(e)
        exit(1)


if __name__ == '__main__':
    main()