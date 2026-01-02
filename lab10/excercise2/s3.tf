# s3.tf

resource "random_id" "bucket_suffix" {
  count       = length(var.regions)
  byte_length = 4
}

# S3_US_EAST_1

resource "aws_s3_bucket" "s3_us_east_1" {
  bucket = "${var.bucket_name_prefix}-${var.regions[0]}${random_id.bucket_suffix[0].hex}"
}

resource "aws_s3_bucket_versioning" "s3_us_east_1" {
  bucket = aws_s3_bucket.s3_us_east_1.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "s3_us_east_1" {
  bucket = aws_s3_bucket.s3_us_east_1.id

  rule {
    id     = "transition-to-glacier"
    status = "Enabled"

    transition {
      days          = 90
      storage_class = "GLACIER_IR"
    }
  }
}

# S3_US_WEST_2

resource "aws_s3_bucket" "s3_us_west_2" {
  bucket = "${var.bucket_name_prefix}-${var.regions[1]}${random_id.bucket_suffix[1].hex}"
}

resource "aws_s3_bucket_versioning" "s3_us_west_2" {
  bucket = aws_s3_bucket.s3_us_west_2.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "s3_us_west_2" {
  bucket = aws_s3_bucket.s3_us_west_2.id

  rule {
    id     = "transition-to-glacier"
    status = "Enabled"

    transition {
      days          = 90
      storage_class = "GLACIER_IR"
    }
  }
}

