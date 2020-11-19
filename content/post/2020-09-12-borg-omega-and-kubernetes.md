---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Borg Omega and Kubernetes Translation 全文翻譯"
subtitle: ""
summary: ""
authors: []
tags: ["kubernetes", "google", "borg"]
category: ["kubernetes"]
date: 2020-09-12T13:50:52+08:00
lastmod: 2020-09-12T13:50:52+08:00
featured: true
draft: false

---

# 前言

這是原文完整版本。太長不讀 (TL;DR) 請見[Borg Omega and Kubernetes 前世今生摘要]({{< ref "/post/2020-08-26-borg-omega-and-kubernetes-tldr" >}})

原文：https://storage.googleapis.com/pub-tools-public-publication-data/pdf/44843.pdf

# 摘要

在 container 技術夯起來前，Google 已經做了 container 十幾年，過程中發展出需三套容器管理系統。雖然每一代系統的開發需求不同，但每一代都深受上一代影響。這篇文章描述 Google 開發這些系統時，學到的經驗。

第一套 container management 系統是 Borg，為了管理 1. 長期執行的服務 2. 批次的短期工作 (batch job)，原本分別是由 Babysitter 與 Global Work Queue 兩套系統分開管理。後者的架構深刻影響 Borg，但 Global Work Queue 專注於 batch job。兩套系統都在 Linux control groups 之前。Borg 將上述兩種應用放在共享的機器上，來增加資源的使用率，以節省成本。這種共享基於支援 container 的 Linux Kernel (Google 也貢獻許多 Linux kernel container 程式碼)，提供更好的隔離 (isolation) 給延遲敏感的使用者服務 (latency-sentitive user-facing services)，以及消耗大量 cpu 的 batch 程式。

越來越多應用都在 Borg 上開發執行， Google 的應用與 infratructure 團隊開發許多工具與服務，形成 Borg 生態系。這些系統提供設定 (configure) 與更新 (update) 工作、預測資源需求、動態推送設定到執行中的工作、服務發現 (service discovery) 與負載均衡 (Load balancing)，等等功能。這些生態系的開發基於 Google 不同團隊的需求，產生一個不同起源 (heterogeneous)、只針對各別需求的 (ad-hoc) 一個堆不同系統，Borg 的使用者需要使用不同的程式語言與程序，來與這些系統互動。Borg 仍然是 Google 主要的容器管理系統，因為他規模 (scale) 巨大，功能多樣，而且極度堅固 (robustness)。

Omega 是 Borg 的下一代，目的是改善 Borg 生態系的軟體工程。Omega 承襲許多 Borg 測試成功的模式，但不同於 Borg，Omega 有完整的架構設計，整體更加一致。Omega 將集群狀態 (cluster state) 存放在中心化 (centralized)、基於 Paxos 算法、交易導向 (transaction-oriented) 的儲存系統，讓集群的控制面板 (control panel) 存取，例如 scheduler。Omega 使用樂觀的併發控制 (optimistic concurrency control) 來處理偶發的衝突，這一層解藕 (decoupling) 的設計，使得原先的 Borgmaster 的功能可以拆分成多個元件，取代原本單一 (monolithic) 集中 (centralized) 的 master，被所有變更請求堵塞。許多 Omage 成功的創新也會被迭代回去 Borg 中。

第三套 Google 開發的容器管理系統是 Kubernetes，這時外界工程師也開始對 Linux 容器有興趣，而 Google 同時在開發並推展自己的公有雲架構。Kubernetes 在這樣的背景下構思並開發。與 Borg 及 Omega 不同，Kubernetes 是開源軟體，不限於 Google 內部開發。Kubernetes 內部有共享的持久層儲存 (persistent store)，服務元件持續監測有關物件，與 Omega 類似。不同的是，Omega 允許信任的控制面板的元件直接存取儲存庫，Kubernetes 則透過 domain-specific 的 REST API 存取，來提供高階 (higher-level) 的 API 版本控制、驗證、語意處理 (semantics)、以及存取政策 (policy)，來支援更廣泛的用戶端。更重要的是 Kubernetes 著重工程師在 cluster 上開發與執行應用的體驗，簡化複雜分散式系統 (distributed system) 的管理與部屬 (deploy)，同時仍能透過容器來提升資源的使用率。

