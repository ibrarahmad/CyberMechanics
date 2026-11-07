# Episode 02 — Follow-along notes

**Repo:** https://github.com/ibrarahmad/CyberMechanics  
**Folder:** `episodes/02-nmap-local-port-scan/`

## Hook (illustrative)

Scan this computer → stop one service → scan changes → Ubuntu for real.

## Commands

```bash
cd CyberMechanics/episodes/02-nmap-local-port-scan
make lab-up-native
nmap -sT -p 5050,8080,9090 127.0.0.1
make stop-http-demo
nmap -sT -p 5050,8080,9090 127.0.0.1
make start-http-demo
nmap -sT -p 5050,8080,9090 127.0.0.1
make lab-down-native
```

Open ≠ vulnerable. Closed = nothing listening. Loopback only.
