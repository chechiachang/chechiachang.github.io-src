---
title: "Kubernetes Summit: Get started with Etcd & Kubernetes"
summary: "Etcd 是 Kubernetes 的重要元件之一，本次工作坊將帶領觀眾初探 Etcd，包含安裝，設定，以及操作。並藉由本地的 Etcd 來架設一個最簡單的 Kubernetes Cluster。"
authors: []
tags: ["etcd", "kubernetes"]
categories: ["kubernetes"]
date: '2024-08-05T00:45:00Z'
slides:
  # Choose a theme from https://github.com/hakimel/reveal.js#theming
  #theme: black
  theme: white
  # Choose a code highlighting style (if highlighting enabled in `params.toml`)
  #   Light style: github. Dark style: dracula (default).
  highlight_style: dracula
---

### Workshop: Get started with Etcd & Kubernetes

- 在 docker 中啟動 Etcd 與 k8s control plane
- 使用 etcdctl 操作 etcd
- 操作 etcd cluster
- 在 docker 中啟動 k8s control plane
- 使用 kubectl 操作 k8s control plane

---

### Workshop: Get started with Etcd & Kubernetes
### 手把手搭建 Etcd 與 K8s 工作坊

Che Chia Chang
[https://chechia.net/](https://chechia.net/)

{{% speaker_note %}}
{{% /speaker_note %}}

---

### 關於我

- Che Chia Chang
- SRE @ [Maicoin](https://www.linkedin.com/company/maicoin/jobs/)
- [Microsoft MVP](https://mvp.microsoft.com/zh-TW/MVP/profile/e407d0b9-5c01-eb11-a815-000d3a8ccaf5)
- 個人部落格[chechia.net](https://chechia.net/)
- presentation and speaker notes
- 鐵人賽 (Terraform / Vault 手把手入門)

---

### 大綱

- Etcd 基礎操作
- Etcd Clusters 操作
- 搭建 Kubernetes Cluster Control Plane
  - (Optional) Kubernetes the hard way
- (Optional) 搭建 Worker Node
- Q&A

{{% speaker_note %}}
{{% /speaker_note %}}

---

### 準備

1. 你有一台電腦，可以上網，能夠點滑鼠右鍵
2. 你會使用 bash 或 powershell terminal

---

### 存取機器

1. 至[workshop.chechia.net](https://workshop.chechia.net) 領取一台 VM 並簽名
2. 從講師取得使用者名稱與密碼
3. 透過 url 連線至你的 VM
4. 下載教材（複製底下指令，滑鼠右鍵貼到 terminal）

```
git clone https://github.com/chechiachang/etcd-playground.git
```

---

### Etcd 基礎操作: 啟動一台 Etcd

```
cd etcd-playground
ls

cd 00-prerequsites/
docker compose up -d
docker ps
docker logs -f etcd-1
```

ctrl + c to exit
tab to auto complete

---

### Etcd 基礎操作: Etcdctl

請嘗試操作 https://etcd.io/docs/v3.5/tutorials/ 中的幾個範例
- Reading from etcd
- Writing to etcd
- How to get keys by prefix
- How to delete keys
- How to watch keys
- How to check Cluster status

```
etcdctl get foo
etcdctl put foo "Hello World"
```

---

### Etcd 基礎操作: 重啟 Etcd

透過以下 command 重啟 Etcd

```
docker compose down
docker ps
docker compose up -d
```

---

### Etcd 基礎操作: Quiz

1. 重啟後，是否還能讀取到 foo 的值？為什麼？
2. 請用50個字，描述你目前覺得 etcd 是什麼？
   - 把答案填到 [workshop.chechia.net](https://workshop.chechia.net)
   - 不是考試，隨意發揮，重點在促進大家思考

```
etcdctl put foo bar
docker compose down
docker compose up -d
etcdctl get foo
```

---

### Etcd 基礎操作: Answer

1. 本 workshop 的 docker-compose.yml 中，Etcd 的資料是存放在本地的 etcd1 資料夾中，因此重啟後，資料不會遺失。透過以下指令可以清除 etcd1 資料夾中的資料
2. https://etcd.io/docs/v3.5/learning/why/

```
cd 00-prerequsites/

docker-compose down --volumes
rm -rf etcd1/*

# 新的 etcd
docker-compose up -d
```

---

### 閱讀資料

- https://etcd.io/docs/v3.5/learning/why/
- https://github.com/chechiachang/etcd-playground/blob/main/00-prerequsites/README.md

---

### 加分題為自己加分：authentication

啟用 etcd 的 authentication
- 使用 userA 登入 etcd
- 使用 userA 寫入資料
- 使用 userB 讀取資料
- 關閉匿名存取
- 卡住乃兵家常事，大俠請重新來過即可
- https://etcd.io/docs/v3.5/op-guide/authentication/

---

### 加分題為自己加分：authentication

```
etcdctl role add
etcdctl role grant-permission
etcdctl user add
etcdctl user list
etcdctl auth status
etcdctl auth enable
```

---

### Etcd Clusters: 啟動多台 Etcd

- 先關閉 01-prerequsites 的 Etcd

```
docker compose down --volumes
```

---

### Etcd Clusters: 啟動多台 Etcd

```
cd 01-cluster/
docker compose up -d
docker ps

etcdctl endpoint status

export ENDPOINTS="http://127.0.0.1:2379,http://127.0.0.1:2380,http://127.0.0.1:2381"
etcdctl --endpoints $ENDPOINTS endpoint status

etcdctl --endpoints $ENDPOINTS endpoint status --write-out=table

export ETCDCTL_ENDPOINTS="http://127.0.0.1:2379,http://127.0.0.1:2380,http://127.0.0.1:2381"
```

---

### Etcd Clusters: 操作

https://etcd.io/docs/v3.5/tutorials/
- How to check Cluster status

```
etcdctl endpoint status
# 查詢 help 檢查每個欄位的意義
etcdctl endpoint status --help
etcdctl endpoint health
etcdctl endpoint hashkv
```

---

### Etcd Clusters: Member

```
etcdctl --write-out=table endpoint status

docker exec -it etcd-1 etcdctl move-leader 88d11e2649dad027
etcdctl --write-out=table endpoint status
```

---

### Etcd Clusters: Member

https://etcd.io/docs/v3.5/tutorials/
- How to Add and Remove Members

---

- 移除一個 member，name: etcd-3 id: c3697a4fd7a20dcd
- 添加回來
- https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#replacing-a-failed-etcd-member

```
etcdctl member remove
etcdctl member remove c3697a4fd7a20dcd
etcdctl member list

etcdctl member add c3697a4fd7a20dcd --peer-urls="http://etcd-3:2380"
etcdctl member list

rm -rf etcd3/member
docker start etcd-3
etcd member list
```

---

### Etcd Clusters: network partition and recovery

- https://etcd.io/docs/v3.5/op-guide/failures/

---

### 閱讀資料

- https://etcd.io/docs/v3.5/learning/design-learner/

---

### 加分題為自己加分：authentication

啟用 etcd cluster 的 tls，並讓 etcdcetl 透過 tls 連線
- https://etcd.io/docs/v3.5/op-guide/clustering/
- 關閉服務
- 產生 ca 與 certs
- 配置到 etcd* 資料夾中
- 更改 01-cluster/docker-compose.yaml
- docker compose 重啟服務

---

### K8s: 搭建 K8s Control Plane

```
cd 02-k8s-control-plane/

cd certs
./generate.sh

cd ../
docker compose up -d
docker ps
docker logs kube-apiserver
docker logs kube-controller-manager
docker logs kube-scheduler
```

---

### K8s: kubectl

```
kubectl --kubeconfig=certs/admin.kubeconfig cluster-info
kubectl --kubeconfig=certs/admin.kubeconfig get all -A
```

---

### K8s: the hard way

[kelseyhightower/kubernetes-the-hard-way](https://github.com/kelseyhightower/kubernetes-the-hard-way/tree/master) 是一個很棒的學習資源，可以讓你了解到 Kubernetes 的每個細節
- 我沒辦法做得更好，但我們可以一起過一次裡面做了哪些事

{{% speaker_note %}}
{{% /speaker_note %}}

---

### K8s: ./generate.sh

[certs/generate.sh](https://github.com/chechiachang/etcd-playground/blob/main/02-control-panel/certs/generate.sh) 有附上對應的 k8s-the-hard-way 的說明文件
- ca 與 certs 是部署 k8s control plane 的必要檔案
- 但非常花時間，本 workshop 會直接使用腳本產生配置
- 加分題：鼓勵大家自己操作過一次 certs 的產生

```
vi certs/generate.sh
ls certs
```

---

### K8s: Quiz

3. 請簡述 etcd / apiserver / controller-manager / scheduler 的功能
4. 為何不同 component 中使用的 certs / kubeconfig 檔案不同？

```
ls apiserver
ls controller-manager
ls scheduler
```

---

### K8s: Answer

3. https://kubernetes.io/docs/concepts/overview/components/
4. 呈 3.

---

### K8s: etcd operations for k8s

https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/
- [Securing etcd Clusters](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#securing-etcd-clusters) 放在加分題

---

### K8s: etcd backup and restore

https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#backing-up-an-etcd-cluster

```
# 確定 leader 與 raft index
etcdctl --write-out=table endpoint status
# 備份
docker exec -it etcd-1 etcdctl snapshot save /etcd_data/snapshot.db
ls etcd1
```

---

### K8s: etcd backup and restore

https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#restoring-an-etcd-cluster
- 停止 k8s control plane (apiserver)

```
docker stop kube-apiserver

# 恢復
cp etcd1/snapshot.db etcd2/snapshot.db
cp etcd1/snapshot.db etcd3/snapshot.db
docker exec -it etcd-1 etcdctl snapshot restore /etcd_data/snapshot.db
docker exec -it etcd-2 etcdctl snapshot restore /etcd_data/snapshot.db
docker exec -it etcd-3 etcdctl snapshot restore /etcd_data/snapshot.db
```

---

### K8s: etcd backup and restore

https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#scaling-out-etcd-clusters
- 修改 01-cluster/docker-compose.yaml
- 調整底下 comment 中的部分
- 增加兩台 etcd member 到 cluster 中


---

### 加分題為自己加分：自己做 ca and tls certs

- 閱讀 generate.sh 的 comment 部分網頁連結
- 將 generate.sh 的內容，到 terminal 中一段一段 copy paste 執行

---

### 加分題為自己加分: 增加 apiserver

- 更改 02-control-panel/docker-compose.yaml
- 修改底下 comment 中的部分 kube-apiserver-1 的部分
- 使用 docker compose up 啟動服務
- 使用 kubectl 存取 kube-apiserver-1
  - 需要修改 generate.sh，調整 certs/admin.kubeconfig

---

### (Optional) 搭建 K8s Node

---

### 後續

- 回家自己找一台 linux 機器，跑完 k8s the hard way

---

### 參考資料

- etcd
  - https://etcd.io/
  - https://etcd.io/docs/v3.5/learning/
  - http://play.etcd.io/play
  - https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/
- kubernetes
  - https://kubernetes.io/docs/concepts/overview/components/
  - 中文 https://kubernetes.feisky.xyz/concepts/components/
  - https://github.com/kelseyhightower/kubernetes-the-hard-way
