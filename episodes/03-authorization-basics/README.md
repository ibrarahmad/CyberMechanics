# Authorization Basics: Logged In Is Not Enough

**Alice can open her invoice. Bob must not open Alice’s — and “I have a session cookie” is not a free pass.**

This is Episode 03 of [Cyber Mechanics](https://github.com/ibrarahmad/CyberMechanics). You will use a local practice app with two fictional users, **Alice** and **Bob**, and prove the difference between:

- **Authentication** — who you are (you signed in)
- **Authorization** — what you are allowed to see

No Burp Suite required. Terminal `curl` shows the same HTTP status codes.

---

## The story

The training app on `127.0.0.1:5050` has private “invoices” (fake lab data).

| Check | What should happen |
| --- | --- |
| Alice reads **her** invoice `101` on the **safe** route | **200** — allowed |
| Alice reads **Bob’s** invoice `201` on the **unsafe** route | **200** — intentional teaching flaw |
| Alice reads **Bob’s** invoice `201` on the **safe** route | **403** — ownership check refused |

That middle row is the bug you are meant to **see**, not celebrate. The safe route is the finish line.

---

## What you need

- Python 3.9+, Make, curl
- Willingness to stay on loopback

---

## Setup

```bash
git clone https://github.com/ibrarahmad/CyberMechanics.git
cd CyberMechanics/episodes/03-authorization-basics
make lab-up-native
```

---

## The walkthrough

### 1. Sign in as Alice

```bash
curl -i -c cookies.txt -X POST http://127.0.0.1:5050/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"alice"}'
```

You get a session cookie in `cookies.txt`. That proves **who** you are — not what you may read.

### 2. Alice reads her own invoice

```bash
curl -i -b cookies.txt http://127.0.0.1:5050/api/invoices/safe/101
```

Expect **200** and Alice’s fictional invoice.

### 3. Same cookie, Bob’s invoice — unsafe route

```bash
curl -i -b cookies.txt http://127.0.0.1:5050/api/invoices/unsafe/201
```

Expect **200** and Bob’s data. Logged in was treated as “allowed.” That is the lesson’s broken pattern.

### 4. Same request — safe route

```bash
curl -i -b cookies.txt http://127.0.0.1:5050/api/invoices/safe/201
```

Expect **403**. The app checked ownership and refused.

### 5. Clean up

```bash
make lab-down-native
rm -f cookies.txt
```

---

## Tests

```bash
make test
```

Covers Alice→own 200, Alice→Bob unsafe 200, Alice→Bob safe 403.

---

## What “done” looks like

See [OBJECTIVES.md](OBJECTIVES.md). In one sentence: **authentication answers who; authorization answers whether that who may see this object.**

Notes: [deck/episode-03.md](deck/episode-03.md).

---

## Next

| Next | Why |
| --- | --- |
| [04 — Safer SQL queries](../04-safer-sql-queries/) | Wrong product counts → parameterized fix |

---

## Safety

Fictional users and invoices only. Localhost only. Do not copy the unsafe route into production. [SAFETY.md](../../SAFETY.md).
