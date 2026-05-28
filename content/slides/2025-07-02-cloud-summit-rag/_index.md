---
title: "Cloud Summit 2025: 用 RAG 打造企業可對話 AI 知識庫《有問題問過 AI 後再來問我》"
description: 透過 RAG（檢索增強生成）技術，將企業內部文件轉為智能知識庫，提升資訊檢索與決策效率。本演講將探討 RAG 應用、技術架構與落地實踐，幫助開發團隊與企業更高效利用內部知識。企業內部文件往往分散於 Confluence、Google Drive、Notion 等平台，傳統關鍵字搜尋難以快速獲取準確資訊，導致溝通成本高、開發流程受阻。本演講將介紹如何運用 RAG（Retrieval-Augmented Generation）技術，結合 OpenAI 及向量數據庫，將企業內部文檔轉為智能知識庫。我們將探討文件解析、嵌入索引、AI 問答系統的技術架構與實作，幫助開發團隊構建高效 AI 助手，節省溝通成本，加速開發流程，提升決策與問題解決能力
tags: ["rag", "devops"]
categories: ["devops"]
date: '2025-06-25T00:45:00Z'
outputs: ["Reveal"]
reveal_hugo:
  custom_theme: "reveal-hugo/themes/robot-lung.css"
  margin: 0.2
  highlight_theme: "color-brewer"
  transition: "slide"
  transition_speed: "fast"
  templates:
    hotpink:
      class: "hotpink"
      background: "#FF4081"
---

#### Cloud Summit 2025
## 用 RAG 打造可對話 AI 知識庫
##### 《有問題問過 AI 後再來問我》
##### ~ Che Chia Chang @ [chechia.net](https://chechia.net) ~

---

{{% section %}}

{{< slide content="slides.about-me" >}}
🔽

---

### [DevOpsDay 2025: RAG Workshop](../../slides/2025-06-05-devops-rag-internal-ai)

---

![](images/2025-devopsday-rag-workshop.jpg)

{{% /section %}}

---

### 大綱

1. 什麼是 RAG
1. 為什麼需要 RAG
1. 為何需要內部知識庫
1. RAG Agent 的優勢
1. RAG Agent 的應用場景
1. 如何開始/如何進步
1. QA

---

{{% section %}}

### 什麼是 RAG

- RAG（Retrieval-Augmented Generation 檢索增強生成）
- 結合檢索系統與生成式模型（如 GPT）的自然語言處理架構
- 在生成答案時引用外部知識，增加上下文內容，提供給 LLM（大型語言模型）
- 使模型回答更準確且具事實根據

🔽

---

### 什麼是 RAG

1. **Retrieval（檢索）：** 從一個外部知識庫（如文件、向量資料庫等）中找到與問題相關的資訊。通常會用文字嵌入向量（embeddings）做相似度搜尋。
2. **Generation（生成）：** 把檢索到的內容與使用者問題一起丟給 LLM（如 GPT、Claude 等）去生成答案。生成的內容會更具事實根據，並能引用具體資料。

---

![](mermaid/generative-ai.svg)

