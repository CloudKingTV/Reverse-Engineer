# T1: In-game mod (one game, via loader or script extender)

Use this to change or add things inside one game: new items or mechanics, UI reskins, balance changes, logging, and making one game *feel like* another (e.g. Minecraft-style HUD and hearts in Skyrim). It's the cheapest technique, so prefer it.

## Steps

1. **Find the official path first.** Official SDK, Creation Kit, Workshop tools or a mod kit. Official tools carry the least risk and the best compatibility. Read their license: mod-tool EULAs usually allow making mods but not decompiling the tool itself.
2. **Otherwise use the community loader** for the engine (`engines.md`): BepInEx/MelonLoader (Unity), UE4SS (Unreal), SKSE/F4SE (Bethesda), ModEngine2 (FromSoft, offline), Fabric (Minecraft), ASI loader with a game SDK (native).
3. **Test the loader with an existing mod** before writing anything, so problems aren't confused with your own code.
4. **First milestone: a log line.** Your code loads and writes "hello" to the game's or loader's log. Nothing else until this works.
5. **Find hook points.**
   - Decompile, or dump via UE4SS, the code around the behavior.
   - Look at what open-source mods already patch: their `[HarmonyPatch(typeof(X), "Method")]` targets show where the logic lives.
   - Prefer hooking managed methods. Burst-compiled jobs and inlined native code are hard to patch, so hook the managed caller or the data instead.
6. **Change data before code.** Many mods are only table or param edits: items, recipes, loot, stats. Use the data path when it can deliver.
7. **Build in small playtestable increments.** Logging-only mods are the safest way to confirm how a system really behaves (damage events, world-gen seeds, drop rolls).

## Patterns

- **Harmony** prefix/postfix/transpiler: a prefix that returns false skips the original. Postfixes can read and modify `__result`.
- **ECS games:** add a system to the right group, or add components at conversion time. Core Keeper exposes `ECSManager.BeforeInitialEntityConversion` for this.
- **Multiplayer-architected single-player** (Netcode for Entities etc.): figure out whether logic runs on the server or client world, and run your system in the right one.
- **Reskins:** replace textures or UI prefabs from the user's own other games at runtime. Never ship them.

## Pitfalls

- Version drift: pin the game and loader versions, and expect breakage after patches.
- Burst: patches to Burst-compiled methods silently do nothing. Some SDKs offer a way to disable Burst for a system while debugging.
- Save compatibility: new components or items can corrupt saves when the mod is removed. Warn the user and back up their saves.
