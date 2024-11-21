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

- K3s kubernetes cluster managed by ArgoCD
- Component services are defined as Dockerfiles and Kubernetes manifests
- GitHub Action workflows deploy  Kubernetes objects defined in git repository
- Build artifacts pushed to private container registry
- Secrets managed as GitHub secrets to avoid unwanted exposure of sensitive data

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

---

### Fraud Classification

---

### MongoDB

---

### Summary Scripts

---

### MariaDB (MySQL)

---

### Monitoring and Dashboards

---

<!-- Repeat this slide at the end after going through each component. -->
![Architecture Diagram](./assets/architecture_diagram.png)

---

### Questions?
