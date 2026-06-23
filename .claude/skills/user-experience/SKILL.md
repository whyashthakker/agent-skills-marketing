---
name: user-experience
description: Apply UX thinking to product decisions, flows, and copy. Use this skill when the user asks to improve user experience, review flows, write UX copy, reduce friction, simplify onboarding, audit confusing UI patterns, or think through what a user sees vs. what happens behind the scenes. The core principle: users care about outcomes, not implementation.
license: Complete terms in LICENSE.txt
---

This skill guides UX thinking across product decisions — what to show, what to hide, and how to communicate with users in a way that builds trust without exposing internal complexity.

The user provides a flow, feature, screen, or copy to review. They may include context about the audience, the goal, or a specific problem they're seeing.

## Core UX Principle: Outcomes Over Implementation

Users think in goals, not systems. They want to know:
- What will this do for me?
- Is this safe / will I lose anything?
- What happens next?

They do not want to know:
- Which AI model generated this
- Which third-party API is being called
- What database query is running
- What the retry logic looks like
- Internal status codes or error stack traces

**Before any copy, label, tooltip, or status message — ask: "Is this information for the user, or for the engineer?"** If it's for the engineer, it doesn't belong in the UI.

## UX Thinking Framework

Before suggesting changes, understand:
- **Who is the user?** Their mental model, vocabulary, and context. A developer reads differently than a CMO.
- **What is the job to be done?** The single thing they came to accomplish right now.
- **Where are they in the flow?** Entry, decision point, waiting, success, error, or exit.
- **What do they fear?** Data loss, irreversibility, cost, confusion, embarrassment.

## What to Show vs. What to Hide

**Show:**
- Progress toward the user's goal ("Your file is ready")
- Confirmation that something worked ("Saved")
- What the user can do next
- Relevant constraints in plain language ("Max 10 members on free plan")
- Recoverable errors with a clear path forward ("Something went wrong — try again")

**Hide:**
- Service names, model names, vendor names unless the user explicitly chose them
- Technical error messages (log them, don't surface them)
- Processing steps the user can't act on ("Calling GPT-4o-mini..." → just show a spinner)
- Internal state transitions ("Queuing...", "Initialising...", "Hydrating...")
- Percentage progress that isn't meaningful ("12%... 13%...")

## Language & Copy Guidelines

Write copy the way a calm, knowledgeable colleague would speak — not a system log:

- **Action labels**: Verb + object. "Save draft", "Send invite", "Export PDF". Never "Submit", "Proceed", "Execute".
- **Status messages**: Past tense for done ("Saved"), present continuous for in-progress ("Saving…"), imperative for next step ("Add a team member").
- **Error messages**: Say what happened in plain language, then what to do. Never show error codes to end users.
- **Empty states**: Tell the user what they'll get here and give them one clear action to start.
- **Tooltips**: Only if the label alone is genuinely ambiguous. Don't use them to explain implementation.
- **Loading states**: Name the outcome, not the process. "Getting your results" beats "Fetching data from API".

## Flow Review Checklist

When auditing a flow or screen:

1. **Can the user tell where they are?** (orientation)
2. **Can the user tell what to do next?** (wayfinding)
3. **Does every piece of text serve the user's goal?** (relevance)
4. **Are any internal details leaking into the UI?** (abstraction)
5. **What happens on error — does the user know what to do?** (recovery)
6. **What is the user feeling at this moment?** (emotional state — anxious, excited, confused, relieved?)
7. **Is anything asking for effort the user shouldn't have to give?** (friction)

## Friction Audit

Common friction sources to eliminate:
- Asking for information you don't need yet (forms that ask for credit card before showing value)
- Requiring a decision with insufficient context ("Do you want to enable advanced mode?" — what is that?)
- Success screens that don't tell the user what to do next
- Modals that interrupt flow without a clear purpose
- Copy that explains how the system works instead of what it means for the user
- Loading states with no feedback on progress or expected duration
- Confirmation dialogs for low-stakes, reversible actions

## Onboarding UX

Good onboarding shows value before asking for commitment:
- Lead with what the user can accomplish, not a feature list
- Delay account creation until the user has experienced something worth returning for
- Use progressive disclosure — reveal complexity only when the user is ready for it
- The first "aha moment" should be reachable in under 60 seconds

## Applying This Alongside frontend-design

UX and UI are complementary. The [[frontend-design]] skill handles how things look and feel visually. This skill handles what is shown, what is said, and when. Apply both together:
- `frontend-design` makes it beautiful
- `user-experience` makes it make sense

When conflicts arise — always side with clarity over aesthetics. A stunning interface that confuses the user has failed.
