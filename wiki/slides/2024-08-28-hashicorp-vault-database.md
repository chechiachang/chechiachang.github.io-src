# Hashicorp: managed database credentials with Hashicorp Vault

- Source: `content/slides/2024-08-28-hashicorp-vault-database/_index.md`
- Slide: `https://chechia.net/slides/2024-08-28-hashicorp-vault-database/`
- Date: `2024-08-20T11:00:00Z`
- Tags: `kubernetes`
- Categories: `kubernetes`
- Description: `分享如何使用 Hashicorp Vault 管理資料庫的帳號密碼，並透過 AWS IAM Role 與 Kubernetes Service Account 進行驗證，以及如何連線到資料庫，監控與審查。`

## Pages (Section | Summary)

1. `(frontmatter)` | Frontmatter metadata for reveal-hugo settings and slide metadata.
2. `Vault: Managed Database Credentials` | Vault: Managed Database Credentials
3. `(frontmatter)` | About Me
4. `(frontmatter)` | 相關資源
5. `(frontmatter)` | 大綱
6. `(frontmatter)` | DB 帳號密碼管理的難題
7. `(frontmatter)` | Authentication 認證
8. `(frontmatter)` | User Story
9. `(frontmatter)` | 難題/認證
10. `(frontmatter)` | 難題/認證/密碼保管與暴露
11. `(frontmatter)` | 難題/認證/密碼暴露
12. `(frontmatter)` | Vault DB secret engine
13. `(frontmatter)` | Vault DB secret engine
14. `(frontmatter)` | Vault DB secret engine
15. `(frontmatter)` | User Story (v2)
16. `(frontmatter)` | Vault DB secret engine 支援，沒支援可以自己寫 plugin
17. `(frontmatter)` | Demo 1: Vault DB secret engine
18. `(frontmatter)` | Demo 1: Vault DB secret engine
19. `(frontmatter)` | Demo 1: Vault DB secret engine
20. `(frontmatter)` | Demo 1: Vault DB secret engine
21. `(frontmatter)` | 解決存放與取用，回到難題/認證
22. `(frontmatter)` | Vault 的解決方案
23. `(frontmatter)` | 難題/認證/Vault Auth method
24. `(frontmatter)` | 難題/認證/Vault Auth method/AWS
25. `(frontmatter)` | app 跑在 Ec2 上，使用 Ec2 做認證
26. `(frontmatter)` | app 跑在 Kubernetes 上，使用 Service Account 做認證
27. `(frontmatter)` | > 使用 Vault auth method，信任第三方取得身份
28. `(frontmatter)` | 有支援的 auth method，可以自己搭配
29. `(frontmatter)` | User Story (v3)
30. `(frontmatter)` | Demo 2: Auth method
31. `(frontmatter)` | Demo 2: Auth method
32. `(frontmatter)` | 難題/認證/Vault Auth method/Kubernetes
33. `(frontmatter)` | 難題/認證/Vault Auth method/小結
34. `(frontmatter)` | User Story (v?)
35. `(frontmatter)` | 難題/授權
36. `(frontmatter)` | 難題/授權/Scale up
37. `(frontmatter)` | 難題/授權/Scale up
38. `(frontmatter)` | 難題/授權/PR Review
39. `(frontmatter)` | 難題/授權/Automation
40. `(frontmatter)` | Demo 3: Terraform 設定 Vault 與 DB secret engine
41. `(frontmatter)` | Demo 3: Terraform 設定 Vault 與 DB secret engine
42. `(frontmatter)` | 總結
43. `Q&A` | Q&A

## Time-to-Syntax

