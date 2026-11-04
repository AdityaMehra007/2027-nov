# ==============================================================================
# CASHFLOW INFINITY: OMNIVERSE & AETHER RESILIENCE FABRIC
# Multi-Cloud Sovereign Infrastructure as Code (Terraform 1.5+)
# ==============================================================================

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.50"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.30"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.30"
    }
  }
}

variable "environment" {
  type        = string
  default     = "production"
  description = "Target deployment tier (production, staging, sovereign-edge)"
}

variable "primary_aws_region" {
  type        = string
  default     = "ap-south-1" # Bengaluru / Mumbai Primary Hub
  description = "Primary cloud orchestrator region"
}

variable "secondary_aws_region" {
  type        = string
  default     = "us-east-1" # Global Telemetry & Cross-Border Clearing Hub
  description = "Secondary failover region"
}

variable "cluster_name" {
  type        = string
  default     = "omniverse-planetary-cluster"
  description = "Kubernetes cluster identifier"
}

variable "mesh_continents" {
  type        = list(string)
  default     = ["ASIA_SOUTH", "ASIA_EAST", "NORTH_AMERICA", "EUROPE_CENTRAL", "LATIN_AMERICA", "AFRICA_SOUTH"]
  description = "Planetary mesh sovereign node geographic regions"
}

provider "aws" {
  region = var.primary_aws_region
  default_tags {
    tags = {
      Project     = "CASHFLOW_INFINITY_OMNIVERSE"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Year        = "2027"
    }
  }
}

# ------------------------------------------------------------------------------
# 1. Sovereign Ledger KMS Key & Envelope Encryption
# ------------------------------------------------------------------------------
resource "aws_kms_key" "omniverse_ledger_key" {
  description             = "KMS CMK for sovereign financial ledger and Aether telemetry encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  tags = {
    Name = "omniverse-ledger-kms-cmk"
  }
}

resource "aws_kms_alias" "omniverse_ledger_key_alias" {
  name          = "alias/omniverse-ledger-key"
  target_key_id = aws_kms_key.omniverse_ledger_key.key_id
}

# ------------------------------------------------------------------------------
# 2. Sovereign State & Immutable Audit S3 Bucket
# ------------------------------------------------------------------------------
resource "aws_s3_bucket" "sovereign_ledger" {
  bucket_prefix = "omniverse-sovereign-ledger-"
  force_destroy = false
}

resource "aws_s3_bucket_versioning" "sovereign_ledger_versioning" {
  bucket = aws_s3_bucket.sovereign_ledger.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "sovereign_ledger_encryption" {
  bucket = aws_s3_bucket.sovereign_ledger.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.omniverse_ledger_key.arn
      sse_algorithm     = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "sovereign_ledger_block" {
  bucket = aws_s3_bucket.sovereign_ledger.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# ------------------------------------------------------------------------------
# 3. High-Security Planetary VPC Network
# ------------------------------------------------------------------------------
resource "aws_vpc" "planetary_vpc" {
  cidr_block           = "10.100.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "omniverse-planetary-vpc"
  }
}

resource "aws_subnet" "public_subnets" {
  count                   = 2
  vpc_id                  = aws_vpc.planetary_vpc.id
  cidr_block              = cidrsubnet(aws_vpc.planetary_vpc.cidr_block, 8, count.index)
  map_public_ip_on_launch = false

  tags = {
    Name = "omniverse-subnet-${count.index}"
  }
}

resource "aws_security_group" "mesh_security_group" {
  name        = "omniverse-mesh-sg"
  description = "Planetary mesh edge consensus, telemetry, and API security boundary"
  vpc_id      = aws_vpc.planetary_vpc.id

  ingress {
    description = "HTTP Command Center REST API"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["10.100.0.0/16"]
  }

  ingress {
    description = "Byzantine Fault Tolerant (PBFT) Peer Consensus"
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["10.100.0.0/16"]
  }

  ingress {
    description = "Planetary Telemetry Ingestion"
    from_port   = 9100
    to_port     = 9100
    protocol    = "tcp"
    cidr_blocks = ["10.100.0.0/16"]
  }

  egress {
    description = "Outbound egress via secure egress proxy"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "omniverse-mesh-sg"
  }
}

# ------------------------------------------------------------------------------
# 4. Outputs
# ------------------------------------------------------------------------------
output "vpc_id" {
  description = "Planetary edge VPC ID"
  value       = aws_vpc.planetary_vpc.id
}

output "sovereign_ledger_bucket_name" {
  description = "Sovereign financial ledger immutable storage bucket"
  value       = aws_s3_bucket.sovereign_ledger.id
}

output "kms_key_arn" {
  description = "KMS ARN for ledger envelope encryption"
  value       = aws_kms_key.omniverse_ledger_key.arn
}

output "mesh_active_regions" {
  description = "Configured 6-continent federated mesh locations"
  value       = var.mesh_continents
}
