---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Vault Workshop 07: Policy & approle"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2023-09-14T03:42:26+08:00
lastmod: 2023-09-14T03:42:26+08:00
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

# Day 07: Policy & Approle

在 Vault 中，策略（Policies）控制著使用者可以訪問的資源。在上一篇身份驗證中，你已經學到了身份驗證方法(authentication method)。而這一節是關於授權(Authorization)，也就是合法的用戶登入後，應該能夠取得怎樣的權限。

在身份驗證方面，Vault 提供了多種啟用和使用的選項或方法。Vault 在授權和 policy 方面也使用相同的設計。所有身份驗證方法都將登入者的身份 map 回與 Vault 配置的核心 policy。

### 準備環境

在 [vault 官方網站文件](https://developer.hashicorp.com/vault/tutorials/getting-started/getting-started-policies)中，Hashicorp 官方準備了 [https://instruqt.com/](https://instruqt.com/)的 session lab

筆者個人覺得 interactive lab 的 browser tab 很難用，也不喜歡 Terminal session 連 remote VM 的延遲，以下內容還是會使用 local dev Server 說明。

觀眾們可以自己斟酌使用。

### Policy 格式

策略（Policies）是以HCL撰寫的，但也兼容JSON格式。以下是一個範例策略：

```hcl
# Dev servers have version 2 of KV secrets engine mounted by default, so will
# need these paths to grant permissions:
path "secret/data/*" {
  capabilities = ["create", "update"]
}

path "secret/data/foo" {
  capabilities = ["read"]
}
```

這個範例 policy 授予了對 KV v2 秘密管理（secrets engine）的資源的能力。如果你對於與這個秘密管理引擎相關的路徑不熟悉，可以查閱該秘密管理引擎文件中的 [ACL 規則](https://developer.hashicorp.com/vault/docs/secrets/kv/kv-v2#acl-rules)部分。

根據這個 policy，使用者可以對 `secret/data/` 中的任何秘密進行寫入操作，但對於 `secret/data/foo` 的存取僅允許讀取。policy 的預設行為是 Deny，因此不允許對未指定路徑的資源進行任何存取。

policy 格式使用 prefix 匹配系統來確定對 API 路徑的訪問控制。使用最具體的已定義策略，即精確匹配或最長 prefix 匹配。也就是存取 `secret/data/foo` 路徑符合上面兩條規則，但是由於第二條規則的路徑 match 最長最精確，所以最終拿到的權限是 "read"

由於 Vault 中的一切都必須通過 API 進行訪問，這使得對 Vault 的每個方面都有嚴格的控制，包括啟用秘密管理引擎、啟用身份驗證方法、身份驗證，以及存取秘密等。

有一些內建的策略無法被移除。例如，root policy 和 default policy 是必需的策略，無法被刪除。
- default policy 提供了一組常見的權限，並且 default 包含在所有 token 中。
- root policy 給予 token 超級管理員權限，類似於Linux機器上的 root 用戶。

### 啟動本地開發環境

步驟在前幾篇已經出現過數次，這邊就簡單帶過

```bash
vault server -dev -dev-no-store-token

export VAULT_ADDR='http://127.0.0.1:8200'

unset VAULT_TOKEN

vault login
```

### Defult policy

你可以用下列指令列出預設的 policy

```bash
vault policy list
```

output

```bash
default
root
```

可以用以下指令讀取 default policy 的內容

```bash
vault policy read default
```

output 回傳許多條 policy rule，主要是給予 token 基本的操作權限

```bash
# Allow tokens to look up their own properties
path "auth/token/lookup-self" {
    capabilities = ["read"]
}

# Allow tokens to renew themselves
path "auth/token/renew-self" {
    capabilities = ["update"]
}

# Allow tokens to revoke themselves
path "auth/token/revoke-self" {
    capabilities = ["update"]
}
...
```

熟悉 default policy 內容後，可以斟酌使用。或是選擇從頭編寫自己的 policy。

### 編寫第一個 policy

要撰寫 policy ，使用 vault policy write 指令。請查閱該指令的幫助文件以進一步了解用法。

```bash
vault policy write -h
```

```bash
Usage: vault policy write [options] NAME PATH

  Uploads a policy with name NAME from the contents of a local file PATH or
  stdin. If PATH is "-", the policy is read from stdin. Otherwise, it is
  loaded from the file at the given path on the local disk.

# 使用 vault policy write 指令，可以從本地文件 PATH 或標準輸入（stdin）的內容上傳一個名為 NAME 的策略。如果 PATH 是 "-"，則策略將從 stdin 讀取。否則，它將從本地 disk 上給定路徑的文件中載入。

  Upload a policy named "my-policy" from "/tmp/policy.hcl" on the local disk:

      $ vault policy write my-policy /tmp/policy.hcl

  Upload a policy from stdin:

      $ cat my-policy.hcl | vault policy write my-policy -
```

使用以下指令創建名為 "my-policy" 的 policy，並將其內容來自 stdin（標準輸入）

```bash
vault policy write my-policy - << EOF

# Dev servers have version 2 of KV secrets engine mounted by default, so will
# need these paths to grant permissions:
path "secret/data/*" {
  capabilities = ["create", "update"]
}

path "secret/data/foo" {
  capabilities = ["read"]
}
EOF
```

output

```bash
Success! Uploaded policy: my-policy
```

使用下列指令列出 policy

```bash
vault policy list
```

output

```bash
default
my-policy
root
```

讀取 my-policy 的內容

```bash
vault policy read my-policy
```

output

```
# Dev servers have version 2 of KV secrets engine mounted by default, so will
# need these paths to grant permissions:
path "secret/data/*" {
  capabilities = ["create", "update"]
}

path "secret/data/foo" {
  capabilities = ["read"]
}
```

### 測試 policy


你所建立的 policy ，提供對 KV-V2 秘密引擎所定義的秘密進行管理。policy 被附加到 Vault 直接生成的 otoken，或透過其各種授權方法生成的 token 上。

創建一個 token ，添加 my-policy。-field flag 設定只回傳部分 key-vault data，而不是傳整個 metadata table。-policy 設定連結 token 的 policy。

```bash
vault token create -field token -policy=my-policy
```

```bash
hvs.CAESIIDh...UxbUU
```

為了簡化，本內容使用 dev 模式伺服器，直接從 token 授權方法創建 token 。請記住，在大多數 production 環境部署中，token 將由已啟用的授權方法(ex. github auth method)創建。

可以使用 token login

```bash
vault login
```

output 回傳登入資訊，以及連結 token 的 policy，policy 包含 default 與 my-policy

```
Success! You are now authenticated. The token information displayed below
is already stored in the token helper. You do NOT need to run "vault login"
again. Future Vault requests will automatically use this token.

Key                  Value
---                  -----
token                hvs.CAESIIDh...UxbUU
token_accessor       vY3aLwMSezlxeOn7YwcjxuhZ
token_duration       767h56m52s
token_renewable      true
token_policies       ["default" "my-policy"]
identity_policies    []
policies             ["default" "my-policy"]
```

你可以執行 vault token lookup，查找目前 token 的完整資訊

```bash
vault token lookup
```

output

```bash
Key                 Value
---                 -----
accessor            vY3aLwMSezlxeOn7YwcjxuhZ
creation_time       1694917062
creation_ttl        768h
display_name        token
entity_id           n/a
expire_time         2023-10-19T10:17:42.723364+08:00
explicit_max_ttl    0s
id                  hvs.CAESIIDh...UxbUU
issue_time          2023-09-17T10:17:42.723365+08:00
meta                <nil>
num_uses            0
orphan              false
path                auth/token/create
policies            [default my-policy]
renewable           true
ttl                 767h55m45s
type                service
```

這個policy 啟用了 secret/ 秘密引擎內每個路徑的創建和更新功能，除了一個例外路徑 secret/data/foo 僅允許 read。

寫入資料到 secret/data/creds

```bash
vault kv put -mount=secret creds password="my-long-password"
```

output 回傳成功資訊，秘密已成功創建。

```bash
== Secret Path ==
secret/data/creds

======= Metadata =======
Key                Value
---                -----
created_time       2023-09-17T02:26:44.179748Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            1
```

該政策僅啟用了對 secret/data/foo 路徑的讀取功能。嘗試向此路徑寫入將導致"權限拒絕"錯誤。請嘗試寫入 secret/data/foo 路徑。

```bash
vault kv put -mount=secret foo robot=beepboop
```

output，顯示權限錯誤。

```bash
Error writing data to secret/data/foo: Error making API request.

URL: PUT http://127.0.0.1:8200/v1/secret/data/foo
Code: 403. Errors:

* 1 error occurred:
	* permission denied
```

此 policy 定義了一組有限的路徑和功能。如果沒有對 sys 的訪問權限，則系統相關玄線，像 vault policy list 或 vault secrets list 這樣的命令將無法運作。

### kv v2 與 v1 語法

當你使用 vault kv CLI 命令訪問 KV v2 秘密引擎時，我們建議使用 -mount flag 語法，來引用 KV v2 秘密引擎的路徑。

`vault kv get -mount=secret foo` 

你也可以使用兼容 KV v1 風格的路徑 prefix 語法，在某個範圍內上是等效的，系統將自動附加 /data 到秘密路徑，可能會引起混淆。

`vault kv get secret/foo`

### 連結 policy 與 auth method

Vault 本身只有唯一的 policy 授權管理機構，不同於身份驗證，你可以啟用多個身份驗證方法。

你可以配置身份驗證方法，以自動分配一組 policy，給使用某些身份驗證方法創建的 token 。這樣做的方式取決於相關的身份驗證方法，但通常涉及將 role 映射到 policy ，或者將 identity 或 group 映射到 policy。

例如：當設定 github auth method 的 role 時，你可以使用 token policies 參數來實現這一點。

我們這邊嘗試建立另外一個 auth method，AppRole，順便在整理一次 vault -> auth method -> policy 的關係

### 配置 AppRole 身份驗證方法

在以下步驟中，使用權限更高的 root token 進行操作與登入

```bash
vault login
```

output

```bash
Token (will be hidden):

Success! You are now authenticated. The token information displayed below
is already stored in the token helper. You do NOT need to run "vault login"
again. Future Vault requests will automatically use this token.

Key                  Value
---                  -----
token                hvs.uCGr6...749AI
token_accessor       SlAe0epU6CLngp2iclB5WN2A
token_duration       ∞
token_renewable      false
token_policies       ["root"]
identity_policies    []
policies             ["root"]
```

啟用 approle auth method

```bash
vault auth enable approle
```

output

```bash
Success! Enabled approle auth method at: approle/
```

vault server log

```bash
2023-09-17T10:44:26.460+0800 [INFO]  core: enabled credential backend: path=approle/ type=approle version=""
```

### approle 配置 role

我們已經啟用 approle 這個 auth method，接下來要設定名為 "my-role" 的 AppRole role，配置一些基本的token 設定，並將先前定義的 "my-policy" policy，附加到所有通過該 role 創建的 token。

你可以使用下列指令，在 auth/approle/role/ 下新增 my-role，path 也代表 approle / role / my-role 的階層關係

```bash
vault write auth/approle/role/my-role \
   secret_id_ttl=10m \
   token_num_uses=10 \
   token_ttl=20m \
   token_max_ttl=30m \
   secret_id_num_uses=40 \
   token_policies=my-policy
```

output

```bash
Success! Data written to: auth/approle/role/my-role
```

你可以通過使用 auth 方法來驗證這個 AppRole role 是否附加了policy。

要使用 AppRole 進行身份驗證，首先需要獲取角色ID

首先先讀取目前 approle/role/my-role 的設定

```bash
v read auth/approle/role/my-role
```

```bash
Key                        Value
---                        -----
bind_secret_id             true
local_secret_ids           false
secret_id_bound_cidrs      <nil>
secret_id_num_uses         40
secret_id_ttl              10m
token_bound_cidrs          []
token_explicit_max_ttl     0s
token_max_ttl              30m
token_no_default_policy    false
token_num_uses             10
token_period               0s
token_policies             [my-policy]
token_ttl                  20m
token_type                 default
```

然後讀取 my-role 的 role-id

```bash
vault read auth/approle/role/my-role/role-id
```

output

```bash
Key        Value
---        -----
role_id    600dce48-244c-094e-aeae-cb819ec7f5dd
```

接下來，獲取一個秘密ID(它類似於應用程式用於 AppRole 身份驗證的密碼)，由於我們這個示範並不提供額外參數值，這先需要使用 -f | -force flag，強迫 vault 寫入一個沒有 value 的資料到 auth/approle/role/my-role/secret-id endpoint

```bash
vault write -f auth/approle/role/my-role/secret-id
```

可以想像是向 API server 打 POST my-role/secret-id，向 approle 註冊一個 app，server 則回傳一組 id，以辨識這個 app。

```bash
Key                   Value
---                   -----
secret_id             d80db935-9792-faf7-306d-93a2f0c3a18f
secret_id_accessor    32451384-f985-a387-175b-67140225856f
secret_id_num_uses    40
secret_id_ttl         10m

```

最後進行 login 取得 token，這裡使用 vault write 進行 AppRole 身份驗證，指定 role path並使用相應的選項傳遞role id和secret id

```bash
export ROLE_ID=600dce48-244c-094e-aeae-cb819ec7f5dd
export SECRET_ID=d80db935-9792-faf7-306d-93a2f0c3a18f

vault write auth/approle/login \
    role_id=$ROLE_ID \
    secret_id=$SECRET_ID
```

output，取得合法的 token，並且具有我們為 approle/my-role 配置的 my-policy 權限

```bash
Key                     Value
---                     -----
token                   hvs.CAESIB9gD3aupV5X06IRIWMEvhL4QeBtizO20i2Hh2YderxpGh4KHGh2cy5BWVVWVDVFUVI3dkw5VUFUbmdoZmpnUFA
token_accessor          QGrKxnHH4e9SVLqhpaqgYsCZ
token_duration          20m
token_renewable         true
token_policies          ["default" "my-policy"]
identity_policies       []
policies                ["default" "my-policy"]
token_meta_role_name    my-role
```

實務中，這個 `secret_id` 會設置在 application 上，讓 application 具有合法存取 vault 的權限

### 實務範例講解

我們可以重複使用設定好的 policy，綁定到 auth method 上，policy 對 auth method 是多對多的，這邊透過我們上篇 github auth method 來對照一下，解釋 auth method 與 role / policy 的關係

chechia-net 是一個組織

as a admin，我希望藉由 github auth method，讓有 github 權限的工程師，可以存取 vault
  - 並且在 github 上的 org / team 管理各個使用者，vault 可以直接複用 github 的權限階層

於是，透過 github auth method，自動配置 vault 權限給 chechia-net github org 下的使用者

```bash
vault auth enable -path=github-chechia github
vault write auth/github-chechia/config organization=chechia-net
```

as a github user，我希望藉由 github auth method，直接登入 vault，不用註冊額外的帳號

```bash
vault login -method=github -path=github-chechia
```

換成 approle 也是相同道理

as a admin，我希望我的 application 能夠有辦法存取 vault
  - 可能是一個 badkend golang server，需要存取 vault 中的 mysql database credential

```bash
vault auth enable -path=approle-golang-server approle
```

這個 application 可能有複數不同種類工作，所以也希望能夠配置不同的 role，給予不同的 policy 權限
  - role/default 有 default policy
  - role/my-role 有 default, my-policy 兩個 policy

更接近實務的例子，底下可能是常見的 role 用途
  - approle/database，當 application 需要向 db 存取時使用，ex. 去取得 mysql 相關的 credential
  - approle/frontend，讓 application 可以向前端存取測試需要 credential
  - approle/qa，也許是 application 自動化測試的 credential
想表達，雖然來源都是相同 application，使用 approle auth method，vault 還是可以設定不同的 policy，讓 application 取用最小的可用權限，而不會每次登入 vault 都是很大的權限

身為 admin，你可以使用以下命令，在 approle-golang-server 中產生一個 default role

```bash
vault write auth/approle-golang-server/role/default \
   secret_id_ttl=10m \
   token_num_uses=10 \
   token_ttl=20m \
   token_max_ttl=30m \
   secret_id_num_uses=40 \
   token_policies=default
```

增加一個 my-role

```bash
vault write auth/approle-golang-server/role/my-role \
   secret_id_ttl=10m \
   token_num_uses=10 \
   token_ttl=20m \
   token_max_ttl=30m \
   secret_id_num_uses=40 \
   token_policies=default,my-policy
```

列出在 approle-golang-server 中啟用的 role

```bash
vault list auth/approle-golang-server/role/
```

output

```
Keys
----
default
my-role
```

admin 配置完 role 後，記得讀取 role-id，並將 role-id 配置到 application 上
- 可以在 application 中維護一個 map，當使用這透過 application，拿到 default role，就使用 default/role-id
- 搭配接近實務的例子，就是如果是後端工程師使用 application，application 要能夠使用 role/backend/role-id，來向 vault 進行 authentication
  - 你也可以讓 application 有權限讀取 `auth/approle-golang-server/role/*/role-id`，讓 application 透過 vault API 自動取得 role-id

```bash
vault read auth/approle-golang-server/role/default/role-id
vault read auth/approle-golang-server/role/my-role/role-id
```

output

```bash
Key        Value
---        -----
role_id    f0340d97-a97d-85f9-30d5-65a2058baf11

Key        Value
---        -----
role_id    c1f3cd3e-8f0a-8b1f-91f7-a3a310b9755f
```

上面是 admin 需要配置的內容

現在角色換成 application，application 上線了。application 依照情境，選擇要使用那個 role，去取得 secret-id
- 例如 application 要去存取 database，就自己使用 role/database

注意，這個 role/database 與 policy/database 上面都沒有配置，請讀者自己練習，配置一個 placeholder 空的權限，或是發揮創意也可以

```bash
vault write -f auth/approle-golang-server/role/my-role/secret-id
```

output，vault 回覆一組短時效的 secret-id，ttl=10 min

```bash
Key                   Value
---                   -----
secret_id             ad70d84b-56a5-eec2-0a95-6aa7f2cfceef
secret_id_accessor    76a5b993-a139-9837-5990-b6adc483542a
secret_id_num_uses    40
secret_id_ttl         10m
```

application 可以使用 role-id + secret-id，去取得 token

```bash
vault write auth/approle-golang-server/login \
    role_id=$ROLE_ID \
    secret_id=$SECRET_ID
```

output

```bash
Key                     Value
---                     -----
token                   hvs.CA...ZXRVc
token_accessor          zjBhj70A6ed72zksuooxCpYt
token_duration          20m
token_renewable         true
token_policies          ["default" "database"]
identity_policies       []
policies                ["default" "database"]
token_meta_role_name    database
```

### chatGPT

本段部分內容使用 chatGPT-3.5 翻譯
https://developer.hashicorp.com/vault/tutorials/getting-started/getting-started-policies
https://developer.hashicorp.com/vault/docs/concepts/policies
內容，並由筆者人工校驗

base context
```
我希望你能充當一名繁體中文翻譯，拼寫修正者和改進者。我將用英文與程式語言與你對話，你將翻譯它，並以已糾正且改進的版本回答，以繁體中文表達。我希望你能用更美麗和優雅、高級的繁體中文詞語和句子替換我簡化的詞語和句子。保持意義不變。我只希望你回答糾正和改進，不要寫解釋。

很重要：不要使用敬語，翻譯結果中若出現"您"，請用"你"取代"您"。
```

result correction
```
部分英文內容為專有名詞，產生的繁體中文翻譯結果中，這些名詞維持英文，不需要翻譯成中文：key，value，certificate，token，policy，policy rule，path，path-based，key rolling，audit，audit trail，plain text，key value，Consul，S3 bucket，Leasing，Renewal，binary，prefix，instance，metadata。

修正下列翻譯：將 "數據" 改為 "資料"，將 "數據庫" 改為 "資料庫"，將 "數據" 改為 "資料"，將 "訪問" 改為 "存取"，將 "源代碼" 改為 "原始碼"，將 "信息" 改為 "資訊"，將 "命令" 改為 "指令"，將 "禁用" 改為 "停用"，將 "默認" 改為 "預設"。
```

