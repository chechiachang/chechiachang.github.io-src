---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Kubernetes Introduction for Non Engineer"
summary: ""
authors: []
tags: []
categories: []
date: 2019-10-30T11:26:31+08:00
slides:
  # Choose a theme from https://github.com/hakimel/reveal.js#theming
  theme: league
  # Choose a code highlighting style (if highlighting enabled in `params.toml`)
  #   Light style: github. Dark style: dracula (default).
  highlight_style: github
---

### Kubernetes 是啥能吃嗎

給非工程師的 Kubernetes 簡介

{{< figure src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Kubernetes_logo_without_workmark.svg/1200px-Kubernetes_logo_without_workmark.svg.png" height="40%" width="40%" title="" >}}

---

### 大綱

* kubernetes 是一個工具，[越來越夯](https://trends.google.com.tw/trends/explore?date=today%205-y&q=docker,kubernetes,blockchain)
* 這個工具想解決的問題
* 最後才說 Kubernetes 是啥能吃嗎

---

### 寫完 app 到上線要走的路

工程團隊產出完美的程式碼後，大家從此過著幸福快樂的日子?

---

### 寫完 app 到上線要走的路

{{< figure src="https://images.vexels.com/media/users/3/143600/isolated/preview/1b2a1e1747f67ce87ea8af5fdf410d23-yao-ming-face-meme-by-vexels.png" height="60%" width="60%" title="" >}}

---

### 常見問題

* "It works on MY PC !"
* 一個 app 不夠力，有沒有試過兩個 app ？
* staging 跟 production 的差別 = 把使用者當QA ？
* Valar Morghulis. Valar Dohaeris.

---

### 1. It works on my PC !

* app 是好的，server 是好的，app 放上 server 就壞了。why?
* server 跟 mac 不一樣。mac 有的東西 server 不一定有
* 跑程式之前要先裝某某東西
  * 系統依賴性(dependency)

---

### 1. 容器 (Container)

使用容器來解決 It works on my PC ! 的問題

{{< figure src="https://www.portablespace.co.uk/wp-content/uploads/2018/08/7-Portable-Space-40FT-HC-final.jpg" height="60%" width="60%" title="" >}}

---

### 1. 容器 (Container)

* 怕缺東西整麼辦，整包包好放上去跑
  * app
  * app 的程式庫(library)
  * 作業系統 Linux 的一部分，補足不同 server 上缺的東西
  * App + 程式庫 + 作業系統的一部分 = container
* 開發 -> 打包 -> 部署

---

### 1. 容器 (Container)

* keywords: 容器，容器化，container, [docker](https://www.docker.com/)

{{< figure src="https://cdn.worldvectorlogo.com/logos/docker.svg" height="60%" width="60%" title="" >}}

---

### 2. 一個 app 不夠力，有沒有試過兩個 app ？

1 app = 100 使用者使用，1,000 使用者要怎麼辦?

1. 把 app 放到 10 倍大的 server
2. 把 10 個 app 放到 10 台 server

* 垂直擴展(vertical scaling), 水平擴展(horizontal scaling)

---

### 2. 水平擴展與效能提升

{{< figure src="https://www.cbronline.com/wp-content/uploads/2018/02/docker-swarm-containers.png" height="60%" width="60%" title="" >}}

---

### 3. staging 跟 production 的差別

* staging 有一個 QA
* production 有很多 QA
* 壞了被使用者發現，把使用者當 QA ，會遭到報應的

---

### 3. staging 跟 production 的差別

* production 穩定嗎？有多穩？
* production 速度快嗎？有多快？
* 程式不只要跑的對，還要跑的又快又好
* 服務監測(monitoring)

---

### 3. staging 跟 production 的差別

* 壞了才發現壞掉
* 壞之前發現即將要壞掉
* 即時告警(alerting)

---

### 4. Valar Morghulis. Valar Dohaeris.

* app 終有一死
* Google 每個月都在死 [status.cloud.google.com](https://status.cloud.google.com/summary)
* 上版就壞掉，v1.20.1-hotfix-hotfix-hotfix

---

### 4. Valar Morghulis. Valar Dohaeris.

* 確保寫好 app 的同時，也要思考死了怎麼辦
* 預設 app 就是會死
  * 測試活著還是死了(Health check)
  * 讓他自動站起來(auto recovery)

---

### 複習一下

1. "It works on MY PC !"
1. 一個 app 變成兩個 app
1. staging 跟 production 的差別
1. Valar Morghulis. Valar Dohaeris.

---

### Kubernetes 是啥能吃嗎

* Kubernetes (K8s) is an open-source system for automating deployment, scaling, and management of containerized applications.
* [https://kubernetes.io/](https://kubernetes.io/)

{{< figure src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Kubernetes_logo_without_workmark.svg/1200px-Kubernetes_logo_without_workmark.svg.png" height="40%" width="40%" title="" >}}

---

### Kubernetes 是啥能吃嗎

1. Containerized: "It works on every PC"
1. Scaling: 1 app -> 10 apps
1. Monitoring, Alerting: staging -> production
1. Health Check, Auto Recovery

---

### 我們用 Kubernetes 做到的事

* 一鍵部署上線
* 自動監測
* 自動警告
* 水平擴展
* 自動復原

---

### keywords

* app, library, os dependency, docker
* horizontal scaling
* monitoring, alerting
* health check, auto recovery, high available
* kubernetes
