---
marp: true
theme: default
paginate: true
size: 16:9
transition: fade
auto-advance: 20
---

<!-- _class: lead -->

# NoobFromMM Profile OS

## Vibe Code Tours — Chapter 3

**Building a GitHub profile portfolio with Claude Code**

⏱ 20 seconds

---

<!-- _class: default -->

# The Problem

- My GitHub profile was a blank repo
- I wanted to learn Claude Code by **building in public**
- I needed a way to show my workflow, not just my code
- Chapter 3 challenge: ship a complete "profile OS" with skills, agents, MCP

⏱ 20 seconds

---

# The Solution

**Superpowers methodology** — three built-in Claude Code capabilities:

| Superpower | What it does |
|------------|-------------|
| 🧠 **Skills** | Reusable prompt packs (UI/UX review) |
| 🤖 **Agents** | Independent sub-agents (profile reviewer) |
| 🔌 **MCP** | Model Context Protocol (filesystem access) |

Plus a PechaKucha deck to explain the whole thing.

⏱ 20 seconds

---

# Claude Code Workflow

```
1. Write spec.md          → define "done"
2. Configure .mcp.json    → safe filesystem access
3. Create SKILL.md        → UI/UX review skill
4. Create agent           → profile-reviewer
5. Build README.md        → polished profile
6. Build slides           → PechaKucha 6×20
7. Commit each slice      → small, meaningful commits
```

⏱ 20 seconds

---

# Evidence

Every Ch3 requirement is a file in the repo:

| Requirement | Evidence |
|-------------|----------|
| Methodology | [`methodology.md`](../methodology.md) |
| MCP config | [`.mcp.json`](../.mcp.json) |
| Skill | [`.claude/skills/ui-ux-pro-max/SKILL.md`](../.claude/skills/ui-ux-pro-max/SKILL.md) |
| Agent | [`.claude/agents/profile-reviewer.md`](../.claude/agents/profile-reviewer.md) |
| Spec | [`spec.md`](../spec.md) |
| Slides | [`slides/pechakucha-6x20.md`](./pechakucha-6x20.md) |

⏱ 20 seconds

---

<!-- _class: lead -->

# The Result

✅ Polished GitHub profile README
✅ Visible Claude Code workflow
✅ Reusable skills, agents, MCP config
✅ Small, honest, beginner-friendly
✅ Ready for Chapter 4

**github.com/NoobFromMM**

⏱ 20 seconds
