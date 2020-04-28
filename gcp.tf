variable "gcp_key_file_location" {}
variable "username" {}
variable "project_name" {}
variable "node_count" {}
variable "private_ssh_key_location" {}
variable "public_ssh_key_location" {}
variable "repository_name" {}
variable "preemptible" {}

provider "google" {
  credentials = var.gcp_key_file_location
  project     = var.project_name
  region      = "us-east1"
}

resource "google_container_cluster" "primary" {
  name     = "my-gke-cluster"
  location = "us-east1"

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count       = 1

  master_auth {
    username = ""
    password = ""

    client_certificate_config {
      issue_client_certificate = false
    }
  }

  cluster_autoscaling {
    enabled = "true"
    resource_limits {
      resource_type = "cpu"
      minimum = 8
      maximum = 128
    }
    resource_limits {
      resource_type = "memory"
      minimum = 51200 
      maximum = 102400
    }

  }
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "my-node-pool"
  location   = "us-east1"
  cluster    = google_container_cluster.primary.name
  node_count = 1

  node_config {
    machine_type = "n1-standard-1"

    metadata = {
      disable-legacy-endpoints = "true"
    }

    oauth_scopes = [
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]
  }
}
