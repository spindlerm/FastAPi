cd h:\Terraform
terraform destroy -auto-approve
cd h:\fap
docker build . -t fap:latest
aws ecr get-login-password | docker login --username AWS --password-stdin 355633558229.dkr.ecr.eu-west-2.amazonaws.com/image-registry
aws ecr batch-delete-image --repository-name image-registry --image-ids imageTag=fap
docker tag fap:latest 355633558229.dkr.ecr.eu-west-2.amazonaws.com/image-registry:fap
docker push 355633558229.dkr.ecr.eu-west-2.amazonaws.com/image-registry:fap
cd h:\Terraform
terraform apply -auto-approve