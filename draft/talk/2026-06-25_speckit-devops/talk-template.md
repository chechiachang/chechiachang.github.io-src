# Talk Template

## Talk Info

- Title: DevOpsDay: 規格驅動的 AI 強化 DevOps
- Audience: DevOps / SRE / Platform Engineers, Tech Leads
- Duration (minutes): 35
- Paper/Source: content/posts/2026-06-25-speckit-devops/index.md
- Date: 2026-06-25

## Core Message

- Aha sentence (1 line): 在 DevOps 任務中，先把規格寫清楚，比先下 prompt 更能穩定交付。
- Gimmick/hook (1 line): 把 Runbook 從「文件」變成「可執行規格」。
- Why this is memorable (1 line): 多數團隊不是缺模型，而是缺可驗證流程。
- One-line close people can repeat to a friend: Vibe 是聊天，Spec 是工程；先定義規格再讓 AI 產出才可控可驗證。

## Talk vs Paper

- What to keep from paper (must support the aha): SDD 定義、Spec-kit 流程、適合/不適合情境、導入風險邊界。
- What to skip (non-essential details): Spec-kit 全部內部實作細節、泛用 AI 歷史背景、與主軸無關的工具比較。
- What to add from outside the paper (background/related): DevOps 現場痛點、SOP/Runbook 範例、YouBike demo 流程、analyze/checklist 驗收視角。
- Different angle used in the talk: 從平台工程「可操作與可驗收」角度切入，不從純開發流程切入。

## Spoken Plan

- Claim 1: DevOps 任務先規格化，AI 產出才穩定。
- Example for claim 1: Incident Runbook 規格化後，值班同仁可用一致流程執行與驗收。
- Intuition for claim 1: 先定義 Done 長相，AI 才知道怎樣算做完。
- Claim 2: 流程化比 prompt 技巧更能降低返工。
- Example for claim 2: `/speckit.specify -> /speckit.plan -> /speckit.tasks -> /speckit.implement`，需求改動時只回 spec 重跑。
- Intuition for claim 2: 把變更集中在 spec，能避免分散到 code 和口頭說明。
- Claim 3: analyze/checklist 是交付品質保險絲。
- Example for claim 3: demo 後用 `/speckit.analyze` 看落差、用 `/speckit.checklist` 做可交付檢查。
- Intuition for claim 3: 沒有驗收迴路，快只是更快出錯。
- Spoken transition 1 ("You might think A, but B..."): 你可能以為 AI 先上就會加速，但真正決定穩定性的其實是規格品質。
- Spoken transition 2: 我們先不談大改造，先看每一項日常任務怎麼跑通。
- Spoken transition 3: 有了成功案例後，再談哪些情境該擴大、哪些該先停。

## Audience Engagement

- Audience participation moment (guess/vote/call-on): 請現場舉手：你們有多少 Runbook 是半年內沒演練過？
- Question asked before answer: 為什麼同一份 SOP，A 組很順、B 組一直出錯？
- Reveal method on slide: 先展示「文件版 SOP」與「規格版 SOP」對照，再給流程圖和 checkpoint。
- Backup interaction (if audience quiet): 請大家用 1-5 分自評目前 Runbook 可重現度，接著對照導入前置條件。

## Rehearsal Notes

- What I actually said that worked:
  - 「不是缺模型，是缺可驗證流程」通常能立刻抓到注意力。
  - 「需求改了先回 spec」用真實案例講最有說服力。
- Written phrasing that sounded unnatural:
  - 「秒殺」改成「成功率更高/返工更少」。
  - 避免過長句；每句盡量 15 秒內講完。
- Timing result (target vs actual): Target 35 min / Actual __ min
- Final fixes before delivery:
  - Demo 區段最多 8 分鐘，超時就切換成截圖版流程。
  - 每段只保留一個關鍵句，避免資訊過載。
