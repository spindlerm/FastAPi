

resource "aws_lambda_function" "fast_api_lammbda" {
  function_name = "${var.image_name}-${var.env_name}"
  timeout       = 5 # seconds
  image_uri     = "${data.aws_ecr_repository.repository.repository_url}:${var.image_name}"
  package_type  = "Image"
  role = aws_iam_role.fast_api_lammbda_role.arn

  environment {
    variables = {
      ENVIRONMENT = var.env_name
    }
  }
}


resource "aws_iam_role" "fast_api_lammbda_role" {
  name = "fast_api_lambda-${var.env_name}"

  assume_role_policy = jsonencode({
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_model_policy_attachement" {
  role       = aws_iam_role.fast_api_lammbda_role.name
  policy_arn = aws_iam_policy.lambda_model_policy.arn
}

resource "aws_iam_policy" "lambda_model_policy" {
  name = "my-lambda-model-policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
EOF
}