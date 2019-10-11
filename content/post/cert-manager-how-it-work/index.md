---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Cert Manager How It Work"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2019-10-11T11:24:34+08:00
lastmod: 2019-10-11T11:24:34+08:00
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: false

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects: []
---

[2020 It邦幫忙鐵人賽](https://ithelp.ithome.com.tw/2020ironman) 系列文章

這邊改了一些大綱，原本的內容還有一些 kubernetes 的設定，以及 GCP 相關服務的介紹。但既然我們的主題是把東西搬上 k8s 的踩雷旅程，那我們就繼續搬，繼續踩。剩下的時間大概會有四個題目。

- Nginx Ingress Controller
- Cert-manager
- Jenkin-x on Kubernetes
- Kubernetes CRD & Operator-sdk

由於我比較熟悉 GCP / GKE 的服務，這篇的操作過程都會以 GCP 平台作為範例，不過操作過程大體上是跨平台通用的。

寫文章真的是體力活，覺得我的文章還有參考價值，請左邊幫我點讚按個喜歡，右上角幫我按個追縱，底下歡迎留言討論。給我一點繼續走下去的動力。

對我的文章有興趣，歡迎到我的網站上 [https://chechiachang.github.io](https://chechiachang.github.io) 閱讀其他技術文章，有任何謬誤也請各方大德直接聯繫我，感激不盡。

![Exausted Cat Face](https://d32l83enj9u8rg.cloudfront.net/wp-content/uploads/iStock-966846550-cat-overheating-simonkr-1-940x470.jpg)

---

今天我們來實際使用 cert-manager，為 nginx ingress controller 產生 certificates with ACME Issuer

# CA Terminology

先把實際執行 CA 簽發的名詞定義一下，以免跟 cert-manager 的資源搞混

* Certificate: 憑證，x509 certificate，cert-manager 自動管理的目標，透過 let's encript 取得的 x509 certificates
* CA (Certificate Authority): issue signed certificate 的機構
* issue: 頒發，指 CA 產生 certificate 與 key (今天的範例格式是 .crt 與 .key)
* Sign vs self-signed: 簽核，自己簽核，使用信任的 CA issue certificate，或是使用自己產生的 CA self-sign，然後把 CA 加到可以被信任的 CA 清單中。

Let's Encript CA issues signed certificates

Kubernetes in-cluster CA issues self-signed certificates

cert-manager 的 CRD 資源，使用來描述 cert-manager 如何執行上述操作，CRD 底下都會加上 ``*.certmanager.k8s.io` 方便辨識。

# 設定 Issuer

Issuer 要怎麼翻成中文XD，憑證頒發機構？

總之在開始簽發 certificates 前，要先定義 issuers.certmanager.k8s.io ，代表一個能簽發 certificate CA，例如 Let's Encript，或是 kubernetes 內部也有內部使用的憑證簽發，放在 secrets 中。

這些 Issuer 會讓 certificates.certmanager.k8s.i8o 使用，定義如何取得 certificate 時，選擇 Issuer。

cert-manager 上可以定義單一 namespace 的 issuers.certmanager 與集群都可使用的 clusterissuers.certmanager

有了簽發憑證的單位，接下來要定義如何取得 certificate

# Certificate

certificates.certmanager.k8s.io 是 CRD，用來告訴 cert-manager 要如何取得 certificate

[certifcates.certmanager.k8s.io](https://docs.cert-manager.io/en/latest/reference/certificates.html#certificates) 提供了簡單範例

```
apiVersion: cert-manager.io/v1alpha2
kind: Certificate
metadata:
  name: acme-crt
spec:
  secretName: acme-crt-secret
  duration: 90d
  renewBefore: 30d
  dnsNames:
  - foo.example.com
  - bar.example.com
  acme:
    config:
    - http01:
        ingressClass: nginx
      domains:
      - foo.example.com
      - bar.example.com
  issuerRef:
    name: letsencrypt-prod
    # We can reference ClusterIssuers by changing the kind here.
    # The default value is Issuer (i.e. a locally namespaced Issuer)
    kind: Issuer
```

上面這個 certificate.certmanger 告訴 cert-manager

* 針對 foo.example.com 與 bar.example.com 兩個 domainsc
* 使用 letsencript-prd Issuer 去取得 certificate key pair
* 成功後把 ceritifcate 與 key 存在 secret/acme-crt-secret 中(以 tls.key, tls.crt 的形式)
* 與 certificate.certmanager 都放在相同 namespace 中，產生 certificate.certmanager 的時候要注意才不會找不到 secret
* 這邊指定了 certificate 的有效期間與 renew 時間 (預設值)，有需要可以更改



* certificaterequests.certmanager.k8s.io 
  * challenges.certmanager.k8s.io
  * clusterissuers.certmanager.k8s.io
  * issuers.certmanager.k8s.io
  * orders.certmanager.k8s.io
