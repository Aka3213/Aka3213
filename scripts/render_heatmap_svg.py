"""Render contribution JSON as an animated 53-week SVG heatmap."""
from datetime import date,timedelta
from pathlib import Path
from xml.sax.saxutils import escape
import json
DATA=Path("data/contributions.json"); OUT=Path("contrib-heatmap.svg")
PALETTE=["#ebedf0","#c6e48b","#7bc96f","#239a3b","#196127","#0b3d1e"]
CELL,GAP=11,3; STEP=CELL+GAP; LEFT,TOP=44,34; WEEKS,DAYS=53,7; WIDTH=LEFT+WEEKS*STEP+16; HEIGHT=TOP+DAYS*STEP+74
def sunday(d): return d-timedelta(days=(d.weekday()+1)%7)
def main():
    if not DATA.exists(): raise SystemExit("Run fetch_contributions.py first.")
    p=json.loads(DATA.read_text()); dm={x["date"]:x for x in p["days"]}; dates=sorted(date.fromisoformat(x) for x in dm); end=dates[-1]; first=sunday(end)-timedelta(weeks=WEEKS-1)
    rects=[]
    for w in range(WEEKS):
        for dow in range(DAYS):
            d=first+timedelta(weeks=w,days=dow); item=dm.get(d.isoformat(),{"level":0,"count":0}); l=max(0,min(5,int(item["level"]))); delay=w*.035+dow*.012; x=LEFT+w*STEP; y=TOP+dow*STEP
            rects.append(f'<rect class="cell" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{PALETTE[l]}" data-date="{d}" data-count="{item.get("count",0)}" style="animation-delay:{delay:.3f}s"/>')
    s=p["stats"]; total=int(s.get("contributions",0)); active=int(s.get("active_days",0)); current=int(s.get("current_streak",0)); longest=int(s.get("longest_streak",0))
    legend=''.join(f'<rect x="{WIDTH-170+i*23}" y="{HEIGHT-27}" width="12" height="12" rx="2" fill="{c}"/>' for i,c in enumerate(PALETTE))
    svg=f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
<rect width="100%" height="100%" rx="12" fill="#fff" stroke="#d1d5db" stroke-width="2"/>
<text x="18" y="20" class="title">GitHub contribution activity</text>
<text x="18" y="{TOP+DAYS*STEP+24}" class="stats">{escape(f"{total:,} contributions · {active} active days · {current} day current streak · {longest} day longest streak")}</text>
<g aria-label="Contribution calendar">{''.join(rects)}</g>
<text x="18" y="{HEIGHT-17}" class="legend-label">Less</text>{legend}<text x="{WIDTH-25}" y="{HEIGHT-17}" class="legend-label" text-anchor="end">More</text>
<style>.title,.stats,.legend-label{{font-family:"Courier New","Liberation Mono",monospace}}.title{{font-size:13px;font-weight:700;fill:#111827}}.stats{{font-size:10px;fill:#6b7280}}.legend-label{{font-size:9px;fill:#6b7280}}.cell{{opacity:0;transform-box:fill-box;transform-origin:center;animation:reveal .48s cubic-bezier(.2,.7,.2,1) forwards}}@keyframes reveal{{0%{{opacity:0;transform:translate(-10px,-10px) scale(.7)}}100%{{opacity:1;transform:translate(0,0) scale(1)}}}}</style>
</svg>'''
    OUT.write_text(svg,encoding="utf-8"); print(f"Wrote {OUT}")
if __name__=="__main__": main()
