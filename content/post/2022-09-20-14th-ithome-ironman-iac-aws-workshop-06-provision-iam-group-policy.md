---
title: "14th Ithome Ironman Iac Aws Workshop 06 Provision Iam Group Policy" # Title of the blog post.
date: 2022-09-20T10:39:37+08:00 # Date of post creation.
description: "Article description." # Description used for search engine.
featured: true # Sets if post is a featured post, making appear on the home page side bar.
draft: false # Sets whether to render this page. Draft of true will not be rendered.
toc: false # Controls if a table of contents should be generated for first-level links automatically.
# menu: main
featureImage: "/images/path/file.jpg" # Sets featured image on blog post.
thumbnail: "/images/path/thumbnail.png" # Sets thumbnail image appearing inside card on homepage.
shareImage: "/images/path/share.png" # Designate a separate image for social media sharing.
codeMaxLines: 10 # Override global value for how many lines within a code block before auto-collapsing.
codeLineNumbers: false # Override global value for showing of line numbers within code block.
figurePositionShow: true # Override global value for showing the figure label.
categories:
  - terraform
tags:
  - terraform
  - iac
  - aws
---

昨天我們將 root account IAM user import 到 terraform 中
- 示範 terraform import
- 增加 iam user 的功能到 module repository 中

今天要完成 root account 中 IAM Group + Policy，順便聊聊 aws IAM policy 管理原則
- [x] root 中設定 IAM User
  - [x] 將手動產生的 Administrator 的 IAM User import terraform 中
  - [ ] 補上 root account IAM Policy
  - [ ] 補上 root account IAM Group

