+++
title = "Redis Ha on Kubernetes"
subtitle = "Deploy & operate High Available Redis on Kubernetes"

# Add a summary to display on homepage (optional).
summary = "Deploy & operate High Available Redis on Kubernetes"

date = 2019-08-23T16:12:10+08:00
draft = true

# Authors. Comma separated list, e.g. `["Bob Smith", "David Jones"]`.
authors = []

# Is this a featured post? (true/false)
featured = false

# Tags and categories
# For example, use `tags = []` for no tags, or the form `tags = ["A Tag", "Another Tag"]` for one or more tags.
tags = ["kubernetes", "redis", "ci", "cd"]
categories = []

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["deep-learning"]` references 
#   `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
# projects = ["internal-project"]

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder. 
[image]
  # Caption (optional)
  caption = ""

  # Focal point (optional)
  # Options: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight
  focal_point = ""
+++

[Redis](https://redis.io)

[Redis Sentinel](https://redis.io/topics/sentinel) is official solution to High Availablility of Redis. Redis-sentinel provides monitoring to instances, notification on changed behavior, and auto-failover in case a master is down.

[Redis Cluster](https://redis.io/topics/cluster-spec) is a solution to data sharding and automatic management. Data is split across multiple nodes. It also provides some degree of availablity.
