# Shared lab runtime

Python services used by Episodes **02–04** (and compatible with Episode 01 ports).

| File | Role |
| --- | --- |
| `training_app.py` | `127.0.0.1:5050` — health, login, invoices, product search |
| `http_demo.py` | `127.0.0.1:8080` — second independent listener |
| `labctl.py` | Safe start/stop (managed PIDs only; never kills foreign processes) |

```bash
python3 labctl.py up
python3 labctl.py status
python3 labctl.py stop-demo
python3 labctl.py start-demo
python3 labctl.py down
```

Learners normally use the episode Makefiles instead of calling this folder directly.
