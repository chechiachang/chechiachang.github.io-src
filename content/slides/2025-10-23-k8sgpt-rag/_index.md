---
title: "K8s Summit 2025: RAG + k8sGPT 檢索增強生成與 K8sGPT"
description: "K8sGPT 是一套結合 AI 與最佳實踐的 Kubernetes 問題診斷與修復工具，能有效降低故障排除難度並自動化修復流程。RAG（Retrieval-Augmented Generation 檢索增強生成）結合檢索系統與生成式模型（如 GPT）的自然語言處理架構，在生成答案時引用外部知識，使模型回答更準確且具事實根據。本演講將介紹如何使用 RAG 技術來增強 Kubernetes 問題診斷與修復的能力，並展示 k8sGPT 的實際應用。"
tags: ["kubernetes", "openai", "gemini", "rag", "aiops", "devops"]
categories: ["kubernetes", "aiops"]
date: '2025-10-01T00:45:00Z'
outputs: ["Reveal"]
reveal_hugo:
  custom_theme: "reveal-hugo/themes/robot-lung.css"
  margin: 0.2
  highlight_theme: "color-brewer"
  transition: "slide"
  transition_speed: "fast"
  templates:
    hotpink:
      class: "hotpink"
      background: "#FF4081"

---

#### Kubernetes Summit 2025
## k8sGPT + RAG 檢索增強生成
##### 用 LLM 自動修復 k8s
##### ~ Che Chia Chang @ [chechia.net](https://chechia.net) ~

---

{{% section %}}

{{< slide content="slides.about-me" >}}
🔽

---

### We're hiring!

https://www.cake.me/companies/maicoin/jobs

![](we-re-hiring.png)

{{% /section %}}

---

### Live demo
##### 不管怎樣先 Live demo :rocket:

https://github.com/chechiachang/k8sgpt-playground

---

https://github.com/chechiachang/k8sgpt-playground/tree/main/k8s

```
minikube config set driver docker
minikube start --kubernetes-version=v1.34.0

helm repo add k8sgpt https://charts.k8sgpt.ai
helm repo update
helm install k8sgpt-operator k8sgpt/k8sgpt-operator --values k8sgpt-operator/values.yaml

kubectl create secret generic azureopenai --from-literal=azure-api-key=your-api-key
# create crd k8sgpt
kubectl create -f config/azureopenai.yaml

kubectl get pods
```

---

```
kubectl logs azureopenai # 確認 LLM backend 連線正常
kubectl get results # results.core.k8sgpt.ai

kubectl apply -f cases/01-missing-image
kubectl get pods -w
kubectl get results -w
kubectl get mutations -w # mutations.core.k8sgpt.ai
```

---

### Live demo 1
##### 所以在座的各位要被取代了嗎？

---

### 大綱

- 不管怎樣先 Live demo :rocket:
- 什麼是 k8sGPT
- 什麼是 RAG
- Live demo 2 :rocket:
- 目前能/不能做什麼
- 如何 get started
- 未來展望

---

### What is K8sGpt

