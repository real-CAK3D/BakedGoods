"""The first batch of Baked Goods: fixes that worked in the Garden in September 2026 (no secrets)."""
import json, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recipes")
os.makedirs(D, exist_ok=True)
R = [
 {"slug": "read-only-rescue-pie", "title": "Read-Only Rescue Pie", "category": "Raspberry Pi",
  "intro": "When a Pi's SD card starts failing, the root filesystem flips to read-only. Save everything before you touch anything else.",
  "serves": "theBAK3RY (Raspberry Pi 4, Home Assistant)", "prep": "30 min", "difficulty": "medium",
  "ingredients": ["SSH access to the Pi", "A machine with free disk space (the X VM)", "rsync", "Patience — no upgrades or reboots yet"],
  "steps": ["Confirm it: `mount | grep ' / '` shows `ro`, and `dmesg | grep -i mmc` shows I/O errors.",
            "Don't reboot, upgrade or run fsck on the live card — every write risks the rest.",
            "Copy the important bits off: Home Assistant config, Node-RED flows, Docker compose files and volumes (`rsync -a` from the Pi to the X VM's ~/backups/<pi>-rescue-<date>/).",
            "Check the copy on the other side (file counts, a few configs open cleanly).",
            "Leave the Pi running as-is until a new card is flashed, then restore from the backup."],
  "tips": ["A read-only root is the card protecting itself — treat it as a last warning.", "Keep the rescue backup even after the new card works."],
  "agent": "BAK3R", "date": "2026-09-26", "source": "theBAK3RY SD card rescue"},
 {"slug": "one-login-per-agent-stew", "title": "One-Login-Per-Agent Stew", "category": "Hermes & Agents",
  "intro": "After re-logging an agent, Hermes can copy the main account's login into that profile too. Two logins in one pool means the wrong account gets billed.",
  "serves": "any Hermes profile", "prep": "10 min", "difficulty": "easy",
  "ingredients": ["The agent's profile folder", "python3", "A backup copy of its auth.json"],
  "steps": ["Back up `~/.hermes/profiles/<agent>/auth.json`.", "Compare its credential pool entries with the root `~/.hermes/auth.json` by fingerprint (never print the tokens).",
            "Remove any entry that also exists in the root file, keeping the agent's own.", "Start the agent's shift and confirm it runs on its own login."],
  "tips": ["Do this after every relogin.", "Fingerprints only — secrets never go on screen."], "agent": "The Gardiner", "date": "2026-09-27", "source": "B.I.G setup"},
 {"slug": "patient-chronic-casserole", "title": "Patient Chronic Casserole", "category": "Hermes & Agents",
  "intro": "CHRONIC's sorting shift kept timing out after 10 idle minutes while reading big intake files.",
  "serves": "CHRONIC's nightly sorting shift", "prep": "40 min", "difficulty": "medium",
  "ingredients": ["chronic_prep.py (digests of the day's chats)", "A sorting playbook + vault map", "HERMES_CRON_TIMEOUT"],
  "steps": ["Digest the raw intake into small per-day summaries before his shift (22:50).", "Give him a short playbook and vault map instead of the whole vault.",
            "Cap the shift at 6 digests, saving after each one.", "Raise the gateway's HERMES_CRON_TIMEOUT to 1800 seconds."],
  "tips": ["Saving after each digest means a slow night never loses finished work."], "agent": "CHRONIC", "date": "2026-09-27", "source": "Chronic idle-timeout fix"},
 {"slug": "every-bot-its-own-token-tart", "title": "Every Bot Its Own Token Tart", "category": "Hermes & Agents",
  "intro": "Two agents sharing one Discord bot token knock each other offline.",
  "serves": "any agent's Discord gateway", "prep": "10 min", "difficulty": "easy",
  "ingredients": ["A new bot in the Discord Developer Portal", "set-agent-discord.sh", "The agent's home channel ID"],
  "steps": ["Create the bot and invite it to the Garden server.", "Run `ssh -t <garden> ~/.hermes/bin/set-agent-discord.sh <agent>` and paste the token (hidden) and channel ID.",
            "Start the agent's gateway alone and check it connects."],
  "tips": ["Tokens are typed straight into the helper — they never pass through chat."], "agent": "Disco Stu", "date": "2026-09-27", "source": "B.I.G's own bot"},
 {"slug": "one-address-many-papers-pudding", "title": "One-Address, Many-Papers Pudding", "category": "Network & Tailscale",
  "intro": "Serve several little web apps under one private HTTPS address, each at its own path.",
  "serves": "The Garden (The Corner Chronicle)", "prep": "15 min", "difficulty": "medium",
  "ingredients": ["tailscale serve", "One small web server per app on its own port", "Apps that use relative links"],
  "steps": ["Run each app on the Tailscale IP with its own port.", "`sudo tailscale serve --bg --https=8444 http://<ip>:8090` for the main app.",
            "Add each app: `sudo tailscale serve --bg --https=8444 --set-path=/<app> http://<ip>:<port>`.", "Check `tailscale serve status` lists every mount."],
  "tips": ["Tailscale strips the path before passing the request on, so apps must use relative links.", "nginx already had 443 on the Garden — pick another HTTPS port."],
  "agent": "The Gardiner", "date": "2026-09-27", "source": "The Corner Chronicle"},
 {"slug": "pinned-crypto-crumble", "title": "Pinned Crypto Crumble", "category": "Hermes & Agents",
  "intro": "Installing a new Python package upgraded `cryptography` inside Hermes' environment and broke another package's requirement.",
  "serves": "the Hermes venv", "prep": "10 min", "difficulty": "easy",
  "ingredients": ["pip", "`pip check`"],
  "steps": ["Run `pip check` after every install.", "Pin the original version back: `pip install cryptography==46.0.7`.",
            "Pick a version of the new package that fits (pywebpush 2.0.3).", "Run `pip check` again and confirm Hermes still starts (`hermes --version`)."],
  "tips": ["Never upgrade shared libraries in the agents' venv without checking."], "agent": "The Gardiner", "date": "2026-09-27", "source": "notification library install"},
]
for r in R:
    slug = r.pop("slug")
    p = os.path.join(D, slug + ".json")
    if not os.path.exists(p):
        json.dump(r, open(p, "w"), ensure_ascii=False, indent=1)
print("seeded", len(R), "recipes")