這篇文章描述 Google 從 Borg 到 Kubernetes 獲得的知識與經驗。

# 容器 (Containers)

回顧歷史，第一個容器只提供 root file system (透過 chroot)。FreeBSD jail 進一步延伸出額外的命名空間 (namespace) 例如 process ID。Solaris 大幅地探索相關的新功能。Linux control groups (cgroups) 吸收這些想法，直到今日仍持續開發。

容器提供資源隔離 (resource isolation)，Google 得以大幅提升資源使用率 (utilization) 超出當時產業平均值，例如 Borg 使用容器，將批次暫時工作、與面對用戶需要注意延遲的應用，兩者放在同樣的物理機器上。用戶應用需要預留更多額外的資源，來處理突然產生的負載高峰 (load spikes) 以及錯誤處理 (fail-over) ，這些預留的資源常常都不會用到，可以轉讓批次工作使用。容器提供的資源管理工具實現此類需求，kernel-level 的資源隔離也確保程序之間不會互相干擾。Google 開發 Borg 中，同時也提交新功能給 Linux 容器，來滿足上述的需求。然而目前的隔離並不完整，如果 Linux kernel 不管理的資源，容器自然也無法格理，例如 level-3 的處理器快取 (level-3 processor cache) 與記憶體帶寬 (memory bandwith)，容器還需要增加一層安全保護層 (例如虛擬機器 Virtual Machine) 才能對付公有雲上出現的惡意行為。

現代的容器不只提供隔離機制，更提供映像檔 (image)，在這個檔案上建構容器的應用。Google 使用 Midas Package Manager (MPM) 來建構並部屬容器映像檔，隔離機制與 MPM package 的關係，可以對比 Docker daemon 與 Docker image registry。這個章節描述的「容器」同時包含兩個概念：隔離、映像檔。

# 應用導向的架構 (Application-oriented infrastructure)

隨著時間證明，容器不只能提供高階的資源使用率，容器化 (containerization) 使資料中心 (data center) 從原本機器導向 (machine-oriented) 變成應用導向 (application-oriented)，這個段落提供兩個例子：

- 容器封裝 (encapsulate) 應用的環境 (environment)，在機器與作業系統的細節上，增加一層抽象層，解藕兩件事情：應用開發、部屬到架構。
- 良好設計的容器與映像檔只專注在單一個應用，管理容器意味管理應用，而不是管理機器。這點差異使得管理的 API，從機器導向變成影用導向，大幅度的改善應用的部屬與監控。


### 應用的環境 (Application environment)

原本 kernel 內的 cgroup、chroot、與命名空間，是用來保護應用不被旁邊其他應用的雜訊影響。將這些工具與容器映像檔一起使用，產生一層抽象層，分離應用、與底下的 (各種不同家的) 作業系統。解藕映像檔與作業系統，進一步提供相同的環境給開發環境 (development) 與生產環境 (production)，降低環境間的不一致性造成的問題，最終提升開發的可靠程度、並加速開發的流程。

建構這層抽象的關鍵是，使用密閉的容器映象檔 (hermetic container image) ，將所有應用有關的依賴 (dependencies) 都打包，整包部屬到容器中。正確執行的話，容器對外部的依賴只剩下 Linux kernel 系統調用介面 (system-call interface)。這層介面大幅改善映象檔的部屬方便性 (protability)，但目前機制仍不完美，應用仍然暴露在某些作業系統的介面上，特別是 socket options、/proc、以及 ioctl 的調用參數。Google 希望透過推廣開放容器倡議 (Open Container Initiative) 來清楚界定，上述介面與容器的抽象層。

次外，容器提供的隔離與最小依賴，在 Google 證明非常有效，容器是 Google 架構上唯一的可執行單位 (runnable entity)，進一步使 Google 只提供少數的作業系統版本給所有機器，只需要少數的維護人員來負責管理版本。

