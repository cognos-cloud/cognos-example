# GitHub Agent

Reviews pull requests automatically and sends a daily engineering digest to Slack.

## What it does

**On new PR (via webhook):**
- Reads the full diff and changed files
- Posts a structured code review on the PR
- Returns an approval or request-for-changes verdict
- Flags bugs, edge cases, and security concerns

**Daily at 5pm weekdays (via cron):**
- Lists all open PRs with age and review status
- Flags stale PRs open > 3 days without review
- Posts digest to `#engineering` in Slack

## Deploy

```bash
pip install cognos
cognos login
cognos deploy
```

## Configure the webhook

After deploy, your agent gets a live endpoint. Add it to your GitHub repo:

1. Go to **Settings → Webhooks → Add webhook**
2. Set the payload URL:
   ```
   https://api.cognoscloud.xyz/v1/agents/github-agent/webhook/github
   ```
3. Content type: `application/json`
4. Events: **Pull requests**, **Issues**

## Configuration

Edit `agent.py` to change:
- `cron` — when the daily digest runs (default: 5pm UTC weekdays)
- `instructions` — review criteria, digest format, Slack channel

## Execution trace (PR webhook)

```
0ms    Webhook: pull_request.opened (#142)
18ms   → github.get_pull_request(pr=142)
190ms  ← github: diff returned (1,240 lines)
220ms  → github.get_file_contents(paths=[...])
380ms  ← github: 4 files returned
2.1s   → github.create_review(verdict="approve")
2.4s   ← github: review posted
2.4s   ● Complete · 2.4s · $0.06
```

## Cost

~$0.05–0.10 per PR review. Daily digest ~$0.02.
