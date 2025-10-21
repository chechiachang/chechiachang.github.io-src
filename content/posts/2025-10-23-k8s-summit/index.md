---
title: "K8s Summit 2025: RAG + k8sGPT 檢索增強生成與 K8sGPT"
date: '2025-10-01T13:20:00Z'
# weight: 1
# aliases: ["/test"]
tags: ["rag", "devops", "kubernetes", "aiops"]
categories: ["kubernetes", "aiops"]
description: "K8sGPT 是一套結合 AI 與最佳實踐的 Kubernetes 問題診斷與修復工具，能有效降低故障排除難度並自動化修復流程。RAG（Retrieval-Augmented Generation 檢索增強生成）結合檢索系統與生成式模型（如 GPT）的自然語言處理架構，在生成答案時引用外部知識，使模型回答更準確且具事實根據。本演講將介紹如何使用 RAG 技術來增強 Kubernetes 問題診斷與修復的能力，並展示 k8sGPT 的實際應用。"
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

### 📅 活動時間：2025-10-23T13:30-14:10 (ABC會議室)
### 🔗 [活動連結](https://k8s.ithome.com.tw/2025/session-page/4081)
### 📘 聯繫我 [Facebook](https://www.facebook.com/engineer.from.scratch)
### 📑 [投影片](https://chechia.net/slides/2025-10-22-etcd-workshop)

---

## Workshop

Workshop: Get started with Etcd & Kubernetes / 手把手搭建 Etcd 與 K8s Components

### Outline

**K8sGPT** 是一個結合 AI 的 Kubernetes 叢集診斷與自動化排錯工具，能自動掃描叢集狀態、辨識異常並用自然語言解釋問題，提供可執行的修復建議，甚至支援自動修復。K8sGPT 讓使用者用更低門檻掌握叢集健康狀況，加速問題定位與排除，是 DevOps 與 SRE 團隊提升營運效率的實用工具。

在排查問題時，比起人類工程師，K8sGPT 缺乏對 workload 架構的深入了解，也無法存取內部架構設計文件，或是 Runbook 與 SOP。這限制了其診斷能力並可能因為幻覺（hallucination）而提供不正確的建議。K8sGPT 主要依賴 Kubernetes API 與叢集狀態資訊來進行診斷，但這些資訊並不足以涵蓋所有可能的問題情境。

本次演講展現一個使用案例，嘗試透過 RAG（Retrieval-Augmented Generation 檢索增強生成）技術來增強其診斷能力，展現目前基於大語言模型的解決方案，面對 Kubernetes 叢集問題時的優勢與挑戰。

參考資料
- [https://k8sgpt.ai/](https://k8sgpt.ai/)
- [KubeCon Europe 2025/04/02 Superpowers for Humans of Kubernetes: How K8sGPT Is Transforming Enter... Alex Jones & Anais Urlichs](https://www.youtube.com/watch?v=EXtCejkOJB0)

## Author

Che-Chia Chang 是一名專注於後端開發、開發維運、容器化應用及 Kubernetes 開發與管理的技術專家，同時也是 Microsoft 最有價值專業人士（MVP）。

活躍於台灣技術社群，經常在 CNTUG、DevOps Taipei、GDG Taipei、Golang Taipei Meetup 等社群分享 DevOps、SRE、Kubernetes 及雲端運算相關技術。致力於推動開發與維運的最佳實踐，並熱衷於研究與應用最新的雲端與 AI 技術。

個人部落格：https://chechia.net

Che-Chia Chang is a technology expert specializing in backend development, DevOps, site reliability engineering (SRE), containerized applications, and Kubernetes development and management. He is also recognized as a Microsoft Most Valuable Professional (MVP).

Actively engaged in the Taiwanese tech community, he frequently shares insights on DevOps, SRE, Kubernetes, and cloud computing at CNTUG, DevOps Taipei, GDG Taipei, and Golang Taipei Meetup. Passionate about promoting best practices in development and operations, he continuously explores and applies the latest advancements in cloud and AI technologies.

https://chechia.net
