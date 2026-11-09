---
title: "Cyber Mechanics E03 — Authorization Basics"
description: "Alice 200 vs Bob 403 on 127.0.0.1 — ownership check, Terminal only"
lab_commit: "main"
---

# AUTHORIZATION: 200 VS 403

**Source:** https://github.com/ibrarahmad/CyberMechanics  
**Folder:** `episodes/03-authorization-basics/`  
**Pinned lab commit:** `main` (single commit on this repo — after clone run `git rev-parse HEAD` for the SHA).  
**Production deck:** `/Volumes/data/apps/channels/cybersecurity/e03-burp-authorization/`

**HTTP 200** = the app answered with data.  
**HTTP 403** = the app refused this user.  
Being signed in is not the same as being allowed.

## Opening map (illustrative — E01 style)

### Exact narration (hook)

> One user. One invoice. Alice can open her own. Bob must not. Now we prove that on Ubuntu.

Alice opens her own invoice → 200.  
Bob must not open Alice’s invoice → 403 on the safe route.  
Then prove it on Ubuntu.

## Commands

```bash
cd CyberMechanics/episodes/03-authorization-basics
make lab-up-native
curl -i -c cookies.txt -X POST http://127.0.0.1:5050/login \
  -H 'Content-Type: application/json' -d '{"username":"alice"}'
curl -i -b cookies.txt http://127.0.0.1:5050/api/invoices/safe/101     # 200
curl -i -b cookies.txt http://127.0.0.1:5050/api/invoices/unsafe/201   # 200 flaw
curl -i -b cookies.txt http://127.0.0.1:5050/api/invoices/safe/201     # 403 fix
make lab-down-native
```

No Burp required — Terminal shows the same status codes. Loopback only.
