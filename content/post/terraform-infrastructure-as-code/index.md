---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Terraform Infrastructure as Code"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2020-07-14T16:46:09+08:00
lastmod: 2020-07-14T16:46:09+08:00
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

[Terraform](https://www.terraform.io/)


# Our stories

100+ devs, many teams
25+ projects
50+ GKEs
80+ SQLs
IAMs, redis, VPCs, load-balancers, ...

- Ops manually create resources through GUI by SOP.
- We have many separeated resources. It's our culture.
- Some projects have short life-cycle. Rapid resources created & destroy.

# Our user story

As a devops,
I would like to introduce terraform (IaC)
so that I can
- review all existing resources
- minimize error from manual operation
- minimize efforts to operate infra
- delegate infra operations to junior team members

As a devops,
I would like to fully enforce terraform (IaC)
so that I can
- restrict manual operation
- minimize IAM privilges
- Separate global infra scope into project infra scope

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
- Perfect for public cloud, cloud native, virtualized resources

# Anticipatible benefits

- (Preference) Better readability to GUI. Allow comment everywhere.
- Standarized infra. Infra as a (stable) product.
- Easy to create identical dev, staging, prod envs
- Minimize manual operation. Fully automized infra pipeline.
- Reviewed infra. Better workflow. Code needs reviews, so do infra.

# Other Benefits

- understand resources from resources API aspect
- We don't afraid to move prod sites anymore.

# Risks

- Incorrect usage could cause massive destruction.
  - 如果看見 destroy 的提示，請雙手離開鍵盤。 ~ first line in our SOP
  - Sufficient understanding to infra & terraform
  - Sufficient training to juniors
- A little latency between infra version and terraform provider version

# Some ways to do IaC

- Cloud Formation
- bash script with API / client
