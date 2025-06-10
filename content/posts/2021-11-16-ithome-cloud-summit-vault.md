---
title: "2021 11 16 Ithome Cloud Summit Vault" # Title of the blog post.
date: 2021-11-16T01:04:12+08:00 # Date of post creation.
#description: "Article description." # Description used for search engine.
featured: true # Sets if post is a featured post, making appear on the home page side bar.
draft: false
toc: false # Controls if a table of contents should be generated for first-level links automatically.
# menu: main
#featureImage: "/images/path/file.jpg" # Sets featured image on blog post.
#thumbnail: "/images/path/thumbnail.png" # Sets thumbnail image appearing inside card on homepage.
#shareImage: "/images/path/share.png" # Designate a separate image for social media sharing.
#codeMaxLines: 10 # Override global value for how many lines within a code block before auto-collapsing.
#codeLineNumbers: false # Override global value for showing of line numbers within code block.
#figurePositionShow: true # Override global value for showing the figure label.
categories:
  - Technology
tags:
  - kubernetes
  - vault
  - terraform
---

各位好

關於這個 QRcode

每次上台前，我都會想要帶什麼樣的內容給觀眾，讓觀眾值得花 30 分鐘在底下聽。後來就習慣先發表一篇文章，把對觀眾有幫助的資源包成一包：
- 首先是完整投影片：https://slides.com/chechiac.../terraform-introduction-a56697
- 逐字講稿：(最後校稿中）
- 然而只有本次演講內容，回去可能還是不太容易操作。所以這次附上使用 Terraform 一鍵部署 vault 的 Github Repository：https://github.com/.../southe.../chechia_net/vault/singleton
- 如果不熟 Terraform，再附上 30 天手把手 Terraform 教學文章，只要願意花時間，全篇中文一個月帶你上手 Terraform。
  - IThome 鐵人賽好讀版：https://ithelp.ithome.com.tw/users/20120327/ironman/4057
  - Github Repository 完整版：https://github.com/.../terraform-30.../tree/main/lecture/zh
- 如果遇到問題還是需要找人發問，所以再推薦兩個社群，可以來這邊發問，要找我本人也找得到。甚至只是加入潛水不講話，都可以被動吸收許多新知。
  - Cloud Native Taiwan User Group
    - https://t.me/cntug
    - https://fb.cloudnative.tw
  - DevOps Taiwan Meetup Group
    - https://t.me/devopstw

大家可以手機拍完這個就出去吃午餐了。
或是拍回家，然後傳給一個同事叫他花 30 天把 Terraform 跟 Vault 這些都學會。

總之希望對各位有幫助，讓國內技術力能持續進步成長。

---

回到本次演講。

本次演講有三個關鍵字
- Kubernetes
- Vault
- Terraform 這個是隱藏的

請問平時工作會用到這三個技術之一的朋友，請舉個手，好讓我知道一下觀眾的分布，等等分享的內容會照比例做一些調整。

我們今天不會講太多 Kubernetes 的內容，重點放在 Vault，以及如何設定 Vault，所以 Terraform Infrastructure as Code 或是 configuration as Code 會在這邊跑出來。

---

關於我，我是哲嘉。我在 Maicoin 當 SRE。常出現的社群是 CNTUG 與 DevOpsTW。

---

我們今天談的更大的主題其實是 Key Management 私鑰管理，或是密碼管理。這是一個很大的題目，今天演講內容只是其中的一個實作案例。

---

舉個例子，一邊是 API Server，另一邊 Database，或是第三方服務

Database 來 Authenticate 合法的 Client 用戶端，可能是 username + password，或是 API Key + Secret，或是 Access Token，或是 Private Key，Client Certificate，都可以。

在跨不同平台或是介面的服務，我們常用的 Auth 方法。認 Key 不認人。

---

那中間這些 Key 要怎麼管理，就有很多學問
其中最基本的，是怎麼配置給 API Server 讓他使用
注意：讓 API Server 使用，隱含的意思是，其他人不管是其他微服務，或是開發工程師，閒雜人等都不能看到。

---

這邊我們假設 API Server 是在 Kubernetes 裡面跑，微服務架構，所以 API Server 可能是一個 Pod，我們 SRE 要為這組 Pod 配置密碼。

這邊列出的應該是 K8s 比較常見的幾種做法。
- plain text，直接寫進 file 讓 Pod 去讀取
- k8s secret 做 base64 encode
- 安全一點的透過外部機制作加密解密
- 或是寫在 API Server 的 memory 中

事實上如果沒有使用 K8s，使用 VM 或是公有雲 Container Service，應該都是類似的原理，大家都是 Linux base，secret 放進來看要放在 disk 或是 memory 裏面。

---

實際放到 K8s 大概會長長這些 yaml

最簡單，就直接把 secret 壓到 Pod env 裏面，

最簡單也最危險
- 所有看得到 yaml 的人都明碼看見密碼
- 所有能進到 file system

提外話

API Server 被從正面打穿，滲透到拿到這組密碼的機會多高？
- 如果 API Server golang library 有在跟安全性更新
- Kubernetes 用公有雲的 Kubernetes Service，有在更新
- OS ami 跟 docker image 都有在更新
- 然後有功能正常的防火牆

打掛蠻有可能的，但打穿服務到拿到密碼，是有難度的。

更多時候，至少在幣圈有被爆出來的資安事件，大多是是公司員工被釣魚信掉到，被植入惡意軟體在 local 電腦，然後他又看得到明碼的密碼，直接爆炸。

明碼糟糕的地方，大家都看得到，一開始就是 exposed 的狀態，風險不可控，也無從管制。

---

然後是 K8s secret，也是從 env 掛進去 Pod

---

放在 k8s secret，是 base64 的格式

看起來跟原先內容不一樣了，有人就跟我說，他們家的 k8s secret 有用 base64 加密。

encode 跟 encrypt

---

k8s secret 有什麼問題
- 明碼 plain text 的問題，不該看到的人很容易就看到
- 根本的問題還是 RBAC 懶得設定，大家都用 default role 進來

要用可以，先看 k8s secret 後面的儲存實作是什麼？
- 是 k8s etcd
- 透過 k8s API server 存取

etcd 跟 kube-api 一般來說是夠安全的。官方文件還建議
- secret 要加密 encrypt
- 增強 RBAC 控制，只有特定 role 才看得到 secret，，而不是每個人都用 default role 近來 k8s，然後進到 namespace 全部 secret 就看光光

RBAC 有設定好，有加密，是可以做到安全。當然還是沒有專門 key Management 工具，如 Vault 有額外管理上的優化功能。

加密範例可以看強者我朋友的文章

---

加密完可能長這樣，還要額外透過其他機制才能進行解密，拿到原始資料
- 例如透過 k8s controller 解密
- 或是透過 vault server
- 或是透過公有雲的 Key Management Service 做解密

---

其他的 k8s secret 加密解決方案

---

今天我們使用 Vault，其中一個目的就是要坐中間這段 Safe Magic
- 給這個 Pod secret
- 然後只給這個 Pod Secret

---

當然 Key Management 其他還有一堆事情要處理

- 密碼洩漏的話有沒有 revoke 機制
- 能不能定時 Rotate 汰換密碼？

- 改架構，底下的設定好不好耕著動態調整，還是要跟著 rename / mv k8s secret

- 怎麼做稽核，怎麼檢查內容。我看不到 vault 幫我看一下內容對不對，這個很容易發生。

臆想頭就很痛

---

今天的目的很單純
- 密碼的露出盡量小
- 最好密碼是有期限的，逾期自動失效
- 暴露了可以 revoke

---

Vault

有人用過？這邊簡介一下

---

在 CNCF 的 landscape 漱渝 Key Management，應該是裡面市佔最高的開源項目

---

重點就是保護與管理 secret

---

Vault 的核心概念，這個影片是 Hashicorp 官方介紹的影片，講得很好，大家自己回去看一下

---

這邊簡單 vault 101

現在有一台 vault server 已經設定好了，我們可以使用 vault client 連線

例如這邊
- 使用 VAULT TOKEN 告訴 vault 你是什麼身份的用戶
- 或是進行 login，Vault 會呸發一組臨時的 TOKEN 給你

拿著組 TOKEN 去問 Vault，請問我可以要 /user/mysql 這個路徑下的資料嗎？

Vault 檢查 TOKEN 的 role 與 permission，可以就回傳值
不行就 permission denied

Vault 就是金庫，真正重要的 key 存在裡面，使用這要來問 Vault，要先過 Vault 這關

---

Vault 實際存放 Secret Engine，這邊也跳過，大家先把他當 key / value 存放好了 XD

---

等等，這樣 vault Auth 有點怪

本來拿 username / password 去控制 Mysql
先在多一步，先拿到 VAULT TOKEN，再拿 TOKEN 去跟 Vault 拿 Mysql password，再去連 MySQL

咦這樣不是很怪？我如果 Vault token 暴露了，有心人士還是可以從 vault 拿到資料啊

這樣有比較安全嗎？還是只是花式被駭

對，只是做 token 交換的話，還是不夠，所以 Vault 有提供許多 Auth method
- token 只是其中一種
- 有很多認證方法不用 token 交換，但也能讓 vault 認得 k8s pod 與 api server

這是今天的重點之一，token / 密碼傳遞不安全，那就用其他手段 auth

---

以 AWS IAM auth 為例

如果今天是在 aws ec2 上跑，那可以透過 aws internal api 去取得身份認證資料，也就是 ec2 instance metadata

拿這個 metadata 去問 vault，vault 再透過 aws api 去確認，這個 ec2 instance 真的是合法的

然後依據 ec2 instance 身份，配發權限跟資料
- api server ec2 就給 api server secret
- frontend server ec2 就給 frontend secret

中間沒有多餘的密碼 / token 交換

---

來往的對話大概是這樣

- AWS API 是可信的
- Vault 自己維護是可信的
- 服務透過三方交握去認證，認 runtime 環境的 metadata，不再是認 key 不認人

---

至於 api server ec2 近來 vault 後，應該有什麼樣的權限，在 vault 內部透過 policy 配置
- 設定 path
- 設定允許的 operation 例如 read write list delete ... 等

runtime 動態調整

---

當然 Vault 還有提供很多更加安全的功能
- 例如如何安全地存放 secret

Storage 這邊跳過

---

Secret + auth 搭配跳過

---

以及 dynamic secret，來解認 key 不認人的問題

例如 mysql 的靜態 username / password，透過 vault 設定可以變成動態的

---

回到 k8s，使用 token auth，然後把 VAULT TOKEN 放在 k8s secret 裏面，只有比較安全一點點

就是 VAULT TOKEN 可以快速 rotate 跟 revoke

這邊可以搭配其他 auth 方式來解決

---

剛剛不是讓 vault 去認 aws ec2？

在 k8s 中，可以讓 vault 去認 k8s cluster / service account

---

路徑圖長這樣

- pod runtime 都會有 service account
- 使用 service account 的 metadata 去問 vault
- vault 去問 k8s，這個 service account 是真的假的
- k8s 回答 vault，Pod 跟service account 是合法的
- vault 再配權限給 Pod

---

auth detail 的文字描述，跟上面講的一樣

---

配合 k8s sidecar，可以把 vault 拿到的 key 寫到 memory mount 裏面
- Pod init 時 init container 才去 invoke vault API
- key 不會透過 k8s api 傳遞，也不會在 etcd 內出現
- main container 透過 memory mount 存取 key
- key 的 lifecycle 跟 pod 一樣， pod delete 掉這組 in-memory key 也自動清除

---

好處
- 更少 expose，沒有過 kube-api 與 etcd
- in-memory 
- vault 跟 pod 之間的 vault token 的 time-to-live 期限可以很短，幾十秒內，init 完即可拋棄的 token

---

壞處（？）
- 每個 pod 起來會去打 vault api
  - 實務經驗上 loading 很低
  - 而且 vault server 可以做 HA 跟 horizontal scaling
- 最大的成本，其實是 vault 設定
  - 讓 vault 認 k8s
  - 根據 service account 去配權限
  - 其他花俏功能都需要額外的設定
  - 系統複雜，保證配到你頭昏眼花

---

想像一下，這張圖里的
- policy 跟為服務數量呈正比
- secret path 也耕服務數量呈正比
- auth k8s 數量也跟服務數量呈正相關
- 用越久，內容隨時間增加
- 改架構時更刺激

---

建議使用 vault 務必 搭配 Terraform 管理
- infrastructure as code
- configuration as code
- policy as code

Terraform 非常適合管理複雜，但有常常需要細部調整的設定資料

---

其他功能，跳過

---

其他功能

---

secret debug 超麻煩
- 內容正確性，valid key 還是 invalid key，還是根本是另一隻 key
- 權限正確性，是不是這個 username / password 的權限是正確的
- 跨團隊溝通更頭痛，不是可以貼在 slack 大家一起幫看的東西

---

terraform 可以幫助 vault 設定 debug
- 至少跨環境復現問題很方邊

---

Vault 有 HA

---

Vault Performance 通常不是問題
- 雖然 loading 隨 micro service 線性增加
- 但本身可以是無狀態 server，可以 horizontal scale

---

注意一下 auto-retry
- pod fail restart 又再 init 一次，如果一萬個 pod 一直 retry 可能真的會把 vault 打爆
- backup limit 要注意
- 使用 init container 的話，是 cache 在 Pod 層級，container fail restart 不會重新打 vault api

---

安全性
- vault 有專業資安團隊把關
- 不要怕 vault 被打穿，而是要怕同事被釣魚

---

結論

---

要不要 vault

---

qrcode 最後機會

---

有問題可以來社群找我

---

Maicoin 是間好公司 2014 服務上線到現在，在台灣已經邁入第八年。顧客數一直增加，我們也持續緩慢擴編。

覺得自己有能力，歡迎來挑戰，等等私下找我聊

---

謝謝

---

Q & A

Terraform vs Pulumi
- 操作語言差異，有好有壞
- vault 跟 terraform 的 hcl 是增強版 json，本質還是 json，有興趣可以去看我的文章
- terraform 目前是站跟星星還是領先，未來繼續看

Kubernetes Service account token 要不要更新
- 要，應該定期更新，官方文件有操作步驟

Vault / Terraform 實務上的工作負擔會很花時間跟人力嗎
- 學習曲線比較奇怪，要花一點時間做中學
- 學熟了之後就很好改，效率很高
- 至少是屌打用 gui 改或是 client 直接下 cmd 拉
