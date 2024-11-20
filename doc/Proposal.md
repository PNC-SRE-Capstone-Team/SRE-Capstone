# SRE-Capstone

## Proposal

### Goals and Objectives

- To build a system for detecting credit card fraud using machine learning
- Entire system is implemented using infrastructure as code (IaC)
- Ingestion of credit card activity is trained on and simulated using a sample dataset of 100,000 transactions
- Monitor credit card activity to detect fraudulent transactions in real time
  - Real time transaction data sent to Apache Kafka as processing queue
  - Machine learning model takes transactions from Kafka for classification
  - Classifications are then stored in MongoDB
  - Finally, results are summarized and stored in MariaDB
  - Return classified result and alert on fraudulent transactions
  - Monitor systems using Prometheus
  - Visualize system health and results using Grafana

### Architecture Diagram

![Architecture Diagram](./assets/architecture_diagram.png)

### Tools and Technologies Used

- Apache Kafka
- MongoDB
- MariaDB (MySQL)
- Prometheus
- Grafana
- Kubernetes
- Docker
- Python
- Github Actions
- ArgoCD
- Github
