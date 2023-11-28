#!/bin/bash

podman pull docker.io/library/emqx
podman pull docker.io/timescale/timescaledb:latest-pg13
podman pull docker.io/grafana/grafana:latest
