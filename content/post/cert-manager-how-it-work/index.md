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

cert-manager 有支援幾種的 issuer type

* CA: 使用 x509 keypair 產生certificate，存在 kubernetes secret
* Self signed: 自簽 certificate
* ACME: 從 ACME (ex. Let's Encrypt) server 取得 ceritificate
* Vault: 從 Vault PKI backend 頒發 certificate
* Venafi: Venafi Cloud

# Certificate

有了簽發憑證的單位，接下來要定義如何取得 certificate。certificates.certmanager.k8s.io 是 CRD，用來告訴 cert-manager 要如何取得 certificate

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

# 配合 Ingress 設置 tls

有上述的設定，接下來可以請求 tls certificate

記得我們上篇 Nginx Ingress Controller 提到的 ingreess 設定嗎？這邊準備了一個適合配合 nginx ingress 使用的 tls 設定

```
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: my-nginx-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/issuer: "letsencrypt-prod"

spec:
  tls:
  - hosts:
    - foo.example.com
    secretName: my-nginx-ingrss-tls
  rules:
  - host: foo.example.com
    http:
      paths:
      - path: /
        backend:
          serviceName: chechiachang-backend
          servicePort: 80
```

這個 ingress apply 後，就會根據 spec.tls 的 hosts 設定，自動產生一個 certificate.certmanager 資源，並在這個資源使用 letsencryp-prod。

不用我們手動 apply 新的 ceritificate，這邊是 cert-manager 使用了 annotation 來觸發 [Ingress-shim](https://docs.cert-manager.io/en/latest/tasks/issuing-certificates/ingress-shim.html)，簡單來說，當 ingress 上有使用 cert-manager.io 的 annotation 時，cert-manager 就會根據 ingress 設定內容，抽出 spec.tls 與 isuer annotation，來產生同名的 certificates.certmanager，這個 certificateas.certmanager 會觸發接下的 certificate 頒發需求。

只要部署 Issuer 與 Ingress 就可以自動產生 certificate。當然，希望手動 apply certificates.certmanager 也是行得通。

把產生了 certificate.certmanager 拉出來看
 
```
kubectl describe certificate my-nginx-ingress

 Name:         my-nginx-ingress
 Namespace:    default
 API Version:  cert-manager.io/v1alpha2
 Kind:         Certificate
 Metadata:
   Cluster Name:
   Creation Timestamp:  2019-10-10T17:58:37Z
   Generation:          0
   Owner References:
     API Version:           extensions/v1beta1
     Block Owner Deletion:  true
     Controller:            true
     Kind:                  Ingress
     Name:                  my-nginx-ingress
   Resource Version:        9295
 Spec:
   Dns Names:
     example.your-domain.com
   Issuer Ref:
     Kind:       Issuer
     Name:       letsencrypt-prod
   Secret Name:  my-nginx-ingress-tls
 Status:
   Acme:
     Order:
       URL:  https://acme-prod-v02.api.letsencrypt.org/acme/order/7374163/13665676
   Conditions:
     Last Transition Time:  2019-10-10T18:05:57Z
     Message:               Certificate issued successfully
     Reason:                CertIssued
     Status:                True
     Type:                  Ready
 Events:
   Type     Reason          Age                From          Message
   ----     ------          ----               ----          -------
   Normal   CreateOrder     1d                 cert-manager  Created new ACME order, attempting validation...
   Normal   DomainVerified  1d                 cert-manager  Domain "foo.example.com" verified with "http-01" validation
   Normal   IssueCert       1d                 cert-manager  Issuing certificate...
   Normal   CertObtained    1d                 cert-manager  Obtained certificate from ACME server
   Normal   CertIssued      1d                 cert-manager  Certificate issued Successfully
```

把 certificate 從 secret 撈出來看

```
$ kubectl describe secret my-nginx-ingress-tls

Name:         my-nginx-ingress-tls
Namespace:    default
Labels:       cert-manager.io/certificate-name=my-nginx-ingrsss-tls
Annotations:  cert-manager.io/alt-names=foo.example.com
              cert-manager.io/common-name=foo.example.com
              cert-manager.io/issuer-kind=Issuer
              cert-manager.io/issuer-name=letsencrypt-prod

Type:  kubernetes.io/tls

Data
====
tls.crt:  3566 bytes
tls.key:  1675 bytes
```

如此便可以透過 ingress 設定 nginx 使用 https

# 小結

 * 了解 *.certmanager.k8s.io CRD 定義與意義
 * 設定 Issuer 與 certificate
 * 透過 ingress-shim 直接部署 ingress 來產生 certificate
