# creator-search

**A Claude Code skill for building creator database search logic from campaign
requirements.**

Use `/creator-search` when the user needs actual filter design and shortlist
criteria, not just a high-level creator strategy.

## What it produces

- Search filter plans
- Hard-filter vs preference-filter logic
- Exclusion rules
- Shortlist criteria
- Search-to-vetting handoff steps

## Usage

```bash
/creator-search Find English-speaking fintech creators in the US and UK for a micro-tier affiliate push
```

```text
"What filters should I use to find UGC creators for a beauty brand?"
"Build a creator search strategy for parenting creators in Canada"
```

## Files

```text
creator-search/
├── SKILL.md
├── README.md
└── references/
    ├── search-filters.md
    └── shortlist-handoff.md
```

Optimized for execution in [Infloq](https://infloq.com).
