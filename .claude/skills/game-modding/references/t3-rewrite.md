# T3: Engine rewrite / port (new engine, user's own game data)

Rebuild a game's engine, or one subsystem of it, from scratch. The new engine loads models, maps, textures and sounds from **the user's installed copy at runtime**, and the repo holds only new code. Examples:
- IW4L: Modern Warfare 2 (2009) in Rust; its fork adds Skate 3 and Minecraft modes
- hl2-rs: Half-Life 2, partial
- gang-beasts-rust (Bevy)
- benilla: a WoW 1.12 client
- Halo CE in the browser
- finished long-term examples: OpenMW, OpenRCT2, OpenTTD

Use it for porting (another OS, the browser), preservation, mashups whose host has no loader, and pulling one subsystem out of a console game (Skate 3's skating engine).

## Decide the scope in one sentence

"Load the first map and walk around with correct movement" is a good first goal. "Rewrite Half-Life 2" is not. A rewrite is large, so keep an honest list of what works and what's missing from day one.

## Order of preference for knowledge

1. **Community format specs and open-source readers.** Free, and usually enough for assets and maps.
2. **Official source releases or SDKs**: Quake/Doom GPL releases, the Source SDK, the Unreal source license, etc.
3. **Community decomp projects**: gta-reversed, sm64, OoT, and others.
4. **Decompile the user's own executable with Ghidra.** Do this only for logic nothing above covers (movement constants, physics, AI). Keep Ghidra databases out of the repo, and write findings up as notes.

## Build steps

1. **Extract.** Write extractor scripts (Python is common) that read the user's install, or the user's own disc dump for console games, and write convertible data into a gitignored folder. Alternatively, read the original formats at runtime.
2. **Engine.** Pick the stack the user wants:
   - **Rust + Bevy:** the compiler errors steer the agent well.
   - **C/C++:** fine if the user prefers it.
   - **TypeScript + WebGL/WebGPU** for browser targets. Watch out for:
     - asset loading: the user selects their install folder via the File System Access API or drag-and-drop
     - worker threads for simulation
     - typed arrays for chunk and tile data
3. **Rebuild the rules in order:** movement and camera, then maps and collision, then interactions and weapons, then AI, then everything else. Constants come from documentation or decompilation notes.
4. **Compare side by side** with the original. Record clips and numbers (jump height, run speed, damage), and log the differences as tasks.
5. **Document** what works, what's missing, the required game versions, and credits.

## Subsystem-as-library pattern (for mashups)

- Build the rebuilt subsystem as a library with a C ABI (a Rust `cdylib` with `extern "C"`): init, step(dt, input), get_state, shutdown.
- Load it from the host game's plugin (T1/T2).
- The host provides collision and rendering. The library owns its own physics and state machine.
- Example: GTA San AnSkateas loads `skate_ffi.dll` from an ASI plugin.

## Version-matching tools

Downgraders that move the user's own copy to the build a project targets are acceptable (gtasa-open-downgrader, for example). Anything that strips or bypasses protection is not.
