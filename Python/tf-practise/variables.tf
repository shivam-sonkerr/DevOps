variable "aws_region" {
  type        = string
  default     = "us-west-2"
  description = "AWS Region"
}

variable "environment" {
  type = string
  validation {
    condition = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Select the environment"
  }
}

variable "instance_count" {
  type    = number
  default = 2
}

variable "instance_type" {
  type = string
}

variable "common_tags" {
  type = map(string)
  default = {
    ManagedBy = "Terraform"
  }
}
