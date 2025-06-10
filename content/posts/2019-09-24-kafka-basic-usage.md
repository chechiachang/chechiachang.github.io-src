---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Kafka-basic-usage"
subtitle: ""
summary: ""
authors: []
tags: ["鐵人賽2019", "kafka", "kubernetes", "ithome"]
categories: ["kubernetes", "kafka"]
date: 2019-09-24T21:59:49+08:00
lastmod: 2019-09-24T21:59:49+08:00
featured: false
draft: false
---

[2020 It邦幫忙鐵人賽](https://ithelp.ithome.com.tw/2020ironman) 系列文章

- ELK Stack
  - [Self-host ELK stack on GCP]({{< ref "/posts/2019-09-15-self-host-elk-stack-on-gcp" >}})
  - [Secure ELK Stask]({{< ref "/posts/2019-09-15-secure-elk-stack" >}})
  - [監測 Google Compute Engine 上服務的各項數據]({{< ref "/posts/2019-09-18-monitoring-gce-with-elk" >}})
  - [監測 Google Kubernetes Engine 的各項數據]({{<ref "/posts/2019-09-19-monitoring-gke-with-elk" >}})
  - [是否選擇 ELK 作為解決方案]({{< ref "/posts/2019-09-18-elastic-or-not-elastic" >}})
  - [使用 logstash pipeline 做數據前處理]({{< ref "/posts/2019-09-21-logstash-on-gke" >}})
  - Elasticsearch 日常維護：數據清理，效能調校，永久儲存
  - Debug ELK stack on GCP
- Kafka HA on Kubernetes(6)
  - [Deploy kafka-ha]({{< ref "/posts/2019-09-22-kafka-deployment-on-kubernetes" >}})
  - [Kafka Introduction]({{< ref "/posts/2019-09-23-kafka-introduction" >}})
  - [kafka 基本使用]({{< ref "/posts/2019-09-24-kafka-basic-usage" >}}) 
  - [kafka operation scripts]({{< ref "/posts/2019-09-25-kafka-operation-scripts" >}})
  - [集群內部的 HA topology]({{< ref "/posts/2019-09-25-kafka-ha-topology" >}})
  - [集群內部的 HA 細節]({{< ref "/posts/2019-09-26-kafka-ha-continued" >}})
  - Prometheus Metrics Exporter 很重要
  - 效能調校
  
由於我比較熟悉 GCP / GKE 的服務，這篇的操作過程都會以 GCP 平台作為範例，不過操作過程大體上是跨平台通用的。

寫文章真的是體力活，覺得我的文章還有參考價值，請左邊幫我點讚按個喜歡，右上角幫我按個追縱，底下歡迎留言討論。給我一點繼續走下去的動力。

對我的文章有興趣，歡迎到我的網站上 [https://chechia.net](https://chechia.net) 閱讀其他技術文章，有任何謬誤也請各方大德直接聯繫我，感激不盡。

![Exausted Cat Face](https://d32l83enj9u8rg.cloudfront.net/wp-content/uploads/iStock-966846550-cat-overheating-simonkr-1-940x470.jpg)

---

# 摘要

* 在 Kubernetes 中連線 kafka
* 使用 golang library 連線到 Kafka
* 透過 kafka script 操作 kafka

# kubernetes 中連線 kafka

先看一看 kafka pods

```
$ kubectl get pods --selector='app=kafka'

NAME        READY   STATUS    RESTARTS   AGE
kafka-1-0   1/1     Running   1          26d
kafka-1-1   1/1     Running   0          26d
kafka-1-2   1/1     Running   0          26d

$ kubectl get pods -l 'app=zookeeper'

NAME                  READY   STATUS    RESTARTS   AGE
kafka-1-zookeeper-0   1/1     Running   0          26d
kafka-1-zookeeper-1   1/1     Running   0          26d
kafka-1-zookeeper-2   1/1     Running   0          26d

$ kubectl get pods -l 'app=kafka-exporter'

NAME                               READY   STATUS    RESTARTS   AGE
kafka-1-exporter-88786d84b-z954z   1/1     Running   5          26d
```

```
kubectl describe pods kafka-1-0

Name:           kafka-1-0
Namespace:      default
Priority:       0
Node:           gke-chechiachang-pool-1-e4622744-wcq0/10.140.15.212
Labels:         app=kafka
                controller-revision-hash=kafka-1-69986d7477
                release=kafka-1
                statefulset.kubernetes.io/pod-name=kafka-1-0
Annotations:    kubernetes.io/limit-ranger: LimitRanger plugin set: cpu request for container kafka-broker
Status:         Running
IP:             10.12.6.178
Controlled By:  StatefulSet/kafka-1
Containers:
  kafka-broker:
    Image:         confluentinc/cp-kafka:5.0.1
    Port:          9092/TCP
    Host Port:     0/TCP
    Command:
      sh
      -exc
      unset KAFKA_PORT && \
      export KAFKA_BROKER_ID=${POD_NAME##*-} && \
      export KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://${POD_IP}:9092 && \
      exec /etc/confluent/docker/run

    Requests:
      cpu:      100m
    Liveness:   exec [sh -ec /usr/bin/jps | /bin/grep -q SupportedKafka] delay=30s timeout=5s period=10s #success=1 #failure=3
    Readiness:  tcp-socket :kafka delay=30s timeout=5s period=10s #success=1 #failure=3
    Environment:
      POD_IP:                                   (v1:status.podIP)
      POD_NAME:                                kafka-1-0 (v1:metadata.name)
      POD_NAMESPACE:                           default (v1:metadata.namespace)
      KAFKA_HEAP_OPTS:                         -Xmx4G -Xms1G
      KAFKA_ZOOKEEPER_CONNECT:                 kafka-1-zookeeper:2181
      KAFKA_LOG_DIRS:                          /opt/kafka/data/logs
      KAFKA_CONFLUENT_SUPPORT_METRICS_ENABLE:  false
      KAFKA_DEFAULT_REPLICATION_FACTOR:        3
      KAFKA_MESSAGE_MAX_BYTES:                 16000000
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR:  1
      KAFKA_JMX_PORT:                          5555
    Mounts:
      /opt/kafka/data from datadir (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-2tm8c (ro)
Conditions:
Volumes:
  datadir:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  datadir-kafka-1-0
    ReadOnly:   false
  default-token-2tm8c:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-2tm8c
    Optional:    false
```

講幾個重點：

* 這邊跑起來的是 kafka-broker，接收 producer 與 consumer 來的 request
* 這邊用的是 statefulsets，不是完全無狀態的 kafka broker，而把 message 記在 datadir 上，降低故障重啟時可能遺失資料的風險。
* 啟動時，把 kubernetes 指定的 pod name 塞進環境變數，然後作為當前 broker 的 ID
* 沒有設定 Pod antiAffinity，所以有可能會啟三個 kafka 結果三個跑在同一台 node 上，這樣 node 故障就全死，沒有HA

### Service & Endpoints

看一下 service 與 endpoints
zookeeper 與 exporter 我們這邊先掠過不談，到專章講高可用性與服務監測時，再來討論。

```
$ kubectl get service -l 'app=kafka'

NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
kafka-1            ClusterIP   10.15.242.178   <none>        9092/TCP   26d
kafka-1-headless   ClusterIP   None            <none>        9092/TCP   26d

```

兩個 services

* 一個是 cluster-ip service，有 single cluster IP 與 load-balance，DNS 會過 kube-proxy。
* 一個是 headless service，DNS 沒有過 kube-proxy，而是由 endpoint controller 直接 address record，指向把符合 service selector 的 pod。適合做 service discovery，不會依賴於 kubernetes 的實現。

[詳細說明在官方文件](https://kubernetes.io/docs/concepts/services-networking/service/#headless-services)

簡單來說，kafka broker 會做 auto service discovery，我們可以使用 headless service。

客戶端(consumer & producer) 連入時，則使用 cluster-ip service，做 load balancing。

```
$ kubectl get endpoints -l 'app=kafka'

NAME                            ENDPOINTS                                                          AGE
kafka-1                         10.12.1.14:9092,10.12.5.133:9092,10.12.6.178:9092                  26d
kafka-1-headless                10.12.1.14:9092,10.12.5.133:9092,10.12.6.178:9092                  26d
```

# Golang Example

附上簡單的 Golang 客戶端，[完整 Github Repository 在這邊](https://github.com/chechiachang/kafka-on-kubernetes)

```
package main

import (
	"context"
	"fmt"
	"strconv"
	"time"

	"github.com/segmentio/kafka-go" // 使用的套件
)

func main() {
	topic := "ticker" // 指定 message 要使用的 topic
	partition := 0 // 指定 partition，由於底下連線指定連線到 partition 的 leader，所以需要指定 partition
	kafkaURL := "kafka-0:9092" // 指定 kafkaURL，也可以透過 os.GetEnv() 從環境變數裡拿到。

  // producer 對指定 topic, partition 的 leader 產生連線
	producerConn, _ := kafka.DialLeader(context.Background(), "tcp", kafkaURL, topic, partition)
  // 程式結束最後把 connection 關掉。不關會造成 broker 累積大量 connection，需要等待 broker 端 timeout 才會釋放。
	defer producerConn.Close()

	//producerConn.SetWriteDeadline(time.Now().Add(10 * time.Second))
  // 使用 go routine 跑一個 subprocess for loop，一直產生 message 到 kafka topic，這邊的範例是每秒推一個秒數。
	go func() {
		for {
			producerConn.WriteMessages(
				kafka.Message{
					Value: []byte(strconv.Itoa(time.Now().Second())),
				},
			)
			time.Sleep(1 * time.Second)
		}
	}()

	// make a new reader that consumes from topic-A, partition 0
	r := kafka.NewReader(kafka.ReaderConfig{
		Brokers:   []string{kafkaURL},
		Topic:     topic,
		Partition: 0,
		MinBytes:  10e2, // 1KB
		MaxBytes:  10e3, // 10KB
	})
	defer r.Close()
	//r.SetOffset(42)

  // 印出 reader 收到的 message
	for {
		m, err := r.ReadMessage(context.Background())
		if err != nil {
			break
		}
		fmt.Printf("%v message at offset %d: %s = %s\n", time.Now(), m.Offset, string(m.Key), string(m.Value))
	}

}
```

這邊可以使用 Dockerfile 包成一個 container image，然後丟上 kubernetes

我稍晚補一下 docker image 跟 deployment 方便大家操作好了。

或是攋人測試，直接 kubectl run 一個 golang base image 讓它 sleep，然後在連進去
```
kubectl run DEPLOYMENT_NAME --image=golang:1.13.0-alpine3.10 sleep 3600

kubectl exec -it POD_NAME sh
```

```
# 裡面沒有 Git 跟 vim 裝一下
apk add git vim

go get github.com/chechiachang/kafka-on-kubernetes

cd src/github.com/chechiachang/kafka-on-kubernetes/
vim main.go

go build .
./kafka-on-kubernetes

2019-09-24 14:20:46.872554693 +0000 UTC m=+9.154112787 message at offset 1:  = 46
2019-09-24 14:20:47.872563087 +0000 UTC m=+9.154121166 message at offset 2:  = 47
2019-09-24 14:20:48.872568848 +0000 UTC m=+9.154126926 message at offset 3:  = 48
2019-09-24 14:20:49.872574499 +0000 UTC m=+9.154132576 message at offset 4:  = 49
2019-09-24 14:20:50.872579957 +0000 UTC m=+9.154138032 message at offset 5:  = 50
2019-09-24 14:20:51.872588823 +0000 UTC m=+9.154146892 message at offset 6:  = 51
2019-09-24 14:20:52.872594672 +0000 UTC m=+9.154152748 message at offset 7:  = 52
2019-09-24 14:20:53.872599986 +0000 UTC m=+9.154158060 message at offset 8:  = 53
```

這樣就連上了，完成一個最簡單的使用範例。

這個例子太過簡單，上一篇講的 consumer group, partitions, offset 什麼設定全都沒用上。實務上這些都需要好好思考，並且依據需求做調整設定。

### Clean up

把測試用的 deployment 幹掉

```
kubectl delete deployment DEPLOYMENT_NAME
```

# 小結

* 簡述 kafka 在 kubernetes 上運行的狀況，連線方法
* Demo 一個小程式
