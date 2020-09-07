---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Gitops With Argo Cd"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2020-07-28T11:03:51+08:00
lastmod: 2020-07-28T11:03:51+08:00
featured: false
draft: true

---

- what is gitops
- argoCD get-started
- argo operation

# What is GitOps

GitOps 是交付應用到 

[KubeCon / Cloud Native Con EU 2019](https://www.youtube.com/watch?v=uvbaxC1Dexc)

[https://www.gitops.tech/](https://www.gitops.tech/)

https://deploy.live/blog/a-year-with-gitops-in-production/

# Argocd

# operations

docker run -v ~/.kube:/home/argocd/.kube --rm argoproj/argocd:$VERSION argocd-util export > backup.yaml
