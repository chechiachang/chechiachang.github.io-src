---
title: "Jenkins X on Kubernetes"
subtitle: ""

# Add a summary to display on homepage (optional).
summary: ""

date: 2019-04-19T12:15:41+08:00
draft: false

# Authors. Comma separated list, e.g. `["Bob Smith", "David Jones"]`.
authors: []

# Is this a featured post? (true/false)
featured: false

# Tags and categories
# For example, use `tags: []` for no tags, or the form `tags: ["A Tag", "Another Tag"]` for one or more tags.
tags: ["jenkins", "ci", "cd", "kubernetes"]
categories: []

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects: ["deep-learning"]` references 
#   `content/project/deep-learning/index.md`.
#   Otherwise, set `projects: []`.
projects: ["jenkins-x-on-kubernetes"]

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder. 
image:
  # Caption (optional)
  caption: "jenkis-x.png"

  # Focal point (optional)
  # Options: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight
  focal_point: "Top"

menu:
  main:
    parent: "Kubernetes"
    weight: 1
---

[Jenkins](https://jenkins.io/) is one of the earliest open source antomation server and remains the most common option in use today. Over the years, Jenkins has evolved into a powerful and flexible framework with hundreds of plugins to support automation for any project.

[Jenkins X](https://jenkins-x.io/), on the other hand, is a CI/CD platform (Jenkins Platform) for modern cloud applications on Kubernetes. 

Here we talk about some basic concepts about Jenkins X and provide a hand-to-hand guide to deploy jenkins-x on Kubernetes.

- [Architecture of Jenkins X](#architecture)
- [Install Jenkins with jx](#install)
- [Create a Pipeline with jx](#pipeline)
- [Develope with jx client](#client)

For more information about jx itself, check [Jenkins-X Github Repo](https://github.com/jenkins-x/jx)

<a name="architecture"></a>

# Architecture

Check this beautiful diagram.

{{< figure library="1" src="jenkins/architecture-serverless.png" title="https://jenkins-x.io/architecture/diagram/" >}}

---

<a name="install"></a>

# Install

### Create GKE cluster & Get Credentials

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

# After cluster initialization, get credentials to access cluster with kubectl
gcloud container clusters get-credentials ${CLUSTER_NAME}

# Check cluster stats.
kubectl get nodes
```

### Install jx on Local Machine

