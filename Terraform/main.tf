terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "2.16.0"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

resource "docker_image" "alpine" {
  name = "alpine"
  keep_locally = false
}

resource "docker_container" "alpine" {
  image = docker_image.alpine.latest
  name  = "at"
  tty = true
}
