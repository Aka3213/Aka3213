"""Fetch GitHub's public contribution calendar without a PAT."""
from collections import defaultdict
from datetime import date,timedelta,datetime,timezone
import json,os
from pathlib import Path
import requests
from bs4 import BeautifulSoup
USERNAME=os.getenv("GITHUB_USERNAME") or os.getenv("GITHUB_REPOSITORY_OWNER") or os.getenv("GITHUB_ACTOR")
if not USERNAME: raise SystemExit("Set GITHUB_USERNAME locally.")
url=f"https://github.com/users/{USERNAME}/contributions"
r=requests.get(url,headers={"User-Agent":"Mozilla/5.0 GitHub-profile-art/1.0"},timeout=30); r.raise_for_status()
soup=BeautifulSoup(r.text,"html.parser")
days={}; counts={}
for cell in soup.select("[data-date]"):
    raw=cell.get("data-date")
    if not raw: continue
    try: d=date.fromisoformat(raw)
    except ValueError: continue
    try: level=int(cell.get("data-level","0"))
    except ValueError: level=0
    days[d.isoformat()]=max(0,min(5,level))
    label=cell.get("aria-label","")
    try: counts[d.isoformat()]=int(label.split(" ",1)[0].replace(",",""))
    except (ValueError,IndexError): counts[d.isoformat()]=0
if not days: raise SystemExit("No contribution cells found; GitHub may have changed its HTML.")
parsed=sorted((date.fromisoformat(k),v) for k,v in days.items()); latest=parsed[-1][0]; start=latest-timedelta(days=364)
filtered=[x for x in parsed if x[0]>=start]; level_by_day=dict(filtered)
current=0; cursor=latest
while cursor in level_by_day and level_by_day[cursor]>0: current+=1; cursor-=timedelta(days=1)
longest=run=0; best_day=None; best_level=-1
for d,l in filtered:
    if l>0: run+=1; longest=max(longest,run)
    else: run=0
    if l>best_level: best_level=l; best_day=d
monthly=defaultdict(int)
for d,l in filtered: monthly[d.strftime("%Y-%m")]+=counts.get(d.isoformat(),0)
total=sum(counts.get(d.isoformat(),0) for d,_ in filtered)
payload={"username":USERNAME,"source":url,"fetched_at":datetime.now(timezone.utc).isoformat(),"days":[{"date":d.isoformat(),"level":l,"count":counts.get(d.isoformat(),0)} for d,l in filtered],"stats":{"contributions":total,"current_streak":current,"longest_streak":longest,"best_day":best_day.isoformat() if best_day else None,"active_days":sum(1 for _,l in filtered if l>0),"monthly_totals":dict(sorted(monthly.items()))}}
Path("data").mkdir(exist_ok=True); Path("data/contributions.json").write_text(json.dumps(payload,indent=2),encoding="utf-8")
print(f"Fetched {len(filtered)} days for @{USERNAME}; {total:,} contributions.")
