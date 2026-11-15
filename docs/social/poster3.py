from common import *

# Metro map: four lines (bots), stations (cells), one interchange (the ledger), one terminus (you).
COL={"program":"#5b7fb5","people":"#d08a6e","oe":"#6f9f68","chief":"#8b7fc0"}
LIGHT={"program":"var(--blue2)","people":"var(--peach2)","oe":"var(--sage2)","chief":"var(--lilac2)"}

LEDGER=(880,330); YOU=(170,730)
LINES={
 "program":{"y":140,"xend":880,"to":LEDGER,"stations":[(170,"Monday sweep","Mon 08:00"),(350,"Sync doc pre-fill","Wed, Thu"),(530,"Steering block","bi-weekly"),(710,"Program Update","2nd Monday")]},
 "people": {"y":330,"xend":880,"to":LEDGER,"stations":[(170,"1:1 prep","day before"),(350,"Hiring loop","per candidate"),(530,"Talent cards","per cycle"),(710,"Promo pack","per quarter")]},
 "oe":     {"y":520,"xend":880,"to":LEDGER,"stations":[(170,"On-call digest","Mon 07:30"),(350,"Sev2 reminder","Thu, Fri"),(530,"OOTO relay","on invite"),(710,"Gap finder","6 weeks out")]},
}

