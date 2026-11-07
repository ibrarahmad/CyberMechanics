# Episode 01 — requirements

## Required

| Tool | Notes |
| --- | --- |
| Python 3.9+ | Standard library only (no pip packages for this episode) |
| GNU Make | `make` |
| curl | Manual checks in the walkthrough |

## Optional

| Tool | Notes |
| --- | --- |
| nmap | **Not required for Episode 01** (preview for Episode 02) |

## Operating system

Documented for **Ubuntu / Linux** beginners. Also works on macOS with Python 3 and Make. Bind address is always `127.0.0.1`.

## Not required

- Docker
- Juice Shop
- Root / sudo (except optional package install)
- External network targets
- Login credentials
- Exploit tooling

## Install (Ubuntu)

```bash
sudo apt update
sudo apt install -y python3 make curl
```

## Runtime files

Managed PIDs and logs live under gitignored `.run/` in this episode folder. Never commit that directory.
