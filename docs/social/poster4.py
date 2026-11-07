"""Sheet 4: The Kernel Clock. Dark blueprint palette, line icons, Syne + JetBrains Mono + Space Grotesk."""
import os
from common import VALIDATOR, FONTS

CSS = f"""
@font-face{{font-family:Syne;src:url(file://{FONTS}/Syne.ttf)}}
@font-face{{font-family:JB;src:url(file://{FONTS}/JetBrains.ttf)}}
@font-face{{font-family:Grotesk;src:url(file://{FONTS}/SpaceGrotesk.ttf)}}
:root{{--bg:#0b1220;--panel:#111a2e;--panel2:#162238;--line:#223252;--ink:#e8eef8;--mute:#8fa1c2;
 --cyan:#5fe3d3;--amber:#f6b94a;--coral:#ff7b72;--violet:#b39dfc;--lime:#b8e986}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1200px;height:1500px;overflow:hidden;background:var(--bg);color:var(--ink);font-family:Grotesk,sans-serif}}
.page{{position:relative;width:1200px;height:1500px;background:
 linear-gradient(rgba(95,227,211,.07) 1px,transparent 1px) 0 0/40px 40px,
 linear-gradient(90deg,rgba(95,227,211,.07) 1px,transparent 1px) 0 0/40px 40px, var(--bg)}}
.abs{{position:absolute}}
.card{{position:absolute;background:var(--panel);border:1px solid var(--line);border-radius:14px}}
.mono{{font-family:JB,monospace}}
.kicker{{font-family:JB,monospace;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--cyan)}}
.k2{{font-family:JB,monospace;font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--mute)}}
.title{{font-family:Syne;font-weight:800;font-size:60px;line-height:1;letter-spacing:-.02em}}
.sub{{font-family:Grotesk;font-size:19px;color:var(--mute)}}
.chip{{display:inline-block;border:1px solid var(--line);border-radius:6px;padding:4px 10px;font-family:JB,monospace;font-size:12px;color:var(--ink);background:var(--panel2);margin:0 6px 6px 0}}
.small{{font-size:13px;color:var(--mute);line-height:1.45}}
"""

def icon(name, color, size=22):
    P={
     "clock":  '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
     "inbox":  '<path d="M3 13h5l2 3h4l2-3h5"/><path d="M5 5h14l2 8v6H3v-6z"/>',
     "doc":    '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5"/><path d="M10 13h7M10 17h7"/>',
     "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
     "bolt":   '<path d="M13 2L5 14h6l-1 8 9-13h-6z"/>',
     "cal":    '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
     "loop":   '<path d="M4 12a8 8 0 0 1 14-5l2 2"/><path d="M20 4v5h-5"/><path d="M20 12a8 8 0 0 1-14 5l-2-2"/><path d="M4 20v-5h5"/>',
     "send":   '<path d="M3 11l18-8-7 18-2-8z"/>',
     "bell":   '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 21h4"/>',
    }[name]
    return f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{P}</svg>'

BADGE = f"""<svg viewBox="0 0 160 160" width="160" height="160">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5fe3d3"/><stop offset="1" stop-color="#b39dfc"/></linearGradient></defs>
<path d="M80 12 L140 46 V114 L80 148 L20 114 V46 Z" fill="none" stroke="url(#g)" stroke-width="3"/>
<path d="M80 30 L124 55 V105 L80 130 L36 105 V55 Z" fill="#162238" stroke="#223252" stroke-width="1.5"/>
<circle cx="80" cy="80" r="26" fill="none" stroke="#5fe3d3" stroke-width="3"/>
<path d="M80 62v18l12 7" stroke="#f6b94a" stroke-width="4" stroke-linecap="round" fill="none"/>
<circle cx="80" cy="80" r="3.5" fill="#e8eef8"/>
</svg>"""

