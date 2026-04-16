provider "aws"{
  region = "us-east-1"
}
resource "aws_s3_bucket" "learning" {
  bucket_prefix = "sh"


  tags = {
    Name        = "Practise"
    Environment = "Dev"
  }
}