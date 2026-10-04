# Prior art (as of October 2026, so verify that links and versions are current)

Projects to clone, fork or study before building. Most are Windows-first.

## Passthrough mashups (T2)

| Project | Games | Notes |
|---|---|---|
| [SkyCraft](https://github.com/chasmlol/SkyCraft) | Skyrim SE/AE 1.6–1.7 + Minecraft Java (Fabric) | Reference design. SKSE plugin plus Fabric mod over shared memory. Read `docs/DESIGN.md` |
| [FalloutCraft](https://github.com/zeyvu/FalloutCraft) | Fallout 4 + Minecraft | SkyCraft port that replaces the host plugin |
| [OWCraft](https://github.com/Yaekai/OWCraft) | Outer Wilds + Minecraft | SkyCraft-based, with a design doc and development log |
| [GTA San AnSkateas](https://github.com/ryglizzy/GTA-San-AnSkateas) | GTA SA 1.0 US + Skate 3 (X360 `default.xex`) | ASI plugin (plugin-sdk) plus a Rust Skate 3 engine DLL |

## Rewrites (T3)

| Project | Notes |
|---|---|
| [IW4L](https://github.com/vladtrc/iw4L) | MW2 (2009) rewritten in Rust and loading MW2 data. Base of the viral MW2/Skate/Minecraft mashup |
| [2010 Rust Rewrite Mashup](https://github.com/chasmlol/2010-rust-rewrite-mashup) | IW4L fork with Skate 3 skating and a Minecraft world as a map (Apache-2.0) |
| [skate-3-rust-engine](https://github.com/SK8-ENGINE/skate-3-rust-engine) | Skate 3 skating engine rebuilt in Rust |
| [hl2-rs](https://github.com/kvalls/hl2-rs) | Half-Life 2, partial, with an honest status list |
| [gang-beasts-rust](https://github.com/muffinmxn/gang-beasts-rust) | Bevy. Python extractors and a whitelist `.gitignore` |
| [benilla](https://github.com/samwhosung/benilla) | WoW 1.12.1 client in Rust and Bevy |
| [OpenMW](https://github.com/OpenMW/openmw), [OpenRCT2](https://github.com/OpenRCT2/OpenRCT2), [OpenTTD](https://github.com/OpenTTD/OpenTTD) | Finished long-term reimplementations |

## Guides and tooling

- [ai-game-modding-guides](https://github.com/trevaintdead/ai-game-modding-guides): beginner guides for passthrough mods and rewrites with AI agents, prompts, rules, and an FAQ
- [universal-modder](https://github.com/rehan-remade/universal-modder): skills and tools that guide an agent through modding a game
- [gta-reversed](https://github.com/gta-reversed/gta-reversed): an example of a community decomp used as reference
- [SkyLink AI / SkryimMCM](https://github.com/jarvann/SkryimMCM): live Skyrim state tools for agents

## Per-game starting points seen in practice

- **Core Keeper** (Unity 6 Mono, Entities/Netcode 1.2.x):
  - official [Mod SDK](https://github.com/Pugstorm/CoreKeeperModSDK) and [docs](https://github.com/Pugstorm/CoreKeeperModDocs)
  - [CoreLib](https://github.com/CoreKeeperMods/CoreLib)
  - [limoka's mods](https://github.com/limoka/CoreKeeperMods), which are MIT and full of Harmony patch targets
  - the free Dedicated Server (Steam app 1963720) contains the server-side assemblies
- **Minecraft Java:** Fabric with official mappings
- **Skyrim:** SKSE plus Address Library, CommonLibSSE
- **Elden Ring:** ModEngine2, Smithbox, offline only
- **Terraria:** tModLoader
- **Stardew Valley:** SMAPI
