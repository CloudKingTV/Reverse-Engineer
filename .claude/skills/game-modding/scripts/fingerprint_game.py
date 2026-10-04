#!/usr/bin/env python3
"""Locate an installed PC game and fingerprint it for modding / reverse engineering.

Reports engine, scripting backend, game-specific code files, installed mod loaders,
anti-cheat markers and suggested tools. Read-only: never modifies or copies game files.

Usage:
  python fingerprint_game.py --find "Core Keeper"      # search Steam/Epic libraries
  python fingerprint_game.py --path "D:/Games/Foo"     # fingerprint a folder
  python fingerprint_game.py --list                    # list installed games found
  add --json for machine-readable output
"""
import argparse, json, os, re, sys
from pathlib import Path

HOME = Path.home()

# ---------------------------------------------------------------- locating installs

def steam_roots():
    roots = []
    if sys.platform == "win32":
        try:
            import winreg
            for hive, key in [(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam"),
                              (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")]:
                try:
                    with winreg.OpenKey(hive, key) as k:
                        for name in ("SteamPath", "InstallPath"):
                            try: roots.append(Path(winreg.QueryValueEx(k, name)[0]))
                            except OSError: pass
                except OSError: pass
        except ImportError: pass
        for env in ("ProgramFiles(x86)", "ProgramFiles"):
            if os.environ.get(env): roots.append(Path(os.environ[env]) / "Steam")
    elif sys.platform == "darwin":
        roots.append(HOME / "Library/Application Support/Steam")
    else:
        roots += [HOME / ".steam/steam", HOME / ".local/share/Steam",
                  HOME / ".var/app/com.valvesoftware.Steam/.local/share/Steam"]
    return [r for r in dict.fromkeys(roots) if r.is_dir()]

def steam_libraries():
    libs = []
    for root in steam_roots():
        libs.append(root)
        vdf = root / "steamapps" / "libraryfolders.vdf"
        if vdf.is_file():
            for m in re.finditer(r'"path"\s+"([^"]+)"', vdf.read_text(errors="ignore")):
                libs.append(Path(m.group(1).replace("\\\\", "\\")))
    if sys.platform == "win32":
        for d in "CDEFGH":
            libs.append(Path(f"{d}:/SteamLibrary"))
    return [l for l in dict.fromkeys(libs) if (l / "steamapps" / "common").is_dir()]

def installed_games():
    games = {}
    for lib in steam_libraries():
        for d in (lib / "steamapps" / "common").iterdir():
            if d.is_dir(): games[d.name] = ("steam", d)
    manifests = Path(os.environ.get("ProgramData", "C:/ProgramData")) / "Epic/EpicGamesLauncher/Data/Manifests"
    if manifests.is_dir():
        for f in manifests.glob("*.item"):
            try:
                j = json.loads(f.read_text(errors="ignore"))
                p = Path(j.get("InstallLocation", ""))
                if p.is_dir(): games[j.get("DisplayName", p.name)] = ("epic", p)
            except (ValueError, OSError): pass
    return games

def norm(s): return re.sub(r"[^a-z0-9]", "", s.lower())

def find_game(name):
    games = installed_games()
    n = norm(name)
    exact = [v for k, v in games.items() if norm(k) == n]
    partial = [v for k, v in games.items() if n in norm(k) or norm(k) in n]
    hit = (exact or partial or [None])[0]
    return hit, games

# ---------------------------------------------------------------- fingerprinting

ENGINE_DLL_RX = re.compile(r"^(System|Mono\.|mscorlib|netstandard|Microsoft\.|UnityEngine|Unity\.|Newtonsoft|"
                           r"0Harmony|MonoMod|modio|Facepunch|Rewired|I2\.|QFSW|Sentry|io\.sentry|"
                           r"Steamworks|com\.rlabrecque|DOTween|Cinemachine|TextMeshPro|Zenject|"
                           r"Bolt|Photon|FMOD|Wwise|AK\.|Mirror|Telepathy|KinematicCharacter)", re.I)

ANTICHEAT = {
    "Easy Anti-Cheat": ["EasyAntiCheat", "EasyAntiCheat_EOS", "EasyAntiCheat_EOS_Setup.exe", "start_protected_game.exe"],
    "BattlEye": ["BattlEye", "BEService.exe", "BEService_x64.exe"],
    "Riot Vanguard": ["vgk.sys", "vgc.exe"],
    "XIGNCODE": ["xigncode", "XIGNCODE"],
    "nProtect GameGuard": ["GameGuard", "nProtect"],
    "EQU8": ["equ8", "EQU8"],
    "ACE (Tencent)": ["ACE-Base", "AntiCheatExpert"],
    "mhyprot": ["mhyprot2.sys", "mhyprot3.sys"],
}

LOADERS = {
    "BepInEx": ["BepInEx", "doorstop_config.ini", "winhttp.dll"],
    "MelonLoader": ["MelonLoader", "version.dll"],
    "UE4SS": ["ue4ss", "UE4SS.dll", "UE4SS-settings.ini"],
    "SKSE64": ["skse64_loader.exe"],
    "F4SE": ["f4se_loader.exe"],
    "ModEngine2": ["modengine2", "modengine2_launcher.exe", "config_eldenring.toml"],
    "ASI Loader": ["dinput8.dll", "scripts"],
    "tModLoader": ["tModLoader.dll", "tModLoader.exe"],
    "SMAPI": ["StardewModdingAPI.exe", "StardewModdingAPI.dll", "smapi-internal"],
    "Official mods folder": ["Mods", "mods", "StreamingAssets/Mods"],
}

def walk_limited(root, max_depth=4, max_entries=60000):
    count = 0
    root_depth = len(root.parts)
    for dirpath, dirnames, filenames in os.walk(root):
        depth = len(Path(dirpath).parts) - root_depth
        if depth >= max_depth: dirnames[:] = []
        for f in filenames + dirnames:
            count += 1
            if count > max_entries: return
            yield Path(dirpath) / f

def is_dotnet_assembly(p):
    try:
        with open(p, "rb") as fh:
            data = fh.read(4 * 1024 * 1024)
        return data[:2] == b"MZ" and b"BSJB" in data
    except OSError:
        return False

def unity_version(data_dir):
    for name in ("globalgamemanagers", "data.unity3d", "mainData"):
        f = data_dir / name
        if f.is_file():
            with open(f, "rb") as fh: head = fh.read(4096)
            m = re.search(rb"(20\d\d\.\d+\.\d+[abfp]\d+|[56]\d{3}\.\d+\.\d+[abfp]\d+)", head)
            if m: return m.group(1).decode()
    return None

def kb(p):
    try: return round(p.stat().st_size / 1024, 1)
    except OSError: return None

def fingerprint(root: Path):
    r = {"path": str(root), "engine": "Unknown / native", "backend": None, "version": None,
         "code_files": [], "engine_packages": [], "anticheat": [], "mod_loaders": [],
         "notes": [], "suggested_tools": []}
    files = list(walk_limited(root))
    names = {p.name for p in files}
    lower = {p.name.lower() for p in files}
    rel = {str(p.relative_to(root)).replace("\\", "/") for p in files}

    # anti-cheat and loaders
    for ac, markers in ANTICHEAT.items():
        if any(m in names or m.lower() in lower for m in markers): r["anticheat"].append(ac)
    for ld, markers in LOADERS.items():
        hits = [m for m in markers if m in names or any(x.endswith("/" + m) or x == m for x in rel)]
        if ld == "ASI Loader" and not ("dinput8.dll" in lower and any(n.endswith(".asi") for n in lower)): continue
        if ld == "BepInEx" and "BepInEx" not in names: continue
        if ld == "MelonLoader" and "MelonLoader" not in names: continue
        if hits: r["mod_loaders"].append(ld)

    data_dirs = [p for p in root.iterdir() if p.is_dir() and p.name.endswith("_Data")] if root.is_dir() else []
    # --- Unity
    if data_dirs and ("UnityPlayer.dll" in names or any((d / "globalgamemanagers").exists() or (d / "data.unity3d").exists() for d in data_dirs)
                      or "UnityPlayer.so" in names or "UnityPlayer.dylib" in names):
        d = data_dirs[0]
        r["engine"], r["version"] = "Unity", unity_version(d)
        managed = d / "Managed"
        il2cpp = any(n in names for n in ("GameAssembly.dll", "GameAssembly.so", "GameAssembly.dylib")) or (d / "il2cpp_data").is_dir()
        if il2cpp:
            r["backend"] = "IL2CPP"
            r["suggested_tools"] += ["Cpp2IL or Il2CppDumper (signatures + dummy DLLs)", "Ghidra (method bodies)",
                                     "BepInEx 6 IL2CPP / MelonLoader", "AssetRipper"]
            r["notes"].append("IL2CPP: C# bodies are compiled to native code; expect signatures, not source.")
        elif managed.is_dir():
            r["backend"] = "Mono"
            dlls = sorted(managed.glob("*.dll"), key=lambda p: -p.stat().st_size)
            r["code_files"] = [{"file": p.name, "kb": kb(p)} for p in dlls if not ENGINE_DLL_RX.match(p.name)]
            r["engine_packages"] = sorted({".".join(p.stem.split(".")[:2]) for p in dlls if p.name.startswith("Unity.")})
            r["suggested_tools"] += ["ILSpy / ilspycmd (dotnet tool install -g ilspycmd), pass -r <Managed>",
                                     "dnSpyEx (debugging)", "BepInEx/MelonLoader + Harmony (or the official SDK)",
                                     "AssetRipper / AssetStudio", "UnityExplorer (live inspection)"]
        if list(root.rglob("lib_burst_generated*")):
            r["notes"].append("Burst present: hot jobs are native, but their C# is still in the managed DLLs; patching them needs care.")
        if "Unity.Entities" in r["engine_packages"]:
            r["notes"].append("Unity DOTS/ECS: look for *System, IComponentData (*CD), *Authoring, [UpdateInGroup].")
        if "Unity.NetCode" in r["engine_packages"]:
            r["notes"].append("Netcode for Entities: client/server worlds exist even in single-player.")
    # --- Unreal
    elif any(x.endswith(".pak") and "/Content/Paks/" in "/" + x for x in rel) or any(n.endswith("-Shipping.exe") for n in names):
        r["engine"] = "Unreal Engine"
        r["backend"] = "IoStore (.utoc/.ucas)" if any(n.endswith(".utoc") for n in lower) else "Pak"
        r["code_files"] = [{"file": p.name, "kb": kb(p)} for p in files if p.name.endswith("-Shipping.exe")]
        r["suggested_tools"] += ["UE4SS (runtime Lua/C++ mods, reflection dump)", "FModel (unencrypted paks only)", "Ghidra"]
        r["notes"].append("If paks are encrypted, stop at official tools; do not extract keys.")
    # --- Godot
    elif any(n.endswith(".pck") for n in lower):
        r["engine"] = "Godot"
        r["suggested_tools"] += ["GDRE Tools (recover project + GDScript)", "Godot Mod Loader"]
    # --- GameMaker
    elif any(n in lower for n in ("data.win", "game.unx", "game.ios")):
        r["engine"] = "GameMaker"
        r["suggested_tools"] += ["UndertaleModTool"]
    # --- RPG Maker
    elif any(x.endswith(("js/rpg_core.js", "js/rmmz_core.js")) for x in rel):
        r["engine"] = "RPG Maker MV/MZ (JavaScript)"
        r["suggested_tools"] += ["Read www/js and data/*.json directly"]
    # --- Electron
    elif "app.asar" in lower:
        r["engine"] = "Electron / HTML5"
        r["suggested_tools"] += ["npx @electron/asar extract resources/app.asar out/"]
    # --- Bethesda
    elif any(n.endswith(".esm") for n in lower) and any(n.endswith((".bsa", ".ba2")) for n in lower):
        r["engine"] = "Bethesda Creation Engine"
        r["suggested_tools"] += ["SKSE/F4SE + Address Library", "xEdit", "Creation Kit (Papyrus sources)", "Ghidra"]
    # --- FromSoftware
    elif "regulation.bin" in lower:
        r["engine"] = "FromSoftware engine"
        r["suggested_tools"] += ["ModEngine2 (offline, EAC off)", "Smithbox / DSMapStudio", "WitchyBND"]
    # --- Source
    elif "gameinfo.txt" in lower or any(n.endswith(".vpk") for n in lower):
        r["engine"] = "Source"
        r["suggested_tools"] += ["Source SDK 2013", "VPKEdit / GCFScape", "Crowbar"]
    # --- Java
    elif any(n.endswith(".jar") for n in lower):
        r["engine"] = "Java"
        r["suggested_tools"] += ["Vineflower / CFR", "Fabric/NeoForge toolchain if Minecraft"]
    else:
        exes = [p for p in files if p.suffix.lower() == ".exe" and p.parent == root]
        xna = [n for n in names if re.match(r"(FNA|MonoGame\.Framework|Microsoft\.Xna\.Framework.*)\.dll$", n)]
        dotnet = [p for p in exes if is_dotnet_assembly(p)]
        if xna or dotnet:
            r["engine"], r["backend"] = ("XNA/FNA/MonoGame" if xna else ".NET"), "Managed (.NET)"
            r["code_files"] = [{"file": p.name, "kb": kb(p)} for p in dotnet]
            r["suggested_tools"] += ["ILSpy / dnSpyEx", "Harmony", "game-specific loader (tModLoader, SMAPI, ...)"]
        else:
            lua = [p for p in files if p.suffix.lower() == ".lua"] or [p for p in files if p.name == "scripts.zip"]
            if len(lua) > 5:
                r["engine"] = "Lua-scripted"
                r["suggested_tools"] += ["Read the Lua scripts directly", "official mod API"]
            else:
                r["code_files"] = [{"file": p.name, "kb": kb(p)} for p in exes]
                r["suggested_tools"] += ["Search for a community decomp / format docs first", "Ghidra",
                                         "ASI loader or game-specific SDK for injection"]

    if r["anticheat"]:
        r["notes"].insert(0, "ANTI-CHEAT PRESENT: online/competitive modes are off-limits. Proceed only in an official "
                             "offline mode with anti-cheat disabled, otherwise stop.")
    return r

def to_markdown(r):
    out = [f"# Fingerprint: {Path(r['path']).name}", "", f"- Path: `{r['path']}`",
           f"- Engine: **{r['engine']}**" + (f" {r['version']}" if r["version"] else ""),
           f"- Backend: **{r['backend'] or 'n/a'}**",
           f"- Anti-cheat: **{', '.join(r['anticheat']) or 'none detected'}**",
           f"- Mod loaders installed: {', '.join(r['mod_loaders']) or 'none detected'}"]
    if r["engine_packages"]: out.append(f"- Engine packages: {', '.join(r['engine_packages'])}")
    if r["code_files"]:
        out += ["", "## Game code files", "", "| File | Size (KB) |", "|---|---|"]
        out += [f"| {c['file']} | {c['kb']} |" for c in r["code_files"][:60]]
    if r["notes"]: out += ["", "## Notes", ""] + [f"- {n}" for n in r["notes"]]
    out += ["", "## Suggested tools (ask before installing)", ""] + [f"- {t}" for t in r["suggested_tools"]]
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--find", help="game name to search for in Steam/Epic libraries")
    g.add_argument("--path", help="game install folder")
    g.add_argument("--list", action="store_true", help="list installed games found")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.list:
        games = installed_games()
        if not games:
            print("No Steam/Epic libraries found. If this is a cloud/remote container, the games are on the user's PC.")
            return 1
        for k, (src, p) in sorted(games.items()): print(f"{src:6} {k}  ->  {p}")
        return 0
    if a.find:
        hit, games = find_game(a.find)
        if not hit:
            msg = {"error": "not_found", "query": a.find, "steam_libraries": [str(l) for l in steam_libraries()],
                   "installed_count": len(games),
                   "hint": "Pass --path, or if this is a cloud/remote container, run locally where the game is installed."}
            print(json.dumps(msg, indent=2) if a.json else
                  f"'{a.find}' not found. Libraries searched: {msg['steam_libraries'] or 'none'}.\n{msg['hint']}")
            return 2
        root = hit[1]
    else:
        root = Path(a.path)
        if not root.is_dir():
            print(f"Not a folder: {root}"); return 2
    r = fingerprint(root)
    print(json.dumps(r, indent=2) if a.json else to_markdown(r))
    return 0

if __name__ == "__main__":
    sys.exit(main())
