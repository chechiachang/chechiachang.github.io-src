# Cloud Summit: Cloud Infrastructure Saving Engineering  雲端省錢工程

- Source: `content/slides/2024-07-03-saving-money-on-cloud-k8s/_index.md`
- Slide: `https://chechia.net/slides/2024-07-03-saving-money-on-cloud-k8s/`
- Date: `2024-07-01T12:45:00Z`
- Tags: `kafka, kubernetes`
- Categories: `kubernetes`
- Description: `分享幾個節省雲端開銷的方法，包含：導入 spot instance，成本計算與預測工具，動態資源調整HPA與VPA，saving plan`

## Pages (Section | Summary)

1. `(frontmatter)` | Frontmatter metadata for reveal-hugo settings and slide metadata.
2. `(frontmatter)` | 投影片跟講稿我都放在我的網站上，如果有興趣可以參考
3. `雲端K8s省錢工程` | 雲端K8s省錢工程
4. `關於我` | 關於我
5. `大綱` | 大綱
6. `動機` | 動機
7. `公有雲的費用` | 公有雲的費用
8. `今天只會講這個算力成本` | 今天只會講這個算力成本
9. `算力成本` | 算力成本
10. `尋找多餘的算力` | 尋找多餘的算力
11. `維持SLO` | 維持SLO
12. `基於 SLO 的成本調降` | 基於 SLO 的成本調降
13. `小結：成本控管的基本概念` | 小結：成本控管的基本概念
14. `k8s cpu / memory management` | k8s cpu / memory management
15. `How k8s manage cpu / memory` | How k8s manage cpu / memory
16. `上面都是概念，底下進實作` | 上面都是概念，底下進實作
17. `Monitoring 監控是成本控管的基礎` | Monitoring 監控是成本控管的基礎
18. `(frontmatter)` | No textual content.
19. `監測：調整前設定目標基準線` | 監測：調整前設定目標基準線
20. `(frontmatter)` | No textual content.
21. `監測: 調整後` | 監測: 調整後
22. `推薦監測工具` | 推薦監測工具
23. `(frontmatter)` | 大家都知道 prometheus 是什麼嗎？
24. `(frontmatter)` | https://grafana.com/grafana/dashboards/17375-k8s-resource-monitoring/
25. `導入成本分析與預測工具` | 導入成本分析與預測工具
26. `成本分析` | 成本分析
27. `(frontmatter)` | No textual content.
28. `成本分析：公有雲 billing` | 成本分析：公有雲 billing
29. `成本分析: Kubecost / Opencost` | 成本分析: Kubecost / Opencost
30. `(frontmatter)` | No textual content.
31. `(frontmatter)` | https://docs.kubecost.com/using-kubecost/navigating-the-kubecost-ui/cost-allocation
32. `(frontmatter)` | https://docs.kubecost.com/using-kubecost/navigating-the-kubecost-ui/cost-allocation/efficiency-idle
33. `推薦工具` | 推薦工具
34. `推薦工具: Kubecost / Opencost Savings` | 推薦工具: Kubecost / Opencost Savings
35. `推薦工具: KRR` | 推薦工具: KRR
36. `推薦工具: KRR` | 推薦工具: KRR
37. `(frontmatter)` | No textual content.
38. `推薦工具: KRR` | 推薦工具: KRR
39. `推薦工具: VPA recommendator` | 推薦工具: VPA recommendator
40. `推薦工具: 比較` | 推薦工具: 比較
41. `剛上手的做法` | 剛上手的做法
42. `小結` | 小結
43. `自動拓展：HPA` | 自動拓展：HPA
44. `自動拓展：HPA 的考量` | 自動拓展：HPA 的考量
45. `自動拓展：VPA` | 自動拓展：VPA
46. `Saving Plan / RI` | Saving Plan / RI
47. `Spot Instance` | Spot Instance
48. `Spot Instance` | Spot Instance
49. `Spot Instance: 如何開始` | Spot Instance: 如何開始
50. `小結` | 小結
51. `展望` | 展望
52. `小結` | 小結
53. `感謝` | 感謝
54. `(frontmatter)` | No textual content.

