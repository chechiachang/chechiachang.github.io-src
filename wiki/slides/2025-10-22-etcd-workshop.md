# K8s Summit 2025: Workshop: Get started with Etcd & Kubernetes

- Source: `content/slides/2025-10-22-etcd-workshop/_index.md`
- Slide: `https://chechia.net/slides/2025-10-22-etcd-workshop/`
- Date: `2025-06-25T00:45:00Z`
- Tags: `iac, aws, terraform, kubernetes, etcd`
- Categories: `kubernetes, workshop`
- Description: `Etcd 是 Kubernetes 的重要元件之一，本次工作坊將帶領觀眾初探 Etcd，包含安裝，設定，以及操作。並藉由本地的 Etcd 來架設一個最簡單的 Kubernetes Cluster。工作坊內容請見投影片`

## Pages (Section | Summary)

1. `(frontmatter)` | Frontmatter metadata for reveal-hugo settings and slide metadata.
2. `Etcd workshop 行前準備` | Etcd workshop 行前準備
3. `Kubernetes Summit 2025` | Kubernetes Summit 2025
4. `(frontmatter)` | 🔽
5. `We're hiring!` | We're hiring!
6. `大綱` | 大綱
7. `如何進行 workshop` | 如何進行 workshop
8. `準備環境` | 準備環境
9. `選項1: 存取遠端VM` | 選項1: 存取遠端VM
10. `選項1: 存取遠端VM` | 選項1: 存取遠端VM
11. `選項2: 使用非 ubuntu 的電腦` | 選項2: 使用非 ubuntu 的電腦
12. `選項3: 產生 ubuntu VM 的環境` | 選項3: 產生 ubuntu VM 的環境
13. `確認大家都有操作環境` | 確認大家都有操作環境
14. `(frontmatter)` | https://kubernetes.io/docs/concepts/overview/components/
15. `(frontmatter)` | https://kubernetes.io/docs/concepts/overview/components/
16. `etcd 基礎操作: 啟動一台 etcd` | etcd 基礎操作: 啟動一台 etcd
17. `etcd 基礎操作: 啟動一台 etcd` | etcd 基礎操作: 啟動一台 etcd
18. `etcd 基礎操作: etcdctl` | etcd 基礎操作: etcdctl
19. `etcd 基礎操作: etcdctl` | etcd 基礎操作: etcdctl
20. `etcd 基礎操作: etcdctl` | etcd 基礎操作: etcdctl
21. `etcd 基礎操作: 重啟 etcd` | etcd 基礎操作: 重啟 etcd
22. `etcd 基礎操作: Quiz` | etcd 基礎操作: Quiz
23. `etcd 基礎操作: Answer` | etcd 基礎操作: Answer
24. `閱讀資料` | 閱讀資料
25. `加分題為自己加分：authentication` | 加分題為自己加分：authentication
26. `加分題：如何使用 vim 編輯 docker-compose.yaml` | 加分題：如何使用 vim 編輯 docker-compose.yaml
27. `加分題卡住乃兵家常事，大俠請重新來過即可` | 加分題卡住乃兵家常事，大俠請重新來過即可
28. `加分題為自己加分：authentication` | 加分題為自己加分：authentication
29. `etcd Clusters: 準備啟動多台 etcd` | etcd Clusters: 準備啟動多台 etcd
30. `etcd Clusters: 啟動多台 etcd` | etcd Clusters: 啟動多台 etcd
31. `etcd Clusters: 檢視狀態` | etcd Clusters: 檢視狀態
32. `etcd Clusters: 多台 etcd 架構圖` | etcd Clusters: 多台 etcd 架構圖
33. `etcd Clusters: 檢視狀態` | etcd Clusters: 檢視狀態
34. `etcd Clusters: raft basic` | etcd Clusters: raft basic
35. `etcd Clusters: 什麼是 Raft 共識算法` | etcd Clusters: 什麼是 Raft 共識算法
36. `etcd Clusters: 操作 Member` | etcd Clusters: 操作 Member
37. `etcd Clusters: Remove member` | etcd Clusters: Remove member
38. `removed member 會關閉` | 移除一個 member，name: etcd-3 id: c3697a4fd7a20dcd
39. `etcd Clusters: 多台 etcd 架構圖` | etcd Clusters: 多台 etcd 架構圖
40. `etcd Clusters: Add member` | etcd Clusters: Add member
41. `etcd Clusters: add member 後的 etcd 架構圖` | etcd Clusters: add member 後的 etcd 架構圖
42. `etcd Clusters: 替換 member 要先減後增` | etcd Clusters: 替換 member 要先減後增
43. `閱讀資料` | 閱讀資料
44. `加分題為自己加分：tls` | 加分題為自己加分：tls
45. `K8s: 搭建 K8s Control Plane` | K8s: 搭建 K8s Control Plane
46. `K8s: 搭建 K8s Control Plane` | K8s: 搭建 K8s Control Plane
47. `(frontmatter)` | https://kubernetes.io/docs/concepts/overview/components/
48. `K8s: kubectl` | K8s: kubectl
49. `K8s: data in etcd` | K8s: data in etcd
50. `K8s: data in etcd` | K8s: data in etcd
51. `K8s: the hard way` | K8s: the hard way
52. `K8s: ./generate.sh` | K8s: ./generate.sh
53. `K8s: 認識 control plane components` | K8s: 認識 control plane components
54. `K8s: etcd operations for k8s` | K8s: etcd operations for k8s
55. `K8s: etcd backup and restore` | K8s: etcd backup and restore
56. `K8s: etcd backup and restore` | K8s: etcd backup and restore
57. `加分題為自己加分：增加 etcd member` | 加分題為自己加分：增加 etcd member
58. `加分題為自己加分：自己做 ca and tls certs` | 加分題為自己加分：自己做 ca and tls certs
59. `加分題為自己加分: 增加 apiserver` | 加分題為自己加分: 增加 apiserver
60. `加分題為自己加分: 搭建 K8s Node` | 加分題為自己加分: 搭建 K8s Node
61. `參考資料` | 參考資料

