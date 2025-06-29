---
title: "Workshop: DevOpsDay 2025: RAG打造企業AI知識庫：把一甲子功力傳給新人"
date: '2025-06-05T12:45:00Z'
# weight: 1
# aliases: ["/test"]
tags: ["openai", "generative", "ai", "kubernetes", "devops"]
categories: ["generative", "ai"]
description: 學員將學會如何利用 RAG 技術，結合 OpenAI、LangChain、Qdrant 向量數據庫，構建企業內部文檔的智能知識庫，並能設計與實作一個基於自然語言處理（NLP）的查詢系統，來提升開發團隊的效率與知識管理能力。
#canonicalURL: "https://canonical.url/to/page"

showToc: true
TocOpen: false
#UseHugoToc: true

draft: false

hidemeta: false
comments: true
disableHLJS: false

hideSummary: false
ShowReadingTime: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
ShowWordCount: true
ShowRssButtonInSectionTermList: true

searchHidden: false
disableShare: false

#cover:
#    image: "" # image path/url
#    alt: "" # alt text
#    caption: "" # display caption under cover
#    relative: false # when using page bundles set this to true
#    hidden: false # only hide on current single page
---

### 📅 活動時間: 2025-06-05T12:45:00Z
### 🔗 [活動連結](https://devopsdays.tw/2025/workshop-page/3788)
### 📘 聯繫我 [Facebook](https://www.facebook.com/engineer.from.scratch)
### 📑 [投影片](../../slides/2025-06-05-devops-rag-internal-ai)

---

## RAG workshop 行前通知

本次 workshop 以 hands-on 的方式進行，累積操作經驗為主，講解與說明為輔。觀念內容有準備教材，需要參與者自行閱讀。講師會免費提供

1. Azure OpenAI models API key (gpt-4.1, gpt-4.1-mini, text-embedding-3, text-embedding-ada-002...)
1. Azure VM 供同學遠端操作使用

# --> [投影片與教材](../../slides/2025-06-05-devops-rag-internal-ai/) <--

---

### Workshop 基本需求

1. 有自己的電腦，可以上網
  1. 選項1: 使用自己的電腦，在 docker 啟動開發環境
  1. 選項2: 使用自己的電腦，遠端連線講師提供的 VM，在VM 中啟動 docker 開發環境
1. 會使用 docker
1. 會使用 python 與 jupyter notebook
1. 會使用 chatgpt.com 協助除錯

---

### 選項1: 使用自己的電腦

在 workshop 開始前，在自己的電腦上

1. 安裝 docker
1. git clone github repository
1. 啟動 docker 開發環境，下載 docker images
1. 開啟瀏覽器，連線到 Jupyter Notebook，token `workshop1234!`
1. 在 Jupyter Notebook 中，安裝所需的 Python 套件

```bash
git clone https://github.com/chechiachang/rag-workshop.git

cd rag-workshop

docker compose up -d

docker exec -it notebook pip install pandas openai qdrant_client tqdm tenacity wget tenacity unstructured markdown ragas sacrebleu langchain_qdrant langchain-openai langchain_openai langchain_community tiktoken
```

---

### 選項2: 使用遠端 VM

1. 建議使用個人電腦，畢竟免費 VM 名額現場有限
1. 需要有自己的電腦，有穩定的網路，可以連線到遠端 VM
1. 需要註冊 tunnel 工具（沒有業配）[ngrok](https://dashboard.ngrok.com/login)
  1.  登入 Login -> 左手邊 Identity & Access -> Authtokens -> Add Tunnel authtoken -> 記在安全的地方
  1. 也可以使用 [pinggy](https://pinggy.io/)，但免費有限時

---

### 投影片與教材會放在網站上

[https://chechia.net/zh-hant/slides/2025-06-05-devops-rag-internal-ai/](https://chechia.net/zh-hant/slides/2025-06-05-devops-rag-internal-ai/)

如何存取 VM 也會放在敨影片裡

---
RAG workshop 行前通知完，大家當天現場見
---

## Info

開發團隊需要將經驗與知識，透過文件化的方式保存下來，以便未來查詢與學習。然而，企業內部文件往往分散於 Confluence、Google Drive、Notion 等平台，傳統關鍵字搜尋難以快速獲取準確資訊，導致溝通成本高、開發流程受阻。又或是，當開發團隊需要查詢特定知識時，往往需要透過 Slack、Email 等方式詢問同事，這樣的溝通成本不僅浪費時間，也容易造成資訊不對稱。

學員將學會如何利用 RAG 技術，結合 OpenAI、LangChain、Qdrant 向量數據庫，構建企業內部文檔的智能知識庫，並能設計與實作一個基於自然語言處理（NLP）的查詢系統，來提升開發團隊的效率與知識管理能力。

- 什麼是 RAG？
  - 介紹 RAG（Retrieval-Augmented Generation）技術如何結合檢索與生成提升問答準確性。
  - 為什麼企業需要智能知識庫？
  - RAG 的應用場景：知識庫建立、開發支援、技術決策等。
- Python 與 OpenAI：
  - 使用 OpenAI API 架構與語言模型，快速構建生成模型
- LangChain：介紹 LangChain 框架如何簡化 RAG 實現
- 如何利用 LangChain 整合多種數據源與生成模型
- Qdrant 向量數據庫：
  - 向量數據庫的概念與作用
  - 如何利用 Qdrant 儲存與檢索內部文檔的嵌入向量
- 構建 RAG 系統：實作步驟與演示
  - 數據預處理與文檔轉換
  - 將處理後的文本轉換為向量表示（embedding）
  - 利用 Qdrant 向量數據庫儲存這些嵌入並執行檢索
- 使用 LangChain 結合 OpenAI 模型與 Qdrant，製作自動化問答系統

# Target group

本次工作坊會提供參與者一個簡單的環境，讓參與者可以透過遠端操作來實作基本 RAG AI Agent。參與者必備個人筆電，透過 SSH 操控遠端機器。

必備知識：Linux 操作基本知識，Docker 操作基本知識，會使用 SSH 連線 / Bash / docker。

工作坊結束後，學員將能夠：
- 理解並實作 RAG 技術，將內部文檔轉化為智能知識庫
- 使用 Python、LangChain 和 OpenAI 構建基於檢索的問答系統
- 利用 Qdrant 向量數據庫進行高效檢索，提升開發流程中的知識管理效率。
- 這樣的工作坊結構能夠平衡理論與實踐，並為學員提供實際動手操作的機會。

## Author

Che-Chia Chang 是一名專注於後端開發、開發維運、容器化應用及 Kubernetes 開發與管理的技術專家，同時也是 Microsoft 最有價值專業人士（MVP）。

活躍於台灣技術社群，經常在 CNTUG、DevOps Taipei、GDG Taipei、Golang Taipei Meetup 等社群分享 DevOps、SRE、Kubernetes 及雲端運算相關技術。致力於推動開發與維運的最佳實踐，並熱衷於研究與應用最新的雲端與 AI 技術。

個人部落格：https://chechia.net

Che-Chia Chang is a technology expert specializing in backend development, DevOps, site reliability engineering (SRE), containerized applications, and Kubernetes development and management. He is also recognized as a Microsoft Most Valuable Professional (MVP).

Actively engaged in the Taiwanese tech community, he frequently shares insights on DevOps, SRE, Kubernetes, and cloud computing at CNTUG, DevOps Taipei, GDG Taipei, and Golang Taipei Meetup. Passionate about promoting best practices in development and operations, he continuously explores and applies the latest advancements in cloud and AI technologies.

https://chechia.net
