---
title: "Workshop: RAG打造企業AI知識庫：把一甲子功力傳給新人"
summary: "學員將學會如何利用 RAG 技術，結合 OpenAI、LangChain、Qdrant 向量數據庫，構建企業內部文檔的智能知識庫，並能設計與實作一個基於自然語言處理（NLP）的查詢系統，來提升開發團隊的效率與知識管理能力。"
authors: []
tags: ["rag", "devops"]
categories: ["devops"]
date: '2025-05-05T00:45:00Z'
slides:
  # Choose a theme from https://github.com/hakimel/reveal.js#theming
  #theme: black
  theme: white
  # Choose a code highlighting style (if highlighting enabled in `params.toml`)
  #   Light style: github. Dark style: dracula (default).
  highlight_style: dracula
---

### RAG Workshop

##### 本次 workshop 以 hands-on 的方式進行，累積操作經驗為主，講解與說明為輔。觀念內容有準備教材，需要參與者自行閱讀

---

### 基本需求

1. 有自己的電腦，可以上網
  1. 選項1: 使用自己的電腦，在 docker 啟動開發環境
  1. 選項2: 使用自己的電腦，遠端連線講師提供的 VM，在VM 中啟動 docker 開發環境
1. 會使用 docker
1. 會使用 python 與 jupyter notebook

---




### 準備開發環境

##### 選擇一：使用自己的電腦

請提前在家先試跑一遍，把 docker image 跟 pip 套件都下載好，現場要載很久

```
git clone https://github.com/chechiachang/rag-workshop.git

cd rag-workshop

docker compose up -d

open http://localhost:8888
```

---

##### 選擇二：講師提供的 VM

請註冊 ngrok 帳號

