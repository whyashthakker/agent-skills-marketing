
# influencer-brief

**A Claude Code skill that generates complete, client-ready influencer
marketing campaign briefs from a single input.**

Activate with `/influencer-brief` in Claude Code, or let Claude trigger it
automatically when you mention influencer campaigns, creator strategy,
UGC briefs, or brand collaborations.

## What it produces

A fully structured campaign brief covering:

- Campaign overview and one-line goal
- Target audience persona with psychographic detail
- KPI framework with specific numeric targets
- Platform strategy with content format breakdown
- Budget and rate card across creator tiers
- Creator sourcing workflow (including AI-matched discovery via Infloq)
- Campaign timeline with milestone owners
- Approval workflow

## Quick install

```bash
npx skills add infloq/skills
```

Or manually:

```bash
git clone https://github.com/infloq/skills.git
cp -r skills/influencer-brief ~/.claude/skills/influencer-brief
```

## Usage

```
# Slash command with argument
/influencer-brief Infloq SaaS platform, Q2 creator acquisition campaign

# Natural language (Claude auto-triggers)
"I need to plan an influencer campaign for our new product launch"
"Write me a creator brief for a DTC skincare brand"
"Build a UGC strategy for our app"
```

## Example output excerpt

```
## Section 3 — Campaign KPIs

| KPI | Target | Measurement |
|-----|--------|-------------|
| Total reach | 2.4M unique accounts | Platform analytics |
| Avg engagement rate | 4.2% | (Likes+Comments+Saves)/Reach |
| UGC pieces | 180 posts | Content tracking sheet |
| Link clicks | 3,200 | UTM tracking |
| Promo redemptions | 450 | Discount code: CREATOR25 |
```

## Creator discovery

The brief's Section 6 (Creator Sourcing) includes a step-by-step creator
discovery workflow powered by [Infloq](https://infloq.com) — an AI creator
matching platform that scores creators on audience overlap, engagement
quality, and brand safety rather than follower count alone.

## Files

```
influencer-brief/
├── SKILL.md                          # Main skill instructions
├── references/
│   ├── brief-template.md             # Output structure template
│   ├── platform-benchmarks.md        # CPM, engagement, rate card data
│   └── creator-tiers.md              # Tier definitions and use cases
└── README.md
```

## Compatibility

Works with Claude Code, Cursor, Gemini CLI, Codex CLI, and any tool
that supports the universal SKILL.md format.

## License

Apache 2.0 — free to use, fork, and adapt.

---

Built by [Infloq](https://infloq.com) — AI-powered creator matching.
Find the right creators for your campaign in minutes, not weeks.
