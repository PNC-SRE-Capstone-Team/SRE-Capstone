# SRE-Capstone

## Github Actions
The Github Actions runner is currently deployed on control-plane-1 of the Kubernetes cluster. After it's deployed and authenticated with the script provided by Github, the persistent service is created with the following commands:

```console
sudo nano /etc/systemd/system/github-action-runner.service
```

```ini
[Unit]
Description=My Script Service that starts on internet connection
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/home/op/action-runner/script.sh
RemainAfterExit=yes

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

##