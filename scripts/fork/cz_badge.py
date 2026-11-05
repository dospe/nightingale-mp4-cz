"""Add the Nightingale CZ badge to the upstream logos.

Reads the original logos from a git ref (default ``upstream/master``) so the
badge is never drawn twice, then writes the fork logos, the favicon and the
Apple touch icon. Regenerate the Tauri icon set afterwards with
``pnpm --dir client icons``.

Requires Pillow and a bold font (default: Inter ExtraBold from fonts-inter).
"""

import argparse
import io
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
SQUARE = "client/src/assets/images/logo_square.png"
WIDE = "client/src/assets/images/logo.png"
FAVICON = "client/public/favicon.png"
TOUCH_ICON = "client/public/apple-touch-icon.png"
DEFAULT_FONT = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"

BLUE = (17, 69, 126, 255)
RED = (215, 20, 26, 255)
WHITE = (255, 255, 255, 255)
SUPERSAMPLE = 4

# Badge box as fractions of the source image size: x, y, width, height.
SQUARE_BOX = (183 / 309, 218 / 309, 122 / 309, 74 / 309)
WIDE_BOX = (800 / 924, 222 / 310, 118 / 924, 72 / 310)


def badge(width: int, height: int, font_path: str) -> Image.Image:
    w, h = width * SUPERSAMPLE, height * SUPERSAMPLE
    ring = max(2, round(height * 0.09)) * SUPERSAMPLE
    radius = h // 2
    inner = [ring, ring, w - 1 - ring, h - 1 - ring]

    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=WHITE)
    draw.rounded_rectangle(inner, radius=radius - ring, fill=BLUE)

    inner_mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(inner_mask).rounded_rectangle(inner, radius=radius - ring, fill=255)
    stripe_h = round((h - 2 * ring) * 0.2)
    stripe = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(stripe).rectangle([0, h - ring - stripe_h, w, h], fill=RED)
    stripe_mask = Image.composite(stripe.getchannel("A"), Image.new("L", (w, h), 0), inner_mask)
    img.paste(stripe, (0, 0), stripe_mask)

    font = ImageFont.truetype(font_path, round((h - 2 * ring) * 0.68))
    left, top, right, _ = draw.textbbox((0, 0), "CZ", font=font, anchor="ls")
    x = (w - (right - left)) / 2 - left
    y = ring + (h - 2 * ring - stripe_h - top) / 2
    draw.text((x, y), "CZ", font=font, fill=WHITE, anchor="ls")

    return img.resize((width, height), Image.LANCZOS)


def with_badge(src: Image.Image, box: tuple[float, float, float, float], font_path: str) -> Image.Image:
    out = src.convert("RGBA")
    sw, sh = out.size
    x, y, w, h = round(box[0] * sw), round(box[1] * sh), round(box[2] * sw), round(box[3] * sh)
    out.alpha_composite(badge(w, h, font_path), (x, y))
    return out


def read_from_ref(ref: str, path: str) -> Image.Image:
    data = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{ref}:{path}"],
        check=True,
        capture_output=True,
    ).stdout
    return Image.open(io.BytesIO(data))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--ref", default="upstream/master", help="git ref with the original logos")
    parser.add_argument("--font", default=DEFAULT_FONT, help="bold font file for the badge text")
    args = parser.parse_args()

    square = with_badge(read_from_ref(args.ref, SQUARE), SQUARE_BOX, args.font)
    wide = with_badge(read_from_ref(args.ref, WIDE), WIDE_BOX, args.font)

    square.save(ROOT / SQUARE, optimize=True)
    wide.save(ROOT / WIDE, optimize=True)
    square.resize((32, 32), Image.LANCZOS).save(ROOT / FAVICON, optimize=True)
    square.resize((180, 180), Image.LANCZOS).save(ROOT / TOUCH_ICON, optimize=True)


if __name__ == "__main__":
    main()
