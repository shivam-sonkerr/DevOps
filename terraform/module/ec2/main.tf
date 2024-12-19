provider "aws" {
  region = var.instance_region
}

resource "aws_instance" "ec2" {
  ami = var.ami_id
  instance_type = var.instance_type
  tags = {
    Name = var.instance_name
  }
}

output "public_ip" {
  value =aws_instance.ec2.public_ip
  description = "The public IP of the EC2 instance"
}