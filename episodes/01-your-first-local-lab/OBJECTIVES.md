# Episode 01 — learning objectives

By the end of this episode you can:

1. **Clone and enter** `episodes/01-your-first-local-lab` from https://github.com/ibrarahmad/CyberMechanics
2. **Start** two local services with `make lab-up-native` (training app on `:5050`, HTTP demo on `:8080`)
3. **Check** each service with `curl -i` and recognize HTTP **200** as “answered”
4. **Stop only** the demo with `make stop-http-demo` and see **connection refused** on `:8080`
5. **Prove** the training app on `:5050` still answers after the demo stops
6. **Restart** the demo with `make start-http-demo` and confirm HTTP 200 again
7. **Shut down** both managed services with `make lab-down-native`
8. **Run** `make test` to confirm safe process control (including refusing to kill unmanaged listeners)

## Success checklist

- [ ] `curl -i http://127.0.0.1:5050/health` returns 200 and JSON with `"ok": true`
- [ ] Response has exactly one `Server: CyberMechanicsTraining/1.0` header
- [ ] `curl -i http://127.0.0.1:8080/` returns 200 and HTML titled HTTP Demo Service
- [ ] After `make stop-http-demo`, `:8080` fails and `:5050` still returns 200
- [ ] After `make start-http-demo`, `:8080` returns 200 again
- [ ] `make test` passes
