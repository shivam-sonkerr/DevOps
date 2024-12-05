resource "aws_db_instance" "default" {
  allocated_storage = 5
  db_name = "mydb"
  instance_class = "db.t4g.micro"
  engine = "mysql"
  engine_version = "8.0.39"
  skip_final_snapshot = true
  username = "maverick"
  password = "learn_db_tf"
}

