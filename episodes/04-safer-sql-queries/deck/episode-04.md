---
title: "Cyber Mechanics E04 — Safer SQL Queries"
description: "Unsafe search returns too much; safe parameterized query treats input as data"
lab_commit: "main"
---

# SAFER SEARCH: DATA, NOT CODE

**Source:** https://github.com/ibrarahmad/CyberMechanics  
**Folder:** `episodes/04-safer-sql-queries/`  
**Pinned lab commit:** `main` (single commit on this repo — after clone run `git rev-parse HEAD` for the SHA).  
**Production deck:** `/Volumes/data/apps/channels/cybersecurity/e04-sql-injection-fix/`

**Unsafe** = user text is glued into the query string.  
**Safe** = the query stays fixed; user text is data only.

## Opening map (illustrative — E01 style)

### Exact narration (hook)

> Wrong search, then fixed search. A normal search looks fine. A bad input on the unsafe route returns too much. The safe route treats input as data. Now Ubuntu.

Normal search → one product.  
Unsafe crafted input → too many rows.  
Safe crafted input → zero extras.  
Then prove it on Ubuntu.

## Commands

```bash
cd CyberMechanics/episodes/04-safer-sql-queries
make lab-up-native
curl -s 'http://127.0.0.1:5050/api/products/search/unsafe?q=Sensor'
curl -s 'http://127.0.0.1:5050/api/products/search/safe?q=Sensor'
make test
make lab-down-native
```

Loopback only. Keep practice on computers you own.
