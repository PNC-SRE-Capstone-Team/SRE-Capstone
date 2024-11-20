from kafka.admin import KafkaAdminClient

admin_client = KafkaAdminClient(
    bootstrap_servers='10.100.200.23:9094',  # Replace with your broker address
    client_id='kafka-admin-client'
)

# List all consumer groups
consumer_groups = admin_client.list_consumer_groups()
topics = admin_client.list_topics()

for topic in topics:
    print(topic)

print("Consumer Groups:")
for group in consumer_groups:
    print(group)
