---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Vault Workshop 04: Secret Engine KV V2"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2023-09-14T00:42:26+08:00
lastmod: 2023-09-14T00:42:26+08:00
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

# Day 04：Secret Engine KV V2

KV秘密引擎，用於在Vault的已配置物理Storage中，存儲任意秘密。

key 名稱必須始終是字符串。如果你直接通過CLI編寫非字串 value，它們將被轉換為字串。但是，你可以通過從JSON文件中將key-value pair寫入Vault，或使用HTTP API來保留非字串 value。

此秘密引擎遵照ACL policy中，創建(create)和更新(update)權限之間的設定。它還支持patch功能，用於表示部分更新(patch)，而更新功能(update)則表示完全覆蓋。

### 設置

大多數秘密引擎必須在執行其功能之前事先配置。這些步驟通常由操作人員或配置管理工具完成。

啟用v2 kv秘密引擎：

啟動一個乾淨的本地的開發模式 Vault Server，全新的 Vault Server 包含底下預設啟用的引擎

```bash
vault server -dev

export VAULT_ADDR='http://127.0.0.1:8200'

vault secrets list

Path          Type         Accessor              Description
----          ----         --------              -----------
cubbyhole/    cubbyhole    cubbyhole_57a4ca51    per-token private secret storage
identity/     identity     identity_c2ecbd49     identity store
secret/       kv           kv_c41afde8           key/value secret storage
sys/          system       system_c063e514       system endpoints used for control, policy and debugging
```

你可以在指定的路徑下，啟用一個新的 v2 kv 秘密引擎。若不指定 -path 參數，則預設 path 為 type，也就是 path=kv。

```bash
vault secrets enable -version=2 -path=kv kv

Path          Type         Accessor              Description
----          ----         --------              -----------
cubbyhole/    cubbyhole    cubbyhole_57a4ca51    per-token private secret storage
identity/     identity     identity_c2ecbd49     identity store
kv/           kv           kv_904eee17           n/a
secret/       kv           kv_c41afde8           key/value secret storage
sys/          system       system_c063e514       system endpoints used for control, policy and debugging
```

或者，你可以將kv-v2作為秘密引擎類型，以參數傳遞：

```bash
vault secrets enable kv-v2
```

上面的指令與下面的指令等效，重複執行會出現路徑重複錯誤

```bash
vault secrets enable -path kv-v2 -version=2 kv-v2

Error enabling: Error making API request.

URL: POST http://127.0.0.1:8200/v1/sys/mounts/kv-v2
Code: 400. Errors:

* path is already in use at kv-v2/
```

你可以停用一個秘密引擎

```bash
vault secrets disable kv-v2
```

為了學習效果，往後課程都會使用更完整的指令，作為示範。

更多啟用秘密引擎的指令，你可以參考 vault secrets enable --help 的協助指令

```bash
vault secrets enable --help

Usage: vault secrets enable [options] TYPE

  Enables a secrets engine. By default, secrets engines are enabled at the path
  corresponding to their TYPE, but users can customize the path using the
  -path option.

  啟用秘密引擎。預設情況下，秘密引擎會在與其類型相對應的路徑啟用，但使用者可以使用
  -path 選項自訂路徑。

  Once enabled, Vault will route all requests which begin with the path to the
  secrets engine.

  一旦啟用，Vault 將將所有以該路徑開頭的請求路由到秘密引擎。

  Enable the AWS secrets engine at aws/:

      $ vault secrets enable aws

  Enable the SSH secrets engine at ssh-prod/:

      $ vault secrets enable -path=ssh-prod ssh

  Enable the database secrets engine with an explicit maximum TTL of 30m:

      $ vault secrets enable -max-lease-ttl=30m database

  Enable a custom plugin (after it is registered in the plugin registry):

      $ vault secrets enable -path=my-secrets -plugin-name=my-plugin plugin

  OR (preferred way):

      $ vault secrets enable -path=my-secrets my-plugin
```

從上面的內容，可以看到秘密引擎支援各種不同的秘密類型，例如以下都是一個秘密引擎類型：aws，ssh，database，plugin。