密閉容器映想檔有很多方式達成，在 Borg 建構映想檔時，應用的執行檔 (binary) 靜態連結到可用的程序庫 (library) 版本，程式庫在公司內部存放。至此 Borg 容器映像檔還不是完全密閉，底下還有依賴一層基底映象檔 (base image)，直接事先安裝到機器上，而不是隨映像檔部屬，基底映象檔包含通用工具例如 tar 與 libc 程式庫，因此更新基底映象檔仍會影響應用，偶爾會產生大麻煩。

現代的容器映像檔格式，如 Docker 與 ACI，都加強這層抽象、提供更緊密的封裝，移除特定作業系統的依賴性，並要求使用者在分享映象檔內容時，必須明確宣告。

### 容器作為管理單位 (Container as the unit of management)

圍繞容器建構管理 API，而非圍繞機器，使得資料中心的「Primary key」從機器變成應用。帶來許多好處：

1. 應用工程師與維運團隊 (operation team) 不需再煩惱機器與作業系統的細節
1. 架構團隊 (infrastructure team) 獲得更多升版或是調度硬體的彈性，實際對應用與開發團隊的影響非常小
1. 管理系統收集應用的監測數據 (例如 CPU 與 Memory 使用 metrics)，而非機器的監測數據，直接提升應用的監測與自我檢查 (introspection)，特別是擴展 (scale-up)、機器錯誤、或是維護時，造成應用移到其他位置時，監測依然可用。

容器提供許多切入點給泛用 API (generic API)，泛用 API 使資訊在管理系統與應用之間流動，但其實兩者互相不清楚對方的實作細節。在 Borg 中有一系列的 API 連結到所有容器，例如 /healthz 端點回報應用的健康程度給協調管理者 (orchestrator)，當發現不健康的應用，自動終止並重啟應用。這個自動修復功能是可靠的分散式系統的基礎。(Kubernetes 也提供類似功能，透過 HTTP 端點或是 exec command 來檢查容器內部的應用)

容器提供、或是提供給容器的資訊，可以透過許多使用者介面呈現。Borg 提供可以動態更新的文字狀態訊息，Kubernetes 提供 key-value 的 annotation 存放在給個物件的 metadata，這些都能溝通應用。annotation 可以是容器自行設定、或是由管理系統設定 (例如滾動更新版本時標註新版本)。

容器管理系統可以取得容器內部訊息，例如資源使用狀況、容器的 metadata，並傳播給日誌 (logging) 或是監控 (monitoring)，例如使用者名稱、監控任務名稱、用戶身分。甚至進一步在節點維護時，提早提供安全終止 (graceful-termination) 的警示。

容器有其他方式可以提供應用導向的監測，例如 Linux Kernel cgroups 會提供應用的資源使用率，這些資訊可以擴展，並將客製化的 metrics 構過 HTTP API 送出。基於這些資料，進一步開發出泛用工具如自動擴展 (auto-scaler) 與 cAdvisor，他們不需要知道應用的規格就可以記錄 metrics。由於容器本身是應用，因次不需要在實體或虛擬機器、與多個應用之間，做信號多工轉發或多路分配 (multiplex / demultiplex signals)。這樣更簡單、更堅固、並且可以產生精度更高的 metrics 與日誌，並提供更精細的控制操作。你可以對比使用 ssh 登入機器，並且使用 top 指令監測。雖然工程師可以 ssh 登入容器，但很少需要這樣做。

應用導向變遷在管理架構上產生更多回響，監測只是其中一個。Google 的附載均衡器 (load balancer) 不再根據機器做附載均衡，而是根據應用實體 (application instances)。日誌會根據應用打上標籤 (key) 而不是機器，因此可以跨機器的收集所有相同應用的日誌，而不會影響其他的應用日誌或是影像作業系統。我們可以檢測應用失效，更容易的描述錯誤原因，不需要先拆解處理機器的各層信號。由於容器實體的身分資訊，從基礎上都是由容器管理系統控制，工程師可以明確的指定應用的執行身分，使得應用更容易建構、管理、除錯。

