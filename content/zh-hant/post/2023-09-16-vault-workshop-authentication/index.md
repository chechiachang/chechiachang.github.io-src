---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Vault Workshop 05: Authentication"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2023-09-14T01:42:26+08:00
lastmod: 2023-09-14T01:42:26+08:00
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

整篇 Workshop 會使用的範例與原始碼，放在 [Github Repository: vault-playground](http://chechia.net/zh-hant/#projects)

# Day 06：Authentication

在前面的文章中，你已經創建了第一個秘密，了解了秘密引擎，並在以開發模式啟動的 Vault 服務器中探索了動態秘密。

接下來的內容中，我們將深入研究使用 Vault token 和 GitHub 憑證進行身份驗證。

### Token 身份驗證

Token 身份驗證已自動啟用。當你啟動開發模式服務器時，輸出顯示了 Root token。Vault CLI 從 `$VAULT_TOKEN` 環境變數中讀取 Root token。這個根 token 可以在 Vault 內執行任何操作，因為它被分配了 Root policy 權限。允許的權限中包含創建新的 token。

現在，讓我們創建一個新的 token。

啟動全新的 dev Vault Server

```bash
vault server -dev
```

output，server log 回傳 dev 模式的警告

```
WARNING! dev mode is enabled! In this mode, Vault runs entirely in-memory
and starts unsealed with a single unseal key. The root token is already
authenticated to the CLI, so you can immediately begin using Vault.

# 警告！已啟用開發模式！在此模式下，Vault完全運行在內存中，使用單個unseal key解封。
# root token已被CLI驗證，因此你可以立即開始使用Vault。

You may need to set the following environment variables:

    $ export VAULT_ADDR='http://127.0.0.1:8200'

# 以下顯示了unseal key 和 root token，以防你想要封存/解封Vault，或重新進行身份驗證。

    The unseal key and root token are displayed below in case you want to
    seal/unseal the Vault or re-authenticate.

# dev 模式預設配置的 unseal key 與 root token
    Unseal Key: QDUAuY7Kltsc/3bVwUYF39u8aEFgWNRs/1D5yxFtim4=
    Root Token: hvs.J30e53uuKDhrWVttCvK0DJaN

# 開發模式絕不應在生產安裝中使用！
    Development mode should NOT be used in production installations!
```

依據提示 export 需要的變數

```
export VAULT_ADDR='http://127.0.0.1:8200'
```

在 dev mode 下，未使用 token 也可以存取 Vault Server 中的資料，這是因為 vault server 在啟用時，預設使用 token helper，將 root token 寫入到 local filesystem

[Vault token helper 說明](https://developer.hashicorp.com/vault/docs/commands/token-helper)

你可以使用以下指令，檢查儲存於本地的 vault token

```bash
cat ~/.vault-token
```

output

```bash
hvs.J30e53uuKDhrWVttCvK0DJaN%
```

vault CLI 自動取用本地儲存的 root token，所以已經自動完成 authentication，不用額外進行 authentication，也可以使用 Vault

使用 Vault 時，須額外注意本地儲存的 token

### 避免 dev 模式下儲存 root token

Vault dev server 自動寫入 root token，讓開發 Vault 功能時十分便利。然而在資訊安全的領域，便利往往代表著風險。在非 dev Server 環境中，我們會嚴格控制所有 token 的曝險程度，特別是 root token，根本不該被 print 出，當然也萬萬不能儲存在本地電腦。

依據你的開發需求，你可能不希望 dev 模式下，long-live 永久有效的 root token 儲存在本地電腦中，你可以使用 -dev-no-store-token flag 來避免 Vault dev server 暴露 root token。

```bash
vault server -dev -dev-no-store-token
```

output

```bash
WARNING! dev mode is enabled! In this mode, Vault runs entirely in-memory
and starts unsealed with a single unseal key. The root token is already
authenticated to the CLI, so you can immediately begin using Vault.

You may need to set the following environment variables:

    $ export VAULT_ADDR='http://127.0.0.1:8200'

The unseal key and root token are displayed below in case you want to
seal/unseal the Vault or re-authenticate.

Unseal Key: hNi8T3YctTZrLYlKezLAJttfiF97D1Vy7Tq+HMM3y9w=
Root Token: hvs.qCqY9ZO3oNS6VrrKMHp89KYv

Development mode should NOT be used in production installations!
```

你可以檢查本地使否有儲存的的 vault token

```bash
cat ~/.vault-token
```

output

```bash
cat: /Users/che-chia/.vault-token: No such file or directory
```

然後試圖在沒有 .vault-token 的狀態下，存取 Vault Server

```bash
vault secrets list
```

output，沒有合法的 access token，Vault server 回傳 403 權限被拒

```bash
vault secrets list
Error listing secrets engines: Error making API request.

URL: GET http://127.0.0.1:8200/v1/sys/mounts
Code: 403. Errors:

* permission denied
```

### Authentication

你可以使用 vault dev Server log 中回傳的 root token 來存取 Vault server

你可以將 token 在寫回 .vault-token，這是最方便，也最危險

建議：永遠不要儲存 root token 在本地電腦上。非常容易遺忘自己本地有儲存 root token。

```bash
echo hvs.qCqY9ZO3oNS6VrrKMHp89KYv > ~/.vault-token
```

另一個方式是使用環境變數 `VAULT_TOKEN`

```bash
VAULT_TOKEN=hvs.qCqY9ZO3oNS6VrrKMHp89KYv vault secrets list
```

上面是在 CLI 前面插入環境變數，下面是 export `VAULT_TOKEN` 到當前 session 的環境變數

```bash
export VAULT_TOKEN=hvs.qCqY9ZO3oNS6VrrKMHp89KYv
vault secrets list
```

output

```bash
Path          Type         Accessor              Description
----          ----         --------              -----------
cubbyhole/    cubbyhole    cubbyhole_9cc57bcf    per-token private secret storage
identity/     identity     identity_41faabef     identity store
secret/       kv           kv_fca914b5           key/value secret storage
sys/          system       system_5dd83198       system endpoints used for control, policy and debugging
```

你可以檢查目前環境變數中，與 Vault 有關的 env

```bash
env | grep VAULT
```

output

```bash
VAULT_ADDR=http://127.0.0.1:8200
VAULT_TOKEN=hvs.qCqY9ZO3oNS6VrrKMHp89KYv
```

當然，`VAULT_TOKEN` 的存在時間越久，token 曝險的機率就越高。

也很容易忘記 `VAULT_TOKEN` 有存在的環境變數。

### VAULT TOKEN 雷點

workshop 至今，你目前只有一台 vault dev server，而且裡面並沒有任何的機密資料，這個 vault server 可以隨時拋棄。

然而，在實務上，Vault 管理員手上可能會有多個 Vault server 需要管理。

想像你有 dev / stag / prod 的 server，某一天你正在 dev 開發一個新功能，由於本地有 `VAULT_TOKEN` 與 `VAULT_ADDR`，你不疑有他的在這台 server 上運行許多測試的指令，包含新增一對測試 secret，刪刪改改現有的 secret。

然後你的本能忽然覺得怪怪的，我沒有設置任何 vault env，為何可以直接存取 dev server？

你拉出 env 看，發現是 production server 的 addr + token，上次進入 production server 時的 session，還存有有效的 addr 與 token

```bash
VAULT_ADDR=http://vault.prod.chechia.net
VAULT_TOKEN=this-is-prod-token
```

你麻煩大了

心得：永遠不要儲存長效期的 token 在本地。本 workshop 會不斷地強調，提醒各種操作中的資安風險，請各位學習過程中就養成良好習慣，以免方便一時，遺憾終身。

### root token

https://developer.hashicorp.com/vault/docs/concepts/tokens#root-tokens

root token是附帶root policy的token。root token可以在Vault中執行任何操作。任何操作。

此外，它們是Vault中唯一可以設置為永不過期，且無需進行任何續訂的 token 類型。由於 root token 權限如此大，Vault 設計上刻意讓創建root token 很困難；實際上只有三種方法可以創建root token：

1. 在 vault operator init 時生成的初始root token - 此token不會過期

2. 使用另一個root token 創建 root token。這點有個限制：使用有限期的root token，無法創建永不過期的root token

3. 在擁有 unseal keys quorum的權限下，使用 vault operator generate-root 來創建root token

root token在開發中很有用，但在 production 環境中應該非常謹慎使用。

事實上，Vault團隊建議 root token 只能進行必要的初始設置，通常是設置身份驗證方法(auth method)，和必要的 policy，以允許管理員獲取更有限的token。或是緊急情況下使用root token，並在不再需要時立即撤銷(revoke)。

如果需要新的root token，可以使用 operator generate-root 指令，使用相關的 API endpoint即時生成。

同時，當root token處於活動狀態時，建議團隊中提供多人一起協作，共同檢查 terminal session，養成一種良好的安全實踐。這樣多人可以驗證使用root token執行的任務，以及這些任務完成後，立即撤銷了該token。

### 使用 root token 產生 short-live token

root token 預設配置 root policy，我們可以產生權限較小的 token，並指配置最小必要權限(least privilege)

```
VAULT_TOKEN=hvs.qCqY9ZO3oNS6VrrKMHp89KYv vault token create

Key                  Value
---                  -----
token                hvs.FbAeXWmXGAeCCCV0G04kjBIp
token_accessor       rPOOSI06WGnFo9MVOvS8luhn
token_duration       ∞
token_renewable      false
token_policies       ["root"]
identity_policies    []
policies             ["root"]
```

已創建token，輸出中以key value的表格描述了此token。創建的token在此處顯示為 hvs.FbAeXWmXGAeCCCV0G04kjBIp

此token是root token的子token，並且預設情況下，它會繼承其 parent token的policy 權限。

token是核心身份驗證方法(core auth method)。你可以使用生成的token來 login Vault，只需在提示時複製並粘貼即可。

你可以使用以下指令登入 vault

```bash
vault login
```

在回傳的輸入令中輸入新產生的 child token hvs.FbAeXWmXGAeCCCV0G04kjBIp
```bash

WARNING! The VAULT_TOKEN environment variable is set! The value of this
variable will take precedence; if this is unwanted please unset VAULT_TOKEN or
update its value accordingly.

# 警告！已設置 VAULT_TOKEN 環境變數！此變數的值將優先考慮；如果不需要此設置，請取消設置 VAULT TOKEN 或相應地更新其值。
```

由於在前面的操作中，環境變數中仍帶有 `VAULT_TOKEN`，而且是更高權限的永不過期 root token，vault CLI 偵測到 VAULT TOKEN env，跳出警告。

你可以透過以下指令清除 `VAULT_TOKEN` 環境變數

```bash
unset VAULT_TOKEN
```

然後再次執行 vault login，在回傳的輸入令中輸入新產生的 child token hvs.FbAeXWmXGAeCCCV0G04kjBIp

```bash
vault login
```

output，顯示成功登入，並回傳 token 的相關訊息

```
Token (will be hidden):

Success! You are now authenticated. The token information displayed below
is already stored in the token helper. You do NOT need to run "vault login"
again. Future Vault requests will automatically use this token.

Key                  Value
---                  -----
token                hvs.FbAeXWmXGAeCCCV0G04kjBIp
token_accessor       rPOOSI06WGnFo9MVOvS8luhn
token_duration       ∞
token_renewable      false
token_policies       ["root"]
identity_policies    []
policies             ["root"]
```

此token是root token的子token，繼承其 parent token的policy 權限，也就是 root。本身是無效期限制的永久 root token。

在創建一把 token，此時由於 vault login，進入登入狀態，token 已經存在本地中

```bash
vault token create
```

output，第二隻 token 為 hvs.FDjvyRFXoVC6DF5tYvLCQVFG。每一隻 token 都是不重複的。

```
Key                  Value
---                  -----
token                hvs.FDjvyRFXoVC6DF5tYvLCQVFG
token_accessor       gLe7IrUMUq4eb2pZWVdUhbHv
token_duration       ∞
token_renewable      false
token_policies       ["root"]
identity_policies    []
policies             ["root"]
```

### revoke 撤銷 token

當我們不再需要使用 token 時，最好盡快撤銷 revoke token

目前的 token 樹狀結構

初始 root token (啟動 dev Server 時預設產生的)
  - child: hvs.FbAeXWmXGAeCCCV0G04kjBIp
    - grandchild: hvs.FDjvyRFXoVC6DF5tYvLCQVFG

你可以使用指令，撤銷第一把產生的 token (child)

```bash
vault token revoke hvs.FbAeXWmXGAeCCCV0G04kjBIp
```

CLI output，顯示 token 已經撤銷

```bash
Success! Revoked token (if it existed)
```

同時，vault server log 紀錄 revoked lease

```bash
2023-09-16T21:29:21.464+0800 [INFO]  expiration: revoked lease: lease_id=auth/token/create/hf153f5e80ed722f6816f592032a43906a5606a889bab4c13ff3368c9a1b95b69
```

還記得我們是使用地一把產生的 token (child) login 的嗎？目前的登入當然也隨著 token 失效，嘗試存取回傳 403 權限被拒

```
vault secrets list

Error listing secrets engines: Error making API request.

URL: GET http://127.0.0.1:8200/v1/sys/mounts
Code: 403. Errors:

* permission denied
```

嘗試重新 login，使用地一把產生的 token (child) 一樣被拒

```bash
vault login
```

output

```
Token (will be hidden):
Error authenticating: error looking up token: Error making API request.

URL: GET http://127.0.0.1:8200/v1/auth/token/lookup-self
Code: 403. Errors:

* permission denied
```

撤銷token 時，也會一併撤銷使用這把 token 產生的子 token (grandchild)

嘗試重新 login，使用第二把產生的 token (grandchild) 一樣被拒

```bash
vault login
```

output

```
Token (will be hidden):
Error authenticating: error looking up token: Error making API request.

URL: GET http://127.0.0.1:8200/v1/auth/token/lookup-self
Code: 403. Errors:

* permission denied
```

### 為何總是要使用 root token

上面講了 vault 核心的 token auth method，相信讀者一定有一個奇怪的感覺

- 最開始 login 需要 token
- 產生 token 在去產生新的 token

這樣產生 token 的 admin 不就需要將 token 先傳給使用者，使用者才能登入嗎？這樣傳遞 token 的行為，不是反而增加更大的曝險。

這樣真的有比一般使用 username password 登入的方法更安全嗎？

上面的想法都是有道理的，也就是說，光使用 token auth methods 是無法滿足我們的安全需求。這些安全需求，需要使用其他 auth method 方法來解決，而 vault 強大之處便是支援的許多 auth method，將 vault 的安全建立在其他更穩定的服務上，例如 github / aws / azure / gcp / kubernetes 等。

下一篇，我們就來實作 github auth method。

### chatGPT

本段部分內容使用 chatGPT-3.5 翻譯
https://developer.hashicorp.com/vault/tutorials/getting-started/getting-started-authentication
內容，並由筆者人工校驗

base context
```
我希望你能充當一名繁體中文翻譯，拼寫修正者和改進者。我將用英文與程式語言與你對話，你將翻譯它，並以已糾正且改進的版本回答，以繁體中文表達。我希望你能用更美麗和優雅、高級的繁體中文詞語和句子替換我簡化的詞語和句子。保持意義不變。我只希望你回答糾正和改進，不要寫解釋。

不要使用敬語，翻譯結果中若出現"您"，請用"你"取代"您"。
```

result correction
```
部分英文內容為專有名詞，產生的繁體中文翻譯結果中，這些名詞維持英文，不需要翻譯成英文：key，value，certificate，token，policy，policy rule，path，path-based，key rolling，audit，audit trail，plain text，key value，Consul，S3 bucket，Leasing，Renewal，binary，prefix，instance，metadata。

修正下列翻譯：將 "數據" 改為 "資料"，將 "數據庫" 改為 "資料庫"，將 "數據" 改為 "資料"，將 "訪問" 改為 "存取"，將 "源代碼" 改為 "原始碼"，將 "信息" 改為 "資訊"，將 "命令" 改為 "指令"，將 "禁用" 改為 "停用"，將 "默認" 改為 "預設"。
```

