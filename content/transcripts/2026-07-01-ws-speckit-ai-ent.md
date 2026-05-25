# 2026-07-01 Workshop Transcript: Spec-kit AI Enterprise

## Slide 1
各位早安，歡迎來到今天 90 分鐘的 Spec-kit 工作坊，先從行前準備開始：請確認你有筆電、網路、VS Code、Spec-kit CLI，以及 workshop 的範例程式碼，模型部分今天會提供 Azure OpenAI Key，也可以用你自己習慣的模型；這堂課最重要的是動手做與保持懷疑，遇到標記了問號的地方，先想再問，目標是練習怎麼判斷 AI 回答是否可靠。

## Slide 2
這一頁我帶大家完成 VS Code 起手式：先安裝或打開 VS Code，開底下 Terminal，把 `speckit-playground` clone 下來，再用 File > Open Folder 開啟該目錄，等一下所有操作都會在這個 workspace 裡進行。

## Slide 3
這張畫面就是 `git clone` 的示意，我想強調的是大家先不要急著跑指令以外的步驟，先確認你已經成功 clone、資料夾也真的在 VS Code 裡打開，這會讓後面指令跟代理流程順很多。

## Slide 4
接著安裝 Spec-kit CLI：先在終端機確認 `uv --version`，如果沒有就先安裝 uv，之後用指定版本安裝 `specify-cli`，我建議 workshop 先固定版本，避免每個人看到的行為不同而增加排錯成本。

## Slide 5
這張圖是安裝 Spec-kit CLI 成功後的畫面，請對照一下你的終端輸出，確認沒有權限或 PATH 問題，因為後面 `/speckit.*` 流程會直接依賴這一步。

## Slide 6
接著做 API Key 設定：在 VS Code 右側 Chat 面板選 model，再進入 Manage Model Settings，新增 Azure OpenAI，先把 Group Name、API Key 填好，這一步會打開 `chatLanguageModels.json` 讓你編輯模型設定。

## Slide 7
這張截圖示範從 model 清單進入管理頁面的路徑，請大家跟著點一次，確保你找得到設定入口，因為不同 extension 版本 UI 位置可能略有差異。

## Slide 8
這一頁是 `chatLanguageModels.json` 畫面，等等我們會把 id、name、url 補完整，重點是先理解模型宣告檔是你與 IDE 模型能力的契約，工具呼叫與 token 上限都在這裡定義。

## Slide 9
回到設定重點：填好模型 `id`、顯示名稱與 endpoint URL，存檔後回到 model 清單選 Azure GPT-5.4 Nano，跟模型打聲招呼驗證連線；也請注意 `maxInputTokens` 與 `maxOutputTokens` 會直接影響成本、可處理任務大小與回應品質。

## Slide 10
這張圖示範 Azure OpenAI 設定填寫位置，我建議你對照欄位名稱逐一檢查，尤其 endpoint 與 api-version 最容易手誤。

## Slide 11
這張圖是回到 Chat 面板選擇 Azure GPT-5.4 Nano 的步驟，看到模型可選且可對話，就代表今天 workshop 的基礎環境已經準備完成。

## Slide 12
補充一下，如果你暫時不想用 Azure，也可以切回其他可用模型先練流程，今天核心是學會 Spec-driven workflow，不是綁死單一供應商。

## Slide 13
這頁是行前最重要的 mindset：講師不一定對、投影片也不一定對，請主動質疑並驗證；你要把 AI 當強力助手，不是權威，真正的能力是在不確定下建立可驗證流程。

## Slide 14
正式開始前先自我介紹與課程定位：今天是 AI Enterprise Summit 2026 的 90 分鐘 hands-on workshop，我會帶你從零開始用 Spec-kit 把需求轉成可執行規格，再落地到實作與驗收。

## Slide 15
這頁是講者簡介，我的背景主要在後端、DevOps、Kubernetes 與雲端實戰，所以今天內容會偏工程落地與團隊可複製流程，而不是只談提示詞技巧。

## Slide 16
先看大綱：LAB1 先實作第一個 Spec-kit 專案，再穿插講解 Spec-kit、SDD 為何常比純 Vibe Coding 穩定，接著做 LAB2 自選題，最後驗收、回顧與 Q&A。

