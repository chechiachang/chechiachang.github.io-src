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

[官方的文件在這裡](https://www.elastic.co/guide/en/elastic-stack-overview/7.3/elasticsearch-security.html)，碎念一下，除非對 ELK 的功能有一定了解，不然這份真的不是很友善。建議從官方文件底下的[Tutorial: Getting started with security](https://www.elastic.co/guide/en/elastic-stack-overview/7.3/security-getting-started.html) 開始，過程比較不會這麼血尿。

總之為了啟用 authentication & https，這篇要做的事情：

* enable x-pack & activate basic license
* Generate self-signed ca, server certificate, client certificate
* Configure Elasticsearch, Kibana, & other components to
  * use server certificate when act as server
  * use client certificate when connect to an ELK server

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

上面加了 username/password authentication，但如果沒 https/tls 基本上還是裸奔。接下來要處理連線加密。

[官方 tutorial](https://www.elastic.co/guide/en/elastic-stack-overview/7.3/encrypting-internode-communications.html)

一堆官方文件，我們先跳過XD

* [elasticsearch security](https://www.elastic.co/guide/en/elastic-stack-overview/7.3/elasticsearch-security.html)
* [elastic stack ssl tls](https://www.elastic.co/guide/en/elastic-stack-overview/7.3/ssl-tls.html)
* [elasticsearch configuring tls](https://www.elastic.co/guide/en/elasticsearch/reference/7.3/configuring-tls.html#configuring-tls)
* [certutil](https://www.elastic.co/guide/en/elasticsearch/reference/7.3/certutil.html)

# 分析一下需求跟規格

我們需要為每一個 node 生一組 node certificate，使用 node certificate 產生 client certificates 提供給其他 client，連入時會驗證 client 是否為 authenticated user。

針對目前這個 single-node ELK stack，我們可能有幾種選擇

* 簽署一個 localhost，當然這個只能在 localhost 上的客戶端元件使用，別的 node 無法用這個連入
* 簽署一個 public DNS elk.chechiachang.com，可以在公開網路上使用，別人也可以使用這個DNS嘗試連入
* 簽署一個私有網域的 DNS，例如在 GCP 上可以使用[內部dns服務](https://cloud.google.com/compute/docs/internal-dns?hl=zh-tw)
  * 長這樣 elk.asia-east1-b.c.chechiachang.internal
  * [INSTANCE_NAME].[ZONE].c.[PROJECT_ID].internal
* 有需要也可以一份 server certificate 中簽署複數個 site

我們這邊選擇使用內部 dns，elk.asia-east1-b-c-chechaichang.internal，讓這個 single-node elk 只能透過內部網路存取。

  * elasticsearch: elk.asia-east1-b.c.chechaichang.internal:9200
  * kibana: elk.asia-east1-b.c.chechaichang.internal:5601
  * 外部要連近來 kibana，我們使用 vpn 服務連進私有網路

如果想使用外部 dns，讓 elk stack 在公開網路可以使用，ex. elk.chechiachang.com，可以

  * GCP 的 load balancer掛進來，用 GCP 的 certificate manager 自動管理 certificate
  * 或是在 node 上開一個 nginx server，再把 certificate 用 certbot 生出來

# Generate certificates

先把 X.509 digital certificate 的 certificate authority(CA) 生出來。我們可以設定密碼保護這個檔案

```
mkdir -p /etc/elasticsearch/config

# CA generated with Elastic tool
/usr/share/elasticsearch/bin/elasticsearch-certutil ca \
  -out /etc/elasticsearch/config/elastic-stack-ca.p12
```

生出來是 PKCS#12 格式的 keystore，包含：

* CA 的 public certificate
* CA 的基本資訊
* 簽署其他 node certificates 使用的私鑰(private key)

用 openssl 工具看一下內容，如果有密碼這邊要用密碼解鎖

```
$ openssl pkcs12 -in /etc/elasticsearch/config/elastic-stack-ca.p12 -info -nokeys
```

附帶說明，X.509 有多種檔案格式

* .pem
* .cer, .crt, .der
* .p12
* .p7b, .p7c
* ...

另外檔案格式可以有其他用途，也就是說裡面裝的不一定是 X.509 憑證。裡面的內容也不同。

ELK 設定的過程中，由於不是所有的 ELK component 都支援使用 .p12 檔案，我們在設定過程中會互相專換，或是混用多種檔案格式。

# Generate certificate

我們用 elastic-stack-ca.p12 這組 keystore裡面的 CA 與 private key，為 elk.asia-east1-b.c.chechiachang.internal 簽一個 p12 keystore，裡面有

* node certificate
* node key
* CA certificate

這邊只產生一組 server certificate 給 single-node cluster 的 node-1

如果 cluster 中有多個 elasticsearch，為每個 node 產生 certificate 時都要使用同樣 CA 來簽署，讓 server 信任這組 CA。

使用 elasticsearch-certutil 簡化簽署過程，從產生 CA ，到使用 CA 簽署 certificate。另外，再產生 certificate 中使用 Subject Alternative Name(SAN)，並輸入 ip 與 dns。

```
# certificate for site: private dns with Elastic CA
/usr/share/elasticsearch/bin/elasticsearch-certutil cert \
  --ca /etc/elasticsearch/config/elastic-stack-ca.p12 \
  --name elk.asia-east1-b.c.chechaichang.internal \
  --dns elk.asia-east1-b.c.chechaichang.internal \
  --ip 10.140.0.10 \
  -out /etc/elasticsearch/config/node-1.p12
```

用 openssl 看一下內容，如果有密碼這邊要用密碼解鎖

```
$ openssl pkcs12 -in /etc/elasticsearch/config/node-1.p12 -info -nokeys
```

server 用這個 certificate ，啟用 ssl。

client 使用這個 certificate 產生出來的 client.cer 與 client.key 與 server 連線，server 才接受客戶端是安全的。

記得把所有權還給 elasticsearch 的使用者，避免 permission denied

```
# Change owner to fix read permission
chown -R elasticsearch:elasticsearch /etc/elasticsearch/config
```

有密碼記得也要用 keystore 把密碼加密後喂給 elasticsearch

```
/usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.transport.ssl.keystore.secure_password
/usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.transport.ssl.truststore.secure_password
```

關於 X.509 Certifcate 之後有空我們來聊一下

# 更新 elasticsearch 設定

Certificates 都生完了，接下來更改 elasticsearch 的參數，在 transport layer 啟用 ssl。啟用 security 後，在 transport layer 啟動 ssl 是必須的。

```
$ sudo vim /etc/elasticsearch/elasticsearch.yml

xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
# use certificate. full will verify dns and ip
xpack.security.transport.ssl.verification_mode: certificate
xpack.security.transport.ssl.keystore.path: /etc/elasticsearch/config/node-1.p12
xpack.security.transport.ssl.truststore.path: /etc/elasticsearch/config/node-1.p12
```

啟用 security 與 transport layer 的 ssl，然後指定 keystore路徑，讓 server 執行 client authentication
由於這筆 p12 帶有 CA certificate 作為 trusted certificate entry，所以也可以順便當作 trustore，讓 client 信任這個 CA

security 這邊提供了 server side (elasticsearch) 在檢查客戶端連線時的檢查模式(vertification mode)，[文件有說明](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-settings.html#ssl-tls-settings)，可以設定 

* certificate: 檢查 certificate 加密是否有效
* full: 簽 node certificate 時可以指定 ip dns，啟用會檢查來源 node ip dns 是否也正確

(Optional) HTTP layer 啟動 ssl

```
vim /etc/elasticsearch/elasticsearch.yml

xpack.security.http.ssl.enabled: true
xpack.security.http.ssl.keystore.path: /etc/elasticsearch/config/node-1.p12
xpack.security.http.ssl.truststore.path: /etc/elasticsearch/config/node-1.p12

/usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.http.ssl.keystore.secure_password
/usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.http.ssl.truststore.secure_password
```

重啟 elasticsearch，看一下 log

```
sudo systemctl restart elasticsearch
tail -f /var/log/elasticsearch/elasticsearch.log
```

然後你就發現，原來 kibana 連入 的 http 連線，不斷被 server 這端拒絕。所以以下要來設定 kibana

---

# Kibana

* [using kibana with security](https://www.elastic.co/guide/en/kibana/7.3/using-kibana-with-security.html)
* [kibana configuring tls](https://www.elastic.co/guide/en/kibana/7.3/configuring-tls.html)

使用剛剛簽的 server certificate，從裡面 parse 出 client-ca.cer，還有 client.cer 與 client.key

```
mkdir -p /etc/kibana/config

$ openssl pkcs12 --help
Usage: pkcs12 [options]
Valid options are:
 -chain              Add certificate chain
 -nokeys             Don't output private keys
 -nocerts            Don't output certificates
 -clcerts            Only output client certificates
 -cacerts            Only output CA certificates
 -info               Print info about PKCS#12 structure
 -nodes              Don't encrypt private keys
 -in infile          Input filename

# no certs, no descript
openssl pkcs12 -in /etc/elasticsearch/config/node-1.p12 -nocerts -nodes > /etc/kibana/config/client.key
openssl pkcs12 -in /etc/elasticsearch/config/node-1.p12 -clcerts -nokeys > /etc/kibana/config/client.cer
openssl pkcs12 -in /etc/elasticsearch/config/node-1.p12 -cacerts -nokeys -chain > /etc/kibana/config/client-ca.cer

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

* 指定 ssl.certificate, ssl.key 做連線 elasticsearch server 時的 user authentication
* 由於我們是 self-signed CA，所以需要讓客戶端信任這個我們自簽的 CA

注意這邊 elasticsearch.hosts 我們已經從 http://localhost 換成 https 的內部 dns，原有的 localhost 已經無法使用（如果 elasicsearch 有 enforce https 的話）

重啟 Kibana，看一下 log

```
sudo systemctl restart kibana
journalctl -fu kibana
```

如果沒有一直噴 ssl certificate error 的話，恭喜你成功了

然而，除了 kibana 以外，我們還有其他的 client 需要連入 elasticsearch

* 把上述步驟在 apm-server, filebeat, 其他的 beat 上也設定
* 如果在 k8s 上，要把 cer, key 等檔案用 volume 掛進去

Kibana 本身也有 server 的功能，讓其他 client 連入。例如讓 filebeat 自動將 document tempalte 匯入 kibana，我們也需要設定 

* kibana server certificate
* filebeat client to kibana server

就是他們彼此互打，都要有 ca, key, cert

### 但基本上的設定都一樣，下面可以不用看下去了XD

如果有用到再查文件就好，這邊直接小結

* 設定 security 前要先想號自己的需求，如何連入，安全性設定到哪邊
* 使用 utility 自簽 CA，然後產生 server certificate
* 使用 server certificate 再 parse 出 ca-certificate, client cers, key




---

# kibana 作為 server

工作路徑可能是這樣： app(apm-client library) -> apm-server -> kibana -> elasticsearch

* kibana 連入 elasticsearch時， kibana 是 client 吃 elasticsearch 的憑證
* apm-server 連入 kibana時，kibana 是 server，apm-server 吃 kibana 的憑證

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

# Apm-server

https://www.elastic.co/guide/en/apm/server/7.3/securing-apm-server.html

應用端的 apm-client (ex. apm-python-client)，連入 apm-server

* 在 http 的狀況下，雖然有使用 secret-token，但還是裸奔
* 在 https 的狀況下，要把 certificates，然後餵給應用端的client library

更改 apm-server 的設定

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
  password: "*******************"
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

# APM library

應用端的設定就需要依據 library 的實做設定，例如 flask-apmagent-python

```
ELASTIC_APM_SERVER_CERT=/etc/elk/certificates/client.cer
```

[apm agent python config server cert](https://www.elastic.co/guide/en/apm/agent/python/current/configuration.html#config-server-cert)

# filebeat

記得我們在 node 上有安裝 Self-monitoring filebeat，elasticsearch 改成 ssl 這邊當然也連不盡去了，再做同樣操作

https://www.elastic.co/guide/en/beats/filebeat/7.3/filebeat-reference-yml.html

```
sudo apt-get install filebeat

mkdir -p /etc/filebeat/config
openssl pkcs12 -in /etc/elasticsearch/config/node-1.p12 -nocerts -nodes > /etc/filebeat/config/client.key
openssl pkcs12 -in /etc/elasticsearch/config/node-1.p12 -clcerts -nokeys > /etc/filebeat/config/client.cer
openssl pkcs12 -in /etc/elasticsearch/config/node-1.p12 -cacerts -nokeys -chain > /etc/filebeat/config/client-ca.cer
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
openssl pkcs12 -in /etc/elasticsearch/config/node-1.p12 -nocerts -nodes > /etc/beats/config/client.key
openssl pkcs12 -in /etc/elasticsearch/config/node-1.p12 -clcerts -nokeys > /etc/beats/config/client.cer
openssl pkcs12 -in /etc/elasticsearch/config/node-1.p12 -cacerts -nokeys -chain > /etc/beats/config/client-ca.cer

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
