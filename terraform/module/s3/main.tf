terraform {
  required_providers {
    awscc = {
      source  = "hashicorp/awscc"
      version = "1.2.0"
    }
  }
}
provider "aws" {
  region = "us-east-2"
}

resource "aws_s3_bucket" "state-manage" {
  bucket = "state-management-87"

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "enabled" {
  bucket = aws_s3_bucket.state-manage.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "default" {
  bucket = aws_s3_bucket.state-manage.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "public_access" {
  bucket = aws_s3_bucket.state-manage.id
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}

resource "aws_dynamodb_table" "locks" {
  name = "locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}


terraform {
  backend "s3" {
  bucket = "state-management-87"
  key = "global/s3/terraform.state"
  region = "us-east-2"

  dynamodb_table = "locks"
  encrypt = true
}
}