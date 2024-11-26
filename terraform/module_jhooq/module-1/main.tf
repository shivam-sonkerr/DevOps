resource "aws_instance" "ec2_example" {
  ami = "ami-0c80e2b6ccb9ad6d1"
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.main.id]
}

user_data =<<-EOF
          #!/bin/sh
          sudo apt-get update
          sudo apt install -y apache2
          sudo systemctl status apache2
          sudo systemctl start apache2
          sudo chown -R $USER:$USER /var/www/html
          sudo echo "<html> <body> <h1> Hello This is module-1 at instance"
          EOF



resource "aws_security_group" "main" {
  name = "EC2-webserver-1"
  description = "Webserver for EC2 instances"


  ingress {
    from_port = 80
    protocol = "TCP"
    to_port = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    protocol = "-1"
    to_port = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}
