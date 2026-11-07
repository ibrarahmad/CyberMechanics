# Episode 04 — Follow-along notes

**Folder:** `episodes/04-safer-sql-queries/`

```bash
make lab-up-native
curl -s 'http://127.0.0.1:5050/api/products/search/unsafe?q=Sensor'
curl -s 'http://127.0.0.1:5050/api/products/search/safe?q=Sensor'
make test
make lab-down-native
```

Parameterized queries keep user text as **data**, not SQL code. Loopback only.
