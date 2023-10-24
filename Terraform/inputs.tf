variable "env_name" {
  type = string
  description = "The Lambda Environment Name"
  default = "dev"
}

variable "image_name" {
  type = string
  description = "The name of the Lambda container image"
  default = "fap"
}

variable "ecr_repository_name" {
  type = string
  description = "The name of the ECR repository"
  default = "image-registry"
}