[iThome 鐵人賽好讀版](https://ithelp.ithome.com.tw/articles/10290931)

[賽後文章會整理放到個人的部落格上 http://chechia.net/](http://chechia.net/)

[追蹤粉專可以收到文章的主動推播](https://www.facebook.com/engineer.from.scratch)

![https://ithelp.ithome.com.tw/upload/images/20210901/20120327NvpHVr2QC0.jpg](https://ithelp.ithome.com.tw/upload/images/20210901/20120327NvpHVr2QC0.jpg)

---

承接昨天的 plan 結果，我們今天要把 IAM policy 與 group 開出來

### Iam User

首先 review `aws_iam_user` 的 resource
```
# module.iam_user["Administrator"].aws_iam_user.this[0] will be updated in-place
  ~ resource "aws_iam_user" "this" {
      + force_destroy = true
        id            = "Administrator"
        name          = "Administrator"
        tags          = {}
        # (4 unchanged attributes hidden)
    }`
```
`force_destroy` 這個參數我們需要嗎？可以一找以下的步驟查文件判斷
- 直接 google "terraform aws iam user"，找到 [Terraform registry 上 AWS iam user 的說明](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_user#force_destroy)
- 這裡有說明，刪除 user 時，如果有 non-terraform-managed 的 access key, login profile, MFA devices，是否仍要強制刪除
- 這裡我們希望如果有 access key 或 MFA device 存在的話，不要直接刪除 User
將 [https://github.com/chechiachang/terragrunt-infrastructure-modules/pull/1/files#diff-b15a741b1129d8f5451060653922d85c934792a1dd41c7fae1b02f3a6398094aR8](https://github.com/chechiachang/terragrunt-infrastructure-modules/pull/1/files#diff-b15a741b1129d8f5451060653922d85c934792a1dd41c7fae1b02f3a6398094aR8) 改成 false

### Iam Group & Policy

今天要來調整 Iam Group & Policy
- [Gruntwork 文件: Root Account 說明](https://docs.gruntwork.io/guides/build-it-yourself/landing-zone/production-grade-design/the-root-account)，root account 下應該有兩個 policy group
  - group/full-access 給予 root account 超級管理員完整的控制權限
  - billing 給予 billing 的會計人員進來報帳

首先 full-access 的 `iam_group` plan 後的結果如下
- 由於我們使用的 [module 是 terraform-aws-iam 的 group with policies](https://github.com/terraform-aws-modules/terraform-aws-iam/tree/master/modules/iam-group-with-policies) `module.iam_group_with_policies_full_access` 裡面有 group 也有 policy
- `.aws_iam_group.this[0]` 是主要的 group

```
  # module.iam_group_with_policies_full_access.aws_iam_group.this[0] will be created
  + resource "aws_iam_group" "this" {
      + arn       = (known after apply)
      + id        = (known after apply)
      + name      = "full-access"
      + path      = "/"
      + unique_id = (known after apply)
    }

  # module.iam_group_with_policies_full_access.aws_iam_group_membership.this[0] will be created
  + resource "aws_iam_group_membership" "this" {
      + group = (known after apply)
      + id    = (known after apply)
      + name  = "full-access"
      + users = [
          + "Administrator",
        ]
    }
```

有了 group，接下來就是要配 policy
- 一樣透過 group + policy -> attachment 的 resource，把 group 跟 policy 綁在一起
- [我們這邊的程式碼](https://github.com/chechiachang/terragrunt-infrastructure-modules/pull/1/files#diff-858c29afbd11c170c1b2d1f0368b50368ff0d056682ec1ddc51cd2014b04f275R22) 直接使用 aws 預先定義好的 policy `arn:aws:iam::aws:policy/AdministratorAccess`

```
  # module.iam_group_with_policies_full_access.aws_iam_group_policy_attachment.custom_arns[0] will be created
  + resource "aws_iam_group_policy_attachment" "custom_arns" {
      + group      = (known after apply)
      + id         = (known after apply)
      + policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
    }
```

### IAM AWS 預先定義的 policy

有哪些 aws 已經預先定義好的 policy 可以使用？
- 可以上 aws web console -> iam -> policies 下查詢

![AWS Web Console IAM Policies](https://ithelp.ithome.com.tw/upload/images/20220920/20120327I5BmCCMAky.png)

這些預先定義的 policy，是 aws 依照最常出現的使用情境，事先建立的 policy
- 使用者不用再建議
- ex. AWS 覺得 administrator 大概會需要這些權限，都先開到這個 policy/admin 上
- ex. AWS 覺得 billing 大概會需要這些權限，都先開到這個 policy/billing 上
- 由於是 AWS 依照大部分人的需求開的 policy，所以會多開許多權限
  - 這也是用預先定義 policy 的缺點，就是為了滿足很多人的需求，權限太大
  - 違反最小權限原則，給予權限過多也造成安全性的風險

不使用預先定義的 policy 的話，我們可以自己寫 policy
- 一個 policy 開出來 default 沒有任何 permission 
- 依據最小權限原則，一句一句增加 permission 到 policy 上
- 如此可以確保 policy 上的 permission 都是需要的，而不會有多開但是用不到的權限

權限愈大，安全性風險越高，所以最佳實踐會希望所有 policy 都是配得剛剛好夠用就好
- 然而配 policy 很花時間，用 aws 已經寫好的 policy 馬上可以用
- 實務上可以考量專案時間與整體人力，以及需要的安全等級，來考慮要不要做到這麼細

### AWS policy access advisor

通常寫 policy 很難配到非常完美剛剛好，通常都會多開 permission
- 權限多開功能不會壞，少開直接 permission denied
- 那多開的權限沒有用到，之後要如何把沒有用到的權限收回來？

AWS web console 提供根據使用紀錄，提建議修改 policy

[https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_access-advisor.html](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_access-advisor.html)

[aws 會統計各個 IAM 元件，存取 AWS API 使用/沒使用的權限](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_access-advisor-view-data.html)
- 例如這個 User 過去 90 天使用了哪些 permission 去打 API
- 以及 User 還有哪些 policy permission，是過去 90 天都沒有用到的 

這些長時間都沒有用到的 policy，我們就應該定期 review，然後移除這些不必要的權限
- User / Group / ... 等等都需要做一樣的事情

### module 作為一個組成元件使用

由於我們在 module input 中開啟了 `attach_iam_self_management_policy = true` 參數，在 module 中便連帶產生
- `.aws_iam_policy.iam_self_management[0]`，裡面定義的要做 self management 所需要的 permission
- 再把 policy 透過 `.aws_iam_group_policy_attachment.iam_self_management[0]` 綁到 group 上

```
  # module.iam_group_with_policies_full_access.aws_iam_policy.iam_self_management[0] will be created
  + resource "aws_iam_policy" "iam_self_management" {
    ...
    }

  # module.iam_group_with_policies_full_access.aws_iam_group_policy_attachment.iam_self_management[0] will be created
  + resource "aws_iam_group_policy_attachment" "iam_self_management" {
      + group      = (known after apply)
      + id         = (known after apply)
      + policy_arn = (known after apply)
    }
```

上面就是我們的 root account group/full-access 與對應的 policy

### billing account

接著是 root account group/full-access 與對應的 policy
- 我們可以自己手寫 policy，依照最小權限原則，一條一條加入 permission
- 或是我們可以上 aws web console 找看看有無預先定義好的 policy

![AWS Web Console IAM Policies: billing](https://ithelp.ithome.com.tw/upload/images/20220920/20120327nNp3eZnW9v.png)

![AWS Web Console IAM Policies: billing difference](https://ithelp.ithome.com.tw/upload/images/20220920/20120327nhmspwn04K.png)

我們搜尋 billing 有看到四個 policy，每個 policy 都有附上 description 說明使用的目的
- Billing
- AWSBillingConductorReadOnlyAccess
- AWSBillingConductorFullAccess
- AWSBillingReadOnlyAccess

這裡就要依據使用的需求選擇
- 給予 billing 管理員的權限，就會是 ConductorFullAccess 或 ConductorReadOnlyAccess
- 給予 billing 報帳人員，應該不用更改 aws 的其他設定，只需要讀取跟輸出，就會是 AWSBillingReadOnlyAccess

我們這邊選擇 AWSBillingConductorFullAccess，做個示範
- 點擊 AWSBillingConductorFullAccess，跳到 Policies >> AWSBillingConductorFullAccess 頁面
- 可以看到 policy 的完整 arn，Amazon Resource Name (ARN) 唯一識別AWS 資源，類似於 ID
- 然後把 arn 填入 [module.am_group_with_policies_billing](https://github.com/chechiachang/terragrunt-infrastructure-modules/pull/1/files#diff-858c29afbd11c170c1b2d1f0368b50368ff0d056682ec1ddc51cd2014b04f275R46)

![AWS Web Console IAM Policies: AWSBillingConductorFullAccess](https://ithelp.ithome.com.tw/upload/images/20220920/20120327PmO72VOmMV.png)

### plan & apply

上面的變更我們的 PR 如下
- [terragrunt-infrastructure-modules PR](https://github.com/chechiachang/terragrunt-infrastructure-modules/pull/2)
- [terragrunt-infrastructure-live-example PR](https://github.com/chechiachang/terragrunt-infrastructure-live-example/pull/2)

由於我們 module 中有新增 `module "iam_group_with_policies_billing"`，記得要先執行 init
```
aws-vault exec terraform-30day-root-iam-user --no-session  --  terragrunt plan

╷
│ Error: Module not installed
│
│   on group.tf line 29:
│   29: module "iam_group_with_policies_billing" {
│
│ This module is not yet installed. Run "terraform init" to install all
│ modules required by this configuration.
╵

aws-vault exec terraform-30day-root-iam-user --no-session  --  terragrunt init
aws-vault exec terraform-30day-root-iam-user --no-session  --  terragrunt plan

Terraform used the selected providers to generate the following execution
plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # module.iam_group_with_policies_billing.aws_iam_group.this[0] will be created
  + resource "aws_iam_group" "this" {
      + arn       = (known after apply)
      + id        = (known after apply)
      + name      = "billing"
      + path      = "/"
      + unique_id = (known after apply)
    }

  # module.iam_group_with_policies_billing.aws_iam_group_membership.this[0] will be created
  + resource "aws_iam_group_membership" "this" {
      + group = (known after apply)
      + id    = (known after apply)
      + name  = "billing"
      + users = [
          + "Accounting",
        ]
    }

  # module.iam_group_with_policies_billing.aws_iam_group_policy_attachment.custom_arns[0] will be created
  + resource "aws_iam_group_policy_attachment" "custom_arns" {
      + group      = (known after apply)
      + id         = (known after apply)
      + policy_arn = "arn:aws:iam::aws:policy/AWSBillingConductorFullAccess"
    }

  # module.iam_group_with_policies_billing.aws_iam_group_policy_attachment.iam_self_management[0] will be created
  + resource "aws_iam_group_policy_attachment" "iam_self_management" {
      + group      = (known after apply)
      + id         = (known after apply)
      + policy_arn = (known after apply)
    }

  # module.iam_group_with_policies_billing.aws_iam_policy.iam_self_management[0] will be created
  + resource "aws_iam_policy" "iam_self_management" {
      + arn         = (known after apply)
      + id          = (known after apply)
      + name        = (known after apply)
      + name_prefix = "IAMSelfManagement-"
      + path        = "/"
      + policy      = jsonencode(
            {
              + Statement = [
                  + {
                      + Action   = [
                          + "iam:UploadSigningCertificate",
                          + "iam:UploadSSHPublicKey",
                          + "iam:UpdateUser",
                          + "iam:UpdateLoginProfile",
                          + "iam:UpdateAccessKey",
                          + "iam:ResyncMFADevice",
                          + "iam:List*",
                          + "iam:Get*",
                          + "iam:GenerateServiceLastAccessedDetails",
                          + "iam:GenerateCredentialReport",
                          + "iam:EnableMFADevice",
                          + "iam:DeleteVirtualMFADevice",
                          + "iam:DeleteLoginProfile",
                          + "iam:DeleteAccessKey",
                          + "iam:CreateVirtualMFADevice",
                          + "iam:CreateLoginProfile",
                          + "iam:CreateAccessKey",
                          + "iam:ChangePassword",
                        ]
                      + Effect   = "Allow"
                      + Resource = [
                          + "arn:aws:iam::706136188012:user/*/${aws:username}",
                          + "arn:aws:iam::706136188012:user/${aws:username}",
                          + "arn:aws:iam::706136188012:mfa/${aws:username}",
                        ]
                      + Sid      = "AllowSelfManagement"
                    },
                  + {
                      + Action   = [
                          + "iam:List*",
                          + "iam:Get*",
                        ]
                      + Effect   = "Allow"
                      + Resource = "*"
                      + Sid      = "AllowIAMReadOnly"
                    },
                  + {
                      + Action    = "iam:DeactivateMFADevice"
                      + Condition = {
                          + Bool            = {
                              + "aws:MultiFactorAuthPresent" = "true"
                            }
                          + NumericLessThan = {
                              + "aws:MultiFactorAuthAge" = "3600"
                            }
                        }
                      + Effect    = "Allow"
                      + Resource  = [
                          + "arn:aws:iam::706136188012:user/*/${aws:username}",
                          + "arn:aws:iam::706136188012:user/${aws:username}",
                          + "arn:aws:iam::706136188012:mfa/${aws:username}",
                        ]
                      + Sid       = "AllowDeactivateMFADevice"
                    },
                ]
              + Version   = "2012-10-17"
            }
        )
      + policy_id   = (known after apply)
      + tags_all    = (known after apply)
    }

  # module.iam_group_with_policies_full_access.aws_iam_group.this[0] will be created
  + resource "aws_iam_group" "this" {
      + arn       = (known after apply)
      + id        = (known after apply)
      + name      = "full-access"
      + path      = "/"
      + unique_id = (known after apply)
    }

  # module.iam_group_with_policies_full_access.aws_iam_group_membership.this[0] will be created
  + resource "aws_iam_group_membership" "this" {
      + group = (known after apply)
      + id    = (known after apply)
      + name  = "full-access"
      + users = [
          + "Administrator",
        ]
    }

  # module.iam_group_with_policies_full_access.aws_iam_group_policy_attachment.custom_arns[0] will be created
  + resource "aws_iam_group_policy_attachment" "custom_arns" {
      + group      = (known after apply)
      + id         = (known after apply)
      + policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
    }

  # module.iam_group_with_policies_full_access.aws_iam_group_policy_attachment.iam_self_management[0] will be created
  + resource "aws_iam_group_policy_attachment" "iam_self_management" {
      + group      = (known after apply)
      + id         = (known after apply)
      + policy_arn = (known after apply)
    }

  # module.iam_group_with_policies_full_access.aws_iam_policy.iam_self_management[0] will be created
  + resource "aws_iam_policy" "iam_self_management" {
      + arn         = (known after apply)
      + id          = (known after apply)
      + name        = (known after apply)
      + name_prefix = "IAMSelfManagement-"
      + path        = "/"
      + policy      = jsonencode(
            {
              + Statement = [
                  + {
                      + Action   = [
                          + "iam:UploadSigningCertificate",
                          + "iam:UploadSSHPublicKey",
                          + "iam:UpdateUser",
                          + "iam:UpdateLoginProfile",
                          + "iam:UpdateAccessKey",
                          + "iam:ResyncMFADevice",
                          + "iam:List*",
                          + "iam:Get*",
                          + "iam:GenerateServiceLastAccessedDetails",
                          + "iam:GenerateCredentialReport",
                          + "iam:EnableMFADevice",
                          + "iam:DeleteVirtualMFADevice",
                          + "iam:DeleteLoginProfile",
                          + "iam:DeleteAccessKey",
                          + "iam:CreateVirtualMFADevice",
                          + "iam:CreateLoginProfile",
                          + "iam:CreateAccessKey",
                          + "iam:ChangePassword",
                        ]
                      + Effect   = "Allow"
                      + Resource = [
                          + "arn:aws:iam::706136188012:user/*/${aws:username}",
                          + "arn:aws:iam::706136188012:user/${aws:username}",
                          + "arn:aws:iam::706136188012:mfa/${aws:username}",
                        ]
                      + Sid      = "AllowSelfManagement"
                    },
                  + {
                      + Action   = [
                          + "iam:List*",
                          + "iam:Get*",
                        ]
                      + Effect   = "Allow"
                      + Resource = "*"
                      + Sid      = "AllowIAMReadOnly"
                    },
                  + {
                      + Action    = "iam:DeactivateMFADevice"
                      + Condition = {
                          + Bool            = {
                              + "aws:MultiFactorAuthPresent" = "true"
                            }
                          + NumericLessThan = {
                              + "aws:MultiFactorAuthAge" = "3600"
                            }
                        }
                      + Effect    = "Allow"
                      + Resource  = [
                          + "arn:aws:iam::706136188012:user/*/${aws:username}",
                          + "arn:aws:iam::706136188012:user/${aws:username}",
                          + "arn:aws:iam::706136188012:mfa/${aws:username}",
                        ]
                      + Sid       = "AllowDeactivateMFADevice"
                    },
                ]
              + Version   = "2012-10-17"
            }
        )
      + policy_id   = (known after apply)
      + tags_all    = (known after apply)
    }

  # module.iam_user["Accounting"].aws_iam_user.this[0] will be created
  + resource "aws_iam_user" "this" {
      + arn           = (known after apply)
      + force_destroy = false
      + id            = (known after apply)
      + name          = "Accounting"
      + path          = "/"
      + tags_all      = (known after apply)
      + unique_id     = (known after apply)
    }

Plan: 11 to add, 0 to change, 0 to destroy.

aws-vault exec terraform-30day-root-iam-user --no-session  --  terragrunt apply
```

眼尖的同學應該有注意到我們把 `create_login_profile = false` 先關掉
- 因為我們還沒有準備 pgp key，這個又要明天再來了

### TODO 與進度

- [x] 透過 root account 設定一組 IAM User
- [x] 透過 root account 設定多個 aws child accounts
- [x] root 中設定 IAM User
  - [x] 將手動產生的 Administrator 的 IAM User import terraform 中
  - [x] 補上 root account IAM Policy
  - [x] 補上 root account IAM Group
- [ ] security 中設定 IAM User
  - [ ] security 設定 password policy
  - [ ] security 設定 MFA policy
- [ ] security 中設定 IAM Policy & Group
- [ ] dev 中設定 IAM role
- [ ] 允許 security assume dev IAM role
