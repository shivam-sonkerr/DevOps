variable "instance_count"{
  type = number
}

variable "instance_type" {
  type = string
}

variable "ami_id"{
  type = string
}

variable "subnet_id" {
  type = string
}

variable "security_groups"{
  type = list(string)
}

variable "environment"{
  type = string
}

variable "tags" {
  type = map(string)
}