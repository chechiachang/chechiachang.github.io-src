# Kubernetes Summit: Get started with etcd & Kubernetes

- Source: `content/slides/2024-10-24-etcd-workshop/_index.md`
- Slide: `https://chechia.net/slides/2024-10-24-etcd-workshop/`
- Date: `2024-08-05T00:45:00Z`
- Tags: `etcd, kubernetes`
- Categories: `kubernetes`
- Description: `etcd 是 Kubernetes 的重要元件之一，本次工作坊將帶領觀眾初探 etcd，包含安裝，設定，以及操作。並藉由本地的 etcd 來架設一個最簡單的 Kubernetes Cluster。`

## Pages (Section | Summary)

1. `(frontmatter)` | Frontmatter metadata for reveal-hugo settings and slide metadata.
2. `etcd Workshop` | etcd Workshop
3. `etcd Workshop` | etcd Workshop
4. `關於我` | 關於我
5. `We're hiring!` | We're hiring!
6. `大綱` | 大綱
7. `如何進行 workshop` | 如何進行 workshop
8. `如何存取遠端VM` | 如何存取遠端VM
9. `回家如何自建 workshop 環境` | 回家如何自建 workshop 環境
10. `回家如何自建 workshop 環境` | 回家如何自建 workshop 環境
11. `etcd 基礎操作: 啟動一台 etcd` | etcd 基礎操作: 啟動一台 etcd
12. `etcd 基礎操作: etcdctl` | etcd 基礎操作: etcdctl
13. `etcd 基礎操作: etcdctl` | etcd 基礎操作: etcdctl
14. `etcd 基礎操作: etcdctl` | etcd 基礎操作: etcdctl
15. `etcd 基礎操作: 重啟 etcd` | etcd 基礎操作: 重啟 etcd
16. `etcd 基礎操作: Quiz` | etcd 基礎操作: Quiz
17. `etcd 基礎操作: Answer` | etcd 基礎操作: Answer
18. `閱讀資料` | 閱讀資料
19. `加分題為自己加分：authentication` | 加分題為自己加分：authentication
20. `加分題為自己加分：authentication` | 加分題為自己加分：authentication
21. `etcd Clusters: 移除舊的 etcd` | etcd Clusters: 移除舊的 etcd
22. `etcd Clusters: 啟動多台 etcd` | etcd Clusters: 啟動多台 etcd
23. `etcd Clusters: 檢視狀態` | etcd Clusters: 檢視狀態
24. `etcd Clusters: 檢視狀態` | etcd Clusters: 檢視狀態
25. `etcd Clusters: 操作 Member` | etcd Clusters: 操作 Member
26. `etcd Clusters: Member` | etcd Clusters: Member
27. `(frontmatter)` | 移除一個 member，name: etcd-3 id: c3697a4fd7a20dcd
28. `閱讀資料` | 閱讀資料
29. `加分題為自己加分：authentication` | 加分題為自己加分：authentication
30. `K8s: 搭建 K8s Control Plane` | K8s: 搭建 K8s Control Plane
31. `K8s: 搭建 K8s Control Plane` | K8s: 搭建 K8s Control Plane
32. `(frontmatter)` | https://kubernetes.io/docs/concepts/overview/components/
33. `K8s: kubectl` | K8s: kubectl
34. `K8s: data in etcd` | K8s: data in etcd
35. `K8s: data in etcd` | K8s: data in etcd
36. `K8s: the hard way` | K8s: the hard way
37. `K8s: ./generate.sh` | K8s: ./generate.sh
38. `K8s: 認識 control plane components` | K8s: 認識 control plane components
39. `K8s: etcd operations for k8s` | K8s: etcd operations for k8s
40. `K8s: etcd backup and restore` | K8s: etcd backup and restore
41. `K8s: etcd backup and restore` | K8s: etcd backup and restore
42. `加分題為自己加分：增加 etcd member` | 加分題為自己加分：增加 etcd member
43. `加分題為自己加分：自己做 ca and tls certs` | 加分題為自己加分：自己做 ca and tls certs
44. `加分題為自己加分: 增加 apiserver` | 加分題為自己加分: 增加 apiserver
45. `加分題為自己加分: 搭建 K8s Node` | 加分題為自己加分: 搭建 K8s Node
46. `參考資料` | 參考資料

## Time-to-Syntax

