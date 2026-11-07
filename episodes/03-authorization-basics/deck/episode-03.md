# Episode 03 — Follow-along notes

**Folder:** `episodes/03-authorization-basics/`

```bash
make lab-up-native
curl -i -c cookies.txt -X POST http://127.0.0.1:5050/login \
  -H 'Content-Type: application/json' -d '{"username":"alice"}'
curl -i -b cookies.txt http://127.0.0.1:5050/api/invoices/safe/101     # 200
curl -i -b cookies.txt http://127.0.0.1:5050/api/invoices/unsafe/201   # 200 flaw
curl -i -b cookies.txt http://127.0.0.1:5050/api/invoices/safe/201     # 403 fix
make lab-down-native
```

No Burp required — Terminal shows the same HTTP status codes.
