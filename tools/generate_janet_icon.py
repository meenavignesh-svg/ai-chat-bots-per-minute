"""Generate a light-themed JANET .ico for Windows builds."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
ICO_PATH = ASSETS / "janet_icon.ico"
PNG_PATH = ASSETS / "janet_icon.png"


def load_font(size: int) -> ImageFont.ImageFont:
    for name in ("segoeuib.ttf", "arialbd.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def make_icon(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    pad = int(size * 0.08)
    draw.rounded_rectangle((pad, pad, size - pad, size - pad), radius=int(size * 0.22), fill=(255, 255, 255, 255), outline=(16, 185, 129, 255), width=max(3, size // 28))

    center = size // 2
    ring_r = int(size * 0.30)
    draw.ellipse((center - ring_r, center - ring_r, center + ring_r, center + ring_r), outline=(37, 99, 235, 255), width=max(3, size // 24))

    # Four small science nodes, intentionally rounded and non-angular.
    node_r = max(4, size // 22)
    for x, y, color in (
        (center, center - ring_r, (16, 185, 129, 255)),
        (center + ring_r, center, (37, 99, 235, 255)),
        (center, center + ring_r, (124, 58, 237, 255)),
        (center - ring_r, center, (20, 184, 166, 255)),
    ):
        draw.ellipse((x - node_r, y - node_r, x + node_r, y + node_r), fill=color)

    font = load_font(int(size * 0.27))
    text = "J"
    box = draw.textbbox((0, 0), text, font=font)
    tw = box[2] - box[0]
    th = box[3] - box[1]
    draw.text((center - tw / 2, center - th / 2 - int(size * 0.02)), text, fill=(17, 24, 39, 255), font=font)
    return img


def main() -> None:
    large = make_icon(512)
    large.save(PNG_PATH)
    sizes = [make_icon(size) for size in (16, 24, 32, 48, 64, 128, 256)]
    sizes[-1].save(ICO_PATH, sizes=[(img.width, img.height) for img in sizes], append_images=sizes[:-1])
    print(f"Generated {ICO_PATH}")


if __name__ == "__main__":
    main()
