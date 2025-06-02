---
title: "Workshop: RAG打造企業AI知識庫：把一甲子功力傳給新人"
summary: "學員將學會如何利用 RAG 技術，結合 OpenAI、LangChain、Qdrant 向量數據庫，構建企業內部文檔的智能知識庫，並能設計與實作一個基於自然語言處理（NLP）的查詢系統，來提升開發團隊的效率與知識管理能力。"
authors: []
tags: ["rag", "devops"]
categories: ["devops"]
date: '2025-06-01T00:45:00Z'
slides:
  # Choose a theme from https://github.com/hakimel/reveal.js#theming
  #theme: black
  theme: white
  # Choose a code highlighting style (if highlighting enabled in `params.toml`)
  #   Light style: github. Dark style: dracula (default).
  highlight_style: dracula
---

### RAG workshop 行前通知：基本需求

1. 當天帶自己的電腦，可以上網
  1. 選項1: 用電腦在 docker 運行開發環境
  1. 選項2: 用電腦遠端連線講師提供的 VM，在遠端VM 中運行 docker 開發環境
1. 會使用 docker
1. 會使用 python 與 jupyter notebook

---

##### 選項1: 使用自己的電腦

- 在 workshop 開始前，在自己的電腦上
   1. 安裝 [docker](https://docs.docker.com/get-started/get-docker/)
   1. git clone 教材
   1. 啟動 docker 開發環境，下載 docker images
   1. 安裝所需的 Python 套件
   1. 可以開啟瀏覽器，連線到 [Jupyter Notebook](http://localhost:8888)，token=workshop1234!

```bash
git clone https://github.com/chechiachang/rag-workshop.git

cd rag-workshop

docker compose up -d

docker exec -it notebook pip install pandas openai qdrant_client tqdm tenacity wget tenacity unstructured markdown ragas sacrebleu langchain_qdrant langchain-openai langchain_openai langchain_community tiktoken
```
---

##### 選項2: 使用遠端 VM

1. 有自己的電腦，當天有穩定的網路，可以連線到遠端 VM
1. 提前註冊 tunnel 工具（沒有業配）
1. [Ngrok](https://dashboard.ngrok.com/login) 登入 Login -> 左手邊 Identity & Access -> Authtokens -> Add Tunnel authtoken -> 記在安全的地方
1.  也可以使用 [Pinggy](https://pinggy.io/)，但免費有限時

---

### 建議

1. 優先使用個人電腦，免費 VM 名額會盡量提供，但依參與人數不保證現場有
1. 在家先試跑一遍，把 docker image 跟 pip 套件都下載好，現場要載很久
1. 在家試玩後記得關掉 ngrok，以免用完每月的免費額度
1. 如果事先看完內容覺得太簡單可以不用來，但歡迎會後找我聊天ＸＤ

---

### 投影片與教材與完整程式碼放在網站上

- [https://chechia.net](https://chechia.net)
- [https://chechia.net/zh-hant/slides/2025-06-05-devops-rag-internal-ai/](https://chechia.net/zh-hant/slides/2025-06-05-devops-rag-internal-ai/)
- [Github 投影片原始碼與講稿](https://github.com/chechiachang/chechiachang.github.io-src/blob/master/content/zh-hant/slides/2025-06-05-devops-rag-internal-ai/index.md)

---

### 以下是 RAG Workshop 當天內容

可以先看，也可以當天再看

---

### RAG Workshop 流程

1. **環境設定：確定參與者都有設定好開發環境**
1. 為什麼需要 RAG（Retrieval-Augmented Generation）
1. RAG: Embedding 與向量數據庫
1. RAG: Embedding Search
1. RAG: Evaluation
1. RAG 實際應用: 以 k8s official docs 為例

---

##### 選項1: 使用自己的電腦

1. 有在家先試跑一遍，應該可以在本地存取 Notebook [http://localhost:8888](http://localhost:8888)
1. 到 [workshop.chechia.net](https://workshop.chechia.net) 取得 OpenAI Key
1. 可以試著跑 notebook 2-5
1. 忘記怎麼啟動，可以回到投影片最開始

```
notebook token: workshop1234!
AZURE_OPENAI_API_KEY=""
AZURE_OPENAI_ENDPOINT=""
```

---

##### 選項2: 使用遠端 VM

1. 至[workshop.chechia.net](https://workshop.chechia.net) 領取一台 VM 並簽名
1. googel sheet 左邊 url，開啟 bastion 連線
1. Protocol: SSH，port 22，authentication type: password
1. 帳號密碼在 google sheet 上

---

![](azure-bastion.png)

---

##### 選項2: 使用 ngrok 連線到 jupyter notebook


1. 進入 VM 後，修改下面 ngrok authtoken。指令一行一行貼上（右鍵）到 bastion 中執行
1. 透過 https://4d11-52-230-24-207.ngrok-free.app/ 就可以使用 notebook (每個人不一樣)

```
cd rag-workshop
NGROK_AUTHTOKEN=<改成你的token>
sed -i "s/your-token/$NGROK_AUTHTOKEN/" docker-compose.yaml
docker compose up -d
docker logs ngrok

t=2025-06-02T06:17:41+0000 lvl=info msg="started tunnel" obj=tunnels name=command_line addr=http://notebook:8888 url=https://4d11-52-230-24-207.ngrok-free.app
```

---

### 以上是 Workshop 環境設定

1. 後面上課都透過這個網址操作
1. 還沒有看到 jupyter notebook 的人，請舉手

---

### RAG Workshop 流程

1. 環境設定：確定參與者都有設定好開發環境
1. **為什麼需要 RAG（Retrieval-Augmented Generation）**
1. RAG: Embedding 與向量數據庫
1. RAG: Embedding Search
1. RAG: Evaluation
1. RAG 實際應用: 以 k8s official docs 為例

---

### 什麼是 RAG

##### RAG（Retrieval-Augmented Generation，檢索增強生成）是一種結合檢索系統與生成式模型（如 GPT）的自然語言處理架構，在生成答案時引用外部知識，使模型回答更準確且具事實根據。

1. **Retrieval（檢索）：** 從一個外部知識庫（如文件、向量資料庫等）中找到與問題相關的資訊。通常會用語意向量（embeddings）做相似度搜尋。
2. **Generation（生成）：** 把檢索到的內容與使用者問題一起丟給 LLM（如 GPT、Claude 等）去生成答案。生成的內容會更具事實根據，並能引用具體資料。

---

### 為什麼會需要 RAG

- 資訊爆炸：企業內部文檔、知識庫、技術文件等資料量龐大，傳統搜尋方式無法有效檢索
- 選擇RAG（Retrieval-Augmented Generation）或傳統程式設計（Traditional Programming）
- 在特定任務的效能是否優於人類
- 不問「為什麼需要 RAG」，而是問「哪裡適合用 RAG，哪裡適合用傳統程式設計」。

{{% speaker_note %}}
{{% /speaker_note %}}

---

![](rag-vs-code.png)

{{% speaker_note %}}
適合用 RAG 的情境：客服問答、技術搜尋、知識型 Chatbot、內部知識導航、法規彙整、教學內容輔助。
適合用傳統程式的情境：金流控制、流程引擎、帳務系統、驗證邏輯、安全控制、任務排程。
{{% /speaker_note %}}

---

### 情境：新人工程師要如何到 k8s doc 查到想要的內容？

1. 有問題去 google / stack overflow
1. 需要搜尋引擎(k8s doc 有提供，但內部文件系統不一定有)
1. 需要關鍵字(新人怎麼知道要查 Dynamic Persistent Volume Resizing)
1. 協助理解（例如：舉例，旁徵博引，換句話說）
1. 跨語言門檻

{{% speaker_note %}}
k8s doc 有提供關鍵字搜尋，這個搜尋功能是怎麼做的？
Programmable Search Engine（PSE）https://developers.google.com/custom-search/docs/tutorial/introduction
Fulltext Search Engine 例如 elasticsearch 使用 Lucene
{{% /speaker_note %}}

---

![](search-in-k8s-official-doc.png)

{{% speaker_note %}}
{{% /speaker_note %}}

---

### 有了大語言模型（LLM）後，情境變成：

1. 去 google -> 先問 chatgpt，初步問答理解問題，找到關鍵字
1. 需要搜尋引擎 -> chatgpt 整合，直接上網搜尋
1. 需要關鍵字 -> chatgpt 會幫你找到關鍵字
1. 協助理解 -> chatgpt 很會舉例，旁徵博引，換句話說
1. 跨語言門檻 -> chatgpt 可以翻譯

{{% speaker_note %}}
chatgpt 會用通順的語言回答問題（優於平均工程師）
{{% /speaker_note %}}

---

- chatgpt 會用通順的語言，快速（數秒內）上網搜尋，回答問題
- 過程中不厭其煩地對答，旁徵博引，換句話說
- 回答的格式高度客製化

##### LLM 只差專業知識。沒有內容根據，LLM 容易產生幻覺

{{% speaker_note %}}
LLM 只差專業知識，沒有內容根據的話，容易產生幻覺。這時候就需要 RAG 技術來補強。
{{% /speaker_note %}}

---

### RAG Workshop 流程

1. 環境設定：確定參與者都有設定好開發環境
1. 為什麼需要 RAG（Retrieval-Augmented Generation）
   1. RAG 在「文件檢索與提示」上優於人類
   1. LLM 補強工程師的語言能力
1. **RAG: Embedding 與向量數據庫**
1. RAG: Embedding Search
1. RAG: Evaluation
1. RAG 實際應用: 以 k8s official docs 為例

---

### RAG Jupyter Notebook

1. Embedding with OpenAI.ipynb
2. Embedding Search with Qdrant and OpenAI.ipynb
3. RAG with OpenAI.ipynb
4. RAG DIY.ipynb
5. Evaluation.ipynb
6. k8s RAG QA.ipynb