注意，請不要弄混 path=aws 的秘密引擎，以及 type=aws 的秘密引擎。底下是一個十分混淆的例子：

```bash
vault secrets enable --version=2 --path=kv-v1 kv
vault secrets enable --version=1 --path=kv-v2 kv

vault secrets list --detailed

Path          Plugin       Accessor              Default TTL    Max TTL    Force No Cache    Replication    Seal Wrap    External Entropy Access    Options           Description                                                UUID                                    Version    Running Version          Running SHA256    Deprecation Status
----          ------       --------              -----------    -------    --------------    -----------    ---------    -----------------------    -------           -----------                                                ----                                    -------    ---------------          --------------    ------------------
cubbyhole/    cubbyhole    cubbyhole_57a4ca51    n/a            n/a        false             local          false        false                      map[]             per-token private secret storage                           cee0001e-95f8-efaa-6a9a-a3d5c3573abc    n/a        v1.14.3+builtin.vault    n/a               n/a
identity/     identity     identity_c2ecbd49     system         system     false             replicated     false        false                      map[]             identity store                                             3b481e0d-1c6d-6698-85c3-c52839b4d6e4    n/a        v1.14.3+builtin.vault    n/a               n/a
kv-v1/        kv           kv_c8de7a39           system         system     false             replicated     false        false                      map[version:2]    n/a                                                        98289587-5b5d-06f3-c3cf-469e830eda9e    n/a        v0.15.0+builtin          n/a               supported
kv-v2/        kv           kv_f83d9acd           system         system     false             replicated     false        false                      map[version:1]    n/a                                                        5fc
```

請不要做這種不良的命名，誤導自己也誤導別人。不建議把 engine type 當作 path，實務上也沒有必要這個做。

```bash
vault secrets disable kv-v1
vault secrets disable kv-v2
```

使用公司組織，團隊，專案名稱，作為 engine path 的命名，是個不錯的起點。
- org = chechia.net
- team = sre
- project = workshop

```bash
vault secrets enable --version=2 --path=chechia-net/sre/workshop kv
```

###  使用 v2 kv

在秘密引擎配置完成，且用戶/機器具備具有適當權限的Vault token後，它可以生成憑證。KV秘密引擎允許將任意vvalue寫入指定的key。

在KV-v2中仍然可以使用類似路徑的KV-v1語法來引用秘密（secret/foo），但我們建議使用-flag的語法以避免將其錯誤認為是秘密的實際路徑（secret/data/foo是真正的路徑）。

### 寫入/讀取任意資料

寫入任意資料：

```bash
vault kv put -mount=chechia-net/sre/workshop my-secret foo=a bar=b

============= Secret Path =============
chechia-net/sre/workshop/data/my-secret

======= Metadata =======
Key                Value
---                -----
created_time       2023-09-15T16:48:45.817265Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            1
```

讀取任意資料：

```bash
vault kv get -mount=chechia-net/sre/workshop my-secret

============= Secret Path =============
chechia-net/sre/workshop/data/my-secret

======= Metadata =======
Key                Value
---                -----
created_time       2023-09-15T16:48:45.817265Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            1

=== Data ===
Key    Value
---    -----
bar    b
foo    a
```

### 多版本控制

v2 kv 支援記錄多版本的秘密。請提供另一個版本，以前的版本仍然可訪問。

可以選擇傳遞-cas flag以執行寫入前檢查(check-and-set)。如果未設置，將直接允許寫入。

為了使寫入成功，cas必須設置為秘密的當前版本。如果設置為0，只有在密鑰不存在時才允許寫入，因為未設置的密鑰沒有任何版本信息。

還要記住，soft delete 不會從存儲中刪除任何底層版本數據。為了寫入 soft delete 的密鑰，cas參數必須匹配密鑰的當前版本。

```bash
vault kv put -mount=chechia-net/sre/workshop -cas=1 my-secret foo=aa bar=bb

============= Secret Path =============
chechia-net/sre/workshop/data/my-secret

======= Metadata =======
Key                Value
---                -----
created_time       2023-09-15T16:50:26.621978Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            2
```

讀取會回傳最新版本的秘密