def metro():
    W,H=1128,800
    o=[f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="position:absolute;left:0;top:52px;overflow:visible">']
    lx,ly=LEDGER
    # private zone
    o.append('<rect class="solid" data-name="private-zone" x="118" y="282" width="682" height="98" rx="18" fill="rgba(208,138,110,.08)" stroke="#d08a6e" stroke-width="1.5" stroke-dasharray="8 6"/>')
    o.append('<text class="hand" x="122" y="404" font-family="Caveat" font-size="20" fill="#9a5a40">private lane: its own memory, its own files. The only way out is the ledger, and no rating rides on it.</text>')
    # rails
    hubs=f"{lx},{ly}"
    def rail(name,d,color,dash=""):
        o.append(f'<path class="rail" data-name="{name}" data-hubs="{hubs}" d="{d}" stroke="{color}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round" {dash}/>')
    rail("program",f"M120 140 H{lx-40} Q{lx} 140 {lx} 180 V{ly}",COL["program"])
    rail("people", f"M120 330 H{lx}",COL["people"])
    rail("oe",     f"M120 520 H{lx-40} Q{lx} 520 {lx} 480 V{ly}",COL["oe"])
    # chief line: ledger -> right -> down -> left to YOU
    rail("chief",  f"M{lx} {ly} H{1046-40} Q1046 {ly} 1046 {ly+40} V{730-40} Q1046 730 1006 730 H{YOU[0]+84}",COL["chief"])
    # stations
    def station(x,y,color,name,sub,side="above"):
        o.append(f'<circle class="solid" data-name="st-{name}" cx="{x}" cy="{y}" r="9" fill="#faf7f1" stroke="{color}" stroke-width="4"/>')
        if side=="above":
            o.append(f'<text x="{x}" y="{y-34}" text-anchor="middle" font-family="Plex" font-weight="700" font-size="12.5" fill="#2b2a27">{name}</text>')
            o.append(f'<text x="{x}" y="{y-19}" text-anchor="middle" font-family="Plex" font-size="10.5" fill="var(--mute)">{sub}</text>')
        else:
            o.append(f'<text x="{x}" y="{y+30}" text-anchor="middle" font-family="Plex" font-weight="700" font-size="12.5" fill="#2b2a27">{name}</text>')
            o.append(f'<text x="{x}" y="{y+45}" text-anchor="middle" font-family="Plex" font-size="10.5" fill="var(--mute)">{sub}</text>')
    for key,L in LINES.items():
        for x,name,sub in L["stations"]:
            station(x,L["y"],COL[key],name,sub,"above")
        # line name tag at the west end
        o.append(f'<rect x="20" y="{L["y"]-13}" width="92" height="26" rx="13" fill="{COL[key]}"/>')
        o.append(f'<text x="66" y="{L["y"]+4}" text-anchor="middle" font-family="Plex" font-weight="700" font-size="11" fill="#faf7f1">{ {"program":"PROGRAM","people":"PEOPLE","oe":"OE"}[key] }</text>')
    # chief stations on the bottom line, labels below
    for x,name,sub in [(800,"Meeting summaries","17:30 fold"),(590,"Inbox digest","07:00"),(380,"Asks ledger","hourly, Sat index")]:
        station(x,730,COL["chief"],name,sub,"below")
    o.append(f'<rect x="1066" y="{ly+60}" width="26" height="150" rx="13" fill="{COL["chief"]}"/>')
    o.append(f'<text transform="translate(1084 {ly+135}) rotate(90)" text-anchor="middle" font-family="Plex" font-weight="700" font-size="11" fill="#faf7f1">CHIEF OF STAFF</text>')
    # interchange
    o.append(f'<circle class="solid" data-name="ledger" cx="{lx}" cy="{ly}" r="22" fill="#faf7f1" stroke="#2b2a27" stroke-width="4"/>')
    o.append(f'<circle cx="{lx}" cy="{ly}" r="11" fill="none" stroke="#2b2a27" stroke-width="2.5"/>')
    o.append(f'<text x="{lx+34}" y="{ly-16}" font-family="Playfair" font-weight="800" font-size="20" fill="#2b2a27">Ledger</text>')
    o.append(f'<text x="{lx+34}" y="{ly+30}" font-family="Plex" font-size="10.5" fill="var(--mute)">append-only</text>')
    o.append(f'<text x="{lx+34}" y="{ly+44}" font-family="Plex" font-size="10.5" fill="var(--mute)">interchange</text>')
    # terminus: you
    yx,yy=YOU
    o.append(f'<rect class="solid" data-name="you" x="{yx-82}" y="{yy-34}" width="164" height="68" rx="34" fill="#2b2a27"/>')
    o.append(f'<text x="{yx}" y="{yy-4}" text-anchor="middle" font-family="Playfair" font-weight="800" font-size="20" fill="#faf7f1">You</text>')
    o.append(f'<text x="{yx}" y="{yy+16}" text-anchor="middle" font-family="Plex" font-size="10" fill="#faf7f1">terminus · one click</text>')
    # callouts
    o.append('<text class="hand" x="180" y="214" font-family="Caveat" font-size="20" fill="#4b4945">every station is one cell: trigger, gather, diff, write, gate, land, record</text>')
    o.append('<text class="hand" x="120" y="592" font-family="Caveat" font-size="20" fill="#4b4945">the OE line mostly rides on reports the team already publishes</text>')
    o.append(f'<text class="hand" x="560" y="{ly+108}" font-family="Caveat" font-size="20" fill="#4b4945">the hub never visits a source,</text>')
    o.append(f'<text class="hand" x="560" y="{ly+136}" font-family="Caveat" font-size="20" fill="#4b4945">it only reads the interchange</text>')
    o.append('</svg>')
    return "".join(o)

RAIL_CHECK = """
<script>
(function(){const base=window.__validate;window.__validate=function(){const out=base();out.railCrossings=[];out.railHitsText=[];
 const rails=[...document.querySelectorAll('.rail')].map(p=>({p,pts:poly(p),hubs:(p.getAttribute('data-hubs')||'').split(';').filter(Boolean).map(s=>{const [x,y]=s.split(',').map(Number);const m=p.ownerSVGElement.getScreenCTM();const q=new DOMPoint(x,y).matrixTransform(m);return {x:q.x,y:q.y}})}));
 const nearHub=(pt,r)=>r.hubs.some(h=>Math.hypot(h.x-pt.x,h.y-pt.y)<30);
 for(let i=0;i<rails.length;i++)for(let j=i+1;j<rails.length;j++){const A=rails[i].pts,B=rails[j].pts;
  for(let a=0;a<A.length-1;a++)for(let b=0;b<B.length-1;b++){if(segInter(A[a],A[a+1],B[b],B[b+1])&&!nearHub(A[a],rails[i])&&!nearHub(A[a],rails[j])){out.railCrossings.push([rails[i].p.dataset.name,rails[j].p.dataset.name,Math.round(A[a].x),Math.round(A[a].y)])}}
  // also parallel overlap: many sample points of A within 4px of B away from hubs
  let close=0;for(const pa of A){if(nearHub(pa,rails[i]))continue;for(const pb of B){if(Math.hypot(pa.x-pb.x,pa.y-pb.y)<4){close++;break}}}
  if(close>3)out.railCrossings.push([rails[i].p.dataset.name,rails[j].p.dataset.name,'overlap',close])}
 const texts=[...document.querySelectorAll('svg text')].map(t=>({t,r:t.getBoundingClientRect()}));
 for(const r of rails){for(const pt of r.pts){for(const t of texts){const b=t.r;if(pt.x>b.left&&pt.x<b.right&&pt.y>b.top&&pt.y<b.bottom){out.railHitsText.push([r.p.dataset.name,t.t.textContent.slice(0,30)]);break}}}}
 out.railHitsText=[...new Set(out.railHitsText.map(JSON.stringify))].map(JSON.parse);
 out.counts.rails=rails.length;return out}})();
</script>"""

body = header("manager-ops-kernel","metro-map","kernel notes · sheet 3 of 3 · Nov 2026",
  "FOUR LINES, ONE INTERCHANGE, ONE TERMINUS · KERNEL NOTES",
  "The Manager Metro Map",
  "Lines are bots. Stations are cells. All lines end at the ledger, then at you.",
  ["program line","people line","oe line","chief of staff","ledger","terminus: you"], GHOST)

body += f"""
<div class="card" style="left:36px;top:286px;width:1128px;height:900px">
 <div class="abs k2" style="left:22px;top:18px">the map · bots are lines, cells are stations, the ledger is the only interchange</div>
 {metro()}
</div>
<div class="card" style="left:36px;top:1202px;width:1128px;height:222px">
 <div class="abs kicker" style="left:22px;top:18px">how to read it</div>
 <div class="abs" style="left:22px;top:46px;width:340px;font-size:13.5px;line-height:1.45"><b>A line is a memory partition.</b> Two cells share a line when they read the same evidence. The People line keeps its own files and its own memory; nothing team-facing may board it.</div>
 <div class="abs" style="left:394px;top:46px;width:340px;font-size:13.5px;line-height:1.45"><b>A station is one cell.</b> Trigger, gather, diff, write, gate, land, record. Trains run on a clock (cron) or on an event (a heartbeat noticing a 1:1 tomorrow).</div>
 <div class="abs" style="left:766px;top:46px;width:340px;font-size:13.5px;line-height:1.45"><b>The interchange is append-only.</b> Each line records what landed, where and when. The Chief of Staff line never visits a source: it reads the interchange and hands you one digest a day.</div>
 <div class="abs mono" style="left:22px;top:160px;font-size:12.5px;color:var(--mute)">
  <span style="display:inline-block;width:28px;height:8px;border-radius:4px;background:{COL['program']};vertical-align:middle;margin-right:6px"></span>Program &nbsp;&nbsp;
  <span style="display:inline-block;width:28px;height:8px;border-radius:4px;background:{COL['people']};vertical-align:middle;margin-right:6px"></span>People (private) &nbsp;&nbsp;
  <span style="display:inline-block;width:28px;height:8px;border-radius:4px;background:{COL['oe']};vertical-align:middle;margin-right:6px"></span>Operational excellence &nbsp;&nbsp;
  <span style="display:inline-block;width:28px;height:8px;border-radius:4px;background:{COL['chief']};vertical-align:middle;margin-right:6px"></span>Chief of Staff &nbsp;&nbsp;
  <span style="display:inline-block;width:14px;height:14px;border-radius:50%;border:3px solid #2b2a27;vertical-align:middle;margin-right:6px"></span>interchange
 </div>
</div>
""" + footer("Same map, any harness: Claude Code, Codex, Kiro CLI, Kiro Crew.<br>Add a station by adding one cell.json. The map is checked, not drawn: kernel check refuses a line that skips the gate.",
             "github.com/ivikash/manager-ops-kernel · built with Kiro Crew")

html = page(body,"A Manager's Week as a Metro Map").replace("</body>", RAIL_CHECK+"</body>")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"poster3.html"),"w").write(html)
print("poster3.html written")
