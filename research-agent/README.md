# Research Agent

Searches the web every morning and posts a structured briefing to Slack.

## What it does

- Triggers at 9am UTC daily via cron
- Searches for top AI and tech news from the last 24 hours
- Summarises the 5 most important stories in plain language
- Posts the digest to `#research` in Slack
- Remembers prior summaries to avoid repetition (`memory=True`)

## Deploy

```bash
pip install cognos
cognos login
cognos deploy
```

## Configuration

Edit `agent.py` to change:
- `cron` — when it runs (default: daily at 9am UTC)
- `instructions` — what topics to cover, which Slack channel to post to
- `model` — which LLM to use

## Execution trace

```
0ms    Cron triggered (0 9 * * *)
12ms   Memory: loaded 8 prior summaries
240ms  → web.search("top AI news last 24h")
910ms  ← web: 14 results (670ms)
1.2s   → web.search("tech funding news today")
1.8s   ← web: 9 results (580ms)
3.1s   → slack.post(channel="#research")
3.4s   ← slack: message sent
3.5s   ● Complete · 3.5s · $0.04
```

## Cost

~$0.03–0.05 per run. ~$1/month.
