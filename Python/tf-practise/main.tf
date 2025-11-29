provider "aws" {
  region = var.aws_region
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners = ["amazon"]

  filter {
    name = "architecture"
    values = ["x86_64"]
  }
}

#VPC

resource "aws_vpc" "learn" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support = true

  tags = merge(var.common_tags, {
    Name = "${var.environment}-vpc"
    Environment = var.environment
  })
}


#Subnet
resource "aws_subnet" "public" {
  vpc_id = aws_vpc.learn.id
  cidr_block = "10.0.0.0/24"
  map_public_ip_on_launch = true
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = merge (var.common_tags,{
    Name = "${var.environment}-public-subnet"
  })
}

#Data source for AZ's

data "aws_availability_zones" "available"{
  state = "available"
}

#Internet Gateway

resource "aws_internet_gateway" "learn" {
  vpc_id = aws_vpc.learn.id
  tags = merge(var.common_tags,{
    Name = "${var.environment}-igw"
  })
}

#Route Table

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.learn.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.learn.id
  }

  tags = merge(var.common_tags,{
    Name = "${var.environment}-public-rt"
  })
}

resource "aws_route_table_association" "public" {
  subnet_id = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}


resource "aws_security_group" "ec2" {
  name = "${var.environment}-ec2-sg"
  description = "Allow HTTP and SSH"
  vpc_id = aws_vpc.learn.id

  ingress{
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = var.common_tags
}

module "web_servers" {
  source = "./modules/ec2"

  instance_count = var.instance_count
  instance_type = var.instance_type
  ami_id = data.aws_ami.amazon_linux.id
  subnet_id = aws_subnet.public.id
  security_groups = [aws_security_group.ec2.id]
  environment = var.environment
  tags = var.common_tags

}