```bash
vault kv get -mount=chechia-net/sre/workshop my-secret

============= Secret Path =============
chechia-net/sre/workshop/data/my-secret

======= Metadata =======
Key                Value
---                -----
created_time       2023-09-15T16:50:26.621978Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            2

=== Data ===
Key    Value
---    -----
bar    bb
foo    aa
```

可以使用vault kv patch命令進行部分更新。

該命令將首先嘗試進行HTTP PATCH請求，該請求需要patch ACL功能。如果使用的 token 沒有允許patch功能的policy，則PATCH請求將失敗。

在現在的範例，完整的PATCH命令將執行讀取、本地更新和後續寫入，這需要讀取和更新ACL policy權限。

可以選擇傳遞-cas flag 以執行寫入前檢查(check-and-set)。-cas 只會在初始PATCH請求的情況下生效。

```bash
vault kv patch -mount=chechia-net/sre/workshop -cas=2 my-secret bar=bbb

============= Secret Path =============
chechia-net/sre/workshop/data/my-secret

======= Metadata =======
Key                Value
---                -----
created_time       2023-09-15T16:54:03.925959Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            3
```


vault kv patch命令還支持一個 -method 標誌，可用於指定兩種 method
- HTTP PATCH
- 讀取後寫入(read-and-write)
支持的值分別是patch和rw

使用patch方法

```bash
vault kv patch -mount=chechia-net/sre/workshop -method=patch -cas=3 my-secret bar=bbb

============= Secret Path =============
chechia-net/sre/workshop/data/my-secret

======= Metadata =======
Key                Value
---                -----
created_time       2023-09-15T17:02:55.522095Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            4
```

使用read-and-write

如果使用讀取後寫入(read-and-write)流程，將使用讀取返回的秘密版本值，在後續寫入中，執行寫入前檢查(check-and-set)。

```bash
vault kv patch -mount=chechia-net/sre/workshop -method=rw my-secret bar=ccc

============= Secret Path =============
chechia-net/sre/workshop/data/my-secret

======= Metadata =======
Key                Value
---                -----
created_time       2023-09-15T17:03:37.331182Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            5
```

你可以使用 -version flag 來存取更早的版本

```bash
vault kv get -mount=chechia-net/sre/workshop -version=1 my-secret

============= Secret Path =============
chechia-net/sre/workshop/data/my-secret

======= Metadata =======
Key                Value
---                -----
created_time       2023-09-15T16:48:45.817265Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            1

=== Data ===
Key    Value
---    -----
bar    b
foo    a
```

### 刪除資料

在刪除資料時，標準的 vault kv delete 命令將執行 soft delet。它將標記版本為已刪除並填充 `deletion_time` timestamp。soft delete 不會從存儲中刪除底層版本資料，這允許版本可以被還原

還原版本

```bash
vault kv undelete
```

只有當秘密的版本數超過 max-versions 設置允許的版本數時，或者使用 vault kv destroy 時，版本的資料才會永久刪除。

使用 destroy 命令時，底層版本資料將被刪除，並將密鑰 metadata 標記為已銷毀。如果通過超過 max-versions 來清理版本，則版本 metadata 也將從密鑰中刪除。

可以使用 delete 命令刪除密鑰的最新版本，這也可以使用 -versions 標誌刪除之前的版本：

```bash
vault kv delete -mount=chechia-net/sre/workshop my-secret

Success! Data deleted (if it existed) at: chechia-net/sre/workshop/data/my-secret
```

讀取 version=5 時，只回傳 metadata，無法讀取資料

```bash
vault kv get -mount=chechia-net/sre/workshop -version=5 my-secret

============= Secret Path =============
chechia-net/sre/workshop/data/my-secret

======= Metadata =======
Key                Value
---                -----
created_time       2023-09-15T17:03:37.331182Z
custom_metadata    <nil>
deletion_time      2023-09-15T17:10:01.558586Z
destroyed          false
version            5
```

讀取 version=4 時，可以順利讀取資料

