#!/usr/bin/env python3

# Purpose: Analyze text with Amazon Comprehend: sentiment, syntax, entities, topic modeling, key phrases
# Author:  Gary A. Stafford (March 2021)
# SDK Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html
# Sentiment analysis documents limited to 5,000 bytes for sync or async - this example is split into two parts

import json
import logging

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(format='[%(asctime)s] %(levelname)s - %(message)s', level=logging.INFO)

client = boto3.client('comprehend')


def get_content(file_path, length):
    """Read in text file, trim, and return string"""

    f = open(file_path, "r")
    content = f.read()
    if length > 0:
        content = content[:length]
    if length < 0:
        content = content[length:]
    return content


def detect_entities(content, language):
    """Inspects text for named entities, and returns information about them."""

    try:
        response = client.detect_entities(
            Text=content,
            LanguageCode=language
        )
        logging.info(json.dumps(response, indent=4, sort_keys=True))
        return response['Entities']
    except ClientError as e:
        logging.error(e)
        exit(1)


def detect_key_phrases(content, language):
    """Detects the key noun phrases found in the text."""

    try:
        response = client.detect_key_phrases(
            Text=content,
            LanguageCode=language
        )
        logging.info(json.dumps(response, indent=4, sort_keys=True))
        return response['KeyPhrases']
    except ClientError as e:
        logging.error(e)
        exit(1)


def detect_syntax(content, language):
    """Inspects text for syntax and the part of speech of words in the document."""

    try:
        response = client.detect_syntax(
            Text=content,
            LanguageCode=language
        )
        logging.info(json.dumps(response, indent=4, sort_keys=True))
        return response['SyntaxTokens']
    except ClientError as e:
        logging.error(e)
        exit(1)


def detect_sentiment(content, language):
    """Inspects text and returns an inference of the prevailing sentiment."""

    try:
        response = client.detect_sentiment(
            Text=content,
            LanguageCode=language
        )
        logging.info(json.dumps(response, indent=4, sort_keys=True))
        return response['Sentiment'], response['SentimentScore']
    except ClientError as e:
        logging.error(e)
        exit(1)


def start_topics_detection_job(job_name, s3_uri_in, s3_uri_out, data_access_role_arn):
    """Starts an asynchronous topic detection job."""

    try:
        response = client.start_topics_detection_job(
            InputDataConfig={
                'S3Uri': s3_uri_in,
                'InputFormat': 'ONE_DOC_PER_FILE'
            },
            OutputDataConfig={
                'S3Uri': s3_uri_out
            },
            DataAccessRoleArn=data_access_role_arn,
            JobName=job_name,
            NumberOfTopics=5
        )
        logging.info(f'Topic Detection Job Id: {response}')
    except ClientError as e:
        logging.error(e)
        exit(1)


def start_entities_detection_job(job_name, s3_uri_in, s3_uri_out, data_access_role_arn, language):
    """Starts an asynchronous entity detection job for a collection of documents."""

    try:
        response = client.start_entities_detection_job(
            InputDataConfig={
                'S3Uri': s3_uri_in,
                'InputFormat': 'ONE_DOC_PER_FILE'
            },
            OutputDataConfig={
                'S3Uri': s3_uri_out
            },
            DataAccessRoleArn=data_access_role_arn,
            JobName=job_name,
            LanguageCode=language
        )
        logging.info(f'Entities Detection Job Id: {response["JobId"]}')
    except ClientError as e:
        logging.error(e)
        exit(1)


def start_key_phrases_detection_job(job_name, s3_uri_in, s3_uri_out, data_access_role_arn, language):
    """Starts an asynchronous key phrase detection job for a collection of documents."""

    try:
        response = client.start_key_phrases_detection_job(
            InputDataConfig={
                'S3Uri': s3_uri_in,
                'InputFormat': 'ONE_DOC_PER_FILE'
            },
            OutputDataConfig={
                'S3Uri': s3_uri_out
            },
            DataAccessRoleArn=data_access_role_arn,
            JobName=job_name,
            LanguageCode=language
        )
        logging.info(f'Key Phrase Detection Job Id: {response["JobId"]}')
    except ClientError as e:
        logging.error(e)
        exit(1)


def start_sentiment_detection_job(job_name, s3_uri_in, s3_uri_out, data_access_role_arn, language):
    """Starts an asynchronous sentiment detection job for a collection of documents."""

    try:
        response = client.start_sentiment_detection_job(
            InputDataConfig={
                'S3Uri': s3_uri_in,
                'InputFormat': 'ONE_DOC_PER_FILE'
            },
            OutputDataConfig={
                'S3Uri': s3_uri_out
            },
            DataAccessRoleArn=data_access_role_arn,
            JobName=job_name,
            LanguageCode=language
        )
        logging.info(f'Sentiment Detection Job Id: {response["JobId"]}')
    except ClientError as e:
        logging.error(e)
        exit(1)
