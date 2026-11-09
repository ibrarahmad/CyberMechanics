---
title: "Cyber Mechanics E01 — Your First Local Lab"
description: "Beginner diagram first (~12s), then START → CHECK → STOP → VERIFY → RESTORE on Ubuntu (127.0.0.1 only)"
lab_commit: "main"
---

# YOUR FIRST LOCAL LAB: START → CHECK → STOP → VERIFY → RESTORE

**Source:** https://github.com/ibrarahmad/CyberMechanics  
**Folder:** `episodes/01-your-first-local-lab/`  
**Pinned lab commit:** `main` (single commit on this repo — after clone run `git rev-parse HEAD` for the SHA).  
**Diagram assets:** `assets/hook/lab-map.svg`, `assets/hook/lab-map-stopped.svg`  
**Editable production hook:** channels deck `components.js` → `LabHookDiagram` (SVG wires + cards)  
**Production deck:** `/Volumes/data/apps/channels/cybersecurity/e01-first-ethical-hacking-lab/`

HTTP **200** means the service **answered**. It is **not** proof the app is secure.  
**Connection refused** means **nothing is listening** on that port — not that the machine is compromised.  
This lesson does **not** cover authentication or permissions. Loopback only (`127.0.0.1`).

---

## Beginner-first opening (before Ubuntu) — V4 compact hook

**Purpose:** A complete beginner understands the outcome before any terminal appears.  
The diagram is an **illustrative map**, not live lab evidence. Real proof is the Ubuntu lab that follows.  
Frame **0** must show both services **NOT STARTED**. Never open on RESTORED / settle-end. Never open on a dark cinematic reset (V3 defect — fixed in V4).

### Exact recorded narration (target ~11–13s; prefer clean delivery over a rushed 11s)

>Two small websites on one computer. Both answer. Stop just the second one. The first keeps working. Start it again. Now we prove that on Ubuntu.

### Sequence (adjust to final Kokoro timings)

| Time (approx) | Show | Spoken | On-screen readable label |
| --- | --- | --- | --- |
| 0.0–1.5 | Machine diagram, **NOT STARTED** 5050/8080, subtle first motion | “Two small websites on one computer.” | TWO SMALL WEBSITES · ONE COMPUTER |
| 1.5–3.0 | Both services green; connectors light | “Both answer.” | BOTH ANSWER · HTTP 200 |
| 3.0–4.6 | 8080 amber STOPPED, 5050 stays green | “Stop just the second one,” | STOP 8080 |
| 4.6–6.7 | 8080 red REFUSED, 5050 green STILL 200 | “The first keeps working.” | 8080 REFUSED · 5050 STILL ANSWERS |
| 6.7–8.9 | Restart 8080, green RESTORED | “Start it again.” | 8080 RESTORED |
| 8.9–11.8+ | Cut to genuine Ubuntu + first project command | “Now we prove that on Ubuntu.” | REAL UBUNTU LAB · LOCAL ONLY |

Helper text (one big definition at a time; do not rely on color alone):

- **200** = the page answered  
- **Refused** = nothing listening on this port  
- A **service** = a small local website/program  
- A **port** = an address number on this computer  

### Transition into Ubuntu

Immediately after the last hook line, cut to the authentic Ubuntu desktop and Terminal. No cinematic interstitial. No Google Flow / stock “hacker” footage. No stale settle-end frame at the edit head.

Phone readability for the Ubuntu half uses **CMD / RESULT title strips** over the real session (not camera zoom that replaces the desktop). Keep terminal chrome, prompt, and genuine output visible.

---

## Two listeners on this computer

| Port | Program | Start | Stop | Check |
| --- | --- | --- | --- | --- |
| **5050** | Training app (`training_app.py`) | `make lab-up-native` (or stays up when demo stops) | `make lab-down-native` | `curl -i http://127.0.0.1:5050/health` |
| **8080** | HTTP demo (`http_demo.py`) | `make lab-up-native` / `make start-http-demo` | `make stop-http-demo` | `curl -i http://127.0.0.1:8080/` |

Independent processes: stopping 8080 must leave 5050 answering HTTP 200. That contrast is the episode’s highest-value proof.

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

## Illustration vs real proof

| Asset | Label |
| --- | --- |
| Opening `LabHookDiagram` / SVG maps | ILLUSTRATIVE MAP — not live evidence |
| Ubuntu Terminal + curl / make | REAL PROOF — local lab on this computer |
| End Nmap teaser | ILLUSTRATIVE PREVIEW — NOT A LIVE NMAP CAPTURE |

---

## Recap

**START → CHECK → STOP → VERIFY → RESTORE** on your own safe Ubuntu practice lab.  
All four checklist stages must finish highlighting before the cut.

Code: https://github.com/ibrarahmad/CyberMechanics  

**NEXT EPISODE — ILLUSTRATIVE PREVIEW (not this lesson):** Nmap on `127.0.0.1` only.  
This episode does **not** run Nmap. Preview teaches meaning (OPEN / CLOSED), not live capture.