- [https://k8sgpt.ai/](https://k8sgpt.ai/)
- [文件要看這裡 https://docs.k8sgpt.ai/](https://docs.k8sgpt.ai/)
- [cncf sandbox project](https://www.cncf.io/projects/k8sgpt/)

---

### K8sGpt

主要有兩個工具
- [k8sgpt-cli: command line interface](https://github.com/k8sgpt-ai/k8sgpt)
- [k8sgpt-operator](https://github.com/k8sgpt-ai/k8sgpt-operator)

---

##### K8sGpt cli

{{< mermaid >}}
graph TD
    B[k8sgpt-cli]
    subgraph  "kubernetes"
        C[API Server]
    end
    subgraph "LLM AI Backends"
        D["OpenAI API
            gpt-4"]
        E["Google GenAI API
            Gemini Pro"]
    end
    subgraph  "Custom Backend"
        F[其他的 API Backend]
    end
    B --fetch resources, error--> C
    B --prompt + errorMessage--> D
    D --analyzed response--> B
    B --> F
    F --> B
{{< /mermaid >}}

---

##### K8sGpt cli

```
kubectx minikube

k8sgpt auth add --backend azureopenai
k8sgpt analyze --backend azureopenai --explain --filter Pod,Service,Ingress

 100% |█████████████████████████████████████████████████████████| (2/2, 15 it/min)
AI Provider: azureopenai
0: Deployment default/missing-image-deployment()
- Error: Deployment default/missing-image-deployment has 1 replicas but 0 are available with status running
Error: The deployment "missing-image-deployment" in the default namespace has 1 replica defined, but none are currently available or running.

Solution:
1. Check the deployment status: `kubectl describe deployment missing-image-deployment`
2. Look for events indicating issues (e.g., image pull errors).
3. If an image is missing, update the deployment with a valid image: `kubectl set image deployment/missing-image-deployment <container-name>=<new-image>`
4. Redeploy: `kubectl rollout restart deployment/missing-image-deployment`
```

---

![](https://docs.k8sgpt.ai/imgs/operator.png)

https://docs.k8sgpt.ai/reference/operator/overview/

---

##### k8sgpt-operator

1. watch k8s resource
1. analyze: resource + error message 送到 LLM backend (OpenAI, Gemini, ...)
1. calculate remediation: 根據 LLM 回傳的修正建議，產生 k8s 修正後的 yaml
1. 自動化修復 (auto-remediation) apply 修正後的 yaml

---

{{< mermaid >}}
graph TD
    subgraph "k8sgpt-operator controller"
        A["CRD: k8sgpt"]
        B["k8sgpt-controller"]
        C["deployment/k8sgpt"]
        D["mutation-controller"]
        H["k8s resources(Deployment)"]
        I["CRD: Results(error message)"]
        J["CRD: Mutations"]
        K["new k8s resources(Deployment)"]
    end
    B --watches--> A
    B --creates--> C
    C --analyze--> H
    C --creates--> I
    C --calculate remediation--> I
    D --compute similarity score--> J
    D --applys--> K
{{< /mermaid >}}

---

##### k8sgpt-operator 

1. k8sgpt-controller
    1. watches k8sgpt CRD -> create deployment/k8sgpt
    1. analyze
        1. loop fetch resource and error message
        1. send to LLM backend -> get analyzed response
        1. create Result CRD
    1. calculate remediation: compute remediation -> create Mutation CRD
1.  mutation controler
    1. compute similarity score: 計算 config vs targetConfig 差異
    1. ResourceToExecution: execute (apply) resource

---

##### k8sgpt 能做到跟不能做到的事

- 常見問題都是秒解
  - ex. resources issues, typos, misconfigurations, scaling
  - 一個 kubectl apply yaml 就能解決的問題，k8sgpt 都能解決

- 那不常見/複雜的問題呢？
  - domain knowledge
  - multi-step task

---

##### 問題: LLM 直接回答 k8s 問題的挑戰

- LLM 可能會「幻覺」(hallucination)
- 就算答對，沒有幻覺，也無從解釋 LLM 答案的根據
- domain knowledge 不足（公司內部知識庫, runbook, SOP)
- 沒有 tool (上網查k8s 官方文件）
- 其他因素（成本、隱私政策、安全性等）
- 特別需求 ex「沒壞不要動」
- Evaluation

---

RAG: Retrieval-Augmented Generation

{{< mermaid >}}
graph TD
    B[k8sgpt-cli]
    subgraph  "k8s"
        C[API Server]
    end
    subgraph  "Custom Backend"
        H["RAG Retriever
            ex. Python FastAPI"]
        I["LLM Model
            OpenAI gpt-4
            Gemini Pro"]
        K{Knowledge Base}
        L[Official Docs]
        M[Internal Wiki]
        N[SOPs]
    end
    B --> C
    B --> H
    H --query--> K
    K --docs--> H
    H --"promp+query+docs"--> I
    I --response--> H
    K --> L
    K --> M
    K --> N
{{< /mermaid >}}

---

RAG prompt

```
1. 你是一位 Kubernetes 專家。根據以下知識庫文件，分析所提供的錯誤訊息
   並提出可能的原因和解決方案。
2. 如果知識庫中沒有相關資訊，請誠實地說「我不知道」。

知識庫文件:
{檢索到的文件內容}

錯誤訊息:
{錯誤訊息}
```

LLM
```
根據知識庫文件，錯誤訊息顯示 Pod 無法啟動，可能是因為映像檔不存在或無法存取。
請確認映像檔名稱和標籤是否正確，並檢查映像檔倉庫的存取權限。
```

---

### Live demo 2 RAG :rocket:

---

```
cd RAG
cat data/qa.csv

# embedding + save to qdrankjt
kubectl -n qdrant port-forward svc/qdrant 6334:6334 6333:6333
uv run 01_embedding.py
uv run 02_save_to_qdrant.py

# start custom backend RAG server
uv run fastapi dev rag-custom-backend.py

k8sgpt auth add --backend customrest \
    --baseurl http://localhost:8000/completions \
    --model gpt-4o-mini

k8sgpt analyze --backend customrest --explain --filter Deployment
```

---

```
cat deploy/k8sgpt.yaml
kubectl delete -f ../k8s/config/azureopenai.yaml
kubectl apply -f deploy/k8sgpt.yaml

kubectl apply -f ../k8s/cases/02-dont-do-anything
kubectl get pods -w
kubectl get results -w
kubectl get mutations -w # mutations.core.k8sgpt.ai
```

---

### Live demo 2 RAG
##### 所以在座的各位要被取代了嗎？

---

##### RAG: Retrieval-Augmented Generation

1. 讓 LLM 基於外部知識庫來生成答案
  1. 除錯與改進 context engineering
1. 補齊必要知識 domain knowledge
  1. k8s 官方文件
  1. 公司內部知識庫 (wiki, runbook, SOP, etc.)
1. 提供 tools 使用能力 (上網google, github-mcp, jira-mcp, etc.)
1. 通往 Evaluation 的橋樑

---

##### RAG: Retrieval-Augmented Generation

- [2025/10/15 Hello World Dev Workshop](https://chechia.net/posts/2025-10-15-hwdc-rag/)
- embedding, vector database, retriever, evaluation

---

### k8sgpt: Getting Started

所以我要如何開始我的 k8sgpt + RAG 之旅呢？

---

### k8sgpt: Getting Started

- [Playground on Killercoda](https://killercoda.com/matthisholleville/scenario/k8sgpt-cli)
- [Install k8sgpt-cli](https://docs.k8sgpt.ai/getting-started/installation/)
- [CI/CD cronjob example](https://k8sgpt.ai/docs/explanation/integration)
- Deploy to k8s

---

##### Deploy to k8s

- Model hyperparameter to reduce randomness (ex. temperature: 0.0) 🌡️
- Rbac RoleBinding + Role for k8sgpt-operator
- Multi-agent :robot:
- Custom Backend + RAG
- Evaluation
- Go production :rocket:

---

### k8s: rbac RoleBinding + Role

1. 最小權限原則 (least privilege)
1. 解決最大的恐懼：k8sgpt 把我 k8s cluster 弄壞了怎麼辦？

```
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```
---

### k8s: multi-agent 

- 1 個 llm agent 管理整個 cluster
- vs 多個 llm agent 各司其職
  - ns-reader, ns-writer, resource-scaler, cmd-fixer, ...
- context 更好管理，權限管理精細
- 除錯
- Easier to context engineering
- Evaluation

---

### 未來展望

Evaluation + Go to production

> 沒有 Evaluation 就沒有 Production

---

### 所以 SRE 要被取代了嗎？

---

### k8sGPT 能做什麼？

k8sGPT 做得好的事情
- 文字處理：yaml 除錯, typo, 基礎修復
- 24/7 online，秒級修復
- 找出初階錯誤的效率優於人類
- 加上 RAG 可執行有明確 SOP 的事務
- 加上 Tool 可上網查文件 + mcp/jira/github

---

### 未來 SRE 要做的事

- 複雜/超出 scope 的任務還是需要人類 SRE 來處理
  - ex. [https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/](https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/)
- 多步驟決策
- 從處理問題，變成維護 k8sGPT + RAG 系統 + Tools
- 文件 pipeline -> Knowledge Base -> RAG -> Evaluation

---

### Q&A
