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

### RAG workshop 行前通知

###### 本次 workshop 以 hands-on 的方式進行，累積操作經驗為主，講解與說明為輔。觀念內容有準備教材，需要參與者自行閱讀

##### Workshop 基本需求

1. 有自己的電腦，可以上網
  1. 選項1: 使用自己的電腦，在 docker 啟動開發環境
  1. 選項2: 使用自己的電腦，遠端連線講師提供的 VM，在VM 中啟動 docker 開發環境
1. 會使用 docker
1. 會使用 python 與 jupyter notebook

---

##### 選項1: 使用自己的電腦

- 在 workshop 開始前，在自己的電腦上
   1. 安裝 [docker](https://docs.docker.com/get-started/get-docker/)
   1. git clone 教材
   1. 啟動 docker 開發環境，下載 docker images
   1. 安裝所需的 Python 套件
   1. 可以開啟瀏覽器，連線到 [Jupyter Notebook](http://localhost:8888)

```bash
git clone https://github.com/chechiachang/rag-workshop.git

cd rag-workshop

docker compose up -d

docker exec -it notebook pip install pandas openai qdrant_client tqdm tenacity wget tenacity unstructured markdown ragas sacrebleu langchain_qdrant langchain-openai langchain_openai langchain_community tiktoken
```
---

### 選項2: 使用遠端 VM

- 建議使用個人電腦，免費 VM 名額現場有限
  1. 需要有自己的電腦，有穩定的網路，可以連線到遠端 VM
  1. 需要註冊 tunnel 工具（沒有業配）[Ngrok](https://dashboard.ngrok.com/login)
  1.  登入 Login -> 左手邊 Identity & Access -> Authtokens -> Add Tunnel authtoken -> 記在安全的地方
  1. 也可以使用 [Pinggy](https://pinggy.io/)，但免費有限時

---

### 投影片與教材會放在網站上

[https://chechia.net](https://chechia.net)

---

### RAG Workshop

##### 本次 workshop 以 hands-on 的方式進行，累積操作經驗為主，講解與說明為輔。觀念內容有準備教材，需要參與者自行閱讀

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

### 下課前如何保存自己的進度

[github](https://github.com/) repository 開一個新的 repository，然後上傳

1. 移除 notebook 內所有 OpenAI API key
1. ssh 進去 vm

```
cd rag-workshop

git remote add new <your-repo-url>

git add .

git commit -m "save my progress"

git push new main
```
