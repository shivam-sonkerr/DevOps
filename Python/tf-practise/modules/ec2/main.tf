resource "aws_instance" "server" {
  count = var.instance_count

  ami = var.ami_id
  instance_type = var.instance_type
  subnet_id = var.subnet_id
  vpc_security_group_ids = var.security_groups

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y httpd
              systemctl start httpd
              systemctl enable httpd
              echo "<h1> Server ${count.index +1 } - ${var.environment} <h1>" > /var/www/html/index.html
              EOF

  tags = merge(var.tags,{
    Name = "${var.environment} - server - ${count.index+1}"
  })

  lifecycle {
    create_before_destroy = true
  }
}
