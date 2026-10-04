# Engine fingerprints → tools and loaders

`scripts/fingerprint_game.py` detects most of these automatically. Use this table to read its output and choose tools. Every tool listed is free unless marked otherwise. Ask before installing.

| Engine / backend | How to recognise it | Read the code | Run your code inside it | Data and assets |
|---|---|---|---|---|
| **Unity (Mono)** | `<Game>_Data/Managed/Assembly-CSharp.dll`, `UnityPlayer.dll` | ILSpy / `ilspycmd` (`dotnet tool install -g ilspycmd`), dnSpyEx. Burst jobs still have readable C# in the managed DLLs | Official SDK if one exists; otherwise BepInEx 5 or 6 (Mono) or MelonLoader, plus Harmony | AssetRipper, AssetStudio; UnityExplorer for live inspection |
| **Unity (IL2CPP)** | `GameAssembly.dll` + `<Game>_Data/il2cpp_data/Metadata/global-metadata.dat` | Cpp2IL (produces dummy DLLs with signatures, not bodies), Il2CppDumper, then Ghidra for method bodies | BepInEx 6 (IL2CPP) or MelonLoader with Il2CppInterop | AssetRipper |
| **Unreal 4/5** | `<Game>/Content/Paks/*.pak` (and `.utoc/.ucas`), `*-Win64-Shipping.exe` | Ghidra; UE4SS dumps reflection data (classes, properties, functions) at runtime; no source-level decompile | UE4SS (Lua and C++ mods); official mod kit if shipped | FModel / UModel for **unencrypted** paks. If the paks are encrypted, use only official tools, never extract keys |
| **Godot** | `.pck` file or embedded pack (magic `GDPC`), `godot` strings in the exe | GDRE Tools (recovers GDScript and the project) | Script injection via a recovered project, or community mod loaders (e.g. Godot Mod Loader) | GDRE Tools |
| **.NET / XNA / FNA / MonoGame** | Main exe is a .NET assembly; `FNA.dll`, `MonoGame.Framework.dll`, `Microsoft.Xna.Framework*.dll` | ILSpy, dnSpyEx (near-source quality) | Game-specific loaders (tModLoader for Terraria, SMAPI for Stardew), Harmony | Content pipeline `.xnb` unpackers |
| **Java** (Minecraft etc.) | `.jar`, launcher JSON manifests | Minecraft: Fabric/NeoForge toolchains decompile with official mappings. Generic: Vineflower, CFR | Fabric/NeoForge (Minecraft); Java agents for others | Unzip jars |
| **Bethesda Creation** (Skyrim, Fallout 4/76, Starfield) | `*.esm`, `*.bsa`/`*.ba2`, `skse64_loader.exe` if modded | Papyrus sources ship with the Creation Kit; engine via CommonLibSSE/F4SE headers and Ghidra | SKSE/F4SE C++ plugins (with Address Library), Papyrus, ESP plugins | Creation Kit, xEdit (SSEEdit/FO4Edit), BAE |
| **FromSoftware** (Elden Ring, DS3, Sekiro) | `regulation.bin`, `*.bdt/*.bhd`, `EasyAntiCheat/` | Ghidra; community param definitions | ModEngine2 / Mod Engine 3 DLL mods, **offline with EAC off only** | Smithbox / DSMapStudio, WitchyBND |
| **Source / GoldSrc** | `gameinfo.txt`, `*.vpk`, `hl2.exe` | Public Source SDK (2013) is legal source; Ghidra for the rest | Source SDK mods, SourceMod (servers you run) | GCFScape, VPKEdit, Crowbar |
| **GameMaker** | `data.win` (or `game.unx` / `game.ios`) | UndertaleModTool (decompiles GML) | UndertaleModTool scripts | UndertaleModTool |
| **RPG Maker MV/MZ** | `www/js/rpg_core.js` or `js/rmmz_core.js` | Plain JavaScript, read directly | JS plugins | `www/data/*.json` |
| **Electron / HTML5** | `resources/app.asar` | `npx @electron/asar extract` gives readable JS (maybe minified) | Patch JS or preload scripts | Same |
| **Lua-scripted** (Don't Starve, Factorio, many indies) | Many `.lua` files or `scripts.zip` | Usually plain text | Official mod API | Same |
| **Native C/C++ (custom engine)** | None of the above | Ghidra (free); check for a community decomp first | ASI loaders (`dinput8.dll`/`version.dll` proxies), game-specific SDKs (plugin-sdk for GTA) | Format specs from the community; write your own extractor |
| **Console titles** | Disc dump of the user's own copy (`default.xex`, `EBOOT.BIN`, `.nso`) | Ghidra with the right processor module (PowerPC for X360/PS3); check decomp projects first | Emulator plugins; usually a T3 rewrite instead | extract-xiso, format specs |

## Anti-cheat markers (guardrail stop for online or competitive titles)

These folders or files mean an anti-cheat is installed, so treat the game as online-protected:
- `EasyAntiCheat/`, `EasyAntiCheat_EOS*`
- `BattlEye/`, `BEService*`
- `vgk.sys` (Vanguard), Ricochet (CoD), `xigncode`, `GameGuard` / `nProtect`, `EQU8`, `ACE-*`, `mhyprot*`

Only proceed when the game has an **official** offline mode with the anti-cheat off (e.g. Elden Ring's offline launch), and then only in that mode.

## Tips that save hours

- **Unity Mono plus an official SDK** (Core Keeper, Valheim-likes): the SDK pins the exact Unity version, and its importer tells you which game DLLs matter.
- **Decompiler setup:** give it the whole `Managed/` folder as reference path (`ilspycmd -p -o out -r Managed Game.dll`). Otherwise generics and extension methods come out broken.
- **ECS/DOTS games:** systems run in groups, and authoring MonoBehaviours convert into components at load time. Search for `*Authoring`, `*CD` / `IComponentData`, `*System`, and `[UpdateInGroup]` to map the architecture.
- **Lookup tables** usually live in ScriptableObjects, `.json`, or param files. Dump them with the asset tool rather than reading the code that loads them.
- **Native games:** symbols from a Linux or macOS build, an old debug build, or a console build with symbols can save weeks. Check whether any shipped.