## Time-to-Syntax

- Markdown:
- `p3:link`
- `p5:image`
- `p9:code-fence`
- `p9:link`
- `p10:image`
- `p11:code-fence`
- `p11:link`
- `p12:link`
- `p13:code-fence`
- `p13:link`
- `p14:image`
- `p16:code-fence`
- `p18:code-fence`
- `p19:code-fence`
- `p20:code-fence`
- `p21:code-fence`
- `p22:code-fence`
- `p22:link`
- `p23:code-fence`
- `p26:code-fence`
- `p27:code-fence`
- `p28:code-fence`
- `p29:code-fence`
- `p30:code-fence`
- `p31:code-fence`
- `p33:code-fence`
- `p34:code-fence`
- `p36:code-fence`
- `p38:code-fence`
- `p40:code-fence`
- `p45:code-fence`
- `p46:code-fence`
- `p47:image`
- `p48:code-fence`
- `p49:code-fence`
- `p50:code-fence`
- `p51:link`
- `p52:code-fence`
- `p52:link`
- `p53:code-fence`
- `p54:link`
- `p55:code-fence`
- `p55:link`
- `p56:code-fence`
- `p56:link`
- `p57:code-fence`
- `p57:link`
- Hugo shortcode:
- `p4:{{% section %}}`
- `p4:{{< slide content="slides.about-me" >}}`
- `p5:{{% /section %}}`
- `p13:{{% section %}}`
- `p15:{{% /section %}}`
- `p17:{{< mermaid >}}`
- `p17:{{< /mermaid >}}`
- `p32:{{< mermaid >}}`
- `p32:{{< /mermaid >}}`
- `p39:{{< mermaid >}}`
- `p39:{{< /mermaid >}}`
- `p41:{{< mermaid >}}`
- `p41:{{< /mermaid >}}`
- Reveal-hugo syntax:
- none.

## Time-to-Sentence

