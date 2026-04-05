# ghchecker

## Configuration as a daemon

### /etc/systemd/system/ghchecker.service

```
[Unit]
Description=GitHub New Release Checker

[Service]
Type=oneshot
User=root
ExecStart=/root/.cargo/bin/uv run python3 ghchecker/ghchecker.py
WorkingDirectory=/opt/ghchecker

[Install]
WantedBy=multi-user.target
```

### /etc/systemd/system/ghchecker.timer

```
[Unit]
Description=GitHub New Release Checker Timer

[Timer]
OnCalendar=*-*-* *:00/20:00
Persistent=true
AccuracySec=1m

[Install]
WantedBy=timers.target
```

### Configuring systemctl

```
systemctl daemon-reload
systemctl enable ghchecker.timer
systemctl start ghchecker.timer
```
