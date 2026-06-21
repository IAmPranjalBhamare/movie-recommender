variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "container_port" {
  description = "Container port"
  type        = number
  default     = 5000
}

variable "container_cpu" {
  description = "Container CPU units"
  type        = string
  default     = "256"
}

variable "container_memory" {
  description = "Container memory in MB"
  type        = string
  default     = "512"
}
