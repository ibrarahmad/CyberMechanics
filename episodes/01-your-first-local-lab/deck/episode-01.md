---
title: "Cyber Mechanics E01 — Your First Local Lab"
description: "Beginner diagram first (~12s), then START → CHECK → STOP → VERIFY → RESTORE on Ubuntu (127.0.0.1 only)"
lab_commit: "b43bd0925034c1d39163833ea882fd545b2b2d78"
---

# YOUR FIRST LOCAL LAB: START → CHECK → STOP → VERIFY → RESTORE

**Source:** https://github.com/ibrarahmad/CyberMechanics  
**Folder:** `episodes/01-your-first-local-lab/`  
**Pinned lab commit:** `b43bd09` (`b43bd0925034c1d39163833ea882fd545b2b2d78`)  
**Diagram assets:** `assets/hook/lab-map.svg`, `assets/hook/lab-map-stopped.svg`  
**Production deck:** `/Volumes/data/apps/channels/cybersecurity/e01-first-ethical-hacking-lab/`

HTTP **200** means the service **answered**. It is **not** proof the app is secure.  
**Connection refused** means **nothing is listening** on that port — not that the machine is compromised.  
This lesson does **not** cover authentication or permissions. Loopback only (`127.0.0.1`).

---

## Beginner-first opening (before Ubuntu) — exact 0–12s storyboard

**Purpose:** A complete beginner understands the outcome before any terminal appears.  
The diagram is an **illustrative map**, not live lab evidence. Real proof is the Ubuntu lab that follows.  
Frame **0** must show both services **NOT STARTED**. Never open on RESTORED / settle-end.

### Exact narration (target ~12s; allow ~13s if natural speech needs it)

> Two small websites, one computer. We'll start both. Then we stop one. We prove the other still works. Then we restart it. Here's the Ubuntu lab.

### Sequence

| Time | Show | Spoken | On-screen |
| --- | --- | --- | --- |
| 0.0–2.0 | Same computer, two service boxes, **NOT STARTED** | “Two small websites, one computer.” | `127.0.0.1 = THIS COMPUTER` · 5050 / 8080 |
| 2.0–4.0 | Both boxes green / answered | “We'll start both.” | 5050: ANSWERED · 8080: ANSWERED · HTTP 200 |
| 4.0–6.0 | 8080 red/warn; 5050 stays green | “Then we stop one.” | 8080: STOPPED |
| 6.0–8.0 | Split contrast | “We prove the other still works.” | 8080: CONNECTION REFUSED · 5050: STILL 200 |
| 8.0–10.0 | 8080 restored green | “Then we restart it.” | 8080: RESTORED |
| 10.0–12.0 | Clean cut into Ubuntu | “Here's the Ubuntu lab.” | REAL LAB — UBUNTU |

Helper text (keep short):

- **200** = the page answered  
- **Connection refused** = nothing is listening on that port  
- A **service** = a small local website/program  
- A **port** = an address number on this computer  

### Transition into Ubuntu

Immediately after the last hook line, cut to the authentic Ubuntu desktop and Terminal. No cinematic interstitial. No stale settle-end frame at the edit head.

---

## Follow the lab (real Ubuntu)

| Step | Command |
| --- | --- |
| Clone | `git clone https://github.com/ibrarahmad/CyberMechanics.git` |
| Enter | `cd CyberMechanics/episodes/01-your-first-local-lab` |
| Start | `make lab-up-native` |
| Check training | `curl -i http://127.0.0.1:5050/health` |
| Check demo | `curl -i http://127.0.0.1:8080/` |
| Stop demo | `make stop-http-demo` |
| Prove refused | `curl -i http://127.0.0.1:8080/` → connection refused |
| Prove training | `curl -i http://127.0.0.1:5050/health` → still 200 |
| Restore | `make start-http-demo` then curl `:8080` again |
| Down | `make lab-down-native` |

Expected start lines (no PID on the OK line):

```text
OK training-app listening on 127.0.0.1:5050
OK http-demo listening on 127.0.0.1:8080
```

Single `Server:` header per service (`CyberMechanicsTraining/1.0`, `CyberMechanics-HTTP-Demo/1.0`).

Prerequisites: Python 3.9+, Make, curl. Loopback only. No Docker / Juice Shop in this episode.

---

## Machine map

```
THIS COMPUTER = 127.0.0.1
 ├─ :5050  training-app   GET /health → 200 + JSON
 └─ :8080  http-demo      GET /       → 200 + HTML
```

---

## Recap

**START → CHECK → STOP → VERIFY → RESTORE** on your own safe Ubuntu practice lab.  
All four checklist stages must finish highlighting before the cut.

Code: https://github.com/ibrarahmad/CyberMechanics  

**NEXT EPISODE — ILLUSTRATIVE PREVIEW (not this lesson):** Nmap on `127.0.0.1` only.  
This episode does **not** run Nmap. Preview teaches meaning (OPEN / CLOSED), not live capture.
