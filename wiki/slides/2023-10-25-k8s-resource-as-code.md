# Kubernetes Summit: Resource as Code for Kubernetes: Stop kubectl apply

- Source: `content/slides/2023-10-25-k8s-resource-as-code/_index.md`
- Slide: `https://chechia.net/slides/2023-10-25-k8s-resource-as-code/`
- Date: `2023-10-23T00:00:00Z`
- Tags: `kafka, kubernetes`
- Categories: `kubernetes`
- Description: `將 k8s resource 以 code 管理，推上 vcs，並使用 argoCD, secret operator 等工具進行管理，來讓避免低級的人工操作錯誤，降低團隊整體失誤率，並降低 k8s admin 管理的成本，提高管理效率`

## Pages (Section | Summary)

1. `(frontmatter)` | Frontmatter metadata for reveal-hugo settings and slide metadata.
2. `(frontmatter)` | Q1: 有過使用 helm 跟 argocd 的人請舉手
3. `Resource as Code for K8s Object` | Resource as Code for K8s Object
4. `Outline` | Outline
5. `Kubectl` | Kubectl
6. `(frontmatter)` | 首先，如同官方文件所描述，kubectl 的使用上，也有各種不同方法。ie. kubectl 交在不同人手上，使用方式是不同的
7. `Issue` | Issue
8. `Issue` | Issue
9. `Declarative object configuration` | Declarative object configuration
10. `(frontmatter)` | 有人在 2014 年前用過 k8s 嗎？
11. `Helm chart` | Helm chart
12. `Helm Chart Library` | Helm Chart Library
13. `helm 生態系` | helm 生態系
14. `更高層級的封裝` | 更高層級的封裝
15. `微服務` | 微服務
16. `Issues` | Issues
17. `Argo CD` | Argo CD
18. `Why Argo CD?` | Why Argo CD?
19. `Argo CD` | Argo CD
20. `applicationset` | applicationset
21. `applicationset` | applicationset
22. `cluster-wide 的 k8s object` | cluster-wide 的 k8s object
23. `Issues` | Issues
24. `More Issues: multi-hybrid cluster` | More Issues: multi-hybrid cluster
25. `More Issues: multi-hybrid cluster` | More Issues: multi-hybrid cluster
26. `More Issues: multi-hybrid cluster` | More Issues: multi-hybrid cluster
27. `More Issues: multi-hybrid cluster` | More Issues: multi-hybrid cluster
28. `More Issues: Test` | More Issues: Test
29. `Test: ansible playbook` | Test: ansible playbook
30. `More Issues: Test` | More Issues: Test
31. `More Issues: Test` | More Issues: Test
32. `Summary` | Summary

## Time-to-Syntax

- Markdown:
- `p3:link`
- `p5:code-fence`
- `p5:link`
- `p7:code-fence`
- `p9:code-fence`
- `p12:code-fence`
- `p13:code-fence`
- `p13:link`
- `p14:code-fence`
- `p17:image`
- `p17:link`
- `p20:code-fence`
- `p20:link`
- `p21:code-fence`
- `p25:code-fence`
- `p25:link`
- `p26:code-fence`
- `p26:link`
- `p29:code-fence`
- Hugo shortcode:
- `p2:{{< slide background-image="onepiece.jpg" >}}`
- `p2:{{% note %}}`
- `p2:{{% /note %}}`
- `p3:{{% note %}}`
- `p3:{{% /note %}}`
- `p4:{{% note %}}`
- `p4:{{% /note %}}`
- `p5:{{% note %}}`
- `p5:{{% /note %}}`
- `p6:{{< slide background-image="kubectl.jpg" >}}`
- `p6:{{% note %}}`
- `p6:{{% /note %}}`
- `p7:{{% note %}}`
- `p7:{{% /note %}}`
- `p8:{{% note %}}`
- `p8:{{% /note %}}`
- `p9:{{% note %}}`
- `p9:{{% /note %}}`
- `p10:{{< slide background-image="helm.jpg" >}}`
- `p10:{{% note %}}`
- `p10:{{% /note %}}`
- `p11:{{% note %}}`
- `p11:{{% /note %}}`
- `p12:{{% note %}}`
- `p12:{{% /note %}}`
- `p14:{{% note %}}`
- `p14:{{% /note %}}`
- `p16:{{% note %}}`
- `p16:{{% /note %}}`
- `p18:{{% note %}}`
- `p18:{{% /note %}}`
- `p19:{{% note %}}`
- `p19:{{% /note %}}`
- `p20:{{% note %}}`
- `p20:{{% /note %}}`
- `p22:{{% note %}}`
- `p22:{{% /note %}}`
- `p24:{{% note %}}`
- `p24:{{% /note %}}`
- `p26:{{% note %}}`
- `p26:{{% /note %}}`
- `p28:{{% note %}}`
- `p28:{{% /note %}}`
- `p30:{{% note %}}`
- `p30:{{% /note %}}`
- `p31:{{% note %}}`
- `p31:{{% /note %}}`
- Reveal-hugo syntax:
- none.

