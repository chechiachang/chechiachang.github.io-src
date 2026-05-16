# Cloud Summit 2025: 用 RAG 打造企業可對話 AI 知識庫《有問題問過 AI 後再來問我》

- Source: `content/slides/2025-07-02-cloud-summit-rag/_index.md`
- Slide: `https://chechia.net/slides/2025-07-02-cloud-summit-rag/`
- Date: `2025-06-25T00:45:00Z`
- Tags: `rag, devops`
- Categories: `devops`
- Description: `透過 RAG（檢索增強生成）技術，將企業內部文件轉為智能知識庫，提升資訊檢索與決策效率。本演講將探討 RAG 應用、技術架構與落地實踐，幫助開發團隊與企業更高效利用內部知識。企業內部文件往往分散於 Confluence、Google Drive、Notion 等平台，傳統關鍵字搜尋難以快速獲取準確資訊，導致溝通成本高、開發流程受阻。本演講將介紹如何運用 RAG（Retrieval-Augmented Generation）技術，結合 OpenAI 及向量數據庫，將企業內部文檔轉為智能知識庫。我們將探討文件解析、嵌入索引、AI 問答系統的技術架構與實作，幫助開發團隊構建高效 AI 助手，節省溝通成本，加速開發流程，提升決策與問題解決能力`

## Pages (Section | Summary)

1. `(frontmatter)` | Frontmatter metadata for reveal-hugo settings and slide metadata.
2. `Cloud Summit 2025` | Cloud Summit 2025
3. `(frontmatter)` | 🔽
4. `DevOpsDay 2025: RAG Workshop` | DevOpsDay 2025: RAG Workshop
5. `(frontmatter)` | No textual content.
6. `大綱` | 大綱
7. `什麼是 RAG` | 什麼是 RAG
8. `什麼是 RAG` | 什麼是 RAG
9. `(frontmatter)` | graph LR
10. `(frontmatter)` | graph LR
11. `為什麼使用 RAG？` | 為什麼使用 RAG？
12. `LLM 不具備專業知識。缺乏內容根據時，容易產生幻覺(hallucination)` | LLM 不具備專業知識。缺乏內容根據時，容易產生幻覺(hallucination)
13. `(frontmatter)` | No textual content.
14. `簡單的RAG範例` | 簡單的RAG範例
15. `使用 Qdrant 作為向量數據庫` | No textual content.
16. `可以增強 gpt-4o 的冷笑話知識` | 可以增強 gpt-4o 的冷笑話知識
17. `或是把 K8s 官方文件全部塞進 vector DB` | 或是把 K8s 官方文件全部塞進 vector DB
18. `我知道 RAG 是什麼了，但為何要打造內部知識庫？` | 我知道 RAG 是什麼了，但為何要打造內部知識庫？
19. `我知道 RAG 是什麼了，但為何要打造內部知識庫？` | 我知道 RAG 是什麼了，但為何要打造內部知識庫？
20. `使用 RAG Agent 增強內部知識傳遞` | 使用 RAG Agent 增強內部知識傳遞
21. `RAG Agent 的優勢` | RAG Agent 的優勢
22. `RAG Agent + MCP Server` | RAG Agent + MCP Server
23. `RAG 自動化: 新人 onboarding` | RAG 自動化: 新人 onboarding
24. `RAG 自動化: 第一時間Alert處理` | RAG 自動化: 第一時間Alert處理
25. `(frontmatter)` | > AI Copilot 不應該像圖書館守門員等人來借書，
26. `修復完全自動化 k8sGPT` | 修復完全自動化 k8sGPT
27. `如何開始？` | 如何開始？
28. `如何改進？` | 如何改進？
29. `持續迭代` | 持續迭代
30. `(frontmatter)` | > 從改善工程團隊品質出發，推廣到跨部門使用。
31. `總結` | 總結
32. `Q & A` | Q & A
33. `MaiCoin: We are Hiring!!` | MaiCoin: We are Hiring!!

## Time-to-Syntax

