---
title: "Kubernetes Nginx Ingress Controller Config"
subtitle: ""

# Add a summary to display on homepage (optional).
summary: ""

date: 2019-10-08T8:12:10+08:00
draft: false

# Authors. Comma separated list, e.g. `["Bob Smith", "David Jones"]`.
authors: []

# Is this a featured post? (true/false)
featured: false

# Tags and categories
# For example, use `tags: []` for no tags, or the form `tags: ["A Tag", "Another Tag"]` for one or more tags.
tags: ["鐵人賽2019", "kubernetes", "nginx", "ingress"]
categories: ["kubernetes", "nginx"]
---

[2020 It邦幫忙鐵人賽](https://ithelp.ithome.com.tw/2020ironman) 系列文章

這邊改了一些大綱，原本的內容還有一些 kubernetes 的設定，以及 GCP 相關服務的介紹。但既然我們的主題是把東西搬上 k8s 的踩雷旅程，那我們就繼續搬，繼續踩。剩下的時間大概會有四個題目。

- Nginx Ingress (3)
  - [Deploy Nginx Ingress Controller]({{< ref "/posts/2019-10-08-kubernetes-nginx-ingress-controller" >}})
  - [Configure Nginx Ingress]({{< ref "/posts/2019-10-08-kubernetes-nginx-ingress-config" >}})
- Cert-manager (3)
  - [Deploy cert-manager]({{< ref "/posts/2019-10-10-cert-manager-deployment" >}})
  - [How cert-manager work]({{< ref "/posts/2019-10-11-cert-manager-how-it-work" >}})
  - [Cert-manager complete workflow]({{< ref "/posts/2019-10-12-cert-manager-complete-workflow" >}})
- Kubernetes CRD & Operator-sdk (3)
  - [Introduction about custom resource]({{< ref "/posts/2019-10-13-kubernetes-custom-resources-basic">}})
  - [Deployment & Usage]({{< ref "/posts/2019-10-13-kubernetes-custom-resources-basic">}})
  - [Deployment & Usage]({{< ref "/posts/2019-10-15-kubernetes-custom-resource-with-operator-sdk">}})

由於我比較熟悉 GCP / GKE 的服務，這篇的操作過程都會以 GCP 平台作為範例，不過操作過程大體上是跨平台通用的。

寫文章真的是體力活，覺得我的文章還有參考價值，請左邊幫我點讚按個喜歡，右上角幫我按個追縱，底下歡迎留言討論。給我一點繼續走下去的動力。

對我的文章有興趣，歡迎到我的網站上 [https://chechia.net](https://chechia.net) 閱讀其他技術文章，有任何謬誤也請各方大德直接聯繫我，感激不盡。

![Exausted Cat Face](https://d32l83enj9u8rg.cloudfront.net/wp-content/uploads/iStock-966846550-cat-overheating-simonkr-1-940x470.jpg)

---

# 摘要

* Nginx Ingress Controller 運作原理
* 設定 Nginx Ingress Controller

# 運作原理

昨天講完 nginx ingress controller 部屬，今天來談談 controller 是如何運作的。

* Nginx 使用 config file (nginx.conf) 做全域設定，為了讓 nginx 能隨 config file 更新，controller 要偵測 config file 變更，並且 reload nginx
* 針對 upstream (後端 app 的 endpoint) 變更，使用 lua-nginx-module 來更新。因為 kubernetes 上，service 後的服務常常會動態的變更，scaling，但 endpint ip list 又需要更新到 nginx，所以使用 lua 額外處理

在 kubernetes 上要如何做到上述兩件事呢?

* 一般 controller 都使用同步 loop 來檢查 current state 是否與 desired state
* desired state 使用 k8s object 描述，例如 ingress, services, configmap 等等 object
* Nginx ingress controller 這邊使用的是 client-go 中的 Kubernetes Informer 的 [SharedInformer](https://godoc.org/k8s.io/client-go/informers#SharedInformerFactory)，可以根據 object 的更新執行 callback
* 由於無法檢查每一次的 object 更動，是否對 config 產生影響，這邊直接每次更動都產生全新的 model
* 如果新產生的 model 與現有相同，就跳過 reload
* 如果 model 只影響 endpoint，使用 nginx 內部的 lua handler 產生新的 endpoint list，來避免因為 upstream 服務變更造成的頻繁 reload
* 如果新 Model 影響不只 endpoint，則取代現有 model，然後觸發 reload


具體會觸發 reload 的事件，[請見官方文件](https://kubernetes.github.io/ingress-nginx/how-it-works/#when-a-reload-is-required)

除了監測 objects，build model，觸發 reload，之前 controller 還會將 ingress 送到 [kubernetes validating admission webhook server](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#validatingadmissionwebhook) 做驗證，避免描述 desired state 的 ingress 有 syntax error，導致整個 controller 爆炸。

# Configuration

要透過 controller 更改 nginx 設定，有以下三種方式

* 更改 configmap，對全域的 controller 設定
* 更改 ingress 上的 annotation，這些 annotation 針對獨立 ingress 生效
* 有更深入的客製化，是上述兩者達不到或尚未實作，可以使用 [Custom Template](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/custom-template/) 來做到，把 nginx.tmpl mount 進 controller

# Configmap 

由於把全域設定放到 configmap 上，nginx ingress controller 非常好調度與擴展，[controller 官方說明文件](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/configmap/) 除了列出目前已經支援的設定外，也直接附上 nginx 官方的文件說明連結，讓使用者查詢時方便比對。

當需要更改需求，可以 google nginx 的關鍵字，找到 nginx 上設定的功能選項後，來 controller 的文件，找看看目前是否已經支援。有時候有需要對照 nginx 官方文件，來正確設定 controller。

# Annotation

有很多 Nginx 的設定是根據 ingress 不同而有調整，例如針對這個 ingress 做白名單，設定 session，設定 ssl 等等，這些針對特定 ingress 所做的設定，可以直接寫在 [ingress annotation](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/) 裡面。

例如下面這個 Ingress

```
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress-nginx
  annotations:
    kubernetes.io/ingress.class: nginx
    kubernetes.io/tls-acme: 'true'
    certmanager.k8s.io/cluster-issuer: letsencrypt-prod
    kubernetes.io/ingress.allow-http: "true"
    ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/whitelist-source-range: "34.35.36.37"
    nginx.ingress.kubernetes.io/proxy-body-size: "20m"
    ingress.kubernetes.io/proxy-body-size: "20m"
    # https://github.com/Shopify/ingress/blob/master/docs/user-guide/nginx-configuration/annotations.md#custom-nginx-upstream-hashing
    nginx.ingress.kubernetes.io/load-balance: "ip_hash"
    # https://kubernetes.github.io/ingress-nginx/examples/affinity/cookie/
    nginx.org/server-snippets: gzip on;
    nginx.ingress.kubernetes.io/affinity: "cookie"
    nginx.ingress.kubernetes.io/session-cookie-name: "route"
    nginx.ingress.kubernetes.io/session-cookie-hash: "sha1"
    nginx.ingress.kubernetes.io/session-cookie-expires: "3600"
    nginx.ingress.kubernetes.io/session-cookie-max-age: "3600"
```

* nginx.ingress.kubernetes.io
  * whitelist-source-range: 只允許白名單 ip
  * load-balance: "ip_hash": 更改預設 round_robin 的 [load balance](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/configmap/#load-balance)，為了做 session cookie
  *  affinity: "cookie": 設定 upstream 的 [session affinity](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#session-affinity)
  *  session-cookie-name: "route"
  *  session-cookie-hash: "sha1"
  *  session-cookie-expires: "3600"
  *  session-cookie-max-age: "3600"


如果後端 server 有 session 需求，希望相同 source ip 來的 request 能持續到相同的 endpoint。才做了以上設定。

# helm configuration

helm 的 configuration 也是重要的設定，這裡在安裝時決定了 nginx ingress controller 的 topology、replicas、resource、k8s runtime 設定如 healthz & readiness、其實都會影響 nginx 具體的設定。這部分就會有很多考量。有機會我們再來分享。
