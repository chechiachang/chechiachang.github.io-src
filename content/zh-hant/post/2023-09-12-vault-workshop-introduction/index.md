---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Vault Workshop 01: Introduction"
subtitle: ""
summary: ""
authors: []
date: 2023-09-12T20:35:19+08:00
lastmod: 2023-09-12T20:35:19+08:00
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: false

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects: []

tags: ["vault", "iac", "workshop", "terraform", "鐵人賽2023", "chatgpt"]
categories: ["vault"]
---

如果你希望追蹤最新的草稿，請見[鐵人賽2023](https://chechia.net/zh-hant/tag/%E9%90%B5%E4%BA%BA%E8%B3%BD2023/)

本 workshop 也接受網友的許願清單，[如果有興趣的題目可於第一篇底下留言](https://ithelp.ithome.com.tw/articles/10317378)，筆者會盡力實現，但不做任何保證

# Day 01 前言：從零開始的 Hashicorp Vault Workshop

從零開始 workshop 系列已經做了四年，內容包含 k8s, terraform, aws 等。

深深覺得要學習一個工具，還是要動手做。

所以有了 30 天手把手 workshop 系列文，讓有興趣接觸的朋友，能以相對低的門檻入門。

關於內容

- 無基礎的手把手的基礎教學
- 完整的範例，提供原始程式碼，也提供 production 的經驗與範例
- 官方最新文件繁中翻譯 (chatGPT based)

建議讀者務必跟著操作，不要只是看過

其他文章 [https://chechia.net/](https://chechia.net/)

過去的 Workshop 

- [2022 鐵人賽: Terraform IaC Best Practice on AWS Cloud / 在 aws 公有雲上找 IaC 最佳實踐 (因故退賽)](https://chechia.net/zh-hant/tag/%E9%90%B5%E4%BA%BA%E8%B3%BD2022/)
- [2021 鐵人賽: Terraform Workshop - Infrastructure as Code for Public Cloud](https://ithelp.ithome.com.tw/users/20120327/ironman/4057)
- [2020 鐵人賽: Kubernetes X DevOps X 從零開始導入工具 X 需求分析](https://chechia.net/zh-hant/tag/%E9%90%B5%E4%BA%BA%E8%B3%BD2020/)
- [2019 鐵人賽: Kubernetes](https://chechia.net/zh-hant/tag/%E9%90%B5%E4%BA%BA%E8%B3%BD2019/)

# 預定內容與許願清單

本 workshop 預計有底下內容
- Day 01 前言：從零開始的 Hashicorp Vault Workshop
- Day 02 準備：執行一個本地開發用途的 Vault
- Day 03：細探 Secret Engine 秘密引擎
- Day 04：Secret Engine KV V2
- Day 05：Authentication
- Day 06: Github auth method
- Day 07: Policy

本 workshop 也接受網友的許願清單，[如果有興趣的題目可於第一篇底下留言](https://ithelp.ithome.com.tw/articles/10317378)，筆者會盡力實現，但不做任何保證
- Dynamic Secrets
- tls certificate management
- Infrastructure as Code for Vault
  - deploy
  - policy
  - auth method
- Vault Kuberntes integration
- Azure integration
- AWS integration
- [token in detail](https://developer.hashicorp.com/vault/docs/concepts/tokens#root-tokens)

### 關於翻譯工具 chatGPT

本系列文章大量使用 chatGPT 翻譯官方文章。目的是使用最新版官方文件內容，提供第一手且精準的資料給讀者，但又能降低非母語讀者得學習門檻。

有翻譯的段落都會標示出處，著作權皆屬於原出處所有。

本系列文章以分享資訊，貢獻社群，提高國內整體技術能力為目的，並不用於商業用途。

使用翻譯工具並不代表作者（譯者）沒有付出相當時間心力，包含規劃文章大綱，測試 prompt engineering，調整參數，並人工校正產生的內容。

本系列作品在於教導讀者使用工具 Hashicorp Vault，而 chatGPT 等大語言模型工具就是近年最值得學習的工具。如果讀者還不會使用 chatGPT，本系列文章都附上 Prompt 提示詞，可以參考，學習，並自由使用。也許學會使用 chatGPT 所帶來的價值，會比學習 Vault 帶來的還多。

很重要所以再說一遍，chatGPT 是近年最值得學習的工具，沒有之一。

- https://github.com/f/awesome-chatgpt-prompts/blob/main/prompts.csv

# What is Vault?

本段內容使用 chatGPT-3.5 翻譯
https://developer.hashicorp.com/vault/docs/what-is-vault
內容，並由筆者人工校驗

base context
```
我希望你能充當一名繁體中文翻譯，拼寫修正者和改進者。我將用英文與程式語言與你對話，你將翻譯它，並以已糾正且改進的版本回答，以繁體中文表達。我希望你能用更美麗和優雅、高級的繁體中文詞語和句子替換我簡化的詞語和句子。保持意義不變。我只希望你回答糾正和改進，不要寫解釋。不要使用敬語，請用你取代您。
```

result correction
```
部分英文內容為專有名詞，產生的繁體中文翻譯結果中，這些名詞維持英文，不需要翻譯成中文：key，certificate，token，policy，policy rule，path，path-based，key rolling，audit，audit trail，plain text，key value，Consul，S3 bucket，Leasing，Renewal，binary

修正下列翻譯：秘密改為私鑰，數據改為資料，數據庫改為資料庫，數據改為資料，訪問改為存取，源代碼改為原始碼。
```

### What is Vault?

HashiCorp Vault 是一套基於身份的私鑰和加密管理系統。所謂的"私鑰"，是你希望嚴格控制存取的資訊，例如 API key、密碼和certificate。Vault 提供加密服務，並透過認證和授權方法進行管控。使用 Vault 的使用者介面、命令列介面或 HTTP API，可以安全地儲存和管理私鑰及其他敏感資料，並能嚴格控制（限制）其存取權，並可進行 audit。

現代系統需要存取大量的私鑰，包括資料庫憑證、外部服務的 API key、面向服務的架構通訊憑證等。了解誰正在存取哪些私鑰可能相當困難，尤其當這種存取可能因平台而異。而在此基礎上加入key rolling、安全儲存和詳細的audit trail，若無自訂的解決方案幾乎是不可能的。這正是 Vault 發揮作用的地方。

Vault 會驗證並授權客戶端（用戶、機器、應用程序）在提供他們存取秘密或儲存的敏感資料之前。

### Vault 如何運作：

Vault 主要使用 token，且 token 與客戶端的 policy 相關聯。每一 policy 都是基於 path-based 的，policy rule 限制每個客戶端對於每一 path 的行動和存取能力。使用 Vault，你可以手動建立 token 並指派給你的客戶端，或客戶端可以登入並獲得 token。下面的插圖顯示了 Vault 的核心工作流程。

![](https://developer.hashicorp.com/_next/image?url=https%3A%2F%2Fcontent.hashicorp.com%2Fapi%2Fassets%3Fproduct%3Dvault%26version%3Drefs%252Fheads%252Frelease%252F1.14.x%26asset%3Dwebsite%252Fpublic%252Fimg%252Fhow-vault-works.png%26width%3D2077%26height%3D1343&w=3840&q=75)

### Vault 工作流程

Vault 的核心工作流程包含四個階段：

認證：在 Vault 中的認證是指客戶端提供資訊，Vault 使用此資訊來判定他們是否是他們所聲稱的那個人。一旦客戶端根據某種認證方式成功認證，將生成一個與策略相關聯的 token。

驗證：Vault 根據第三方受信賴的來源，例如 Github、LDAP、AppRole 等，對客戶端進行驗證。

授權：客戶端根據 Vault 安全策略進行匹配。此策略是一套規則集，定義客戶端使用其 Vault token 可存取哪些 API 端點。策略提供了一種宣告方式來授予或禁止存取 Vault 中的特定路徑和操作。

存取：根據與客戶端身份相關聯的策略，Vault 通過發出 token 來授予存取秘密、金鑰和加密能力的權限。然後，客戶端可以使用他們的 Vault token 進行未來的操作。

![](https://developer.hashicorp.com/_next/image?url=https%3A%2F%2Fcontent.hashicorp.com%2Fapi%2Fassets%3Fproduct%3Dvault%26version%3Drefs%252Fheads%252Frelease%252F1.14.x%26asset%3Dwebsite%252Fpublic%252Fimg%252Fvault-workflow-diagram1.png%26width%3D8300%26height%3D9000&w=3840&q=75)

### 為什麼選擇 Vault？

現今的大多數企業都有憑證散布在其組織中。密碼、API 金鑰和憑證存儲在明文中、應用源代碼、配置文件和其他位置。由於這些憑證存在於各處，因此可能很難真正知道誰有存取和授權權限。明文中的憑證也增加了內部和外部攻擊者進行惡意攻擊的可能性。

考慮到這些挑戰，Vault 被設計出來。Vault 採取所有這些憑證並集中管理，這樣他們就只在一個位置定義，從而減少了憑證的不必要暴露。但 Vault 更進一步，確保用戶、應用程序和系統都被認證並明確授權存取資源，同時也提供一個審計跟踪，捕捉並保留客戶端操作的歷史記錄。

### Vault 的主要功能包括

安全的秘密存儲：可以在 Vault 中存儲任意的金鑰/值秘密。Vault 在將這些秘密寫入持久性存儲之前會對其進行加密，因此獲取原始存儲並不足以存取你的秘密。Vault 可以寫入磁盤、Consul 等。

動態秘密：Vault 可以為某些系統即時生成秘密，例如 AWS 或 SQL 數據庫。例如，當應用程序需要存取 S3 桶時，它會要求 Vault 提供憑證，Vault 將即時生成具有有效權限的 AWS 密鑰對。在創建這些動態秘密後，Vault 也會在租期到期後自動撤銷它們。

數據加密：Vault 可以在不存儲數據的情況下加密和解密數據。這允許安全團隊定義加密參數，並允許開發人員將加密數據存儲在如 SQL 數據庫之類的地方，而不必設計他們自己的加密方法。

租賃和續期：Vault 中的所有秘密都有一個與之相關的租期。在租期結束時，Vault 會自動撤銷該秘密。客戶端可以通過內置的續期 API 來續租。

撤銷：Vault 具有內置的秘密撤銷支援。Vault 不僅可以撤銷單一的秘密，還可以撤銷秘密樹，例如由特定用戶讀取的所有秘密，或特定類型的所有秘密。撤銷在金鑰滾動以及在入侵情況下鎖定系統時都很有幫助。

### 什麼是 HCP Vault？

HashiCorp Cloud Platform (HCP) Vault 是 Vault 的託管版本，由 HashiCorp 運營，使組織能夠快速啟動並運行。HCP Vault 使用與自託管的 Vault 相同的二進制文件，這意味著你將擁有一致的用戶體驗。你可以使用相同的 Vault 客戶端與 HCP Vault 通信，就像你使用自託管的 Vault 一樣。請參考 HCP Vault 文檔以獲得更多資訊。

