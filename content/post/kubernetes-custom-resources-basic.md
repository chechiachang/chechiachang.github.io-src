---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Kubernetes Custom Resources Basic"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2019-10-13T17:28:12+08:00
lastmod: 2019-10-13T17:28:12+08:00
featured: false
draft: false

menu:
  main:
    parent: "Ithelp 鐵人賽"
    weight: 1
---

[2020 It邦幫忙鐵人賽](https://ithelp.ithome.com.tw/2020ironman) 系列文章

這邊改了一些大綱，原本的內容還有一些 kubernetes 的設定，以及 GCP 相關服務的介紹。但既然我們的主題是把東西搬上 k8s 的踩雷旅程，那我們就繼續搬，繼續踩。剩下的時間大概會有四個題目。

- Nginx Ingress Controller
- Cert-manager
- Kubernetes CRD & Operator-sdk

由於我比較熟悉 GCP / GKE 的服務，這篇的操作過程都會以 GCP 平台作為範例，不過操作過程大體上是跨平台通用的。

寫文章真的是體力活，覺得我的文章還有參考價值，請左邊幫我點讚按個喜歡，右上角幫我按個追縱，底下歡迎留言討論。給我一點繼續走下去的動力。

對我的文章有興趣，歡迎到我的網站上 [https://chechia.net](https://chechia.net) 閱讀其他技術文章，有任何謬誤也請各方大德直接聯繫我，感激不盡。

![Exausted Cat Face](https://d32l83enj9u8rg.cloudfront.net/wp-content/uploads/iStock-966846550-cat-overheating-simonkr-1-940x470.jpg)

---

# 摘要

* custom resources
* custom controllers

# 簡介 custom resources

Kubernetes 預先定義許多 resource ，這些 resource 是 [kubernetes API](https://kubernetes.io/docs/reference/using-api/api-overview/) 預先設置的 [API objects](https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/)，例如 kubernetes pods resource 包含許多 pods 物件。

Custom resoure 則是透過擴充 kubernetes API ，讓自定義的物件也可以在 kubernetes 上使用。上篇 cert-manager 就使用了許多 custom resource，這些 resource 在一般安裝的 kubernetes 上沒有安裝，需要安裝 custom resource difinition，向 kubernetes cluster 定義新的 custom resource。例如 certificates.certmanager.k8s.io 就是 cert-manager 自定義的資源，用來代表產生 x509 certificate 的內容。

越來越多的 kubernetes core 方法，如今也使用 custom resources 來定義，讓 kubernetes 核心元件更加模組化。

custom resource 可以在運行中的 kubernetes 集群中註冊 (registration) ，也可以動態註銷，custom resource 並不會影響集群本身的運作。只要向 kubernetes 註冊完 custom resource，就可以透過 API 與 kubectl 控制 custom resource，就像操作 Pod resource 一樣。

# Custom controllers

custom resource 一但註冊，就可以依據 resource 的 CRD (custom resource definition) 來操作，因次可以儲存客製化的資料內容。然而在很多情形，我們並不只要 custom resource 來讀寫，而是希望 custom resource 能執行定義的工作，如同 Pod resource 可以在 kubernetes 集群上控制 Pod，在 Pod resource 上描述的 desired state kubernetes 會透過定義在 Pod API 中的 sync 邏輯，來達到 current state 與 desired state 的平衡。

我們希望 custom resource 也能做到上述的功能，提供 declarative API，讓使用者不需編寫完整的程式邏輯，只要透過控制 custom resource，就可以透過 controller 內定義的邏輯，來實現 desired state。使用者只需要專注在控制 custom resource 上的 desired state，讓 controller 處理細節實作。

例如：我們在 cert-manager 中設定 certificates.certmanager.k8s.io 資源，來描述我們希望取得 x509 certificate 的 desired state，但我們在 certificates.certmanager 上面沒有寫『透過 Let's Encrypt 取得 x509 certificate』的實現邏輯，仍然能透過 cert-manager 產生 x509 certiticate，因為 cert-manager 內部已經定義 certificates.certmanager.k8s.io 的 custom controller。


基本的 custom resource 操作

* 註冊 custom resource definition，讓 kubernetes API 看得懂 custom resource
  * 不然 API 會回覆 error: the server doesn't have a resource type
* 有 CRD 便可以 apply custom resource 到集群中
* 部署 custom controller，監測 custom resource 的 desired state 內容，並實現達到 desired state 的業務邏輯
  * 沒有 custom controller，custom resource 就只是可以 apply 與 update 的資料儲存結構，沒有 cert-manager 中 controller 的邏輯，也還是生不出 x509 certificate。

```
kubectl get chechiachang
error: the server doesn't have a resource type "chechiachang"
```

custom controller 也可以跟其他的 kubernetes resource 互動，例如 cert-manager 在產生 certificate 的時候，會把產生的 certificate 檔案放在 secret 中，cert-manager 會依據 order 中定義的 lifecycle ，持續檢查 certificate 的有效性，如果接近過期，則會觸發新的一輪 order。

我們也可以寫一個操作 Configmap 與 Deployment Resource 的 custom controller，來進行 deploymnet 的 Image 更新。

# 我需要 custom resource 嗎

kubernetes 在[should I add custom resource](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#should-i-add-a-custom-resource-to-my-kubernetes-cluster) 有列表分析該不該使用 custom resource ，將你的 API 邏輯整合到 kubernetes API 上。幾個判斷參考:

* API 是 [declarative model](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#declarative-apis)，如果不是可能不適合跟 kubernetes API 整合，獨立成為一個自己運行的服務即可
* 需要使用 kubernetes 
* 需要使用 kubectl 控制
* API 需要使用 [kubernetes 支援的功能](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#common-features)
* 正哉開發全新功能，因為整合舊的服務到 kubernetes API 工程浩大

# 也許 configmap/secret 就可以解決

如果只是需要將資料儲存在 kubernetes 上，有一個 build-int 的 kubernetes resource 很適合，就是 configmap。可以瘀考以下條件，判斷是否 configmap 搭配能監看 configmap 的 controller 就可以達成需求。

* 已經有完整的 config file，例如 mysql.cnf, nginx.conf...
* 主要用途是把檔案掛載到 Pod 中的 process 使用
* 使用時的格式，是整個檔案放在 Pod 中，或是使用環境變數塞到 Pod 裡面，而不是透過 kubernetes API 存取 (ex 使用 kubectl)
* 更新 configmpa 時更新 Pod，會比更新 custom resource 時更新 Pod 容易

如果使用 CRD 或 Aggregated kubernetes API，大多符合下列條件

* 使用 kubernetes libraries 與客戶端 (ex kubectl) 操作 custom resource
* 需要 top level 的 kubernetes 支援，例如可以 kubectl get cheachiachang
* 自動化 kubernetes 物件
* 需要用到 .spec, .status, .metadata，這些比較 desired state 與 currenty state 的功能
* 需要抽象類別來管理一群 controlled resource

# Custom Resource Definition

[Custom Resoure Definition](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions) 讓使用者可以定義 custom resource，定義 custom resource 的格式包括名稱與 data schema，然後交給 kubernetes API 去處理 custom resource 的儲存。

也就是說，透過 CRD 我們不用寫 custom resource 的 API，例如 cert-manager 不用寫 certificates.certmanager.k8s.io 的 API，而是向 kubernetes API server 註冊 CRD，讓 kubernetes API server 看得懂 custom source 的定義，並且直接使用 kubernetes API server，進行 custom resource 的 CRUD。

我們可以透過 kubectl (API server) 操作 certificates.certmanager.k8s.io，這個請求也是送到 kubernetes API server。

# API server aggregation

能夠透過註冊 CRD ，就可以使用原來的 kubernetes API 來進行 CRUD ，是因為 kubernetes API 對於普通的 API 操作提供泛型 (generic) 介面，直接使用 CRUD 的邏輯。

由於是 kubernetes Aggregated API ，所有 kubernetes 的 clients 都一起兼容新註冊的 custom resource，不用在 API 要定義，在冊戶端也要定義。註冊完的 custom resource definition，可以直接透過 kubectl 存取。

# 小結

* custom resource 簡介
* custom resource 使用的情境與條件
* custom resource definition 與 Aggregated API
