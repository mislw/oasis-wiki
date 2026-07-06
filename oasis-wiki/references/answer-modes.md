# Answer Modes

Use this reference when deciding how detailed an Oasis / UGC answer should be.

The skill has two answer modes:

1. **Normal mode**: concise, practical, review-friendly, and direct.
2. **Teaching mode**: detailed, step-by-step, and beginner-friendly.

Default to normal mode unless the user asks to learn, the task is structurally complex, or the change is risky.

## Normal Mode

Use normal mode when the user wants a quick answer, already knows the project flow, asks a narrow question, or is sharing the answer with experienced teammates who need fast review and implementation guidance.

Trigger phrases:

- "直接说"
- "简单说"
- "快速看一下"
- "给我代码"
- "这个怎么改"
- "哪里有问题"
- "帮我查一下"
- "正常模式"
- "给前辈看"
- "方便 review"
- "快速审一下"

Answer shape:

```text
结论:
<short direct answer>

改哪里:
<file path + function/table>

最小改动:
<focused snippet with detailed Chinese comments inside the code block>

影响范围:
<server/client/UI/save/replication/RPC/reconnect impact, or "only affects this local function">

注意:
<only the key risks and compatibility notes>

怎么测:
<2-4 short checks>
```

Rules:

- Put the conclusion first, then the exact edit target. Do not open with background teaching.
- Keep prose compact and review-friendly. Assume the reader understands the project flow unless the code shows a surprising dependency.
- Prefer the smallest additive diff. State whether the change preserves existing behavior and call order.
- Keep detailed Chinese comments inside code blocks, but keep explanation outside the code short.
- Include `影响范围` for non-trivial changes so reviewers can quickly judge blast radius.
- In `注意`, prioritize server/client authority, RPC registration, replication, save data, reconnect, nil checks, Lua punctuation, compatibility, and rollback risk.
- If useful, include a one-line rollback note such as "回滚: 删除新增 helper 和调用点即可".
- If the user seems confused during follow-up, switch to teaching mode.

## Teaching Mode

Use teaching mode when the user is learning a project, asking for reasoning, or implementing a feature across several systems.

Trigger phrases:

- "教我"
- "详细讲"
- "从底层讲"
- "为什么"
- "我不懂"
- "拆一下"
- "解构这个项目"
- "学一下前辈项目"
- "按流程讲"
- "一步一步"
- "教学模式"

Also use teaching mode automatically for high-risk or cross-system UGC changes:

- Client button -> ServerRPC -> server logic -> ClientRPC/event -> UI refresh.
- Save/archive data.
- Replication and `OnRep_*`.
- Reconnect / recovered / respawn handling.
- Multiplayer authority or anti-cheat-sensitive resource changes.
- Task, reward, inventory, shop, skill, team, rank, phase, damage, or respawn systems.

Teaching mode answer shape is defined in `teaching-mode.md`. It should include numbered steps and, for each non-trivial edit:

- `位置`
- `现在是`
- `改成`
- `为什么这样改`
- `注意`
- `怎么测`

## Mode Switching

- If the user explicitly says "正常模式" or "简短点", use normal mode.
- If the user explicitly says "教学模式" or "详细讲", use teaching mode.
- If a normal-mode answer would hide a dangerous detail, briefly include the detail rather than staying overly short.
- If a teaching-mode answer becomes too long, split it into phases and ask the user to continue with the next file or next step.

## Interaction With Project File Safety

Both modes keep the same safety rule: UGC project files may be read and analyzed freely, but should not be directly modified unless the user explicitly overrides teaching-only project-file behavior for the current task.

