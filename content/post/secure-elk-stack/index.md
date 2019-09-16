---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Secure Elk Stack"
subtitle: "Secure ELK stack"
summary: "Secure ELK stack"
authors: []
tags: ["elk", "tls", "xpack", "kubernetes"]
categories: []
date: 2019-09-15T23:00:33+08:00
lastmod: 2019-09-15T23:00:33+08:00
featured: false
draft: true

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
---

[2020 It邦幫忙鐵人賽](https://ithelp.ithome.com.tw/2020ironman) 系列文章

* [Self-host ELK stack on GCP]({{< ref "/post/self-host-elk-stack-on-gcp" >}})
* [Secure ELK Stask]({{< ref "/post/secure-elk-stack" >}})
* 監測 Google Compute Engine 上服務的各項數據
* 監測 Google Kubernetes Engine 的各項數據
* 使用 logstash pipeline 做數據前處理
* Elasticsearch 日常維護：數據清理，效能調校，永久儲存
* Debug ELK stack on GCP

對我的文章有興趣，歡迎到我的網站上 [https://chechiachang.github.io](https://chechiachang.github.io) 閱讀其他技術文章，有任何謬誤也請各方大德直接聯繫我，感激不盡。

--

上篇[Self-host ELK stack on GCP]({{< ref "/post/self-host-elk-stack-on-gcp" >}}) 介紹了，elk stack 基本的安裝，安裝完獲得一個只支援 http (裸奔)的 elk stack，沒有 https 在公開網路上使用是非常危險的。這篇要來介紹如何做安全性設定。

[官方的文件在這裡](https://www.elastic.co/guide/en/elastic-stack-overview/7.3/elasticsearch-security.html)，碎念一下，除非對 ELK 的功能有一定了解，不然這份真的不是很友善。建議從底下的[Tutorial: Getting started with security](https://www.elastic.co/guide/en/elastic-stack-overview/7.3/security-getting-started.html) 開始，過程比較不會這麼血尿。

總之為了啟用 authentication & https，這篇要做的事情：

- enable x-pack & activate basic license
- Generate self-signed ca & certificates
- Configure Elasticsearch, Kibana, & other components

---

# 啟用 X-pack

Elasticsearch 的安全性模組由 x-pack extension 提供，在 [6.3.0 之後的版本](https://www.elastic.co/what-is/open-x-pack)，安裝 elasticsearch 的過程中就預設安裝 x-pack。

附上[啟用的官方文件](https://www.elastic.co/guide/en/elastic-stack-overview/7.3/get-started-enable-security.html)


然而，由於舊版的 x-pack 是付費內容，目前的 elasticsearch 安裝完後，elasticsearch.yml 設定預設不啟用 x-pack，也就是說沒看到這篇官方文件的話，很容易就獲得沒有任何 security 功能的 ELK。

雖然目前已經可以使用免費的 basic license 使用 security 功能，還是希望官方可以 default 啟用 security。

```
$ sudo vim /etc/elasticsearch/elasticsearch.yml

xpack.security.enabled: true

xpack.license.self_generated.type: basic

discovery.type: single-node
```

我們這邊啟用 xpack.security，同時將 self-generated license 生出來，我們這邊只使用基本的 basic subscription。若希望啟用更多功能，可以看[官方subcription 方案介紹](https://www.elastic.co/cn/subscriptions)

另外，如果不同時設定為 single-node 的話，預設會尋找其他elasticsearch node 來組成 cluster，而我們就必須要在所有 node 上啟用 security，這篇只帶大家做一個 single node cluster，簡化步驟。

重啟 elasticsearch ，檢查 log，看啟動時有沒有載入 x-pack
```
sudo systemctl restart elasticsearch

$ tail -f /var/log/elasticsearch/elasticsearch.log

[2019-09-16T07:39:49,467][INFO ][o.e.e.NodeEnvironment    ] [elk] using [1] data paths, mounts [[/mnt/disks/elk (/dev/sdb)]], net usable_space [423.6gb], net total_space [491.1gb], types [ext4]
[2019-09-16T07:39:49,474][INFO ][o.e.e.NodeEnvironment    ] [elk] heap size [3.9gb], compressed ordinary object pointers [true]
[2019-09-16T07:39:50,858][INFO ][o.e.n.Node               ] [elk] node name [elk], node ID [pC22j9D4R6uiCM7oTc1Fiw], cluster name [elasticsearch]
[2019-09-16T07:39:50,866][INFO ][o.e.n.Node               ] [elk] version[7.3.1], pid[17189], build[default/deb/4749ba6/2019-08-19T20:19:25.651794Z], OS[Linux/4.15.0-1040-gcp/amd64], JVM[Oracle Corporation/OpenJDK 64-Bit Server VM/12.0.2/12.0.2+10]
[2019-09-16T07:39:50,878][INFO ][o.e.n.Node               ] [elk] JVM home [/usr/share/elasticsearch/jdk]
...
[2019-09-16T07:39:59,108][INFO ][o.e.p.PluginsService     ] [elk] loaded module [x-pack-ccr]
[2019-09-16T07:39:59,109][INFO ][o.e.p.PluginsService     ] [elk] loaded module [x-pack-core]
...
[2019-09-16T07:39:59,111][INFO ][o.e.p.PluginsService     ] [elk] loaded module [x-pack-logstash]
[2019-09-16T07:39:59,113][INFO ][o.e.p.PluginsService     ] [elk] loaded module [x-pack-voting-only-node]
[2019-09-16T07:39:59,114][INFO ][o.e.p.PluginsService     ] [elk] loaded module [x-pack-watcher]
[2019-09-16T07:39:59,115][INFO ][o.e.p.PluginsService     ] [elk] no plugins loaded
[2019-09-16T07:40:07,964][INFO ][o.e.x.s.a.s.FileRolesStore] [elk] parsed [0] roles from file [/etc/elasticsearch/roles.yml]
[2019-09-16T07:40:10,369][INFO ][o.e.x.m.p.l.CppLogMessageHandler] [elk] [controller/17314] [Main.cc@110] controller (64 bit): Version 7.3.1 (Build 1d93901e09ef43) Copyright (c) 2019 Elasticsearch BV
[2019-09-16T07:40:11,776][DEBUG][o.e.a.ActionModule       ] [elk] Using REST wrapper from plugin org.elasticsearch.xpack.security.Security
[2019-09-16T07:40:14,396][INFO ][o.e.d.DiscoveryModule    ] [elk] using discovery type [single-node] and seed hosts providers [settings]
[2019-09-16T07:40:16,222][INFO ][o.e.n.Node               ] [elk] initialized
[2019-09-16T07:40:16,224][INFO ][o.e.n.Node               ] [elk] starting ...
[2019-09-16T07:40:16,821][INFO ][o.e.t.TransportService   ] [elk] publish_address {10.140.0.10:9300}, bound_addresses {[::]:9300}
[2019-09-16T07:40:16,872][INFO ][o.e.c.c.Coordinator      ] [elk] cluster UUID [1CB6_Lt-TUWEmRoN9SE49w]
[2019-09-16T07:40:17,088][INFO ][o.e.c.s.MasterService    ] [elk] elected-as-master ([1] nodes joined)[{elk}{pC22j9D4R6uiCM7oTc1Fiw}{Os-2FBjgSTOd1G_I3QYwVQ}{10.140.0.10}{10.140.0.10:9300}{dim}{ml.machine_memory=7836028928, xpack.installed=true, ml.max_open_jobs=20} elect leader, _BECOME_MASTER_TASK_, _FINISH_ELECTION_], term: 9, version: 921, reason: master node changed {previous [], current [{elk}{pC22j9D4R6uiCM7oTc1Fiw}{Os-2FBjgSTOd1G_I3QYwVQ}{10.140.0.10}{10.140.0.10:9300}{dim}{ml.machine_memory=7836028928, xpack.installed=true, ml.max_open_jobs=20}]}
[2019-09-16T07:40:17,819][INFO ][o.e.c.s.ClusterApplierService] [elk] master node changed {previous [], current [{elk}{pC22j9D4R6uiCM7oTc1Fiw}{Os-2FBjgSTOd1G_I3QYwVQ}{10.140.0.10}{10.140.0.10:9300}{dim}{ml.machine_memory=7836028928, xpack.installed=true, ml.max_open_jobs=20}]}, term: 9, version: 921, reason: Publication{term=9, version=921}
[2019-09-16T07:40:17,974][INFO ][o.e.h.AbstractHttpServerTransport] [elk] publish_address {10.140.0.10:9200}, bound_addresses {[::]:9200}
[2019-09-16T07:40:17,975][INFO ][o.e.n.Node               ] [elk] started
[2019-09-16T07:40:18,455][INFO ][o.e.c.s.ClusterSettings  ] [elk] updating [xpack.monitoring.collection.enabled] from [false] to [true]
[2019-09-16T07:40:22,555][INFO ][o.e.l.LicenseService     ] [elk] license [************************************] mode [basic] - valid
[2019-09-16T07:40:22,557][INFO ][o.e.x.s.s.SecurityStatusChangeListener] [elk] Active license is now [BASIC]; Security is enabled
```

# Enable user authentication

啟用 security 之前，我們直接連入 Kibana http://10.140.0.10:5601 ，不用任何使用者登入，便可以完整使用 Kibana 功能（包含 admin 管理介面）。

啟用 security 後，便需要使用帳號密碼登入。在這邊先用工具把使用者密碼產生出來。

```
# 互動式
/usr/share/elasticsearch/bin/elasticsearch-setup-passwords interactive

# 自動產生
/usr/share/elasticsearch/bin/elasticsearch-setup-passwords auto
```

密碼生出來後，就把帳號密碼收好，等等會用到。之後初次登入也是使用這些密碼。

# Configure passwords on client-side

由於已經啟用 authentication，其他 ELK 元件 (Kibana, logstash, filebeat, apm-server,...) 連入 Elasticsearch 也都會需要各自的帳號密碼驗證。

以 Kibana 為例，可以直接在 kibana.yml 中直接設定帳號密碼
```
$ sudo vim /etc/kibana/kibana.yml

elasticsearch.hosts: ["http://localhost:9200"]
xpack.security.enabled: true

elasticsearch.username: "kibana"
elasticsearch.password: "***********"
```

當然，這邊就是明碼的，看了不太安全。

或是使用 keystore 把 built-in user 的密碼加密，存在 kibana 的 keystore 裡面，重啟 kibana 時便會載入。

```
/usr/share/kibana/bin/kibana-keystore create
/usr/share/kibana/bin/kibana-keystore add elasticsearch.username
/usr/share/kibana/bin/kibana-keystore add elasticsearch.password
```

如果有啟用 Filebeat 功能，beat 元件連入 elasticsearch 一樣需要設定

```
/usr/share/apm-server/bin/filebeat keystore create
/usr/share/apm-server/bin/filebeat add elasticsearch.username
/usr/share/apm-server/bin/filebeat add elasticsearch.password
```

如果有啟用 application performance monitoring(APM) 功能，apm-server 元件連入 elasticsearch 一樣需要設定

```
/usr/share/apm-server/bin/apm-server keystore create
/usr/share/apm-server/bin/apm-server add elasticsearch.username
/usr/share/apm-server/bin/apm-server add elasticsearch.password
```

---

# Encrypting Communications

上面加了 authentication，但如果沒 https/tls 基本上還是裸奔。接下來要處理連線加密。

[官方 tutorial](https://www.elastic.co/guide/en/elastic-stack-overview/7.3/encrypting-internode-communications.html)

# Generate certificates

先把 X.509 digital certificate 的 certificate authority(CA) 生出來，由於生出來的 .p12 檔案格式，裡頭除了憑證(public cerficiate)以外還包含私鑰，我們可以設定密碼保護這個檔案

```
mkdir -p /etc/elasticsearch/config

# CA generated with Elastic tool
/usr/share/elasticsearch/bin/elasticsearch-certutil ca \
  -out /etc/elasticsearch/config/elastic-stack-ca.p12
```

生出來是 PKCS#12 格式，包含：

* CA 的 public certificate
* CA 的基本資訊
* 簽署 certificates 使用的私鑰(private key)

附帶說明，X.509 有多種檔案格式

* .pem
* .cer, .crt, .der
* .p12
* .p7b, .p7c
* ...

另外檔案格式可以有其他用途，也就是說裡面裝的不一定是 X.509 憑證

ELK 設定的過程中，由於不是所有的 ELK component 都支援使用 .p12 檔案，我們在設定過程中會互相專換，或是混用多種檔案格式。

# 簡單講一下 certificate

* X.509 是公鑰憑證(public key certificate) 的一套標準，用在很多網路通訊協定 (包含 TLS/SSL)
* certificate 包含公鑰及識別資訊(hostname, organization, ...等資訊)
* certificate 是由 certificate authority(CA) 簽署，或是自簽(Self-signed)
* 客戶端檢查(ex. browser, ELK components...) certifciate 是否由合法機構簽署
  * 若無法認證則會顯示『憑證錯誤』或是『不是安全的連線警告』提醒用戶這個網站可能不可信任
  * 若認證成功，則會使用 cerficiate 中的公鑰加密來進行連線
* self-signed CA 產出來的 certificate 很可能客戶端會不認得
  * 要把自簽的憑證，產生讓客戶端信任的 client-ca，加到客戶端的信任名單
  * 要把產生的 client.cer 與 client.key ，讓客戶端連線後，伺服器端接受這個客戶端

---

# 分析一下需求跟規格

我們需要為每一個 "site" 生一組 certificate，客戶端連入時會驗證這個 site 是否合法。針對目前這個 single-node ELK stack，我們可能有幾種選擇

* 簽一個 localhost，當然這個只能在 localhost 上的客戶端元件使用
* 簽一個 public DNS elk.chechiachang.com，可以在公開網路上使用，別人也可以使用這個DNS嘗試存取
* 簽一個私有網域的 DNS，例如在 GCP 上可以使用[內部dns服務](https://cloud.google.com/compute/docs/internal-dns?hl=zh-tw)
  * 長這樣 elk.asia-east1-b.c.chechiachang-elk.internal
  * [INSTANCE_NAME].[ZONE].c.[PROJECT_ID].internal

我們這邊選擇使用內部 dns，elk.asia-east1-b-c-chechaichang-elk.internal，讓 elk 只能透過內部網路存取

  * elasticsearch: elk.asia-east1-b.c.chechaichang.internal:9200
  * kibana: elk.asia-east1-b.c.chechaichang.internal:5601
  * 外部要連近來 kibana，我們使用 vpn 服務連進私有網路
  * (Optional) 如果真的很想使用外部 dns，elk.chechiachang.com，可以使用
    * GCP 的 load balancer掛進來，用 GCP 的 certificate manager 自動管理 certificate
    * 或是在 node 上開一個 nginx server，再把 certificate 用 certbot 生出來

---

# 開始設定

一堆官方文件，我們先跳過XD

https://www.elastic.co/guide/en/elastic-stack-overview/7.3/elasticsearch-security.html
https://www.elastic.co/guide/en/elastic-stack-overview/7.3/ssl-tls.html
https://www.elastic.co/guide/en/elasticsearch/reference/7.3/configuring-tls.html#configuring-tls
https://www.elastic.co/guide/en/elasticsearch/reference/7.3/certutil.html

### Generate certificate

CA 已經剛剛產生完了，在 /etc/elasticsearch/config/elastic-stack-ca.p12
我們用這組 CA ，為 elk.asia-east1-b.c.chechiachang.internal 簽一個 certificate

```
# certificate for site: private dns with Elastic CA
/usr/share/elasticsearch/bin/elasticsearch-certutil cert \
  --ca /etc/elasticsearch/config/elastic-stack-ca.p12 \
  --name elk.asia-east1-b.c.chechaichang.internal \
  --dns elk.asia-east1-b.c.chechaichang.internal \
  --ip 10.140.0.10 \
  -out /etc/elasticsearch/config/elastic-certificates.p12
```

輸出在 /etc/elasticsearch/config/elastic-certificates.p12

用 openssl 工具看一下內容，如果有密碼這邊要用密碼解鎖

```
# check certificate info
openssl pkcs12 -in /etc/elasticsearch/config/elastic-certificates.p12 -info -nokeys
```

因為我們這邊只有一個 site，所有伺服器端用這個 certificate ，啟用 ssl。
客戶端，去認可這個 certificate 產生出來的 client-ca.cer，客戶端才會接受自簽的伺服器憑證。
客戶端使用 client.cer 與 client.key 與 server 連線，server 才接受客戶端是安全的。

如果是用 root 權限操作，記得把所有權還給 elasticsearch 的使用者，避免 permission denied

```
# Change owner to fix read permission
chown -R elasticsearch:elasticsearch /etc/elasticsearch/config
```

有密碼記得也要用 keystore 把密碼加密後喂給 elasticsearch

```
/usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.transport.ssl.keystore.secure_password
/usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.transport.ssl.truststore.secure_password
```

### 更新 elasticsearch 設定

Certificates 都生完了，接下來把 elasticsearch 的參數改一改

```
$ sudo vim /etc/elasticsearch/elasticsearch.yml

xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
# use certificate. full will verify dns and ip
xpack.security.transport.ssl.verification_mode: certificate
xpack.security.transport.ssl.keystore.path: /etc/elasticsearch/config/elastic-certificates.p12
xpack.security.transport.ssl.truststore.path: /etc/elasticsearch/config/elastic-certificates.p12
```

啟用 security 與 ssl，然後指定 certificate 路徑以外，security 這邊提供了 server side (elasticsearch) 在檢查客戶端連線時的檢查模式(vertification mode)，[文件有說明](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-settings.html#ssl-tls-settings)

HTTP 也開起來

```
vim /etc/elasticsearch/elasticsearch.yml

xpack.security.http.ssl.enabled: true
xpack.security.http.ssl.keystore.path: /etc/elasticsearch/config/elastic-certificates.p12
xpack.security.http.ssl.truststore.path: /etc/elasticsearch/config/elastic-certificates.p12

/usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.http.ssl.keystore.secure_password
/usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.http.ssl.truststore.secure_password
```

重啟 elasticsearch，看一下 log

```
sudo systemctl restart elasticsearch
tail -f /var/log/elasticsearch/elasticsearch.log
```

然後你就發現，原來 kibana 連入連線，不斷被 server 這端拒絕。所以以下要來設定 kibana

---

# Kibana

https://www.elastic.co/guide/en/kibana/7.3/using-kibana-with-security.html
https://www.elastic.co/guide/en/kibana/7.3/configuring-tls.html

使用剛剛簽的 server certificate，產生客戶端的 client-ca.cer，還有 client.cer 與 client.key

```
mkdir -p /etc/kibana/config

openssl pkcs12 -in /etc/elasticsearch/config/elastic-certificates.p12 -nocerts -nodes > /etc/kibana/config/client.key
openssl pkcs12 -in /etc/elasticsearch/config/elastic-certificates.p12 -clcerts -nokeys > /etc/kibana/config/client.cer
openssl pkcs12 -in /etc/elasticsearch/config/elastic-certificates.p12 -cacerts -nokeys -chain > /etc/kibana/config/client-ca.cer

sudo chown -R kibana:kibana /etc/kibana/config/
```

更改 kibana 連入 elasticsearch 的連線設定 

```
sudo vim /etc/kigana/kibana.yml

elasticsearch.hosts: ["https://elk.asia-east1-b.c.chechaichang.internal:9200"]
xpack.security.enabled: true
elasticsearch.ssl.certificate: /etc/kibana/config/client.cer
elasticsearch.ssl.key: /etc/kibana/config/client.key
elasticsearch.ssl.certificateAuthorities: [ "/etc/kibana/config/client-ca.cer" ]
elasticsearch.ssl.verificationMode: full
```

注意這邊 elasticsearch.hosts 我們已經從 http://localhost 換成 https 的內部 dns，原有的 localhost 已經無法使用（如果 elasicsearch 有 enforce https 的話）

把 ca 餵給客戶端，讓客戶端信任這個我們自簽的 CA，並指定連線時使用的 key 與 cer

重啟 Kibana，看一下 log

```
sudo systemctl restart kibana
journalctl -fu kibana
```

如果沒有一直噴 ssl certificate error 的話，恭喜你成功了

然而，除了 kibana 以外，我們還有其他的 client 需要連入 elasticsearch

* 我們還需要把上述步驟在 apm-server, filebeat, 其他的 beat 上也設定
* 如果在 k8s 上，要把 certificate 等檔案用 volume 掛進去...(好苦)
* 然後為了讓這些 client 能連入 kibana ，將 document tempalte 匯入 kibana，我們還需要

就是他們彼此互打，都要有 certificate(汗)，歡迎來到 https 的世界

# 但基本上的設定都一樣，下面可以不用看下去了XD

如果有用到再查文件就好，這邊直接小結

* 設定 security 前要先想號自己的需求，如何連入，安全性設定到哪邊
* 使用 utility 自簽 CA，然後產生 certificates，再產生 client cers



---

# kibana 作為 server

kibana 連入 elasticsearch時， kibana 是 client 吃 elasticsearch 的憑證
apm-server 連入 kibana時，kibana 是 server，要產生 site 憑證，然後餵給 apm-server

首先更改 kibana 設定
```
$ sudo vim /etc/kibana/kibana.yml

server.ssl.enabled: true
server.ssl.certificate: /etc/kibana/config/client.cer
server.ssl.key: /etc/kibana/config/client.key
```

重啟 kibana
```
journalctl -fu kibana
```

---

# Apm-server

https://www.elastic.co/guide/en/apm/server/7.3/securing-apm-server.html

apm-server 連入 kibana時，我們把 kibana 的憑證餵給 apm-server
那應用端的 apm-client (ex. apm-python-client)，連入 apm-server
* 在 http 的狀況下，可以只使用 secret-token(裸奔)
* 在 https 的狀況下，要把 certificates，然後餵給應用端的client library

```
sudo vim /etc/apm-server/apm-server.yml

host: "0.0.0.0:8200"
  secret_token: <設定一組夠安全的 token>

  rum:
    enabled: true

kibana:
  protocol: "https"
  ssl.enabled: true
output.kibana:
  enable: false # can only have 1 output
output.elasticsearch:
monitoring.elasticsearch:
  protocol: "https"
  username: "elastic"
  password: ""
  hosts: ["elk.asia-east1-b.c.checahichang.internal:9200"]
  ssl.enabled: true
  ssl.verification_mode: full
  ssl.certificate_authorities: ["/etc/apm-server/config/client-ca.cer"]
  ssl.certificate: "/etc/apm-server/config/client.cer"
  ssl.key: "/etc/apm-server/config/client.key"
```

重啟 apm-server
```
systemctl restart apm-server
journalctl -fu apm-server
```


應用端的設定就需要依據 library 的實做設定，例如 flask-apmagent-python

```
ELASTIC_APM_SERVER_CERT=/etc/elk/certificates/client.cer
```

[細節文件在此](https://www.elastic.co/guide/en/apm/agent/python/current/configuration.html#config-server-cert)

---

# 怎麼還有

記得我們在 node 上有安裝 Self-monitoring filebeat，elasticsearch 改成 ssl 這邊當然也連不盡去了，再做同樣操作...

https://www.elastic.co/guide/en/beats/filebeat/7.3/filebeat-reference-yml.html

```
sudo apt-get install filebeat

mkdir -p /etc/filebeat/config
openssl pkcs12 -in /etc/elasticsearch/config/elastic-certificates.p12 -nocerts -nodes > /etc/filebeat/config/client.key
openssl pkcs12 -in /etc/elasticsearch/config/elastic-certificates.p12 -clcerts -nokeys > /etc/filebeat/config/client.cer
openssl pkcs12 -in /etc/elasticsearch/config/elastic-certificates.p12 -cacerts -nokeys -chain > /etc/filebeat/config/client-ca.cer
```

Restart filebeat
```
systemctl restart filebeat
journalctl -fu filebeat
```

---

# 如果你的應用在 kubernetes 上

可以使用下面方法拿到 client.cer ，然後用 secret 塞進 k8s，在用 volume from secrets，掛給監測應用的 filebeat

```

mkdir -p /etc/beats/config
openssl pkcs12 -in /etc/elasticsearch/config/elastic-certificates.p12 -nocerts -nodes > /etc/beats/config/client.key
openssl pkcs12 -in /etc/elasticsearch/config/elastic-certificates.p12 -clcerts -nokeys > /etc/beats/config/client.cer
openssl pkcs12 -in /etc/elasticsearch/config/elastic-certificates.p12 -cacerts -nokeys -chain > /etc/beats/config/client-ca.cer

gcloud compute scp elk:/etc/beats/config/* .
 client-ca.cer
 client.cer
 client.key

kubectl -n elk create secret generic elk-client-certificates \
  --from-file=client-ca.cer=client-ca.cer \
  --from-file=client.cer=client.cer \
  --from-file=client.key=client.key

kubectl apply -f elk/gke/filebeat/
```
