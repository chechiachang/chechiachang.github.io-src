---
name: chechia-content
description: "Ingest and generate content for this Hugo repo using content/posts, content/slides, and wiki. Use for slide/post authoring, wiki recompilation, and append-only ingest logging."
---

# Chechia Content Skill

Use this skill to maintain and generate content for this repository.

## When To Use

- Append ingest history to `wiki/log.md`.
- Generate or update posts in `content/posts/<date>-<slug>/index.md`.
- Generate or update slides in `content/slides/<date>-<slug>/_index.md`.
- Ingest updates from `content/*` into `wiki/*`.
- Rebuild navigation in `wiki/index.md`.

## What To Load

- `AGENTS.md`
- Relevant source files under `content/posts/*` and `content/slides/*`
- `skills/presentation.md`
- `wiki/index.md`
- `wiki/log.md`
- `wiki/purpose-plan.md`

## Operating Rules

- Keep outputs short, actionable, and minimal.
- Never rewrite old log lines in `wiki/log.md`; append only.
- Preserve old wiki knowledge unless newer source clearly supersedes it.
- Treat `content/*` as source of truth and immutable during ingest.
- Use `./tmp` for temporary files.

## Operating Contract

### Scope And Source

- Do not edit raw source files during ingest.
- For ingest, read from `content/*` and write to `wiki/*` only.
- Prefer incremental updates over full rewrites.

### Language And Style

- Keep technical terms in English when standard (`RAG`, `MCP`, `evaluation`, `runbook`).
- Keep wording concise, direct, and practical.
- Match user language; default to Traditional Chinese when ambiguous.

### Tone Persistence

- Keep the same practical, spoken tone from start to end; avoid switching to abstract analyst prose mid-response.
- Use short, direct lines and problem-first framing, consistent with existing decks.

#### Short Sentence Rhythm

- 今天只講一件事
- 我們先定義這次要解的問題
- 這個問題的解法是 Spec-driven development
- 這裡先用一句話總結重點
- 所以會發生這些問題
- 不管怎樣先 Live demo
- 可以先看，也可以當天再看
- K8s 升級有問題，不是有問題
- 太晚發現才是問題
- 有很多問題也很正常，產生疑問也是工作坊的目的
- LLM 很會補 pattern
- 但不會讀你的腦
- Prompt 是聊天
- Spec 是工程
- system behavior 不可預測
- 這是今天的大綱
- 我們會先說明如何進行 workshop
- 接著進入 etcd 基礎操作 Quiz
- 最後會說明 etcd 基礎操作答案
- 這個段落會說明 etcd Clusters 與 Raft 共識算法
- 這個段落會說明 K8s 的 etcd backup 與 restore
- 這個段落會說明 etcd Clusters 如何 add member
- 加分題是自己動手做 CA 與 TLS certs
- 加分題為自己加分: 增加 apiserver

#### The Simplification Instinct

