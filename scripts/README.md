# Scripts — Intro GIF Generator

This folder contains the tools that generate the animated intro banner
(`assets/intro.gif`) used in the NoobFromMM profile README and portfolio page.

---

## Files

| File | Purpose |
|------|---------|
| `banner.html` | The HTML banner — animated network background, typewriter text, blinking cursor. Open in a browser to preview. |
| `make_intro_html.py` | Generates `banner.html` from Python. Edit the constants at the top to customize name, nickname, and animation speed. |
| `capture_banner_gif.py` | Captures `banner.html` as individual frames using Playwright, then assembles them into `assets/intro.gif`. |
| `make_intro_gif.py` | Alternative generator that creates `assets/intro.gif` directly with Pillow (no browser needed). Uses Python-based network animation. |

---

## Quick Start

### Preview the banner locally

```bash
# If banner.html doesn't exist yet, generate it:
python3 scripts/make_intro_html.py

# Then open it:
open scripts/banner.html
```

### Generate assets/intro.gif (Playwright method)

```bash
pip install playwright pillow
playwright install chromium

python3 scripts/make_intro_html.py    # step 1: generate HTML
python3 scripts/capture_banner_gif.py  # step 2: capture frames → GIF
```

Output: `assets/intro.gif`

### Generate assets/intro.gif (Pillow-only method)

```bash
# Uses .venv from the project root
.venv/bin/python scripts/make_intro_gif.py
```

Output: `assets/intro.gif`

---

## How to Customize

### Change the display name and nickname

**In `make_intro_html.py`:**

Edit these lines near the top:

```python
DISPLAY_NAME = "Your Full Name"    # typed first, then erased
NICKNAME = "XX"                    # 1-3 letters that remain
INSERT = "YourNickname"            # inserted before the nickname
```

Then regenerate:

```bash
python3 scripts/make_intro_html.py
python3 scripts/capture_banner_gif.py
```

**In `make_intro_gif.py`:**

Edit these in the text animation section:

```python
first_name = "Your Full Name"      # typed first
insert_part = "YourNickname"       # inserted before "MM"
```

Then regenerate:

```bash
.venv/bin/python scripts/make_intro_gif.py
```

### Change animation speed

**In `banner.html` / `make_intro_html.py`:**

The `type()`, `eraseToMM()`, and `insertNoobFrom()` functions accept a `speed`
parameter (milliseconds per character). Lower = faster.

```javascript
await type(prefix + first, 68);     // type-in speed (ms/char)
await eraseToMM(38);                // backspace speed (ms/char)
await insertNoobFrom(70);           // nickname insert speed (ms/char)
```

Also adjust the `await sleep()` calls to change pause durations.

**In `make_intro_gif.py`:**

The pause counts in the timeline control animation pacing:

```python
for _ in range(16):    # pause after full name is typed
    timeline.append(first_text)

for _ in range(6):     # pause after erasing to initials
    timeline.append(keep_text)

for _ in range(34):    # final pause before loop
    timeline.append(final_text)
```

Increase these numbers for longer pauses, decrease for faster animations.

### Capture only a specific frame range

In `capture_banner_gif.py`, edit these lines:

```python
TOTAL_FRAMES = 95          # capture frames 0 through 94
DURATION_SECONDS = 6.33    # = TOTAL_FRAMES / FPS (95 / 15)
```

For example, to get only frames 0000–0094, set `TOTAL_FRAMES = 95`.

---

## Requirements

| Tool | Dependencies |
|------|-------------|
| `banner.html` | None — just a browser |
| `make_intro_html.py` | Python 3, no external packages |
| `capture_banner_gif.py` | `pip install playwright pillow` + `playwright install chromium` |
| `make_intro_gif.py` | `pip install Pillow` (installed in `.venv/`) |

**No API keys, no external image assets, no secrets required.** Everything is
generated from code.