- Markdown:
- `p1:title: "K8s Summit 2025: Workshop: Get started with Etcd & Kubernetes"`
- `p1:description: "Etcd 是 Kubernetes 的重要元件之一，本次工作坊將帶領觀眾初探 Etcd，包含安裝，設定，以及操作。並藉由本地的 Etcd 來架設一個最簡單的 Kubernetes Cluster。工作坊內容請見投影片"`
- `p1:tags: ["iac", "aws", "terraform", "kubernetes", "etcd"]`
- `p2:本次 workshop 以 hands-on 的方式進行，累積操作經驗為主，講解與說明為輔。觀念內容有準備教材，需要參與者自行閱讀。講師會免費提供 Azure VM 供同學遠端操作使用。`
- `p2:選項2: 使用自己的電腦，遠端連線講師提供的 VM，在VM 中啟動 docker 開發環境`
- `p3:Get started with Etcd & Kubernetes`
- `p3:~ Che Chia Chang @ chechia.net ~`
- `p5:We're hiring!`
- `p8:選項1: 使用任何電腦，遠端連線講師提供的 VM，在VM 中啟動 docker 開發環境`
- `p8:選項2: 使用非 ubuntu (mac, windows) VM / 電腦，在本機 docker 啟動開發環境`
- `p8:選項3: 使用 ubuntu VM / 電腦，在本機 docker 啟動開發環境`
- `p9:googel sheet 左邊 url，開啟 bastion 連線`
- `p11:mac, linux 或 windows 都可以(用 windows 可能會有指令格式相容性問題)`
- `p12:workshop 提供的機器，是 ubuntu 24.04 + docker 環境。安裝這些東西，即可自行產生一台 workshop 環境`
- `p13:git clone repository + docker compose up -d`
- `p15:> Consistent and highly-available key value store used as Kubernetes' backing store for all cluster data.`
- `p15:例如 AWS 的 EKS, Azure 的 AKS, GCP 的 GKE`
- `p16:卡住時 ctrl + c to exit`
- `p17:C -- Azure ssh bastion --> B`
- `p19:How to get keys by prefix`
- `p19:etcdctl get foo --prefix --keys-only --sort-by=KEY --limit=5`
- `p19:etcdctl get foo --prefix --keys-only --sort-by=MODIFY --limit=5`
- `p22:重啟 etcd 後，是否還能讀取到 foo 的值？為什麼？`
- `p22:請用50個字，描述你目前覺得 etcd 是什麼？`
- `p23:本 workshop 的 docker-compose.yml 中，etcd 的資料是存放在本地的 etcd0 資料夾中，因此重啟後，資料不會遺失。透過以下指令可以清除 etcd0 資料夾中的資料`
- `p26:輸入 冒號WQ (:wq) + enter 儲存並離開 vim`
- `p26:卡住可以嘗試連按 esc 鍵，然後輸入 :q! + enter 強制離開 vim`
- `p31:endpoint, ID, version, db size, is leader, is learner, raft term, raft index, raft applied index, errors`
- `p31:127.0.0.1:2379, b8c6addf901e4e46, 3.5.15, , 688 kB, 541 kB, 22%, 0 B, false, false, 5, 2104, 2104, , , false`
- `p31:找到那個 node 是 leader 了嗎? （每個人的結果可能不一樣）`
- `p34:請找到 raft term 與 raft index`
- `p34:讀取資料，raft index 會有什麼變化嗎?`
- `p36:leader 是 etcd cluster 中的一個 member`
- `p36:raft term 與 raft index 有什麼變化嗎?`
- `p37:How to Add and Remove Members`
- `p40:被移掉的是 etcd-1 還是 etcd-2 還是 etcd-3?`
- `p40:把 node 的 disk volume 刪掉`
- `p40:更改 docker-compose.yaml 中，該 node --initial-cluster-state=new 為 --initial-cluster-state=existing`
- `p40:etcdctl 添加 member 到 cluster 中`
- `p41:etcd Clusters: add member 後的 etcd 架構圖`
- `p42:Proposal (ex. update key/value) requires a majority quorum (n/2 +1)`
- `p42:3 nodes -> majority is 2，3 nodes 中，2 個 node 同意即可達成共識`
- `p42:3 - 1 = 2 nodes -> majority is 2，3 nodes 減掉 1 個 node 後，2 個 node 仍然可以達成共識`
- `p42:if 3 + 1 = 4 nodes -> majority is 3，3 nodes 增加 1 個 node 後，4 個 node 需要 3 個 node 同意才能達成共識`
- `p42:4 nodes vs 2 nodes 的風險一樣，都是 -1 node 後，就無法達成共識`
- `p44:啟用 etcd cluster 的 tls，並讓 etcdcetl 透過 tls 連線`
- `p45:確定 01-cluster 的 etcd cluster 都正常運行`
- `p45:透過 docker 啟動 K8s Control Plane`
- `p48:kubectl 是 Kubernetes 的 CLI 工具，可以透過 kubectl 存取 k8s control plane`
- `p49:選幾個 /registry 的 key，探索更多 k8s 內容`
- `p49:etcdctl get "/" --prefix --keys-only --sort-by=KEY`
- `p49:etcdctl get /registry/namespaces/default -w json | jq`
- `p49:etcdctl get /registry/namespaces/default -w json | yq -P`
- `p50:透過 kubectl create namespace workshop 創建一個 namespace`
- `p50:透過 etcdctl 存取 workshop namespace 的資料`
- `p50:etcdctl get "/registry/namespaces" --prefix --keys-only --sort-by=KEY`
- `p50:etcdctl get /registry/namespaces/workshop -w json | yq -P`
- `p51:k8s 的部分，在於 k8s 跟 etcd 的互動`
- `p52:ca 與 certs 是部署 k8s control plane 的必要檔案`
- `p55:etcdctl 確定 leader 與 raft index`
- `p55:向 leader node 發送 snapshot request`
- `p55:docker exec -it etcd-1 etcdctl snapshot save /etcd_data/snapshot.db`
- `p56:複製 snapshot.db 到 etcd2 與 etcd3 資料夾中`
- `p56:docker exec -it etcd-1 etcdctl snapshot restore /etcd_data/snapshot.db`
- `p56:docker exec -it etcd-2 etcdctl snapshot restore /etcd_data/snapshot.db`
- `p56:docker exec -it etcd-3 etcdctl snapshot restore /etcd_data/snapshot.db`
- `p57:增加兩台 etcd member 到 cluster 中`
- `p58:不使用 generate.sh 產生 certs，拉起 k8s control plane`
- `p58:將 generate.sh 的內容，到 terminal 中一段一段 copy paste 執行`
- Hugo shortcode:
- `p4:{{% section %}}`
- `p4:{{< slide content="slides.about-me" >}}`
- `p5:{{% /section %}}`
- `p13:{{% section %}}`
- `p15:{{% /section %}}`
- `p17:{{< mermaid >}}`
- `p17:{{< /mermaid >}}`
- `p32:{{< mermaid >}}`
- `p32:{{< /mermaid >}}`
- `p39:{{< mermaid >}}`
- `p39:{{< /mermaid >}}`
- `p41:{{< mermaid >}}`
- `p41:{{< /mermaid >}}`
- Reveal-hugo syntax:
- none.
