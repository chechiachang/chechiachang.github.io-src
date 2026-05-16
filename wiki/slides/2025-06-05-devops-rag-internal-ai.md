# Workshop: RAG打造企業AI知識庫：把一甲子功力傳給新人

- Source: `content/slides/2025-06-05-devops-rag-internal-ai/_index.md`
- Slide: `https://chechia.net/slides/2025-06-05-devops-rag-internal-ai/`
- Date: `2025-06-01T00:45:00Z`
- Tags: `rag, devops`
- Categories: `devops`
- Description: `學員將學會如何利用 RAG 技術，結合 OpenAI、LangChain、Qdrant 向量數據庫，構建企業內部文檔的智能知識庫，並能設計與實作一個基於自然語言處理（NLP）的查詢系統，來提升開發團隊的效率與知識管理能力。`

## Pages (Section | Summary)

1. `(frontmatter)` | Frontmatter metadata for reveal-hugo settings and slide metadata.
2. `RAG workshop 行前通知：基本需求` | RAG workshop 行前通知：基本需求
3. `選項1: 使用自己的電腦 :computer:` | 選項1: 使用自己的電腦 :computer:
4. `選項2: 使用遠端 VM` | 選項2: 使用遠端 VM
5. `建議` | 建議
6. `投影片與教材與完整程式碼放在網站上` | 投影片與教材與完整程式碼放在網站上
7. `以下是 RAG Workshop 當天內容` | 以下是 RAG Workshop 當天內容
8. `RAG Workshop` | RAG Workshop
9. `關於我` | 關於我
10. `RAG Workshop 流程` | RAG Workshop 流程
11. `選項1: 使用自己的電腦` | 選項1: 使用自己的電腦
12. `選項2: 使用遠端 VM` | 選項2: 使用遠端 VM
13. `(frontmatter)` | No textual content.
14. `選項2: 使用 ngrok 連線到 jupyter notebook` | 選項2: 使用 ngrok 連線到 jupyter notebook
15. `以上是 Workshop 環境設定` | 以上是 Workshop 環境設定
16. `(frontmatter)` | No textual content.
17. `RAG Workshop 流程` | RAG Workshop 流程
18. `什麼是 RAG` | 什麼是 RAG
19. `(frontmatter)` | https://cookbook.openai.com/images/llamaindex_rag_overview.png
20. `知識獲取效率在 DevOps 的難題` | 知識獲取效率在 DevOps 的難題
21. `情境：新人工程師要如何到 k8s doc 查到想要的內容？` | 情境：新人工程師要如何到 k8s doc 查到想要的內容？
22. `(frontmatter)` | No textual content.
23. `(frontmatter)` | https://kubernetes.io/search/
24. `情境：Senior 工程師要如何分享知識？` | 情境：Senior 工程師要如何分享知識？
25. `(frontmatter)` | 我們不是懶，而是現在要解答許多基本問題，LLM 回答得比人好
26. `RAG 讓 DevOps 更智慧的即時反應` | RAG 讓 DevOps 更智慧的即時反應
27. `(frontmatter)` | > DevOps AI Copilot 不應該像圖書館守門員等人來借書，
28. `RAG vs 其他工具` | RAG vs 其他工具
29. `(frontmatter)` | 適合用 RAG 的情境：客服問答、技術搜尋、知識型 Chatbot、內部知識導航。
30. `有了大語言模型後` | 有了大語言模型後
31. `(frontmatter)` | chatgpt 會用通順的語言，快速（數秒內）上網搜尋，回答問題
32. `LLM 不具備專業知識。缺乏內容根據時，容易產生幻覺(hallucination)` | LLM 不具備專業知識。缺乏內容根據時，容易產生幻覺(hallucination)
33. `RAG Workshop 流程` | RAG Workshop 流程
34. `RAG Workshop 流程` | RAG Workshop 流程
35. `如何評估 RAG 系統的品質?` | 如何評估 RAG 系統的品質?
36. `評估：確保回答品質可靠性與可控性` | 評估：確保回答品質可靠性與可控性
37. `RAG 應用: 以 k8s official docs 為例` | RAG 應用: 以 k8s official docs 為例
38. `總結` | 總結
39. `由衷地感謝為 workshop 提供協助的夥伴!` | 由衷地感謝為 workshop 提供協助的夥伴!
40. `MaiCoin: We are Hiring!!` | MaiCoin: We are Hiring!!
41. `DIY + Q&A + 建議` | DIY + Q&A + 建議

## Time-to-Syntax

- Markdown:
- `p3:code-fence`
- `p3:link`
- `p4:link`
- `p6:link`
- `p7:image`
- `p9:link`
- `p11:code-fence`
- `p11:link`
- `p12:link`
- `p13:image`
- `p14:code-fence`
- `p16:image`
- `p19:image`
- `p19:link`
- `p22:image`
- `p23:image`
- `p23:link`
- `p25:image`
- `p29:image`
- `p32:image`
- `p39:link`
- `p40:link`
- Hugo shortcode:
- `p21:{{% note %}}`
- `p21:{{% /note %}}`
- `p23:{{% note %}}`
- `p23:{{% /note %}}`
- `p24:{{% note %}}`
- `p24:{{% /note %}}`
- `p25:{{% note %}}`
- `p25:{{% /note %}}`
- `p27:{{% note %}}`
- `p27:{{% /note %}}`
- `p28:{{% note %}}`
- `p28:{{% /note %}}`
- `p29:{{% note %}}`
- `p29:{{% /note %}}`
- `p30:{{% note %}}`
- `p30:{{% /note %}}`
- `p32:{{% note %}}`
- `p32:{{% /note %}}`
- `p36:{{% note %}}`
- `p36:{{% /note %}}`
- Reveal-hugo syntax:
- none.

