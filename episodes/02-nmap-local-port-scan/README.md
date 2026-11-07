# Scan Your Own Ports with Nmap

**Ask one computer a simple question: which ports are open right now?**

This is Episode 02 of [Cyber Mechanics](https://github.com/ibrarahmad/CyberMechanics). You already know how to start and stop local services. Now you will **watch those facts show up in a scan** — then change the lab and watch the scan change with it.

Scope is strict: **`127.0.0.1` only**. You are not scanning the internet.

---

## The idea in plain English

A **port** is just a number a program uses to receive connections on this computer.

- **Open** → a program answered.
- **Closed** → nothing listened.

Open does **not** mean vulnerable. It only means something is listening.

In this lab you will look at three numbers:

| Port | Story |
| --- | --- |
| **5050** | Training app (should be open while the lab is up) |
| **8080** | HTTP demo (open, then closed when you stop it, then open again) |
| **9090** | Nothing here — stays closed on purpose |

---

## What you need

- Episode 01 habits (or just follow along — this episode starts the shared lab itself)
- Python 3.9+, Make, curl
- **nmap** for the human walkthrough (`make test` works even without nmap)

Install nmap on Ubuntu with `sudo apt install nmap`, or on macOS with Homebrew.

---

## Setup

```bash
git clone https://github.com/ibrarahmad/CyberMechanics.git
cd CyberMechanics/episodes/02-nmap-local-port-scan
make lab-up-native
make verify-lab
```

---

## The walkthrough

### 1. First scan

```bash
make scan
# same as: nmap -sT -p 5050,8080,9090 127.0.0.1
```

Read the table. You want **5050** and **8080** open, **9090** closed.

### 2. Predict, then stop one service

Out loud: *If I stop only the demo on 8080, the next scan should show 8080 closed and 5050 still open.*

```bash
make stop-http-demo
make scan
```

That before-and-after is the whole lesson.

### 3. Restore and confirm

```bash
make start-http-demo
make scan
```

8080 open again. Same command, new truth.

### 4. Shut down

```bash
make lab-down-native
```

---

## Automated checks

```bash
make test
```

These tests use socket probes so CI and machines without nmap still pass. Use `make scan` when you want the real Nmap output on your screen.

---

## What “done” looks like

See [OBJECTIVES.md](OBJECTIVES.md). You can explain open vs closed, and you can make the scan change by stopping and starting one local service.

Notes: [deck/episode-02.md](deck/episode-02.md).

---

## Next

| Next | Why |
| --- | --- |
| [03 — Authorization basics](../03-authorization-basics/) | Being logged in is not the same as being allowed |
| [04 — Safer SQL queries](../04-safer-sql-queries/) | One unsafe search, one safe fix |

---

## Safety

Loopback only. Never point `nmap` at hosts you do not own or lack written permission to test. [SAFETY.md](../../SAFETY.md).
