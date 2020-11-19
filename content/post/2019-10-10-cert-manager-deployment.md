---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/
title: "Cert Manager Deployment on Kubernetes"
subtitle: ""

# Add a summary to display on homepage (optional).
summary: ""

date: 2019-10-10T16:12:10+08:00
draft: false

# Authors. Comma separated list, e.g. `["Bob Smith", "David Jones"]`.
authors: []

# Is this a featured post? (true/false)
featured: false

# Tags and categories
# For example, use `tags: []` for no tags, or the form `tags: ["A Tag", "Another Tag"]` for one or more tags.
tags: ["kubernetes", "cert-manager", "devops"]
categories: ["kubernetes", "cert-manager"]

menu:
  main:
    parent: "Ithelp 鐵人賽"
    weight: 1
---

[2020 It邦幫忙鐵人賽](https://ithelp.ithome.com.tw/2020ironman) 系列文章

這邊改了一些大綱，原本的內容還有一些 kubernetes 的設定，以及 GCP 相關服務的介紹。但既然我們的主題是把東西搬上 k8s 的踩雷旅程，那我們就繼續搬，繼續踩。剩下的時間大概會有四個題目。

- Nginx Ingress (3)
  - [Deploy Nginx Ingress Controller]({{< ref "/post/2019-10-08-kubernetes-nginx-ingress-controller" >}})
  - [Configure Nginx Ingress]({{< ref "/post/2019-10-08-kubernetes-nginx-ingress-config" >}})
- Cert-manager (3)
  - [Deploy cert-manager]({{< ref "/post/2019-10-10-cert-manager-deployment" >}})
  - [How cert-manager work]({{< ref "/post/2019-10-11-cert-manager-how-it-work" >}})
  - [Cert-manager complete workflow]({{< ref "/post/2019-10-12-cert-manager-complete-workflow" >}})
- Kubernetes CRD & Operator-sdk (3)
  - [Introduction about custom resource]({{< ref "/post/2019-10-13-kubernetes-custom-resources-basic">}})
  - [Deployment & Usage]({{< ref "/post/2019-10-13-kubernetes-custom-resources-basic">}})
  - [Deployment & Usage]({{< ref "/post/2019-10-15-kubernetes-custom-resource-with-operator-sdk">}})

由於我比較熟悉 GCP / GKE 的服務，這篇的操作過程都會以 GCP 平台作為範例，不過操作過程大體上是跨平台通用的。

寫文章真的是體力活，覺得我的文章還有參考價值，請左邊幫我點讚按個喜歡，右上角幫我按個追縱，底下歡迎留言討論。給我一點繼續走下去的動力。

對我的文章有興趣，歡迎到我的網站上 [https://chechia.net](https://chechia.net) 閱讀其他技術文章，有任何謬誤也請各方大德直接聯繫我，感激不盡。

![Exausted Cat Face](https://d32l83enj9u8rg.cloudfront.net/wp-content/uploads/iStock-966846550-cat-overheating-simonkr-1-940x470.jpg)

---

# 摘要

* Cert-manager Introduction
* Deploy cert-manager

# 簡介 cert-manager

TLS certificate 管理很重要，但在 kubernetes 上管理 TLS certificates 很麻煩。

以往我們使用 [Let's Encrypt](https://letsencrypt.org/zh-tw/) 提供的免費自動化憑證頒發，搭配 [kube-lego](https://github.com/jetstack/kube-lego) 來自動處理 certificate issuing，然而隨著 kube-lego 已不再更新後，官方建議改使用 [Cert-manager](https://github.com/jetstack/cert-manager/) 來進行 kubernetes 上的憑證自動化管理。

cert-manager 是 kubernetes 原生的憑證管理 controller。是的他的核心也是一個 controller，透過 kubernetes object 定義 desired state，監控集群上的實際狀態，然後根據 resource object 產生憑證。cert-manager 做幾件事情

* 在 kubernetes 上 使用 CRD (Customized Resource Definition) 來定義 certificate issuing 的 desired state
* 向 let's encrypt 取得公開的憑證
* 在 kubernetes 上自動檢查憑證的有效期限，並自動在有效時限內 renew certificate。

# 安裝

官方文件有提供 [詳細步驟](https://docs.cert-manager.io/en/latest/getting-started/install/kubernetes.html) 可以直接使用 release 的 yaml 部屬，也可以透過 helm。

### 使用 yaml 部屬

```
# Create a namespace to run cert-manager in
kubectl create namespace cert-manager

# Disable resource validation on the cert-manager namespace
kubectl label namespace cert-manager certmanager.k8s.io/disable-validation=true
```

開一個獨立的 namespace 來管理 cert-manager resources

取消 namespcae 中的 kubernetes validating webhook。由於 cert-manager 本身就會使用 [ValidatingWebhookConfiguration](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/) 來為 cert-manager 定義的 Issuer, Certificate resource 做 validating。然而這會造成 cert-manager 與 webhook 的循環依賴 (circling dependency)

```
# Install the CustomResourceDefinitions and cert-manager itself
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v0.10.1/cert-manager.yaml
```


```
# Install the CustomResourceDefinitions and cert-manager itself
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v0.10.1/cert-manager.yaml
```

這個 yaml 裡面還有幾個元件

* Cluster Role-bindings
* CustomResourceDefinition
  * certificaterequests.certmanager.k8s.io
  * certificates.certmanager.k8s.io
  * challenges.certmanager.k8s.io
  * clusterissuers.certmanager.k8s.io
  * issuers.certmanager.k8s.io
  * orders.certmanager.k8s.io

這些元件的細節，留待運作原理分析時再詳解。

### helm deployment

這邊也附上使用 helm 安裝的步驟

```
#!/bin/bash

# Install the CustomResourceDefinition resources separately
kubectl apply -f https://raw.githubusercontent.com/jetstack/cert-manager/release-0.10/deploy/manifests/00-crds.yaml

# Create the namespace for cert-manager
kubectl create namespace cert-manager

# Label the cert-manager namespace to disable resource validation
kubectl label namespace cert-manager certmanager.k8s.io/disable-validation=true

# Add the Jetstack Helm repository
helm repo add jetstack https://charts.jetstack.io

# Update your local Helm chart repository cache
helm repo update

# Install the cert-manager Helm chart
helm install \
  --name cert-manager \
  --namespace cert-manager \
  --version v0.10.1 \
  jetstack/cert-managerNAMESPACE=cert-manager
```

部屬完檢查一下

```
kubectl get pods --namespace cert-manager

NAME                                       READY   STATUS    RESTARTS   AGE
cert-manager-5c6866597-zw7kh               1/1     Running   0          2m
cert-manager-cainjector-577f6d9fd7-tr77l   1/1     Running   0          2m
cert-manager-webhook-787858fcdb-nlzsq      1/1     Running   0          2m
```

這邊部屬完，會獲得完整的 cert-manager 與 cert-manager CRD，但 certificate 的 desired state object 還沒部屬。也就是關於我們要如何 issue certificate 的相關描述，都還沒有 deploy， cert-manager 自然不會工作。關於 issuing resources configuration，我們下次再聊。
