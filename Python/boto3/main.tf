resource "aws_instance" "server" {
  ami = "ami-0caa91d6b7bee0ed0"
  instance_type = "t2.micro"

  tags = {
    Name = "my-server"
  }
}