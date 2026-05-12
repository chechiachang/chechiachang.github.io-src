---
title: "AI 強化的規格驅動開發：自動化所有 SOP 與 Runbook"
description: "以 Spec-driven development（SDD）結合 AI Agent，把 SOP 與 Runbook 轉為可執行規格，建立可驗證、可回歸、可持續交付的自動化流程。"
tags: ["ai", "sdd", "spec", "agent", "devops", "runbook", "sop"]
categories: ["ai", "devops"]
date: '2026-07-01T12:00:00Z'
outputs: ["Reveal"]
reveal_hugo:
  custom_theme: "reveal-hugo/themes/robot-lung.css"
  margin: 0.2
  highlight_theme: "color-brewer"
  transition: "slide"
  transition_speed: "fast"
---

## From Spec to Code
### 控制 LLM Coding Agent 的實務方法

---

## 今天只講一件事

> 怎麼讓 LLM「穩定寫對 code」

---

## 現況（大家都懂）

```text
Prompt -> Code -> 修 -> 再 Prompt
```

---

## 問題

- 不穩
- 不可預測
- 無法 debug
- 無法 scale

---

## GitHub 怎麼說？

> looks right, but does not quite work

---

## 關鍵問題

> LLM 很會補 pattern
> 但不會讀你的腦

---

## 解法：Spec-driven development

---

## 核心概念

- Spec = source of truth
- Code = artifact

---

## Spec Kit 是什麼？

GitHub 的 SDD toolkit

---

## 基本流程

```text
/specify -> /plan -> /tasks -> /implement
```

---

## 每一步在幹嘛？

- specify -> 需求變成 spec
- plan -> 設計
- tasks -> 拆任務
- implement -> 寫 code

---

## 重點

> 每一步都有 artifact

---

## Demo（快速帶）

接 demo repo

---

## Spec Kit 的優點

---

## 1. 結構化

不再是 free-form prompt

---

## 2. 減少猜測

spec 把 ambiguity 拿掉

---

## 3. 可重複

同一 spec -> 類似結果

---

## 跟 vibe coding 比

---

## Vibe coding

- 快
- 但不穩
- 無法 scale

---

## Spec Kit

- 慢一點
- 但穩
- 可工程化

---

## 一句話

> Prompt 是聊天
> Spec 是工程

---

## 但 Spec Kit 解完了嗎？

還沒有

---

## 為什麼？

```text
Spec -> Plan -> Tasks -> Implement
```

---

## 缺了什麼？

```text
Test -> Evaluate -> Iterate
```

---

## 關鍵問題

> 誰來告訴你「這是對的？」

---

## /analyze 不夠

- 有 consistency check
- 沒有 quality control

---

## 所以會發生

- code 能跑
- 但不一定正確
- 更不一定好

---

## More than Spec Kit

---

## 加三個東西

```text
1. Evaluation
2. Iteration loop
3. Automation
```

---

## 1) Evaluation（最重要）

- 不只 test
- spec alignment
- code quality
- simplicity

---

## 可以怎麼做？

```text
LLM as a judge + rubric
```

---

## 2) Iteration loop

```text
fail -> fix -> rerun
```

---

## 重點

> 讓系統收斂

---

## 3) Automation

把整個 flow：

- script 化
- pipeline 化

---

## 完整流程

```text
Spec -> Plan -> Tasks -> Implement
                         |
               Test -> Eval -> Loop
```

---

## 對比一下

---

## Spec Kit

```text
pipeline
```

---

## 完整系統

```text
pipeline + feedback loop
```

---

## 三個 Insight

---

## Insight 1

> Spec 解決清楚

---

## Insight 2

> Eval 解決品質

---

## Insight 3

> Loop 解決收斂

---

## 最後 Takeaways

- LLM coding 不是 prompt 而已
- Spec 是基礎
- 但不夠
- 必須加 eval + loop

---

## 最後一句

> Spec Kit 告訴你做什麼
> Feedback loop 告訴你做得對不對

---

## 延伸到 SOP / Runbook

- 把 SOP 與 Runbook 規格化
- 讓 AI 在邊界內執行
- 用 eval + loop 保證交付品質
- 讓自動化可以規模化擴張

---

## References

- https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
- https://github.com/github/spec-kit/blob/main/spec-driven.md

---

## Q&A