- Markdown:
- `p2:link`
- `p3:link`
- `p4:link`
- `p12:image`
- `p12:link`
- `p13:image`
- `p13:link`
- `p14:link`
- `p16:image`
- `p17:code-fence`
- `p18:code-fence`
- `p19:code-fence`
- `p20:code-fence`
- `p22:image`
- `p25:image`
- `p25:link`
- `p26:image`
- `p26:link`
- `p28:image`
- `p28:link`
- `p30:code-fence`
- `p31:code-fence`
- `p32:link`
- `p35:code-fence`
- `p37:code-fence`
- `p38:link`
- `p39:code-fence`
- `p40:code-fence`
- Hugo shortcode:
- `p2:{{% note %}}`
- `p2:{{% /note %}}`
- `p5:{{% note %}}`
- `p5:{{% /note %}}`
- `p6:{{% note %}}`
- `p6:{{% /note %}}`
- `p7:{{% note %}}`
- `p7:{{% /note %}}`
- `p8:{{% note %}}`
- `p8:{{% /note %}}`
- `p9:{{% note %}}`
- `p9:{{% /note %}}`
- `p10:{{% note %}}`
- `p10:{{% /note %}}`
- `p11:{{% note %}}`
- `p11:{{% /note %}}`
- `p15:{{% note %}}`
- `p15:{{% /note %}}`
- `p21:{{% note %}}`
- `p21:{{% /note %}}`
- `p22:{{% note %}}`
- `p22:{{% /note %}}`
- `p23:{{% note %}}`
- `p23:{{% /note %}}`
- `p25:{{% note %}}`
- `p25:{{% /note %}}`
- `p26:{{% note %}}`
- `p26:{{% /note %}}`
- `p28:{{% note %}}`
- `p28:{{% /note %}}`
- `p29:{{% note %}}`
- `p29:{{% /note %}}`
- `p32:{{% note %}}`
- `p32:{{% /note %}}`
- `p33:{{% note %}}`
- `p33:{{% /note %}}`
- `p34:{{% note %}}`
- `p34:{{% /note %}}`
- `p36:{{% note %}}`
- `p36:{{% /note %}}`
- `p37:{{% note %}}`
- `p37:{{% /note %}}`
- `p38:{{% note %}}`
- `p38:{{% /note %}}`
- `p39:{{% note %}}`
- `p39:{{% /note %}}`
- `p41:{{% note %}}`
- `p41:{{% /note %}}`
- `p42:{{% note %}}`
- `p42:{{% /note %}}`
- Reveal-hugo syntax:
- none.

## Time-to-Sentence