- 換句話說，因為有 USB 存在，各家硬體廠商才會覺得只要做一套 USB 接口，所有人都可以用，所以才會有 USB 支援很多功能的感覺
- Node 升級簡單來說是建新拆舊
- 我們今天要做的是成本優化，白話的說是降低 cpu / memory 的設定配額，但是我們不能降低到影響服務品質
- MCP 不是提供 tool，而是提供一個統一的標準，讓 LLM 可以使用這些 tool 產生的結果，格式是統一的
- 我們看得到 system，但無法控制 system
- 適合用 RAG 的情境：客服問答、技術搜尋、知識型 Chatbot、內部知識導航
- 適合用傳統程式的情境：金流控制、流程引擎、帳務系統、安全控制
- Retrieval（檢索）： 從一個外部知識庫（如文件、向量資料庫等）中找到與問題相關的資訊。通常會用語意向量（embeddings）做相似度搜尋
- Generation（生成）： 把檢索到的內容與使用者問題一起丟給 LLM（如 GPT、Claude 等）去生成答案。生成的內容會更具事實根據，並能引用具體資料
- LLM（大型語言模型）本身並不具備事實知識，而是依賴訓練時的語料與提示輸入來生成回答。當缺乏明確上下文或內容根據時，LLM 容易出現幻覺現象，也就是生成看似合理但實際不正確的資訊。專業領域問題若未提供準確資料支撐，也容易導致錯誤回答
- LLM 會根據使用者的問題調整回答方式，例如互動問答、舉例說明與換句話說
- 這樣可以減少 LLM 的幻覺（hallucination），並提高回答的準確性
- 增加可觀測性，每個回答都可以追溯到具體的上下文文件
- Observability（例如 Langfuse）可以提供：
- 發生了什麼？
- 我應不應該改？
- 這個改動是不是變好？
- etcd 是一個分散式的 key-value 資料庫
- Kubernetes 的資料都存放在 etcd 中
- 使用公有雲服務時，etcd 通常是被管理起來的
- 使用自建的 Kubernetes 時，etcd 通常需要自行安裝與維運
- kubectl 是 Kubernetes 的 CLI 工具，可以透過 kubectl 存取 k8s control plane
- k8s 官方文件中，從維運 k8s 角度，講述如何維運 etcd
- k8s 運行時，會將資料存放在 etcd 中
- 預設 etcdctl 會連線到 --endpoints=[127.0.0.1:2379]
- 使用 --endpoints 指定要連線到的 etcd
- 使用 export ETCDCTL_ENDPOINTS 指定要連線到的 etcd
- member 是 etcd cluster 中的一個節點
- leader 是 etcd cluster 中的一個 member
- Proposal (ex. update key/value) requires a majority quorum (n/2 +1)

#### Genuine Reactions

- 我們不是懶，而是現在要解答許多基本問題，LLM 回答得比人好
- 所以在座的各位要被取代了嗎？
- 喜歡這種內容歡迎來找我聊天！
- 事先看完內容覺得太簡單可以不用來，但歡迎會後找我聊天ＸＤ
- 想當個 sre，或是想當個會 MCP 的 sre 嗎？這邊都可以實現
- 沒使用過的人不是這個 session 的目標聽眾，可以 QR code 拍下來去聽別場。例如對面同題材的session
- 這些人可以出去吃零食，今天講的內容你們都會了，我沒什麼東西可以跟你們分享
- 有問題問過 AI 後再來問我
- 開場先 Demo 一波！
- 沒時間的話可以待會來找我聊天
- 由衷地感謝為 workshop 提供協助的夥伴!
- Demo 我在本地隨手跑一下測試
- 進度落後不太會影響後續操作，不必擔心
- 參與者可以跟台上的進度，也可以超前進度向後操作
- 這是一場手把手入門 Etcd 與 Kubernetes 的 workshop
- 加分題卡住乃兵家常事，大俠請重新來過即可
- 本次 workshop 以 hands-on 的方式進行，累積操作經驗為主，講解與說明為輔
- 觀念內容有準備教材，需要參與者自行閱讀
- 講師會免費提供 Azure VM 供同學遠端操作使用

#### The Deadpan Absurd

- 不是考試，隨意發揮，重點在促進大家思考
- 問題不是 vault 在 VM 上安全，還是在 k8s 上安全
- 微服務不是問題，微服務底下的 k8s object 才是問題
- 現在應該沒有人會因為要去使用 redis 或是 mysql，自己跑去寫 k8s object 了吧
- code 能跑
- looks right, but does not quite work
- LLM judge 是 heuristic，不是 truth
- 結論：judge 是 heuristic，不是 truth
- Observability 不是 Decision System
- 不是 logging tool
- 卡住可以嘗試連按 esc 鍵，然後輸入 :q! + enter 強制離開 vim
- 4 nodes vs 2 nodes 的風險一樣，都是 -1 node 後，就無法達成共識
- 如果 4 nodes 中，新+1 node 有問題，會導致 2 nodes 永遠無法達成 majority 3，此時預設也無法 add member
- 此時需要透過 restore snapshot，--force-new-cluster 等方式，強制建立新的 cluster
- 這是一個極度簡化的 k8s control plane
- 沒有 kubelet 與 node
- 正式環境不會長這樣

