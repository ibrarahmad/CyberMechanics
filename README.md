# Cyber Mechanics

Hands-on cybersecurity labs you run on **your own computer**.

You learn by starting real local services, checking them with ordinary commands, and proving what changed — always on `127.0.0.1` only.

| | |
| --- | --- |
| Level | Beginner → intermediate |
| Format | Self-paced episodes with local practice |
| You need | Python 3.9+, Make, curl (nmap for Episode 02) |
| Scope | **Authorized local practice only** |

These labs teach defensive understanding. They are not attack kits. Never point them at systems you do not own or have written permission to test.

---

## Course map

| # | Episode | What you learn |
| --- | --- | --- |
| **01** | [Your First Local Lab](episodes/01-your-first-local-lab/) | Start two local services, check them with `curl`, stop one, prove the other still runs, restart |
| **02** | [Scan Your Own Ports with Nmap](episodes/02-nmap-local-port-scan/) | See which ports are open on this computer — then watch the scan change when a service stops |
| **03** | [Authorization Basics](episodes/03-authorization-basics/) | Why “logged in” is not the same as “allowed” (HTTP 200 vs 403) |
| **04** | [Safer SQL Queries](episodes/04-safer-sql-queries/) | How an unsafe search returns the wrong result — and how a parameterized query fixes it |

Full outline: [Syllabus](docs/syllabus.md) · New here? [Getting started](docs/getting-started.md)

---

## How to begin

```bash
git clone https://github.com/ibrarahmad/CyberMechanics.git
cd CyberMechanics/episodes/01-your-first-local-lab
```

Open that episode’s README and follow the walkthrough. Complete the episodes in order when you can — each one builds on the last.

---

## Safety (short)

- Stay on `127.0.0.1` (this computer only).
- HTTP **200** means the service **answered** — not that it is secure.
- **Connection refused** means nothing was listening on that local port.

Full rules: [SAFETY.md](SAFETY.md)

---

## License

See [LICENSE](LICENSE).
