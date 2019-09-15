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

上篇[Self-host ELK stack on GCP]({{< ref "/post/self-host-elk-stack-on-gcp" >}}) 介紹了，elk stack 基本的安裝，安裝完獲得一個裸奔的 elk stack，沒有 tls/https 在公開網路上使用是非常危險的。這篇要來介紹如何做安全性設定。

Secure elastic stack

# 簡單講一下 SSL & TLS

https://www.feistyduck.com/books/openssl-cookbook/
https://github.com/ssllabs/research/wiki/SSL-and-TLS-Deployment-Best-Practices

# Preflight check

Generate password before enable ssl
```
/usr/share/elasticsearch/bin/elasticsearch-setup-passwords auto
```

(Optional) Nginx & certbot (For out-cluster communication)
```
sudo apt-get install -y nginx certbot python3-certbot-nginx

#configure nginx & certbot
```

---

# Security Specs

To enforce ssl/tls, we have three available connections through dns
- https://localhost: available on single node
- https://elk.asia-east1-b.c.machi-x.internal: a private dns available within gcp private network
- https://elk.machix.com: public dns, available from public network

We choose to use private dns:
- elasticsearch only visible in private network
  - access from private network (GKE, GCE in default) use https://elk.asia-east1-b.c.machi-x.internal:9200
- kibana only visible in private network
  - access from private network (GKE, GCE...) use https://elk.asia-east1-b.c.machi-x.internal:5601
  - access from external vpn network use https://elk.machix.com (35.236.154.151). Nginx will proxy to localhost:5601 port
- apm-server only visible in private network
  - access from private network (GKE, GCE...) use https://elk.asia-east1-b.c.machi-x.internal:8200

# Check GCP Firewall Rules

default-allow-internal: a default firewall rule which allow ingress from GCE instances in same network
Source IP range: 10.128.0.0/9
Protocaol & ports: all

allow-k8s-to-elk: enable ingress from kubernetes cluster CIDR
Source IP ranges: 10.8.0.0/16, 10.14.0.0/16, ...
Protocol & Ports: tcp: 5044(logstash), 5601(kibana), 9200(elasticsearch), 8200(apm-server)

---

# ELK

https://www.elastic.co/guide/en/elastic-stack-overview/7.3/elasticsearch-security.html
https://www.elastic.co/guide/en/elastic-stack-overview/7.3/ssl-tls.html

# Secure elasticsearch

https://www.elastic.co/guide/en/elasticsearch/reference/7.3/configuring-tls.html#configuring-tls
https://www.elastic.co/guide/en/elasticsearch/reference/7.3/certutil.html

Generate CA, certificate
```
mkdir -p /etc/elasticsearch/config

# CA generated with Elastic tool
/usr/share/elasticsearch/bin/elasticsearch-certutil ca \
  -out /etc/elasticsearch/config/elastic-stack-ca.p12

# Self-signed certificate for subject: private dns with Elastic CA
/usr/share/elasticsearch/bin/elasticsearch-certutil cert \
  --ca /etc/elasticsearch/config/elastic-stack-ca.p12 \
  --name elk.asia-east1-b.c.machi-x.internal \
  --dns elk.asia-east1-b.c.machi-x.internal \
  --ip 10.140.0.60 \
  -out /etc/elasticsearch/config/elastic-certificates.p12

# check certificate info
openssl pkcs12 -in /etc/elasticsearch/config/elastic-certificates.p12 -info -nokeys

# Change owner to fix read permission
chown -R elasticsearch:elasticsearch /etc/elasticsearch/config

/usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.transport.ssl.keystore.secure_password
/usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.transport.ssl.truststore.secure_password
```

Update elasticsearch.yml
```
vim /etc/elasticsearch/elasticsearch.yml

xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
# use certificate. full will verify dns and ip
xpack.security.transport.ssl.verification_mode: certificate
xpack.security.transport.ssl.keystore.path: /etc/elasticsearch/config/elastic-certificates.p12
xpack.security.transport.ssl.truststore.path: /etc/elasticsearch/config/elastic-certificates.p12
```

