---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Kubernetes Custom Resource Deployment"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2019-10-13T22:03:08+08:00
lastmod: 2019-10-13T22:03:08+08:00
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

# 摘要

* CRD 內容
* Deploy CRD
* Use custom resource

# Recap

在上次的 cert-manager 內容中我們走過 cert-manager 的安裝步驟，其中有一個步驟是 apply cert-manager 的 manigests 檔案 `*.yaml`)

[https://github.com/jetstack/cert-manager/tree/release-0.11/deploy/manifests](https://github.com/jetstack/cert-manager/tree/release-0.11/deploy/manifests)

```
$ git clone https://github.com/jetstack/cert-manager
$ git checkout release-0.11
$ ls deploy/manifest

00-crds.yaml
01-namespace.yaml
BUILD.bazel	
README.md	
helm-values.yaml
```

我們快速看一下這個 00-crds.yaml，這個 yaml 非常長，直接[跳到 certificates.certmanager.k8s.io](https://github.com/jetstack/cert-manager/blob/release-0.11/deploy/manifests/00-crds.yaml#L1786)

希望看 golang 源碼文件的話，可以搭配[godoc.org/k8s.io/apiextensions](https://godoc.org/k8s.io/apiextensions-apiserver/pkg/apis/apiextensions#CustomResourceDefinitionSpec) 來閱讀，更能理解 definition。

在看之前先注意幾件事，CRD 內除了 schema 外，還定義了許多不同情境的使用資料。

* CRD 內定義了 custom resource 的資料儲存 .spec.validation.openAPIV3Schema，使用 custom resource 會透過 validator 驗證
* .openAPIV3Schema 內定義了 .spec，以及 rumtime 中紀錄 .status 的資料
  * controller 可以把狀態 sync 到 custom resource 的 .status 中紀錄
  * controller 可以比對 .spec 與 .status 來決定是否要 sync 以及如何 sync
* CRD 內定義了與 server 以及 client 互動的方式，
  * names 中定義各種使用情境的 custom resource 名稱
  * additionalPrinterColumns 中添加 kubectl 中的顯示內容

```
// 這邊使用的是 v1beta1 的 API (deprecated at v1.16) ，新版開發建議使用 apiextension.k8s.io/v1 的 api
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  creationTimestamp: null
  name: certificates.cert-manager.io
spec:
  // 使用 kubectl 會額外顯示的資訊內容，透過 jsonpath 去 parse 顯示
  additionalPrinterColumns:
  - JSONPath: .status.conditions[?(@.type=="Ready")].status
    name: Ready
    type: string
  - JSONPath: .spec.secretName
    name: Secret
    type: string
  - JSONPath: .spec.issuerRef.name
    name: Issuer
    priority: 1
    type: string
  - JSONPath: .status.conditions[?(@.type=="Ready")].message
    name: Status
    priority: 1
    type: string
  - JSONPath: .metadata.creationTimestamp
    description: CreationTimestamp is a timestamp representing the server time when
      this object was created. It is not guaranteed to be set in happens-before order
      across separate operations. Clients may not set this value. It is represented
      in RFC3339 form and is in UTC.
    name: Age
    type: date
  group: cert-manager.io
  // 定義 CRD 在不同情境下使用的名稱
  names:
    kind: Certificate
    listKind: CertificateList
    plural: certificates
    shortNames:
    - cert
    - certs
    singular: certificate
  scope: Namespaced
  subresources:
    status: {}
  validation:
    // openAPIV3Schema 中是 custom resource 實際操作會使用的內容
    // properties 使用 . .description .type ，分別定義名稱，描述，檢查型別
    openAPIV3Schema:
      description: Certificate is a type to represent a Certificate from ACME
      properties:
        apiVersion:
          description: 'APIVersion defines the versioned schema of this representation
            of an object. Servers should convert recognized schemas to the latest
            internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources'
          type: string
        kind:
          description: 'Kind is a string value representing the REST resource this
            object represents. Servers may infer this from the endpoint the client
            submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds'
          type: string
        // custom resource runtime 中的 metadata
        metadata:
          type: object
        // custom resource 使用時的 spec，定義 custom resoure 的 desired status
        spec:
          ...
        // custom controller 監測 custom resource 的 current status，這邊的資料完全視 controller 實作來產生，如果沒有實作 sync status，也可以沒有資料
        status:
          ...
      type: object
  // 這個是 CRD 物件的 version，可以定義多個不同 version 的 CRD，調用時需要註明版本
  version: v1alpha2
  versions:
  - name: v1alpha2
    served: true
    storage: true
// 這個是 CRD 物件的 status，描述 CRD 部署到 API server 的狀態，例如 CRD 儲存適用 configmap 的儲存空間，這邊顯示在 API server 上的儲存狀態。不要跟 custom resource 的 status 弄混了
status:
  acceptedNames:
    kind: ""
    plural: ""
  conditions: []
  storedVersions: []
```

helm-values.yaml 與 01-namespace.yaml 很單純，前者是使用 helm 部署的可設定參數，預設只有 kubernetes resources，後者則是為之後的 cert-manager 元件新增一個 kubernetes namespace。

# 小結 CRD 內容 (apiextensions/v1beta1)

* CRD 顯示名稱，內容
* CRD spec 驗證
  * custom resource
  * custom resource schema
* CRD 自身部署狀態

# 部署

部署相較定義本身就非常簡單，直接 kubectl apply 到 kubernetes 上

# 使用 custom resource

有了 CRD，我們便可以使用 CRUD API，互動模式與其他 build-in kubernetes resources 相同，只是內容會照 CRD 上的定義調整

```
kubectl get certificates.certmanager.k8s.io
kubectl get certificates
kubectl get certs --all-namespaces
kubectl get cert -n cert-manager

NAMESPACE          NAME                READY   SECRET              AGE
cert-manager       ingress-nginx-tls   True    ingress-nginx-tls   221d
```

這邊看到的內容可能會有些落差，因為我當初用的版本比較舊，但內容大同小異。

底下的 describe 內容已經跟上面的 CRD 版本差太多，對不起來了。但我也懶得再佈一組，還要重做 dnsName 與 authotization challenge

直接讓大家感受一下舊版的內容XD

```
$ kubectl describe cert ingress-nginx-tls

Name:         ingress-nginx-tls
Namespace:    cert-manager
API Version:  certmanager.k8s.io/v1alpha1
Kind:         Certificate
Metadata:
  Creation Timestamp:  2019-03-06T06:48:26Z
  Generation:          4
  Owner References:
    API Version:           extensions/v1beta1
    Block Owner Deletion:  true
    Controller:            true
    Kind:                  Ingress
    Name:                  ingress-nginx
  Self Link:               /apis/certmanager.k8s.io/v1alpha1/namespaces/default/certificates/ingress-nginx-tls
Spec:
  Acme:
    Config:
      Domains:
        chechiachang.com
      Http 01:
        Ingress:
        Ingress Class:  nginx
  Dns Names:
    chechiachang.com
  Issuer Ref:
    Kind:       ClusterIssuer
    Name:       letsencrypt-prod
  Secret Name:  ingress-nginx-tls
// 當前的 status，controller sync 上來
// controller 會比對 .spec 與 .status，判斷是否需要做事，ex. renew
Status:
  Acme:
    Order:
      URL:  https://acme-v02.api.letsencrypt.org/acme/order/*
  Conditions:
    Last Transition Time:  2019-09-02T03:52:03Z
    Message:               Certificate renewed successfully
    Reason:                CertRenewed
    Status:                True
    Type:                  Ready
    Last Transition Time:  2019-09-02T03:52:01Z
    Message:               Order validated
    Reason:                OrderValidated
    Status:                False
    Type:                  ValidateFailed
Events:                    <none>
```

想要新增，可以回去看 [cert-manager tutorial](https://docs.cert-manager.io/en/latest/getting-started/install/kubernetes.html#verifying-the-installation)，這個是新版的文件

當然，不爽這個 cert resource 也可以幹掉

```
$ kubectl delete cert ingress-nginx-tls -n cert-manager
```

以上

# 小結

* 簡介 CRD 與 CRD 內容
* 操作 custom resource
