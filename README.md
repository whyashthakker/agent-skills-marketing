# Infloq Skills

A reusable library of Claude Code style skills for marketing, creator
operations, SEO, GEO, lifecycle, and campaign execution.

These skills live under [`.claude/skills`](/Users/yash/code/infloq-skill/.claude/skills) and are designed to be used in two ways:

1. Use the repo as a full skill library.
2. Copy individual skill folders into your own local `.claude/skills/` directory.

## What These Skills Are

Each skill is a self-contained folder with:

- `SKILL.md` for trigger rules and workflow instructions
- `README.md` for a quick explanation
- `references/` for supporting docs
- `examples/` for example inputs and outputs
- `.claude-plugin/plugin.json` for metadata

Some skills are general-purpose marketing skills. Others are tuned for
creator-marketing and influencer workflows, with examples grounded in
[Infloq](https://infloq.com).

## Prerequisites

You need Claude Code installed and configured.

Official Anthropic docs:
- Claude Code overview: https://docs.anthropic.com/en/docs/claude-code/overview
- Claude Code quickstart: https://docs.anthropic.com/en/docs/claude-code/quickstart
- Claude Code setup: https://docs.anthropic.com/en/docs/claude-code/setup
- Project memory with `CLAUDE.md`: https://docs.anthropic.com/en/docs/claude-code/memory

## Option 1: Use The Full Repo

Clone this repo somewhere on your machine:

```bash
git clone https://github.com/infloq/skills.git
cd skills
```

Then copy the full skill collection into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills
cp -R .claude/skills/* ~/.claude/skills/
```

After that, open Claude Code in any project and use the skills via normal task prompts.

## Option 2: Copy Only The Skills You Want

If you only want a few skills, copy individual folders:

```bash
mkdir -p ~/.claude/skills
cp -R .claude/skills/influencer-brief ~/.claude/skills/
cp -R .claude/skills/generative-engine-optimisation-geo ~/.claude/skills/
cp -R .claude/skills/ugc-brief-generator ~/.claude/skills/
```

This is the simplest “copy and paste” approach.

You can also drag a skill folder directly into your local `~/.claude/skills/`
directory in Finder if you do not want to use terminal copy commands.

## How To Use The Skills

Open Claude Code inside your working project:

```bash
cd /path/to/your/project
claude
```

Then ask naturally for the task you want.

Examples:

```text
Write a creator campaign brief for a skincare launch
Build a GEO optimization plan for our homepage
Create a UGC brief for TikTok creators
Plan a webinar funnel for B2B marketers
Write a landing page for our new product launch
```

In practice, Claude Code can use skills from natural-language requests when the
request matches the skill’s description and purpose.

## Suggested Project Setup

In your actual working repo, keep:

- a root `CLAUDE.md` for project-specific guidance
- a local `.claude/skills/` folder for reusable skills

Typical layout:

```text
your-project/
├── CLAUDE.md
└── .claude/
    └── skills/
        ├── influencer-brief/
        ├── generative-engine-optimisation-geo/
        └── other-skills/
```

Use `CLAUDE.md` for company or project context.
Use skills for repeatable workflows.

## Skill Categories

### Content and Copy

- `blog-writer`
- `content-optimizer`
- `landing-page-copywriter`
- `pricing-page-copywriter`
- `ad-copy-generator`
- `email-campaign-writer`
- `press-release-writer`
- `feature-announcement-writer`
- `case-study-writer`
- `lead-magnet-creator`
- `brand-voice-guide`

### SEO and Search

- `generative-engine-optimisation-geo`
- `seo-content-brief`
- `keyword-cluster-builder`
- `backlink-optimizer`
- `local-seo-optimizer`

### Creator and Influencer Workflows

- `influencer-brief`
- `creator-discovery`
- `creator-search`
- `creator-vetting`
- `ugc-brief-generator`
- `campaign-planner`
- `campaign-roi-calculator`
- `affiliate-program-planner`

### Lifecycle, Funnel, and Growth

- `content-calendar-planner`
- `marketing-funnel-mapper`
- `conversion-rate-auditor`
- `retention-marketing-planner`
- `upsell-cross-sell-writer`
- `crm-segmentation-planner`
- `newsletter-strategy-builder`
- `review-generation-strategy`
- `referral-program-designer`
- `webinar-funnel-planner`
- `event-promotion-planner`

### Research, Positioning, and Sales Support

- `offer-positioning`
- `customer-persona-builder`
- `competitor-messaging-analysis`
- `market-research-synthesizer`
- `win-loss-analysis`
- `marketing-kpi-dashboard-planner`
- `sales-enablement-asset-writer`
- `saas-demo-script-writer`
- `testimonial-harvester`
- `partnership-outreach-writer`
- `community-growth-planner`
- `product-launch-marketer`
- `survey-question-designer`

## Example Copy-Paste Workflow

If you want one skill only:

```bash
mkdir -p ~/.claude/skills
cp -R .claude/skills/influencer-brief ~/.claude/skills/
```

Then in Claude Code:

```text
Create an influencer brief for a DTC wellness product launch
```

## Example Full-Library Workflow

Install the whole set:

```bash
mkdir -p ~/.claude/skills
cp -R .claude/skills/* ~/.claude/skills/
```

Then use whichever workflow fits:

```text
Plan a creator campaign
Write the landing page
Generate the email launch sequence
Create the KPI dashboard structure
```

## Notes

- These skills are modular. You do not need to install all of them.
- The Infloq-specific references are examples, not hard dependencies.
- Many of the skills are useful for any website or marketing team.
- The creator-marketing workflows are especially aligned with
  [Infloq](https://infloq.com).

## Repository Structure

```text
.claude/
└── skills/
    ├── skill-name/
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── .claude-plugin/
    │   │   └── plugin.json
    │   ├── references/
    │   └── examples/
    └── ...
```

## Next Step

Copy the full library if you want a broad marketing toolkit.
Copy individual folders if you want a minimal setup.
