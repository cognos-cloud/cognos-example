# Crypto Agent

Monitors wallets on Solana and Ethereum. Alerts on large movements. Fully read-only.

## What it does

Every 5 minutes:
- Checks SOL and ETH balances for all watched wallets
- Fetches the last 10 transactions per wallet
- Flags any transaction above $10,000 USD
- Simulates flagged transactions to understand what they do
- Sends structured alerts to `#crypto-alerts` in Slack
- Remembers prior balances to detect changes

## Deploy

```bash
pip install cognos
cognos login
cognos deploy
```

## Configure wallets

Edit `agent.py` and add your wallets to the `WATCHED_WALLETS` list:

```python
WATCHED_WALLETS = [
    "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU",  # Solana
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",     # Ethereum
]
```

## Add wallets at runtime (no redeploy)

```bash
curl -X POST https://api.cognoscloud.xyz/v1/agents/crypto-agent/run \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"input": "add wallet 0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B"}'
```

## Alert format

```
🚨 Large movement detected

Wallet:    7xKX...sU
Chain:     Solana
Amount:    50,000 SOL (~$8.2M)
Type:      Token swap
To:        9yZ3...Qm
Explorer:  https://solscan.io/tx/abc123...
Simulated: SOL → USDC via Jupiter aggregator
```

## Execution trace

```
0ms    Cron triggered (*/5 * * * *)
8ms    Memory: loaded prior balances (4 wallets)
90ms   → solana.get_balance(wallet=7xKX...)
210ms  ← solana: 12,400 SOL ($2.04M)
220ms  → solana.get_transactions(wallet=7xKX..., limit=10)
390ms  ← solana: 10 txs — 1 flagged (50,000 SOL)
400ms  → solana.simulate_transaction(tx=sig...)
560ms  ← solana: simulation ok — token swap
580ms  → slack.post(channel="#crypto-alerts", ...)
720ms  ← slack: alert sent
730ms  ● Complete · 730ms · $0.02
```

## Cost

~$0.01–0.03 per run. ~$4–8/month running every 5 minutes.

## Safety

- **Read-only.** Never executes transactions.
- Simulation runs before alerting so you understand what happened.
- Threshold is configurable via `ALERT_THRESHOLD_USD` in `agent.py`.