# ---------- the day strip ----------
PINS = [  # (hour decimal, lane, label, sub, color, icon)
 (7.0, 4,"Daily digest",      "chief · every day",   "var(--violet)","inbox"),
 (7.25,3,"Audio briefing",    "chief · on request",  "var(--violet)","bell"),
 (7.5, 2,"On-call digest",    "oe · Monday",         "var(--lime)",  "shield"),
 (8.0, 1,"Monday sweep",      "program · Monday",    "var(--cyan)",  "doc"),
 (8.48,0,"Program update",    "program · weekdays",  "var(--cyan)",  "doc"),
 (15.0,2,"Sev2 draft check",  "oe · Thursday",       "var(--lime)",  "shield"),
 (17.0,1,"Sync doc pre-fill", "program · Wed, Thu",  "var(--cyan)",  "doc"),
 (17.5,0,"Meeting summaries", "chief · every day",   "var(--violet)","clock"),
]
def strip():
    W=1088; x0=40; hw=(W-2*x0)/24; ys=250; laneH=36; top=ys-40
    o=[f'<svg viewBox="0 0 {W} 300" width="{W}" height="300" style="position:absolute;left:20px;top:46px;overflow:visible">']
    o.append(f'<rect class="solid" data-name="strip" x="{x0}" y="{ys-6}" width="{W-2*x0}" height="12" rx="6" fill="#162238" stroke="#223252"/>')
    # night shading 00-06 and 20-24
    o.append(f'<rect x="{x0}" y="{ys-6}" width="{6*hw}" height="12" rx="6" fill="#0b1220" stroke="#223252"/>')
    o.append(f'<rect x="{x0+20*hw}" y="{ys-6}" width="{4*hw}" height="12" rx="6" fill="#0b1220" stroke="#223252"/>')
    for h in range(0,25,2):
        x=x0+h*hw
        o.append(f'<path d="M{x} {ys+8} v8" stroke="#8fa1c2" stroke-width="1"/>')
        o.append(f'<text x="{x}" y="{ys+32}" text-anchor="middle" font-family="JB" font-size="10.5" fill="#8fa1c2">{h:02d}</text>')
    for h,lane,label,sub,color,ic in PINS:
        x=x0+h*hw; yl=top-lane*laneH
        o.append(f'<path class="edge" data-name="pin-{label}" d="M{x} {ys-6} V{yl+2}" stroke="{color}" stroke-width="1.6" stroke-dasharray="3 3"/>')
        o.append(f'<circle class="solid" data-name="dot-{label}" cx="{x}" cy="{ys}" r="5.5" fill="{color}"/>')
        o.append(f'<g transform="translate({x+8} {yl-20})"><rect class="solid" data-name="lbl-{label}" x="0" y="0" width="148" height="30" rx="6" fill="#162238" stroke="{color}" stroke-width="1"/>'
                 f'<text x="10" y="13" font-family="JB" font-weight="700" font-size="11" fill="#e8eef8">{label}</text>'
                 f'<text x="10" y="25" font-family="JB" font-size="9.5" fill="#8fa1c2">{sub}</text></g>')
    o.append('</svg>')
    return "".join(o)

# ---------- the week grid ----------
WEEK = [
 ("Daily digest",        [1,1,1,1,1,1,1],"var(--violet)"),
 ("Meeting summaries",   [1,1,1,1,1,0,0],"var(--violet)"),
 ("Asks ledger index",   [0,0,0,0,0,1,0],"var(--violet)"),
 ("Program update",      [1,1,1,1,1,0,0],"var(--cyan)"),
 ("Monday sweep",        [1,0,0,0,0,0,0],"var(--cyan)"),
 ("Sync doc pre-fill",   [0,0,1,1,0,0,0],"var(--cyan)"),
 ("Sync doc rollover",   [0,0,0,0,1,0,0],"var(--cyan)"),
 ("On-call digest",      [1,0,0,0,0,0,0],"var(--lime)"),
 ("Sev2 draft check",    [0,0,0,1,1,0,0],"var(--lime)"),
]
def week():
    o=['<div class="abs" style="left:22px;top:48px;width:560px">']
    o.append('<div class="mono" style="display:grid;grid-template-columns:170px repeat(7,52px);font-size:11px;color:var(--mute);margin-bottom:8px"><div></div>'+"".join(f'<div style="text-align:center">{d}</div>' for d in ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])+'</div>')
    for name,days,color in WEEK:
        o.append(f'<div class="mono" style="display:grid;grid-template-columns:170px repeat(7,52px);align-items:center;height:26px;font-size:11.5px"><div style="color:var(--ink)">{name}</div>'+
                 "".join(f'<div style="text-align:center"><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:{color if d else "transparent"};border:1.5px solid {color if d else "var(--line)"}"></span></div>' for d in days)+'</div>')
    o.append('</div>')
    return "".join(o)

EVENTS = [
 ("cal",  "var(--coral)", "1:1 prep",        "the calendar item for a 1:1 with a report, minus one day"),
 ("cal",  "var(--coral)", "Hiring loop",     "interview invite minus one day, debrief minus two hours"),
 ("bolt", "var(--amber)", "FYI to your lead","one of your docs moves to In Review"),
 ("bolt", "var(--amber)", "OOTO relay",      "an out-of-office invite lands in the team calendar"),
 ("loop", "var(--cyan)",  "Launch note",     "a What's New post names one of your services"),
]
def events():
    o=['<div class="abs" style="left:614px;top:48px;width:474px">']
    for ic,color,name,desc in EVENTS:
        o.append(f'<div style="display:flex;gap:12px;align-items:flex-start;margin-bottom:14px"><div style="flex:none;width:34px;height:34px;border-radius:8px;background:var(--panel2);border:1px solid var(--line);display:flex;align-items:center;justify-content:center">{icon(ic,color,20)}</div>'
                 f'<div><div class="mono" style="font-size:12.5px;font-weight:700">{name}</div><div class="small">{desc}</div></div></div>')
    o.append('</div>')
    return "".join(o)

