---
title: "When Not to Vibe：從 Vibe Coding 到 Spec-driven AI Engineering 的轉折點"
date: '2026-07-01T13:20:00Z'
# weight: 1
# aliases: ["/test"]
tags: ["openai", "generative", "ai", "speckit", "devops"]
categories: ["generative", "ai"]
description: 這場分享從 vibe coding 的失焦問題出發，拆解 LLM 在長時間任務中的限制，並說明 SpecKit 在 spec-driven AI engineering 中的角色、代價與適用場景，以及從 spec-driven 走向 agent-driven 的演進方向。
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

### 活動時間：2026-07-01T09:00-10:30
### [活動連結](https://hwdc.ithome.com.tw/2025/lab-page/4003)
### 聯繫我 [Facebook](https://www.facebook.com/engineer.from.scratch)
### [投影片](https://chechia.net/slides/2026-07-01-speckit-cloud-summit/)

---

### Title

When Not to Vibe  
從 Vibe Coding 到 Spec-driven AI Engineering

### Outline

AI 讓「寫 code」變得容易，但實際在開發上，常見現象是一開始很順、越做越亂，LLM 逐步偏離設計，context 越長結果反而越不準。這不是 prompt 不夠強或模型不夠大，而是 LLM 本質上不擅長長時間、持續演進的任務。vibe coding 適合快速探索小範圍任務與短期 context，但長任務會走向失焦（loss of alignment）；context window 也不是越大越好，資訊堆疊會造成 attention 稀釋，且 LLM 沒有真正長期記憶。

這場分享現實：AI 讓寫 code 變快，卻不保證長時間任務不失焦；為何 vibe coding 會在 context 拉長後 drift。並以 SpecKit 補上的結構化上下文價值、並了解其代價，以及從 spec-driven 走向 agent-driven 的實務經驗。

1. 從 Vibe 出發：為何 LLM 在長時間任務中逐漸失焦
2. LLM 原理：Context 不斷堆疊，為何反而降低準確性
3. SpecKit 的價值：從 Prompt Chaos 到 Structured Spec 作為 Source of Truth
4. 現實限制：Spec Tax、Drift，以及無法解決的痛點
5. SDD（Spec-driven Development）適用場景：PoC、Greenfield 等
6. 從 Spec-driven 到 Agent-driven：Speckit 作為過渡形態

你將能清楚辨識 vibe coding 的有效範圍與失效訊號、理解 LLM 在長上下文下準確率下降的原因、評估 SpecKit 在實務上的收益與成本，並帶走一套可用於 PoC、Greenfield 與複雜系統規劃的導入與決策視角。

### Target group

- 正在使用 AI 開發、但感受到流程越來越混亂的工程師
- 想把 AI 導入團隊 workflow 的技術主管與架構師
- 關注 AI-native engineering 與開發流程演進的實務工作者

### 主要收穫

你將能清楚辨識 vibe coding 的有效範圍與失效訊號、理解 LLM 在長上下文下準確率下降的原因、評估 SpecKit 在實務上的收益與成本，並帶走一套可用於 PoC、Greenfield 與複雜系統規劃的導入與決策視角。

### Description

SpecKit 的核心價值在於把短期對話轉換為可持續、可引用的結構化上下文（Prompt -> Spec），但它並非銀彈，仍有 Spec Tax、Spec Drift、Cognitive Overload 等成本，且無法徹底解決失焦問題。實務上，Spec-driven Development 較適合 PoC、Greenfield 與複雜系統設計，不適合小功能、快速迭代或重度 legacy；長期來看，SpecKit 更像是從 prompt-driven 走向 agent-driven systems 的過渡形態。

### References

- SpecKit Official Repository  
  https://github.com/spec-kit/spec-kit
- Prompt Engineering for Spec-driven Development  
  https://techcommunity.microsoft.com/
- Community Discussions on Spec-driven Development  
  https://www.reddit.com/r/SpecDrivenDevelopment/
- GitHub Copilot Community Insights  
  https://www.reddit.com/r/GithubCopilot/

## Author

Chechia Chang

- Organizer of Golang Taipei
- DevOps / SRE / Cloud / AI Speaker
- Focus on Kubernetes, Cloud Infrastructure, and AI Engineering

---

> When vibe coding stops working,  
> it's time to design how AI remembers.
