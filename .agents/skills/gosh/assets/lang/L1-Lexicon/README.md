# L1 · Lexicon

Gosh 词汇层规范入口。L1 处理词项、局部短语、规范词收敛和令词等级，不在入口文件中堆积大型词表。

## Core Rule

遇到匹配场景，先查 L1 Lexicon；已有规范时，使用规范词，不自由发挥近义词。

## Groups

| File | Purpose | Use When |
|------|---------|----------|
| [Canonical.md](./Canonical.md) | 唯一规范词 | 同类场景必须收敛到一个词 |
| [Imperatives.md](./Imperatives.md) | 令词等级表 | 需要表达义务、禁止、优先级、注意力旗帜 |
| [Research.md](./Research.md) | 研究模板 | 需要比较候选词、构造对照、决定是否晋升 |

## Canonical vs Imperatives

| Type | Core Question | Decision Shape |
|------|---------------|----------------|
| Canonical | 这个场景唯一应该用哪个词？ | 选定一个词，其他近义词收敛到它 |
| Imperatives | 这个约束应该用多强的令词？ | 按强度等级和场景选择 |

## Promotion Path

1. 新词项或近义词组先进入 [Research.md](./Research.md) 模板。
2. 若结论是“同类场景必须唯一使用某词”，晋升到 [Canonical.md](./Canonical.md)。
3. 若结论是“该词表达不同强度的义务、禁止或注意力信号”，晋升到 [Imperatives.md](./Imperatives.md)。

## Writing Protocol

1. 先查 [Canonical.md](./Canonical.md)。如果目标场景已有 canonical term，使用该词。
2. 再查 [Imperatives.md](./Imperatives.md)。如果目标是约束、禁止、强调或优先级，按等级选择令词。
3. 若两个文件都无法覆盖，使用 [Research.md](./Research.md) 建立候选比较，不直接新增规范结论。