- Markdown:
- `p1:title: "Hashicorp: managed database credentials with Hashicorp Vault"`
- `p1:description: "分享如何使用 Hashicorp Vault 管理資料庫的帳號密碼，並透過 AWS IAM Role 與 Kubernetes Service Account 進行驗證，以及如何連線到資料庫，監控與審查。"`
- `p5:Demo 2 github login and auth`
- `p5:Demo 3 terraform 設定 vault 與 DB secret engine`
- `p7:> you are who you say you are`
- `p7:> you are allowed to do what you are trying to do`
- `p8:DB > hi, app!`
- `p9:有帳號密碼是否就相信他是app？`
- `p9:有沒有賬號密碼以外的方式確認app的身份？`
- `p11:不要存放密碼，卻能使用密碼??`
- `p16:Vault DB secret engine 支援，沒支援可以自己寫 plugin`
- `p17:Demo 1: Vault DB secret engine`
- `p17:apk update && apk add mysql-client`
- `p17:mysql -h mariadb_1 -u root -p`
- `p18:Demo 1: Vault DB secret engine`
- `p18:// Configure secret engine database (terraform)`
- `p19:Demo 1: Vault DB secret engine`
- `p19:// root configure (already done by terraform)`
- `p19:// create token for dba (will automatically done in Demo 2)`
- `p19:vault token create -policy=dba -display-name=dba \`
- `p20:Demo 1: Vault DB secret engine`
- `p20:mysql --sql -h localhost -u <username> -p`
- `p20:...`
- `p21:有帳號密碼是否就相信他是app？`
- `p21:有沒有賬號密碼以外的方式確認app的身份？`
- `p23:aws / azure / gcp iam role / github / saml / LDAP ...`
- `p23:aws / azure / gcp iam role / github / saml`
- `p24:登入的 aws user / 合法的 iam role`
- `p24:核對正確，vault 提供短期 database credential 給 user / app`
- `p25:app 跑在 Ec2 上，使用 Ec2 做認證`
- `p25:如果你有使用 aws ec2，可以透過 aws api 來取得 iam role / ec2 metadata`
- `p25:aws login 比單純 mysql login 安全，因為多了更多認證檢查`
- `p25:access key / password / MFA`
- `p26:app 跑在 Kubernetes 上，使用 Service Account 做認證`
- `p28:aws/gcp/azure iam role, github, saml, LDAP`
- `p28:kubernetes api server (pod service account)`
- `p29:app < (identity) < trusted authority`
- `p29:app > (identity) > vault > trusted authority`
- `p29:app < (DB credential) < vault>`
- `p31:aws-vault exec dev -- vault login -method=aws -path=aws=sre`
- `p31:gcloud ... vault login -method=gcp -path=gcp=sre`
- `p31:az login ... vault login -method=azure -path=azure=sre`
- `p32:app > sa -> k8s api server -> vault -> DB`
- `p32:app 跑在 Pod，Pod 取得 k8s service account 短期 jwt token`
- `p32:app 透過 jwt token 給 vault 聲稱自己是 app`
- `p32:vault 使用 jwt token 與 k8s api server 核對 pod service account`
- `p32:k8s 核對成功，vault 認為 app 是 k8s 中的 app`
- `p34:app + admin + metabase 不同權限`
- `p34:需求會一直改變，目前管理方式有足夠的彈性去面對需求的改變嗎？`
- `p35:grant write on mydb.* to app@'%'`
- `p35:grant all on mydb.* to admin@'%'`
- `p35:grant read on mydb.* to metabase@'%'`
- `p35:grant all on mydb.* to myrole;`
- `p36:Scale up，100 個 user x 100 個 database`
- `p36:100 個 user，就要下 100 次 sql grant role`
- `p36:100 個 database，就要下 x100 次 sql grant role`
- `p37:privileges = each.value.privilleges // ["SELECT", "UPDATE"]`
- `p38:Terraform 有比較好嗎？`
- `p38:把 mysql admin username/password 放在雲端 ex. aws secret manager，透過 terraform 來取得帳號密碼`
- `p39:Or Vault + Terraform？`
- `p39:capabilities = ["create", "read", "update", "patch", "delete", "list"]`
- `p40:Demo 3: Terraform 設定 Vault 與 DB secret engine`
- `p41:Demo 3: Terraform 設定 Vault 與 DB secret engine`
- `p42:Github / AWS IAM Role / Kubernetes Service Account`
- Hugo shortcode:
- `p2:{{% note %}}`
- `p2:{{% /note %}}`
- `p5:{{% note %}}`
- `p5:{{% /note %}}`
- `p6:{{% note %}}`
- `p6:{{% /note %}}`
- `p7:{{% note %}}`
- `p7:{{% /note %}}`
- `p8:{{% note %}}`
- `p8:{{% /note %}}`
- `p9:{{% note %}}`
- `p9:{{% /note %}}`
- `p10:{{% note %}}`
- `p10:{{% /note %}}`
- `p11:{{% note %}}`
- `p11:{{% /note %}}`
- `p15:{{% note %}}`
- `p15:{{% /note %}}`
- `p21:{{% note %}}`
- `p21:{{% /note %}}`
- `p22:{{% note %}}`
- `p22:{{% /note %}}`
- `p23:{{% note %}}`
- `p23:{{% /note %}}`
- `p25:{{% note %}}`
- `p25:{{% /note %}}`
- `p26:{{% note %}}`
- `p26:{{% /note %}}`
- `p28:{{% note %}}`
- `p28:{{% /note %}}`
- `p29:{{% note %}}`
- `p29:{{% /note %}}`
- `p32:{{% note %}}`
- `p32:{{% /note %}}`
- `p33:{{% note %}}`
- `p33:{{% /note %}}`
- `p34:{{% note %}}`
- `p34:{{% /note %}}`
- `p36:{{% note %}}`
- `p36:{{% /note %}}`
- `p37:{{% note %}}`
- `p37:{{% /note %}}`
- `p38:{{% note %}}`
- `p38:{{% /note %}}`
- `p39:{{% note %}}`
- `p39:{{% /note %}}`
- `p41:{{% note %}}`
- `p41:{{% /note %}}`
- `p42:{{% note %}}`
- `p42:{{% /note %}}`
- Reveal-hugo syntax:
- none.
