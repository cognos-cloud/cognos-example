"""
Research Agent
==============
Searches the web every morning and posts a summary to Slack.

Deploy:
    cognos deploy

What it does:
  1. Triggers at 9am UTC daily via cron
  2. Searches for top AI and tech news from the last 24 hours
  3. Summarises the 5 most important stories
  4. Posts the digest to #research in Slack
  5. Remembers past summaries to avoid repetition
"""

from cognos import Agent

agent = Agent(
    name="research-agent",
    model="gpt-4o",
    memory=True,
    tools=["web", "slack"],
    cron="0 9 * * *",
    instructions="""
    You are a research assistant that delivers a daily AI and tech briefing.

    Every morning:
    1. Search for the top AI and tech news from the last 24 hours using the web tool.
       Use 2–3 specific search queries to get broad coverage.
    2. Check your memory for topics covered in previous summaries — skip repetition.
    3. Summarise the 5 most important stories in plain language:
       - What happened
       - Why it matters
       - Source link
    4. Post the formatted summary to the #research channel in Slack.

    Format:
    🗞 Daily Briefing — {date}

    1. **{Title}** ({source})
    {2-sentence summary}
    → {link}

    ... (5 stories)

    Keep it tight. No filler. Developers are reading this between meetings.
    """,
)

agent.deploy()
