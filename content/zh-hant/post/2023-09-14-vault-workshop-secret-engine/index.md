---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Vault Workshop 03: Secret Engine"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2023-09-13T22:42:26+08:00
lastmod: 2023-09-13T22:42:26+08:00
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

整篇 Workshop 會使用的範例與原始碼，放在 [Github Repository: vault-playground](http://chechia.net/zh-hant/#projects)

# Day 03：細探 Secret Engine 秘密引擎

### 什麼是秘密引擎？

秘密引擎是Vault的組件，用於存儲、生成或加密秘密。在前面的內容中，你使用了Key/Value v2 秘密引擎來存儲數據。一些秘密引擎，比如鍵/值秘密引擎，僅僅是用來存儲和讀取數據的。其他秘密引擎則連接到其他服務並根據需求生成動態憑證。還有一些秘密引擎提供加密作為服務。

![](https://developer.hashicorp.com/_next/image?url=https%3A%2F%2Fcontent.hashicorp.com%2Fapi%2Fassets%3Fproduct%3Dtutorials%26version%3Dmain%26asset%3Dpublic%252Fimg%252Fvault%252Fvault-triangle.png%26width%3D1641%26height%3D973&w=3840&q=75)


前面的內容中，默認情況下，key/value v2 秘密引擎已啟用，並準備在 secret/ 下接收請求，因為我們在-dev 模式下啟動了Vault Server。

在底下我們使用 kv v1 做簡單的範例。

### mount path

建議在使用 KV v2 秘密引擎時，使用可選的 -mount flag 語法，例如

```bash
vault kv get -mount=secret foo
```

請嘗試以下命令，這將導致錯誤：

```bash
vault kv put foo/bar a=b

Error making API request.

URL: GET http://127.0.0.1:8200/v1/sys/internal/ui/mounts/foo/bar
Code: 403. Errors:

* preflight capability check returned 403, please ensure client's policies grant access to path "foo/bar/"
```

Path prefix 路徑前綴告訴 Vault 應該將流量 route 到哪個秘密引擎

當請求到達 Vault 時，它會使用最長前綴匹配來匹配初始路徑部分，然後將請求傳遞給在該路徑啟用的相應秘密引擎。

- 如果 mount 設置為 foo/bar
  - 則會在 foo/bar 這個 path 下的 secret engine，儲存 a=b
- 如果 mount 設置為 foo
  - 則會在 foo 這個 path 下的 secret engine，儲存在 path /bar，a=b

Vault 將這些秘密引擎呈現得類似於文件系統 (ex. )/usr/local/bin/vault) 
- 在 linux 上存取一個 mount path 不存在的 directory path
- 在 vault 中存取 foo 處未掛載秘密引擎，所以上面的命令返回了錯誤。

對於 vault kv 命令，也可以使用 -mount flag

### 啟用一個秘密引擎

要開始，請在路徑 kv 啟用一個新的 KV 秘密引擎。每個路徑都是完全隔離的，無法與其他路徑通信。例如，

啟用在 foo 的 KV 秘密引擎無法與啟用在 bar 的 KV秘密引擎通信。

```bash
/foo a=b

/bar c=d
```

啟用新的秘密引擎以前，先查看一下目前 vault server 中已經啟用的引擎。

除了 default 存在的引擎，還有在 dev 模式下自動建立的 secret/

default
- cubbyhole/
- identity/
- sys/

dev mode
- secret/

```
vault secrets list

Path          Type         Accessor              Description
----          ----         --------              -----------
cubbyhole/    cubbyhole    cubbyhole_9c6d82c2    per-token private secret storage
identity/     identity     identity_8feb8f49     identity store
secret/       kv           kv_6f946f62           key/value secret storage
sys/          system       system_b45bc416       system endpoints used for control, policy and debugging
```

然後在 path=kv 下，啟用一個 secret engine

```
vault secrets enable -path=kv kv

Success! Enabled the kv secrets engine at: kv/
```

秘密引擎啟用的路徑默認為秘密引擎的名稱。因此，以下命令等效於執行上面的命令。

```
 vault secrets enable kv
```

重複執行這個命令會拋出“路徑已在kv/ 中使用”錯誤。

為了驗證我們的成功並獲取有關秘密引擎的更多信息，使用以下的 vault secrets list 命令：

```
vault secrets list

Path          Type         Accessor              Description
----          ----         --------              -----------
cubbyhole/    cubbyhole    cubbyhole_9c6d82c2    per-token private secret storage
identity/     identity     identity_8feb8f49     identity store
kv/           kv           kv_2b6528af           n/a
secret/       kv           kv_6f946f62           key/value secret storage
sys/          system       system_b45bc416       system endpoints used for control, policy and debugging
```

這顯示了在這個Vault伺服器上已啟用的5個秘密引擎。

你可以看到秘密引擎的類型、相應的路徑以及可選的描述（如果沒有提供描述，則為“n/a”）。

使用帶有 -detailed 標誌運行上述命令可以顯示KV秘密引擎的版本和更多信息。

```
vault  secrets list --detailed

Path          Plugin       Accessor              Default TTL    Max TTL    Force No Cache    Replication    Seal Wrap    External Entropy Access    Options           Description                                                UUID                                    Version    Running Version          Running SHA256    Deprecation Status
----          ------       --------              -----------    -------    --------------    -----------    ---------    -----------------------    -------           -----------                                                ----                                    -------    ---------------          --------------    ------------------
cubbyhole/    cubbyhole    cubbyhole_9c6d82c2    n/a            n/a        false             local          false        false                      map[]             per-token private secret storage                           6087f484-a02c-f36c-0a1a-aa07840f988c    n/a        v1.14.3+builtin.vault    n/a               n/a
identity/     identity     identity_8feb8f49     system         system     false             replicated     false        false                      map[]             identity store                                             c3a1e4ae-09c6-29b9-906a-8281b46690f3    n/a        v1.14.3+builtin.vault    n/a               n/a
kv/           kv           kv_2b6528af           system         system     false             replicated     false        false                      map[]             n/a                                                        5ff9bc4c-6d2c-5fd7-cbe0-e9b7fbf03ee5    n/a        v0.15.0+builtin          n/a               supported
secret/       kv           kv_6f946f62           system         system     false             replicated     false        false                      map[version:2]    key/value secret storage                                   ed28307e-0472-c0a7-b7a9-65543a63e68c    n/a        v0.15.0+builtin          n/a               supported
sys/          system       system_b45bc416       n/a            n/a        false             replicated     true         false                      map[]             system endpoints used for control, policy and debugging    9712d56d-95e3-6c07-796f-d44565de5c07    n/a        v1.14.3+builtin.vault    n/a               n/a
```

sys/ 路徑對應到系統後端。這些路徑與Vault的核心系統交互，對於初學者來說不是必需的。

### 建立 Secret

要創建私鑰，使用 kv put 命令。

```
vault kv put kv/hello target=world

Success! Data written to: kv/hello
```

要讀取存儲在kv/hello路徑中的私鑰，使用 kv get 命令。

```bash
vault kv get kv/hello

===== Data =====
Key       Value
---       -----
target    world
```

嘗試建立第二個 kv/my-secret

```bash
vault kv put kv/my-secret value="s3c(eT"

Success! Data written to: kv/my-secret
```

讀取位於 kv/my-secret 的資料

```bash
vault kv get kv/my-secret

==== Data ====
Key      Value
---      -----
value    s3c(eT
```

刪除位於 kv/my-secret 的資料

```bash
vault kv delete kv/my-secret

Success! Data deleted (if it existed) at: kv/my-secret
```

列出位於 kv/my-secret 的資料

```bash
vault kv list kv/

Keys
----
hello
```

### 停用秘密引擎

當不再需要秘密引擎時，可以將其停用。

當停用秘密引擎時，所有私鑰都將被撤銷，相應的Vault數據和配置將被刪除。

```bash
vault secrets disable kv/

Success! Disabled the secrets engine (if it existed) at: kv/
```

請注意，此命令將路徑作為參數，而不是秘密引擎的類型。

對原始路徑的任何數據路由請求都將導致錯誤，但現在可以在該路徑啟用另一個秘密引擎。

```bash
vault kv get kv/hello

Error making API request.

URL: GET http://127.0.0.1:8200/v1/sys/internal/ui/mounts/kv/hello
Code: 403. Errors:

* preflight capability check returned 403, please ensure client's policies grant access to path "kv/hello/"
```

### 秘密引擎是一個抽象

Vault的行為類似於虛擬文件系統。讀取/寫入/刪除/列出操作將轉發到相應的秘密引擎，秘密引擎決定如何對這些操作做出反應。

這種抽象非常強大。它使Vault能夠直接與物理系統、資料庫、HSM 等進行交互。

但除了這些物理系統外，Vault還可以與更多獨特的環境進行交互，比如AWS IAM、動態SQL user 創建等，所有這些都使用相同的讀取/寫入 interface。

### chatGPT

本段內容使用 chatGPT-3.5 翻譯
https://developer.hashicorp.com/vault/tutorials/getting-started/getting-started-secrets-engines
內容，並由筆者人工校驗

base context
```
我希望你能充當一名繁體中文翻譯，拼寫修正者和改進者。我將用英文與程式語言與你對話，你將翻譯它，並以已糾正且改進的版本回答，以繁體中文表達。我希望你能用更美麗和優雅、高級的繁體中文詞語和句子替換我簡化的詞語和句子。保持意義不變。我只希望你回答糾正和改進，不要寫解釋。不要使用敬語，請用你取代您。
```

result correction
```
部分英文內容為專有名詞，產生的繁體中文翻譯結果中，這些名詞維持英文，不需要翻譯成英文：key，certificate，token，policy，policy rule，path，path-based，key rolling，audit，audit trail，plain text，key value，Consul，S3 bucket，Leasing，Renewal，binary

修正下列翻譯：秘密改為私鑰，數據改為資料，數據庫改為資料庫，數據改為資料，訪問改為存取，源代碼改為原始碼。
```

