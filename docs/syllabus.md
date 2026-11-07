# Syllabus — Cyber Mechanics

Self-paced course. Complete episodes in order when possible; each builds on local-lab habits from Episode 01.

## Module A — Foundations (local services)

| # | Episode | Learning outcome | Status |
| --- | --- | --- | --- |
| 01 | [Your First Local Lab](../episodes/01-your-first-local-lab/) | Start, check, stop, and restart two independent local HTTP services | **Available** |
| 02 | [Local port discovery with Nmap](../episodes/02-nmap-local-port-scan/) | List open ports on `127.0.0.1` and interpret results without scanning others | **Available** |

## Module B — Web mechanics (authorized demos)

| # | Episode | Learning outcome | Status |
| --- | --- | --- | --- |
| 03 | [Authorization basics](../episodes/03-authorization-basics/) | Distinguish authentication from authorization using a local demo | **Available** |
| 04 | [Safer queries](../episodes/04-safer-sql-queries/) | Replace unsafe string-built SQL with parameterized queries on a local demo | **Available** |

## Assessment style

Every available episode includes:

1. **Objectives** — what “done” means  
2. **Commands** — exact `make` / `curl` / `nmap` steps  
3. **Automated tests** — `make test`  
4. **Deck notes** — short follow-along outline  

Root shortcut: `make test` runs every episode suite.

## Time estimate

| Episode | Hands-on |
| --- | --- |
| 01 | 20–40 minutes |
| 02 | 15–30 minutes |
| 03 | 20–35 minutes |
| 04 | 20–35 minutes |
