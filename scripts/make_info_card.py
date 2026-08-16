"""Generate the terminal/neofetch-style profile card."""
from pathlib import Path
from xml.sax.saxutils import escape
import os
STATIC=os.getenv("STATIC","0")=="1"
rows=[
("Name","Akash Senthilkumar"),
("Role","AI / Software Engineering"),
("Focus","LLM • RAG • AI Agents"),
("Languages","C • C++ • Java • Python • SQL"),
("AI Stack","Watsonx.ai • LLMs • RAG"),
("Web","React • Next.js • Flask • Node.js"),
("Building","Practical AI applications"),]
highlights=["AI Healthcare / Multi-Agent RAG","LegacyOps AI / Code Modernization","AI-powered web applications"]
svg_rows=[]
for i,(k,v) in enumerate(rows):
    y=118+i*34; delay=0 if STATIC else i*.10
    svg_rows.append(f'<g class="line" style="animation-delay:{delay:.2f}s"><text x="30" y="{y}" class="key">{escape(k)}</text><text x="118" y="{y}" class="value">{escape(v)}</text></g>')
hl=[]
for i,item in enumerate(highlights):
    y=372+i*22; delay=0 if STATIC else (len(rows)+i)*.10
    hl.append(f'<text x="30" y="{y}" class="highlight" style="animation-delay:{delay:.2f}s">› {escape(item)}</text>')
animation='' if STATIC else '.line,.highlight{opacity:0;transform:translateX(-8px);animation:enter .42s ease-out forwards}@keyframes enter{to{opacity:1;transform:translateX(0)}}'
svg=f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="490" height="424" viewBox="0 0 490 424">
<rect x="1" y="1" width="488" height="422" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="2"/>
<rect x="1" y="1" width="488" height="42" rx="12" fill="#161b22"/>
<circle cx="24" cy="22" r="6" fill="#ff5f56"/><circle cx="44" cy="22" r="6" fill="#ffbd2e"/><circle cx="64" cy="22" r="6" fill="#27c93f"/>
<text x="92" y="27" class="title">akash@github: ~/profile</text>
<text x="30" y="72" class="prompt">akash@github ~ $ neofetch</text>
<line x1="30" y1="88" x2="460" y2="88" stroke="#e5e7eb"/>
{''.join(svg_rows)}
<text x="30" y="354" class="section">Highlights</text>
{''.join(hl)}
<style>
.title,.prompt,.key,.value,.section,.highlight{{font-family:"Courier New","Liberation Mono",monospace}}.title{{font-size:14px;fill:#e8e6e3;font-weight:700}}.prompt{{font-size:13px;fill:#00f0ff;font-weight:700}}.key{{font-size:12px;fill:#ff007f;font-weight:700}}.value{{font-size:12px;fill:#c9d1d9}}.section{{font-size:12px;fill:#8a2be2;font-weight:700}}.highlight{{font-family:"Courier New","Liberation Mono",monospace;font-size:11px;fill:#39ff14}}{animation}
</style></svg>'''
Path("info-card.svg").write_text(svg,encoding="utf-8")
print("Wrote info-card.svg")
