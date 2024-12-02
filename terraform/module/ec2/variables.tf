variable "instance_name" {
  type = string
  description = "Name of the EC2 Instance"
}

variable "instance_type" {
  description = "Type of the EC2 instance"
  type = string
}

variable "ami_id" {
  description = "AMI ID Of the instance"
  type = string
}

variable "instance_region" {
  type = string
  description = "Region of the instance"
}