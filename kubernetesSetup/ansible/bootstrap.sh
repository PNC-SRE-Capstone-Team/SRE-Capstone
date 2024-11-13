#!/bin/sh

echo "Setting up primary server 1"
k3sup install --host 10.100.200.28 \
--user op \
--cluster \
--local-path kubeconfig \
--context default \
--k3s-extra-args "--disable traefik"

echo "Fetching the server's node-token into memory"

export NODE_TOKEN=$(k3sup node-token --host 10.100.200.28 --user op)

echo "Setting up additional server: 2"
k3sup join \
--host 10.100.200.29 \
--server-host 10.100.200.28 \
--server \
--node-token "$NODE_TOKEN" \
--user op \
--k3s-extra-args "--disable traefik" &

echo "Setting up additional server: 3"
k3sup join \
--host 10.100.200.23 \
--server-host 10.100.200.28 \
--server \
--node-token "$NODE_TOKEN" \
--user op \
--k3s-extra-args "--disable traefik" &

echo "Setting up worker: 1"
k3sup join \
--host 10.100.200.32 \
--server-host 10.100.200.28 \
--node-token "$NODE_TOKEN" \
--user op &

echo "Setting up worker: 2"
k3sup join \
--host 10.100.200.33 \
--server-host 10.100.200.28 \
--node-token "$NODE_TOKEN" \
--user op &

echo "Setting up worker: 3"
k3sup join \
--host 10.100.200.35 \
--server-host 10.100.200.28 \
--node-token "$NODE_TOKEN" \
--user op &

