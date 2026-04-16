output "bucket"{
  value = aws_s3_bucket.learning.bucket
}

output "arn" {
  value = aws_s3_bucket.learning.arn
}