{{% note %}}
{{< mermaid >}}
graph LR
    subgraph "Generative AI"
        direction LR
        A1(("Query"))
        B1("LLM
        (gpt-4.2)")
        C1("文字接龍產生回答 Response")
        A1 --User Input--> B1
        B1 --Chat Completion--> C1
    end
{{< /mermaid >}}
{{% /note %}}

---

![](mermaid/rag-embedding.svg)

{{% note %}}
{{< mermaid >}}
graph LR
    subgraph "RAG"
        direction LR
        A2(("Query"))
        B2("LLM
        (gpt-4.2)")
        C2("Response")
        D2("Vector DB")
        A2 --User Input--> B2
        A2 --Embedding Search--> D2
        D2 --Context--> B2
        B2 --Chat Completion--> C2
    end
    subgraph "Embedding"
        direction LR
        A3(("Document"))
        B3("Embedding Model")
        C3("Embedding Vector")
        D3("Vector DB")
        A3 ----> B3
        B3 --Embedding--> C3
        A3 --Store--> D3
        C3 --Store--> D3
    end
{{< /mermaid >}}
{{% /note %}}

---

### 為什麼使用 RAG？

- 希望 LLM 根據知識庫產生回答
- 而不是只根據 Model 訓練資料，進行生成式回答。
- 這樣做可以達到以下目的：
  - ✅ 減少模型幻覺（hallucination）
  - ✅ 為使用者提供即時且相關的資訊
  - ✅ 利用你自己的內容與知識庫

---

##### LLM 不具備專業知識。缺乏內容根據時，容易產生幻覺(hallucination)

![](images/llm-hallucination.png)

{{% note %}}
LLM（大型語言模型）本身並不具備事實知識，而是依賴訓練時的語料與提示輸入來生成回答。當缺乏明確上下文或內容根據時，LLM 容易出現「幻覺」現象，即生成看似合理但實際不正確的資訊。專業領域問題若未提供準確資料支撐，也容易導致錯誤回答。
{{% /note %}}

---

![](images/k8s-hallucination.jpg)

{{% /section %}}

---

{{% section %}}

### 簡單的RAG範例

[https://github.com/chechiachang/rag-workshop/blob/main/notebook/3_RAG_with_OpenAI.ipynb](https://github.com/chechiachang/rag-workshop/blob/main/notebook/3_RAG_with_OpenAI.ipynb)

```
┌──────────────┐       ┌─────────────────────┐
│ User Input   │       │ Embedding Model     │
│ (e.g., Query)├──────▶│ (OpenAI Embeddings) │
└──────────────┘       └────────────┬────────┘
                                    │
                                    ▼
                            ┌───────────────┐
                            │ Vector Query  │
                            │ to Qdrant DB  │
                            └──────┬────────┘
                                   ▼
                        ┌────────────────────┐
                        │ Retrieved Contexts │
                        └────────┬───────────┘
                                 ▼
                   ┌────────────────────────────┐
                   │ Prompt Construction Module │
                   │ (Query + Top-K Contexts)   │
                   └────────┬───────────────────┘
                            ▼
                    ┌────────────────────┐
                    │ OpenAI Chat Model  │
                    │ (GPT-4.1 / GPT-4)  │
                    └────────┬───────────┘
                             ▼
                    ┌────────────────────┐
                    │ Final Answer       │
                    └────────────────────┘
```
🔽

---

```python
import qdrant_client

# 使用 Qdrant 作為向量數據庫
client = qdrant_client.QdrantClient(
    host="localhost",
    prefer_grpc=True,
)

'''
query_docs 函數用於查詢相關文檔
查詢指定的 collection_name
使用指定的模型model進行嵌入查詢
返回最相關的文檔
'''
def query_docs(query, collection_name="covid-qa-3-large", model="text-embedding-3-large" , top_k=5):

    '''
    query_embeddings 函數用於獲取查詢的語意嵌入向量
    換句話說，把查詢的問題轉換為向量表示
    example: "What is COVID-19?" -> [0.1, 0.2, 0.3, ...] 一個固定長度的向量
    '''
    query_embeddings = get_embedding(query, model)

    '''
    使用 Qdrant 客戶端 query_points 函數查詢相關文檔
    返回指定 collection_name 中與 query_embeddings 最相似的前 top_k 個點
    '''
    results = client.query_points(
        cㄨollection_name=collection_name, // 查詢的 collection 名稱
        query=query_embeddings, // 輸入查詢的語意嵌入向量
        limit=5, // 返回前 5 個最相關的點
        with_payload=True,
        using="title" // 使用指定的索引字段進行查詢
    )

    # 提取查詢結果中的 payload（即答案）
    payloads = [point.payload["answer"] for point in results.points]
    return payloads

'''
使用 OpenAI 的 GPT 模型生成回答
docs 是從向量數據庫中查詢到的相關文檔
將 context 與原始問題組合成 prompt 將 query + context 組合起來，如：

根據以下資料回答問題：
===
[段落1]
[段落2]
===
問題：COVID 的全名是什麼？
'''
def generate_answer(query, docs, model="gpt-4o-mini"):
    context = "\n\n".join(docs)
    prompt = f"""根據以下內容回答問題：
    1. 請用繁體中文回答
    2. 依照內容產生回答
    3. 附上內容原文作為依據，原文保留內容的原始語言
    4. 如果內容不包含就回答我不知道
    
    內容：
    {context}
    
    問題：
    {query}
    """

    res = openai_client.chat.completions.create(
        model=model, # 使用指定的 OpenAI 模型
        messages=[
            {"role": "system", "content": "你是一個 helpful AI 助理"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return res.choices[0].message.content.strip()

# 使用範例
query = "COVID 的全名是什麼"

# 根據 query 查詢相關文檔 docs
docs = query_docs(
    query=query,
    collection_name="covid-qa-3-large",
    model="text-embedding-3-large")

# 將查詢結果 docs 與 query 一起生成回答
answer = generate_answer(
    query=query, 
    docs=docs, 
    model="gpt-4o-mini")

print("\n🧠 回答：")
print(answer)

🧠 回答：
COVID 的全名是「Coronavirus Disease 2019」，簡稱 COVID-19。

依據原文：
"WHO announced “COVID-19” as the name of this new disease on 11 February 2020, following guidelines previously developed with the World Organisation for Animal Health (OIE) and the Food and Agriculture Organization of the United Nations (FAO)."
```

---

#### 可以增強 gpt-4o 的冷笑話知識

![](images/rag-cold-joke.jpg)

---

#### 或是把 K8s 官方文件全部塞進 vector DB

[https://github.com/chechiachang/rag-workshop/blob/main/notebook/6_k8s_RAG_QA.ipynb](https://github.com/chechiachang/rag-workshop/blob/main/notebook/6_k8s_RAG_QA.ipynb)

- 透過 prompt 嚴格限制 LLM 根據上下文提供的文件回答，而不要依賴 LLM 的訓練資料
- LLM 只提供語言邏輯
- 這樣可以減少 LLM 的幻覺（hallucination），並提高回答的準確性
- 增加可觀測性，每個回答都可以追溯到具體的上下文文件

{{% /section %}}

---

{{% section %}}

##### 我知道 RAG 是什麼了，但為何要打造內部知識庫？
🔽

---

##### 我知道 RAG 是什麼了，但為何要打造內部知識庫？

- 企業內部文件往往分散於 Slack、Confluence、Google Drive、Notion 等平台
- 傳統關鍵字搜尋難以快速獲取準確資訊
- 特定職位的工程師會變成回答問題的「門神」
- 相同的問題被問了無數次
- 新人需要花費大量時間去搜尋、理解與學習
- 導致溝通成本高、開發流程受阻

需要一個統一的知識庫，能夠快速檢索、理解並回答問題

---

##### 使用 RAG Agent 增強內部知識傳遞

- 入門的的問題與重複的問題，不需要人類回答
- LLM 的語言修飾能力優於平均工程師（表達的更通順）
- LLM 可以根據使用者的問題，提供多元的回答方式（舉例說明，換句話說）
- **Agent** 結合 [function tools](https://openai.github.io/openai-agents-python/tools/) / mcp server 可以整合更多資料來源
- RAG Agent 24/7 可用不需休息，也不會失去耐心

---

##### RAG Agent 的優勢

- 入門的的問題與重複的問題 ---> 基礎問題的正確率高
- LLM 的語言修飾能力優於平均人類 ---> 表達的更通順
- LLM 根據使用者的問題調整回答方式 ---> 互動問答，舉例說明，換句話說
- RAG Agent 不需休息，不會失去耐心 ---> 比我本人還高可用
- 自動化 ---> 結合監測系統，主動推送需要的訊息
- 標準化回答

---

##### RAG Agent + MCP Server

![](mermaid/mcp-server.svg)

{{% note %}}
{{< mermaid >}}
graph LR
    subgraph " "
        direction LR
        A1("RAG Agent / MCP Client")
        B1("Confluence MCP Server")
        B2("Confluence")
        C1("Github MCP Server")
        C2("Github")
        D1("Slack MCP Server")
        D2("Slack Bot")
        E1("MySQL MCP Server")
        E2("MySQL")
        F1("工程師")
        A1 --> B1
        B1 --> B2
        A1 --> C1
        C1 --> C2
        A1 --> D1
        D1 --> D2
        A1 --> E1
        E1 --> E2
        D2 <--問答--> F1
    end
{{< /mermaid >}}
{{% /note %}}

透過 [MCP Protocol](https://modelcontextprotocol.io/introduction#general-architecture)，可以將不同的資料來源（如 Confluence、Github、Slack 等）整合到 RAG Agent 中。這樣，RAG Agent 可以在不同的上下文中提供一致的回答。不需要寫額外的程式碼，或只需要 LLM generate 一些簡單的程式碼。

---

##### RAG 自動化: 新人 onboarding

![](mermaid/rag-agent-onboarding.svg)

{{% note %}}
{{< mermaid >}}
graph LR
    subgraph " "
        direction LR
        A1("Onboarding Tasks")
        B1("RAG Agent")
        C1("架構設計文件/SOP/Runbook")
        D1("階段性測驗")
        F1("庶務/交接")
        E1("新人工程師")
        A1 --> B1
        C1 --> B1
        D1 --> B1
        F1 --> B1
        B1 --互動式 Onboarding--> E1
        E1 --提出問題--> B1
    end
{{< /mermaid >}}
{{% /note %}}

傳統的 onboarding 過程往往依賴資深工程師手動指導和文檔查閱，效率低下。透過 RAG Agent，可以提供互動式的 onboarding 體驗，並且可以不斷溫習和更新知識。

---

##### RAG 自動化: 第一時間Alert處理

![](mermaid/rag-agent-alert.svg)

{{% note %}}
{{< mermaid >}}
graph LR
    subgraph " "
        direction LR
        A1(("Alert/Metrics"))
        B1("內部文件 RAG")
        C1("內部Runbook")
        D1("架構設計文件")
        E1("Slack")
        F1("Alert/文件/處理步驟
        交給on-duty工程師")
        A1 --> B1
        B1 --> C1
        B1 --> D1
        A1 --> E1
        C1 --> E1
        D1 --> E1
        E1 --> F1
    end
{{< /mermaid >}}
{{% /note %}}

工程師處理 alert 時，通常需要查閱內部文件、Runbook 或架構設計文件。這些文件往往分散在不同的系統中，導致查找過程耗時。

---

> AI Copilot 不應該像圖書館守門員等人來借書，
> 而應該像導航系統，在你開車時主動告訴你：前方有彎道。

{{% note %}}
基本上我們期待的解決方案是這樣
{{% /note %}}

---

##### 修復完全自動化 k8sGPT

![](mermaid/k8sgpt.svg)

{{% note %}}
{{< mermaid >}}
graph LR
    subgraph " "
        direction LR
        A1(("K8s Events/Metrics"))
        B1("內部文件 RAG")
        C1("錯誤處理Runbook")
        D1("架構設計文件")
        E1("k8sGPT Apply")
        A1 --> B1
        B1 --> C1
        B1 --> D1
        A1 --> E1
        C1 --> E1
        D1 --> E1
    end
{{< /mermaid >}}
{{% /note %}}

當 k8s 事件或指標觸發時，k8sGPT 可以自動查詢內部文件、Runbook 或架構設計文件，並根據檢索到的內容生成修復建議。

- [KubeCon Europe 2025](https://www.youtube.com/watch?v=EXtCejkOJB0)
  - Superpowers for Humans of Kubernetes: How [K8sGPT](https://k8sgpt.ai/) Is Transforming Enterprise Ops - Alex Jones, AWS & Anais Urlichs, JP Morgan Chase

{{% /section %}}

---

{{% section %}}

##### 如何開始？

1. 學習如何使用 RAG 與 LLM Agent（ex. 參加我的工作坊）
2. 挑選一個簡單卻耗時的日常任務
3. 將任務所有已知的知識存入向量數據庫
4. 使用 RAG Agent 來回答問題
5. 結合通訊軟體（如 Slack）來提供即時回答
6. 根據使用者反饋不斷優化知識庫與回答方式

🔽

---

##### 如何改進？

1. 設定量化目標
2. Evaluation 量化 RAG Agent 性能
3. 根據 Evaluation 結果調整RAG，追求特定 Metrics（如回答準確率）提升
4. 持續迭代：根據使用者反饋與新知識更新向量數據庫

[../../slides/2025-06-05-devops-rag-internal-ai/#/32](../../slides/2025-06-05-devops-rag-internal-ai/#/32) /
[https://github.com/chechiachang/rag-workshop/blob/main/notebook/5_Evaluation.ipynb](https://github.com/chechiachang/rag-workshop/blob/main/notebook/5_Evaluation.ipynb)

---

##### 持續迭代

RAG Agent + Slack Bot 整合就可以完成第一個迭代版本

{{< mermaid >}}
graph LR
    subgraph " "
        direction LR
        A1(("RAG Agent"))
        B1("Slack")
        C1("Daily Jobs")
        A1 --實際使用--> B1
        B1 --更新知識--> A1
        B1 --Agent支援--> C1
        C1 --使用回饋--> B1
    end
{{< /mermaid >}}

---

> 從改善工程團隊品質出發，推廣到跨部門使用。
> 基於Evaluation與使用者體驗持續改進。

{{% /section %}}

---

### 總結

1. 什麼是 RAG
1. 為什麼需要 RAG
1. 為何需要內部知識庫
1. RAG Agent 的優勢
1. RAG Agent 的應用場景
1. 如何開始/如何進步

---

{{% section %}}

### Q & A

沒時間的話可以待會來找我聊天
🔽

---

### MaiCoin: We are Hiring!!

- [Senior Site Reliability Engineer](https://www.linkedin.com/jobs/view/4236558674/)
- [Senior Data Engineer](https://www.linkedin.com/jobs/view/4236555801)
- [Senior IT Engineer](https://www.linkedin.com/jobs/view/4236555811)
- [Blockchain Engineer (Wallet Team)](https://www.linkedin.com/jobs/view/4236556713)
- [Senior Backend Engineer](https://www.linkedin.com/jobs/view/4236558714)
- [Micro Service Software Engineer](https://www.linkedin.com/jobs/view/4236523560/)
- [Cyber Security Engineer](https://www.linkedin.com/jobs/view/4236559632)

{{% /section %}}
