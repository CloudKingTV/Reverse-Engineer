# T0: Clean-room design research

Goal: understand how a game works and write **plain-English specs** the user can build their own game from. The output is documentation, never copied code or assets. This is the route behind open reimplementations like OpenMW and OpenRCT2.

## Phases

Unless the user asked for phase stops, run them back to back and give a short summary at each boundary.

0. **Recon.** Run `fingerprint_game.py`. Report the engine and version, the scripting backend, game-specific assemblies or executables with sizes, and the engine packages present (e.g. Unity Entities, Burst, Netcode). If IL2CPP or native, switch tools per `engines.md`.
1. **Decompile into a gitignored `decomp/`.** One folder per assembly or module. Build `research/index/types.md`: every namespace, with types grouped into ECS systems, components and buffers, authoring components, ScriptableObjects and data tables, MonoBehaviours (UI and visuals), and other. Note which systems are Burst-compiled jobs.
2. **Architecture map** in `research/architecture.md`:
   - boot and world loading
   - update loop or system groups and their order
   - how authored content becomes runtime data
   - world, chunk or tile storage, streaming and saving
   - the client/server split (even in single-player)
   - where lookup tables live
   
   Include one Mermaid diagram of the main loop or system groups.
3. **Data overview.** Dump the data tables with the asset tool into `decomp/assets/`. Summarize them in `research/data-overview.md`: which tables exist, their fields, entry counts, and cross-references. Give **ranges and examples, not full dumps**.
4. **System specs.** One file per system in `research/systems/`, using the template below. Derive the system list from the code, not from a generic checklist. Typical systems: world-gen, biomes, tiles/mining, lighting, crafting, inventory, equipment/stats, combat/damage, enemy AI, bosses, progression/skills, farming, cooking, fishing, NPCs, pets, building, automation/wiring, save system.
5. **Live verification (optional, ask first).** Propose small logging-only mods (T1 tooling) that confirm the open questions. Don't build them until approved.
6. **Final deliverable.** `research/README.md` containing:
   - an index of every file
   - one paragraph per system
   - the top 10 design insights
   - a recommended build order for the user's own game

## Spec template (every system file)

- **Summary**: what it does from the player's point of view
- **How it works**: rules, state, data flow and update order in plain English
- **Formulas and numbers**: damage calculations, drop rates, timers, with value ranges
- **Key types**: class and component names, for reference
- **Design notes**: what makes it feel good, plus 2–3 ideas for doing it differently
- **Implementation notes for the user's stack** (e.g. TypeScript/browser): data structures, update loop, performance concerns
- **Open questions**: anything not confirmable statically

## Rules for writing specs

- Describe behavior in your own words. No pasted code blocks from the decompiled source. Short identifiers are fine.
- Formulas are fine as math. Write `damage = base × (1 + crit) − armor/2`, not the method body.
- Don't copy full data tables, art or audio into anything shippable.

## When the binaries aren't reachable (cloud session, blocked network)

Do the useful parts anyway:
- **Pin versions:** read the official SDK or mod docs for the engine version and packages.
- **Map the API surface:** pull Harmony patch targets and type references from open-source mods. Write the result to `research/index/api-surface-from-mods.md`.
- **Write a local script** the user runs on their PC to finish recon and decompilation (e.g. a PowerShell script that finds the Steam install and runs `ilspycmd`). It must install nothing.
