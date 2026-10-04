# Legal lines and publishing (not legal advice)

## Why the guardrails exist

- **Own copies, single-player or offline.** Studying software you lawfully own, on your own machine, is broadly accepted. Many jurisdictions explicitly allow observing and testing how a program works. Online play adds other players, servers you don't own, and ToS enforcement, including bans.
- **No anti-cheat or DRM circumvention.** Bypassing technical protection measures is separately illegal in many places (the DMCA §1201 in the US, the EU InfoSoc Directive). It's also where the community and the agents draw a hard line.
- **No redistribution.** Decompiled source, extracted assets and game data are the rights holder's copyrighted work. Sharing *findings* (documentation, formats, your own code) is how OpenMW and OpenRCT2 exist. Sharing the *game's* files is infringement.
- **Mechanics vs. expression.** Game rules and mechanics generally aren't copyrightable. Code, art, audio, text, names and trademarks are. That's why T0 specs are written in your own words and the user's game uses its own art and names.
- **EULAs.** Game and mod-tool EULAs may restrict reverse engineering beyond what law allows, or limit tools to "making mods". Flag conflicts to the user and let them decide. Don't decompile an SDK whose license forbids it.

## Fine

- studying and decompiling a game you own, on your machine, for your own use
- publishing findings as documentation
- extractor tools that read each player's own copy
- downgraders that move your own copy to a matching version
- dumping your own disc

## Not fine

- bypassing DRM, encryption, activation or anti-cheat
- downloading ISOs, dumps or leaked source
- redistributing extracted or decompiled material
- tools whose purpose is bypassing access controls
- online or multiplayer cheats

## Repo hygiene

- Whitelist `.gitignore` from day one (`assets/gitignore-whitelist`).
- Workspace folders for decompiled or extracted material (`decomp/`, `extracted/`, `ghidra/`) are never committed.
- If something was pushed by mistake: assume it was copied, remove it, rewrite history, and tell the user.

## Publish checklist

- [ ] No game files, decompiled code or extracted assets in the repo or release zip
- [ ] README lists the required games and **exact versions**, loaders, and setup that builds from the player's own copies
- [ ] A "what works / what's missing" list
- [ ] Credits and licenses for everything built on (`THIRD-PARTY-NOTICES.md`)
- [ ] Marked as an unofficial fan project; AI use disclosed
- [ ] License chosen for the user's own code (MIT is common)
- [ ] Tested on a clean setup
- [ ] If a rights holder asks for removal, comply
