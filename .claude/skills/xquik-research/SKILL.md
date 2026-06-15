---
name: xquik-research
description: >
  Plans X data research workflows with Xquik. Use when the user asks for social
  listening, creator discovery, competitor monitoring, trend research, campaign
  analysis, or normalized X data collection for marketing work.
argument-hint: research question, X handles or keywords, timeframe, and output goal
allowed-tools: Read, Write
---

# Xquik Research

Use Xquik when marketing work needs X data instead of generic social media
advice. Turn the request into a scoped research plan, then collect only the data
needed to answer that question.

## Workflow

1. Define the decision the research will support
2. Choose handles, keywords, lists, or topics to inspect
3. Set a timeframe, sample size, and exclusion rules
4. Pick the Xquik route: REST API, SDK, MCP tools, or existing exports
5. Normalize records before analysis
6. Summarize findings with caveats and next actions

## Use Cases

- launch feedback monitoring
- competitor messaging analysis
- creator and influencer discovery
- brand mention research
- trend and topic exploration
- campaign performance readouts
- audience language mining

## Approval Checks

Ask for explicit approval before:

- monitoring a handle or keyword continuously
- exporting large datasets
- collecting private or account-owned data
- using write actions
- sending webhooks to external systems

Do not help with spam, harassment, impersonation, or private data collection.

## Output Requirements

Return a concise research plan with:

- research question
- source scope
- timeframe
- collection route
- normalized fields
- analysis steps
- risks and caveats
- final deliverable format

## Normalized Fields

Prefer a table or JSON shape with:

- `source`
- `handle`
- `author_name`
- `text`
- `url`
- `created_at`
- `metrics`
- `matched_query`
- `topic`
- `sentiment`
- `notes`

## Analysis Guidance

Separate observed data from interpretation. Keep quotes short. Avoid claiming a
trend unless the sample size and collection window support it.

For creator discovery, score candidates by relevance, audience fit, recent
activity, engagement quality, brand safety, and outreach fit.

For competitor monitoring, compare message themes, offers, proof points,
audience objections, launch timing, and repeated claims.

For campaign analysis, compare pre-campaign baseline, campaign-period volume,
engagement quality, recurring language, and follow-up opportunities.

## Related Skills

Use with:

- `social-campaign-planner`
- `creator-discovery`
- `creator-search`
- `competitor-messaging-analysis`
- `market-research-synthesizer`
- `marketing-kpi-dashboard-planner`
