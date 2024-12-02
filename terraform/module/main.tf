provider "aws" {
  region = var.default_region
}

module "ec2_us_east" {
  source = "./ec2"
  instance_name = "east_ec2_instance"


}