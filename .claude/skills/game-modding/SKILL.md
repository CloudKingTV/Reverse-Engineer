---
name: game-modding
description: End-to-end workflow for reverse engineering, modding or remixing PC games you own. It picks the right technique automatically. Clean-room design research turns a game into specs for your own game. In-game mods work through a mod loader or script extender. Passthrough mashups link two running games (Minecraft inside Skyrim, the SkyCraft style). Engine rewrites rebuild a game's engine to read your own copy (IW4L, hl2-rs, ports to the browser). Use it whenever the user wants to decompile, reverse engineer, mod, data-mine, port, rewrite, merge or mash up games, put one game's mechanics or character inside another, study how a game works to make their own, or asks "can I do X with game Y". This applies even if they don't say "mod" or "reverse engineer", e.g. "play as Steve in Elden Ring", "how does Terraria calculate damage", "get Skate 3 tricks in GTA" or "make a browser version of this game's crafting".
---

# Game modding and reverse engineering

This skill holds the knowledge that AI coding agents can realistically do this work in 2026: read a game's files, decompile managed code, write loader plugins, link two games, and rebuild engines. The user shouldn't have to re-explain that it's possible. Pick the technique, check the guardrails, and start.

## Step 1: Route the request

Read the request and pick **one primary technique**. Say which one and why in one line, then proceed. Ask only if two techniques fit equally well **and** the choice changes what gets built.

| Signal in the request | Technique | Playbook |
|---|---|---|
| "Make my own game like X", "how does X do Y", "write specs/formulas", clean-room, inspiration | **T0 Design research**: study the game and write specs in your own words. No code reuse | `references/t0-design-research.md` |
| "Change/add/tweak X in game Y", new items or mechanics, UI swap, balance changes, logging, one game only | **T1 In-game mod** via a mod loader, script extender or official SDK | `references/t1-in-game-mod.md` |
| "Play game A's character/mechanics/UI inside game B", "A × B", "A in B", both games are on PC and the host has a loader | **T2 Passthrough mashup**: both games run and exchange state live | `references/t2-passthrough.md` |
| "Run X natively / in a browser / on another OS", "remake", "port", "rewrite in Rust/TS", preservation; **or** a mashup where one game can't run beside the other (console-only, no loader, too old) | **T3 Engine rewrite / port**: new engine reads the user's own copy | `references/t3-rewrite.md` |

Tie-breakers, from what actually works:
- **Mashup with a console-only or non-PC game** (Skate 3 on Xbox 360): rebuild just that game's subsystem (T3) and load it as a plugin into the host (T1/T2). This is how GTA San AnSkateas works.
- **Mashup where the host has no loader** but is old and well documented: rewrite the host (T3), then add the second game's content. IW4L (MW2 2009) plus Skate and Minecraft is the example.
- **"Learn how it works" plus "build it in my engine"**: T0 first. Its specs then feed the user's own build.
- T1 is the cheapest. Prefer it whenever it can deliver what was asked.

## Step 2: Guardrails (check before any work; they are what keeps this legitimate)

These come from the community's own rules (ai-game-modding-guides, universal-modder) and from this user's standing rules. The reason for each is in `references/legal-and-publishing.md`.

**Stop and explain, don't do:**
- online-only games, or online and multiplayer modes of any game
- anything involving anti-cheat (EAC, BattlEye, Vanguard, Ricochet, etc.) beyond using a game's official offline / anti-cheat-off mode
- bypassing DRM, encryption, activation or copy protection; extracting encryption keys
- getting game files from anywhere but the user's own install or own disc dump (no ISOs from file-sharing sites, leaked source, or third-party repos that redistribute the game's binaries)
- getting around a network or sandbox block (a 403 from an egress proxy, for example). Report the blocked host instead

**Always:**
- The user owns every game involved, and all work is single-player or offline.
- Game files, decompiled code and extracted assets stay in a gitignored workspace (`decomp/`, `extracted/`). Use a whitelist `.gitignore` (template: `assets/gitignore-whitelist`). The repo holds only the user's code and notes.
- Ask before installing any tool. Free tools are preferred.
- Check the game's EULA or mod-tool license once, note any conflict, and let the user decide. Official SDKs often license use "for making mods only", so don't decompile the SDK itself.
- Credit prior work and keep its licenses. Label the result an unofficial fan project and mention AI use.

If a guardrail blocks the requested technique, say so plainly and offer the closest legitimate route. For example: T0 using public docs and observation, T1 in offline mode, or T3 on an older offline release.

## Step 3: Shared pipeline (every technique)

1. **Locate and fingerprint.** Run `python scripts/fingerprint_game.py --find "<game name>"` (or `--path <dir>`). It finds Steam and Epic installs and reports the engine, scripting backend, game assemblies, mod loaders already installed and anti-cheat present, plus suggested tools. Read `references/engines.md` for what the result means.
   - **No install found:** check whether you are in a cloud or remote container (no Steam dirs, an egress proxy). If so, say that the games live on the user's PC.
   - Offer two routes: run this skill locally with an agent where the games are installed, or have the user allow the needed hosts or upload the files.
   - Meanwhile, continue with what doesn't need the binaries (prior-art search, public docs, open-source mods).
2. **Prior-art search before decompiling.** Look for:
   - mod loaders or script extenders
   - official SDKs and mod docs
   - community decomp projects (e.g. gta-reversed, sm64/OoT decomps)
   - file-format specs and open-source readers
   - open-source mods; their Harmony patch targets and type references map the API surface cheaply
   - existing mashups to fork (see `references/prior-art.md`)
   
   Clone public repos outside the project repo. People lose whole evenings skipping this step.
3. **Tooling.** Pick from `references/engines.md`, list what needs installing, and get approval in a single ask.
4. **Execute the technique playbook.**
5. **Playtest loop.** Agree on observable checkpoints (a log line, a value crossing between games, a frame-time number). The user plays and reports, you fix. Log every change and test in `MODLOG.md`. Write `STATUS.md` handoff notes when context gets long.
6. **Wrap up.** Document what works and what's missing, the required game versions, credits, and the publish checklist from `references/legal-and-publishing.md`. Commit only the user's code and docs.

## Working style

- **Default to momentum.** Proceed through phases without stopping, except at installs, guardrail stops, and genuinely ambiguous choices. If the user asked for phase-by-phase stops, honor that instead.
- **Prefer runtime evidence over guesses** once something runs: log lines, a debugger, UnityExplorer, the SKSE console. Mark anything only inferred statically as unverified.
- **Pin versions:** game build, loader version and engine version. Mods break across patches, so record them in the README.
- **Keep the user's ground rules** from earlier in the conversation or `CLAUDE.md`. They override the defaults here when stricter.