OUTCOMES = [
 ("inbox","var(--violet)","One digest in your channel","needs me · done · blocked. Nothing else lands in your chat."),
 ("send", "var(--cyan)",  "Drafts waiting for one click","Slack compose box, a [DRAFT] doc, an Outlook draft. Never sent for you."),
 ("shield","var(--lime)", "A ledger line per run","what landed, where, when, how many gate passes. Append-only."),
 ("loop", "var(--amber)", "A cache that is already warm","this week's 1:1 evidence is next quarter's review pack."),
]
def outcomes():
    o=[]
    for i,(ic,color,h,d) in enumerate(OUTCOMES):
        x=22+i*272
        o.append(f'<div class="abs" style="left:{x}px;top:48px;width:250px;height:128px;border:1px solid var(--line);border-radius:10px;background:var(--panel2);padding:14px">'
                 f'<div style="display:flex;gap:10px;align-items:center;margin-bottom:8px">{icon(ic,color,22)}<div class="mono" style="font-size:12.5px;font-weight:700;color:{color}">{h}</div></div>'
                 f'<div class="small">{d}</div></div>')
    return "".join(o)

body=f"""
<div class="abs mono" style="left:40px;top:26px;font-size:15px;color:var(--mute)"><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:var(--cyan);vertical-align:-1px;margin-right:10px"></span>manager-ops-kernel / <b style="color:var(--ink)">kernel-clock</b></div>
<div class="abs mono" style="right:40px;top:27px;font-size:12px;letter-spacing:.14em;color:var(--mute)">kernel notes · sheet 4 of 4 · Nov 2026</div>
<div class="card" style="left:36px;top:62px;width:1128px;height:206px">
  <div class="abs" style="left:22px;top:22px;width:160px;height:160px">{BADGE}</div>
  <div class="abs kicker" style="left:214px;top:26px">when every cell wakes · and what you hold by 07:00</div>
  <div class="abs title" style="left:212px;top:50px">The Kernel Clock</div>
  <div class="abs sub" style="left:214px;top:122px;width:880px">Clocks for the cadence work, events for the rest. One digest a day, drafts waiting for one click.</div>
  <div class="abs" style="left:214px;top:160px;width:890px"><span class="chip">cron</span><span class="chip">heartbeat</span><span class="chip">07:00 digest</span><span class="chip">17:30 fold</span><span class="chip">events</span><span class="chip">ledger</span><span class="chip">one click</span></div>
</div>

<div class="card" style="left:36px;top:286px;width:1128px;height:366px">
  <div class="abs k2" style="left:22px;top:18px">the day · clock-driven cells on a 24-hour strip, local time</div>
  {strip()}
</div>

<div class="card" style="left:36px;top:668px;width:1128px;height:352px">
  <div class="abs k2" style="left:22px;top:18px">the week · which day each clock fires</div>
  {week()}
  <div class="abs" style="left:590px;top:44px;width:1px;height:280px;background:var(--line)"></div>
  <div class="abs k2" style="left:614px;top:18px">the events · cells that wait for something to happen</div>
  {events()}
</div>

<div class="card" style="left:36px;top:1036px;width:1128px;height:200px">
  <div class="abs k2" style="left:22px;top:18px">by 07:00 you hold</div>
  {outcomes()}
</div>

<div class="card" style="left:36px;top:1252px;width:1128px;height:172px">
  <div class="abs k2" style="left:22px;top:18px">the four rules the clock obeys</div>
  <div class="abs" style="left:22px;top:48px;width:1084px;display:grid;grid-template-columns:repeat(4,1fr);gap:18px">
    <div><div class="mono" style="font-size:12.5px;font-weight:700;color:var(--cyan);margin-bottom:6px">01 · diff before write</div><div class="small">Nothing changed since the last wake? The cell stops. No draft, no noise.</div></div>
    <div><div class="mono" style="font-size:12.5px;font-weight:700;color:var(--amber);margin-bottom:6px">02 · gate before land</div><div class="small">Two to five critic passes. A fix may never invent a fact.</div></div>
    <div><div class="mono" style="font-size:12.5px;font-weight:700;color:var(--coral);margin-bottom:6px">03 · private stays private</div><div class="small">People cells run on their own memory. Only drafts and sanitised ledger lines leave.</div></div>
    <div><div class="mono" style="font-size:12.5px;font-weight:700;color:var(--violet);margin-bottom:6px">04 · record or it did not happen</div><div class="small">One ledger line per run. The 07:00 digest reads ledgers, never sources.</div></div>
  </div>
</div>

<div class="abs mono" style="left:40px;top:1446px;width:640px;font-size:11.5px;line-height:1.5;color:var(--mute)">Times are the defaults in cells/*.json; edit the cron field to move a station.<br>Same clock on Claude Code, Codex, Kiro CLI and Kiro Crew.</div>
<div class="abs mono" style="right:40px;top:1455px;width:420px;text-align:right;font-size:11.5px;color:var(--mute)">github.com/ivikash/manager-ops-kernel · built with Kiro Crew</div>
"""

html=f"""<!doctype html><html><head><meta charset="utf-8"><title>The Kernel Clock</title><style>{CSS}</style></head>
<body><div class="page">{body}</div>{VALIDATOR}</body></html>"""
open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"poster4.html"),"w").write(html)
print("poster4.html written")
