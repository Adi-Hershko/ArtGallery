#!/bin/bash

# Create the S3 bucket
awslocal --endpoint-url=http://0.0.0.0:4566 s3api create-bucket --bucket art-gallery --create-bucket-configuration LocationConstraint=eu-west-1
