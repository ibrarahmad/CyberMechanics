---
title: "Cyber Mechanics E02 — Local Port Scan with Nmap"
description: "Proof-first 8080 open→closed on 127.0.0.1, then START → SCAN → STOP → RESCAN → RESTART → RESCAN"
lab_commit: "main"
---

# LOCAL NMAP: WATCH PORT 8080 CHANGE

**Source:** https://github.com/ibrarahmad/CyberMechanics  
**Folder:** `episodes/02-nmap-local-port-scan/`  
**Pinned lab commit:** `main` (single commit on this repo — after clone run `git rev-parse HEAD` for the SHA).  
**Shared listeners:** `shared/labctl.py` via `make lab-up-native` / `stop-http-demo` / `start-http-demo`  
**Production deck:** `/Volumes/data/apps/channels/cybersecurity/e02-nmap-port-scanning/`

**Open** = a listener answered. **Closed** = reachable, nothing accepted.  
**Open ≠ vulnerable.** Nmap `SERVICE` names are port-name guesses, not proof of the lab app.

---

## Proof-first opening (before the full walkthrough)

Show genuine before/after **8080** rows from real `nmap -sT -p 5050,8080,9090 127.0.0.1` within the first seconds. Label panels as genuine Nmap. Do **not** invent a `NOTE` column inside stdout.

### Exact narration (target ~11s; prefer clarity)

>Watch port 8080 on this computer. First the scan shows it open. We stop only the demo. The same scan shows it closed. Now we prove that on Ubuntu.

---

## Commands (verified)

```bash
cd CyberMechanics/episodes/02-nmap-local-port-scan
make lab-up-native
nmap -sT -p 5050,8080,9090 127.0.0.1          # 5050/8080 open, 9090 closed
make stop-http-demo                           # → Stopped http-demo
# confirm 8080 not listening (ss/lsof), then:
nmap -sT -p 5050,8080,9090 127.0.0.1          # 8080 closed, 5050 still open
make start-http-demo                          # → OK http-demo listening on 127.0.0.1:8080
nmap -sT -p 5050,8080,9090 127.0.0.1          # 8080 open again
make lab-down-native
```

Or `make scan` for the same Nmap command.

### Illustration vs proof

| Asset | Label |
| --- | --- |
| Opening before/after panels | Genuine scan rows · still a teaching composition |
| Instructor port cards / notes | **INSTRUCTOR NOTE — not Nmap stdout** |
| Ubuntu Terminal + nmap | **REAL PROOF** |

---

## Recap

**SCAN → READ → STOP 8080 → RESCAN → RESTART → RESCAN** on loopback only.

Next: Episode 03 — why access controls matter (200 vs 403). This episode does **not** prove authorization.