## Time-to-Sentence

- Markdown:
- `p1:title: "Kubernetes Summit: Resource as Code for Kubernetes: Stop kubectl apply"`
- `p1:description: "將 k8s resource 以 code 管理，推上 vcs，並使用 argoCD, secret operator 等工具進行管理，來讓避免低級的人工操作錯誤，降低團隊整體失誤率，並降低 k8s admin 管理的成本，提高管理效率"`
- `p2:Q1: 有過使用 helm 跟 argocd 的人請舉手`
- `p2:Q2: k8s object 走 gitflow 管理的比例有超過 9 成的`
- `p3:Resource as Code for K8s Object`
- `p4:kubectl 使用，然後官方有提醒我們使用 kubectl 管理 k8s object 時的 trade-off，這些 trade-off 我們可以使用其他的工具來彌補`
- `p4:導入 helm chart，來打包 k8s objects 變成一個完整地發布單位`
- `p4:然後在 workflow 裡加入測試，確保 k8s objects 的交付品質`
- `p5:kubectl create deployment nginx --image nginx`
- `p5:作為官方的 cli 工具，kunectl 非常強大，可以控制幾乎大部分 k8s 的 api，也能對幾乎所有 k8s object 進行操作`
- `p6:kubectl create deployment nginx，一行命令告訴 k8s 你要 create deployment`
- `p6:kubectl create -f nginx.yaml，使用者選擇要 create / apply / delete 而 nginx.yaml 裡面描述一個 nginx deployment 物件`
- `p6:kubectl apply -f -R nginx/，使用者描述一個或多個物件，描述物件的狀態。apply 時，由 kubectl 決定要對 object 執行，create / update / delete`
- `p7:kubectl create deployment nginx --image nginx`
- `p7:kubectl 這麼好用，那為何不繼續用下去？`
- `p7:2.3. 的問題，你必須對 object 夠了解，才寫得出完整沒 bug 的 spec yaml`
- `p7:聽起來是最完整的，他的問題就是要如何維持 local file 與 live 連結，或是說 sync`
- `p8:change review / diff before apply`
- `p8:change review / diff before apply`
- `p9:microservice-a b c ...`
- `p9:為了 change review，通常會走向 3. Declarative object configuration，可能會長這樣`
- `p9:使用 kubectl 一次 apply 整個 directory，所以 local file 基本上也反應 live object`
- `p9:PR -> review -> merged -> apply master / release tag`
- `p10:有人在 2014 年前用過 k8s 嗎？`
- `p10:古早時期，要用個 redis 還要自己包 service / ingress / deployment，先去 dockerhub 找 redis，然後依據 readme 自己包 deployment，自己測試看 redis 會不會動`
- `p10:現在應該沒有人會因為要去使用 redis 或是 mysql，自己跑去寫 k8s object 了吧`
- `p10:如果只是使用低三方開源的 helm chart，社群幫你維護 service / ingress / deployment`
- `p10:跑得起來後，跑得好，能使用 k8s orchestration 提供完整的功能，透過 value.yaml 控制`
- `p11:chart 作為一個 k8s object 的 release / artifact，有開發流程，版本控管，測試，完整的發佈`
- `p11:app 本身，例如 redis，當然是整個應用的核心。但要能夠在 k8s 執行，並正確地享受 k8s orchestration 的好處，k8s object 非常的重要`
- `p11:甚至，k8s object 複雜度已經遠遠超過過去在 vm 上跑一個 redis，兜一個 systemd unit 就可以跑起來`
- `p11:k8s object 需要 release / version，才能做 object 的固定版本 apply，upgrade 生版，有問題 rollback`
- `p14:例如我有一百個 api service group，都是 restful api，都需要 ingress / service / nginx 等等`
- `p14:例如 daemon service，底下依賴 queue / redis / db`
- `p16:V change review / diff before apply`
- `p16:ex. 可以跑 for loop / for each`
- `p16:這個在 IaC 或是 resource as code 的 xxx as code 都十分有利`
- `p18:Why Argo CD?`
- `p18:Application definitions, configurations, and environments should be declarative and version controlled. Application deployment and lifecycle management should be automated, auditable, and easy to understand.`
- `p18:描述 application 本身，附帶的設定 secret / configmap`
- `p18:UI 圖像描述，一目瞭然。但事實上如果有做到講 local file 推到版本控制，光是使用 editor 也可以做到一目瞭然`
- `p19:argocd application sync file from repository`
- `p19:k8s object 的 change 是需要 PR review 的，不是想改就 kubectl apply 下去`
- `p19:能夠直接掌握 live object，透過 editor 檢查 git repository，或是透過 argocd UI 檢視`
- `p19:在複雜的環境裡很重要，ex. k8s 內有成千上百個 helm release，可以用 editor 檢視 local file`
- `p20:applicationset 定義一組 set，可以透過 generator 迭代的產生大量的 application`
- `p22:使用 helm template helper 來管理 value.yaml label / annotation / env / ...`
- `p22:cluster-wide 的 k8s object 也很適合塞進 argocd 管理`
- `p22:例如 cluster access control，複雜的 rbac rule，也很適合整理成為 helm chart`
- `p23:V change review / diff before apply`
- `p24:由於 k8s 內部的 component 都已經標準化，可以很輕易地複製測試過的 component`
- `p24:dev 測試 PR branch，staging 跑 release candicate，production 選擇經過測試的 release`
- `p24:能夠確保 dev / stag / prod 的 k8s object 是完全相同的`
- `p24:hybrid 環境管理，某些 k8s 元件應該安裝在哪些 cluster 上`
- `p24:aws ingress controller / csi driver / cni node daemonsets`
- `p28:stress / load test / chaos engineering`
- `p28:當然，有測試的 helm releae 與沒測試的 helm release 也是天差地遠`
- `p29:測試 apply 後 k8s object 的 status`
- `p29:shell: kubectl get deployment {{ deployment_name }} -o=jsonpath='{.status.readyReplicas}'`
- `p29:fail_msg: 'Deployment {{ deployment_name }} is not running.'`
- Hugo shortcode:
- `p2:{{< slide background-image="onepiece.jpg" >}}`
- `p2:{{% note %}}`
- `p2:{{% /note %}}`
- `p3:{{% note %}}`
- `p3:{{% /note %}}`
- `p4:{{% note %}}`
- `p4:{{% /note %}}`
- `p5:{{% note %}}`
- `p5:{{% /note %}}`
- `p6:{{< slide background-image="kubectl.jpg" >}}`
- `p6:{{% note %}}`
- `p6:{{% /note %}}`
- `p7:{{% note %}}`
- `p7:{{% /note %}}`
- `p8:{{% note %}}`
- `p8:{{% /note %}}`
- `p9:{{% note %}}`
- `p9:{{% /note %}}`
- `p10:{{< slide background-image="helm.jpg" >}}`
- `p10:{{% note %}}`
- `p10:{{% /note %}}`
- `p11:{{% note %}}`
- `p11:{{% /note %}}`
- `p12:{{% note %}}`
- `p12:{{% /note %}}`
- `p14:{{% note %}}`
- `p14:{{% /note %}}`
- `p16:{{% note %}}`
- `p16:{{% /note %}}`
- `p18:{{% note %}}`
- `p18:{{% /note %}}`
- `p19:{{% note %}}`
- `p19:{{% /note %}}`
- `p20:{{% note %}}`
- `p20:{{% /note %}}`
- `p22:{{% note %}}`
- `p22:{{% /note %}}`
- `p24:{{% note %}}`
- `p24:{{% /note %}}`
- `p26:{{% note %}}`
- `p26:{{% /note %}}`
- `p28:{{% note %}}`
- `p28:{{% /note %}}`
- `p30:{{% note %}}`
- `p30:{{% /note %}}`
- `p31:{{% note %}}`
- `p31:{{% /note %}}`
- Reveal-hugo syntax:
- none.
