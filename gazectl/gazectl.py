#!/usr/bin/env python

import docker

client = docker.from_env()

client.containers.run("ubuntu:latest", "echo hello world")
