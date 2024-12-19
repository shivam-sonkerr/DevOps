resource "aws_security_group" "alb" {
name = "${var.cluster_name}-alb"

ingress {
from_port = 80
to_port = 80
protocol = "tcp"
cidr_blocks = ["0.0.0.0/0"]

}

egress {
from_port=0
to_port=0
protocol="-1"
cidr_blocks=["0.0.0.0/0"]
}
}

data "terraform_remote_state" "db" {
backend = "s3"

config = {
  bucket = var.db_remote_state_bucket
  key = var.db_remote_state_key
  region = "us-east-2"
}
}