## Time-to-Syntax

- Markdown:
- `p3:link`
- `p4:link`
- `p14:link`
- `p15:link`
- `p22:link`
- `p26:link`
- `p29:link`
- `p33:link`
- `p34:link`
- `p35:link`
- `p36:code-fence`
- `p39:link`
- `p43:link`
- `p45:link`
- `p47:link`
- `p53:link`
- Hugo shortcode:
- `p2:{{< slide background-image="onepiece.png" >}}`
- `p2:{{% note %}}`
- `p2:{{% /note %}}`
- `p3:{{% note %}}`
- `p3:{{% /note %}}`
- `p5:{{% note %}}`
- `p5:{{% /note %}}`
- `p6:{{% note %}}`
- `p6:{{% /note %}}`
- `p7:{{% note %}}`
- `p7:{{% /note %}}`
- `p8:{{% note %}}`
- `p8:{{% /note %}}`
- `p9:{{% note %}}`
- `p9:{{% /note %}}`
- `p10:{{% note %}}`
- `p10:{{% /note %}}`
- `p11:{{% note %}}`
- `p11:{{% /note %}}`
- `p12:{{% note %}}`
- `p12:{{% /note %}}`
- `p13:{{% note %}}`
- `p13:{{% /note %}}`
- `p14:{{% note %}}`
- `p14:{{% /note %}}`
- `p15:{{% note %}}`
- `p15:{{% /note %}}`
- `p17:{{% note %}}`
- `p17:{{% /note %}}`
- `p18:{{< slide background-image="grafana-dashboard.png" >}}`
- `p19:{{% note %}}`
- `p19:{{% /note %}}`
- `p20:{{< slide background-image="grafana-cpu-dashboard.png" >}}`
- `p21:{{% note %}}`
- `p21:{{% /note %}}`
- `p23:{{< slide background-image="prometheus.png" >}}`
- `p23:{{% note %}}`
- `p23:{{% /note %}}`
- `p24:{{< slide background-image="grafana-cpu-usage.png" >}}`
- `p24:{{% note %}}`
- `p24:{{% /note %}}`
- `p25:{{% note %}}`
- `p25:{{% /note %}}`
- `p27:{{< slide background-image="azure-cost-management.jpeg" >}}`
- `p30:{{< slide background-image="kubecost.jpeg" >}}`
- `p31:{{< slide background-image="kubecost-allocation.jpeg" >}}`
- `p32:{{< slide background-image="kubecost-efficiency.png" >}}`
- `p34:{{% note %}}`
- `p34:{{% /note %}}`
- `p36:{{% note %}}`
- `p36:{{% /note %}}`
- `p37:{{< slide background-image="krr.jpeg" >}}`
- `p38:{{% note %}}`
- `p38:{{% /note %}}`
- `p39:{{% note %}}`
- `p39:{{% /note %}}`
- `p41:{{% note %}}`
- `p41:{{% /note %}}`
- `p42:{{% note %}}`
- `p42:{{% /note %}}`
- `p44:{{% note %}}`
- `p44:{{% /note %}}`
- `p45:{{% note %}}`
- `p45:{{% /note %}}`
- `p46:{{% note %}}`
- `p46:{{% /note %}}`
- `p48:{{% note %}}`
- `p48:{{% /note %}}`
- `p49:{{% note %}}`
- `p49:{{% /note %}}`
- `p51:{{% note %}}`
- `p51:{{% /note %}}`
- Reveal-hugo syntax:
- none.

## Time-to-Sentence

