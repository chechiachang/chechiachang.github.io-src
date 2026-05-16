# Kubernetes Summit: Upgrade A VM Based Cluster

- Source: `content/slides/2024-10-23-upgrade-k8s-cluster/_index.md`
- Slide: `https://chechia.net/slides/2024-10-23-upgrade-k8s-cluster/`
- Date: `2024-08-04T12:45:00Z`
- Tags: `kubernetes`
- Categories: `kubernetes`
- Description: `分享如何升級 VM-based Kubernetes Cluster 的版本，包含 etcd，control plane，與 node。升級前如何規劃，升級步驟該如何操作，升級後應該如何檢查。`

## Pages (Section | Summary)

1. `(frontmatter)` | Frontmatter metadata for reveal-hugo settings and slide metadata.
2. `Upgrade A VM Based Cluster` | Upgrade A VM Based Cluster
3. `(frontmatter)` | No textual content.
4. `今天的主題` | 今天的主題
5. `今天的目的` | 今天的目的
6. `背景：什麼是 VM-based Cluster` | 背景：什麼是 VM-based Cluster
7. `(frontmatter)` | No textual content.
8. `什麼是 VM-based Cluster` | 什麼是 VM-based Cluster
9. `(frontmatter)` | Self-hosted control plane
10. `所以為何要在AWS上自架 K8s？` | 所以為何要在AWS上自架 K8s？
11. `因為 2016 年的時候沒有 eks` | 因為 2016 年的時候沒有 eks
12. `2015- 年有很多 self-hosted k8s 解決方案` | 2015- 年有很多 self-hosted k8s 解決方案
13. `Self-hosted control plane` | Self-hosted control plane
14. `Self-hosted control plane: 壞處` | Self-hosted control plane: 壞處
15. `Self-hosted 多了要升級的東西` | Self-hosted 多了要升級的東西
16. `(frontmatter)` | No textual content.
17. `實際來看升級的步驟` | 實際來看升級的步驟
18. `實際升級的順序` | 實際升級的順序
19. `事前研究跟規劃` | 事前研究跟規劃
20. `K8s Release Cycle ~ 4 months` | K8s Release Cycle ~ 4 months
21. `(frontmatter)` | 加上 ~ 8 months patch release
22. `多久升級一次 k8s` | 多久升級一次 k8s
23. `升級變成 routine` | 升級變成 routine
24. `必讀文件 K8s CHANGELOG` | 必讀文件 K8s CHANGELOG
25. `不看 CHANGELOG 真的不行嗎？` | 不看 CHANGELOG 真的不行嗎？
26. `升級事前研究跟規劃` | 升級事前研究跟規劃
27. `需要升級的 K8s Components` | 需要升級的 K8s Components
28. `Etcd Upgrade 官方文件` | Etcd Upgrade 官方文件
29. `Etcd Upgrade 步驟` | Etcd Upgrade 步驟
30. `terraform for IaC` | terraform for IaC
31. `terraform gitflow` | terraform gitflow
32. `從專注完成升級，變成專注在自動化流程` | 從專注完成升級，變成專注在自動化流程
33. `Etcd Upgrade 該注意` | Etcd Upgrade 該注意
34. `kube-apiserver` | kube-apiserver
35. `apiserver doc` | apiserver doc
36. `Supported Version Skew` | Supported Version Skew
37. `api deprecated` | api deprecated
38. `使用工具掃描 k8s resource` | 使用工具掃描 k8s resource
39. `kube-no-trouble` | kube-no-trouble
40. `產生新版 apiserver VM` | 產生新版 apiserver VM
41. `移除舊版 apiserver graceful shutdown` | 移除舊版 apiserver graceful shutdown
42. `scheduler and controller manager` | scheduler and controller manager
43. `依賴 k8s api 的 app` | 依賴 k8s api 的 app
44. `app 升級檢查` | app 升級檢查
45. `(frontmatter)` | https://docs.nginx.com/nginx-ingress-controller/technical-specifications/
46. `(frontmatter)` | https://docs.nginx.com/nginx-ingress-controller/technical-specifications/
47. `小結：k8s control plane 升級` | 小結：k8s control plane 升級
48. `Node 升級` | Node 升級
49. `Node 升級簡單來說是建新拆舊` | Node 升級簡單來說是建新拆舊
50. `Node 升級需要搬移 worklaod` | Node 升級需要搬移 worklaod
51. `Workload retry` | Workload retry
52. `如何重啟有依賴的 Workload` | 如何重啟有依賴的 Workload
53. `驗證` | 驗證
54. `升級後跨環境測試` | 升級後跨環境測試
55. `K8s 升級有問題，不是有問題` | K8s 升級有問題，不是有問題
56. `好的監測是升級的保護傘` | 好的監測是升級的保護傘
57. `(frontmatter)` | 怎麼知道 k8s 升級有沒有壞？用 kubectl 打看看
58. `監測` | 監測
59. `監測參考工具` | 監測參考工具
60. `願景：自動化 k8s 升級` | 願景：自動化 k8s 升級
61. `We're hiring!` | We're hiring!
62. `參考資料` | 參考資料

## Time-to-Syntax

