---
name: docker-training-exercise
description: Create a Docker training exercise for the Docker_Training curriculum. Use this when writing a new hands-on exercise, lab, or demonstration for any training phase (Phase 01–06). Produces consistently structured exercise files with objectives, commands, validation steps, and explanations targeting a Windows/PowerShell learner.
argument-hint: "[phase-number] [topic] [exercise-title]"
---

# Docker Training Exercise Creator

## Learner Context
- Platform: Windows 11 with Docker Desktop (WSL2 backend)
- Shell: PowerShell 7 (`pwsh`)
- Existing containers to reference: Traefik, Calibre-web, OpenMemory (Node.js), AdGuard Home
- Goal: CLI-first, cross-platform Docker mastery

## Exercise File Structure

Create the exercise as a Markdown file at:
`Phase_XX_<PhaseName>/Exercises/<exercise-title>.md`

### Template

```markdown
# Exercise N.N – <Title>

## Phase Context
Phase <N>: <Phase Name> | Module <N>: <Module Name>

## Objectives
By the end of this exercise you will be able to:
- [ ] <verb> <specific, measurable outcome>
- [ ] <verb> <specific, measurable outcome>

## Background
<!-- 2-4 sentences: What concept does this cover and WHY does it matter in production? -->

## Prerequisites
- Completed Exercise N.N–1
- Docker Desktop running, WSL2 backend active
- (List any images or containers that must already exist)

## Exercise

### Part 1: <Sub-topic>

**What**: <!-- one sentence -->
**Why**: <!-- one sentence — production relevance -->

```powershell
# Command with meaningful comment
docker <command> [options]
```

**Expected output:**
```
<sample output>
```

### Part 2: …

## Validation
Run each check and confirm the expected result:

```powershell
# Validation command
docker inspect <container> --format '{{.State.Status}}'
```

Expected: `running`

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| `Error response from daemon` | Daemon not running | Start Docker Desktop |
| Permission denied | WSL socket issue | `sudo usermod -aG docker $USER` |

## Real-World Connection
<!-- 1-2 sentences connecting to learner's existing containers (Traefik, Calibre-web, etc.) -->

## Summary
<!-- 3-5 bullet recap of what was practiced -->

## Next Exercise
<!-- Link to the next logical exercise -->
```

## Writing Rules

1. **Always use PowerShell syntax** — no `bash` or `cmd` blocks.
2. **Show both modern and legacy commands** when they differ (e.g., `docker container run` vs `docker run`).
3. Include the **What / Why / How / Gotchas** structure for every new command.
4. Reference the learner's **existing containers** as concrete examples wherever possible.
5. Validation steps must be **runnable commands**, not just "check Docker Desktop."
6. Complexity must match the phase: Phase 01 = basics, Phase 06 = advanced topics.