最後，雖然上述都針對容器與應用在一對一的狀況下，但實務上我們需要套裝的容器群 (nested containers)，這群容器一起排程到相同機器上，最外層的容器提供資源，內層的容器提供部屬的隔離。Borg 中，最外層容器叫做資源分配 (resource allocation or alloc)，在 Kubernetes 上稱做 Pod。Borg 允許最上層的應用直接跑在外層的 alloc 上，但這點產生了一些不便，所以這點在 Kubernetes 做了調整，應用永遠跑在最外層 Pod 的內部，就算只有單一一個容器。

一個常見的使用情境，是一個 Pod 內部跑一個複雜的應用，大部分的應用都是一個一個子容器 (child containers)，其他的子容器則執行輔助工具，例如 log rotation 或是將日誌移轉到分散式檔案系統。對比把上述功能都打包到 binary 執行檔中，拆分更容易讓不同團隊各自開發負責的功能，拆分還提供更好的耐用程度 (就算主要應用終止，子容器仍能成功將日誌移轉出去)，更容易組裝應用 (composability) (由於每個服務都是獨立運作在各自的容器中，因此可以直接增加新的支援服務)，提供更精細的資源隔離 (所有容器資源隔離，所以日誌服務不會搶占主要應用的資源，反之亦然)。

# 協調管理只是開始，而不是終點 (Orchestration is the beginning, not the end)

Borg 的初衷只是分配不同的工作附載 (workload) 到相同的機器上，來提升資源使用率。然而 Borg 生態系中，支援系統的快速演化，表明容器管理系統本身只是一個起點：通往一個新的分散式系統開發與管理環境。許多新的系統在 Borg 上打造、嵌入 Borg、或是圍繞 Borg 打造，提升 Borg 的基本容器管理服務，底下是部分服務清單：

- 命名與服務發現 (Naming and service discovery) Borg Name Service (BNS)
- 主節點選舉 (master election) 使用 Chubby
- 應用感知的 (application-aware) 的負載均衡
- 自動水平擴展 (horizontal) 與垂直擴展 (vertical)
- 新的執行檔與設定檔的滾動升級工具 (rollout)
- 工作流程工具 (workflow) (例如在不同工作階段，執行多任務的分析 pipeline)
- 監控工具，可以收集容器資訊、整合統計、在 dashboard 上顯示、並可以觸發告警

這些服務都是用來處理開發團隊面臨的問題，Google 選出成功的服務並廣泛的應用，讓工程師工作更加輕鬆。然而這些工具大多各自需要特別的 (idiosyncratic) API，例如需要知道檔案的位置，也需要 Borg 的深度整合。產生一個不好的副作用，就是部屬 Borg 生態系變得更複雜了。

Kubernetes 試圖降低這些複雜度，因此導入一致性設計的 API (consistent API)，例如每個 Kubernetes 物件都會有三個基礎內容：ObjectMetadata、Specification (Spec)、以及 Status。

所有物件的 ObjectMetadata 都是一樣的，包含物件的名稱、UID、物件的版本 (作為樂觀併發控制 optimistic concurrency control 時使用)、標籤 (key-value label)。Spec 與 Status 的內容因物件型別有所不同，但核心概念一致：Spec 是描述期望狀態 (desired state)，而 Status 是紀錄物件的當前狀態 (current state)。

統一 API 帶來很多好處，從系統獲取資訊更加簡單：所有物件都有相同的資訊，才可以開發所有物件都適用的泛用工具，而這點更進一步，使工程師開發的使用體驗更加一致。從 Borg 與 Omega 中的經驗學習，所以 Kubernetes 是一堆組合的區塊打造而成，使用者還可以自行擴展。有統一的 API 以及 object-metadata 結構讓這件事更簡單。例如 Pod API 用戶可以使用、Kubernetes 內部元件也使用、外部的自動化工具也使用。一致性繼續延伸，Kubernetes 允許用戶動態增加客製化的 API，與 Kubernetes 核心的 API 一起工作。