[Jenkins X Release](https://github.com/jenkins-x/jx/releases](https://github.com/jenkins-x/jx/releases)

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

### (Option 1) Install Serverless Jenkins Pipeline

```
DEFAULT_PASSWORD=mySecretPassWord123
jx install \
  --default-admin-password=${DEFAULT_PASSWORD} \
  --provider='gke'
```

Options:

- Enter Github user name
- Enter Github personal api token for CI/CD
- Enable Github as Git pipeline server
- Select Jenkins installation type:
  - [x] Serverless Jenkins X Pipelines with Tekon
  - [ ] Static Master Jenkins
- Pick default workload build pack
  - [x] Kubernetes Workloads: Automated CI+CD with GitOps Promotion
  - [ ] Library Workloads: CI+Release but no CD
- Select the organization where you want to create the environment repository:
  - chechiachang

```
Your Kubernetes context is now set to the namespace: jx
INFO[0231] To switch back to your original namespace use: jx namespace jx
INFO[0231] Or to use this context/namespace in just one terminal use: jx shell
INFO[0231] For help on switching contexts see: https://jenkins-x.io/developing/kube-context/
INFO[0231] To import existing projects into Jenkins:       jx import
INFO[0231] To create a new Spring Boot microservice:       jx create spring -d web -d actuator
INFO[0231] To create a new microservice from a quickstart: jx create quickstart
```

### (Option 2) Install Static Jenkins Server

```
DEFAULT_PASSWORD=mySecretPassWord123

jx install \
  --default-admin-password=${DEFAULT_PASSWORD} \
  --provider='gke'
```

Options:

- Enter Github user name
- Enter Github personal api token for CI/CD
- Enable Github as Git pipeline server
- Select Jenkins installation type:
  - [ ] Serverless Jenkins X Pipelines with Tekon
  - [x] Static Master Jenkins
- Pick default workload build pack
  - [x] Kubernetes Workloads: Automated CI+CD with GitOps Promotion
  - [ ] Library Workloads: CI+Release but no CD
- Select the organization where you want to create the environment repository:
  - chechiachang

```
INFO[0465]Your Kubernetes context is now set to the namespace: jx
INFO[0465] To switch back to your original namespace use: jx namespace default
INFO[0465] Or to use this context/namespace in just one terminal use: jx shell
INFO[0465] For help on switching contexts see: https://jenkins-x.io/developing/kube-context/
INFO[0465] To import existing projects into Jenkins:       jx import
INFO[0465] To create a new Spring Boot microservice:       jx create spring -d web -d actuator
INFO[0465] To create a new microservice from a quickstart: jx create quickstart
```

Access Static Jenkins Server through Domain with username and password
Domain http://jenkins.jx.11.22.33.44.nip.io/

### Uninstall

```
jx uninstall
# rm -rf ~/.jx
```

---
<a name="pipeline"></a>

# Setup CI/CD Pipeline

### Create Quickstart Repository

```
kubectl get pods --namespace jx --watch
```

```
# cd workspace
jx create quickstart
```

Options:

- Which organisation do you want to use? chechiachang
- Enter the new repository name:  serverless-jenkins-quickstart
- select the quickstart you wish to create  [Use arrows to move, type to filter]
  angular-io-quickstart
  aspnet-app
  dlang-http
> golang-http
  jenkins-cwp-quickstart
  jenkins-quickstart
  node-http

```
INFO[0121] Watch pipeline activity via:    jx get activity -f serverless-jenkins-quickstart -w
INFO[0121] Browse the pipeline log via:    jx get build logs chechiachang/serverless-jenkins-quickstart/master
INFO[0121] Open the Jenkins console via    jx console
INFO[0121] You can list the pipelines via: jx get pipelines
INFO[0121] Open the Jenkins console via    jx console
INFO[0121] You can list the pipelines via: jx get pipelines
INFO[0121] When the pipeline is complete:  jx get applications
```

### Check log of the first run

```
jx logs pipeline
```

### Add Step to Pipeline

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

### Check Build Status on Prow (Serverless)

http://deck.jx.130.211.245.13.nip.io/
Login with username and password

### Import Existing Repository

In source code repository:

Import jx to remote jenkins-server. This will apply a Jenkinsfile to repository by default
```
jx import --url git@github.com:chechiachang/serverless-jenkins-quickstart.git
```

Update jenkins-x.yml
```
jx create step
```

git commit & push

### Trouble Shooting

Failed to get jx resources
```
jx get pipelines
```

Make sure your jx (or kubectl) context is with the correct GKE and namespace
```
kc config set-context gke_my-project_asia-east1-b_jenkins \
  --namespace=jx
```

### Why not use helm chart?

It's readlly depend on what we need in CI/CD automation.

[Jenkins Helm Chart](https://github.com/helm/charts/tree/master/stable/jenkins) create Jenkins master and slave cluster on Kubernetes utilizing the Jenkins Kubernetes plugin.
Jenkin Platform with jx is Jenkins Platform native to Kubernetes. It comes with powerful cloud native components like Prow automation, Nexus, Docker Registry, Tekton Pipeline, ...

### Check jenkins-x examples

https://github.com/jenkins-x-buildpacks/jenkins-x-kubernetes/tree/master/packs

---
<a name="client"></a>

# Client

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

### Get Cluster Status

```
jx diagnose
```

### Get Applications & Pipelines

```
jx get applications
jx get pipelines
```

### Get CI Activities & build log

```
jx get activities
jx get activities --filter='jenkins-x-on-kubernetes'

jx get build log

INFO[0003] view the log at: http://jenkins.jx.11.22.33.44.nip.io/job/chechiachang/job/jenkins-x-on-kubernetes/job/feature-add-test/3/console
...
```

### Trigger Build & Check Activity

```
jx start pipeline
jx start pipeline --filter='jenkins-x-on-kubernetes/feature-add-test'

jx get activities --filter='jenkins-x-on-kubernetes'
```

### Create Pull Request

```
jx create pullrequest
```
