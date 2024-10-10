#!/bin/bash

echo "Script started to push changes to git repository"

git add .

echo "Add the commit message: "
read msg

echo "Commit message is : $msg"

git commit -m "$msg"

git push

echo "Changes pushed successfully"
