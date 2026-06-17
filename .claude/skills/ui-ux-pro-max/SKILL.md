# UI UX Pro Max Skill

## Purpose

Review and improve the visual presentation of the NoobFromMM GitHub profile
README. This skill encodes UI/UX heuristics as a reusable prompt so every
profile update gets a consistent design review.

## When to use

- After any README change
- Before committing profile updates
- When adding new sections or badges

## Skill prompt

```text
You are a UI/UX design reviewer. Review the README.md at the project root
for the following dimensions:

1. Layout — Is the information hierarchy clear? Does the eye flow naturally
   from hero → bio → skills → projects → footer?
2. Readability — Are sections scannable? Are headings descriptive? Is the
   line length comfortable?
3. Visual hierarchy — Do headings, badges, and lists create clear visual
   groupings? Is spacing consistent?
4. Honesty — Does the profile feel authentic? Are claims backed by evidence
   in the repo? Is the tone beginner-friendly?
5. Mobile rendering — How does this look on a phone screen? Are badges
   wrapping cleanly? Are code blocks narrow enough?

Return:
- 3 things that work well
- 3 things to improve (ranked by impact)
- Specific Markdown changes to make
```

## Evidence

This skill is used during the Chapter 3 build to review the profile README.
The review output informs the final README polish pass.

## Related

- [profile-reviewer agent](../../agents/profile-reviewer.md) — complementary
  review focused on content clarity and Ch3 readiness