- Markdown:
- `p2:link`
- `p7:image`
- `p7:link`
- `p9:image`
- `p12:link`
- `p13:link`
- `p15:link`
- `p16:image`
- `p16:link`
- `p20:image`
- `p20:link`
- `p21:image`
- `p21:link`
- `p24:link`
- `p27:image`
- `p27:link`
- `p29:link`
- `p34:image`
- `p34:link`
- `p37:link`
- `p38:link`
- `p39:image`
- `p43:link`
- `p45:image`
- `p46:image`
- `p48:link`
- `p49:image`
- `p49:link`
- `p57:code-fence`
- `p59:link`
- `p61:image`
- `p62:link`
- Hugo shortcode:
- `p2:{{% note %}}`
- `p2:{{% /note %}}`
- `p3:{{< slide content="slides.about-me" >}}`
- `p12:{{% note %}}`
- `p12:{{% /note %}}`
- Reveal-hugo syntax:
- none.

## Time-to-Sentence

- Markdown:
- `p1:title: "Kubernetes Summit: Upgrade A VM Based Cluster"`
- `p1:description: "分享如何升級 VM-based Kubernetes Cluster 的版本，包含 etcd，control plane，與 node。升級前如何規劃，升級步驟該如何操作，升級後應該如何檢查。"`
- `p6:Managed Kubernetes Service (GKE, EKS, AKS)`
- `p8:kubeadm, kops, kubespray / docker, containerd, cri-o / container or systemd / ...`
- `p8:自己管理 control plane，包含 etcd, apiserver, controller-manager, scheduler`
- `p8:依需求選用公有雲提供的架構，ex VPC, ELB, EBS, S3, RDS, IAM, Route53, CloudWatch, CloudTrail...`
- `p10:所以為何要在AWS上自架 K8s？`
- `p15:VM: based image / package / CVEs (不在今天的範圍)`
- `p18:必讀 K8s CHANGELOG / Urgent Upgrade Notes`
- `p18:檢查 app 的版本依賴 (i.e 升 k8s 會壞的 app)`
- `p19:每個小版號 Release Cycle ~ 4 months`
- `p20:K8s Release Cycle ~ 4 months`
- `p21:加上 ~ 8 months patch release`
- `p24:Urgent Upgrade Notes (No, really, you MUST read this before you upgrade)`
- `p24:最少要看 Urgent Upgrade Notes 跟 action required`
- `p25:不看 CHANGELOG 真的不行嗎？`
- `p25:一路從 app, infra, k8s resource, 查到 k8s 上的問題`
- `p29:etcd 在 minor version 升級時，可以 zero downtime rolling upgrade`
- `p29:delete then add member (維持 quorum 先減後增）`
- `p29:保留 etcd data 與 endpoint ip，開回後直接上線`
- `p29:只需 sync delete -> add 中間的資料差`
- `p30:要換的 etcd VM 可以拆解成 terraform module`
- `p30:data disk (etcd data) -> EBS`
- `p30:etcd config / flags -> launch template / cloud init`
- `p31:PR 改 binary etcd:v3.4.34 -> etcd:v3.5.4`
- `p31:PR review -> 自動 trigger terraform plan`
- `p31:PR merge -> 自動 apply dev / stag`
- `p31:沒問題: 人工確認上述步驟，開出 prod PR -> 自動 apply prod`
- `p35:apiserver 小版號 rolling upgrade zero downtime`
- `p35:如果建立 k8s 時有用工具/平台，ex kubeadm, kops, kubespray，會有對應的升級指令`
- `p36:controller manager, scheduler, cloud controller manager`
- `p36:apiserver 1.30 升 1.31 時，node 1.28, 1.29, 1.30 可以無痛`
- `p38:如何確認 app 的 k8s resource 有沒有使用到 deprecated API`
- `p38:app 開發的 CI 應該導入 lint --kube-version`
- `p38:如果有 app 使用到 deprecated API，通知 app owner 提早更新`
- `p40:Auto Scaling Group + Load balancer`
- `p40:更新apiserver binary -> S3 launch template / cloud formation`
- `p40:apiserver config / flags -> launch template / cloud init`
- `p41:load balancer -> auto scaling group -> EC2 instance`
- `p41:透過 load balancer 的設定，確保 apiserver 有足夠的時間離線`
- `p42:如果是 master VM (api-server, scheduler, controller manager, cloud controller manager)`
- `p44:掃描 k8s resource 使用的 api version 大部分掃得出來`
- `p44:以及如何升級 app controller 到新版的 k8s api`
- `p44:或是使用工具 or script 快速列出 cluster 內部的服務`
- `p48:有沒有 worklaod 依賴 k8s api (ex. client-go`
- `p48:有直接與 k8s api 互動的 app，強烈建議要寫 unit test`
- `p50:開新的 node，舊的 node 上的 workload 需要轉移`
- `p50:舊 node 打上 node taint，避免 worklaod 跑上去`
- `p50:app 彼此可能會有依賴關係，i.e. 重啟 a 時 b 會噴錯`
- `p51:app 要實作 auto retry，來處理暫時斷線與達到 auto recovery`
- `p51:ex. backend + in-k8s redis，大量的 backend pod 同時重啟，會打壞 redis`
- `p53:針對 worklaod 有設定 monitoring 與 metrics`
- `p53:ex. api 在重啟過程中噴 5xx，5xx 的次數異常增加，自動 alert`
- `p53:ex. non 2xx 的 access log 量增加`
- `p54:chaos engineering 在平時就持續注入 error，根據 scenario 設定 k8s 的反應`
- `p54:load testing 測試 app 在新版本 k8s 上的效能`
- `p61:We're hiring!`
- Hugo shortcode:
- `p2:{{% note %}}`
- `p2:{{% /note %}}`
- `p3:{{< slide content="slides.about-me" >}}`
- `p12:{{% note %}}`
- `p12:{{% /note %}}`
- Reveal-hugo syntax:
- none.
