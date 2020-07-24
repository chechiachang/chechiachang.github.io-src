---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Terraform Infrastructure as Code"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2020-06-14T16:46:09+08:00
lastmod: 2020-06-14T16:46:09+08:00
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

menu:
  main:
    parent: "Kubernetes"
    weight: 1
---

# About this presentation

- [Full transcript]({{< ref "/post/terraform-infrastructure-as-code-transcript" >}})
- [Github get-started / SOP](https://github.com/chechiachang/terraform-playground)
- [chechia.net](https://chechia.net) <- full contents
- [Follow my page to get notification](https://www.facebook.com/engineer.from.scratch)
  - Like it if you really like it :)

# Outlline

- our story: issues, steps, & results
- basics IaC, terraform
- benefits
- risks and 坑
- to be or not to be

experience oriented

# Our stories

- 100+ devs, many teams
- 25+ projects
- 50+ GKEs
- 80+ SQLs
- IAMs, redis, VPCs, load-balancers, ...

# Issues

- Ops manually create resources through GUI by SOP.
- We have many isolated, separeated resources, VPCs. It's our culture, and we (devops) want to change.
- Some projects have short life-cycle. Rapid resources created & destroy.

# Our user story

As a devops,
I would like to introduce terraform (IaC)
so that I can
- review all existing resources
- minimize error from manual operation
- ASAP!!

As a devops,
I would like to fully enforce terraform (IaC)
so that I can
- minimize efforts to operate infra
- delegate infra operations to junior team members
- minimize IAM privilges

# Introduction

1. import existing resources
1. review existing resources code
1. plan best practice resource templates
1. create new resources with templates
1. introduce git workflow, plan, commit, PR, and review
1. add wrapper handler
1. automation pipeline
1. repeat 2-4

# IaC

- Programatic way to operate infra
- declarative (functional) vs. imperative (procedural) 
- Perfect for public cloud, cloud native, virtualized resources
- Benefits: cost (reduction), speed (faster execution) and risk (remove errors and security violations)

# Terraform

[Terraform](https://www.terraform.io/)

- Declarative (functional) IaC
- Invoke API delegation
- State management
- providers: azure / aws / gcp /alicloud / ...

# Demo

https://github.com/chechiachang/terraform-playground

# Scope

- Compute Instances
- Kubernetes
- Databases

- IAM
- Networking
- Load Balancer

# Expected benefits

- Minimize manual operation.
- Zero manual operation error
  - Standarized infra. Infra as a (stable) product.
- fast, really fast to duplicate envs

- Infra workflow with infra review
  - Easy to create identical dev, staging, prod envs
  - Reviewed infra. Better workflow. Code needs reviews, so do infra.
- Fully automized infra pipeline.

# Other Benefits

- Don't afraid to change prod sites anymore
  - We made a massive infra migration in this quater!!
- Better readability to GUI. Allow comment everywhere.

# Risks

- Incorrect usage could cause massive destruction.
  - 如果看見 destroy 的提示，請雙手離開鍵盤。 ~ first line in our SOP
  - If see "destroy", cancel operation & call for help.
- State management
- A little latency between infra version and terraform provider version

# Reduce Risks

- Sufficient understanding to infra & terraform
- Sufficient training to juniors
- Minimize IAM privilege: remove update / delete permissions

# Git-flow

[Our SOP](https://github.com/chechiachang/terraform-playground/blob/master/SOP.md)

- edit tf
- push new branch commit
- PR, review & discussion
- merge & apply
- revert to previous tag if necessary

# (Utility) Provide template

- wrap resources for
  - better accesibility
  - lower operation risks
  - uniform naming convention
  - best practice
  - suggested default value

# About introducing new tool

- The hardest part is always people
  - Focus on critical issues (痛點) instead of tool itself. "We introduce tool to solve..."
  - Put result into statistics "The outage due to misconfig is reduced by..."

# Overall, my IaC experience is GREAT!

- IaC to automation.
- Comment (for infra) is important. You have to write doc anyway. Why not put in IaC?

# Q&A

- [Full transcript]()
- [Presentation file]()
- [Source Code on Github](https://github.com/chechiachang/chechiachang.github.io-src/blob/master/content/post/terraform-infrastructure-as-code/index.md)
- [chechia.net](https://chechia.net) <- full contents
- [Follow my page to get notification](https://www.facebook.com/engineer.from.scratch)
  - Like it if you really like it :)

# Appendix.I more about terraform

terraform validate
terraform import
terraform module
terraform cloud & state management

# Appendix.I understand State conflict

- Shared but synced
- watch out for state conflicts when colaborating
  - state diff. could cause terraform mis-plan
- Solution: synced state lock
  - Colatorative edit (git branch & PR), synchronized terraform plan & apply
  - or better: automation


# Appendix.II understand resources from API aspect

GCP Load Balancer

### GCP Load Balancing

- understand resources from API aspect
  - how terraform work with GCP API

- internal
  - regional
    - pass-through: tcp / udp   -> internal TCP/UDP
    - proxy: http / https       -> internal HTTP(S)
- external
  - regional
    - pass-through: tcp / udp   -> tcp/udp network
  - global / effective regional
    - proxy
      - tcp                     -> TCP Proxy
      - ssl                     -> SSL Proxy
      - http / https            -> External HTTP(S)

### Terraform Resource

- forwarding_rule
  - forwarding_rule: tcp & http
  - global_forwarding_rule: only http

- backend_service
  - backend_service
    - health_check
    - http_health_check
    - https_health_check
  - region_backend_service
    - region_health_check
    - region_http_health_check
    - region_https_health_check

# Some ways to do IaC

- Cloud Formation
- bash script with API / client
