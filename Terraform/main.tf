terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }

  required_version = ">= 1.3.6"

  backend "s3" {
    region  = "eu-west-2" // also replicated in eu-west-1
    bucket = "355633558229-client-tf-state" 
    key    = "FastApi"
    encrypt = true
  }
}

data "aws_ecr_repository" "repository" {
  name = "${var.ecr_repository_name}"
}