#### Lecture Structure: The Roadmap-First Pattern

- 我們今天要聊什麼
- 這是我們今天的大綱
- 10min - 為什麼需要 RAG（Retrieval-Augmented Generation）
- 如何開始/如何進步
- 如何開始？
- 如何改進？
- 這裡先說明這次的目標
- 這裡先說明 hands-on 的流程安排
- 這裡先定義問題陳述
- 確認大家都有操作環境
- docker 啟動 etcd
- 透過 etcdctl 存取 etcd
- docker 啟動 etcd cluster
- docker 啟動 k8s control plane
- 透過 kubectl 存取 k8s control plane
- 維運 k8s 所需的 etcd operation
- 這個段落會說明如何準備啟動多台 etcd
- 這個段落會說明如何啟動多台 etcd
- 這個段落會說明如何搭建 K8s Control Plane
- 這個段落會說明如何操作 etcd Clusters 的 member
- 這個段落會說明 etcd Clusters 如何 remove member

#### Core Pedagogical Moves

- 你可以帶走的重點
- Retrieval（檢索）： 從一個外部知識庫（如文件、向量資料庫等）中找到與問題相關的資訊。通常會用文字嵌入向量（embeddings）做相似度搜尋
- 情境：新人工程師要如何到 k8s doc 查到想要的內容？
- 情境：Senior 工程師要如何分享知識？
- 有問題去 google / stack overflow
- 那不常見/複雜的問題呢？
- 100 行程式碼就可以接上 3 個資料源
- 為什麼需要 RAG
- 這裡提供一個簡單的 RAG 範例
- 根據以下資料回答問題：
- 問題：COVID 的全名是什麼？
- 我知道 RAG 是什麼了，但為何要打造內部知識庫？
- 入門的的問題與重複的問題，不需要人類回答
- RAG Agent + Slack Bot 整合就可以完成第一個迭代版本
- 一行一行執行底下指令，來啟動一台 etcd
- 透過以下 command 重啟 etcd
- 重啟 etcd 後，是否還能讀取到 foo 的值？為什麼？
- 本 workshop 的 docker-compose.yml 中，etcd 的資料是存放在本地的 etcd0 資料夾中，因此重啟後，資料不會遺失
- 請找到 raft term 與 raft index
- 寫入資料，觀察 raft index 的變化
- 讀取資料，raft index 會有什麼變化嗎?
- 透過 move-leader 指令，可以交接 leader
- 觀察 raft index 的變化
- 請用50個字，描述你目前覺得 etcd 是什麼？
- 找到那個 node 是 leader 了嗎？每個人的結果可能不一樣
- raft term 與 raft index 有什麼變化嗎?
- 被移掉的是 etcd-1 還是 etcd-2 還是 etcd-3?
- 透過 etcdctl 存取 workshop namespace 的資料
- etcdctl 確定 leader 與 raft index
- 向 leader node 發送 snapshot request
- 停止 k8s control plane (apiserver)

### Evidence And Safety

- Base summaries on repository content, not assumptions.
- If source is missing, stop and report the exact missing path.
- Use safe, non-destructive actions only.

## Ingest Workflow

1. Read `wiki/purpose-plan.md`.
2. Compare `content/slides/*/_index.md` with `wiki/slides/*.md`.
3. Compile missing/stale slide wiki notes.
4. Rebuild `wiki/index.md` topic navigation.
5. Append one chronological line to `wiki/log.md`.

## Output Workflow

1. Keep post/slide slug aligned: `<date>-<slug>`.
2. Posts stay concise and agenda-oriented.
3. Slides hold full technical narrative and workshop flow.
4. Ensure post includes slide link: `https://chechia.net/slides/<date>-<slug>/`.
5. Keep metadata coherent across post and slide (title/date/tags).
