# AGENTS.md

This repository's agent instructions live in one file so every tool follows the same rules.

**Before doing anything, read `CLAUDE.md` at the repository root and follow it exactly**: the hard
rules (never invent experience), the mode routing table (which guide to load for each task), the
precedence order, and the Pre-Send Check. This applies even when you were started inside a
`JobSearches/<Company>_<Role>/` folder.

Its Step 0 is a setup check: if the user's personal files don't exist yet or setup is incomplete,
run the onboarding in `SETUP.md` with them before anything else (in Claude Code this is also the
`/setup` skill; elsewhere the user says "set me up").
