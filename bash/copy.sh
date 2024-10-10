#!/bin/bash

echo "Let us start the copy wizard"

echo "Zipping the files first"

tar -czf backup.tar.gz /root/DevOps/

echo "Zipping of folder is completed"

echo "Copy to S3 bucket"

echo "Starting to copy to S3 bucket"

aws s3 mv backup.tar.gz s3://daily-folder-upload/devops/

echo "Copied folder successfully"





