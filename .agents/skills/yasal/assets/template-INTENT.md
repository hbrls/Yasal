# Intent

You don't write intent. The `skills/codex-autoresearch` infers everything from your sentence and your repo:

Before starting, The `skills/codex-autoresearch` always shows what it found and asks you to confirm. Then you choose foreground or background and say "go."

### Goal

Your sentence: "get rid of all any types"

### Scope

Scans repo structure: src/**/*.ts

### Metric

Proposes based on goal + tooling: any count (current: 47)

### Direction

Infers from "improve" / "reduce" / "eliminate": lower

### Verify

Matches to repo tooling: grep count + tsc --noEmit

### Guard

Suggests if regression risk exists: npm test
