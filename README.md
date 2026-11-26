# JokeVirus

> No harm. Pure chaos.

## What it does

| Effect | Detail |
|---|---|
| **Wallpaper swap** | Sets desktop wallpaper to `1111474383075081824.png` on launch |
| **PNG popup flood** | Random popups with your Assets PNGs every ~2 seconds. Clicking OK spawns 3 more. |
| **Icon swarm** | 25 error/warning/info system icons that chase and scatter around the cursor |
| **File bomb** | Copies all Assets PNGs to Desktop, Documents, and Temp with `CHAOS_` prefix + 15 extra desktop copies |

## Setup

1. Requires [.NET 6 SDK](https://dotnet.microsoft.com/download) to build
2. Drop your PNG files into the `Assets/` folder
3. Make sure `1111474383075081824.png` is in `Assets/` for the wallpaper effect
4. Run `build.bat` → grab `dist/JokeVirus.exe`
5. Keep `Assets/` folder next to the exe when deploying

## Build

```bat
build.bat
```

Output lands in `dist/JokeVirus.exe` — single self-contained exe, no .NET runtime needed on target.

## Cleanup (run on victim machine after)

```bat
cleanup.bat
```

Removes all `CHAOS_*` files, resets the temp BMP, restores blank wallpaper.
