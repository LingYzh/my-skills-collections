---
name: grilling
description: Grill the user about a plan, decision, design, requirement, or idea until the material decision tree is resolved. Ask the whole currently-answerable frontier in concise rounds, research facts yourself, give a recommendation for every real decision, preserve settled answers, and do not act until the user confirms shared understanding.
license: MIT
metadata:
    author: github.com/mattpocock
    customized_by: github.com/LingYzh
    upstream_commit: "85f83d3fde1d3a90d5c9a657f6998c79a6c37308"
    upstream_skill_blob: "8ca78c6d8f901aab0c5a1f896034b70e666ff2a3"
    version: "1.0.0-personal.1"
---

# Grilling

Use this Skill to stress-test a plan, product decision, requirement set, architecture, workflow, or idea until the user and agent share the same material understanding.

The goal is not to maximize the number of questions. The goal is to expose and settle every **material decision** without wasting the user's time on facts, trivial implementation details, or questions whose answers already follow from settled decisions.

## Core Model: Design Tree and Frontier

Represent the problem as a **design tree**:

- each decision can unlock later decisions
- a decision may depend on facts or earlier decisions
- settled decisions constrain later branches

Work in **rounds**.

The **frontier** is the set of material decisions whose prerequisites are already settled. Ask the whole frontier in the current round. Do not ask a question whose answer depends on another still-open question in the same round; leave it for a later round.

After the user answers, update the tree, preserve settled decisions, recompute the frontier, and continue.

## 1. Facts Are the Agent's Job

Do not ask the user for information that can reasonably be discovered from available sources or tools.

Before turning something into a question:

1. inspect the current codebase, files, docs, linked sources, project configuration, or connected tools when relevant
2. search external/current information when the decision depends on changing facts
3. use sub-agents when available and useful, but do not depend on them existing
4. distinguish a **fact** from a **preference/decision**

Examples:

- "Does the project already have a request wrapper?" -> inspect the project
- "Does the reference project already solve this?" -> inspect the reference project
- "Which behavior do you want when both designs are valid?" -> ask the user

If the user is the only source of a genuinely necessary fact, ask it plainly.

## 2. Existing Architecture and Reference Implementations Are Strong Defaults

When the current project or a user-designated reference implementation already has an analogous policy, treat it as a strong recommendation unless there is a concrete reason not to.

Do not manufacture a fresh architecture choice merely to create another question.

When relevant, explain the recommendation briefly:

> The existing project already handles X this way, so I recommend keeping the same behavior unless this feature has a specific reason to diverge.

The user still owns the decision, but consistency should be the default recommendation when it reduces unnecessary design surface.

## 3. Ask in the User's Language and Keep Questions Easy to Parse

Match the language the user is using unless they request otherwise.

Questions must be direct and concrete:

- prefer ordinary words over specialist terminology
- avoid dense compound nouns and jargon-heavy phrasing
- if a technical term is necessary, define it briefly the first time
- keep one underlying decision per question
- do not hide several unrelated decisions inside one long paragraph
- give concrete choices when the decision naturally has discrete options

Do not make later rounds harder to understand just because the design tree has become deeper.

## 4. Every Material Question Gets a Recommendation

Each question must include one clear recommended answer.

Recommendations should be decisive rather than neutral summaries. Base them on, in order:

1. already-settled user decisions
2. existing project/reference behavior
3. implementation cost and maintainability
4. factual research
5. general best practices only when the earlier signals do not decide the issue

If the user has already established a general policy that resolves the current branch, apply that policy instead of asking the same decision again in a narrower form.

## 5. Preferred Round Format

Number questions continuously across the whole grilling session.

When choices are useful, prefer a compact A/B/C-style format:

```text
❓ **Q12 — <short title>**

<plain-language question>

A. <choice>
B. <choice>
C. <choice>

➡️ **Recommended: B** — <short reason>

---

❓ **Q13 — <short title>**
...
```

Do not force artificial multiple-choice options when a direct question is clearer.

Keep the recommendation short enough that the user can scan the entire round quickly.

## 6. Ask the Whole Frontier, but Do Not Over-Grill

Ask every currently answerable **material** decision in the round. Do not arbitrarily limit a round to one or two questions when several independent decisions are already unblocked.

At the same time, do not create questions for:

- facts you can determine yourself
- reversible implementation details already covered by project conventions
- cosmetic differences with no meaningful consequence unless the user cares about them
- hypothetical edge cases with little realistic impact
- decisions whose answers logically follow from an already-settled policy
- the same underlying issue reworded several ways

"Relentless" means no material branch is silently assumed; it does not mean maximizing friction.

## 7. Accept Compressed and Batch Answers

Users do not need to answer every question with a full sentence.

Correctly interpret answers such as:

- `Q12 B, Q13 C`
- `12/13 按推荐，14 选 A`
- `除了 Q20，其他都按推荐`
- `这轮推荐都没问题`
- `其余照现有项目做`

When the user's intent is clear, settle those decisions without asking them to restate each one.

If one answer is ambiguous, reopen only that decision and branches that depend on it.

## 8. Preserve Settled Decisions and Detect Conflicts

Maintain a compact decision ledger throughout the session.

For each settled decision, preserve at least:

- question/decision identifier
- selected answer or policy
- any important constraint introduced by the answer

Do not ask a settled question again unless:

- new evidence materially changes the decision
- a later answer conflicts with it
- the user explicitly reopens it

If a new answer conflicts with an earlier settled decision, do **not** silently overwrite history. Point out the conflict clearly and reopen the smallest affected branch.

## 9. Use Checkpoints in Long Sessions

Long grilling sessions are vulnerable to context compression and forgotten constraints.

When enough decisions have accumulated that losing them would be costly, surface a compact checkpoint containing:

- important settled policies
- explicitly rejected alternatives that could otherwise reappear
- unresolved decisions/fact dependencies

Do not dump a full transcript. Summarize decisions, not conversation history.

If the user asks to persist the checkpoint into files/docs and the required tools are available, do so. Otherwise keep the checkpoint in the conversation.

## 10. Research Can Run Alongside the Frontier

If one branch depends on research that is still unresolved, do not stall the whole round when other frontier questions are independent.

Research the fact with available tools and continue asking unrelated frontier questions. Only dependent branches wait.

Never pretend a fact is settled while research is incomplete.

## 11. Completion Condition

The grilling session is complete when:

- no unresolved **material** decision remains in the design tree
- no important assumption is still silently inferred
- any factual dependencies that affect the design are resolved or explicitly marked unavailable
- earlier decisions are internally consistent

At that point, provide a concise final decision summary and tell the user that the material frontier is empty.

**Do not execute the resulting plan, modify code, or otherwise act on the decisions until the user confirms that shared understanding has been reached.**

If the user corrects the summary, reopen only the affected branches and continue grilling.
