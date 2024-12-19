provider "aws" {
  region = var.default_region
}

module "ec2_us_east" {
  source = "./ec2"
  instance_name = "east_ec2_instance"
  instance_type = "t2.micro"
  ami_id = "ami-0453ec754f44f9a4a"
  instance_region = "us-east-1"
}

module "ec2_us_west" {
  source = "./ec2"
  instance_name = "ec2_west"
  instance_type = "t2.micro"
  ami_id = "ami-055e3d4f0bbeb5878"
  instance_region = "us-west-2"
}