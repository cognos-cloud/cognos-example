"""
Crypto Agent
============
Monitors wallets on Solana and Ethereum, alerts on large movements.
Fully read-only — never executes transactions.

Deploy:
    cognos deploy

What it does (every 5 minutes):
  1. Checks SOL and ETH balances for all watched wallets
  2. Fetches the last 10 transactions per wallet
  3. Flags any transaction > $10,000 USD equivalent
  4. Simulates flagged transactions to understand intent
  5. Sends structured alerts to #crypto-alerts in Slack

Add wallets at runtime via the API — no redeploy needed.
"""

from cognos import Agent

# Add your wallets here
WATCHED_WALLETS = [
    "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU",  # Solana example
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",     # Ethereum example
]

ALERT_THRESHOLD_USD = 10_000

agent = Agent(
    name="crypto-agent",
    model="gpt-4o",
    memory=True,
    tools=["solana", "ethereum", "slack"],
    cron="*/5 * * * *",
    instructions=f"""
    You are an on-chain monitoring agent. You are read-only — you never execute transactions.

    Watched wallets:
    {chr(10).join(f'  - {w}' for w in WATCHED_WALLETS)}

    Alert threshold: ${ALERT_THRESHOLD_USD:,} USD

    === Every run ===

    1. For each watched wallet:
       a. Check current balance (SOL or ETH depending on chain)
       b. Fetch the last 10 transactions
       c. Compare balances to memory — flag significant changes (>5%)

    2. For each transaction above the alert threshold:
       a. Simulate the transaction using the chain's simulation tool
       b. Determine: token swap, transfer, NFT purchase, contract interaction, etc.

    3. Send a Slack alert to #crypto-alerts for any flagged transaction.

    Alert format:
    🚨 Large movement detected

    Wallet:   {'{'}wallet_short{'}'}
    Chain:    Solana / Ethereum
    Amount:   {'{'}amount{'}'} {'{'}token{'}'} (~${'{'}usd_value{'}'})
    Type:     {'{'}transaction_type{'}'}
    To:       {'{'}counterparty_short{'}'}
    Explorer: {'{'}explorer_link{'}'}
    Simulated: {'{'}what_it_does{'}'}

    4. Update memory with current balances for next comparison.

    === If prompted via API ===

    If the input contains "add wallet {'{'}address{'}'}", add it to the monitoring list
    and confirm in Slack.

    If the input contains "remove wallet {'{'}address{'}'}", remove it and confirm.

    Never execute transactions. Monitoring and alerting only.
    """,
)

agent.deploy()