- Markdown:
- `p2:link`
- `p4:link`
- `p5:image`
- `p9:image`
- `p10:image`
- `p12:image`
- `p13:image`
- `p14:code-fence`
- `p14:link`
- `p15:code-fence`
- `p16:image`
- `p17:link`
- `p20:link`
- `p22:image`
- `p22:link`
- `p23:image`
- `p24:image`
- `p26:image`
- `p26:link`
- `p28:link`
- `p33:link`
- Hugo shortcode:
- `p3:{{% section %}}`
- `p3:{{< slide content="slides.about-me" >}}`
- `p5:{{% /section %}}`
- `p7:{{% section %}}`
- `p9:{{% note %}}`
- `p9:{{< mermaid >}}`
- `p9:{{< /mermaid >}}`
- `p10:{{% note %}}`
- `p10:{{< mermaid >}}`
- `p10:{{< /mermaid >}}`
- `p12:{{% note %}}`
- `p12:{{% /note %}}`
- `p13:{{% /section %}}`
- `p14:{{% section %}}`
- `p17:{{% /section %}}`
- `p18:{{% section %}}`
- `p22:{{% note %}}`
- `p22:{{< mermaid >}}`
- `p22:{{< /mermaid >}}`
- `p23:{{% note %}}`
- `p23:{{< mermaid >}}`
- `p23:{{< /mermaid >}}`
- `p24:{{% note %}}`
- `p24:{{< mermaid >}}`
- `p24:{{< /mermaid >}}`
- `p25:{{% note %}}`
- `p25:{{% /note %}}`
- `p26:{{% note %}}`
- `p26:{{< mermaid >}}`
- `p26:{{< /mermaid >}}`
- `p27:{{% section %}}`
- `p29:{{< mermaid >}}`
- `p29:{{< /mermaid >}}`
- `p30:{{% /section %}}`
- `p32:{{% section %}}`
- `p33:{{% /section %}}`
- Reveal-hugo syntax:
- none.

## Time-to-Sentence

