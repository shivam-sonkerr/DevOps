resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  instance_tenancy = "default"

  tags = {
    Name = "main_learn"
  }
}


resource "aws_instance" "learn" {
  ami = "ami-0a9f08a6603f3338e"
  instance_type = "t2.micro"

  tags = {

  }
}