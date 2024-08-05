---
title: "Kubernetes Summit: Upgrade A VM Based Cluster"
summary: 分享如何升級 VM-based Kubernetes Cluster 的版本，包含 etcd，control plane，與 node。升級前如何規劃，升級步驟該如何操作，升級後應該如何檢查。
authors: []
tags: ["kubernetes"]
categories: ["kubernetes"]
date: '2024-08-04T12:45:00Z'
slides:
  # Choose a theme from https://github.com/hakimel/reveal.js#theming
  #theme: black
  theme: white
  # Choose a code highlighting style (if highlighting enabled in `params.toml`)
  #   Light style: github. Dark style: dracula (default).
  highlight_style: dracula
---

{{< slide background-image="onepiece.png" >}}

{{% speaker_note %}}
投影片跟講稿我都放在我的網站上，如果有興趣可以參考
{{% /speaker_note %}}

---

### Upgrade A VM Based Cluster

[Che Chia Chang](https://chechia.net/)

{{% speaker_note %}}
{{% /speaker_note %}}

---

### 關於我

- Che Chia Chang
- SRE @ [Maicoin](https://www.linkedin.com/company/maicoin/jobs/)
- [Microsoft MVP](https://mvp.microsoft.com/zh-TW/MVP/profile/e407d0b9-5c01-eb11-a815-000d3a8ccaf5)
- 個人部落格[chechia.net](https://chechia.net/)
- presentation and speaker notes
- 鐵人賽 (Terraform / Vault 手把手入門)

---

### 大綱

- [Overview: Official doc](https://kubernetes.io/docs/tasks/administer-cluster/cluster-upgrade/)
- Preflight Check: API Version
- etcd
- kube-apiserver
- kube-controller-manager
- kube-scheduler
- Q&A

{{% speaker_note %}}
{{% /speaker_note %}}

---

### 參考資料

- https://kubernetes.io/docs/tasks/administer-cluster/cluster-upgrade/
