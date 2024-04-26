---
title: "SRE Conference: Cloud Infrastructure Saving Engineering  雲端省錢工程"
summary: 分享幾個節省雲端開銷的方法，包含：導入 spot instance，成本計算與預測工具，動態資源調整HPA與VPA，saving plan
authors: []
tags: ["kafka", "kubernetes"]
categories: ["kubernetes"]
date: '2024-03-26T00:00:00Z'
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
投影片跟講稿我都放在我的網站上，如果有興趣可以參考
{{% /speaker_note %}}

---

### Cost Management of Cloud Kubernetes
### 雲端K8s省錢工程

[Che Chia Chang](https://chechia.net/)

{{% speaker_note %}}
兩個關鍵字：雲端 / k8s
如果你有在使用公有雲，而且有在跑 k8s，你是這篇演講的最主要對象
如果你是私有雲 k8s，或是其他的雲端服務，有一些相通的概念，會有一些參考價值
如果你是地端的機器，雖然概念相同，但成本控制的做法完全是另外一個故事，你可以當午休時間的故事聽聽看
{{% /speaker_note %}}

---

### About Me
### Che Chia Chang

- SRE @ [Maicoin](https://www.linkedin.com/company/maicoin/jobs/)
- [Microsoft MVP](https://mvp.microsoft.com/zh-TW/MVP/profile/e407d0b9-5c01-eb11-a815-000d3a8ccaf5)
- 個人部落格[chechia.net](https://chechia.net/)
- presentation and speaker notes
- 鐵人賽 (Terraform / Vault 手把手入門)

---

### Outline

- Cost on Public Cloud
- K8s Compute Resource Management
- Monitoring
- Cost Analysis and Prediction
- Resource Recommendation
- Saving Plan
- Spot Instance
- HPA / VPA
- Q&A

{{% speaker_note %}}
這是我們今天的大綱

我們會先講一下在公有雲上的成本
然後講一下 k8s 的運算資源管理
接著講一下監控，為何成本控管的基礎是監控
如何使用工具成本分析，未來成本預測
然後使用工具建議合適的資源
最後講實務上要如何降低成本，例如 saving plan / spot instance / HPA / VPA，依照執行的難度排序，有時間的話也會講如何從無到有開始進行
{{% /speaker_note %}}

---

### Cost on Public Cloud

open your cloud billing

- Compute Resource (cpu, memory)
- Storage (Disk, EBS, S3...)
- Database (Compute Resource + Storage)
- Networking

{{% speaker_note %}}
有在使用公有雲的人，把公有雲的 billing 帳單打開來看，可能看到的大概是這幾個項目
當然因為不同團隊的服務不同，可能會有一些出入，但如果你的公司的產品是 web service，應該會有這幾個項目
{{% /speaker_note %}}

---

### Today's topic

- Today's topic
  - Compute Resource
  - cpu & memory

- Maybe next time
  - Storage (Disk, EBS, S3...)
  - Database (Compute Resource + Storage)
  - Networking

{{% speaker_note %}}
Storage 不太好說省就省，因為你的資料量就在那邊，放不下就是要再買，所以 storage 的成本控制，可能是在資料的使用上，例如資料的壓縮，或是資料的備份，或是資料的存取方式，這些是另外一個故事
使用公有雲的服務，基本上 storage 都是依據使用的大小計價，而且需多服務都可以動態增長，例如動態增加 disk

Storage / Database / Networking 這幾個項目，我們下集再來談
{{% /speaker_note %}}

---

### Cost on Public Cloud

CPU / memory intense web service
- RESTful api
- long-connetion service
- business logic
- save state to disk / database 

{{% speaker_note %}}
如果你跟敝社一樣是 web service，那麼 cpu / memory 可能是你最大的一筆成本

你需要足夠運算能力 serve 客戶，不管是支持用戶的request，進行商業邏輯的運算，然後把運算完成的狀態回傳給客戶，或是存在資料庫中，每一個動作都需要算力

足夠的 cpu 跟 memory，不是越多越好，而是足夠，不會浪費，也不會因為不足而影響服務品質
我們要省錢，就要從這裡下手
{{% /speaker_note %}}

---

### 尋找多餘的算力

- 已有足夠的 cpu / memory，多給也不會增加服務品質的多餘算力
- 多少才是夠？
- 減去多少 cpu / memory，依然不改變服務品質

{{% speaker_note %}}
多少才是夠？這是一個複雜的問題，實務上通常使用 SLA / SLO 來衡量服務品質，然後根據服務品質的要求，來設定 cpu / memory 的配額

我們今天要做的是成本優化，白話的說是降低 cpu / memory 的設定配額，但是我們不能降低到影響服務品質
甚至退一百步，防守性的來說，我們不希望因為降低 cpu / memory 的設定配額，為了省錢而導致負面的結果，甚至為服務的穩定度背鍋。
{{% /speaker_note %}}

---

### 維持SLO

以維持各個服務元件的 SLO為前提，降低 cpu / memory 使用量

{{% speaker_note %}}
維持個個服務元件的 SLO
是一個很好的指標，如果你的服務是 99.9% 的 SLA，那麼你的服務就要保證 99.9% 的時間都是正常運作的，那麼你的 cpu / memory 就要足夠支持這個 SLA

談 SLO 之前，你要先知道你的服務的 SLA 是多少，你要先知道當前的狀態是多少
這個在稍後的 monitoring 會提到，為什麼監控是成本管理的基礎
{{% /speaker_note %}}

---

### 基於 SLO 的成本調降

- 負載穩定的元件，可以抓過去 30d 的 p99 cpu time 或 p99 memory usage + buffer
- 負載不穩定的元件，例如 cpu usage 與受活躍用戶數量正比，需要搭配 HPA 水平拓展
- 負載不穩定的元件，但又不能水平拓展，例如 stateful service，可以考慮 VPA

{{% speaker_note %}}
負載穩定的元件，固定吃多少 cpu / memory，他的附載不太容易隨外部因素波動的服務，可以抓過去 30d 的 p99 cpu time 或 p99 memory usage + buffer，然後降低 cpu / memory 的設定配額
{{% /speaker_note %}}

---

### 小結：成本控管的基本概念

- 尋找服務中多餘算力
- 以維持 SLO 為前提
- 降低 cpu / memory 使用量
- 依據元件負載特性，選擇適當的調降方式

{{% speaker_note %}}
{{% /speaker_note %}}

---

### Background Knowledge
### [k8s cpu / memory management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers)

https://kubernetes.io/docs/concepts/configuration/manage-resources-containers

- k8s 如何管理 workload 的 cpu 與 memory
- 調降多少會影響服務品質

{{% speaker_note %}}
這裡面再講一下 k8s 如何管理 cpu / memory

這邊的重點是，怎麼樣的調整會影響到服務品質，那我們做成本控制的時候，就不要去踩到這個底線
{{% /speaker_note %}}

---

### [How k8s manage cpu / memory](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#how-pods-with-resource-limits-are-run)

- scheduler 依據 cpu / memory request 調度 pod
- container runtime 設定 cgroup
  - cpu 使用量依據 request 佔 node 比例分配
  - 控制 cpu 用量不超過 limit
  - memory 使用 limit，超過 limit 會被 oomkill，並依據設定重啟
  - 當前 node memory 不足時，會依據 pod request Evict pod

{{% speaker_note %}}
文件講得很清楚
{{% /speaker_note %}}

---

### 上面都是概念，底下進實作

---

### Monitoring

- Monitoring 是 cost management 的基礎
- 沒有 monitoring 就沒有 p99 cpu time / p99 memory usage，也沒有 SLI/SLO
- 如果沒有 monitoring 先補 monitoring

{{% speaker_note %}}
如果沒有 monitoring，上面的兩大前提都不存在
目前的 cpu / memory usage，runtime utilization 的資料
目前SLO，調降之後新的SLO
{{% /speaker_note %}}

---

{{< slide background-image="grafana-dashboard.png" >}}

---

### Monitoring: 調整前

- 過去的 p99 資源用量
- 目前的效能表現
- 多餘的算力 = (分配的 resource - p99)

{{% speaker_note %}}
做之前要能評估做完大概能省多少
例如評估完後

如果評估完發現省不了什麼錢，那當然團隊就不一定要做這件事
{{% /speaker_note %}}

---

### Monitoring: 調整後

調整前後比較
- 資源用量
- 目前的效能表現
- 確定沒有改壞東西
- 有改壞，要有及時的 alert

{{% speaker_note %}}
如果你改壞了，及時的 alert 會救你一命
{{% /speaker_note %}}

---

### Monitoring Tools

- [prometheus.io](https://prometheus.io/)
- [Kubecost / Opencost](https://docs.kubecost.com/using-kubecost)

---

{{< slide background-image="prometheus.png" >}}

{{% speaker_note %}}
大家都知道 prometheus 是什麼嗎？

知道的人請舉個手
不知道的我很簡單說一下

我們想要知道一個 pod 會需要花多少 cpu / memory，你就把它跑起來，然後去紀錄跑起來的 pod 用了多少 cpu / memory，然後根據時間統計，你就可以拉出一張圖，看到這個 pod 用了多少 cpu / memory
你的 kubelet / cadvisor / container runtime 會知道你的 container 的 cpu / memory 使用量，包含 request & limit 然後是否有 throttling 或是 oomkill，這些資訊都會被 prometheus 收集起來，然後你可以透過其他工具，例如 kubecost 看到這些資訊
{{% /speaker_note %}}

---

{{< slide background-image="grafana-cpu-usage.png" >}}

https://grafana.com/grafana/dashboards/17375-k8s-resource-monitoring/

{{% speaker_note %}}
這是 prometheus 收集的資料，vm 的 resource 使用量的 grafana dashboard
{{% /speaker_note %}}

---

### Cost Analysis and Prediction

- 有了 prometheus 後，我們知道短期/長期的資源使用狀況
- 要把資源使用轉成成本，需要一個成本計算工具
- 評估是否要做成本精簡，能夠減少多少錢
- 管理上的考量：投資人力成本，與預期回報

{{% speaker_note %}}

政治上的考量，做成本節省需要時間跟人力資源
有一個精準的成本分析，節省空間估算的工具十分有說服力

有這些資料，才可以科學化決策要不要做，該怎麼做
做之前就能評估做完大概能省多少

如果評估完發現省不了什麼錢，那當然團隊就不一定要做這件事

{{% /speaker_note %}}

---

### Cost Analysis:  billing

- 各家公有元都有自己的費用計算工具
- [Azure Cost Management](https://azure.microsoft.com/en-us/products/cost-management)
- [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/)
- [GCP Cost Breakdown](https://cloud.google.com/billing/docs/how-to/cost-breakdown)

---

{{< slide background-image="azure-cost-management.jpeg" >}}

---

### Cost Analysis: Cloud billing

- 計算長時間的費用趨勢
- 適合當作成本精簡後的成果回報
- 不適合當做調整的依據
- 時間計算較長，反饋時間長，不及時，項目不夠精細
- 有無更即時的成本分析工具？

---

### Cost Analysis: [Kubecost / Opencost](https://docs.kubecost.com/using-kubecost/)

- 有提供 UI
- 基於 prometheus
- 可以針對 allocation 做成本分析 [Cost Allocation](https://docs.kubecost.com/using-kubecost/navigating-the-kubecost-ui/cost-allocation)
- 可以透過 cloud provider 去撈雲端的使用資料

---

{{< slide background-image="kubecost.jpeg" >}}

---

{{< slide background-image="kubecost-allocation.jpeg" >}}

https://docs.kubecost.com/using-kubecost/navigating-the-kubecost-ui/cost-allocation

---

{{< slide background-image="kubecost-efficiency.png" >}}

https://docs.kubecost.com/using-kubecost/navigating-the-kubecost-ui/cost-allocation/efficiency-idle

---

### Recommedation Tools

- [https://github.com/robusta-dev/krr](https://github.com/robusta-dev/krr)
- [Kubecost / Opencost Savings](https://docs.kubecost.com/using-kubecost/navigating-the-kubecost-ui/savings)
- [VPA recommendator](https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/pkg/recommender/README.md)

---

### Recommedation Tools: [Kubecost / Opencost Savings](https://docs.kubecost.com/using-kubecost/navigating-the-kubecost-ui/savings)

- 設定 target utilization
  - dev 80%+
  - prod 60%

{{% speaker_note %}}
根據服務品質的要求，以及公司政策去做設定
SLA/SLO
開發與測試環境，在不影響工作的前提，都可以拉到 overcommit
{{% /speaker_note %}}

---

### Recommedation Tools: KRR

- [https://github.com/robusta-dev/krr](https://github.com/robusta-dev/krr)
- 免安裝，不影響 k8s 本身
- 使用外部工具讀取 prometheus 資料

---

### Recommedation Tools: KRR

```
kubectl port-forward svc/prometheus 9090

git clone https://github.com/robusta-dev/krr.git
source .venv/bin/activate

python krr.py simple \
  -p http://127.0.0.1:9090 \
  --mem-min 10 \
  --cpu-min 10 \
  --history_duration 720 -q
```

{{% speaker_note %}}
{{% /speaker_note %}}

---

{{< slide background-image="krr.jpeg" >}}

---

### Recommedation Tools: KRR

- 根據 krr 計算的結果，手動調整
- 有一些工具有提供自動調整 ex VPA

{{% speaker_note %}}
自動工具比手動需要考量更多因素，這個我們稍候 VPA 再提

請詳閱工具說明再服用
{{% /speaker_note %}}

---

### Recommedation Tools: [VPA recommendator](https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/pkg/recommender/README.md)

- 需要先知道 VPA 是什麼
- 直接安裝在 k8s cluster 內
- 透過 Prometheus 資料，推薦適當的資源
- 可以自動化推薦資源，調整運行中的 pod，依照設定重啟 pod [VPA mode](https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/README.md#quick-start)
- 需要可以參考 [helm chart](https://github.com/cowboysysop/charts/tree/master/charts/vertical-pod-autoscaler)

{{% speaker_note %}}
krr 是可以無腦用的工具，但是 VPA 就不是了
請設定 VPA mode Off
請務必需要研究一下在使用
{{% /speaker_note %}}

---

### Recommedation Tools: 比較

- kubecost 需要 helm install，krr 不需要
- kubecost 產生一個漂亮的 UI，krr 產生 command line 報表

- VPA 需要 helm install，並且會需要 cluster 權限
- VPA 可以做到自動化調整，邏輯更複雜，有侵入性，設定有問題會出事

---

### 剛上手的做法

沒時間細部研究研究元件的行為，直接調整 request 與 limit

- 先調降 request，不動 limit，對服務衝擊較小
- 用抓比例的方式動態調整，例如目前 request 距離 p99 request 差距 1000Mi，你先收 500Mi 回來試個水溫
- p99 直接使用 tool 計算，細節在後面
- 測試環境先行，有信心在上 production

{{% speaker_note %}}
如果你第一次做，但對服務元件沒有熟到這種程度，這是比較安全的做法
公司規模大服務元件複雜，身為 SRE 你只能仰賴 metrics 來判斷服務品質是否受影響，但很多複雜的服務，以及不熟悉的服務，會很難評估

先調降 request，提升單一 node 上的 pod 數量，然後觀察服務品質，如果服務品質沒有受到影響，那麼你可以進一步調降 limit
市場喊價，先喊個一半，在看能繼續壓到什麼程度
{{% /speaker_note %}}

---

### 小結

- 收集目前資源使用資料
- 轉化成公有雲的成本
- 透過 tool 建議適當的資源
- 根據服務品質的要求，調降 cpu / memory
- 回頭檢查 SLO 是否有受到影響

{{% speaker_note %}}
{{% /speaker_note %}}

---

### HPA

- [k8s/horizontal-pod-autoscale](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- 使用 HPA 在成本精簡的意義：因為外部因素改變負載的元件
- 低負載時不要開太多，高負載時自動加開 pod

---

### HPA: 考量

元件是否能夠水平拓展
- 啟動的 liveness check / readiness check
- laod balancer
- 需要持續調整 scale up / down 的條件與 time windows
- scale up 對依賴服務的 loading 會有影響 ex. 後面的 db
- 退場機制，要如何安全的中斷連線，紀錄 state

{{% speaker_note %}}
要能安全地進出場

進場，pod readiness / liveness
loading 增加時 scale up time windows
scale out 對後方服務的影響，是否會出現新的瓶頸

loading 降低時 scale down 是否會影響服務
{{% /speaker_note %}}

---

### VPA

- [k8s/autoscaler/vertical-pod-autoscaler](https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/README.md#quick-start)
- 不能水平拓展，只好先垂直拓展
- 調整資源，有可能會重啟 pod / container
- [Kubernetes 1.27: In-place Resource Resize for Kubernetes Pods (alpha)](https://kubernetes.io/blog/2023/05/12/in-place-pod-resize-alpha/)
- [In-Place Pod Resource Resizing always restarts pod](https://github.com/kubernetes/kubernetes/issues/122760)
- 如果你的 workload 然後不適合做 HPA，但可以接受 resize 後重啟，那可以試試VPA

{{% speaker_note %}}
1.27 你可以把 InPlacePodVerticalScaling feature gate 開起來
他不保證 resize 後不會重啟 pod，還是要看你的 container runtime 支援程度
請先在測試環境中玩一玩
{{% /speaker_note %}}

---

### Saving Plan / RI

- AWS Saving Plan / RI
- GCP Committed Use Discount
- Azure Reservation

{{% speaker_note %}}
Saving Plan / RI 是一種長期的合約，你可以跟雲端服務商簽約，保證你會用多少資源，然後雲端服務商會給你一個折扣
七折上下，很適合長期使用的客戶

有 monitoring + prediction，基本上可以確定你會用多少資源，這時候就可以考慮 saving plan / RI
{{% /speaker_note %}}

---

### Spot Instance

- [azure spot vm](https://azure.microsoft.com/en-us/products/virtual-machines/spot)
- [aws spot intance](https://aws.amazon.com/ec2/spot/)
- [gcp spot vm](https://cloud.google.com/spot-vms)
- 帳面上最高可省 90%

---

### Spot Instance

- 超便宜，打一折
- 多餘的算力
- interruption，不保證使用
- https://aws.amazon.com/ec2/spot/instance-advisor/

{{% speaker_note %}}
因為一折真的很香，一折是有點拼，但打個 3 折還是很有機會
{{% /speaker_note %}}

---

### Spot Instance: 分類 workload

interruption 直接影響服務品質的就不宜

不影響服務品質的
- stateless
- batch job
- 將 worklaod 從 monolithic 拆分成小的 batch job
- 測試環境 dev / stag
- CI/CD

{{% speaker_note %}}

乍看之下幾個小時~24hr 內會被重啟，好像是犧牲了服務品質，但如果你的服務是可以容忍 interruption 的，例如 batch job，那麼 spot instance 就是一個很好的選擇

將 worklaod 從 monolithic 拆分成小的 batch job，例如你是 api server 處理一個 request 會有很多步驟，你可以把這些步驟拆分成小的 batch job，然後用 queue 串接，這樣你的 api server 就可以用 spot instance 來跑，然後你的 batch job 用 spot instance 跑，這樣你的服務就可以省很多錢

{{% /speaker_note %}}

---

### 小結

- krr 工具調整資源
- HPA 做水平擴展
- VPA 自動化調整資源
- saving plan / RI 長期合約打七折
- spot instance 打一折

---

### 展望

- cost awareness development
- find-grade optimization
- automation

{{% speaker_note %}}
有了資源預測系統，可以在開發階段就將資源使用回饋給開發團隊
根據不同服務元件的品質要求，做更細緻的資源管控
自動化調整，讓人力可以專注在更重要的事情上
{{% /speaker_note %}}

---

### 小結

- cpu / memory
- 監測是基礎
- 依據監測做預測
- 開始調整
- 長期合約打七折
- spot instance 打一折
- HPA / VPA

--- 

### 感謝

- presentation and speaker notes [chechia.net](https://chechia.net/)

- [Maicoin 職缺](https://www.linkedin.com/company/maicoin/jobs/)
- 公司福利不錯，業務成長中，想一起共事，歡迎找我聊