一致性的促成也仰賴 Kubernetes 自身 API 的解藕。把各自元件的面向拆開，讓更高階的服務共享相同的底層基礎實作。例如拆分 Kubernetes 副本控制器 (replication controller) 與水平自動擴展系統 (horizontal auto-scaling system)，副本控制器確保一個腳色的 (ex. 前端網頁) 存在的數量符合期望的數量，自動擴展器則基於副本控制器的功能，只單純調整 Pods 的期望狀態 (desired state)，而不需負責 Pod 的增減，讓自動擴展器可以實作更多使用上的需求，例如預測使用，並可以忽略底下執行的實作細節。

API 解藕也讓許多關聯，但是不盡相同的元件構成近似。例如 Kubernetes 有三個形式的副本 Pod：

- ReplicationController：持續執行的容器副本 (例如 web server)
- DaemonSet：每個節點都有一個實體 (例如日誌收集器)
- Job：執行到工作完成的控制器，知道如何 (平行的) 啟動工作到結束工作

雖然有各自的執行政策 (policy) ，三個控制器都有相同的 Pod 物件，描述希望執行的容器。

一致性也仰賴 Kubernetes 內部元件的相同設計模式 (design patterns)。控制器調和迴圈 (reconciliation controller loop) 是 Borg、Omega、Kubernetes 都共享的設計理念，為了提升系統的彈性：迴圈不斷比對期望狀態 (要求多少符合 label-selector 的 Pod 存在)、與實際狀態 (控制器實際觀察到的數量)，然後控制器採取行動，盡量收斂 (converge) 實際狀況與期望狀況。由於所有行動都基於觀察結果，而非一個狀態圖，調和迴圈更能承受錯誤、更能抵抗擾亂、更加堅固：當一個控制器出錯，只要重啟，就可以繼續上次中斷的工作。

Kubernetes 設計成一堆微服務 (microservice) 的組合，並透過各個小型的控制迴圈 (control loop)，來達成整體的編排結果 (choreography) - 一個期望的狀態，由各個分散的自動元件，協作達成。這個意識的設計選擇，對比一個中心化協調管理系統 (centralized orchestration)，後者更容易建構，但面對不可預期的錯誤與變更時，更顯脆弱與僵化。

# 前車之鑑 (Things to avoid)

Google 在開發這些系統時，學到一些最好別做的事情，我們提供這些資訊，所以其他人可以避免重複的錯誤，而把犯錯的成本放在新的錯誤上。

### 不要使用容器管理系統管理 Port number

Borg 上所有容器都使用宿主機器的 IP，Borg 在分配時便指派給每個容器各自的 port number。每個容器移動到新機器時會取得一個新的 port number，有時在本機重啟也會拿到新的。這點表示既存的網路服務 (例如 DNS) Google 都必須自行改動並使用自維護的版本；服務的客戶端並不能主動獲得服務的 port number 資訊，需要被動告知；port number 也不能放在 URLs 中，還需要額外的轉址機制；所有基於 IP 運作的工具都需要改成使用 IP:Port。

有鑑於此，Kubernetes 上每個 Pod 分配一個 IP，讓應用的身分符合網路身分 (IP address)，讓現成的應用更容易在 Kubernetes 上執行，應用可以直接使用靜態的常規 port number (例如 HTTP 流量使用 80 port)，現有的工具也可以直接使用，例如網段切分 (network segmentation)、帶寬節流 (bandwidth throttling) 與控制。所有的公有雲都提供每個 Pod 一個 IP 的網路基底，在實體機器 (bare metal)，也可以使用軟體定義網路 (Software defined network) 的 overlay 網路，或是設定 L3 路由來配置機器上的 Pod IPs。

### 不要幫容器編號，使用 label 控制容器

