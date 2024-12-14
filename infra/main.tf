# AWS Provider (make sure this is at the top of your file)
provider "aws" {
  region = "us-east-1"  # replace with your preferred region
}

# S3 Bucket Resource
resource "aws_s3_bucket" "football_data_warehouse" {
  bucket = "football-data-warehouse"
}

# Server-side Encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "football_data_warehouse_encryption" {
  bucket = aws_s3_bucket.football_data_warehouse.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Access Control (Public Access Block)
resource "aws_s3_bucket_public_access_block" "football_data_warehouse_public_access" {
  bucket = aws_s3_bucket.football_data_warehouse.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
