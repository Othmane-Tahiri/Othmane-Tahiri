from pathlib import Path
from PIL import Image, ImageOps, ImageFilter

ROOT = Path(__file__).resolve().parents[1] / "assets"
SIZE = (900, 580)

for name in ("vandari", "unistay", "saffron-lane"):
    with Image.open(ROOT / f"{name}.jpg") as original:
        original = original.convert("RGB")
        background = ImageOps.fit(original, SIZE, method=Image.Resampling.LANCZOS)
        background = background.filter(ImageFilter.GaussianBlur(38))
        background = Image.blend(background, Image.new("RGB", SIZE, "#0c0716"), 0.32)
        foreground = ImageOps.contain(original, SIZE, method=Image.Resampling.LANCZOS)
        offset = ((SIZE[0] - foreground.width) // 2, (SIZE[1] - foreground.height) // 2)
        background.paste(foreground, offset)
        background.save(ROOT / f"{name}-card.jpg", quality=87, optimize=True, progressive=True)
