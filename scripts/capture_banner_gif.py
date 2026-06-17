import asyncio
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "scripts" / "banner.html"
FRAMES_DIR = ROOT / "assets" / "frames"
OUT = ROOT / "assets" / "intro.gif"

WIDTH = 900
HEIGHT = 180
FPS = 15
DURATION_SECONDS = 16
TOTAL_FRAMES = FPS * DURATION_SECONDS

async def main():
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": WIDTH, "height": HEIGHT},
            device_scale_factor=2
        )
        await page.goto(HTML.as_uri())

        frame_paths = []
        for i in range(TOTAL_FRAMES):
            await page.screenshot(path=str(FRAMES_DIR / f"frame_{i:04d}.png"))
            frame_paths.append(FRAMES_DIR / f"frame_{i:04d}.png")
            await page.wait_for_timeout(int(1000 / FPS))

        await browser.close()

    frames = []
    for path in frame_paths:
        img = Image.open(path).convert("RGB")
        # Downsample from device_scale_factor=2 to final 900x180 for crisp edges
        img = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
        frames.append(img.convert("P", palette=Image.Palette.ADAPTIVE, colors=128))

    frames[0].save(
        OUT,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / FPS),
        loop=0,
        optimize=True,
        disposal=2,
    )

    print(f"Generated {OUT}")
    print(f"Frames: {len(frames)}")
    print(f"Size: {OUT.stat().st_size / 1024:.1f} KB")

asyncio.run(main())
