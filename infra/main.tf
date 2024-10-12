provider "google" {
  credentials = var.gcp_credentials_file  # This is the path to the service account key  
  project = "football-data-warehouse"
  region  = "us-central1"
}

resource "google_storage_bucket" "data_bucket" {
  name          = "football-data-warehouse"
  location      = "US"
}

