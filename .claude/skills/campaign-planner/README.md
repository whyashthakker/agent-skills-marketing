# campaign-planner

**A Claude Code skill for building execution-ready creator campaign plans from
goal, budget, timing, and audience inputs.**

Use `/campaign-planner` when you need deliverables, KPIs, timeline, tier mix,
and operational steps rather than a loose strategy memo.

## What it produces

- Campaign summary and objective framing
- Creator tier and channel mix
- Deliverables and KPI tables
- Budget allocation
- Timeline and owner mapping
- Risk and dependency notes

## Usage

```bash
/campaign-planner Consumer app launch, $40k budget, 6-week campaign, TikTok-first
```

```text
"Plan a creator campaign for our new product launch"
"Build a UGC plus affiliate campaign with clear KPIs"
```

## Files

```text
campaign-planner/
├── SKILL.md
├── README.md
└── references/
    ├── campaign-types.md
    └── planning-template.md
```

This skill is designed to hand off cleanly into execution inside
[Infloq](https://infloq.com).
