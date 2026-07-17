---
title: "用 Sidecar 模式將 Day-2 運維轉化為 Self-Service 平台"
date: '2026-10-29T00:00:00Z'
tags: ["platform-engineering", "sre", "developer-experience", "gitops"]
categories: ["platform-engineering", "devops"]
description: "以 Sidecar 封裝重型有狀態服務的 Day-2 運維，結合 GitHub Flow 建立安全、可自助使用的平台。"
showToc: true
TocOpen: false
draft: true
hidemeta: false
comments: true
showSummary: true
ShowReadingTime: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
---

### 📅 活動時間：2026-10-29
### 📘 聯繫我 [Facebook](https://www.facebook.com/engineer.from.scratch)

## Title

用 Sidecar 模式將 Day-2 運維轉化為 Self-Service 平台：重型有狀態服務的平台化實踐

## Outline

Stateless 服務的自動化已經相當成熟，但重型有狀態服務的節點輪替、版本升降級、備份與還原，仍然高度依賴維運人員的經驗與手工作業。

這場分享將說明如何以「Platform as a Product」的思維，打造專門服務 Stateful Core Service 的運維 Sidecar，把複雜的 Day-2 操作封裝成可驗證、可重複執行的平台能力，再透過 GitHub Flow 提供跨團隊的 Self-Service 黃金路徑。

1. 為什麼 Stateful 服務是 Platform Engineering 的終極挑戰
2. Stateful Core Service 與運維 Sidecar 的架構與協作方式
3. 版本升降級、配置更新與 EC2 Node Rotation 的自動化
4. Snapshot、備份與 Restore 的 Data Resilience 設計
5. 結合 GitHub Flow 的 Self-Service 與 GitOps 流程
6. 權限控制、防呆 Guardrails 與生產環境安全
7. 從救火隊到平台軟體工程師：實戰成果與團隊轉型

## Target group

- 負責 Stateful Core Service、雲端基礎設施或 SRE 的工程師
- 正在建立 Developer Platform、Internal Developer Platform 或 GitOps 流程的平台團隊
- 想降低手動維運、提升 Developer Experience 的技術主管

## 主要收穫

1. 了解如何用 Sidecar 封裝複雜的 Day-2 運維邏輯。
2. 掌握 Stateful 服務進行節點輪替、版本升級與備份還原時的自動化設計。
3. 學會結合 GitHub Flow 建立兼顧 Self-Service、安全與可維運性的 Golden Path。

## Author

Che-Chia Chang 是一名專注於後端開發、開發維運、容器化應用及 Kubernetes 開發與管理的技術專家，同時也是 Microsoft 最有價值專業人士（MVP）。

活躍於台灣技術社群，經常在 CNTUG、DevOps Taipei、GDG Taipei、Golang Taipei Meetup 等社群分享 DevOps、SRE、Kubernetes、雲端與 AI Engineering 相關技術。

個人部落格：https://chechia.net