- Markdown:
- `p1:title: "Cloud Summit: Cloud Infrastructure Saving Engineering 雲端省錢工程"`
- `p5:最後講實務上要如何降低成本，例如 saving plan / spot instance / HPA / VPA，依照執行的難度排序，有時間的話也會講如何從無到有開始進行`
- `p8:Storage / Database / Networking 這幾個項目，我們下集再來談`
- `p9:如果你跟敝社一樣是 web service，那麼 cpu / memory 可能是你最大的一筆成本`
- `p10:多少才是夠？`
- `p10:多少才是夠？這是一個複雜的問題，實務上通常使用 SLA / SLO 來衡量服務品質，然後根據服務品質的要求，來設定 cpu / memory 的配額`
- `p10:甚至退一百步，防守性的來說，我們不希望因為降低 cpu / memory 的設定配額，為了省錢而導致負面的結果，甚至為服務的穩定度背鍋。`
- `p11:以維持各個服務元件的 SLO為前提，降低 cpu / memory 使用量`
- `p11:是一個很好的指標，如果你的服務是 99.9% 的 SLA，那麼你的服務就要保證 99.9% 的時間都是正常運作的，那麼你的 cpu / memory 就要足夠支持這個 SLA`
- `p12:負載穩定的元件，可以抓過去 30d 的 p99 cpu time 或 p99 memory usage + buffer`
- `p12:負載不穩定的元件，例如 cpu usage 與受活躍用戶數量正比，需要搭配 HPA 水平拓展`
- `p12:負載穩定的元件，固定吃多少 cpu / memory，他的附載不太容易隨外部因素波動的服務，可以抓過去 30d 的 p99 cpu time 或 p99 memory usage + buffer，然後降低 cpu / memory 的設定配額`
- `p14:k8s 如何管理 workload 的 cpu 與 memory`
- `p14:這裡面再講一下 k8s 如何管理 cpu / memory`
- `p15:How k8s manage cpu / memory`
- `p15:scheduler 依據 cpu / memory request 調度 pod`
- `p15:cpu 使用量依據 request 佔 node 比例分配`
- `p15:memory 使用 limit，超過 limit 會被 oomkill，並依據設定重啟`
- `p15:當前 node memory 不足時，會依據 pod request Evict pod`
- `p17:沒有監測就沒有 p99 cpu time / memory usage，也沒有 SLI/SLO`
- `p17:目前的 cpu / memory usage，runtime utilization 的資料`
- `p19:設定節省目標：ex. 過去 3 個月的 p99 資源用量`
- `p19:多餘的算力 = (分配的 resource - p99)`
- `p19:那如果我們把 cpu / memory 降低到 p99 / p99.9 服務品質會受到影響嗎？`
- `p23:大家都知道 prometheus 是什麼嗎？`
- `p23:我們想要知道一個 pod 會需要花多少 cpu / memory，你就把它跑起來，然後去紀錄跑起來的 pod 用了多少 cpu / memory，然後根據時間統計，你就可以拉出一張圖，看到這個 pod 用了多少 cpu / memory`
- `p23:你的 kubelet / cadvisor / container runtime 會知道你的 container 的 cpu / memory 使用量，包含 request & limit 然後是否有 throttling 或是 oomkill，這些資訊都會被 prometheus 收集起來，然後你可以透過其他工具，例如 kubecost 看到這些資訊`
- `p24:這是 prometheus 收集的資料，vm 的 resource 使用量的 grafana dashboard`
- `p28:有無更即時的成本分析工具？`
- `p40:kubecost 產生一個漂亮的 UI，krr 產生 command line 報表`
- `p40:VPA 需要 helm install，並且會需要 cluster 權限`
- `p41:用抓比例的方式動態調整，例如目前 request 距離 p99 request 差距 1000Mi，你先收 500Mi 回來試個水溫`
- `p41:先調降 request，提升單一 node 上的 pod 數量，然後觀察服務品質，如果服務品質沒有受到影響，那麼你可以進一步調降 limit`
- `p44:啟動的 liveness check / readiness check`
- `p44:需要持續調整 scale up / down 的條件與 time windows`
- `p44:scale up 對依賴服務的 loading 會有影響 ex. 後面的 db`
- `p44:loading 增加時 scale up time windows`
- `p45:Kubernetes 1.27: In-place Resource Resize for Kubernetes Pods (alpha)`
- `p45:In-Place Pod Resource Resizing always restarts pod`
- `p45:如果你的 workload 然後不適合做 HPA，但可以接受 resize 後重啟，那可以試試VPA`
- `p45:1.27 你可以把 InPlacePodVerticalScaling feature gate 開起來`
- `p45:他不保證 resize 後不會重啟 pod，還是要看你的 container runtime 支援程度`
- `p46:有 monitoring + prediction，基本上可以確定你會用多少資源，這時候就可以考慮 saving plan / RI`
- `p49:將 worklaod 從 monolithic 拆分成小的 batch job`
- `p49:乍看之下幾個小時~24hr 內會被重啟，好像是犧牲了服務品質，但如果你的服務是可以容忍 interruption 的，例如 batch job，那麼 spot instance 就是一個很好的選擇`
- `p49:將 worklaod 從 monolithic 拆分成小的 batch job，例如你是 api server 處理一個 request 會有很多步驟，你可以把這些步驟拆分成小的 batch job，然後用 queue 串接，這樣你的 api server 就可以用 spot instance 來跑，然後你的 batch job 用 spot instance 跑，這樣你的服務就可以省很多錢`
- Hugo shortcode:
- `p2:{{< slide background-image="onepiece.png" >}}`
- `p2:{{% note %}}`
- `p2:{{% /note %}}`
- `p3:{{% note %}}`
- `p3:{{% /note %}}`
- `p5:{{% note %}}`
- `p5:{{% /note %}}`
- `p6:{{% note %}}`
- `p6:{{% /note %}}`
- `p7:{{% note %}}`
- `p7:{{% /note %}}`
- `p8:{{% note %}}`
- `p8:{{% /note %}}`
- `p9:{{% note %}}`
- `p9:{{% /note %}}`
- `p10:{{% note %}}`
- `p10:{{% /note %}}`
- `p11:{{% note %}}`
- `p11:{{% /note %}}`
- `p12:{{% note %}}`
- `p12:{{% /note %}}`
- `p13:{{% note %}}`
- `p13:{{% /note %}}`
- `p14:{{% note %}}`
- `p14:{{% /note %}}`
- `p15:{{% note %}}`
- `p15:{{% /note %}}`
- `p17:{{% note %}}`
- `p17:{{% /note %}}`
- `p18:{{< slide background-image="grafana-dashboard.png" >}}`
- `p19:{{% note %}}`
- `p19:{{% /note %}}`
- `p20:{{< slide background-image="grafana-cpu-dashboard.png" >}}`
- `p21:{{% note %}}`
- `p21:{{% /note %}}`
- `p23:{{< slide background-image="prometheus.png" >}}`
- `p23:{{% note %}}`
- `p23:{{% /note %}}`
- `p24:{{< slide background-image="grafana-cpu-usage.png" >}}`
- `p24:{{% note %}}`
- `p24:{{% /note %}}`
- `p25:{{% note %}}`
- `p25:{{% /note %}}`
- `p27:{{< slide background-image="azure-cost-management.jpeg" >}}`
- `p30:{{< slide background-image="kubecost.jpeg" >}}`
- `p31:{{< slide background-image="kubecost-allocation.jpeg" >}}`
- `p32:{{< slide background-image="kubecost-efficiency.png" >}}`
- `p34:{{% note %}}`
- `p34:{{% /note %}}`
- `p36:{{% note %}}`
- `p36:{{% /note %}}`
- `p37:{{< slide background-image="krr.jpeg" >}}`
- `p38:{{% note %}}`
- `p38:{{% /note %}}`
- `p39:{{% note %}}`
- `p39:{{% /note %}}`
- `p41:{{% note %}}`
- `p41:{{% /note %}}`
- `p42:{{% note %}}`
- `p42:{{% /note %}}`
- `p44:{{% note %}}`
- `p44:{{% /note %}}`
- `p45:{{% note %}}`
- `p45:{{% /note %}}`
- `p46:{{% note %}}`
- `p46:{{% /note %}}`
- `p48:{{% note %}}`
- `p48:{{% /note %}}`
- `p49:{{% note %}}`
- `p49:{{% /note %}}`
- `p51:{{% note %}}`
- `p51:{{% /note %}}`
- Reveal-hugo syntax:
- none.
