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


# resource "aws_security_group" "instance" {
#   name = "tf-instance"
#
#   ingress {
#     from_port = var.server_port
#     to_port = var.server_port
#     protocol = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#
#   }
# }

resource "aws_launch_template" "launch" {
  image_id      = "ami-036841078a4b68e14"
  instance_type = "t2.micro"

  user_data = <<-EOF
    #!/bin/bash
    echo "Hey there, how are you" > index.html
    nohup busybox httpd -f -p ${var.server_port} &
  EOF


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
  target_group_arns = [aws_lb_target_group.asg.arn]
  health_check_type = "ELB"


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
  security_groups = [aws_security_group.alb.id]
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.lb.arn
  port = 80
  protocol = "HTTP"

  default_action {
    type = "fixed-response"

    fixed_response {
      content_type = "text/plain"
      message_body = "404: page not found"
      status_code = 404
    }
  }
}

resource "aws_security_group" "alb" {
  name = "alb-sg"

  ingress {
    from_port = 80
    to_port = 80
    protocol = "TCP"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_lb_target_group" "asg" {
  name = "tg-alb"
  port = var.server_port
  protocol = "HTTP"
  vpc_id = data.aws_vpc.default.id

  health_check {
    path = "/"
    protocol = "HTTP"
    matcher = "200"
    interval = 15
    timeout = 3
    healthy_threshold = 2
    unhealthy_threshold = 2
  }
}

resource "aws_lb_listener_rule" "asg" {
  listener_arn = aws_lb_listener.http.arn
  priority = 100

  condition {
    path_pattern {
      values = ["*"]
    }
  }

  action {
    type = "forward"
    target_group_arn = aws_lb_target_group.asg.arn
  }
}