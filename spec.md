# Spec — NoobFromMM Profile OS (Chapter 3)

## Gist

Turn `NoobFromMM/NoobFromMM` into a clean GitHub profile portfolio that doubles
as a Claude Code workflow showcase. Chapter 3 uses the **Superpowers**
methodology — a lightweight framework built on skills, agents, and MCP — to
build, review, and present the project.

## Story

I'm learning Claude Code by building in public. Each chapter of *Vibe Code Tours*
adds a real deliverable to my profile repo. Chapter 1 got the repo and CLAUDE.md
set up. Chapter 2 introduced the methodology. Chapter 3 is the first complete
"profile OS" — a README that tells my story, backed by a visible toolchain
(skills, agents, MCP config) and a PechaKucha deck that walks through the build.

## Why

- **Ship something real.** A profile repo people actually land on is more useful
  than a tutorial exercise.
- **Show the workflow, not just the output.** The `.claude/` directory IS the
  deliverable — it proves I can configure skills, agents, and MCP.
- **Learn by doing.** Writing a spec, following a methodology, and reviewing my
  own work teaches more than reading docs.

## Why Not

- **No backend.** This is a static profile — there's nothing to deploy or
  host.
- **No API keys or secrets.** Everything runs locally via Claude Code; MCP
  config points at the project folder only.
- **No fake metrics.** No inflated stats, no invented experience. The profile
  is honest about where I am.

## Tech Spec

| Layer | Choice | Reason |
|-------|--------|--------|
| Repo | Public GitHub, `NoobFromMM/NoobFromMM` | GitHub profile convention |
| Methodology | Superpowers | Lightweight, fits solo builder |
| MCP | `filesystem` server scoped to `./` | Safe context for agents |
| Skill | `ui-ux-pro-max` | Reviews layout, readability, visual hierarchy |
| Agent | `profile-reviewer` | Reviews README for clarity, honesty, Ch3 readiness |
| Slides | Marp PechaKucha (6×20) | Standard format, renders from Markdown |
| Evidence | File paths in this repo | No external dashboard needed |

## Definition of Done

- [x] Public GitHub repo owned by NoobFromMM
- [x] Methodology: Superpowers (documented in `methodology.md`)
- [x] MCP config: `.mcp.json` with safe filesystem scope
- [x] Skill: `.claude/skills/ui-ux-pro-max/SKILL.md`
- [x] Agent: `.claude/agents/profile-reviewer.md`
- [x] Slides: `slides/pechakucha-6x20.md` — 6 slides, 20 seconds each
- [x] Polished `README.md` that ties everything together
- [x] Evidence paths clearly visible in the repo structure
- [x] Small, meaningful commits (one per logical change)
