# 2026-07-01 Talk Transcript: LLM O11y 從 Observability 到 Decision System

## Slide 1
今天這 30 分鐘我想先講清楚一件事：很多團隊已經有 Langfuse、tracing、logging，但真正缺的不是可觀測性本身，而是把這些觀測轉成決策的方法。這場分享會從「看見系統」走到「讓人可以做判斷」。

## Slide 2
先講痛點：AI 工具很多，模型也很多，framework 更是每天都在變，但團隊很常缺的是數據化決策，而不是更多直覺。最後就變成選型靠感覺、升級靠印象、上 production 靠運氣。

## Slide 3
今天的大綱很簡單，先講痛點，再講解法，接著把「效率」定義清楚，然後一步一步收斂變因，最後看 Langfuse 能收集什麼，怎麼從 baseline 走到 human decision。

## Slide 4
如果目標是 Coding Agent 效能更好，那我們其實很直接，就是希望產出更穩定、成本更可控、升級風險更小。這些需求聽起來很抽象，但都可以被拆成可觀測、可比較的指標。

## Slide 5
解法的第一步不是先優化，而是先落實 o11y，把所有行為都觀測起來。至少要看得到 prompt、response、tool call、latency、token、cost 和 execution path，先把系統看清楚，才有可能談改善。

## Slide 6
這裡我想先定義效率，不然大家會一直在講不同的東西。我會先用一個簡化的公式來看：有用的 output，除以時間、成本、iteration，才是我們要的效率；如果這三個變數沒定義，效率就只是主觀感覺。

## Slide 7
但問題是變因太多，model 版本、instruction、tools、workload、context 長度、evaluation 方法，每一個都可能影響結果。只要沒有先收斂變因，你就很難知道是改善了，還是其實惡化了。

## Slide 8
所以先做 baseline，是 Action 0。先收 tracing，先把日常工作看清楚，先把 workload baseline 建起來，讓後面每個改動都有參考點，不然所有比較都會飄在空中。

## Slide 9
以 Langfuse 來說，至少可以收 trace、span、metadata、metrics、latency、token 和 cost。這些資訊不是終點，但它們是最基本的材料；沒有這些資料，你連 baseline 都很難做完整。

## Slide 10
Action 1 是最便宜也最常見的優化：先精簡 Agent。減少 tools usage、精簡 instruction、降低多餘步驟，通常就能先看到效果，因為很多問題其實不是模型不夠強，而是流程太吵。

## Slide 11
Action 2 是用 llm-as-a-judge 做快速 evaluation。這一層不是要取代人，而是先做大量樣本的初篩和 baseline 比較，讓你可以快速知道哪個方向值得繼續看。

## Slide 12
但這裡會遇到一個 issue，就是 multi-turn agent 很難直接評估。因為結果通常不是單一回答造成的，而是多個 tool call、上下文和中間狀態一起作用，所以只看最後輸出，很容易漏掉真正的問題。

## Slide 13
Action 3 的做法，就是把 evaluation 切小，用 llm-as-a-judge 先評估觀測到的單一步驟，例如一次 tool call、一段 instruction、或一個中間輸出。先把局部品質穩住，再回頭看整體 workflow。

## Slide 14
接著是 Dataset。最有價值的資料不是 benchmark，而是 daily work tracing 裡面真實累積下來的 input / output。這些資料最能反映真實使用情境，也最能幫你抓到平常看不到的失敗模式。

## Slide 15
Action 4 就是用 dataset 做 experiment。把同一份 workload data 拿來跑不同變因，例如 model 5.4 換 5.5，或者 tools、instruction 前後對照，這樣你才知道改動到底是改善還是惡化。

## Slide 16
但最後還是要回到 Human Decision。o11y 的價值是幫人看清楚現象、比較差異、縮小不確定性，不是把責任丟給模型。真正能負責、能承擔風險、能做決策的，還是人。

## Slide 17
所以整個流程要變成：先觀測，再收斂變因，再做 evaluation，再跑 experiment，最後由人決策與負責。這樣 AI 系統才不會只是一直累積感覺，而是開始累積證據。

## Slide 18
我的核心結論很簡單：沒有 evaluation，LLM upgrade 就是 gambling。你不可能只靠印象去判斷模型、工具鏈或 instruction 改動，最後一定要回到可比較的數據。

## Slide 19
LLM O11y 的本質，不是 logging tool，而是一個 AI 系統的 feedback control system。它的角色是讓你看見、比較、收斂，然後把不確定性降到可以做決策的程度。

## Slide 20
最後收一下：如果你們已經有 Langfuse 或 tracing，但還缺決策流程，下一步就是把 baseline、judge、dataset 和 experiment 接起來。這些事做完之後，才真的有機會把 AI 協作變成可持續的工程流程。
