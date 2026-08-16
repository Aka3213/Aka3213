"""Prepare a portrait for ASCII conversion."""
from pathlib import Path
import sys
from PIL import Image, ImageEnhance
try:
    import cv2
    import numpy as np
except ImportError as exc:
    raise SystemExit("Install scripts/requirements-local.txt first.") from exc
try:
    from rembg import remove
except ImportError as exc:
    raise SystemExit("Install scripts/requirements-local.txt first.") from exc

def main():
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("source-photo.jpg")
    if not source.exists():
        raise SystemExit(f"Missing {source}.")
    raw = Image.open(source).convert("RGBA")
    isolated = remove(raw)
    background = Image.new("RGBA", isolated.size, (255,255,255,255))
    composite = Image.alpha_composite(background, isolated).convert("RGB")
    gray = np.array(composite.convert("L"))
    clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    final = ImageEnhance.Contrast(Image.fromarray(enhanced, mode="L")).enhance(1.12)
    final.save("source-prepped.png")
    print("Wrote source-prepped.png")
if __name__ == "__main__": main()
