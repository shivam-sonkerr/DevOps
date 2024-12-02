output "instance_public_ip" {
  value = aws_instance.ec2.public_ip
  description = "Public IP of the EC2 Instance"
}