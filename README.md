Source Code of My Github Page
===

[https://chechiachang.github.io](https://chechiachang.github.io)

# Powered by Hugo

# Theme

[Academic](https://sourcethemes.com/academic/docs/install/)

# Create Content

Add new talk
```
TITLE=my-talk-title make talk
```

Add new project
```
TITLE=my-talk-title make project
```

# Bind google analysis

Google Analytics
- Add a new account
  - Filling form
  - Get Google Analytics tracking ID

Enable analytics by entering your Google Analytics tracking ID
```
# config/_default/config.toml
googleAnalytics = ""
```

Publish /public to github
```
make hugo publish
```

# Bind google search

- go to google search console
- Add site https://chechiachang.github.io
  - Authorized by google analysis with google email account
- Submit https://chechiachang.github.io/sitemap.xml to console
- Wait for data processing

# TODOs

ITHome 30 days ironman challenge
https://ithelp.ithome.com.tw/users/20120327/ironman/2444

Features
- step-by-step guide for deployment: guarentee a running deployment on GCP
- basic configuration, usage, monitoring, networking on GKE
- debugging, stability analysis in an aspect of devop

Topics
- Deploy Kafka HA on Kubernetes(4)
  - deploy kafka-ha on Kubernertes with helm
  - in-cluster networking configuration for high availability
  - basic app-side usage, performance tuning
  - Operate Kafka: update config, upgrade version, migrate data
- Promethus / grafana(5)
  - Deploy Prometheus / Grafana stack on GCE instance
  - Monitoring services on Kubernetes with exporters
  - Export Kubernetes metrics to Prometheus
  - Export Redis-ha metrics to Prometheus
  - Export Kafka metrics to Prometheus
- ELK stack(8)
  - Deploy self-hosted ELK stack on GCE instance
  - Secure ELK stack with SSL and role-based authentication
  - Monitoring services on Kubernetes with ELK beats
  - Monitoring services on GCE instances
  - Logstash pipelines and debugging walk through
  - Elasticsearch operations: house-cleaning, tuning, pernament storage
  - Elasticsearch maitainence, trouble shooting
  - Get-Started with Elastic Cloud SASS
- General operations on Kubernetes(4)
  - Secure services with SSL by cert-manager
  - Kubectl cheat sheet
  - Kubernetes Debug SOP
  - Speed up container updating with operator
- GCP networking(4)
  - Firewall basic concept for private network with GCE instances & Kubernetes
  - Load balancer for Kubernetes service & ingress
  - DNS on GCP from Kube-dns to GCP DNS service
  - SSL certificate management on GCP
- GCP log management(3)
  - Basic usage about GCP logging & GCP Error Report
  - Logging on GKE from gcp-fluentd to stackdriver
  - Stackdriver, metrics, alerts
- ?(2)