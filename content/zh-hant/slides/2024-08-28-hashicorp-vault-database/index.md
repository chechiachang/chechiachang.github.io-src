---
title: "Hashicorp: managed database credentials with Hashicorp Vault"
summary: 分享如何使用 Hashicorp Vault 管理資料庫的帳號密碼，並透過 AWS IAM Role 與 Kubernetes Service Account 進行驗證，以及如何連線到資料庫，監控與審查。
authors: []
tags: ["kubernetes"]
categories: ["kubernetes"]
date: '2024-08-20T11:00:00Z'
slides:
  # Choose a theme from https://github.com/hakimel/reveal.js#theming
  #theme: black, sky, beige, simple, serif, blood, league, white, night, moon, solarized
  theme: sky
  # Choose a code highlighting style (if highlighting enabled in `params.toml`)
  #   Light style: github. Dark style: dracula (default).
  highlight_style: dracula
---

{{< slide background-image="onepiece.png" >}}

{{% speaker_note %}}
投影片跟講稿我都放在我的網站上，如果有興趣可以參考
{{% /speaker_note %}}

---

Vault: Managed Database Credentials

with Hashicorp Vault

[Che Chia Chang](https://chechia.net/)

{{% speaker_note %}}
{{% /speaker_note %}}

---

About Me

- Che Chia Chang
- SRE @ [Maicoin](https://www.linkedin.com/company/maicoin/jobs/)
- [Microsoft MVP](https://mvp.microsoft.com/zh-TW/MVP/profile/e407d0b9-5c01-eb11-a815-000d3a8ccaf5)
- [chechia.net](https://chechia.net/)

{{< figure src="mvp.png" height="20%" width="20%" title="" >}}

---

相關資源

- [Demo 範例程式碼 https://github.com/chechiachang/vault-playground](https://github.com/chechiachang/vault-playground) **Demo 用途，請充分理解後再使用**
- [今日投影片與講稿與其他資源 chechia.net](https://chechia.net/zh-hant/talk/hashicorp-managed-database-credentials-with-hashicorp-vault/)
- [2023 Vault 雲端的端通吃的私鑰管理平台](https://chechia.net/zh-hant/talk/hashicorp-vault-on-aws-k8s-%E9%9B%B2%E7%AB%AF%E5%9C%B0%E7%AB%AF%E9%80%9A%E5%90%83%E7%9A%84%E7%A7%81%E9%91%B0%E7%AE%A1%E7%90%86%E5%B9%B3%E5%8F%B0/)
- [從零開始學Terraform手把手入門](https://ithelp.ithome.com.tw/users/20120327/ironman/4057)

---

大綱

- DB 帳號密碼管理的難題
- Vault DB **secret engine**
- Demo 1 需要時自動產生資料庫帳號密碼
- Vault **auth method** 第三方認證身份
- Demo 2 github login and auth
- 程式化權限管理與稽查
- Demo 3 **terraform** 設定 vault 與 DB secret engine
- (看時間) monitoring / audit

{{% speaker_note %}}
{{% /speaker_note %}}

---

DB 帳號密碼管理的難題

- 認證(Authentication)
  - 密碼保管與暴露
- 授權(Authorization)
- 密碼更新

{{% speaker_note %}}
認證可以更好
授權可以更彈性方便
密碼更新可以更頻繁
密碼暴露風險可以被動控制

重要程度第一考量是資訊安全
第二是管理方便度，有沒有 utility 可以幫我們管理

底下透過一個 user story 來說明這些難題
{{% /speaker_note %}}

---

**Authentication 認證**

> you are who you say you are

**Authorization 授權**

> you are allowed to do what you are trying to do

{{% speaker_note %}}
名詞解釋
{{% /speaker_note %}}

---

User Story

- 一個app，為app設定了一個資料庫
- 資料庫存放app資料，只有app能存取資料
- 使用**帳號密碼**認證，app可以存取資料庫

**app(username=app, password) > DB**

**DB > hi, app!**

{{% speaker_note %}}
市面上有很多資料庫，都是使用帳號密碼來認證app的身份
產生第一個難題，就是帳號密碼的存放與管理
{{% /speaker_note %}}

---

難題/認證

對於資料庫來說，**username=app**的人，就是app

1. 有帳號密碼是否就相信他是app？
1. 有沒有賬號密碼以外的方式確認app的身份？

{{% speaker_note %}}
然而這跟我們的 user story 還是有落差
其中也隱藏資安風險
我們很習慣使用帳號密碼來認證身份，但是隨著時代演進，駭客有更多方法取得帳號密碼
{{% /speaker_note %}}

---

難題/認證/密碼保管與暴露

- dba 需要開發db，手上有admin帳號密碼
- 資安風險
  - 開發機器安裝惡意軟體/側錄密碼
  - 帳號密碼被竊取
  - 員工分開私人與公司電腦

{{% speaker_note %}}
駭客將開源的工具修改，增加後門，然後 release 給 admin
夠過社交工程，讓 admin 不知不覺安裝了惡意軟體
很開心拿來用，但是這個工具側錄了 admin 的帳號密碼
{{% /speaker_note %}}

---

難題/認證/密碼暴露

- 更嚴謹的身份確認，更難被破解
  - ex Client Certificate Authentication 
- 安全的存放密碼，避免密碼暴露
- 更好的做法
  - **不要存放密碼，卻能使用密碼??**
  - 放在 Vault 裡面

{{% speaker_note %}}

以往我們沒有更好的方式來確認app的身份，所以只能使用帳號密碼
針對密碼強度，現在有更好的方式來確認app的身份，例如 Client Certificate Authentication
提供更嚴謹的身份確認，現在許多資料庫都支援 tls，可以透過tls來確認app的身份
完整的認證，公正的 ca 簽發，certs 很難被暴力破解

我們要面對的是另外一層的風險，就是密碼暴露
就算你手上是有一個很強的密碼，但是你的開發機器被駭，密碼就被竊取了
dba 手上有存 admin 帳號密碼的
有用密碼管理器 1password ，有比較好，因為他幫你做加密與儲存，但也不能期待 1password 永不被駭
如果你手上的密碼重要程度非常高，高過密碼工具可以承擔的風險，那你就要考慮使用更安全的方式來管理密碼

有沒有可能 dba/sre 手上不要有帳號密碼，而是由內網的 vault 來管理帳號密碼
{{% /speaker_note %}}

---

[Vault DB secret engine](https://developer.hashicorp.com/vault/docs/secrets/databases)

{{< figure src="vault/secret-database-flow.png" height="90%" width="90%" title="" >}}

---

[Vault DB secret engine](https://developer.hashicorp.com/vault/docs/secrets/databases)

{{< figure src="https://www.datocms-assets.com/2885/1576778435-vault-db.png?fit=max&q=80&w=2000" height="90%" width="90%" title="" >}}

---

[Vault DB secret engine](https://developer.hashicorp.com/vault/docs/secrets/databases)

- 需要時自動產生DB使用者密碼
- 短效期使用者與密碼 ex 1hr
- 不延展自動到期，刪除使用者
- 未完成工作可以自動延展
- app可以一直取得新使用者與密碼

---

User Story (v2)

- 只有 vault 有 admin 密碼
- user 需要時，vault 動態產生**短效期使用者與密碼**
  - 效期到自動刪除
- 使用 vault library 程式化連線 db
  - 不在開發機器上存密碼
  - 不手動輸入密碼

{{% speaker_note %}}
{{% /speaker_note %}}

---

Vault DB secret engine 支援，沒支援可以自己寫 plugin

{{< figure src="vault/vault-secrets-databases.png" height="90%" width="90%" title="" >}}

---

Demo 1: Vault DB secret engine

Setup

```
git clone git@github.com:chechiachang/vault-playground.git
cd vault-playground/deploy/04-docker-and-db/
docker-compose up -d

docker ps

docker exec -it 04-docker-and-db-mariadb_1-1 bash

docker exec -it 04-docker-and-db-vault_1-1 sh
apk update && apk add mysql-client
mysql -h mariadb_1 -u root -p
```

---

Demo 1: Vault DB secret engine


```
// Connect to docker vault
export VAULT_ADDR=http://127.0.0.1:8200
vault status
vault login

vault secrets list

// Configure secret engine database (terraform)
vault secrets list
vault policy list

cd usage/03-terraform-lives
terragrunt init
terragrunt apply
```

---

Demo 1: Vault DB secret engine

Use database secret engine

```
// root configure (already done by terraform)
vault secrets list
vault list localhost_mariadb/config
vault read localhost_mariadb/config/localhost_mariadb 

vault list localhost_mariadb/roles
vault read localhost_mariadb/roles/database_admin

vault policy list
vault policy read dba

// create token for dba (will automatically done in Demo 2)
vault token create -policy=dba -display-name=dba -ttl=1h -use-limit=1
```

---

Demo 1: Vault DB secret engine


```
// auth as dba
vault login
vault policy list
vault read localhost_mariadb/creds/database_admin
mysql --sql -h localhost -u <username> -p

// do dba things
show databases;
select user from mysql.user;
...
exit
```

---

解決存放與取用，回到難題/認證

對於資料庫來說，**username=app**的人，就是app

1. 有帳號密碼是否就相信他是app？
1. 有沒有賬號密碼以外的方式確認app的身份？

{{% speaker_note %}}
{{% /speaker_note %}}

---

Vault 的解決方案

{{< figure src="vault/vault-identity-based-security.png" height="90%" width="90%" title="" >}}

{{% speaker_note %}}
{{% /speaker_note %}}

---

難題/認證/Vault **Auth method**

Vault 仰賴外部可信第三方(trusted authority)
- user/app 透過第三方動態取得合法的身份
- aws / azure / gcp iam role / github / saml / LDAP ...

開發機器上沒有密碼，就不會因為機器被駭/側錄，造成密碼洩漏

{{% speaker_note %}}
Vault 仰賴外部可信第三方(trusted authority)
把local開發機器被駭的風險，轉移到其他更安全的地方
aws / azure / gcp iam role / github / saml
內網的Vault
LDAP
{{% /speaker_note %}}

---

難題/認證/Vault Auth method/AWS

- IAM auth method
- EC2 auth method
  - 透過 AWS API 去確認身份
  - 登入的 aws user / 合法的 iam role
  - vault 透過 aws api 去核對身份
  - 核對正確，vault 提供短期 database credential 給 user / app

---

[app 跑在 Ec2 上，使用 Ec2 做認證](https://developer.hashicorp.com/vault/docs/auth/aws)
{{< figure src="aws-auth-method.png" height="90%" width="90%" title="" >}}

{{% speaker_note %}}

EC2 auth method
如果你有使用 aws ec2，可以透過 aws api 來取得 iam role / ec2 metadata

由於 database 本身的認證機制有限，我們可以透過 vault 來管理帳號密碼
將登入的資安管理交給更嚴謹的第三方

aws login 比單純 mysql login 安全，因為多了更多認證檢查
access key / password / MFA
ip 來源檢查
ratelimit
DDOS protection
有問題時會有 audit log

auth method 混搭
可以面對不同的資安風險
{{% /speaker_note %}}

---

[app 跑在 Kubernetes 上，使用 Service Account 做認證](https://www.hashicorp.com/blog/dynamic-database-credentials-with-vault-and-kubernetes)

{{< figure src="https://www.datocms-assets.com/2885/1578078487-screen-shot-2020-01-03-at-19-07-14.png?fit=max&q=80&w=2000" height="90%" width="90%" title="" >}}

{{% speaker_note %}}
{{% /speaker_note %}}

---

> 使用 Vault auth method，信任第三方取得身份
> 從雙方查核，變成三方查核

---

[有支援的 auth method，可以自己搭配](https://developer.hashicorp.com/vault/docs/auth)
{{< figure src="auth-methods.png" height="90%" width="90%" title="" >}}

{{% speaker_note %}}
- user auth method
  - aws/gcp/azure iam role, github, saml, LDAP
  - Login MFA
- app使用auth method認證
  - aws/gcp/azure iam role (ec2 role)
  - kubernetes api server (pod service account)
{{% /speaker_note %}}

---

User Story (v3)

- 只做一次：Vault 設定 DB secret engine
- user 本機不存放 DB 帳號密碼
- user/app 透過 Vault auth method
  - user aws iam role
  - app k8s service account
- user/app可以存取vault中的db帳號密碼

**app > trusted authority**

**app < (identity) < trusted authority**

**app > (identity) > vault > trusted authority**

**app < (DB credential) < vault**>

{{% speaker_note %}}
{{% /speaker_note %}}

---

Demo 2: Auth method

https://developer.hashicorp.com/vault/docs/auth/github

```
// root 
vault policy list
vault policy read sre

vault list auth/github-chechia-net/map/users
vault read auth/github-chechia-net/map/users/chechiachang
vault list auth/github-chechia-net/map/teams
vault read auth/github-chechia-net/map/teams/sre
vault auth help github-chechia-net

// user (github login)
vault login -method=github -path=github-chechia-net token=$TOKEN
vault read localhost_mariadb/creds/database_admin
```

---

Demo 2: Auth method

https://developer.hashicorp.com/vault/docs/auth/aws

```
// User login Public Cloud
aws-vault exec dev -- vault login -method=aws -path=aws=sre
gcloud ... vault login -method=gcp -path=gcp=sre
az login ... vault login -method=azure -path=azure=sre

// app login k8s
```

---

[難題/認證/Vault Auth method/Kubernetes](https://developer.hashicorp.com/vault/docs/auth/kubernetes)


**app > sa -> k8s api server -> vault -> DB**

- 使用 [k8s vault injector](https://developer.hashicorp.com/vault/docs/platform/k8s/injector)
- app 跑在 Pod，Pod 取得 k8s service account 短期 jwt token
- app 透過 jwt token 給 vault 聲稱自己是 app
  - vault 使用 jwt token 與 k8s api server 核對 pod service account
  - k8s 核對成功，vault 認為 app 是 k8s 中的 app
  - vault 提供短期 database credential 給 app
- app 使用短期 database credential 存取資料庫

{{% speaker_note %}}
{{% /speaker_note %}}

---

難題/認證/Vault Auth method/小結

- 本地存放 password 的風險
- 如果有公有雲，存放雲端服務
  - 通過檢驗且合規的安全系統
- 如果是地端，使用 vault 來管理帳號密碼
  - 存放 admin
  - 動態產生 db user

{{% speaker_note %}}
最容易被駭的，不是地端網路被打穿，而是 admin 的開發機器存放帳號密碼，被釣魚被側錄被竊取
用了很好的防火牆，但是 admin 的開發機器存放帳號密碼，或是 1password
{{% /speaker_note %}}

---

User Story (v?)

需求會一直改變

1. app 存取資料，變成
1. app + admin + metabase 不同權限

{{% speaker_note %}}
需求會一直改變，目前管理方式有足夠的彈性去面對需求的改變嗎？
{{% /speaker_note %}}

---

難題/授權

MySQL 為例，使用 sql 管理授權

user based access control

```sql
grant write on mydb.* to app@'%'
grant all on mydb.* to admin@'%'
grant read on mydb.* to metabase@'%'
```

role based access control

```sql
create role myrole;
grant all on mydb.* to myrole;
grant myrole to app@'%';
```

---

難題/授權/Scale up

- Scale up，100 個 user x 100 個 database
- 權限變更難 review
- 變更授權的admin user權力很大，如何存放管理

{{% speaker_note %}}
100 個 user，就要下 100 次 sql grant role
100 個 database，就要下 x100 次 sql grant role
有人離職再進來下 sql

{{% /speaker_note %}}

---

難題/授權/Scale up

```hcl
resource "mysql_role" "myrole" {
  for_each = var.roles

  name     = each.key
}

resource "mysql_grant" "developer" {
  for_each   = var.roles

  role       = each.key
  database   = each.value.database
  privileges = each.value.privilleges // ["SELECT", "UPDATE"]
}
```

{{% speaker_note %}}
SQL 也可以寫 loop，也可以寫 unit test
{{% /speaker_note %}}

---

難題/授權/PR Review

- Terraform 管理 MySQL 授權
- Terraform 有比較好嗎？
  - 程式化設定
  - Reviewable / Testable code
- 請見[從零開始學Terraform手把手入門](https://ithelp.ithome.com.tw/users/20120327/ironman/4057)

{{% speaker_note %}}
透過 terraform 來管理資料庫的授權，可以讓我們更方便的管理授權

把 mysql admin username/password 放在雲端 ex. aws secret manager，透過 terraform 來取得帳號密碼
{{% /speaker_note %}}


---

難題/授權/Automation

Vault 管理授權
- Or Vault + Terraform？

```
vault policy list

database_admin
database_readonly
database_write

vault policy read database_write
path "chechia-net-myapp/database/database" {
  capabilities = ["create", "read", "update", "patch", "delete", "list"]
}
```

{{% speaker_note %}}
很重要所以再說一次
如果你有用雲端服務，可以考慮使用雲端服務來管理帳號密碼
如果你是地端，可以考慮使用 vault 來管理帳號密碼
{{% /speaker_note %}}

---

Demo 3: Terraform 設定 Vault 與 DB secret engine

```
// destroy
cd vault-playground/usage/03-terraform-lives
terragrunt destroy

cd vault-playground/deploy/04-docker-and-db/
docker-compose down

// create new
docker-compose up -d
docker ps

cd vault-playground/usage/03-terraform-lives
terragrunt apply
```

---

Demo 3: Terraform 設定 Vault 與 DB secret engine

- 程式化權限控管
  - 一鍵設定環境
    - CI/CD 測試
      - fmt, lint, unit test
  - PR Review
- Automation plan，apply
  - 避免人工操作的失誤與風險
  - DBA 不用密碼或 login，因為根本不連 prod DB
  - incident 一鍵 roll back

{{% speaker_note %}}
sql 也都能做，也都有工具在做，只是語言的性質導致這件事好不好做
{{% /speaker_note %}}

---

總結

- Vault DB secret engine
  - 管理資料庫帳號密碼
  - 動態產生 db user 
- Vault auth method
  - 第三方認證身份
  - Github / AWS IAM Role / Kubernetes Service Account
- Vault + Terraform
  - 程式化權限控管
  - PR Review
  - Automation plan，apply

{{% speaker_note %}}
{{% /speaker_note %}}

---

### Q&A