## Slide 17
LAB1 開始前先定義目標：先把 Spec-kit 視為一個讓你和 LLM 協作產生程式碼的流程工具，我們要驗證的是在同樣時間內，流程化開發能否比即興對話更可預測、更好驗收。

## Slide 18
第一步初始化專案，在 VS Code Terminal 執行 `specify init --here --integration copilot`，如果看到非空目錄警告就確認後繼續，再跑 `specify check`，確保基礎腳手架與整合都正常。

## Slide 19
這頁補充初始化結果：你會拿到 `.specify` 資料夾與 Copilot 相關設定，包含可觸發的 prompt 模板；建議馬上打開 `.specify/templates` 看內容，並在 Chat 試一次 `/spec`，理解工具如何被掛進你的日常對話。

## Slide 20
這張圖是 `specify init` 的實際畫面，請確認你的整合模式與腳本類型有選對，特別是 Windows 使用者建議選 `ps`，避免後續腳本相容性問題。

## Slide 21
接著建立 principles，也就是專案憲法：在 Chat 輸入 `/speckit.constitution`，讓代理先生成團隊共識，例如簡潔性與測試覆蓋率，然後到 `.specify/memory/constitution.md` 審核，不滿意就迭代到滿意為止。

## Slide 22
這張圖是建立 constitution 的示意，請注意我們不是追求一次寫完，而是透過短回合快速修正文案，直到它真的能約束後續行為。

## Slide 23
我再強調一次：constitution 是 agent 每次行動都會參考的行為準則，它不是裝飾文件，品質好壞會直接反映在後面 plan、tasks 與 implement 的穩定度。

## Slide 24
下一步建立 Spec：打開範例題目或用你自己的題目，聚焦在 what 與 why，讓代理生成 `specs/001-branch-name/spec.md`；如果需求描述清楚，後續返工成本會明顯下降。

## Slide 25
這張圖示範 `/speckit.specify` 後產出的規格檔樣貌，請先看是否可驗收、是否有遺漏邊界條件，不要急著寫 code。

## Slide 26
有了 spec 後依序跑 `/speckit.plan`、`/speckit.tasks`、`/speckit.git.feature`、`/speckit.implement`，中途可用 `/clear` 或 `/compact` 做 context 管理，核心原則是讓每一步都建立在明確中間產物上。

## Slide 27
這張圖展示 plan、tasks、implement 的串接流程，你可以把它看成可追蹤的交付管線，而不是一段無限延長的聊天紀錄。

## Slide 28
實作時常見 interruption 是代理要求切 feature branch 或要求你確認命令，這是正常安全機制；先讀懂它卡住的原因，再決定 allow 或調整流程，避免盲目點擊。

## Slide 29
這張圖是 `speckit.git.feature` 的示例，我建議把分支命名和 spec 編號綁定，這樣回頭查需求、程式碼與提交紀錄會很清楚。

## Slide 30
談 auto-approve：為了速度你可以放寬部分許可，但請以最小權限為原則，只允許 workspace、只開必要讀寫命令，並限制高風險參數，避免省了幾分鐘卻放大安全與成本風險。

## Slide 31
這張設定畫面提醒大家，按下「Allow all commands」前請先想損害半徑；比較好的做法是只放行你可預期的命令集合，持續觀察代理行為再逐步調整。

## Slide 32
當 tasks 都完成後就進入驗收，今天 LAB1 先手動驗收：確認可執行、無錯誤、功能符合 spec；實務上會把測試覆蓋率、lint、style 也寫入規格，讓代理自動產生驗收機制。

## Slide 33
這張圖是手動測試畫面，請邊測邊對照 spec，記錄 mismatch，因為這些 mismatch 會是你下一輪澄清需求或補測試案例的依據。

## Slide 34
遇到錯誤時先分類：如果是規格問題就回 `/speckit.specify` 改 spec；如果是實作問題就提供錯誤訊息與可重現驗證方式，讓代理可以自行修復並回報結果。

## Slide 35
這張圖對應錯誤處理流程，重點是讓問題可重現、可驗證，避免「看起來好了」但下一次又壞掉。