```bash
vault kv get -mount=chechia-net/sre/workshop -version=4 my-secret

============= Secret Path =============
chechia-net/sre/workshop/data/my-secret

======= Metadata =======
Key                Value
---                -----
created_time       2023-09-15T17:02:55.522095Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            4

=== Data ===
Key    Value
---    -----
bar    bbb
foo    aa
```

你可以復原一個刪除的版本 version=5

```bash
vault kv undelete -versions=5  chechia-net/sre/workshop/my-secret

Success! Data written to: chechia-net/sre/workshop/undelete/my-secret
```

這邊 undelete 使用了 legacy 的 secret path，而不使用 -mount flag，是因為 v2 kv 在處理多層 mount path 的 bug [Github Issue: #19811](https://github.com/hashicorp/vault/pull/19811)，[PR #19811](https://github.com/hashicorp/vault/pull/19811) is comming lol。

```bash
vault kv undelete -versions=5 -mount=chechia-net/sre/workshop my-secret

Error writing data to workshop/undelete/my-secret: Error making API request.

URL: PUT http://127.0.0.1:8200/v1/workshop/undelete/my-secret
Code: 404. Errors:

* no handler for route "workshop/undelete/my-secret". route entry not found.
```

### metadata

所有版本和密鑰 metadata 可以使用 metadata 命令和API 進行檢查。

刪除 metadata 密鑰將導致該密鑰的所有 metadata 和版本永久刪除。

有關更多信息，请參見以下命令：

可以查看密鑰的所有元數據和版本：

```bash
vault kv metadata get -mount=chechia-net/sre/workshop my-secret

============== Metadata Path ==============
chechia-net/sre/workshop/metadata/my-secret

========== Metadata ==========
Key                     Value
---                     -----
cas_required            false
created_time            2023-09-15T16:48:45.817265Z
current_version         5
custom_metadata         <nil>
delete_version_after    0s
max_versions            0
oldest_version          0
updated_time            2023-09-15T17:03:37.331182Z

====== Version 1 ======
Key              Value
---              -----
created_time     2023-09-15T16:48:45.817265Z
deletion_time    n/a
destroyed        false

====== Version 2 ======
Key              Value
---              -----
created_time     2023-09-15T16:50:26.621978Z
deletion_time    n/a
destroyed        false

====== Version 3 ======
Key              Value
---              -----
created_time     2023-09-15T16:54:03.925959Z
deletion_time    n/a
destroyed        false

====== Version 4 ======
Key              Value
---              -----
created_time     2023-09-15T17:02:55.522095Z
deletion_time    n/a
destroyed        false

====== Version 5 ======
Key              Value
---              -----
created_time     2023-09-15T17:03:37.331182Z
deletion_time    2023-09-15T17:15:40.767682Z
destroyed        false
```

你可以透過更改 metadata API 調整 secret 的屬性

```bash
vault kv metadata put -mount=chechia-net/sre/workshop \
    -max-versions 2 \
    -delete-version-after="3h25m19s" my-secret

Success! Data written to: secret/metadata/my-secret
```

Delete-version-after 只會應用在新的版本上，Max versions changes 會應用在下次寫入 

```bash
vault kv put -mount=chechia-net/sre/workshop my-secret new=123

============= Secret Path =============
chechia-net/sre/workshop/data/my-secret

======= Metadata =======
Key                Value
---                -----
created_time       2023-09-15T17:34:09.61954Z
custom_metadata    <nil>
deletion_time      2023-09-15T20:59:28.61954Z
destroyed          false
version            6
```

根據 max-version 的設定結果，只保留 version=5 與 version=6，更舊的版本都被刪除

```bash
vault kv metadata get -mount=chechia-net/sre/workshop my-secret

============== Metadata Path ==============
chechia-net/sre/workshop/metadata/my-secret

========== Metadata ==========
Key                     Value
---                     -----
cas_required            false
created_time            2023-09-15T16:48:45.817265Z
current_version         6
custom_metadata         <nil>
delete_version_after    3h25m19s
max_versions            2
oldest_version          5
updated_time            2023-09-15T17:34:09.61954Z

====== Version 5 ======
Key              Value
---              -----
created_time     2023-09-15T17:03:37.331182Z
deletion_time    2023-09-15T17:15:40.767682Z
destroyed        false

====== Version 6 ======
Key              Value
---              -----
created_time     2023-09-15T17:34:09.61954Z
deletion_time    2023-09-15T20:59:28.61954Z
destroyed        false
```

###  Vault 命名空間(namespace) 和掛載(mount)結構

命名空間是功能上創建“Vault中的Vault”的隔離環境。它們具有獨立的登錄路徑，並支持創建和管理與其命名空間隔離的數據。此功能使你能夠將Vault作為服務提供給租戶。

為什麼這個主題很重要？

Vault中的一切都是基於路徑的。每個路徑對應於Vault中的操作或秘密，Vault API endpoint映射到這些路徑。因此，編寫 policy 會配置對特定秘密 path 的允許操作。

例如，為了授予管理根命名空間中的令牌的訪問權限，策略路徑是auth/token/。要管理教育命名空間中的令牌，完全合格的路徑在功能上變為education/auth/token/。

以下圖表示了基於授權方法和秘密引擎啟用位置的API路徑。

![](https://developer.hashicorp.com/_next/image?url=https%3A%2F%2Fcontent.hashicorp.com%2Fapi%2Fassets%3Fproduct%3Dtutorials%26version%3Dmain%26asset%3Dpublic%252Fimg%252Fvault%252Fdiagram_namespaces_paths.png%26width%3D1273%26height%3D582&w=3840&q=75)

你可以使用命名空間，或為每個Vault客戶端專用的掛載來隔離秘密。

例如，你可以為每個獨立的租戶創建一個命名空間，他們負責管理其命名空間下的資源。或者，你可以在組織內的每個團隊專用的路徑上安裝專用秘密引擎。

![命名空間最佳實踐](https://developer.hashicorp.com/_next/image?url=https%3A%2F%2Fcontent.hashicorp.com%2Fapi%2Fassets%3Fproduct%3Dtutorials%26version%3Dmain%26asset%3Dpublic%252Fimg%252Fvault%252Fdiagram_namespaces_intro.png%26width%3D953%26height%3D444&w=1920&q=75)

根據如何隔離秘密，確定了誰負責管理這些秘密，更重要的是與這些秘密相關的策略。

### Prerequisites

如果你對Vault命名空間還不熟悉，請查看帶有命名空間的安全多租戶教程。

注意

創建命名空間應由具有高度特權令牌（例如root）的用戶執行，以為每個組織、團隊或應用程序設置隔離環境。

### 部署注意事項

要計劃和設計Vault命名空間、授權方法路徑和秘密引擎路徑，你需要考慮如何為你的組織，設計Vault的邏輯對象。

組織結構 - 你的組織結構是什麼？

部門、團隊、服務、應用程序之間的層級，在Vault最終設計中需要反映什麼？

Vault policy 如何管理？

團隊是否需要直接管理其負責範圍的 policy？

### chatGPT

本段內容使用 chatGPT-3.5 翻譯
https://developer.hashicorp.com/vault/docs/secrets/kv/kv-v2
https://developer.hashicorp.com/vault/tutorials/recommended-patterns/namespace-structure
內容，並由筆者人工校驗

base context
```
我希望你能充當一名繁體中文翻譯，拼寫修正者和改進者。我將用英文與程式語言與你對話，你將翻譯它，並以已糾正且改進的版本回答，以繁體中文表達。我希望你能用更美麗和優雅、高級的繁體中文詞語和句子替換我簡化的詞語和句子。保持意義不變。我只希望你回答糾正和改進，不要寫解釋。不要使用敬語，請用你取代你。
```

result correction
```
部分英文內容為專有名詞，產生的繁體中文翻譯結果中，這些名詞維持英文，不需要翻譯成中文：key，value，certificate，token，policy，policy rule，path，path-based，key rolling，audit，audit trail，plain text，key value，Consul，S3 bucket，Leasing，Renewal，binary，prefix，instance，metadata。

修正下列翻譯：數據改為資料，數據庫改為資料庫，數據改為資料，訪問改為存取，源代碼改為原始碼，信息改為資訊，命令改為指令，禁用改為停用，默認改為預設。
```

