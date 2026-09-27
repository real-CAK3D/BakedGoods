# Baked Goods

The Garden's cookbook of fixes that actually worked, each written as a recipe: what it fixes, what it serves, prep time, ingredients (tools), the method, and the chef's tips. CHRONIC bakes new ones every Saturday from the week's successful fixes.

Part of the Garden's papers, all read through **[The Corner Chronicle](https://github.com/real-CAK3D/NewsStand)** — one home-screen app that mounts every paper under one private (Tailscale-only) HTTPS address: [The Double Wide](https://github.com/real-CAK3D/TheDoubleWide) (daily), [The Re-Up](https://github.com/real-CAK3D/TheRe-Up) (want ads), [The Sunday Smoke](https://github.com/real-CAK3D/TheSundaySmoke) (Sundays), [Roach Clips](https://github.com/real-CAK3D/RoachClips) (Tuesdays), [The Green Thumb](https://github.com/real-CAK3D/TheGreenThumb) (the directory), [Dime Bags](https://github.com/real-CAK3D/DimeBags), [Trail Mix](https://github.com/real-CAK3D/TrailMix), [Dab Magazine](https://github.com/real-CAK3D/DabMagazine), [Hashish](https://github.com/real-CAK3D/Hashish), [The Perennial](https://github.com/real-CAK3D/ThePerennial), [Baked Goods](https://github.com/real-CAK3D/BakedGoods) and [Extra! Extra!](https://github.com/real-CAK3D/ExtraExtra). The papers are written by [Hermes](https://github.com/NousResearch/hermes-agent) agents running on a small Oracle VM called The Garden.

## Files

| File | What it does |
|---|---|
| `build_baked.py` | Prints the cookbook with a tappable table of contents. |
| `recipes/` | One JSON file per recipe. |
| `seed_recipes.py` | The first batch (September 2026). |
| `prompts/baked_prompt.txt` | CHRONIC's baking-day instructions (also keeps Bedded Roots current). |
| `gardenweb.py` | The small shared web-server kit every Garden paper carries its own copy of. |

## Running

Saturdays at 14:00 Eastern; served at `/baked-goods/`. Each project is Linux-first (`%-d` date formatting) and expects a Hermes install on the same machine.
