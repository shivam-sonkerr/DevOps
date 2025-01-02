provider "aws" {
  region = "us-east-2"
}

# resource "aws_instance" "server" {
#   ami = "ami-036841078a4b68e14"
#   instance_type = "t2.micro"
#   vpc_security_group_ids = [aws_security_group.instance.id]
#
# user_data = <<-EOF
#             #!/bin/bash
#             echo "Hey there" > index.html
#             nohup busybox httpd -f -p ${var.server_port} &
#             EOF
#   user_data_replace_on_change = true
#
#   tags = {
#     Name = "Server"
#   }
# }


resource "aws_security_group" "instance" {
  name = "tf-instance"

  ingress {
    from_port = var.server_port
    to_port = var.server_port
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]

  }
}

resource "aws_launch_template" "launch" {
  image_id      = "ami-036841078a4b68e14"
  instance_type = "t2.micro"

  user_data = base64encode(<<-EOF
    #!/bin/bash
    echo "Hey there, how are you" > index.html
    nohup busybox httpd -f -p ${var.server_port} &
  EOF
  )

  lifecycle {
    create_before_destroy = true
  }
}


data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_autoscaling_group" "launch" {

  launch_template {
    id      = aws_launch_template.launch.id
    version = "$Latest"
  }

  vpc_zone_identifier = data.aws_subnets.default.ids


  min_size = 2
  max_size = 10

  tag {
    key = "Name"
    value = "launch_asg"
    propagate_at_launch = true
  }
}

resource "aws_lb" "lb" {
  name = "learn-lb"
  load_balancer_type = "application"
  subnets = data.aws_subnets.default.ids
}