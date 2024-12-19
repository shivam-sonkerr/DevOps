provider "aws" {
  region = "us-east-2"
}

data "aws_caller_identity" "self" {}


data "aws_iam_policy_document" "cmk_admin_policy" {
  statement {
    effect    = "Allow"
    resources = ["*"]
    actions   = ["kms:*"]
    principals {
      identifiers = [data.aws_caller_identity.self.arn]
      type        = "AWS"
    }
  }
}

resource "aws_kms_key" "cmk" {
  policy = data.aws_iam_policy_document.cmk_admin_policy.json
}

resource "aws_kms_alias" "cmk" {
  target_key_id = aws_kms_key.cmk.id
  name          = "alias/kms-cmk"
}


data "aws_kms_secrets" "creds" {
  secret {
    name    = "db"
    payload = file("${path.module}/db-creds.yml.encrypted")
  }
}

locals {
  db_creds = yamldecode(data.aws_kms_secrets.creds.plaintext["db"])
}

resource "aws_db_instance" "db_kms" {
  allocated_storage   = 5
  db_name             = "mydb"
  instance_class      = "db.t4g.micro"
  engine              = "mysql"
  engine_version      = "8.0.39"
  skip_final_snapshot = true

  username = local.db_creds.username
  password = local.db_creds.password
}