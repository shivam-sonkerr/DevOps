output "mysql_rds_details" {
  value = aws_db_instance.default.db_name
}

output "mysql_rds_address" {
  value = aws_db_instance.default.address
}

output "mysql_rds_arn" {
  value = aws_db_instance.default.arn
}