Encrypt elasticsearch HTTP client communications
```
vim /etc/elasticsearch/elasticsearch.yml

xpack.security.http.ssl.enabled: true
xpack.security.http.ssl.keystore.path: /etc/elasticsearch/config/elastic-certificates.p12
xpack.security.http.ssl.truststore.path: /etc/elasticsearch/config/elastic-certificates.p12

/usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.http.ssl.keystore.secure_password
/usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.http.ssl.truststore.secure_password
```

Restart elasticsearch
```
systemctl restart elasticsearch
tail -f /var/log/elasticsearch/elasticsearch.log
```

---

# Kibana

https://www.elastic.co/guide/en/kibana/7.3/using-kibana-with-security.html
https://www.elastic.co/guide/en/kibana/7.3/configuring-tls.html

Client certificates for elasticsearch
```
mkdir -p /etc/kibana/config
openssl pkcs12 -in /etc/elasticsearch/config/elastic-certificates.p12 -nocerts -nodes > /etc/kibana/config/client.key
openssl pkcs12 -in /etc/elasticsearch/config/elastic-certificates.p12 -clcerts -nokeys > /etc/kibana/config/client.cer
openssl pkcs12 -in /etc/elasticsearch/config/elastic-certificates.p12 -cacerts -nokeys -chain > /etc/kibana/config/client-ca.cer
chown -R kibana:kibana /etc/kibana/config/
```

```
vim /etc/kigana/kibana.yml
elasticsearch.hosts: ["https://elk.asia-east1-b.c.machi-x.internal:9200"]
xpack.security.enabled: true
elasticsearch.ssl.certificate: /etc/kibana/config/client.cer
elasticsearch.ssl.key: /etc/kibana/config/client.key
elasticsearch.ssl.certificateAuthorities: [ "/etc/kibana/config/client-ca.cer" ]
elasticsearch.ssl.verificationMode: full
```

Restart kibana
```
systemctl restart kibana
journalctl -fu kibana
```

### Enforce tls server clients to kibana (ex. apm-server)

```
server.ssl.enabled: true
server.ssl.certificate: /etc/kibana/config/client.cer
server.ssl.key: /etc/kibana/config/client.key
```

Restart kibana
```
journalctl -fu kibana
```

---

# Apm-server

https://www.elastic.co/guide/en/apm/server/current/securing-apm-server.html

```
cp -r /etc/kibana/config /etc/apm-server
chown apm-server:apm-server /etc/apm-server/config
```

```
vim /etc/apm-server/apm-server.yml

host: "0.0.0.0:8200"
  secret_token: 

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
  password: "uEzDtcd0kx3u1nEMcLr7"
  hosts: ["elk.asia-east1-b.c.machi-x.internal:9200"]
  ssl.enabled: true
  ssl.verification_mode: full
  ssl.certificate_authorities: ["/etc/apm-server/config/client-ca.cer"]
  ssl.certificate: "/etc/apm-server/config/client.cer"
  ssl.key: "/etc/apm-server/config/client.key"
```

Restart apm-server
```
systemctl restart apm-server
journalctl -fu apm-server
```

---

# TLS for APM-server and APM-agent

This requires modification to Back-End source code.

We use flask-apmagent-python, for example.

### APM-server

Sign another certificates

```
apm-server:
  ssl:
    enabled: true
    certificate_authorities: []
    certificate: ''
    key: ''
```

---

# Self-monitoring filebeat

https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-reference-yml.html

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

# SSL/https for Application Side client

### APM-agent

https://www.elastic.co/guide/en/apm/agent/python/current/configuration.html#config-server-cert
```
ELASTIC_APM_SERVER_CERT=/etc/elk/certificates/client.cer
```

#  Beats

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