- Markdown:
- `p1:title: "Cloud Summit 2025: 用 RAG 打造企業可對話 AI 知識庫《有問題問過 AI 後再來問我》"`
- `p1:description: 透過 RAG（檢索增強生成）技術，將企業內部文件轉為智能知識庫，提升資訊檢索與決策效率。本演講將探討 RAG 應用、技術架構與落地實踐，幫助開發團隊與企業更高效利用內部知識。企業內部文件往往分散於 Confluence、Google Drive、Notion 等平台，傳統關鍵字搜尋難以快速獲取準確資訊，導致溝通成本高、開發流程受阻。本演講將介紹如何運用 RAG（Retrieval-Augmented Generation）技術，結合 OpenAI 及向量數據庫，將企業內部文檔轉為智能知識庫。我們將探討文件解析、嵌入索引、AI 問答系統的技術架構與實作，幫助開發團隊構建高效 AI 助手，節省溝通成本，加速開發流程，提升決策與問題解決能力`
- `p2:~ Che Chia Chang @ chechia.net ~`
- `p8:Retrieval（檢索）： 從一個外部知識庫（如文件、向量資料庫等）中找到與問題相關的資訊。通常會用文字嵌入向量（embeddings）做相似度搜尋。`
- `p8:Generation（生成）： 把檢索到的內容與使用者問題一起丟給 LLM（如 GPT、Claude 等）去生成答案。生成的內容會更具事實根據，並能引用具體資料。`
- `p11:為什麼使用 RAG？`
- `p11:而不是只根據 Model 訓練資料，進行生成式回答。`
- `p12:LLM（大型語言模型）本身並不具備事實知識，而是依賴訓練時的語料與提示輸入來生成回答。當缺乏明確上下文或內容根據時，LLM 容易出現「幻覺」現象，即生成看似合理但實際不正確的資訊。專業領域問題若未提供準確資料支撐，也容易導致錯誤回答。`
- `p14:│ User Input │ │ Embedding Model │`
- `p14:│ (e.g., Query)├──────▶│ (OpenAI Embeddings) │`
- `p14:│ (Query + Top-K Contexts) │`
- `p15:def query_docs(query, collection_name="covid-qa-3-large", model="text-embedding-3-large" , top_k=5):`
- `p15:example: "What is COVID-19?" -> [0.1, 0.2, 0.3, ...] 一個固定長度的向量`
- `p15:返回指定 collection_name 中與 query_embeddings 最相似的前 top_k 個點`
- `p15:payloads = [point.payload["answer"] for point in results.points]`
- `p15:將 context 與原始問題組合成 prompt 將 query + context 組合起來，如：`
- `p17:透過 prompt 嚴格限制 LLM 根據上下文提供的文件回答，而不要依賴 LLM 的訓練資料`
- `p18:我知道 RAG 是什麼了，但為何要打造內部知識庫？`
- `p19:我知道 RAG 是什麼了，但為何要打造內部知識庫？`
- `p20:Agent 結合 function tools / mcp server 可以整合更多資料來源`
- `p22:透過 MCP Protocol，可以將不同的資料來源（如 Confluence、Github、Slack 等）整合到 RAG Agent 中。這樣，RAG Agent 可以在不同的上下文中提供一致的回答。不需要寫額外的程式碼，或只需要 LLM generate 一些簡單的程式碼。`
- `p23:傳統的 onboarding 過程往往依賴資深工程師手動指導和文檔查閱，效率低下。透過 RAG Agent，可以提供互動式的 onboarding 體驗，並且可以不斷溫習和更新知識。`
- `p24:工程師處理 alert 時，通常需要查閱內部文件、Runbook 或架構設計文件。這些文件往往分散在不同的系統中，導致查找過程耗時。`
- `p25:> 而應該像導航系統，在你開車時主動告訴你：前方有彎道。`
- `p26:當 k8s 事件或指標觸發時，k8sGPT 可以自動查詢內部文件、Runbook 或架構設計文件，並根據檢索到的內容生成修復建議。`
- `p26:Superpowers for Humans of Kubernetes: How K8sGPT Is Transforming Enterprise Ops - Alex Jones, AWS & Anais Urlichs, JP Morgan Chase`
- `p27:如何開始？`
- `p27:學習如何使用 RAG 與 LLM Agent（ex. 參加我的工作坊）`
- `p28:如何改進？`
- `p29:RAG Agent + Slack Bot 整合就可以完成第一個迭代版本`
- `p30:> 從改善工程團隊品質出發，推廣到跨部門使用。`
- `p30:> 基於Evaluation與使用者體驗持續改進。`
- `p33:MaiCoin: We are Hiring!!`
- Hugo shortcode:
- `p3:{{% section %}}`
- `p3:{{< slide content="slides.about-me" >}}`
- `p5:{{% /section %}}`
- `p7:{{% section %}}`
- `p9:{{% note %}}`
- `p9:{{< mermaid >}}`
- `p9:{{< /mermaid >}}`
- `p9:{{% /note %}}`
- `p10:{{% note %}}`
- `p10:{{< mermaid >}}`
- `p10:{{< /mermaid >}}`
- `p10:{{% /note %}}`
- `p12:{{% note %}}`
- `p12:{{% /note %}}`
- `p13:{{% /section %}}`
- `p14:{{% section %}}`
- `p17:{{% /section %}}`
- `p18:{{% section %}}`
- `p22:{{% note %}}`
- `p22:{{< mermaid >}}`
- `p22:{{< /mermaid >}}`
- `p22:{{% /note %}}`
- `p23:{{% note %}}`
- `p23:{{< mermaid >}}`
- `p23:{{< /mermaid >}}`
- `p23:{{% /note %}}`
- `p24:{{% note %}}`
- `p24:{{< mermaid >}}`
- `p24:{{< /mermaid >}}`
- `p24:{{% /note %}}`
- `p25:{{% note %}}`
- `p25:{{% /note %}}`
- `p26:{{% note %}}`
- `p26:{{< mermaid >}}`
- `p26:{{< /mermaid >}}`
- `p26:{{% /note %}}`
- `p26:{{% /section %}}`
- `p27:{{% section %}}`
- `p29:{{< mermaid >}}`
- `p29:{{< /mermaid >}}`
- `p30:{{% /section %}}`
- `p32:{{% section %}}`
- `p33:{{% /section %}}`
- Reveal-hugo syntax:
- none.
