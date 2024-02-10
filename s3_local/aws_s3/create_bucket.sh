#!/bin/bash

# Create the S3 bucket
awslocal --endpoint-url=http://localhost:4566 s3api create-bucket --bucket art-gallery --create-bucket-configuration LocationConstraint=eu-west-1
