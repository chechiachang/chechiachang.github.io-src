---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Kubernetes Custom Resources with Operator SDK"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2019-10-15T17:28:12+08:00
lastmod: 2019-10-15T17:28:12+08:00
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

* 超簡短推坑 oeprator-sdk
* 鐵人賽心得

# 承上

上篇介紹了 crd 與 controller，然而沒有說明 controller 的編寫與操作，因為 controller 的部分比較複雜，我們鐵人挑戰賽尾聲，篇幅說實在是不太夠。

有興趣詳細了解的大德，請參考相同鐵人挑戰團隊的隊友文章，裏頭對 controller 有詳細介紹，這邊就不贅述。直接提供個人使用覺得最簡單上手的 [operator sdk](https://github.com/operator-framework/operator-sdk)

# Operator SDK

[Operator SDK](https://github.com/operator-framework/operator-sdk) 是 [Operator framework](https://github.com/operator-framework) 中的一部分，能有效且自動化的管理 kubernetes native apps, operator 的管理工具。

複雜的 kubernetes application 是非常難管理的，寫 operator 也是很有挑戰，不僅要處理大量 kubernetes 底層的 API，要寫很多樣版。 operator SDK 使用 controller-runtime 的 library 讓編寫 native application 變得簡單許多

* 可以使用上層的 API 與抽象來編寫 operator 邏輯
* 快速使用 code generation
* 有擴充套件

# Workflow

這邊以 golang 為例說明

* 安裝 operator sdk
* 定義新的 API resource (custom resource definition)
* 定義 controller 來監測 custom resource
* 編寫 reconciling 邏輯來 sync desired state 與 current state
* 使用 sdk cli 進行測試
* 使用 sdk cli 來 build，並產生部屬用的 manifests

安裝請依照 [安裝說明](https://github.com/operator-framework/operator-sdk/blob/master/doc/user/install-operator-sdk.md) 操作即可。

這邊使用 sdk cli 來增加新的 crd

```
# Add a new API for the custom resource AppService
$ operator-sdk add api --api-version=app.example.com/v1alpha1 --kind=AppService
```

產生的 go 源碼會放在 pkg 中，可以依自己需求調整 crd 的結構

這邊使用 sdk cli 產生對應 crd 的 controller，裏頭已經寫好大部分的 code gene 與 reconcile 的樣板，直接修改就可使用，非常方便

```
# Add a new controller that watches for AppService
$ operator-sdk add controller --api-version=app.example.com/v1alpha1 --kind=AppService
```

修改完，直接使用 sdk cli build 成 image，然後推到 image hub 上

```
# Build and push the app-operator image to a public registry such as quay.io
$ operator-sdk build quay.io/example/app-operator
$ docker push quay.io/example/app-operator
```

部屬前檢查一下 manefests 檔案，特別是 crd.yaml 與 operator.yaml，如果源碼有調整記得做對應的修改。

```
# Setup Service Account
$ kubectl create -f deploy/service_account.yaml

# Setup RBAC
$ kubectl create -f deploy/role.yaml
$ kubectl create -f deploy/role_binding.yaml

# Setup the CRD
$ kubectl create -f deploy/crds/app.example.com_appservices_crd.yaml

# Deploy the app-operator
$ kubectl create -f deploy/operator.yaml
```

這樣便部屬了 operator，operator 會監看指定的 custom resource，並依照 controller 的邏輯進行 reconcile。

這邊以增加 custom resource 為例

```
# Create an AppService CR
# The default controller will watch for AppService objects and create a pod for each CR
$ kubectl create -f deploy/crds/app.example.com_v1alpha1_appservice_cr.yaml
```

增加一個 cr 到 kubernetes 上，這時 operator 會偵測到 cr 的變化，並且依照 reconcile 的邏輯 sync

檢查一下 cr 與 operator 的狀態

```
# Verify that a pod is created
$ kubectl get pod -l app=example-appservice
NAME                     READY     STATUS    RESTARTS   AGE
example-appservice-pod   1/1       Running   0          1m
```

詳細的操作步驟可以看 [這邊](https://github.com/operator-framework/getting-started/blob/master/README.md)

# 小結

事實上，operator sdk 的功能還有非常多，細講又要花好幾篇文章講，之後有機會會放在我的個人網站上。

另外 operator sdk 也歡迎外部的 Issue 與 PR，團隊的人非常 nice 會願意花時間跟社群朋友溝通，有興趣請來 contribute。

這系列鐵人文章，說實在沒有什麼很深入的技術討論，多半資料都是各個項目的官方文件翻譯，加上一些個人的經驗與解讀，並不是含金量很高的文章。然而我個人在接觸這些項目時，卻往往因為找不到細節操作的步驟分享文章，在許多小細節上撞牆很久，也因此才有了這系列文章。

這系列文就只是踩雷之旅，讓後人如果有用到這些文章，生活能過得開心一點，這 30 天的時間就有了價值。

鐵人挑戰賽的最後一天，感謝各路大德一路相隨，讓我在假日也能心甘情願地坐下來寫文章。游於藝天一篇真的很逼人，有幾天的文章品質是有蠻多問題的，也感謝大德們協助捉錯，給予很多建議。

謝謝各位。
