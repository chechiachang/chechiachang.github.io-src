---
title: "Kubernetes Nginx Ingress Controller"
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

這邊該了一些大綱，原本的內容還有一些 kubernetes 的設定，以及 GCP 相關服務的介紹。但既然我們的主題是把東西搬上 k8s 的踩雷旅程，那我們就繼續搬，繼續踩。剩下的時間大概會有四個題目。

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

# Nginx Ingress Controller

* 簡介 nginx & Ingress Controller
* 部屬並設定 nginx ingress controller

# Nginx Introduction

[Nginx](https://nginx.org/en/docs/) 是一款高效能、耐用、且功能強大的 load balancer 以及 web server，也是市占率最高的 web server 之一。

* 高效能的 web server，遠勝傳統 apache server 的資源與效能
* 大量的模組與擴充功能
* 有充足的安全性功能與設定
* 輕量
* 容易水平擴展

# Ingress & Ingress Controller
 
這邊簡單講一下 [kubernetes ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)。當我們在使用 kubernetes 時需要將外部流量 route 到集群內部，這邊使用 Ingress 這個 api resource，來定義外部到內部的設定，例如:

* service 連接
* load balance 設定
* SSL/TLS 終端
* 虛擬主機設定

一個簡單的 ingress 大概長這樣

```
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: test-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
      - path: /testpath
        backend:
          serviceName: test
          servicePort: 80
```

除了一般的 k8s 資源，nginx 主要的設定會落在 spec，以及依賴底下實作不同，額外設定的 annotation。

這邊可以看到 spec.rule 定義了外部 http 流量，引導到 backend service 的路徑。

annotations 下已經標註的 nginx.ingress 的 annotation，來快速增加額外的設定。

# Ingress & Ingress Controller

雖然已經指定 nginx 的 annotation，但這邊要注意，ingress resource 本身是不指定底層的實現 (ingress controller)，也就是說，底下是 nginx 也好，traefik 也行，只要能夠實現 ingress 裏頭設定的 routing rules 就可以。

只設定好 ingress，集群上是不會有任何作用的，還需要在集群上安裝 ingress controller 的實作，實作安裝完了以後，會依據 ingress 的設定，在 controller 裏頭實現，不管是 routing、ssl/tls termination、load balancing 等等功能。如同許多 Kubernetes resource 的設計理念一樣，這邊也很優雅的用 ingress 與 ingress controller，拆分的需求設定與實作實現兩邊的職責。

例如以 nginx ingress controller，安裝完後會依據 ingress 的設定，在 nginx pod 裡設定對應的 routing rules，如果有 ssl/tls 設定，也一併載入。

Kubernetes 官方文件提供了[許多不同的 controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/#additional-controllers) 可以依照需求選擇。

但如果不知道如何選擇，個人會推薦使用 nginx ingress controller，穩定、功能強大、設定又不至於太過複雜，基本的設定就能很好的支撐服務，不熟悉的大德們比較不容易被雷到。

底下我們就要來開始使用 nginx ingress controller。

# Deployment

我們這邊使用的 [ingress-nginx](https://github.com/kubernetes/ingress-nginx) 是 kubernetes org 內維護的專案，專案內容主要是再 k8s 上執行 nginx，抽象與實作的整合，並透過 configmap 來設定 nginx。針對 nginx ingress kubernetes 官方有提供[非常詳細的說明文件](https://kubernetes.github.io/ingress-nginx/) ，剛接觸 nginx 的大德可以透過這份文件，快速的操作 nginx 的設定，而不用直接寫 nginx.conf 的設定檔案。

* repo 版本是 nginx-0.26.1
* Image 版本是 quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.26.1

### Helm

我們這邊用 helm 部屬，[Nginx Ingress Controller Stable Chart](https://github.com/helm/charts/tree/master/stable/nginx-ingress)，讓各位大德用最簡單的步驟，獲得一個功能完整的 nginx ingress controller。

與前面幾個 helm chart 一樣，我們可以先取得 default values.yaml 設定檔，再進行更改。
```
$ wget https://raw.githubusercontent.com/helm/charts/master/stable/nginx-ingress/values.yaml
$ vim values.yaml
```

安裝時也可以使用 --set 來變更[安裝 chart 時的 parameters](https://github.com/helm/charts/tree/master/stable/nginx-ingress#configuration)
```
$ helm install stable/nginx-ingress \
	--set controller.metrics.enabled=true \
	-f values.yaml
```

安裝完後，resource 很快就起來。

```
kubectl get all --selector app=nginx-ingress
NAME                                                 READY   STATUS    RESTARTS   AGE
pod/nginx-ingress-controller-7bbcbdcf7f-tx69n        1/1     Running   0          216d
pod/nginx-ingress-default-backend-544cfb69fc-rnn6h   1/1     Running   0          216d

NAME                                    TYPE           CLUSTER-IP     EXTERNAL-IP    PORT(S)                      AGE
service/nginx-ingress-controller        LoadBalancer   10.15.246.22   34.35.36.37    80:30782/TCP,443:31933/TCP   216d
service/nginx-ingress-default-backend   ClusterIP      10.15.243.19   <none>         80/TCP                       216d

NAME                                            READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nginx-ingress-controller        1/1     1            1           216d
deployment.apps/nginx-ingress-default-backend   1/1     1            1           216d

NAME                                                       DESIRED   CURRENT   READY   AGE
replicaset.apps/nginx-ingress-controller-7bbcbdcf7f        1         1         1       216d
replicaset.apps/nginx-ingress-default-backend-544cfb69fc   1         1         1       216d

kubectl get configmap -l app=nginx-ingress
NAME                       DATA   AGE
nginx-ingress-controller   2      216d

kubectl get ingress
NAME            HOSTS                  ADDRESS       PORTS     AGE
ingress-nginx   api.chechiachang.com   34.35.36.37   80, 443   216d
```

兩個 Pods

* Nginx ingress controller 是主要的 nginx pod，裡面跑的是 nginx
* Nginx default backend 跑的是 default backend，nginx 看不懂了 route request 都往這邊送。

Service

* nginx-ingress-contrller 是我們在 GCP 上，在集群外部的 GCP 上的對外接口。如果在不同平台上，依據預設 service load balancer 有不同實作。
* 在 gcp 上，會需要時間來啟動 load balancer，等 load balancer 啟動完成，service 這邊就可以取得外部的 ip，接受 load balancer 來的流量
* 另外一個 service 就是 default backend 的 service

# 踩雷

第一個雷點是 helm chart install 帶入的 [parameters](https://github.com/helm/charts/tree/master/stable/nginx-ingress#configuration)，有些 parameter 是直接影響 deployment 的設定，如果沒注意到，安裝完後沒辦法透過 hot reload 來處理，只能幹掉重來。建議把這份表格都看過一次，再依照環境與需求補上。

```
$ helm install stable/nginx-ingress \
	--set controller.metrics.enabled=true \
	--set controller.service.externalTrafficPolicy=Local \
	-f values.yaml
```

這邊開了 prometheus metrics exporter，以及 source IP preservation。

# Nginx Config

再安裝完後，外部的 load balancer 啟用後，就可以透過 GCP 的 external ip 連入 nginx，nginx 依照設定的 rule 向後端服務做集群內的 load balancing 與 routing。

如果在使用過程中，有需要執行更改設定，或是 hot reload config，在 kubernetes 上要如何做呢? 我們下回分解。
