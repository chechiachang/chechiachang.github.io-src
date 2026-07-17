---
title: "從實際落地案例到技術選擇"
date: '2026-10-14T00:00:00Z'
tags: ["ai", "generative", "ai-engineering", "vibe-coding", "coding-agent"]
categories: ["generative", "ai"]
description: "分享三個 AI 真正進入工程流程的案例：Blockchain full node operation platform、Logging Platform 與帳號稽核。"
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

### 📅 活動時間：2026-10-14
### 📘 聯繫我 [Facebook](https://www.facebook.com/engineer.from.scratch)

---

## Title

從實際落地案例到技術選擇

## Outline

這場分享以三個實際落地案例，說明不同問題該搭配什麼樣的 AI 開發方式，以及需求清楚程度、規格化流程與最終產出的取捨。

從需求明確、可以快速驗證的工具平台，到需要跨 team 協作的共用服務，再到整合多個異質系統的帳號稽核，我們會比較 Vibe Coding、SDD 與 Coding Agent 在實際工程中的差異。重點不在於選出唯一最佳的工具，而是理解問題的複雜度、規格成熟度與交付目標，如何影響技術選擇。

1. Blockchain full node operation platform：用 Vibe Coding 降低多鏈維護成本
2. Logging Platform：用 SDD 與 SpecKit 組織跨 team 需求
3. 帳號稽核：用 Coding Agent 整合多平台、不同 API 的權限盤點
4. 從案例看 AI workflow 的選擇

## Target group

- 正在導入 AI、但需要重新檢視成果的工程團隊
- 負責 AI strategy、平台與開發流程的技術主管
- 關心 AI application 落地、維運與長期成本的工程師

## 主要收穫

你將能從實際案例理解 Vibe Coding、SDD 與 Coding Agent 的適用情境，並學會根據需求清楚程度、系統複雜度與交付目標，選擇合適的 AI workflow。

## 實際落地案例

### 案例 1：Blockchain full node operation platform

- 需求：支援的 chain 太多，full node 維護成本高
- 方法：Vibe Coding
- 優勢：需求與規格清楚時，可以快速完成平台功能

### 案例 2：Logging Platform

- 需求：服務多、使用 team 多，需要共同的 logging platform
- 方法：SDD（Spec-driven Development）與 SpecKit
- 優勢：先整理規格與開發任務，讓跨 team 的需求有共同依據

### 案例 3：帳號稽核

- 需求：幾十個內部平台需要精細盤點權限；平台與工具持續增加，且每個平台的 API 規格都不同
- 方法：Coding Agent
- 優勢：不在意中間的實作過程，只關注最後是否產出可用的稽核結果

## Author

Che-Chia Chang 是一名專注於後端開發、開發維運、容器化應用及 Kubernetes 開發與管理的技術專家，同時也是 Microsoft 最有價值專業人士（MVP）。

活躍於台灣技術社群，經常在 CNTUG、DevOps Taipei、GDG Taipei、Golang Taipei Meetup 等社群分享 DevOps、SRE、Kubernetes、雲端與 AI Engineering 相關技術。

個人部落格：https://chechia.net
