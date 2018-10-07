---
title: "Kubernetes Container Runtime Interface"
date: 2018-10-06T12:07:00+08:00
lastmod: 2018-10-06T12:07:00+08:00
draft: false
tags: ["kubernetes", "container", "docker", "cri"]
categories: ["kubernetes"]
author: "Che-Chia Chang"

# You can also close(false) or open(true) something for this content.
# P.S. comment can only be closed
# comment: false
# toc: false

# You can also define another contentCopyright. e.g. contentCopyright: "This is another copyright."
contentCopyright: '<a href="https://github.com/gohugoio/hugoBasicExample" rel="noopener" target="_blank">See origin</a>'
# reward: false
mathjax: true

menu:
  main:
    parent: "docs"
    weight: 1
---

# Outline

1. CRI-O
2. Open Container Initiative (OCI)
3. Container Runtime Interface (CRI)
4. Kubernetes on CRI-O

# What is CRI-O

OCI-based implementation of Kubernetes Container Runtime Interface

http://cri-o.io/

# OCI and CRI

Open Container Inititive
- A industrial standard for container

Container Runtime Interface
- Interface of container runtime for Kubelet

# Open Container Initiative

open governance structure (project) for the express purpose of creating open industry standards around container formats and runtime
- formed under the auspices of the Linux Foundation
- Currently has two spec
  - runtime spec
  - image spec 

https://www.opencontainers.org/

# For user

- All OCI con
- Similar UX

https://www.opencontainers.org/blog/2018/06/20/cri-o-how-standards-power-a-container-runtime

# CRI-O

- Interface of container runtime for Kubelet
- Kubernetes 1.6+ introduced CRI
- Pre-CRI Docker integration was removed in 1.7

# CRI-O vs Docker

- OCI-based implementation for Kubernetes
- Build to support Kubernetes runtime (no unessasary features)

# Let's use CRI-O

Podman

Podman to cri-o as Docker-cli to Docker daemon.

[podman](https://github.com/containers/libpod)

[Podman tutorial](https://github.com/containers/libpod/blob/master/docs/tutorials/podman_tutorial.md)

We should able to migrate from any OCI comfortant runtime and registry without pain.

# Run Kubernetes on CRI-O 

Install cri-o

```
sudo add-apt-repository ppa:projectatomic/ppa \
  && sudo apt-get update \
  && sudo apt-get install cri-o-runc
```
https://github.com/kubernetes-sigs/cri-o/blob/master/kubernetes.md

[Minikube](https://github.com/kubernetes/minikube/blob/master/docs/alternative_runtimes.md#using-cri-o)


```bash
minikube start \
  --network-plugin=cni \
  --container-runtime=cri-o

minikube start \
  --network-plugin=cni \
  --extra-config=kubelet.container-runtime=remote \
  --extra-config=kubelet.container-runtime-endpoint=/var/run/crio/crio.sock \
  --extra-config=kubelet.image-service-endpoint=/var/run/crio/crio.sock
```

# References

https://kubernetes.io/blog/2016/12/container-runtime-interface-cri-in-kubernetes/
