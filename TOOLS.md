# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## Model Configuration

**Primary model:** Anthropic Claude Haiku 4.5
**Fallback model:** Google Gemini 2.0 Flash
- API key stored in `~/.zprofile` as `GOOGLE_API_KEY`
- Fallback activates when primary model is unavailable or rate-limited
- Used for regular tasks, health checks, and heartbeats
- Anthropic reserved for deep analysis and complex work

**Status:** ✅ Configured and ready

**Aliases:**
- `haiku` → anthropic/claude-haiku-4-5
- `gemini-flash` → google/gemini-2-flash

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
