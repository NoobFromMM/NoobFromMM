"""
Generate scripts/banner.html — the HTML banner with animated network background,
typewriter text, and cursor.

This script writes a self-contained HTML file. No external dependencies at
runtime — just open the HTML in a browser to preview.

CUSTOMIZATION — edit these before running:
  - DISPLAY_NAME (line ~28):   full name shown during the initial type-in
  - NICKNAME (line ~29):       the final nickname displayed after transform
  - TYPE_SPEED (line ~175):    ms per character during initial type
  - ERASE_SPEED (line ~188):   ms per character during backspace
  - INSERT_SPEED (line ~195):  ms per character when inserting nickname
"""

from pathlib import Path

# ── CUSTOMIZE THESE ────────────────────────────────────────
# DISPLAY_NAME: your full name as it appears while typing
# NICKNAME:     the short name that remains and gets the INSERT prefix
# INSERT:       the text inserted before the NICKNAME
# ────────────────────────────────────────────────────────────
DISPLAY_NAME = "Myat Thaw Maung"
NICKNAME = "MM"
INSERT = "NoobFrom"

out = Path(__file__).with_name("banner.html")

html = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>NoobFromMM Banner</title>
<style>
  html, body {
    margin: 0;
    width: 100%;
    height: 100%;
    background: #020817;
    display: grid;
    place-items: center;
    overflow: hidden;
  }

  .banner {
    position: relative;
    width: 900px;
    height: 180px;
    overflow: hidden;
    background: linear-gradient(115deg, #03172f 0%, #042d45 48%, #0b6f76 100%);
  }

  canvas {
    position: absolute;
    inset: 0;
    width: 900px;
    height: 180px;
  }

  .text {
    position: absolute;
    left: 0;
    right: 0;
    top: 50%;
    transform: translateY(-50%);
    text-align: center;
    font-family: Menlo, Monaco, Consolas, "Courier New", monospace;
    font-size: 30px;
    font-weight: 800;
    letter-spacing: 0.02em;
    color: #f4fbff;
    text-shadow:
      0 0 10px rgba(0, 255, 255, 0.35),
      0 2px 8px rgba(0, 0, 0, 0.45);
    white-space: nowrap;
  }

  .cursor {
    display: inline-block;
    width: 12px;
    height: 34px;
    margin-left: 5px;
    vertical-align: -7px;
    background: #22ff99;
    box-shadow: 0 0 12px rgba(34,255,153,.85);
    animation: blink .75s steps(1) infinite;
  }

  @keyframes blink {
    0%, 49% { opacity: 1; }
    50%, 100% { opacity: 0; }
  }
</style>
</head>
<body>
  <div class="banner">
    <canvas id="net" width="900" height="180"></canvas>
    <div class="text"><span id="typed"></span><span class="cursor"></span></div>
  </div>

<script>
const canvas = document.getElementById("net");
const ctx = canvas.getContext("2d");
const W = canvas.width;
const H = canvas.height;

const nodes = [
  [0, 70], [45, 30], [100, 92], [150, 58], [230, 118],
  [310, 75], [390, 35], [470, 88], [555, 55], [635, 108],
  [710, 45], [780, 78], [850, 32], [900, 96],
  [70, 145], [260, 35], [520, 132], [820, 142]
].map((p, i) => ({
  x: p[0],
  y: p[1],
  baseX: p[0],
  baseY: p[1],
  r: i % 4 === 0 ? 4.2 : 2.8,
  phase: i * 0.73,
  glow: i % 3 === 0
}));

function drawNetwork(t) {
  ctx.clearRect(0, 0, W, H);

  // background overlay glow
  const g = ctx.createRadialGradient(W * .82, H * .18, 0, W * .82, H * .18, 420);
  g.addColorStop(0, "rgba(0,255,245,0.18)");
  g.addColorStop(1, "rgba(0,255,245,0)");
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, W, H);

  // animated positions
  nodes.forEach(n => {
    n.x = n.baseX + Math.sin(t * 0.0007 + n.phase) * 12;
    n.y = n.baseY + Math.cos(t * 0.00055 + n.phase) * 7;
  });

  // lines
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const a = nodes[i], b = nodes[j];
      const dx = a.x - b.x;
      const dy = a.y - b.y;
      const d = Math.sqrt(dx * dx + dy * dy);

      if (d < 155) {
        const alpha = Math.max(0, 0.55 - d / 280);
        ctx.strokeStyle = `rgba(80,235,255,${alpha})`;
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.stroke();
      }
    }
  }

  // nodes
  nodes.forEach(n => {
    if (n.glow) {
      const glow = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, 22);
      glow.addColorStop(0, "rgba(0,255,255,0.75)");
      glow.addColorStop(.35, "rgba(0,210,255,0.25)");
      glow.addColorStop(1, "rgba(0,210,255,0)");
      ctx.fillStyle = glow;
      ctx.beginPath();
      ctx.arc(n.x, n.y, 22, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.fillStyle = n.glow ? "rgba(0,255,255,.95)" : "rgba(155,230,245,.85)";
    ctx.beginPath();
    ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
    ctx.fill();
  });

  requestAnimationFrame(drawNetwork);
}

requestAnimationFrame(drawNetwork);

// ── TEXT ANIMATION ──────────────────────────────────────────
// EDIT HERE to customize:
//   first  = your full display name (typed first, then erased)
//   keep   = the 1-3 letters that remain after erasing
//   insert = the prefix inserted before those kept letters
//   speed  = ms per character (lower = faster)
// ────────────────────────────────────────────────────────────
const el = document.getElementById("typed");
const prefix = "👋 Hi there! I'm ";
const first = "Myat Thaw Maung";   // EDIT: your full name
const keep = "MM";                 // EDIT: kept initials
const insert = "NoobFrom";         // EDIT: nickname prefix

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function type(text, speed = 70) {   // speed: ms per char
  for (let i = 1; i <= text.length; i++) {
    el.textContent = text.slice(0, i);
    await sleep(speed);
  }
}

async function eraseToMM(speed = 45) {    // speed: ms per char
  let name = first;

  // delete until only the two M letters remain
  while (name.length > 0) {
    if (name.endsWith("MM")) break;
    name = name.slice(0, -1);
    el.textContent = prefix + name;
    await sleep(speed);
  }

  // hard set to the intended kept result
  el.textContent = prefix + keep;
}

async function insertNoobFrom(speed = 72) {  // speed: ms per char
  let mid = "";
  for (let i = 1; i <= insert.length; i++) {
    mid = insert.slice(0, i);
    el.textContent = prefix + mid + keep;
    await sleep(speed);
  }
}

// ── Animation timing ───────────────────────────────────────
// EDIT HERE to change pauses and typing speed.
// All values in milliseconds.
async function runText() {
  await sleep(350);                      // initial delay before typing
  await type(prefix + first, 68);       // type full name at 68 ms/char
  await sleep(850);                      // pause after full name shown

  await eraseToMM(38);                  // erase at 38 ms/char
  await sleep(250);                      // pause before inserting nickname

  await insertNoobFrom(70);             // insert nickname at 70 ms/char
}

runText();
</script>
</body>
</html>
'''

out.write_text(html, encoding="utf-8")
print(f"Generated {out}")
print("Preview: open scripts/banner.html")
