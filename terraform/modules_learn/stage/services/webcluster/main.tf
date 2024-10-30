module "webserver" {
source = "../../../modules/services/webcluster/"

cluster_name = "webserver-stage"
db_remote_state_bucket = "learning-s3-and-tf"
db_remote_state_key = "stage/data-stores/mysql/terraform.tfstate"
}
