# Phase 0: Recon

Status: **partial**. The game binaries (Pug\*.dll) are not available in this environment. See "Source search" at the end for everything that was tried.

## Where I looked

| Source | Result |
|---|---|
| Local Steam library paths in the cloud container | No Core Keeper install (this session runs in a cloud container, not on the user's PC) |
| Steam CDN / SteamCMD (would allow the free *Core Keeper Dedicated Server*, app 1963720) | Blocked by this session's egress policy (proxy 403) |
| Microsoft .NET download hosts (needed for `ilspycmd`) | Blocked (proxy 403). NuGet (`api.nuget.org`) is reachable |
| Community modding wiki `CoreKeeperMods/core-keeper-docs` (public) | Cloned outside the repo; used for context below |
| Official mod SDK `Pugstorm/CoreKeeperModSDK` (public, commit `8216db9`, "Update SDK for 1.3.0.3", 2026-09-29) | Cloned outside the repo. **Does not contain the gameplay DLLs.** Its importer copies them from the user's own game install via an AssetRipper export |

## Findings (from SDK metadata and docs; no decompilation performed)

- **Unity version:** 6000.0.59f2 (Unity 6). The SDK's `ProjectVersion.txt` requires this version, and the docs say the SDK version normally matches the game's.
- **Scripting backend:** Mono. The docs file the older IL2CPP guides under "archive/outdated-il2cpp-guides", and Harmony runtime patching (shipped with the game) needs Mono. Burst-compiled code is native (`lib_burst_generated.dll`) but still has managed C# equivalents in the DLLs.
- **Architecture hints from the docs:** gameplay entities (players, enemies, placeables) are ECS entities, not GameObjects. GameObjects are used only for graphics prefabs and UI. Content is authored with MonoBehaviour Authoring components that convert to ECS. Many lookup tables are ScriptableObjects. Networking uses Netcode for Entities ghosts (client/server even in single-player).

### Game-specific assemblies (names from the SDK importer's include list; sizes need the real install)

`Pug.Base`, `Pug.ECS.Authoring`, `Pug.ECS.Components`, `Pug.ECS.ConditionExtensions`, `Pug.UnityExtensions`, `Pug.Other` (referenced by the SDK's DefineProcessor), `PugProperties`, `PugMod.SDK.Runtime`, plus anything else matching "not Unity/System/Mono/Microsoft". The SDK also ships Pugstorm tooling DLLs: `PugSprite` (151 KB), `ScriptableData` (44.5 KB), `Pug.Changelog` (6.5 KB).

Excluded by the importer, which suggests they exist in the game folder: `Assembly-CSharp.dll`, `PugMod.Loader*`, `SpriteInstancing.dll`, `CgSDK.dll`, `RoslynCSharp.*`, `Trivial.*`, Harmony/MonoMod, mod.io.

### Unity packages (SDK `Packages/`)

| Package | Version |
|---|---|
| com.unity.entities | 1.2.4 (embedded, likely Pugstorm-patched) |
| com.unity.netcode (Netcode for Entities) | 1.2.4 (embedded) |
| com.unity.physics | 1.2.4 (embedded) |
| com.unity.collections | 2.4.3 (embedded) |
| com.unity.transport | 2.1.0 (embedded) |
| com.unity.burst | 1.8.25 |
| com.unity.mathematics | 1.3.2 |
| com.unity.addressables | 2.7.3 (embedded) |
| com.unity.render-pipelines.universal (URP) | 17.0.4 |
| com.unity.ai.navigation | 2.0.9 |
| com.unity.2d.sprite | 1.0.0 |
| Pugstorm: dev.pugstorm.mod / scriptabledata / sprite | 0.1.0 / 0.1.0 / 0.3.0 |

## Licensing note

The Mod SDK's EULA licenses it "solely for ... the creation of Mods" and forbids decompiling it without permission, except where law allows. So this project does **not** decompile anything from the SDK. The SDK was used only to read metadata (version files, package manifests, file names). The gameplay assemblies come from the game itself, whose own EULA governs them. The user should check that EULA before Phase 1.

## Source search (round 2)

### Legitimate sources found and used

| Source | What it gives | Location (outside repo, not committed) |
|---|---|---|
| `Pugstorm/CoreKeeperModSDK` | Unity version, package versions, game assembly names | `/home/user/pugstorm/` |
| `Pugstorm/CoreKeeperModDocs` (official, updated 2026-09-30) | Official modding docs and code examples (ECS systems, RPC, Burst hooks, data blocks), SDK changelogs up to 1.3.0.3 | `/home/user/oss/Pugstorm_CoreKeeperModDocs` |
| `CoreKeeperMods/core-keeper-docs` | Community modding wiki | `/home/user/corekeepermods/` |
| `CoreKeeperMods/CoreLib`, `limoka/CoreKeeperMods` (MIT), `Valgard/ck_mod_settings_menu` | Open-source mods that call the game API: **~250 real game type names and 75 hooked game methods** | `/home/user/oss/` |

These produced [`index/api-surface-from-mods.md`](index/api-surface-from-mods.md), a name-only map of components, buffers, systems, authoring components, databases and hooked methods.

### Blocked by this session's network policy (proxy 403; not circumvented)

- Steam CDN / SteamCMD (`steamcdn-a.akamaihd.net`, `api.steamcmd.net`), which is the free dedicated-server route
- Microsoft .NET downloads (`builds.dotnet.microsoft.com`). Workaround available: NuGet is reachable and hosts both `ilspycmd` (11.1) and the .NET runtime packs
- Wikis: `core-keeper.fandom.com`, `corekeeper.atma.gg`, `corekeeper.wiki.gg`; also `mod.io`

### Deliberately not used

- Third-party forks or mirrors that may contain the game's own DLLs or decompiled source. Those are unlicensed redistributions of Pugstorm's code, and using them would break this project's ground rules.

### Remaining routes to the actual gameplay code

1. **Run locally:** `tools/local-recon.ps1` finds the Steam install, completes this recon (Unity version, backend, assembly sizes, packages) and, with `-Decompile`, exports the `Pug*`/`Assembly-CSharp` DLLs into the gitignored `decomp/`. It installs nothing.
2. **Allow Steam hosts** in this environment's network settings (Custom → Allowed domains), then fetch the free dedicated server here with SteamCMD (needs approval to install SteamCMD).
