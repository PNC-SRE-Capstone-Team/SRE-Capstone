# Proactive Nonsense Crusher
## Credit Card Fraud Detection

Alex Griffin  
Balin Warren  
Chadon Mathurin  
Daniel Nelson

---

### Goals and Objectives

- To build a system for detecting credit card fraud using machine learning
- Using sound engineering practices:
  - Implement using infrastructure as code (IaC)
  - Automated deployment and CI/CD
  - Horizontally scalable architecture (microservices)
  - Instrumented and monitored

---

![Architecture Diagram](./assets/architecture_diagram.png)

---

### Computing Infrastructure

- Running on self-hosted Proxmox server
- HPE ProLiant DL380 Gen9 Server
- Virtual machines provisioned with Terraform
- Kubernetes cluster configured with Ansible

---

### Docker and Kubernetes

- Docker is a container engine for developing, shipping, and running applications
  - More lightweight than virtual machines
- Kubernetes is a container orchestration platform for managing a computing cluster made up of many containerized services

---

### CI/CD

- K3s Kubernetes cluster managed by ArgoCD
- Component services are defined as Dockerfiles and ArgoCD Applications
- GitHub Action workflows deploy  Kubernetes objects defined in git repository
- Build artifacts pushed to private container registry
- Secrets managed by GitHub to avoid unwanted exposure of sensitive data

---

### Ingress Nginx

- Single point of entry into the cluster
- Routes domains and paths to services
- Cert-manager to provision, install, and rotate Cloudflare SSL certificates

---
### Ingesting Credit Card Transactions

- Credit card transaction dataset
  - https://www.kaggle.com/datasets/anurag629/credit-card-fraud-transaction-data/data
- Recorded information:

```txt
Transaction ID,Date,Day of Week,Time,Type of Card,Entry Mode,Amount,Type of Transaction,Merchant Group,Country of Transaction,Shipping Address,Country of Residence,Gender,Age,Bank,Fraud
#3577 209,14-Oct-20,Wednesday,19,Visa,Tap,£5,POS,Entertainment,United Kingdom,United Kingdom,United Kingdom,M,25.2,RBS,0

```

- Python script reads transaction log and feeds data into Apache Kafka

---

### Apache Kafka

- Open-source stream-processing platform

  <!-- Designed for high-throughput, fault-tolerant, and real-time data streaming. -->

- Core Concepts
  - Producers, <!-- Applications that publish data to Kafka topics. -->
    Consumers, <!-- Applications that read data from topics. -->
    Topics, <!-- Categories or feed names to which messages are published. -->
    Partitions, <!-- Sub-divisions of topics for parallel processing. -->
    Brokers <!-- Servers that store and serve messages; form a Kafka cluster. -->

- Use Cases
  - Real-time analytics and monitoring
  - Log aggregation and stream processing
  - Event sourcing and data integration

---

### Fraud Classification

Winning Model (Random Forest):

![Model](.\classifier\training\modelThree\confusion_matrix.png)

---

scikit-learn Classification Model

```python
    # Initialize the model. Class weight is being set due to 
    # imbalance of fraud/not fraud cases
    model = RandomForestClassifier(n_estimators=50, 
      max_depth=10, random_state=42, 
      class_weight={0: 1, 1: 8})
    
    # Split chunk into training and validation subsets
    X_train_chunk, X_val_chunk, y_train_chunk, y_val_chunk = 
    train_test_split(
        X_chunk, y_chunk, test_size=0.2, random_state=42
    )
    
    # Train the model incrementally
    model.fit(X_train_chunk, y_train_chunk)  
```

---

### MongoDB and MariaDB (MySQL)

- MariaDB
  - Open Source branch of MySQL
  - Built to easily scale out
  - Easily multithread for higher transaction throughput

- MongoDB
  -  Scalable (Shardable)
  -  Quickly integrate with microservices
  -  Flexible data structure

---

### Summary Scripts
- Purpose is to take the large amounts of transaction logs and compile into digestible summaries.
- Ingests transaction logs from MongoDB.
- Tabulates data of all transactions into summaries every 5 minutes.
- Generates one summary for all transactions and another summary for just fraud transactions.
- Summaries get inserted into MySQL tables
- Frequency of summaries can be easily adapted to account for volume.

  
---

### Monitoring and Dashboards

---

### Potential Next Steps

1. Detailed tracing of microservices with Jaeger
2. Oauth2 Integration with Ingress Nginx
3. Active-Active node/cluster failover
4. Dev environment with canary releases
5. Hardening checklist for each application
6. App of Apps deployment pattern

---

<!-- Repeat this slide at the end after going through each component. -->
![Architecture Diagram](./assets/architecture_diagram.png)

---

### Questions?
