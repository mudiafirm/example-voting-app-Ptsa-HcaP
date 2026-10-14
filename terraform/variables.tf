variable "project_name" {
  description = "Name of the capstone project"
  type        = string
  default     = "voting-app-capstone"
}

variable "instance_type" {
  description = "EC2 instance type for the learning server"
  type        = string
  default     = "t3.small"
}

variable "admin_cidr" {
  description = "Your public IPv4 address with /32 for SSH access"
  type        = string
  sensitive   = true
}
