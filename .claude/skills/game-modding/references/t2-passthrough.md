# T2: Passthrough mashup (two games run at once, linked live)

One game is the **host** and draws the world. The other, the **gameplay game**, runs hidden and supplies mechanics such as movement, inventory, blocks or combat. Plugins in both games exchange state continuously. Neither half works without the other. Every player needs both games.

Reference implementation: **SkyCraft** (Minecraft inside Skyrim, github.com/chasmlol/SkyCraft). Clone it and read `README.md` and `docs/DESIGN.md` before designing anything. Its authority split is the most expensive thing to get wrong. Ports such as FalloutCraft (Fallout 4) and OWCraft (Outer Wilds) show how to swap the host side.

## Feasibility check (do first)

- Both games are on PC, single-player or offline, and owned by the user.
- **The host has a way to run code inside it** (SKSE, F4SE, an Outer Wilds mod loader, BepInEx, UE4SS, plugin-sdk, ...). If not, this becomes a T3 project.
- The gameplay game has a loader too (Fabric for Minecraft), **or** you rebuild just its subsystem as a library (T3). GTA San AnSkateas loads a Rust rebuild of Skate 3's engine as a DLL.
- The machine can run both: expect a few GB of extra RAM, and GPU headroom for a hidden second renderer.

## Architecture

- **Authority split:** write down who owns what. In SkyCraft, Minecraft owns the player, inventory and blocks, and Skyrim owns the world, NPCs, quests, saves and collision geometry. Each piece of state has exactly one owner.
- **Transport:** shared memory (a ring buffer with a fixed-layout struct) is fastest. Named pipes or localhost UDP are simpler fallbacks.
- **Per-frame exchange:**
  - the host sends player input, camera, nearby collision and NPC positions
  - the gameplay game sends player pose, HUD state, block changes, damage events and its offscreen render or draw lists
- **Rendering:** composite the hidden game's offscreen render into the host's frame and depth buffer, or redraw its objects natively in the host. Match lighting, fog and weather where possible.
- **Collision bridge:** feed host geometry into the gameplay game's physics so movement feels native. Digging or explosions need a shared voxel overlay saved on the gameplay side.
- **Damage and progression bridge:** map gameplay-side weapons onto host stats (SkyCraft scales damage to NPC level and trains Skyrim skills from Minecraft actions).
- **Input routing:** decide which game gets which keys, and keep a few host keys for the host's own menus (activate, journal, map, quickload).
- **Lifecycle:** the host launches the gameplay game hidden (no window, no audio) and shuts it down on exit. Never start a second instance.

## Build ladder (each rung is a playtest checkpoint)

1. Plugin loads in the host and writes a log line.
2. One value crosses from host to gameplay game (the player position).
3. One value crosses back.
4. The player moves in one game and appears correctly in the other.
5. Add features one at a time: HUD, blocks, combat, NPC reactions, progression, effects.

Rungs 1–2 are the whole trick. Once one value crosses, the architecture works and the rest is features.

## Performance

- Skip presenting the hidden window's swapchain. OWCraft went from 25 to 60 fps from that alone.
- Log frame times on both sides and the latency of the message channel. Hand the numbers to the agent and tune from evidence.

## Out of scope

- online or multiplayer games on either side
- anything behind anti-cheat
- sharing game files

LAN co-op of the gameplay game's own world (SkyCraft-style, each player with their own host world) is fine when that game supports it.