## Time-to-Sentence

- Markdown:
- `p1:description: "學員將學會如何利用 RAG 技術，結合 OpenAI、LangChain、Qdrant 向量數據庫，構建企業內部文檔的智能知識庫，並能設計與實作一個基於自然語言處理（NLP）的查詢系統，來提升開發團隊的效率與知識管理能力。"`
- `p2:選項2: 用電腦遠端連線講師提供的 VM，在遠端VM 中運行 docker 開發環境`
- `p3:登入token=workshop1234!`
- `p3:docker exec -it notebook pip install pandas openai qdrant_client tqdm tenacity wget tenacity unstructured markdown ragas sacrebleu langchain_qdrant langchain-openai langchain_openai langchain_community tiktoken ipywidgets`
- `p4:Ngrok 登入 Login -> 左手邊 Identity & Access -> Authtokens -> Add Tunnel authtoken -> 記在安全的地方`
- `p5:在家先試跑一遍，把 docker image 跟 pip 套件都下載好，現場要載很久`
- `p9:個人部落格chechia.net 投影片講稿，鐵人賽 (Terraform / Vault 手把手入門 / Etcd Workshop)`
- `p10:10min - Notebook 2 Embedding 與向量數據庫`
- `p10:10min - Notebook 3 Embedding Search`
- `p10:10min - Notebook 6 k8s RAG QA`
- `p11:notebook token: workshop1234!`
- `p12:googel sheet 左邊 url，開啟 bastion 連線`
- `p14:選項2: 使用 ngrok 連線到 jupyter notebook`
- `p14:進入 VM 後，修改下面 ngrok authtoken。指令一行一行貼上（右鍵）到 bastion 中執行`
- `p14:t=2025-06-02T06:17:41+0000 lvl=info msg="started tunnel" obj=tunnels name=command_line addr=http://notebook:8888 url=https://4d11-52-230-24-207.ngrok-free.app`
- `p17:實際應用: 以 k8s official docs 為例`
- `p18:Retrieval（檢索）： 從一個外部知識庫（如文件、向量資料庫等）中找到與問題相關的資訊。通常會用語意向量（embeddings）做相似度搜尋。`
- `p18:Generation（生成）： 把檢索到的內容與使用者問題一起丟給 LLM（如 GPT、Claude 等）去生成答案。生成的內容會更具事實根據，並能引用具體資料。`
- `p21:情境：新人工程師要如何到 k8s doc 查到想要的內容？`
- `p21:k8s doc 有提供關鍵字搜尋，這個搜尋功能是怎麼做的？`
- `p21:Fulltext Search Engine 例如 elasticsearch 使用 Lucene`
- `p24:情境：Senior 工程師要如何分享知識？`
- `p27:> 而應該像導航系統，在你開車時主動告訴你：前方有彎道。`
- `p28:需要工具提升知識獲取效率，如何選擇 RAG 或是其他 non-LLM 工具？例如 search engine / fulltext search engine / search algorithm`
- `p28:elasticsearch / lucene / fulltext search engine`
- `p28:GNU grep 的 Boyer–Moore string-search algorithm`
- `p29:適合用 RAG 的情境：客服問答、技術搜尋、知識型 Chatbot、內部知識導航。`
- `p29:適合用傳統程式的情境：金流控制、流程引擎、帳務系統、安全控制。`
- `p32:LLM（大型語言模型）本身並不具備事實知識，而是依賴訓練時的語料與提示輸入來生成回答。當缺乏明確上下文或內容根據時，LLM 容易出現「幻覺」現象，即生成看似合理但實際不正確的資訊。專業領域問題若未提供準確資料支撐，也容易導致錯誤回答。`
- `p35:如何評估 RAG 系統的品質?`
- `p35:人人都會下 prompt，但是誰的 prompt 更好？或是沒差別？`
- `p35:如何選擇 vector store 的 chunking 策略？`
- `p35:哪個 retriever 更好？`
- `p35:要如何持續改善 RAG 系統？下個迭代的改善方向是什麼？`
- `p36:Faithfulness：依據來源資料生成？`
- `p37:RAG 應用: 以 k8s official docs 為例`
- `p39:由衷地感謝為 workshop 提供協助的夥伴!`
- `p40:MaiCoin: We are Hiring!!`
- Hugo shortcode:
- `p21:{{% note %}}`
- `p21:{{% /note %}}`
- `p23:{{% note %}}`
- `p23:{{% /note %}}`
- `p24:{{% note %}}`
- `p24:{{% /note %}}`
- `p25:{{% note %}}`
- `p25:{{% /note %}}`
- `p27:{{% note %}}`
- `p27:{{% /note %}}`
- `p28:{{% note %}}`
- `p28:{{% /note %}}`
- `p29:{{% note %}}`
- `p29:{{% /note %}}`
- `p30:{{% note %}}`
- `p30:{{% /note %}}`
- `p32:{{% note %}}`
- `p32:{{% /note %}}`
- `p36:{{% note %}}`
- `p36:{{% /note %}}`
- Reveal-hugo syntax:
- none.
