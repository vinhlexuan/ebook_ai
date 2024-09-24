#!/bin/sh
echo "Initializing sqs on localstack"

awslocal sqs create-queue --queue-name priority-queue --region ap-northeast-1
awslocal sqs create-queue --queue-name normal-queue --region ap-northeast-1

awslocal s3 mb s3://vinh-lx-bucket