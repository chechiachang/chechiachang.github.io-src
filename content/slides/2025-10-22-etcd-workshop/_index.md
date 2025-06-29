---
title: "K8s Summit 2025: Workshop: Get started with Etcd & Kubernetes"
description: "Etcd 是 Kubernetes 的重要元件之一，本次工作坊將帶領觀眾初探 Etcd，包含安裝，設定，以及操作。並藉由本地的 Etcd 來架設一個最簡單的 Kubernetes Cluster。工作坊內容請見投影片"
tags: ["iac", "aws", "terraform", "kubernetes", "etcd"]
categories: ["kubernetes", "workshop"]
date: '2025-06-25T00:45:00Z'
outputs: ["Reveal"]
reveal_hugo:
  custom_theme: "reveal-hugo/themes/robot-lung.css"
  margin: 0.2
  highlight_theme: "color-brewer"
  transition: "slide"
  transition_speed: "fast"
  templates:
    hotpink:
      class: "hotpink"
      background: "#FF4081"
---

### Etcd workshop 行前準備
## （內容準備中）

---

### Etcd workshop 行前準備

本次 workshop 以 hands-on 的方式進行，累積操作經驗為主，講解與說明為輔。觀念內容有準備教材，需要參與者自行閱讀。講師會免費提供 Azure VM 供同學遠端操作使用。

1. 有自己的電腦，可以上網
  1. 選項1: 使用自己的電腦，在 docker 啟動開發環境
  1. 選項2: 使用自己的電腦，遠端連線講師提供的 VM，在VM 中啟動 docker 開發環境
1. 會使用 docker
1. 會使用 python 與 jupyter notebook
1. 會使用 chatgpt.com 協助除錯

---

#### Kubernetes Summit 2025
## Get started with Etcd & Kubernetes
##### 手把手入門 Etcd 與 Kubernetes
##### ~ Che Chia Chang @ [chechia.net](https://chechia.net) ~

---

{{% section %}}

{{< slide content="slides.about-me" >}}
🔽

---

### [DevOpsDay 2025: RAG Workshop](../../slides/2025-06-05-devops-rag-internal-ai)


{{% /section %}}

---

### 大綱

1. docker 啟動 etcd
1. etcdctl 存取 etcd
1. docker 啟動 etcd cluster
1. docker 啟動 k8s control plane
1. kubectl 存取 k8s control plane
1. 維運 k8s 所需的 etcd operation
