---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Cert Manager Complete Workflow"
subtitle: ""
summary: ""
authors: []
tags: ["kubernetes", "cert-manager", "devops"]
categories: ["kubernetes", "cert-manager"]
date: 2019-10-12T17:41:25+08:00
lastmod: 2019-10-12T17:41:25+08:00
featured: false
draft: false

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

# Recap

昨天我們實際使用 cert-manager，為 nginx ingress controller 產生 certificates，過程中我們做了幾件事

* 設置 Let's Encript prod site 的 Issuer
* 設置 certificates.certmanager.k8s.io 資源來定義 certificate 的取得方式
* 或是在 ingress 中配置 tls，讓 cert-manager 自動透過 ingress-shim 產生 certifcates.cert-manager，並且產生 certificate

以上是使用 cert-manager 產生 certificate 的基本操作，剩下的是由 cert-manager 完成。實際上 cert-manager 在產生出 certificate 之前還做了很多事情，我們今天就詳細走過完整流程，藉此了解 cert-manager 配合 issuing certificate 的流程

使用者設置 Issuer

使用者設定 certificate -> cert-manager 根據 certificate -> 產生 certificate

# CertificateRequests

certificaterequests.certmanager 是 cert-manager 產生 certificate 過程中會使用的資源，不是設計來讓人類操作的資源。

當 cert-manager 監測到 certificate 產生後，會產生 certificaterequests.certmanager.k8s.io 資源，來向 issuer request certificate，這個過程與使用其他客戶端 (ex. certbot) 來向 3rd party CA server request certificate 時的內容相同，只是這邊我們使用 kubernetes resource 來定義。

包含的 certificate request，會以 pem encoded 的形式，再變成 base64 encoded 存放在 resource 中。這個 pem key 也會從到遠方的 CA sercer (Let's Encrypt prod) 來 request certificate

如果 issuance 成功，certificaterequest 資源應該會被 cert-manager 吃掉，不會被人類看到。

一個 certificaterequests.certmanager 大概長這樣

```
apiVersion: cert-manager.io/v1alpha2
kind: CertificateRequest
metadata:
  name: my-ca-cr
spec:
  csr: LS0tLS1CRUdJTiBDRVJUSUZJQ0FUR
  ..................................
  LQo=
  isCA: false
  duraton: 90d
  issuerRef:
    name: ca-issuer
    # We can reference ClusterIssuers by changing the kind here.
    # The default value is Issuer (i.e. a locally namespaced Issuer)
    kind: Issuer
    group: cert-manager.io
```

這個 certificaterequests.certmanager 會讓 cert-manager 嘗試向 Issuer (lets-encrypt-prod) request certificate。

# Order

orders.certmanager.k8s.io 被 ACME 的 Issuer 使用，用來管理 signed TLD certificate 的 ACME order，這個 resource 也是 cert-manager 自行產生管理的 resource，不需要人類來更改。

當一個 certificates.certmanager 產生，且需要使勇 ACME isser 時，certmanager 會產生 orders.certmanager ，來取得 certificate。

# Challenges

challenges.certmanager 資源是 ACME Issuer 管理 issuing lifecycle 時，用來完成單一個 DNS name/identifier authorization 時所使用的。用來確定 issue certiticate 的客戶端真的是 DNS name 的擁有者。

當 cert-manager 產生 order 時，order controller 接到 order ，就會為每一個需要 DNS certificate 的 DNSname ，產生 challenges.certmanager。

這段也是 order controller 自動產生，並不需要使用者參與。

# ACME certificate issuing

user -> 設定好 issuers.certmanager

user -> 產生 certificates.certmanager -> 選擇 Issuer ->  

cert-manager -> 產生 certificaterequest -> 

cert-manager 根據 certiticfates.certmanager 產生 orders.certmanager ->

order controller 根據 order ，並且跟每一個 DNS name target，產生一個 challenges.certmanager 

challenges.certmanager 產生後，會開啟這個 DNS name challenge 的 lifecycle

* challenges 狀態為 queued for processing，在佇列中等待，
* 如果沒有別的 chellenges 在進行，challenges 狀態變成 scheduled，這樣可以避免多個 DNS challenge 同時發生，或是相同名稱的 DNS challenge 重複
* challenges 與遠端的 ACME server 'synced' 當前的狀態，是否 valid
  * 如果 ACME 回應這個 DNS name 的 challenge 還是有效的，則直接把 challenges 的狀態改成 valid，然後移出排程佇列。
  * 如果 challenges 狀態仍然為 pending，challenge controller 會依照設定 present 這個 challenge，使用 HTTP01 或是 DNS01，challenges 被標記為 presented
  * challenges 先執行 self check，確定 challenge 狀態已經傳播給 dns servers，如果 self check 失敗，則會依照 interval retry
  * ACME authorization 關聯到 challenge

cert-manager 處理 'scheduled' challenges.certmanager -> ACME challenge