1. 至[workshop.chechia.net](https://workshop.chechia.net) 領取一台 VM 並簽名
2. 從講師取得使用者名稱與密碼
3. 使用瀏覽器，透過 url 連線至你的 VM，輸入使用者名稱與密碼登入
4. Protocol: SSH，port 22，authentication type: password
5. 下載教材（滑鼠複製底下指令，滑鼠右鍵就能貼到 terminal 中）

```
git clone https://github.com/chechiachang/rag-workshop.git

cd rag-workshop

docker compose up -d
```

---

### 如何保存自己的進度

github repository 開一個新的 repository，然後上傳

```
# ssh 進去 vm

cd rag-workshop

git remote add new <your-repo-url>

git add .

git commit -m "save my progress"

git push new main
```

---

---

0. Get-Started
   1. access slides
   2. Docker compose up
      1. use workshop VM. Images pulled, models downloaded, datasets downloaded
      1. use your own laptop. You better start docker pull
1. what is rag
2. why rag
3. how to build rag (jupyter notebook)

---

### 切入點

4. DevOps Processes and Procedures:
Standard Operating Procedures (SOPs):
Documentation defines how different teams collaborate, communicate, and resolve issues.
Incident Response:
Documentation outlines incident response procedures, including steps for identifying, resolving, and preventing incidents.

6. Knowledge Management:
Internal Wiki:
A central repository for DevOps documentation, including internal procedures, best practices, and training materials.
Knowledge Sharing:
Documentation facilitates knowledge sharing and collaboration between teams, ensuring that everyone has access to the information they need. 

##### 本次 workshop 以 hands-on 的方式進行，累積操作經驗為主，講解與說明為輔。觀念內容有準備教材，需要參與者自行閱讀

- docker 啟動 etcd
- etcdctl 存取 etcd
- docker 啟動 etcd cluster
- docker 啟動 k8s control plane
- kubectl 存取 k8s control plane
- 維運 k8s 所需的 etcd operation

##### 參與者需要一台電腦，可以上網，能夠點滑鼠右鍵

---

### etcd Workshop
### 手把手搭建 etcd 與 K8s 工作坊

Che Chia Chang
[https://chechia.net/](https://chechia.net/)

{{% speaker_note %}}
{{% /speaker_note %}}

---

### 關於我

- Che Chia Chang
- SRE @ [Maicoin](https://www.cake.me/companies/maicoin/jobs)
- [Microsoft MVP](https://mvp.microsoft.com/zh-TW/MVP/profile/e407d0b9-5c01-eb11-a815-000d3a8ccaf5)
- 個人部落格[chechia.net](https://chechia.net/)
- presentation and speaker notes
- 鐵人賽 (Terraform / Vault 手把手入門)

---

### We're hiring!

https://www.cake.me/companies/maicoin/jobs

![](we-re-hiring.png)

---

### 大綱

- docker 啟動 etcd
- etcdctl 存取 etcd
- docker 啟動 etcd cluster
- docker 啟動 k8s control plane
- 維運 k8s 所需的 etcd operation
- (Optional) 搭建 Worker Node

{{% speaker_note %}}
{{% /speaker_note %}}

---

### 如何進行 workshop

- 講師會在台上帶頭影片的內容
- 參與者在自己的機器上操作
- 參與者可以跟台上的進度，也可以超前進度向後操作
- 進度落後不太會影響後續操作，不必擔心
- 加分題是重要，但沒時間於今日完成的內容，請自行參考
- 有很多問題也很正常，產生疑問也是工作坊的目的

---

### 如何存取遠端VM

1. 至[workshop.chechia.net](https://workshop.chechia.net) 領取一台 VM 並簽名
2. 從講師取得使用者名稱與密碼
3. 使用瀏覽器，透過 url 連線至你的 VM，輸入使用者名稱與密碼登入
4. Protocol: SSH，port 22，authentication type: password
5. 下載教材（滑鼠複製底下指令，滑鼠右鍵就能貼到 terminal 中）

```
git clone https://github.com/chechiachang/etcd-playground.git
```

---

### 回家如何自建 workshop 環境

workshop 提供的機器
- ubuntu
- 安裝這些東西 [github.com/chechiachang/terraform-azure](https://github.com/chechiachang/terraform-azure/blob/main/templates/cloud_config/workshop.yaml)
mac 安裝以下工具
- docker https://docs.docker.com/desktop/install/mac-install/
- 安裝 [jq](https://jqlang.github.io/jq/) 與 [yq](https://github.com/mikefarah/yq/releases/tag/v4.44.3)

---

### 回家如何自建 workshop 環境

```
VERSION=v4.44.3
BINARY=yq_darwin_amd64
wget https://github.com/mikefarah/yq/releases/download/${VERSION}/${BINARY} -O yq
chmod +x yq
sudo mv yq /usr/bin/yq
```

---

### etcd 基礎操作: 啟動一台 etcd

一行一行執行底下指令，來啟動一台 etcd

```
cd etcd-playground
ls

cd 00-prerequsites/
cat docker-compose.yaml 

docker compose up -d
docker ps
docker logs -f etcd-0
```

卡住時 ctrl + c to exit

只領打一半可以按 tab auto complete

---

### etcd 基礎操作: etcdctl

https://etcd.io/docs/v3.5/tutorials/ 中的幾個範例
- Reading from etcd
- Writing to etcd

```
etcdctl get foo
etcdctl put foo "Hello World"
etcdctl get foo
```

---

### etcd 基礎操作: etcdctl

https://etcd.io/docs/v3.5/tutorials/ 中的幾個範例
- How to get keys by prefix

```
etcdctl get --prefix "" 
etcdctl get "" --prefix --keys-only

etcdctl put foo2 2
etcdctl put foo5 5
etcdctl put foo4 4
etcdctl put foo3 3

etcdctl get foo --prefix --keys-only
etcdctl get foo --prefix --keys-only --sort-by=KEY --limit=5
etcdctl get foo --prefix --keys-only --sort-by=MODIFY --limit=5
```

---

### etcd 基礎操作: etcdctl

請嘗試操作 https://etcd.io/docs/v3.5/tutorials/ 中的幾個範例
- How to delete keys
- How to watch keys
- How to check Cluster status

```
etcdctl del foo

etcdctl put k1 value1
etcdctl put k2 value2
etcdctl del --prefix k
```

---

### etcd 基礎操作: 重啟 etcd

透過以下 command 重啟 etcd
- `docker ps` 確認 etcd 是否還在運行

```
docker ps
docker compose down
docker ps
docker compose up -d
```

---

### etcd 基礎操作: Quiz

1. 重啟 etcd 後，是否還能讀取到 foo 的值？為什麼？
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

### etcd 基礎操作: Answer

1. 本 workshop 的 docker-compose.yml 中，etcd 的資料是存放在本地的 etcd0 資料夾中，因此重啟後，資料不會遺失。透過以下指令可以清除 etcd0 資料夾中的資料
2. https://etcd.io/docs/v3.5/learning/why/

```
cd 00-prerequsites/
sudo ls etcd0
sudo ls etcd0/member

docker compose down --volumes
sudo rm -rf etcd0/*

# 新的 etcd
docker compose up -d
ls etcd0
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
- https://etcd.io/docs/v3.5/op-guide/authentication/

##### 卡住乃兵家常事，大俠請重新來過即可

```
docker compose down --volumes
sudo rm -rf etcd0/*
```

---

### 加分題為自己加分：authentication

```
# 可能會用到的 cmd
etcdctl role add
etcdctl role grant-permission
etcdctl user add
etcdctl user list
etcdctl auth status
etcdctl auth enable
```

---

### etcd Clusters: 移除舊的 etcd

- 先關閉 01-prerequsites 的 etcd
- 透過 `--volumes` 刪除 docker volume
- 刪除 etcd local volume 資料夾

```
docker compose down --volumes
sudo rm -rf etcd0/*
```

---

### etcd Clusters: 啟動多台 etcd

```
cd ../
cd 01-cluster/
cat docker-compose.yaml 

docker compose up -d
docker ps
```

---

### etcd Clusters: 檢視狀態

- 預設 etcdctl 會連線到 --endpoints=[127.0.0.1:2379]
- 使用 --endpoints 指定要連線到的 etcd
- 使用 export ETCDCTL_ENDPOINTS 指定要連線到的 etcd

```
etcdctl endpoint status
etcdctl --endpoints "http://127.0.0.1:2379,http://127.0.0.1:2380" endpoint status
etcdctl --endpoints "http://127.0.0.1:2379,http://127.0.0.1:2380,http://127.0.0.1:2381" endpoint status

export ETCDCTL_ENDPOINTS="http://127.0.0.1:2379,http://127.0.0.1:2380,http://127.0.0.1:2381"
etcdctl --endpoints $ETCDCTL_ENDPOINTS endpoint status
etcdctl endpoint status

```

---

### etcd Clusters: 檢視狀態

https://etcd.io/docs/v3.5/tutorials/
- How to check Cluster status
- 透過 `--help` 檢查每個欄位的意義

```
etcdctl endpoint status
etcdctl endpoint status --help

etcdctl endpoint health
etcdctl endpoint health --help
etcdctl endpoint hashkv
etcdctl endpoint hashkv --help
```

---

### etcd Clusters: 操作 Member

- member 是 etcd cluster 中的一個節點
- leader 是 etcd cluster 中的一個 member
- 透過 `move-leader` 指令，可以交接 leader

```
etcdctl --write-out=table endpoint status

docker exec -it etcd-1 etcdctl move-leader 88d11e2649dad027
etcdctl --write-out=table endpoint status
```

---

### etcd Clusters: Member

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

sudo rm -rf etcd3/member
docker start etcd-3
etcdctl member list
```

---

### 閱讀資料

- https://etcd.io/docs/v3.5/faq/
- https://etcd.io/docs/v3.5/learning/design-learner/
- https://etcd.io/docs/v3.5/learning/persistent-storage-files/

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

- 確定 etcd cluster 都正常運行
  - 裡面沒有資料，有的話可以刪除，啟動新的 etcd
- 透過 docker 啟動 K8s Control Plane
  - kube-apiserver
  - kube-controller-manager
  - kube-scheduler

```
etcdctl member list
docker ps -a

etcdctl get "" --prefix --keys-only
```

---

### K8s: 搭建 K8s Control Plane

- 透過底下指令，啟動 k8s control plane
  - 這是一個極度簡化的 k8s control plane
  - 正式環境不會長這樣

```
cd 02-control-panel

cd certs
./generate.sh

cd ../
cat docker-compose.yaml
docker compose up -d
docker ps
docker logs kube-apiserver
docker logs kube-controller-manager
docker logs kube-scheduler
```

---

https://kubernetes.io/docs/concepts/overview/components/

![](https://kubernetes.io/images/docs/components-of-kubernetes.svg)

---

### K8s: kubectl

- 透過 etcdctl 檢查目前的 etcd 資料內容
- kubectl 是 Kubernetes 的 CLI 工具，可以透過 kubectl 存取 k8s control plane

```
etcdctl get "" --prefix --keys-only

kubectl --kubeconfig=certs/admin.kubeconfig cluster-info
kubectl --kubeconfig=certs/admin.kubeconfig get all -A
```

---

### K8s: data in etcd

- 使用 etcdctl 存取 k8s 的資料
- jq
- yq
- 選幾個 `/registry` 的 key，探索更多 k8s 內容

```
etcdctl get "/" --prefix --keys-only --sort-by=KEY

etcdctl get /registry/namespaces/default -w json | jq
etcdctl get /registry/namespaces/default -w json | yq -P
```

---

### K8s: data in etcd

k8s 運行時，會將資料存放在 etcd 中
- 透過 kubectl create namespace workshop 創建一個 namespace
- 透過 etcdctl 存取 workshop namespace 的資料

```
etcdctl get "/registry/namespaces" --prefix --keys-only --sort-by=KEY

kubectl --kubeconfig=certs/admin.kubeconfig create namespace workshop

etcdctl get /registry/namespaces/workshop -w json | yq -P
```

---

### K8s: the hard way

[kelseyhightower/kubernetes-the-hard-way](https://github.com/kelseyhightower/kubernetes-the-hard-way/tree/master) 是一個很棒的學習資源，可以讓你了解到 Kubernetes 的每個細節
- 這次重點在於 etcd，我們只操作到 etcd 的部分
- k8s 的部分，在於 k8s 跟 etcd 的互動
- 有功能的 k8s 還需要部署 node

---

### K8s: ./generate.sh

[certs/generate.sh](https://github.com/chechiachang/etcd-playground/blob/main/02-control-panel/certs/generate.sh) 有附上對應的 k8s-the-hard-way 的說明文件
- ca 與 certs 是部署 k8s control plane 的必要檔案
- 非常花時間，本 workshop 會直接使用腳本產生
- 加分題：鼓勵大家自己操作過一次 certs 的產生

```
vi certs/generate.sh
ls certs
```

---

### K8s: 認識 control plane components

- https://kubernetes.io/docs/concepts/overview/components/

```
ls apiserver
ls controller-manager
ls scheduler
```

---

### K8s: etcd operations for k8s

k8s 官方文件中，從維運 k8s 角度，講述如何維運 etcd

- https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/
- [Securing etcd Clusters](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#securing-etcd-clusters) 放在加分題

---

### K8s: etcd backup and restore

[backing-up-an-etcd-cluster](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#backing-up-an-etcd-cluster)

- etcdctl 確定 leader 與 raft index
- 向 leader node 發送 snapshot request
- 輸出到 /etcd_data/snapshot.db，會顯示在 etcd1 資料夾中

```
etcdctl --write-out=table endpoint status

docker exec -it etcd-1 etcdctl snapshot save /etcd_data/snapshot.db
ls etcd1
```

---

### K8s: etcd backup and restore

[restoring-an-etcd-cluster](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#restoring-an-etcd-cluster)

- 停止 k8s control plane (apiserver)
- 複製 snapshot.db 到 etcd2 與 etcd3 資料夾中
- 對每一個 etcd member 執行 restore
- 或是針對 leader 執行 restore
- 觀察 raft index 的變化

```
docker stop kube-apiserver

cp etcd1/snapshot.db etcd2/snapshot.db
cp etcd1/snapshot.db etcd3/snapshot.db

docker exec -it etcd-1 etcdctl snapshot restore /etcd_data/snapshot.db
docker exec -it etcd-2 etcdctl snapshot restore /etcd_data/snapshot.db
docker exec -it etcd-3 etcdctl snapshot restore /etcd_data/snapshot.db

etcdctl --write-out=table endpoint status
```

---

### 加分題為自己加分：增加 etcd member

[scaling-out-etcd-clusters](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#scaling-out-etcd-clusters)

- 修改 01-cluster/docker-compose.yaml
- 調整底下 comment 中的部分，修改 ? 的地方
- 增加兩台 etcd member 到 cluster 中

```
# 可能會用到的 cmd
etcdctl member list
etcdctl member add <id> --peer-urls=
etcdctl member list
docker compose up -d
```

---

### 加分題為自己加分：自己做 ca and tls certs

- 不使用 generate.sh 產生 certs，拉起 k8s control plane
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

### 加分題為自己加分: 搭建 K8s Node

https://github.com/kelseyhightower/kubernetes-the-hard-way/blob/master/docs/09-bootstrapping-kubernetes-workers.md


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
