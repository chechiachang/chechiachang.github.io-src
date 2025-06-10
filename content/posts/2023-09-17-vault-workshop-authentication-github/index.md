---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Vault Workshop 06: Github Auth method"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2023-09-14T02:42:26+08:00
lastmod: 2023-09-14T02:42:26+08:00
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

# Day 06：Github auth method

### 不需要使用 root token 的 auth method: github

Vault 支援用於人員使用者的身份驗證方法。GitHub 身份驗證，使用戶可以通過提供他們的 GitHub 憑證來驗證 Vault，並收到一個 Vault token。

簡單來說，github organization [chechia-net](https://github.com/chechia-net)，可以設定適當的權限給成員 chechiachang，讓 chechiachang 可以透過 github 取得有權限的 token。

注意

在練習中所描述的這種身份驗證方法，需要你擁有 GitHub、屬於 GitHub org 中的一個 team ，並生成了具有 `read:org` scope 的 GitHub personal access token。你可以於 github 創建一個 free plan 的 org，並設定一個 team，然後透過個人 Settings / Developer Settings 來產生一把具有 `read:org` 權限的 personal access token

### 啟用 github auth method

你可以使用下列指令，在 path=github/ 下啟用 GitHub 身份驗證方法。

```bash
export VAULT_TOKEN=hvs.qCqY...9KYv
vault auth enable github
```

這個指令使用 root token 設定 auth method，也是整個 github auth methods 中，唯一需要用到 root token 設定的地方，而且只需要設定一次

output

```bash
Success! Enabled github auth method at: github/
```

vault server log 顯示 credential backend 已啟用

```bash
2023-09-16T21:40:10.444+0800 [INFO]  core: enabled credential backend: path=github/ type=github version=""
```

你可以下列指令，列出所有的 auth methods

```bash
vault auth list
```

output

```
Path       Type      Accessor                Description                Version
----       ----      --------                -----------                -------
github/    github    auth_github_9bc96e5f    n/a                        n/a
token/     token     auth_token_b7984c52     token based credentials    n/a
```

github 身份驗證方法已啟用，並位於路徑 auth/github/。

### 設定 github auth method

此身份驗證方法需要你在配置中設置 GitHub organization。GitHub organization中，維護了一個允許與 Vault 驗證的使用者列表。

設置 GitHub 身份驗證的組織。

```bash
vault write auth/github/config organization=chechia-net
```

output

```bash
Success! Data written to: auth/github/config
```

現在，chechia-net GitHub 組織中的所有使用者都可以進行身份驗證。

### 設定 github auth method，給不同 team 不同的 policy

GitHub 組織可以定義團隊(team)。每個團隊可能可以在組織維護的所有 repository 中執行不同的操作。這些團隊也可能需要訪問 Vault 內的特定密碼。

配置 GitHub sre 團隊的身份驗證，以獲得 default 和 application 兩個 policy的授權。

```bash
vault write auth/github/map/teams/sre value=default,application
```

output

```bash
Success! Data written to: auth/github/map/teams/sre
```

GitHub sre 團隊中 chechia-net 組織的成員，將使用 default 和 application policy 進行身份驗證和授權。

備註：application policy 尚未在 Vault 中定義。在該策略定義之前，Vault 仍然允許使用者進行身份驗證，但會產生警告。

你可以使用指令顯示 Vault 啟用的所有身份驗證方法

```bash
vault auth list
```

回傳顯示兩個 auth methods，github/ 與 token/

```bash
Path       Type      Accessor                Description                Version
----       ----      --------                -----------                -------
github/    github    auth_github_9bc96e5f    n/a                        n/a
token/     token     auth_token_b7984c52     token based credentials    n/a
```

### 使用 github auth method login

使用 help 指令來了解 github auth method 的說明

```bash
vault auth help github
```

output

```bash
Usage: vault login -method=github [CONFIG K=V...]

  The GitHub auth method allows users to authenticate using a GitHub
  personal access token. Users can generate a personal access token from the
  settings page on their GitHub account.

# GitHub 身份驗證方法允許使用者使用 GitHub personal access token進行身份驗證。使用者可以從其 GitHub Settings -> Developer Settings -> Personal access tokens (classic) 生成個人訪問令牌。

  Authenticate using a GitHub token:

      $ vault login -method=github token=abcd1234

Configuration:

  mount=<string>
      Path where the GitHub credential method is mounted. This is usually
      provided via the -path flag in the "vault login" command, but it can be
      specified here as well. If specified here, it takes precedence over the
      value for -path. The default value is "github".

# GitHub 憑證方法掛載的路徑。通常透過 "vault login" 指令的 -path flag 提供，但這裡也可以指定。如果在這裡指定，則優先於 -path 的值。預設的路徑值為 "github"。

  token=<string>
      GitHub personal access token to use for authentication. If not provided,
      Vault will prompt for the value.

# 用於身份驗證的 GitHub personal access token。如果未提供，Vault 將提示輸入此值。
```

輸出顯示了使用 GitHub 方法進行 login 的例子。該方法要求必須定義該方法，並由使用者提供 GitHub personal access token。

由於你將嘗試使用身份驗證方法進行登錄，請確保在此 shell session 中未設置 VAULT_TOKEN 環境變數，因為其值將優先於你從 Vault 獲取的任何 token。

取消設定該環境變數。

```bash
unset VAULT_TOKEN
```

嘗試使用 github auth methods 登入

```bash
vault login -method=github
```

output，使用者使用 github personal access token，取得有效的 vault token
- token 格式不同
- token 的效期為 768h，短效期 token 的曝險程度較低
- 這個 token 的 policy 權限只有 default policy
- metadata 是 github 回傳的，vault 中並沒有建立 username=chechiachang 的資料
  - org 是 chechia-net
  - username 是 chechiachang

```
GitHub Personal Access Token (will be hidden):

Success! You are now authenticated. The token information displayed below
is already stored in the token helper. You do NOT need to run "vault login"
again. Future Vault requests will automatically use this token.

Key                    Value
---                    -----
token                  hvs.CAESI...ncU0
token_accessor         lKVpMawotXg1fXcgRvpAOAwQ
token_duration         768h
token_renewable        true
token_policies         ["default"]
identity_policies      []
policies               ["default"]
token_meta_org         chechia-net
token_meta_username    chechiachang
```

當未提供 GitHub personal access token 給命令時，Vault CLI 會提示使用者輸入。

如果提供了有效的 GitHub personal access token，則使用者將成功登錄 vault，並且輸出會顯示一個 Vault token。使用者可以使用這個 Vault token，直到該 token 被撤銷或其有效期超過了 token_duration。

你可以使用 vault token lookup 來檢視當前的 token

```bash
vault token lookup
```

output，顯示使用中的 token，使用的 path 與 methods 是 github/，效期 ttl 在倒數中逐漸減少 767h54m27s

```
Key                 Value
---                 -----
accessor            lKVpMawotXg1fXcgRvpAOAwQ
creation_time       1694873434
creation_ttl        768h
display_name        github-chechiachang
entity_id           5d8af1ab-53a2-e1c5-61bf-bb0b6c7d190f
expire_time         2023-10-18T22:10:34.812089+08:00
explicit_max_ttl    0s
id                  hvs.CAESI...ncU0
issue_time          2023-09-16T22:10:34.812099+08:00
meta                map[org:chechia-net username:chechiachang]
num_uses            0
orphan              true
path                auth/github/login
policies            [default]
renewable           true
ttl                 767h54m27s
type                service
```

記得我們建立 team 的 policy = default + application 嗎？你可以在 github 上把 user 加入到 team/sre

例如我們把 chechiachang 加入到 org/chechia-net 的 team/sre

當前登入 session 權限尚未更新，我們直接重新登入一次

```bash
vault login -method=github
```

output，可以看見登入後的 policy 權限增加成為 default + application

```
GitHub Personal Access Token (will be hidden):

Success! You are now authenticated. The token information displayed below
is already stored in the token helper. You do NOT need to run "vault login"
again. Future Vault requests will automatically use this token.

Key                    Value
---                    -----
token                  hvs.CAES...RcmE
token_accessor         6DbsDizOenhCuWMmUWspTZwp
token_duration         768h
token_renewable        true
token_policies         ["application" "default"]
identity_policies      []
policies               ["application" "default"]
token_meta_org         chechia-net
token_meta_username    chechiachang
```

以上是透過 github/ auth methods
- 管理者設定 github/ method config
- 使用者 chechiachang，使用 github/ method login
- 使用的權限管理是依照 github org / team 來管理，vault 並沒有紀錄 team 與使用者資料

### 清理：移除 auth methods

使用 root token 再次進行登錄。

```bash
vault login
```

output

```
Token (will be hidden):

Success! You are now authenticated. The token information displayed below
is already stored in the token helper. You do NOT need to run "vault login"
again. Future Vault requests will automatically use this token.

Key                  Value
---                  -----
token                hvs.J80w...mjoh
token_accessor       DaI1V1rq9tKZX5EaO4AfMI26
token_duration       ∞
token_renewable      false
token_policies       ["root"]
identity_policies    []
policies             ["root"]
```

使用以下指令撤銷 github/ auth methods 產生的 token

```bash
vault token revoke -mode path auth/github
```

output

```bash
Success! Revoked token (if it existed)
```

vault server log，對於 auth/github 路徑的所有登錄生成的令牌都已被撤銷。

```
2023-09-16T22:25:06.793+0800 [INFO]  expiration: revoked lease: lease_id=auth/github/login/h71720c9bc6fed61d459da4b172dc518a6d55b1dd33c70103cf0b12eb42d7741a
2023-09-16T22:25:06.793+0800 [INFO]  expiration: revoked lease: lease_id=auth/github/login/hd2b110a8eda38814ac0e3ba7ccb926e75205c5065480c9c2675ae5f2860f9f97
```

所有身份驗證方法，除了 token 身份驗證方法，都可以被停用。

停用 github 身份驗證方法

```bash
vault auth disable github
```

output

```bash
Success! Disabled the auth method (if it existed) at: github/
```

vault server log

```bash
2023-09-16T22:27:42.040+0800 [INFO]  core: disabled credential backend: path=auth/github/
```

所有使用此身份驗證方法進行登錄生成的token都已被撤銷。

### 清理 github

如果有建立 org / team / github personal access token 的話，記得移除他

### chatGPT

本段部分內容使用 chatGPT-3.5 翻譯
https://developer.hashicorp.com/vault/tutorials/getting-started/getting-started-authentication
https://developer.hashicorp.com/vault/docs/auth/github
內容，並由筆者人工校驗

base context
```
我希望你能充當一名繁體中文翻譯，拼寫修正者和改進者。我將用英文與程式語言與你對話，你將翻譯它，並以已糾正且改進的版本回答，以繁體中文表達。我希望你能用更美麗和優雅、高級的繁體中文詞語和句子替換我簡化的詞語和句子。保持意義不變。我只希望你回答糾正和改進，不要寫解釋。

不要使用敬語，翻譯結果中若出現"您"，請用"你"取代"您"。
```

result correction
```
部分英文內容為專有名詞，產生的繁體中文翻譯結果中，這些名詞維持英文，不需要翻譯成中文：key，value，certificate，token，policy，policy rule，path，path-based，key rolling，audit，audit trail，plain text，key value，Consul，S3 bucket，Leasing，Renewal，binary，prefix，instance，metadata。

修正下列翻譯：將 "數據" 改為 "資料"，將 "數據庫" 改為 "資料庫"，將 "數據" 改為 "資料"，將 "訪問" 改為 "存取"，將 "源代碼" 改為 "原始碼"，將 "信息" 改為 "資訊"，將 "命令" 改為 "指令"，將 "禁用" 改為 "停用"，將 "默認" 改為 "預設"。
```

