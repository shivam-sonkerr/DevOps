output "ec2_us_east_public_ip" {
  value = module.ec2_us_east.instance_public_ip
}

output "ec2_us_west_public_ip" {
  value = module.ec2_us_west.instance_public_ip
}