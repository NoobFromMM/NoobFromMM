# Methodology — Superpowers

## What is Superpowers?

Superpowers is a lightweight solo-builder methodology. Instead of heavy
ceremony, it leans on three "superpowers" that Claude Code gives you out of the
box:

1. **Skills** — reusable prompt packs that encode expertise (like UI/UX review)
2. **Agents** — specialized sub-agents that review, critique, or generate
3. **MCP** — Model Context Protocol servers that give Claude access to files,
   search, and other tools

The idea: write a spec, build in small slices, and use skills + agents + MCP
to review and tighten every slice before moving on.

## How this project applies it

### 1. Clarify the goal

Before writing code, I wrote `spec.md`. It answers: what are we building, why,
what's out of scope, and what does "done" look like?

Evidence: [`spec.md`](./spec.md)

### 2. Write the spec first

The spec drives every decision. If something isn't in the spec, it doesn't get
built. This prevents scope creep on a small personal project.

Evidence: [`spec.md`](./spec.md)

### 3. Build in small slices

Each file is one slice — README, MCP config, skill, agent, slides. Each gets
its own commit. No monolith commit that mixes concerns.

Evidence: `git log --oneline` (7+ small commits)

### 4. Use a skill for UI/UX review

The `ui-ux-pro-max` skill reviews the README for layout, readability, and
visual hierarchy. It's a reusable skill that can be invoked during any
profile update.

Evidence: [`.claude/skills/ui-ux-pro-max/SKILL.md`](./.claude/skills/ui-ux-pro-max/SKILL.md)

### 5. Use an agent for profile review

The `profile-reviewer` agent checks the README and project evidence for
clarity, honesty, structure, and Ch3 readiness. It runs as an independent
sub-agent that can critique without bias.

Evidence: [`.claude/agents/profile-reviewer.md`](./.claude/agents/profile-reviewer.md)

### 6. Use MCP for project file context

The MCP filesystem server gives Claude Code access to the project directory,
so agents and skills can read and review files without manual path passing.

Evidence: [`.mcp.json`](./.mcp.json)

### 7. Commit as I build

Every logical change gets its own commit with a conventional commit message.
This keeps the history readable and shows the build progression.

Evidence: `git log --oneline`
