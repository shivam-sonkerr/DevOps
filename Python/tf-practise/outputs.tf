output "vpc_id" {
  value = aws_vpc.learn.id
  description = "VPC ID"
}


output "instance_ids" {
  value = module.web_servers.instance_ids
}

output "instance_public_ips" {
  value = module.web_servers.public_ips
  description = "Public IPs of EC2 instances"
}

output "ami_id" {
  value = data.aws_ami.amazon_linux.id
}