- Markdown:
- `p3:link`
- `p4:link`
- `p5:image`
- `p8:code-fence`
- `p8:link`
- `p9:link`
- `p10:code-fence`
- `p11:code-fence`
- `p12:code-fence`
- `p13:code-fence`
- `p14:code-fence`
- `p15:code-fence`
- `p16:code-fence`
- `p16:link`
- `p17:code-fence`
- `p19:code-fence`
- `p20:code-fence`
- `p21:code-fence`
- `p22:code-fence`
- `p23:code-fence`
- `p24:code-fence`
- `p25:code-fence`
- `p27:code-fence`
- `p30:code-fence`
- `p31:code-fence`
- `p32:image`
- `p33:code-fence`
- `p34:code-fence`
- `p35:code-fence`
- `p36:link`
- `p37:code-fence`
- `p37:link`
- `p38:code-fence`
- `p39:link`
- `p40:code-fence`
- `p40:link`
- `p41:code-fence`
- `p41:link`
- `p42:code-fence`
- `p42:link`
- Hugo shortcode:
- `p3:{{% note %}}`
- `p3:{{% /note %}}`
- `p6:{{% note %}}`
- `p6:{{% /note %}}`
- Reveal-hugo syntax:
- none.

## Time-to-Sentence

- Markdown:
- `p1:title: "Kubernetes Summit: Get started with etcd & Kubernetes"`
- `p1:description: "etcd 是 Kubernetes 的重要元件之一，本次工作坊將帶領觀眾初探 etcd，包含安裝，設定，以及操作。並藉由本地的 etcd 來架設一個最簡單的 Kubernetes Cluster。"`
- `p3:手把手搭建 etcd 與 K8s control plane`
- `p5:We're hiring!`
- `p11:卡住時 ctrl + c to exit`
- `p13:How to get keys by prefix`
- `p13:etcdctl get foo --prefix --keys-only --sort-by=KEY --limit=5`
- `p13:etcdctl get foo --prefix --keys-only --sort-by=MODIFY --limit=5`
- `p16:重啟 etcd 後，是否還能讀取到 foo 的值？為什麼？`
- `p16:請用50個字，描述你目前覺得 etcd 是什麼？`
- `p17:本 workshop 的 docker-compose.yml 中，etcd 的資料是存放在本地的 etcd0 資料夾中，因此重啟後，資料不會遺失。透過以下指令可以清除 etcd0 資料夾中的資料`
- `p25:leader 是 etcd cluster 中的一個 member`
- `p25:docker exec -it etcd-1 etcdctl move-leader 88d11e2649dad027`
- `p26:How to Add and Remove Members`
- `p29:啟用 etcd cluster 的 tls，並讓 etcdcetl 透過 tls 連線`
- `p30:透過 docker 啟動 K8s Control Plane`
- `p33:kubectl 是 Kubernetes 的 CLI 工具，可以透過 kubectl 存取 k8s control plane`
- `p34:選幾個 /registry 的 key，探索更多 k8s 內容`
- `p34:etcdctl get "/" --prefix --keys-only --sort-by=KEY`
- `p34:etcdctl get /registry/namespaces/default -w json | jq`
- `p34:etcdctl get /registry/namespaces/default -w json | yq -P`
- `p35:透過 kubectl create namespace workshop 創建一個 namespace`
- `p35:透過 etcdctl 存取 workshop namespace 的資料`
- `p35:etcdctl get "/registry/namespaces" --prefix --keys-only --sort-by=KEY`
- `p35:etcdctl get /registry/namespaces/workshop -w json | yq -P`
- `p36:k8s 的部分，在於 k8s 跟 etcd 的互動`
- `p37:ca 與 certs 是部署 k8s control plane 的必要檔案`
- `p40:etcdctl 確定 leader 與 raft index`
- `p40:向 leader node 發送 snapshot request`
- `p40:docker exec -it etcd-1 etcdctl snapshot save /etcd_data/snapshot.db`
- `p41:複製 snapshot.db 到 etcd2 與 etcd3 資料夾中`
- `p41:docker exec -it etcd-1 etcdctl snapshot restore /etcd_data/snapshot.db`
- `p41:docker exec -it etcd-2 etcdctl snapshot restore /etcd_data/snapshot.db`
- `p41:docker exec -it etcd-3 etcdctl snapshot restore /etcd_data/snapshot.db`
- `p42:增加兩台 etcd member 到 cluster 中`
- `p43:不使用 generate.sh 產生 certs，拉起 k8s control plane`
- `p43:將 generate.sh 的內容，到 terminal 中一段一段 copy paste 執行`
- Hugo shortcode:
- `p3:{{% note %}}`
- `p3:{{% /note %}}`
- `p6:{{% note %}}`
- `p6:{{% /note %}}`
- Reveal-hugo syntax:
- none.
