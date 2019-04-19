---
title: "Jenkins X on Kubernetes"
date: 2019-04-19T21:36:50+08:00
draft: false
---

### [Jenkins](https://jenkins.io/)

- One of the earliest open source antomation server
- Most common option in use
- Flexible and customizable. Hundreds of plugins
- Support automation for any project

---

### [Jenkins X](https://jenkins-x.io/)

- CI/CD platform (Jenkins Platform) 
- Cloud native serverless
- For modern cloud applications on Kubernetes. 

---

### Outlines

- [Install Jenkins with jx](#install)
- [Create a Pipeline with jx](#pipeline)
- [Develope with jx client](#client)

check [Jenkins-X Github Repo](https://github.com/jenkins-x/jx)

---

<a name="install"></a>

### Install

Create GKE cluster & Get Credentials
```
gcloud init
gcloud components update
```

```
CLUSTER_NAME=jenkins-server
#CLUSTER_NAME=jenkins-serverless

gcloud container clusters create ${CLUSTER_NAME} \
  --num-nodes 1 \
  --machine-type n1-standard-4 \
  --enable-autoscaling \
  --min-nodes 1 \
  --max-nodes 2 \
  --zone asia-east1-b \
  --preemptible
```

---

Create GKE cluster & Get Credentials

```
# Get credentials to access cluster with kubectl
gcloud container clusters get-credentials ${CLUSTER_NAME}

# Check cluster stats.
kubectl get nodes
```

---

Download [Jenkins X Release](https://github.com/jenkins-x/jx/releases) & install jx on Local Machine

```
JX_VERSION=v2.0.2
OS_ARCH=darwin-amd64
#OS_ARCH=linux-amd64
curl -L https://github.com/jenkins-x/jx/releases/download/"${JX_VERSION}"/jx-"${OS_ARCH}".tar.gz | tar xzv
sudo mv jx /usr/local/bin
jx version

NAME               VERSION
jx                 2.0.2
Kubernetes cluster v1.11.7-gke.12
kubectl            v1.11.9-dispatcher
helm client        v2.11.0+g2e55dbe
helm server        v2.11.0+g2e55dbe
git                git version 2.20.1
Operating System   Mac OS X 10.14.4 build 18E226
```

---

(Install Option 1) Serverless Jenkins Pipeline

```
DEFAULT_PASSWORD=mySecretPassWord123
jx install \
  --default-admin-password=${DEFAULT_PASSWORD} \
  --provider='gke'
```

---

Install options:

- Select Jenkins installation type:
  - [x] Serverless Jenkins X Pipelines with Tekon
  - [ ] Static Master Jenkins
- Pick default workload build pack
  - [x] Kubernetes Workloads: Automated CI+CD with GitOps Promotion
  - [ ] Library Workloads: CI+Release but no CD

```
Your Kubernetes context is now set to the namespace: jx
INFO[0231] To switch back to your original namespace use: jx namespace jx
...
```

---

(Install Option 2) Static Jenkins Server

```
DEFAULT_PASSWORD=mySecretPassWord123

jx install \
  --default-admin-password=${DEFAULT_PASSWORD} \
  --provider='gke'
```

---

Options:

- Select Jenkins installation type:
  - [ ] Serverless Jenkins X Pipelines with Tekon
  - [x] Static Master Jenkins
- Pick default workload build pack
  - [x] Kubernetes Workloads: Automated CI+CD with GitOps Promotion
  - [ ] Library Workloads: CI+Release but no CD

```
INFO[0465]Your Kubernetes context is now set to the namespace: jx
INFO[0465] To switch back to your original namespace use: jx namespace default

Access Static Jenkins Server through Domain with username and password
Domain http://jenkins.jx.11.22.33.44.nip.io/
```

---

### Uninstall

```
jx uninstall
# rm -rf ~/.jx
```

---

### Setup CI/CD Pipeline

Create Quickstart Repository

```
kubectl get pods --namespace jx --watch
```

```
# cd workspace
jx create quickstart
```

---

Options:

```
$ select the quickstart you wish to create  [Use arrows to move, type to filter]
  aspnet-app
  dlang-http
> golang-http
  jenkins-cwp-quickstart
  jenkins-quickstart
  node-http

INFO[0121] Watch pipeline activity via:    jx get activity -f serverless-jenkins-quickstart -w
```

---

Check log of the first run

```
jx logs pipeline
```

---

Add a setup step for pullrequest
```
cd serverless-jenkins-quickstart
jx create step --pipeline pullrequest \
  --lifecycle setup \
  --mode replace \
  --sh "echo hello world"
```

Validate pipeline step for each modification
```
jx step validate
```

A build-pack pod started after git push. Watch pod status with kubectl.
```
kubectl get pods --namespace jx --watch
```

---

Check Build Status on Prow (Serverless)

http://deck.jx.130.211.245.13.nip.io/
Login with username and password

---

Import Existing Repository

```
# In source code repository
# Import jx to remote jenkins-server. This will apply a Jenkinsfile to repository by default
jx import \
--url git@github.com:chechiachang/serverless-jenkins-quickstart.git
```

---

Update jenkins-x.yml
```
jx create step
git commit
git push
```

---

Trouble Shooting: Failed to get jx resources
```
jx get pipelines
```

Make sure your jx (or kubectl) context is with the correct GKE and namespace
```
kc config set-context gke_my-project_asia-east1-b_jenkins \
  --namespace=jx
```

---

### Helm vs Jenkins X

- [Jenkins Helm Chart](https://github.com/helm/charts/tree/master/stable/jenkins) 
  - create Jenkins master and slave cluster on Kubernetes
  - utilizing the Jenkins Kubernetes plugin.

- Jenkin Platform with jx
  - Jenkins Platform native to Kubernetes
  - Powerful cloud native components: Prow, Nexus, Docker Registry, Tekton Pipeline, ...

---

### Check jenkins-x examples

https://github.com/jenkins-x-buildpacks/jenkins-x-kubernetes/tree/master/packs

---

# jx Client

```
jx get urls

Name                      URL
jenkins                   http://jenkins.jx.11.22.33.44.nip.io
jenkins-x-chartmuseum     http://chartmuseum.jx.11.22.33.44.nip.io
jenkins-x-docker-registry http://docker-registry.jx.11.22.33.44.nip.io
jenkins-x-monocular-api   http://monocular.jx.11.22.33.44.nip.io
jenkins-x-monocular-ui    http://monocular.jx.11.22.33.44.nip.io
nexus                     http://nexus.jx.11.22.33.44.nip.io
```

---

Get Cluster Status

```
jx diagnose
```

Get Applications & Pipelines

```
jx get applications
jx get pipelines
```

---

Get CI Activities & build log

```
jx get activities
jx get activities --filter='jenkins-x-on-kubernetes'

jx get build log

INFO[0003] view the log at: http://jenkins.jx.11.22.33.44.nip.io/job/chechiachang/job/jenkins-x-on-kubernetes/job/feature-add-test/3/console
...
```

---

Trigger Build & Check Activity

```
jx start pipeline
jx start pipeline --filter='jenkins-x-on-kubernetes/feature-add-test'

jx get activities --filter='jenkins-x-on-kubernetes'
```

---

Create Pull Request

```
jx create pullrequest
```

---

#### Summary

- Demonstrate a Jenkins pipeline
- Jenkins plugin
  - master slave cluster
  - kubernetes plugin
  - lovely GUI
- jx on k8s
- jx cli

---

- Jenkins 簡單用
  - 設定與維護人力會比其他工具稍微多

- Jenkins 複雜用
  - Deep Customization: 希望花時間打造最符合自己需求的工具
  - 預期有特殊需求

- Jenkins X
  - 應用依賴 Kubernetes 開發，測試，部屬 (ex. kubernetes client-go)
  - 使用 jx 一站式服務

---
The End
