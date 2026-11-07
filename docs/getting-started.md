# Getting started

## 1. What you need

| Tool | Why |
| --- | --- |
| Git | Clone this course |
| Python 3.9+ | Run lab services (standard library) |
| GNU Make | Episode command shortcuts |
| curl | Prove services answered |
| nmap | Episode 02 walkthrough (optional for automated tests) |

Ubuntu example:

```bash
sudo apt update
sudo apt install -y git python3 make curl nmap
```

macOS: install Xcode Command Line Tools (or Homebrew `python` / `make` / `nmap`), then use Terminal.

## 2. Clone the course

```bash
git clone https://github.com/ibrarahmad/CyberMechanics.git
cd CyberMechanics
```

## 3. Verify everything

```bash
make test
```

All episode suites should pass. Then open an episode README and follow the walkthrough.

## 4. Episode entry points

```bash
cd episodes/01-your-first-local-lab && make help
cd episodes/02-nmap-local-port-scan && make help
cd episodes/03-authorization-basics && make help
cd episodes/04-safer-sql-queries && make help
```

## 5. Rules before you type anything

Read [SAFETY.md](../SAFETY.md). Stay on `127.0.0.1`.
