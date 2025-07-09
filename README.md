# ⚙️ Pharos Testnet Bot

Additional features will be added gradually, run the `update.bat` file periodically

---
## 🧩 Modules

- Login accounts and save sessions
- Fetching native and stable faucet 
- Completing daily checkin
- Completing onchain tasks (swap, send tokens, buy tokens, liquidity)
- Mint Gotchipus NFT  
- Mint testnet badge

---

## ⚙️ Requirements
- Python 3.13
- Proxies (optional)

---

## 🚀 Quick Start Guide
1. Use `git clone https://github.com/overcodeme/pharos-testnet.git` in console
2. Use `cd pharos-testnet` in console
3. Run `install.bat` file to install dependencies
4. Run `start.bat` and choose any option

---

## 🔧 Configuration

Put your private keys in `data/wallets.txt`:
```
private_key1
private_key2
```

Put your proxies in `data/proxies.txt`:
```
ip:port
http://ip:port
http://user:pass@ip:port
```

Configuring `settings.yaml`:
- ATTEMPTS: amount of retries
- SLEEP_DURATION: sleep between tasks and actions
- TASKS: types of tasks
- TASK_COUNT: task count
- AMOUNT: spending during the task
