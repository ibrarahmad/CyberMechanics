# Your First Local Lab

**Start two small websites on this computer. Stop one. Prove the other still answers.**

This is Episode 01 of [Cyber Mechanics](https://github.com/ibrarahmad/CyberMechanics) — a beginner lab you run on your own machine. No cloud account. No remote targets. Everything stays on `127.0.0.1`.

---

## Why this lesson exists

Most “hacking” intros jump straight to tools and jargon. This one does the opposite.

Before you scan ports or talk about bugs, you need a **working practice lab**: two independent programs on your computer that you can start, check, stop, and restart — and **prove** what changed.

When you finish, you will have done that for real.

---

## What you will build

| Service | Address | Job |
| --- | --- | --- |
| Training app | `http://127.0.0.1:5050/` | Practice site + `/health` JSON |
| HTTP demo | `http://127.0.0.1:8080/` | A second, separate listener |

Both bind **only** to loopback. Nothing is published to the internet.

Two phrases you will use forever in this course:

- **HTTP 200** → the endpoint **answered** (not “secure”).
- **Connection refused** → **nothing was listening** on that local port (not “hacked”).

---

## What you need

- Python 3.9+
- Make
- curl
- Git

New here? Start with [Getting started](../../docs/getting-started.md) and [SAFETY.md](../../SAFETY.md).

---

## Setup

```bash
git clone https://github.com/ibrarahmad/CyberMechanics.git
cd CyberMechanics/episodes/01-your-first-local-lab
make help
```

---

## The walkthrough

### 1. Start both services

```bash
make lab-up-native
make status
make verify-lab
```

You should see clean OK lines like:

```text
OK training-app listening on 127.0.0.1:5050
OK http-demo listening on 127.0.0.1:8080
```

No process IDs on those OK lines — PIDs stay in `.run/` for `make status`.

### 2. Open the training app

In a browser: [http://127.0.0.1:5050/](http://127.0.0.1:5050/)

Or from Terminal:

```bash
curl -i http://127.0.0.1:5050/health
```

Expect `HTTP/1.0 200 OK` and a small JSON body. One `Server:` header: `CyberMechanicsTraining/1.0`.

### 3. Check the second service

```bash
curl -i http://127.0.0.1:8080/
```

Again: **200**. Banner `CyberMechanics-HTTP-Demo/1.0`. Same computer, different port — a different program.

### 4. Stop only the demo

```bash
make stop-http-demo
curl -i http://127.0.0.1:8080/
```

Expect **connection refused**.

```bash
curl -i http://127.0.0.1:5050/health
```

Expect **still 200**. Stopping 8080 must not take 5050 with it.

### 5. Restore and prove

```bash
make start-http-demo
curl -i http://127.0.0.1:8080/
```

**200** again. Same check before and after — that is how you know discovery (and your own understanding) tracks listeners.

### 6. Shut down

```bash
make lab-down-native
```

---

## Run the tests

```bash
make test
```

The suite starts and stops its own lab. It also checks that unmanaged processes are **not** killed blindly, and that OK lines stay free of PIDs.

---

## What “done” looks like

See [OBJECTIVES.md](OBJECTIVES.md). Short version: you can start, check, stop one service, prove the other still runs, and restore — with commands you could teach a friend.

Follow-along outline: [deck/episode-01.md](deck/episode-01.md).

---

## Next episode

Once this feels boring (in a good way), move on:

| Next | What you learn |
| --- | --- |
| [02 — Scan your own ports with Nmap](../02-nmap-local-port-scan/) | Open vs closed on `127.0.0.1` |
| [03 — Authorization basics](../03-authorization-basics/) | Logged in ≠ allowed |
| [04 — Safer SQL queries](../04-safer-sql-queries/) | Wrong search count → fixed query |

---

## Safety

Authorized **local** practice only. Do not point these commands at other people’s systems. Full policy: [SAFETY.md](../../SAFETY.md).
