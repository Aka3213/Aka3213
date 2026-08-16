"""Convert source-prepped.png into an animated monochrome ASCII SVG."""
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import Image, ImageOps
RAMP = " .`:-=+*cs#%@"
COLS, ROWS = 100, 53
CELL_W, CELL_H = 3.75, 8.0
FONT_SIZE = 8.2
WIDTH, HEIGHT = COLS*CELL_W, ROWS*CELL_H

def main():
    source = Path("source-prepped.png")
    if not source.exists(): raise SystemExit("Run prep_photo.py first.")
    image = ImageOps.fit(Image.open(source).convert("L"), (COLS,ROWS), method=Image.Resampling.LANCZOS)
    rows=[]
    for y in range(ROWS):
        s=[]
        for x in range(COLS):
            v=image.getpixel((x,y)); idx=round((255-v)/255*(len(RAMP)-1)); s.append(RAMP[idx])
        rows.append("".join(s).rstrip())
    clips=[]
    for i,row in enumerate(rows):
        y=(i+1)*CELL_H; delay=i*0.22
        clips.append(f'''<clipPath id="row{i}"><rect x="0" y="{i*CELL_H:.2f}" width="0" height="{CELL_H+1:.2f}"><animate attributeName="width" from="0" to="{WIDTH:.2f}" begin="{delay:.2f}s" dur="0.72s" fill="freeze"/></rect></clipPath><text x="0" y="{y:.2f}" clip-path="url(#row{i})">{escape(row)}</text>''')
    svg=f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH:.0f}" height="{HEIGHT:.0f}" viewBox="0 0 {WIDTH:.0f} {HEIGHT:.0f}">
<rect width="100%" height="100%" fill="#ffffff"/>
<style>text{{font-family:"Courier New","Liberation Mono",monospace;font-size:{FONT_SIZE}px;font-weight:600;letter-spacing:0;fill:#4b5563;white-space:pre;}}</style>
{''.join(clips)}
</svg>'''
    Path("avi-ascii.svg").write_text(svg,encoding="utf-8")
    print("Wrote avi-ascii.svg")
if __name__ == "__main__": main()