容器建構變得方便後，使用者會產生大量容器，很快就需要一個群組管理的方法。Borg 提供 job 給一組相同的 tasks (task 作為容器的名稱)，一個 job 是一組向量集合 (compact vector) 可以指向一個或多個 tasks，將 task 從 0 開始遞增編號，這個做法很直接也很方便，但等稍後需要重啟容器時，Google 就後悔這個固定的設計，例如其中一個 task 死了需要重啟刀另外一台機器，原本的 task 向量的相同位置，現在需要做兩倍工作：找到新的副本，然後指向舊的副本以免需要除錯。當向量集合中的 task 離開後，這個向量上就有很多空洞，這讓 Borg 上層的管理系統分配，跨級群的 job 時變得很困難。這也造成 Borg 的 job 升級語法中出現許多危險且不可預期的交互 (當滾動升級時依照 index 順序重啟 task)，而應用仰賴 task index (例如應用使用 index 執行資料級的 sharding 或 paritioning)：如果應用使用 task index 來做 sharding，Borg 重啟時會移除鄰近的 tasks，導致資料不可用。Borg 也沒有好方法來增加來自應用的 metadata 到 task 上，例如角色 (e.g. 前端網頁)、或是滾動升級的狀態 (e.g. canary)，工程師只好將 metadata 編碼，壓在 jobs 的名稱上，再使用正規表達式 (regular expression) 解碼。

Kubernetes 直接使用 label 來辨識容器群，label 是鍵值資料對 (key-value pair)，包含可以辨識應用的資料，一個 Pod 可能有 role=frontend 與 state=production 表示 Pod 是屬於 production 環境的前端網頁。label 可以動態增加，並使用自動化工具更改，個團隊可以自行維護一組各自的 label。使用 label-selector 來取得一組物件 (e.g. stage==production && role==frontend)。各組物件可以重複，一個物件也可以屬於多個物件組，所以 label 也比靜態的物件清單更有彈性。由於物件組都是動態查詢時產生的，任何時候都可以增加新的物件組。label-selector 是 Kubernetes 的群組機制，並藉此分界管理維運，又可以同時處理多個實體。

雖然有些使用情形，事先明確知道一組內有哪些 task 很有用 (例如靜態腳色指派、工作 partitioning 或 sharding)，合理的 label 也能產生一樣的效果，只是應用 (或是其他外部管理系統) 就需要負責提供 labeling。label 與 label-selector 為雙邊提供最適的做法。

### 注意 Pod 的所有權

Borg 上 task 依賴 job，不會獨自存在，產生 job 時產生 tasks，這些 tasks 永遠連結特定的 job，刪除 job 同時刪除 tasks。這點很方便，但有一個缺陷，這個單一的群組機制，需要應對所有使用需求。例如 一個 job 需要儲存參數，提供給服務或是提供給應用，但不會一起提供，使用者就需要開發取代方案來協助處理 (e.g. DaemonSet 將 Pod 複製到所有節點上)

Kubernetes 中 Pod 的生命週期管理元件，例如 replication controller，使用 label selector 決定那些 Pod 要負責管理，所以會有一個以上的 controller 認為他們都對某個 Pod 有管轄權，這樣的衝突需要透過明確設定避免的。由於 label 的彈性也有許多優點，例如將 controller 與 Pod 解藕，表示再也不會有以往的孤兒 Pod (orphan) 或是認領的 Pod (adopt)。考慮附載均衡服務，透過 label selector 選擇流量的端點，如果一個 Pod 行為有異，這個 Pod 只要移除對應的 label，Kubernetes service load balancer 就可以避免流量，輕易的被隔離開來，但 Pod 本身還會存在，提供原地除錯。同時，管理 Pod 的 replication controller 會增加一個 Pod 來取代行為有異的 Pod。

### 不要暴露 raw state

Borg、Omega、Kubernetes 的關鍵不同點是 API 的架構設計。Borgmaster 是一個集中單一的 (monolithic) 元件，可見所有的 API 行為，包含級群管理邏輯，例如 job 與 task 的狀態機制，並且使用基於 Paxos 算法的分散式儲存庫。Omega 除了儲存庫以外，沒有集中式的元件，儲存庫只儲存被動的狀態資訊，提供樂觀的平行控制 (optimistic concurrenty control)：所有邏輯與語法都推送到儲存庫的客戶端，所以所有客戶端都可以讀取 Omega 的所有邏輯。實務中 Omega 的元件都使用相同的客戶端程式庫，負責打包/解包資料結構、資料重送、並確保語法的一致性。

