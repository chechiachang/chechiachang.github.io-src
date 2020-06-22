---
title: "CRI, OCI, CRI-O"
date: 2018-08-19T18:00:35+08:00
draft: false
---

footer: Che-Chia David Chang, 2018,  [https://github.com/chechiachang](https://github.com/chechiachang)
slidenumbers: true

# CRI, OCI, CRI-O

---

David Chang DevOps @ Mithril
Back-End Developer, Kuberentes admin, DevOps

{{< figure library="1" src="davidchang.jpg" title="" >}}
{{< figure library="1" src="mithril.jpg" title="" >}}

---

### Outline

1. Container Runtime Interface (CRI)
2. Open Container Initiative (OCI) 
3. CRI-O 
4. Kubernetes on CRI-O 

{{< figure library="1" src="cri-o.jpg" title="" >}}
{{< figure library="1" src="kubernetes.png" title="" >}}

--- 

### Trend Kubernetes 

- Kubernetes 1.3 introduced rktnetes 
- Kubernetes 1.5 introduced CRI 
- Kubernetes 1.7 removed pre-CRI Docker / rkt integration
- Currently works Kubelet to use CRI 

- CRI-O: released 1.0.x to match Kubernetes 1.7 

---

### Nomination

CRI-O
- OCI-based implementation of Kubernetes Container Runtime Interface

CRI
- Kubernetes Container Runtime Interface

OCI
- Open Container initiative

---

### Projects with Container Runtime


docker, rkt, LXC/LXD, runC, containerd, OpenVZ, systemd-nspawn, machinectl, qemu-kvm, lkvm...

Kubernetes (before 1.6) native supports
- Docker
- rkt

{{< figure library="1" src="docker-angry.jpg" title="" >}}
{{< figure library="1" src="rkt.jpg" title="" >}}

---

### Container Runtime Interface(CRI)

- Enable Kubernetes to support more runtimes
- Free kubernetes to focus on orchestration from runtime integration
- Consists
  - a protocol buffers and gRPC API
  - libraries, additional specifications and tools

---

### Container Runtime Interface(CRI)

{{< figure library="1" src="containerd.jpg" title="" >}}

---

### CRI api in kubernetes

[https://github.com/kubernetes/kubernetes/
blob/master/pkg/kubelet/apis/
cri/runtime/v1alpha2/api.proto](https://github.com/kubernetes/kubernetes/blob/master/pkg/kubelet/apis/cri/runtime/v1alpha2/api.proto)

---

### CRI runtimes
 
- Docker CRI shim (cri-containerd)
- CoreOS [rktlet](https://github.com/kubernetes-incubator/rktlet)
- [frakti](https://github.com/kubernetes/frakti): hypervisor-based container runtimes
- Intel [Clear container](https://github.com/clearcontainers/runtime)
- OpenStack [kata runtime](https://github.com/kata-containers/runtime)
- [cri-o](http://cri-o.io/)

---

### Open Container Inititive (OCI)

- open governance structure
- container industry standards

- [runtime spec](https://github.com/opencontainers/runtime-spec/blob/master/spec.md) defines configuration, execution environment, and lifecycle of a container
- [image spec](https://github.com/opencontainers/image-spec/blob/master/spec.md) spec on archetecture and OS, filesystem layers and configuration

---

### OCI from aspect of user

- Use all OCI-conplimant container runtime
- Use all OCI-complimant images registries
- Similar UX

https://www.opencontainers.org/blog/2018/06/20/cri-o-how-standards-power-a-container-runtime

---

### CRI-O

- OCI-based implementation of Kubernetes Container Runtime Interface
- Kubernetes incubator project also part of the CNCF
- Dedicated for Kubernetes
- Enable CRI-O plugin to other runtimes
- Available on RHEL, Fedora, Centos, Ubuntu...

http://cri-o.io/

---

### CRI-O vs Docker (containerd)

kubelet -> cri-containerd (shim) -> containerd -> runC -> container
kubelet -> cri-o -> runC -> container

- Lightweight
- Stability
  - built for Kubernetes
  - No cli, image utilities, ...
  - No swarm, mesosphere integration, ...

---

{{< figure library="1" src="cri-o-arch.jpg" title="" >}}

---

### Let's use CRI-O

- [Install cri-o](https://github.com/kubernetes-sigs/cri-o) and dependencies, runC and CNI
- Install [Podman](https://github.com/containers/libpod) 
  - Podman to cri-o as Docker-cli to Docker daemon

```
sudo podman run --name my-golang golang:alpine bash
```

---

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

--- 

### Run Kubernetes on CRI-O 

[Kubespray](https://github.com/kubernetes-incubator/kubespray/blob/master/docs/cri-o.md)
```
kubeadm_enabled: true
...
container_manager: crio
```

[Full cluster](https://github.com/kubernetes-sigs/cri-o/blob/master/kubernetes.md)

```
kubelet --container-runtime-endpoint=unix:///var/run/crio/crio.sock
...
```

---

### References

https://kubernetes.io/blog/2016/12/container-runtime-interface-cri-in-kubernetes/
https://kubernetes.io/blog/2017/11/containerd-container-runtime-options-kubernetes/
Rttps://kubernetes.io/blog/2017/11/containerd-container-runtime-options-kubernetes/
https://xuxinkun.github.io/2017/12/12/docker-oci-runc-and-kubernetes/
https://www.kubernetes.org.cn/1079.html