## Slide 36
實作階段可能需要一些時間，你可以先讓代理跑任務，再回來做驗收；我會用這段時間講觀念，幫大家把剛剛手上的動作連回方法論與使用情境。

## Slide 37
接下來進觀念段：Spec-kit 是一套 Spec-driven Development toolkit，把腳本、模板、檢查點與流程標準化，讓代理能按 `spec -> plan -> tasks -> implement` 可預測地前進，而不是自由發揮到失焦。

## Slide 38
核心流程非常簡單，但關鍵在紀律：先有 spec 再動手，任何需求變更先改 spec，不先改 code，這樣才能降低 drift 與返工。

## Slide 39
為什麼有幫助？因為它能對抗 context rot 與 spec drift；長對話會讓模型逐步偏離需求，Spec 則提供穩定錨點，讓每輪執行都能回到同一份 source of truth。

## Slide 40
再談 context management：模型 context window 有上限，對話越長越容易退化，compact 又可能遺失關鍵資訊，所以要把流程切段、資料外部化到 spec 與中間檔，而不是把一切塞在聊天記憶裡。

## Slide 41
另外一個好處是平行分工：有了 Spec、Plan、Tasks，中途就能 review、能拆工、能多人協作，最後交付不只有 code，還有可追溯的決策與需求脈絡。

## Slide 42
你可能會問「Code 不就是最精準規格嗎？」在 AI 生成速度極快的時代，單靠 code 已不足以承載商務意圖與驗收標準，Spec 反而成為競爭力與協作契約。

## Slide 43
那可不可以從 code 逆向出 spec？理論上可做部分摘要，但實務上常受限於 token、檔案規模與讀取失真，品質不穩定，所以最好的策略仍是前置維護 spec，而不是事後補文件。

## Slide 44
所以總結這段：Chat 是互動介面，SDD 是方法，Spec-kit 是把方法產品化成可重複執行工作流的工具；三者角色不同，混在一起就容易誤判。

## Slide 45
接著談模型選型，這頁價格表要傳達的是成本結構：Spec-kit 流程會有額外 token 稅，所以在同品質可接受前提下，多數步驟使用 mini 或 nano 往往更划算。

## Slide 46
更具體說，nano 或 mini 通常已足夠處理 specify/plan/tasks 等核心流程，若任務進入超長上下文或高複雜多模態，再考慮升級模型，並把高階模型用在最關鍵環節。

## Slide 47
我們也整理了常見失敗模式：還沒寫 spec 就 implement、規格更新但 tasks 未同步、規格過於模糊、驗收延後到最後；這四件事幾乎都會造成大量返工。

## Slide 48
回顧 LAB 的核心：你不是在練提示詞花招，而是在練如何讓 agent 可預測，spec 是唯一真相，checklist 是品質底線，這兩件事決定結果穩不穩。

## Slide 49
今天請帶走三件事：第一，`spec -> plan -> tasks -> implement` 是可落地流程；第二，規格優先可以降返工；第三，要讓 agent 穩定必須建立 spec 與驗收標準的閉環。

## Slide 50
接著回到實作，大家可以繼續做自己的題目；卡住很正常，先問 agent 為什麼卡住，再看論文與概念文件補觀念，讓你能分辨是流程問題、規格問題還是模型問題。

## Slide 51
如果時間只剩最後五分鐘，我建議最小可行流程就是：`specify -> clarify -> plan -> analyze -> tasks -> git.feature -> implement`，至少把一輪完整閉環跑完。

## Slide 52
最後談可以再做好的地方：更早引入 test suite、lint、pre-commit 與 diff review，再加上模型行為觀測（o11y），你就能從「會用」升級到「能穩定營運」。

## Slide 53
這頁是參考資源，包含 Spec-kit、Spec-driven 文件、workshop playground 與 session 連結，建議課後至少重跑一次流程，把今天的實作整理成你自己的 SOP。

## Slide 54
今天的分享到這裡，謝謝大家投入完成這輪 hands-on，歡迎會後交流你的題目與卡點；只要你持續練習規格先行與可驗收迭代，AI 協作開發的穩定性會很快拉起來，我們下次見。
