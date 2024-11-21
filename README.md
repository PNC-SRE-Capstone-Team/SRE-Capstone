# SRE-Capstone

Alex Griffin, Balin Warren, Chadon Mathurin, Daniel Nelson

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

## Github Actions

GitHub Actions is used as the CI/CD tool for all services. Build artifacts are pushed to a private [GitHub Container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry), and secrets are managed as GitHub Actions secrets which are only accessible through GitHub Action workflows.

### Hosting the GitHub Actions Runner
The Github Actions runner is currently deployed on control-plane-1 of the Kubernetes cluster. This allows the runner to directly perform kubectl, argocd, and helm commands without needing to open public access to the cluster or provision a jumpbox and enable ssh. After it's deployed and authenticated with the script provided by Github, the persistent service is created with the following commands:

```console
sudo nano /etc/systemd/system/github-action-runner.service
```

```ini
[Unit]
Description=Github Action Runner Service
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/home/op/action-runner/run.sh
Restart=always
User=op

[Install]
WantedBy=multi-user.target
```

```console
sudo systemctl daemon-reload
sudo systemctl enable github-action-runner.service
sudo systemctl start github-action-runner.service
```

You can check to make sure that it's authenticated and waiting for jobs with the command
```console
sudo systemctl status github-action-runner.service
```

The download, extraction, and installation of the service can eventually be ported over to ansible, but this is non-critical.

## Computing Infrastructure
The computing infrastructure used for this project is self-hosted, running on an HPE ProLiant DL380 Gen9 Server. It is running the Proxmox virtual machine platform, a free alternative to commercial platforms like VMWare ESXi. Virtual machines for the Kubernetes cluster are provisioned on top of Proxmox with Terraform. To safeguard the infrastructure from hostile actors on the internet, the machines are only accessible over the network to authenticated users with the Tailscale mesh VPN.

## Kubernetes
The K3s project is used as the basic for the Kubernetes cluster. The control plane and nodes are provisioned with Terraform and then configured with Ansible.

### Namespaces
A number of namespaces are used to logically divide the Kubernetes cluster semantically:

- argocd
- cert-manager
- database
- default
- ingress-nginx
- kafka
- kube-node-lease
- kube-public
- kube-system
- monitoring

## Kafka Transaction Log Microservice
The kafkaSendLogs microservice is deployed within the `kafka` namespace within the Kubernetes cluster, as it interacts exclusively with the Apache Kafka database. It reads the transaction log and feeds it into Kafka as a queue for further processing.

This is a small sample of the recorded information contained in the dataset:

```csv
Transaction ID,Date,Day of Week,Time,Type of Card,Entry Mode,Amount,Type of Transaction,Merchant Group,Country of Transaction,Shipping Address,Country of Residence,Gender,Age,Bank,Fraud
#3577 209,14-Oct-20,Wednesday,19,Visa,Tap,£5,POS,Entertainment,United Kingdom,United Kingdom,United Kingdom,M,25.2,RBS,0

```

The data is read into Python, converted into a dictionary object, serialized to JSON, and finally sent to Kafka.

## Credit Card Fraud Transaction Dataset
This dataset was used as the basis for the transaction logs and machine learning models:

- https://www.kaggle.com/datasets/anurag629/credit-card-fraud-transaction-data/data

## Summary Script Microservice
The summary script microservice is deployed within the `database` namespace within the Kubernetes cluster. This made the most sense as the purpose of the service was to ingest logs from MongoDB, interpret and summarize those logs, and then finally insert a summary into the MySQL database every five minutes. Here are the main pieces of code that make the service work: 

#### Scheduler
The scheduler is used to both find logs from the last 5 minutes as well as sleep the program between queries:
```python
now = datetime.now(timezone.utc)

date = now.date()
timestamp = now.time()

time_start = str((now - timedelta(minutes=5)).time())
time_end = str(timestamp)
date_string = str(date)

next_task = (now + timedelta(minutes=5))
sleep_time = (next_task - now).total_seconds()
```

#### Summary Builder
The summary builder is the function that ingests the Mongo logs and tabulates the data into the 5 minute summaries. We decided on building summaries for 2 tables, one for all transaction summaries and another for only fraud transactions. Most fields were simply tabulated, for example we counted how many transactions came from each country, but for transaction amounts we found it would be more effective to average it.

The base summary builder python creates the dictionaries that will store our data and sends it to the counting function before converting the dictionaries to JSON and shipping it to the SQL query builder.
```python
def build_summaries(docs):
    for doc in docs:

        if doc["Fraud"] == 1:
             count_data(all_transactions, fraud_transactions, doc, True)
        else:
             count_data(all_transactions, fraud_transactions, doc, False)

    #get average amount

    all_transactions['Average Amount'] = get_average_amount(all_transactions['Average Amount'])
    fraud_transactions['Average Amount'] = get_average_amount(fraud_transactions['Average Amount'])

    jsonify(all_transactions, fraud_transactions)

    return [all_transactions, fraud_transactions]
```

The count data function is how we are interpreting the data coming from the Mongo logs and adding it to the tally within the transaction dictionaries.
```python
def count_data(all_transactions_dict, fraud_transactions_dict, data_dict, is_fraud):
    categories = ["Type of Card", "Entry Mode", "Type of Transaction", "Merchant Group", "Country of Transaction", "Shipping Address", "Country of Residence", "Bank"]

    for category in categories:
        if data_dict[category] in all_transactions_dict[category]:
                all_transactions_dict[category][data_dict[category]] += 1
        else:
            all_transactions_dict[category].update({data_dict[category]: 1})

        if is_fraud:
            if data_dict[category] in fraud_transactions_dict[category]:
                fraud_transactions_dict[category][data_dict[category]] += 1
            else:
                fraud_transactions_dict[category].update({data_dict[category]: 1})
                

    all_transactions_dict["Average Amount"].append(data_dict["Amount"])

    if is_fraud:
        fraud_transactions_dict["Average Amount"].append(data_dict["Amount"])
        all_transactions_dict["Fraud"] += 1
```

After the data has been tabulated and the amounts have been averaged the script will convert the dictionaries to JSON and return the JSON to the main function to be used in the SQL queries.

#### SQL Query Builder
In order to automate the process of inserting the data into MySQL we had to create a function that would make the SQL queries with the data given. Since we have 2 summaries that don't share all the same fields the function simply runs a check to see what fields the JSON has and returns the corresponding SQL query as well as the data for that query packaged in a tuple for the MySQL Cursor.

```python
def build_query(summary):
        query = """
        INSERT INTO transaction_summaries (
            created_at,
            card_type, 
            entry_mode, 
            average_amount, 
            transaction_type, 
            merchant_group, 
            transaction_country,
            shipping_address,
            residence_country,
            bank,
            fraud_count
        ) VALUES (
            NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )"""

        data = (
            summary["Type of Card"], 
            summary["Entry Mode"], 
            summary["Average Amount"], 
            summary["Type of Transaction"], 
            summary["Merchant Group"], 
            summary["Country of Transaction"], 
            summary["Shipping Address"], 
            summary["Country of Residence"],
            summary["Bank"],
            summary["Fraud"]
            )

    return query, data
```

After the main function receives the query and data back, it inserts it into the designated tables, closes the database connections, and then sleeps for 5 minutes before the next summary will be made.

##
