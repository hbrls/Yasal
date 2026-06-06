# Canonical Terms

Canonical Terms 记录同类场景下必须唯一使用的规范词。

## Rule

当某一场景已有 canonical term：

1. 同类场景 MUST 使用该 canonical term。
2. 近义词不再自由混用。
3. 如果保留近义词，MUST 说明它对应不同场景或不同功能。
4. 修复时 MUST 将同类场景的变体收敛到 canonical term。

## Mission

### Canonical Term

`Mission`

### Competing Terms

| Term | Status |
|------|--------|
| `Mission` | Canonical |
| `Intent` | Replace with `Mission` in the same scenario |
| `Goal` | Replace with `Mission` in the same scenario |
| `Purpose` | Replace with `Mission` in the same scenario |

### Use When

Use `Mission` when defining an Agent's stable task direction, identity-level responsibility, or long-running execution target.

### Replace

| Avoid | Use |
|-------|-----|
| `Intent` | `Mission` |
| `Goal` | `Mission` |
| `Purpose` | `Mission` |

### Fix Protocol

When auditing a Skill document:

1. Find occurrences of `Intent`, `Goal`, and `Purpose` used for the same scenario as `Mission`.
2. Replace them with `Mission`.
3. Keep the original term only if the sentence describes a different scenario.
4. If a different scenario is discovered, add a separate canonical entry before preserving the variant.
