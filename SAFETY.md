# Safety & authorized use

Cyber Mechanics is an **educational** project. Labs exist so beginners can practice on a machine they control.

## Allowed

- Running labs on your own computer (`127.0.0.1` / localhost).
- Following lesson commands exactly as written.
- Modifying lab code **locally** to learn how it works.

## Not allowed

- Pointing lab tools or scans at other people’s systems (including Episode 02 Nmap — loopback only).
- Using these materials to break into, disrupt, or probe networks without written authorization.
- Publishing secrets, real credentials, or personal data inside lab configs.
- Copying intentional teaching flaws (unsafe invoice route, string-built SQL) into production systems.

## What status codes mean here

| Observation | Meaning in this course |
| --- | --- |
| HTTP 200 | The local service answered |
| Connection refused | No process accepted the connection on that local port |
| Port in use (error from `labctl`) | Something else already owns that port — free it or stop the foreign process |

HTTP 200 does **not** mean the application is secure.

## Reporting issues

If a lab ever tries to bind outside loopback, or a script suggests targeting a remote host, open an issue and stop using that revision until it is fixed.
