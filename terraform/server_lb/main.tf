provider "aws" {
  region = "us-east-2"
}

resource "aws_instance" "server" {
  ami = "ami-036841078a4b68e14"
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.instance.id]

user_data = <<-EOF
            #!/bin/bash
            echo "Hey there" > index.html
            nohup busybox httpd -f -p 8080 &
            EOF

  user_data_replace_on_change = true

  tags = {
    Name = "Server"
  }
}


resource "aws_security_group" "instance" {
  name = "tf-instance"

  ingress {
    from_port = 8080
    to_port = 8080
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]

  }
}


output "instance_ip_addr" {
  value = aws_instance.server.private_ip
}