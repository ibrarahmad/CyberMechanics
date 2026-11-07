# Safer SQL Queries: Fix the Wrong Search

**One unsafe search returns too many products. The safe query treats your input as data — not as SQL code.**

This is Episode 04 of [Cyber Mechanics](https://github.com/ibrarahmad/CyberMechanics). You will call a local product search two ways: a broken string-built query, and a parameterized fix. You will judge success by **counts**, not by memorizing attack strings.

Viewer-facing lessons and videos in this series show numbers. The crafted input lives in **tests**, not in the blog copy you teach aloud.

---

## The idea

The training app keeps a tiny product catalog (five fictional items). Searching for `Sensor` should return **one** row.

| Route | Normal `q=Sensor` | Same crafted lab input |
| --- | --- | --- |
| `/api/products/search/unsafe` | count **1** | count **5** (wrong expansion) |
| `/api/products/search/safe` | count **1** | count **0** (no false matches) |

The safe route keeps the SQL structure fixed and sends the user’s text as a bound value.

---

## What you need

- Python 3.9+, Make, curl
- Episode 03 optional — this episode starts the shared lab itself

---

## Setup

```bash
git clone https://github.com/ibrarahmad/CyberMechanics.git
cd CyberMechanics/episodes/04-safer-sql-queries
make lab-up-native
```

---

## The walkthrough (safe to speak)

### 1. Normal search on the unsafe route

```bash
curl -s 'http://127.0.0.1:5050/api/products/search/unsafe?q=Sensor' | python3 -m json.tool
```

Look at `"count": 1`.

### 2. Same normal search on the safe route

```bash
curl -s 'http://127.0.0.1:5050/api/products/search/safe?q=Sensor' | python3 -m json.tool
```

Still **1**. The fix must not break honest searches.

### 3. Prove the expansion privately with tests

```bash
make test
```

The suite includes the crafted-input comparison (unsafe → 5, safe → 0). That keeps exploit detail out of the README while still verifying the mechanism.

### 4. Shut down

```bash
make lab-down-native
```

---

## What “done” looks like

See [OBJECTIVES.md](OBJECTIVES.md). You can explain why sticking user text into a SQL string is dangerous, and why parameters fix the structure.

Notes: [deck/episode-04.md](deck/episode-04.md).

---

## Series wrap

You have now:

1. Built a local lab  
2. Scanned your own ports  
3. Separated login from permission  
4. Fixed an unsafe search pattern  

Keep those habits on every system you are authorized to test.

---

## Safety

Loopback only. Do not paste intentional unsafe SQL builders into production apps. [SAFETY.md](../../SAFETY.md).
