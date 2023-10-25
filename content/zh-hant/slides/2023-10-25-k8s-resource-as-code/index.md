---
title: "Kubernetes Summit: Resource as Code for Kubernetes: Stop kubectl apply"
summary: 將 k8s resource 以 code 管理，推上 vcs，並使用 argoCD, secret operator 等工具進行管理，來讓避免低級的人工操作錯誤，降低團隊整體失誤率，並降低 k8s admin 管理的成本，提高管理效率
authors: []
tags: ["kafka", "kubernetes"]
categories: ["kubernetes"]
date: '2023-10-23T00:00:00Z'
slides:
  # Choose a theme from https://github.com/hakimel/reveal.js#theming
  #theme: black
  theme: white
  # Choose a code highlighting style (if highlighting enabled in `params.toml`)
  #   Light style: github. Dark style: dracula (default).
  highlight_style: dracula
---

{{< slide background-image="onepiece.jpg" >}}

{{% speaker_note %}}
Q1: 有過使用 helm 跟 argocd 的人請舉手
Q2: k8s object 走 gitflow 管理的比例有超過 9 成的
{{% /speaker_note %}}

---

### Resource as Code for K8s Object
### 如何管理 k8s object

[Che Chia Chang](https://chechia.net/)

{{% speaker_note %}}
{{% /speaker_note %}}

---

### Outline

Manage Kubernetes Objects in Gitflow

- kubectl
- helm chart
- argocd (gitflow)
  - applicationset
- test

{{% speaker_note %}}

今天的內容前半部像是講古

首先會講 kubectl create / apply
kubectl 使用，然後官方有提醒我們使用 kubectl 管理 k8s object 時的 trade-off，這些 trade-off 我們可以使用其他的工具來彌補

導入 helm chart，來打包 k8s objects 變成一個完整地發布單位

argocd 走 gitflow 來發布

然後在 workflow 裡加入測試，確保 k8s objects 的交付品質

{{% /speaker_note %}}

---

### Kubectl

```
# Imperative commands 
kubectl create deployment nginx --image nginx

# Imperative object configuration 
kubectl create -f nginx.yaml

# Declarative object configuration
kubectl apply -R -f configs/
```

[https://kubernetes.io/docs/concepts/overview/working-with-objects/object-management/#management-techniques](https://kubernetes.io/docs/concepts/overview/working-with-objects/object-management/#management-techniques)

{{% speaker_note %}}
kubectl 應該是所有人學 k8s 的第一個工具
作為官方的 cli 工具，kunectl 非常強大，可以控制幾乎大部分 k8s 的 api，也能對幾乎所有 k8s object 進行操作
{{% /speaker_note %}}

---

{{< slide background-image="kubectl.jpg" >}}

{{% speaker_note %}}
首先，如同官方文件所描述，kubectl 的使用上，也有各種不同方法。ie. kubectl 交在不同人手上，使用方式是不同的
官方文件描述
- Imperative commands 指令式
- Imperative object configuration 指令物件
- Declarative object configuration 宣告物件

kubectl create deployment nginx，一行命令告訴 k8s 你要 create deployment

kubectl create -f nginx.yaml，使用者選擇要 create / apply / delete 而 nginx.yaml 裡面描述一個 nginx deployment 物件

kubectl apply -f -R nginx/，使用者描述一個或多個物件，描述物件的狀態。apply 時，由 kubectl 決定要對 object 執行，create / update / delete

{{% /speaker_note %}}

---

### Issue

```
# Imperative commands 
kubectl create deployment nginx --image nginx

# Imperative object configuration 
kubectl create -f nginx.yaml

# Declarative object configuration
kubectl apply -R -f configs/
```

{{% speaker_note %}}
kubectl 這麼好用，那為何不繼續用下去？

1. 的問題很明顯，不能 diff
2.3. 會有一個基礎的 spec，關於 deployment/nginx，因此可以在

重點
- change review / diff
- source record other than live
- template，一個可重複使用的樣版

2.3. 的問題，你必須對 object 夠了解，才寫得出完整沒 bug 的 spec yaml

3. 聽起來是最完整的，他的問題就是要如何維持 local file 與 live 連結，或是說 sync
這個有使用 argocd 的人可能就會比較有感覺

大家有興趣可以去看官方描述的內容，這裡不贅述
{{% /speaker_note %}}

---

### Issue

- change review / diff before apply
- source of live record
- template / repetitive apply
- sync local to live

{{% speaker_note %}}

- change review / diff before apply
- source of live record
- template / repetitive apply
- sync local to live

{{% /speaker_note %}}

---

### Declarative object configuration

```
nginx
├── deployment.yaml
├── ingress.yaml
└── service.yaml
redis
├── deployment.yaml
├── ingress.yaml
└── service.yaml
microservice-a b c ...
```

{{% speaker_note %}}
為了 change review，通常會走向 3. Declarative object configuration，可能會長這樣
一個 git repository
裡面有多個 directory，描述每一組服務所需要的資源
使用 kubectl 一次 apply 整個 directory，所以 local file 基本上也反應 live object
有 local file，很自然而然就會想要放到版本控制，例如 git，這樣又可以走 gitflow
PR -> review -> merged -> apply master / release tag
{{% /speaker_note %}}

---

{{< slide background-image="helm.jpg" >}}

{{% speaker_note %}}

有人在 2014 年前用過 k8s 嗎？

古早時期，要用個 redis 還要自己包 service / ingress / deployment，先去 dockerhub 找 redis，然後依據 readme 自己包 deployment，自己測試看 redis 會不會動

現在應該沒有人會因為要去使用 redis 或是 mysql，自己跑去寫 k8s object 了吧

helm v2.0-alpha 2016

現在有 helm + chart

如果只是使用低三方開源的 helm chart，社群幫你維護 service / ingress / deployment 
- 提供基本的 default value，預設就跑得起來
- 跑得起來後，跑得好，能使用 k8s orchestration 提供完整的功能，透過 value.yaml 控制
- 經過測試
- issue tracking
{{% /speaker_note %}}

---

### Helm chart

k8s object 的開發，打包，測試，release
- k8s 十分強大，享受 orchestration
- k8s object 變得太複雜
- 標準化 template，release + upgrade

{{% speaker_note %}}
chart 作為一個 k8s object 的 release / artifact，有開發流程，版本控管，測試，完整的發佈

app 本身，例如 redis，當然是整個應用的核心。但要能夠在 k8s 執行，並正確地享受 k8s orchestration 的好處，k8s object 非常的重要

甚至，k8s object 複雜度已經遠遠超過過去在 vm 上跑一個 redis，兜一個 systemd unit 就可以跑起來

k8s object 需要 release / version，才能做 object 的固定版本 apply，upgrade 生版，有問題 rollback

在 k8s 上要跑得穩邊的十分閫難，透過社群來維護大部分通運的第三方服務
{{% /speaker_note %}}

---

### Helm Chart Library

```
helm repo list

NAME       URL
bitnami    https://charts.bitnami.com/bitnami
argocd     https://argoproj.github.io/argo-helm
chaos-mesh https://charts.chaos-mesh.org
```

{{% speaker_note %}}
k8s objects 能動很簡單，但要跑得穩又能享受 orchestration 的便利，十分困難
透過社群來維護大部分通運的第三方服務，透過單一 value.yaml 

社群維護的 chart 不是就一勞永逸
- 不熱門的 chart
- 特殊需求時，還是需要 fork chart 回來自己維護

但無論如何，都是大幅降低維運的複雜度
{{% /speaker_note %}}

---

### helm 生態系

ex. helmfile

```
repositories:
- name: argocd
  url: https://argoproj.github.io/argo-helm

helmDefaults:
  kubeContext: general
  #verify: true
  wait: true
  timeout: 300

context: general

releases:
- name: argocd
  namespace: argocd
  chart: argocd/argo-cd
  version: 5.31.0
  values:
  - values/argocd.yaml
- name: redis

- name: mysql
```

[https://github.com/cdwv/awesome-helm](https://github.com/cdwv/awesome-helm)

---

### 更高層級的封裝

```
api-services
├── nginx
├── mysql
└── ingress -> nlb
daemon-services
├── redis
├── mysql
└── kafka
```

{{% speaker_note %}}
底下的依賴標準化，依據穩定的 release 發布之後
可以再進行更高層級的封裝

重複性的服務，例如每個 microservice 都需要
例如我有一百個 api service group，都是 restful api，都需要 ingress / service / nginx 等等

底下的元件標準化，降低維護成本
- 統一版本，醫病維護，升級，退版

例如 daemon service，底下依賴 queue / redis / db
{{% /speaker_note %}}

---

### 微服務

微服務不是問題，微服務底下的 k8s object 才是問題
- 可以快速，標準化的產生經過測試，微服務單元

---

### Issues

- V change review / diff before apply
- source of live record
- V template / repetitive apply
- sync local to live

{{% speaker_note %}}
version control / gitflow

helm template 有提供許多語法，可以有系統化的產生重複的 k8s object
ex. 可以跑 for loop / for each
這個在 IaC 或是 resource as code 的 xxx as code 都十分有利
{{% /speaker_note %}}

---

### Argo CD

[Declarative GitOps CD for Kubernetes](https://argo-cd.readthedocs.io/en/stable/)

![](https://argo-cd.readthedocs.io/en/stable/assets/argocd-ui.gif)

---

### Why Argo CD?

Application definitions, configurations, and environments should be declarative and version controlled. Application deployment and lifecycle management should be automated, auditable, and easy to understand.

{{% speaker_note %}}
application 應該是明確宣告的，清楚描述，並且有版本控管
描述 application 本身，附帶的設定 secret / configmap
environment 也應該是宣告式的

application 的部署與 lifecycle 管理，都應該是自動化，可以稽核，而且好理解
標準化，自動化
UI 圖像描述，一目瞭然。但事實上如果有做到講 local file 推到版本控制，光是使用 editor 也可以做到一目瞭然
{{% /speaker_note %}}

---

### Argo CD

- gitflow / git repository
- argocd application sync file from repository
- argocd controller 自動化的確保 sync
  - un-sync 自動化處理
  - 無法 sync 時通知 

{{% speaker_note %}}

gitflow
- k8s object 的 change 是需要 PR review 的，不是想改就 kubectl apply 下去
- k8s object 的品質把關，來自高品質的 review
- 針對 cluster 上的變更都有管控

能夠直接掌握 live object，透過 editor 檢查 git repository，或是透過 argocd UI 檢視

local file 等於 live object
在複雜的環境裡很重要，ex. k8s 內有成千上百個 helm release，可以用 editor 檢視 local file

不然要透過 k8s 去打 api
- api call 也是資源啊，能省則省
- editor 更直覺快速

{{% /speaker_note %}}

---

### applicationset

[git generator](https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-Git/)

```
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: general-argocd
  namespace: argocd
spec:
  generators:
  - git:
      repoURL: https://github.com/chechiachang/azure-argo
      revision: master
      directories:
      - path: clusters/dev/dev-general/argocd/*
  template:
    metadata:
      name: 'dev-general-argocd-{{path.basename}}'
      labels:
        environment: dev
        type: infra
        function: argocd
        cluster: dev-general
    spec:
      project: default
      syncPolicy:
        automated:
          prune: true
      source:
        repoURL: https://github.com/chechiachang/azure-argo
        targetRevision: master
        path: 'clusters/dev/dev-general/argocd/{{path.basename}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: argocd
```

{{% speaker_note %}}
argocd 除了 sync 以外還提供的許多功能

applicationset 定義一組 set，可以透過 generator 迭代的產生大量的 application
ex. 一次 deploy 一群 redis
{{% /speaker_note %}}

---

### applicationset

```
dev-general
├── default/redis
├── default/mysql
├── default/my-app
├── nginx-ingress/nginx-ingress
└── argocd/argocd
stag-general
prod-general
```

---

### cluster-wide 的 k8s object

cluster-wide 的 k8s object 也很適合
- 使用 helm template helper 來管理 value.yaml label / annotation / env / ...
- namespace
- rbac

{{% speaker_note %}}
cluster-wide 的 k8s object 也很適合塞進 argocd 管理

例如 cluster access control，複雜的 rbac rule，也很適合整理成為 helm chart
- 可以輕鬆實現 user -> rule 多對多
- 可以快速增減 user group
{{% /speaker_note %}}

---

###  Issues

- V change review / diff before apply
- V source of live record
- V template / repetitive apply
- V sync local to live

---

### More Issues: multi-hybrid cluster

- multiple k8s
  - dev / stag / prod
- hybrid k8s 
  - bare metal / public cloud

{{% speaker_note %}}
由於 k8s 內部的 component 都已經標準化，可以很輕易地複製測試過的 component
dev 測試 PR branch，staging 跑 release candicate，production 選擇經過測試的 release

能夠確保 dev / stag / prod 的 k8s object 是完全相同的

hybrid 環境管理，某些 k8s 元件應該安裝在哪些 cluster 上
- aws ingress controller / csi driver / cni node daemonsets
- local nginx-ingress controller
{{% /speaker_note %}}

---

### More Issues: multi-hybrid cluster

- [argocd cluster generator](https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-Cluster/)

```
kind: ApplicationSet
metadata:
  name: aws-cni
  namespace: kube-system
spec:
  generators:
  - clusters:
      selector:
        matchLabels:
          eks: true
          #bare-metal: true
          staging: true
```

---

### More Issues: multi-hybrid cluster

- [argocd cluster generator](https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-Cluster/)

```
aws-eks-1
├── aws cni
├── aws ingress controller
└── nginx-ingress controller
bare-metal-1
├── cilium
├── bare-metal ingress
└── nginx-ingress controller
```

{{% speaker_note %}}
多座 cluster
{{% /speaker_note %}}

---

### More Issues: multi-hybrid cluster

- applicationset

---

### More Issues: Test

k8s object 需不需要測試

- infra-test (bare-metal / self-hosted)
- release (helm chart)
- live status
- stress / load test / chaos engineering

{{% speaker_note %}}
k8s object 需不需要測試，覺得需要測試的請舉手

k8s object 需不需要測試，就跟這個投影片一樣
有時間就講一下，沒時間就跳過吧

infra-test provider 應該都測完了
要測的是 k8s object 的功能是否符合預期

當然，有測試的 helm releae 與沒測試的 helm release 也是天差地遠
{{% /speaker_note %}}

---

### Test: ansible playbook

- 測試 apply 後 k8s object 的 status
  - ingress 是否 ready
  - endpoint 是否有產生
- 可以先測
  - networking (ingress / svc)
  - storage (csi / pvc)

```
- name: Test nginx deployment
  hosts: {{ host }}
  gather_facts: no
  vars:
    deployment_name: "nginx"
  tasks:
  - name: Get deployment status
    shell: kubectl get deployment {{ deployment_name }} -o=jsonpath='{.status.readyReplicas}'
    register: deployment_status
    failed_when: deployment_status.rc != 0
  - name: Verify deployment is running
    assert:
      that:
        - deployment_status.stdout != 'null'
        - deployment_status.stdout != '0'
      fail_msg: 'Deployment {{ deployment_name }} is not running.'
```

---

### More Issues: Test

~~Test~~ Monitoring
- prometheus rule with helm chart
- ServiceMonitor

{{% speaker_note %}}
helm release 一個 api-services
api service 有 /metrics endpoint
透過 ServiceMonitor 來持續性的紀錄 metrics
透過 PrometheusRule 來設定異常 metrics 的告警
{{% /speaker_note %}}

---

### More Issues: Test

- stress-test / load test
  - k6 
- chaos-engineering
  - https://chaos-mesh.org/
  - https://github.com/asobti/kube-monkey

{{% speaker_note %}}
{{% /speaker_note %}}

---

### Summary

- kubectl + gitflow
- helm chart
- argocd: applicationset / generator
- test

Q & A