Kubernetes 選擇中間，類似 Omega 元件化架構的架構，確保全域的常數、政策控管、資料轉型，來提供彈性與擴容性。Kubernetes 確保所有的儲存庫存取都透過 API server，API server 隱藏儲存庫的實作、負責物件的驗證、除錯、版本控制。如同 Omega，Kubernetes 提供多種不同的客戶端 (特別給是開源的環境)，但是集中化的 API server，仍能確保相同的語法、恆量、與政策控管。

# 其他困難的開放問題

多年的容器開發系統開發競豔，Google 仍然有一些問題還沒找到合適的答案，這裡分享一些問題，希望能帶來更多討論與解決方案。

### 設定 (configuration)

所有面對的問題中，與設定 (configuration) 有關的問題，產生最多的腦力激盪、文件、與許多程式碼。一組數值提供給應用，但不是直接寫死在程式碼中，我們可以就此寫一大篇些不完，但這邊先聚焦幾個重點。

第一，關於應用的設定，容器管理系統沒做，但已經有包羅萬象的實作，Borg 的歷史中包含：

- 範版 (boilerplate) 的精簡 (e.g. 針對不同工作負載，例如服務或是批次任務，提供預設的 task 重啟政策)
- 調整並驗證應用的參數與命令列標籤 (command-line flags)
- 實作 workaround 給還沒有的 API 抽象，例如 package 管理
- 應用的設定樣本程式庫
- 發布管理工具 (release management)
- 映象檔版本規格

為了與上述需求協作，設定管理系統最終產生一套針對特定領域 (domain-specific) 的設定語言，最終變成 Turing 語言，為了在設定資料中進行運算 (e.g. 透過服務的 sharding 數量，還決定調整機器的 memory)，這會造成一種難以理解的設定程式碼 (configuration is code) ，而這是應用工程師，透過消滅原始碼中寫死的參數，盡力避免的。這點並沒有降低維運的複雜性，新的語言只是將設定的運算，從應用的程式語言中，移到另外一個新的特定語言，而這個語言往往更缺乏開發工具、除錯工具、與測試框架。

Google 認為目前最有效的辦法，是接受一部分無法避免的程式設定，並且清楚的區分運算的程式與資料。呈現資料的語言應該簡單清楚，例如 JSON 或是 YAML，設定運算的邏輯則需要使用完整的程式語言，才有完整的語法、與好的工具。這點可見於 Angular 前端框架，劃分 markup 資料與 JavaScript 運算邏輯。

### 依賴管理 (dependency management)

建立服務往往意味著建立一套相關服務 (監控、CI/CD、等等)，如果一個應用依賴其他應用，是否容器管理系統也能自動提供依賴的服務呢？

讓事情更複雜，啟動依賴服務往往不只是啟動新的副本，例如服務啟動後還需要向使用者註冊 (例如 BigTable 服務)，然後傳送身分認證、權限認證、以及其他中介服務的計價資訊。沒有一個系統可以捕捉、管理、維護、或是暴露這樣的依賴系統資訊。所以開啟一個新服務時，用戶仍需要自己煩惱、部屬新服務仍然困難，而這往往進一步導致使用者沒有跟隨最佳實踐，進而降低服務的可靠性。

一個標準問題是，如果服務是手動提供的，跟上依賴服務更新會很困難。試圖自動化判斷 (e.g. 使用 tracing accesses) 失敗，因為無法取得判讀結果所需要的語法資訊。一個可能的解決方法，是要求應用列舉所有依賴的服務，並且透過架構控制，拒絕其他應用存取 (如同編譯時匯入的程式庫)。這樣可以讓容器管理系統提供自動化的環境設定、提供自動身分認證、並寫自動連接。

不幸的是，這樣描述、分析、使用依賴性的系統太過複雜，還沒被增加到主流的容器管理系統。我們希望有天 Kubernetes 能夠建立起類似的工具，單目前仍是一個尚未完成的挑戰。

# 結論

十年的經驗打掃容器管理系統，給了我們許多經驗，我們將其實作 Kubernetes 上，Kubernetes 的目的是透過容器，提升工程師的生產力，並減輕手動與自動管理系統的負擔，我們希望你也能加入拓展與探索的行列。
