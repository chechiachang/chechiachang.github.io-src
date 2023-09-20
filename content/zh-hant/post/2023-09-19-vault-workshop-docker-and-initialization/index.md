---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Vault Workshop 08: Vault in Docker and Initialization"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2023-09-14T04:42:26+08:00
lastmod: 2023-09-14T04:42:26+08:00
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

tags: ["vault", "iac", "workshop", "docker", "terraform", "鐵人賽2023", "chatgpt"]
categories: ["vault", "docker"]
---

如果你希望追蹤最新的草稿，請見[鐵人賽2023](https://chechia.net/zh-hant/tag/%E9%90%B5%E4%BA%BA%E8%B3%BD2023/)

本 workshop 也接受網友的許願清單，[如果有興趣的題目可於第一篇底下留言](https://ithelp.ithome.com.tw/articles/10317378)，筆者會盡力實現，但不做任何保證

整篇 Workshop 會使用的範例與原始碼，放在 [Github Repository: vault-playground](http://chechia.net/zh-hant/#projects)

# Day 08: Vault in Docker and Initialization

### Vault in container

前幾天我們使用 vault dev Server 來啟用測試用的 Vault server。

在 production 環境我們不會使用 dev Server。Vault 提供許多安裝方法
- 可以使用 binary 直接安裝在VM上
- 也可以透過 hashicorp/vault official docker image，在container 環境中執行
- 或是使用 hashicorp official helm chart，安裝在kuberntes上

### 使用範例 repository

你可以使用筆者準備的範例 repository [https://github.com/chechiachang/vault-playground](https://github.com/chechiachang/vault-playground)

```bash
git clone git@github.com:chechiachang/vault-playground.git

cd deploy/00-docker-dev/
```

你可以使用下列指令啟動 vault in docker
- 並使用 -v flag 來掛載 ./config/ volume 到 container 中的 /vault/config.d/

```bash
docker run --cap-add=IPC_LOCK \
  --volume ./vault/config/:/vault/config.d \
  --volume ./vault/file/:/vault/file \
  --volume ./vault/logs/:/vault/logs \
  -p 8200:8200 \
  --name vault_1 \
  -d \
  hashicorp/vault:1.14.3 \
  vault server -config=/vault/config.d/vault.hcl
```

然後使用 docker logs 指令檢視 vault server log

```bash
docker logs -f vault_1
```

output

```bash
==> Vault server configuration:

Administrative Namespace:
             Api Address: https://0.0.0.0:8200
                     Cgo: disabled
         Cluster Address: https://0.0.0.0:8201
   Environment Variables: GODEBUG, GOTRACEBACK, HOME, HOSTNAME, NAME, PATH, PWD, SHLVL, VERSION
              Go Version: go1.20.8
              Listener 1: tcp (addr: "0.0.0.0:8200", cluster address: "0.0.0.0:8201", max_request_duration: "1m30s", max_request_size: "33554432", tls: "disabled")
               Log Level:
                   Mlock: supported: true, enabled: false
           Recovery Mode: false
                 Storage: file
                 Version: Vault v1.14.3, built 2023-09-11T21:23:55Z
             Version Sha: 56debfa71653e72433345f23cd26276bc90629ce

==> Vault server started! Log data will stream in below:

2023-09-20T13:38:25.914Z [INFO]  proxy environment: http_proxy="" https_proxy="" no_proxy=""
2023-09-20T13:38:25.920Z [INFO]  core: Initializing version history cache for core
```

你會發現，vault server 不是以 dev server 的狀態啟動的，需要進行額外的初始化設定


```bash
export VAULT_ADDR='http://127.0.0.1:8200'
```

檢查 vault status

```bash
vault status
```

output，顯示一個上未初始化的 vault server 與其 storage backend "filesyste"
- 可以在 ./vault/config/vault.hcl 上看到我們使用新的 Storage Backend "file" 設定
- vault server 的 storage backend 目前是 sealed 狀態
  - 不是 vault server sealed，而是沒有提供 vault server 初始化設定 / unseal keys，所以 vault server 無法解密 storage backend

```bash
Key                Value
---                -----
Seal Type          shamir
Initialized        false
Sealed             true
Total Shares       0
Threshold          0
Unseal Progress    0/0
Unseal Nonce       n/a
Version            1.14.3
Build Date         2023-09-11T21:23:55Z
Storage Type       file
HA Enabled         false
```

### Storage Backend: filesystem

https://developer.hashicorp.com/vault/docs/configuration/storage/filesystem

filesystem storage backend將 Vault 的資料存儲在文件系統上，使用標準的目錄結構。

它可以用於持久的Single Server情況，或者在本地開發時，耐久性不是關鍵問題的情況下使用。

filesystem storage backend 不支援高可用性 - 檔案系統後端不支援高可用性。

filesystem storage backend 由HashiCorp 官方支援 - 檔案系統後端是由 HashiCorp 官方支援維護的。

### 初始化 Vault

初始化是配置 Vault 的過程。僅對第一次使用在 Vault server 上的 Backend 上執行一次。在高可用(HA)模式下運行時，這僅在每個叢集(Vault Cluster)中執行一次，而不是每台Server。

在初始化期間，將生成加密金鑰、創建 unseal keys，並創建 init root token。

初始化不需身份驗證，僅適用於全新的 Vault，有資料存在的 Storage Backend 無法用初始化解鎖。

要初始化 Vault，使用以下命令

```bash
vault operator init
```

output

```bash
Unseal Key 1: 9AYJ...kNCn
Unseal Key 2: RqDx...odRU
Unseal Key 3: uHUv...lws4
Unseal Key 4: f+KD...aHgL
Unseal Key 5: AKyF...e6vd

Initial Root Token: hvs.8yU3...7esX

Vault initialized with 5 key shares and a key threshold of 3. Please securely
distribute the key shares printed above. When the Vault is re-sealed,
restarted, or stopped, you must supply at least 3 of these keys to unseal it
before it can start servicing requests.


# Vault 使用了 5 個金鑰份額encryption key share和 3 的 key threshold 進行初始化。請安全地分發上面的金鑰份額。
# 當 Vault 被重新密封、重新啟動或停止時，你必須提供至少 3 個這些金鑰來對其進行解封，然後它才能開始處理請求。

Vault does not store the generated root key. Without at least 3 keys to
reconstruct the root key, Vault will remain permanently sealed!

# Vault 不存儲生成的根金鑰。如果沒有至少 3 個金鑰來重建根金鑰，Vault 將保持永久密封！

It is possible to generate new unseal keys, provided you have a quorum of
existing unseal keys shares. See "vault operator rekey" for more information.

# 如果你有足夠的現有解封金鑰份額，則可以生成新的解封金鑰。有關更多信息，請參閱 "vault operator rekey"。
```

初始化過程輸出了兩個非常重要的信息：解封金鑰和 init root token。這是唯一一次 Vault 顯示這些資料。

為了這個入門課程，請將這些金鑰保存在某個地方，然後繼續進行操作。

- Vault backend storage 認 key 不認人，請收好這五隻 unseal key，放置在五個不同安全的地方
- 有 3/5 的 unseal key 就能重建 encryption key，也就是能夠解密 storage backend
- 可以用 3/5 unseal key 產生 root token `vault operator generate-root`
  - 換句話說，unseal key 是比 root 還大的超級管理員 key
- 在實際的部署情況下，你永遠不應該將這些金鑰保存在一起。
  - 你可能會使用 Vault 的 PGP 和 Keybase.io 支援，使用使用者的 PGP 金鑰加密每個解封金鑰。
  - 這可以防止單個人擁有所有的解封金鑰。

vault server log，可以看到 vault server 開始進行初始化流程

```bash
2023-09-20T13:47:05.113Z [INFO]  core: security barrier not initialized
2023-09-20T13:47:05.117Z [INFO]  core: seal configuration missing, not initialized
2023-09-20T14:03:28.506Z [INFO]  core: security barrier not initialized
2023-09-20T14:03:28.512Z [INFO]  core: seal configuration missing, not initialized
2023-09-20T14:03:28.521Z [INFO]  core: security barrier not initialized
2023-09-20T14:03:28.557Z [INFO]  core: security barrier initialized: stored=1 shares=5 threshold=3
2023-09-20T14:03:28.589Z [INFO]  core: post-unseal setup starting
2023-09-20T14:03:28.609Z [INFO]  core: loaded wrapping token key
2023-09-20T14:03:28.609Z [INFO]  core: successfully setup plugin catalog: plugin-directory=""
2023-09-20T14:03:28.613Z [INFO]  core: no mounts; adding default mount table
2023-09-20T14:03:28.629Z [INFO]  core: successfully mounted: type=cubbyhole version="v1.14.3+builtin.vault" path=cubbyhole/ namespace="ID: root. Path: "
2023-09-20T14:03:28.631Z [INFO]  core: successfully mounted: type=system version="v1.14.3+builtin.vault" path=sys/ namespace="ID: root. Path: "
2023-09-20T14:03:28.631Z [INFO]  core: successfully mounted: type=identity version="v1.14.3+builtin.vault" path=identity/ namespace="ID: root. Path: "
2023-09-20T14:03:28.686Z [INFO]  core: successfully mounted: type=token version="v1.14.3+builtin.vault" path=token/ namespace="ID: root. Path: "
2023-09-20T14:03:28.696Z [INFO]  rollback: starting rollback manager
2023-09-20T14:03:28.697Z [INFO]  core: restoring leases
2023-09-20T14:03:28.698Z [INFO]  expiration: lease restore complete
2023-09-20T14:03:28.713Z [INFO]  identity: entities restored
2023-09-20T14:03:28.714Z [INFO]  identity: groups restored
2023-09-20T14:03:28.720Z [INFO]  core: usage gauge collection is disabled
2023-09-20T14:03:28.733Z [INFO]  core: Recorded vault version: vault version=1.14.3 upgrade time="2023-09-20 14:03:28.720230178 +0000 UTC" build date=2023-09-11T21:23:55Z
2023-09-20T14:03:29.120Z [INFO]  core: post-unseal setup complete
2023-09-20T14:03:29.146Z [INFO]  core: root token generated
2023-09-20T14:03:29.146Z [INFO]  core: pre-seal teardown starting
2023-09-20T14:03:29.146Z [INFO]  rollback: stopping rollback manager
2023-09-20T14:03:29.146Z [INFO]  core: pre-seal teardown complete
```

你可以在這時檢視 ./vault/file 裡面的內容，./vault/file 在 `vault operator init` 前是空白的

```bash
ls -al ./vault/file
```
output，可以看到 ./vault/file 內已經初始化 filesystem storage backend 的內容

```bash
core
logical
sys
```

你可以檢視 ./vault/file/* 內的檔案內容，會發現內容都是 json 相容格式，而且都經過加密
- 在正常的條件下，沒有 unseal key 的人，是無法在有效時間內解鎖這些 filesystem 中的內容，內容還是受到保護
- 這並不代表你可以隨意放置 filesystem storage backend 的內容
  - 例如將他 commit 到 repository 中(vault-playground 已經添加 .gitignore)
- 請選擇安全，經過 vault 資安團隊測試過的 backend，來保障資料安全與可用程度

### Unseal

每個初始化的 Vault Server 都始於密封狀態。根據配置，Vault 可以訪問 storage backend，但它無法讀取其中的任何資料，因為它不知道如何解密它。教會 Vault 如何解密數據稱為解封(unseal) Vault。

每次 Vault 開始運行時都必須進行解封。可以通過 API 和命令行來執行解封操作。

要解封 Vault，你必須擁有解封金鑰的閾值數量(threshold)。在上面的輸出中，請注意 "key threshold" 是 3。這意味著要解封 Vault，你需要 5 個生成的金鑰中的 3 個。

注意

Vault 不存儲任何解封金鑰片段(key share)。Vault 使用一種稱為 Shamir's Secret Sharing 的算法來將 root encryption key 分成片段(share)。只有擁有threshold數量的金鑰，才能將其重建，最終訪問你的資料。

開始解封 Vault：

```bash
vault operator unseal
```
output

```bash
Unseal Key (will be hidden):

Key                Value
---                -----
Seal Type          shamir
Initialized        true
Sealed             true
Total Shares       5
Threshold          3
Unseal Progress    1/3
Unseal Nonce       9d03a4e0-bb4f-cfd5-326b-5afb55fdce53
Version            1.14.3
Build Date         2023-09-11T21:23:55Z
Storage Type       file
HA Enabled         false
```

繼續操作，輸入3/5把 unseal key 就可順利解封 storage backend

```bash
Unseal Key (will be hidden):

Key             Value
---             -----
Seal Type       shamir
Initialized     true
Sealed          false
Total Shares    5
Threshold       3
Version         1.14.3
Build Date      2023-09-11T21:23:55Z
Storage Type    file
Cluster Name    vault-cluster-f90273e8
Cluster ID      5ecc63c9-11eb-c384-355d-dffea2dd6484
HA Enabled      false
```

vault server log，成功解封後

```bash
2023-09-20T14:57:17.077Z [INFO]  core.cluster-listener.tcp: starting listener: listener_address=0.0.0.0:8201
2023-09-20T14:57:17.078Z [INFO]  core.cluster-listener: serving cluster requests: cluster_listen_address=[::]:8201
2023-09-20T14:57:17.089Z [INFO]  core: post-unseal setup starting
2023-09-20T14:57:17.115Z [INFO]  core: loaded wrapping token key
2023-09-20T14:57:17.115Z [INFO]  core: successfully setup plugin catalog: plugin-directory=""
2023-09-20T14:57:17.127Z [INFO]  core: successfully mounted: type=system version="v1.14.3+builtin.vault" path=sys/ namespace="ID: root. Path: "
2023-09-20T14:57:17.128Z [INFO]  core: successfully mounted: type=identity version="v1.14.3+builtin.vault" path=identity/ namespace="ID: root. Path: "
2023-09-20T14:57:17.128Z [INFO]  core: successfully mounted: type=cubbyhole version="v1.14.3+builtin.vault" path=cubbyhole/ namespace="ID: root. Path: "
2023-09-20T14:57:17.148Z [INFO]  core: successfully mounted: type=token version="v1.14.3+builtin.vault" path=token/ namespace="ID: root. Path: "
2023-09-20T14:57:17.154Z [INFO]  rollback: starting rollback manager
2023-09-20T14:57:17.154Z [INFO]  core: restoring leases
2023-09-20T14:57:17.156Z [INFO]  expiration: lease restore complete
2023-09-20T14:57:17.158Z [INFO]  identity: entities restored
2023-09-20T14:57:17.159Z [INFO]  identity: groups restored
2023-09-20T14:57:17.166Z [INFO]  core: usage gauge collection is disabled
2023-09-20T14:57:17.178Z [INFO]  core: post-unseal setup complete
2023-09-20T14:57:17.178Z [INFO]  core: vault is unsealed
```

### Hashicorp Vault docker

使用容器(container) 前需要查閱 image 的官方說明 [https://hub.docker.com/r/hashicorp/vault](https://hub.docker.com/r/hashicorp/vault)，幾件事情要注意

Base Image 是選擇使用 Alpine，比起其他 linux distributions 具有相對較小的安全風險，但功能足夠用於開發和測試。

Vault 始終在 dumb-init 下運行，將 process 與 SIG 傳遞給容器中運行的所有process。

使用的 Binary 由 HashiCorp 構建，並使用 GPG 金鑰簽名，因此你可以驗證Binary。

在不帶任何參數的情況下運行 Vault，容器將為你提供一個處於dev mode的 Vault Server。

容器公開了兩個可選的volume：

/vault/logs，用於寫入 audit log。預設情況下，這裡不會寫入任何內容；必須在Vault config 中啟用文件audit backend。

/vault/file，用於在使用資料storage plugin時，將資料寫入persistency。預設情況下，這裡不寫入任何內容（dev mode使用 in-memory storage）；在啟動容器之前，必須在 Vault 的配置中啟用文件 data storagebackend。

容器在 /vault/config 設置了一個 Vault 配置目錄，Server 將通過volume，載入這裡放置的任何 hcl 或 json config file。或者，也可以通過通過環境變數 `VAULT_LOCAL_CONFIG` 傳遞配置 json 來添加config。

### Vault configuration

如同前面說明，透過 `--volume ./config/:/vault/config.d` flag 將 ./config/vault.hcl 設定檔案掛載進容器中

你可以檢視目前的 vault server configuration，是以 vault.hcl 格式表示

```bash
cat ./config/vault.hcl
```

output，在這裡可以設置 vault server 的啟動參數
- 配置一個 listener "tcp"，監聽容器內 0.0.0.0:8200 進來的 request
- 由於 `docker run` 也設定 `-p 8200:8200` 將主機網路的 8200 port bind 到容器的 8200 port，讓我們可以在主機網路中存取 vault。

```bash
ui            = true
disable_mlock = true
api_addr      = "https://0.0.0.0:8200"

default_lease_ttl = "168h"
max_lease_ttl     = "720h"

storage "file" {
  path = "/vault/file"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = "true"
}
```

### 操作 Vault

Vault in Docker 使用起來與透過 binary 執行的 dev server 一樣。

你可以參照前幾天文章的內容，對 vault server 進行操做，也算是做個練習

```bash
vault login
vault secrets list
vault secrets enable -version=2 -path=chechia-net kv
```

在後面的內容，我們會用更有效率的方式管理，設定 vault

### 關閉 vault container

你可以使用以下指令關閉 vault容器

```bash
docker stop vault_1
```

output，server 接受到後會進行 docker 封鎖

```bash
==> Vault shutdown triggered
2023-09-20T13:06:28.627Z [INFO]  core: marked as sealed
2023-09-20T13:06:28.627Z [INFO]  core: pre-seal teardown starting
2023-09-20T13:06:28.627Z [INFO]  rollback: stopping rollback manager
2023-09-20T13:06:28.628Z [INFO]  core: pre-seal teardown complete
2023-09-20T13:06:28.628Z [INFO]  core: stopping cluster listeners
2023-09-20T13:06:28.628Z [INFO]  core.cluster-listener: forwarding rpc listeners stopped
2023-09-20T13:06:28.641Z [INFO]  core.cluster-listener: rpc listeners successfully shut down
2023-09-20T13:06:28.641Z [INFO]  core: cluster listeners successfully shut down
2023-09-20T13:06:28.641Z [INFO]  core: vault is sealed
```

如果有啟用 storage backend 的話，vault 資料或留存在 storage "file" 上，重啟不會如 dev server in-memory storage 一樣，被清空

### vault operator

你可以使用 vault operator 指令來做更多 vault cluster 相關的操作

```bash
vault operator -h
```

你可以使用下列指令產生新的 root token

```bash
vault operator generate-root -generate-otp
```
output

```bash
A One-Time-Password has been generated for you and is shown in the OTP field.
You will need this value to decode the resulting root token, so keep it safe.
Nonce         13ed8986-7b01-323c-0d06-2c32536fb8c1
Started       true
Progress      0/3
Complete      false
OTP           eYr...cMqx
OTP Length    28
```

vault server log 顯示開始產生 root

```bash
2023-09-20T15:12:08.633Z [INFO]  core: root generation initialized: nonce=13ed8986-7b01-323c-0d06-2c32536fb8c1
```

使用 -otp flag，並輸入 unseal key

```bash
vault operator generate-root -otp="..."
```

output

```bash
Operation nonce: 13ed8986-7b01-323c-0d06-2c32536fb8c1

Unseal Key (will be hidden):

Nonce       13ed8986-7b01-323c-0d06-2c32536fb8c1
Started     true
Progress    1/3
Complete    false
```

持續輸入 3/5 unseal keys，直到取得 encoded token

```bash
Operation nonce: 13ed8986-7b01-323c-0d06-2c32536fb8c1
Unseal Key (will be hidden):
Nonce            13ed8986-7b01-323c-0d06-2c32536fb8c1
Started          true
Progress         3/3
Complete         true
Encoded Token    DS8B...MdGw
```

使用 otp + encoded token 來進行 decode

```bash
vault operator generate-root \
  -decode="DS8B...MdGw" \
  -otp="eYr1...cMqx"
```

output

```bash
hvs.bDKG...Pnlc
```

vault server log 顯示逞生 root 完成

```bash
2023-09-20T15:15:40.541Z [INFO]  core: root generation finished: nonce=13ed8986-7b01-323c-0d06-2c32536fb8c1
```

NOTE: 第一把 init root token 還是有效，加上後來生成的第二把，現在有兩把常效期的 root token

### 清空

你可以刪除 ./vault/file/，完全清除 vault server 使用的 filesystem storage backend

```bash
rm -rf ./vault/file/*
```

vault server 本身幾乎是無狀態，清除 storage backend 後就什麼也不剩了

### chatGPT

本段部分內容使用 chatGPT-3.5 翻譯
https://developer.hashicorp.com/vault/tutorials/getting-started/getting-started-deploy
https://hub.docker.com/r/hashicorp/vault
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

