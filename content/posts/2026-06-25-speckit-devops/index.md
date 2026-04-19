---
title: "DevOpsDay: 以規格為核心的 AI 強化 DevOps 平台工程"
date: '2026-07-01T13:20:00Z'
# weight: 1
# aliases: ["/test"]
tags: ["openai", "generative", "ai", "kubernetes", "devops"]
categories: ["generative", "ai"]
description: Spec-driven development (SDD) is a software development approach that emphasizes the use of specifications to drive the development process. In this workshop, we will explore how to implement SDD using Spec-kit, a powerful tool for creating and managing specifications. We will cover the basics of SDD, how to create effective specifications, and how to use Spec-kit to automate the development process. By the end of this workshop, you will have a solid understanding of SDD and how to apply it in your projects using Spec-kit.
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

### 📅 活動時間：2026-07-01T09:00-10:30
### 🔗 [活動連結](https://hwdc.ithome.com.tw/2025/lab-page/4003)
### 📘 聯繫我 [Facebook](https://www.facebook.com/engineer.from.scratch)
### 📑 [投影片](https://chechia.net/slides/2025-10-15-hello-dev-rag/#/)

---

### title

規格驅動的 AI 強化 DevOps 平台工程

AI-powered Spec-driven DevOps Platform Engineering

### Outline

現代 DevOps 的守備範圍日益擴張，從開發、測試、部署到維運、安全與合規，工作內容變得愈發碎片化且分散。團隊不僅要處理高度例行性且需精確執行（如部署、監控、驗證）的任務，還得應對複雜的跨團隊協作挑戰；然而，即便市面上工具琳瑯滿目，卻往往難以契合團隊既有的流程與文化，導致現狀常演變成「工具主導文化」，而非讓工具去適應團隊真實的作業邏輯。

在 DevOps 的日常運作中，其實存在大量適合導入「規格驅動開發（SDD）」的場景，特別是那些需求明確、重複性高且風險較低的瑣事。透過 SDD，我們可以將這些任務轉化為「可執行的規格」，並結合 AI 技術實現自動化，這不僅能大幅提升效率，更能有效避免人為操作的失誤。無論是自動處理例行文件、快速搭建測試環境，或是將既有的 SOP 與 Runbook 直接轉譯為自動化流程，SDD 都能藉由規格精準設定「完成（Done）」的標準，讓團隊從繁瑣作業中解放，同時確保交付品質始終如一。

本次演講將分享如何結合 AI 與規格驅動開發（SDD） 自建自動化系統，專門處理低磨合與低風險的日常事務，好讓工程人力能回歸到更高價值的工作上。

### References

過去有個笑話：DevOps 做的事是 Dev 與 Ops 都不想做的事

- https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
- https://www.youtube.com/watch?v=zypk-0oYtS8

## Author

Che-Chia Chang 是一名專注於後端開發、開發維運、容器化應用及 Kubernetes 開發與管理的技術專家，同時也是 Microsoft 最有價值專業人士（MVP）。

活躍於台灣技術社群，經常在 CNTUG、DevOps Taipei、GDG Taipei、Golang Taipei Meetup 等社群分享 DevOps、SRE、Kubernetes 及雲端運算相關技術。致力於推動開發與維運的最佳實踐，並熱衷於研究與應用最新的雲端與 AI 技術。

個人部落格：https://chechia.net

Che-Chia Chang is a technology expert specializing in backend development, DevOps, site reliability engineering (SRE), containerized applications, and Kubernetes development and management. He is also recognized as a Microsoft Most Valuable Professional (MVP).

Actively engaged in the Taiwanese tech community, he frequently shares insights on DevOps, SRE, Kubernetes, and cloud computing at CNTUG, DevOps Taipei, GDG Taipei, and Golang Taipei Meetup. Passionate about promoting best practices in development and operations, he continuously explores and applies the latest advancements in cloud and AI technologies.

https://chechia.net

---

### DevOps

身為 DevOps ，可以清楚知道某個需求對全團隊的 Impact，從中選擇適合的工具與流程，來達成目標。
敏捷開發，敏捷平台工程

做 Dev 的 DevOps

- DevOps 的 Spec 都很明確，追求明確指標，基於觀測與數據來做決策，避免模糊的需求

1. DevOps 的核心精神 (The Mental Spirit)
通常以 CALMS 框架來總結其精神支柱：
Culture (文化)：強調開發、維運、測試等團隊間的信任、透明度與共同責任感。
Automation (自動化)：消除手動操作，透過 CI/CD、自動化測試與基礎架構即程式碼 (IaC) 來提高效率。
Lean (精實)：專注於為客戶創造價值，消除開發流程中的浪費與瓶頸。
Measurement (測量)：透過數據監控系統性能與開發指標，作為持續改善的依據。
Sharing (分享)：在組織內部分享知識、工具與成功經驗，促進集體成長。
2. 實際意涵：三步工作法 (The Three Ways)
從實踐層面來看，DevOps 依循《The DevOps Handbook》提出的三種指導原則：
第一步：流動 (Flow)：建立由左至右（開發到維運）的平滑流動。透過小步快跑（小批量交付）與系統思考，最大化價值交付速度。
第二步：回饋 (Feedback)：建立由右至左（維運到開發）的回饋機制。及早發現錯誤，透過 監控工具 縮短修復時間。
第三步：持續學習與實驗 (Continual Learning)：鼓勵大膽實驗，將日常工作的改進制度化，從失敗中學習。


適合先行導入的項目
- 有 SOP 或 Runbook
- 高耗時例行工作
- 無其他服務依賴的流程
- 輔助工具
- 如運行多年的手動SOP，手動腳本、環境搭建、跨工具整合，開發文化統一，文件格式統一等。

不是自幹 Github，而是透過一層 AI tool shim，將提高自動化程度

data driven 的 feedback 驗證落地成果

以 Spec-kit 為例：
1. 對照業務目標與用戶影響，列出 DevOps 中最耗時的工作項目與可追蹤指標。
2. 用 AI 與 Spec-kit 範本撰寫可執行規格，將指標寫進規格內。
3. 將規格串接進 CI/CD 與監控管道，觀察交付成效並在持續學習中調整。

### 主要收穫

使用 Spec-kit 工具來撰寫和管理規格，並能將 SDD 原則應用於實際開發流程中，以提升開發效率和產品質量。並以實務經驗為基礎，分享踩雷經驗，分析適用與不適用的場景，幫助參與者更好地理解 SDD 的優勢和限制。

從無到有，而不是無中生有
明確的需求，如果 SDD 跑不出來，代表需求不夠明確，或是規格不夠好

重複性工作
使用 AI 補足初階 dev，快速產出 poc
滿足需求後直接產出高覆蓋率測試

產生依賴性要怎麼辦？
根據現成的扣產生新的更明確的Spec
- 改寫語言
- 改架構
- Involve 真人 Dev

### content

AI SDD vs human
- lightning fast debug in easy to medium complexity
- more constrained to the spec, more reliable code
