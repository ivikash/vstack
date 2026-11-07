from common import *

STEPS = [
 ("01","Trigger","A clock, or an event: a 1:1 tomorrow, a doc moved to review.","var(--lilac2)","var(--lilac)"),
 ("02","Gather","Cache-first. Fetch by role, never by tool name. Hash the evidence.","var(--sage2)","var(--sage)"),
 ("03","Diff","What changed since last run. Nothing changed? Stop here.","var(--peach2)","var(--peach)"),
 ("04","Write","A pure skill turns evidence into a draft. It calls no tools.","var(--sand2)","var(--sand)"),
 ("05","Gate","A critic checks the draft. Fix, re-run. Two to five passes.","var(--blue2)","var(--blue)"),
 ("06","Land","The draft waits where you press send or approve. Nothing is sent for you.","var(--sage2)","var(--sage)"),
 ("07","Record","One ledger line: what landed, where, when. The next cell reads it.","var(--lilac2)","var(--lilac)"),
]

def ladder():
    W,H=790,690
    sw,sh=346,74; dx,dy=66,86
    x0,ybase=14,H-sh-14
    out=[f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="position:absolute;left:8px;top:58px;overflow:visible">']
    out.append('<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="#4b4945"/></marker></defs>')
    coords=[]
    for i,(n,t,d,fill,edge) in enumerate(STEPS):
        x=x0+i*dx; y=ybase-i*dy
        coords.append((x,y))
        out.append(f'<path d="M{x+sw} {y+6} l14 -10 v{sh} l-14 10 z" fill="{edge}" opacity=".85"/>')
        out.append(f'<path d="M{x} {y+sh} l14 -10 h{sw} l-14 10 z" fill="{edge}" opacity=".55"/>')
        out.append(f'<rect class="solid" data-name="step{n}" x="{x}" y="{y}" width="{sw}" height="{sh}" rx="7" fill="{fill}" stroke="#2b2a27" stroke-width="1.6"/>')
        out.append(f'<text x="{x+18}" y="{y+48}" font-family="Plex" font-weight="700" font-size="28" fill="#4b4945">{n}</text>')
        out.append(f'<text x="{x+72}" y="{y+30}" font-family="Playfair" font-weight="800" font-size="21" fill="#2b2a27">{t}</text>')
        # wrap desc into 2 lines of ~34 chars
        words=d.split(); l1=[];l2=[]
        for w in words:
            if not l2 and len(" ".join(l1+[w]))<=36: l1.append(w)
            else: l2.append(w)
        out.append(f'<text x="{x+72}" y="{y+48}" font-family="Plex" font-size="11.5" fill="#4b4945">{" ".join(l1)}</text>')
        out.append(f'<text x="{x+72}" y="{y+63}" font-family="Plex" font-size="11.5" fill="#4b4945">{" ".join(l2)}</text>')
    # callouts: (step index, side, lines)
    callouts=[
      (0,"R",["Dry run first:","fixture in, files out."]),
      (1,"R",["Writers never fetch.","Gather does, by role."]),
      (3,"R",["Skills are the only place","voice and shape live."]),
      (5,"L",["You click once. Send,","approve, or discard."]),
      (6,"L",["Each level's ledger is","the next level's source."]),
    ]
    for i,side,lines in callouts:
        x,y=coords[i]
        if side=="R":
            tx=x+sw+40; ty=y+22
            out.append(f'<path class="edge" data-name="c{i}" d="M{tx-8} {ty+30} q-14 10 -28 {sh/2-30+4}" transform="translate(0,0)" stroke="#4b4945" stroke-width="1.6" fill="none" marker-end="url(#ah)"/>')
            anchor="start"
        else:
            tx=x-36; ty=y+16
            out.append(f'<path class="edge" data-name="c{i}" d="M{tx+8} {ty+30} q14 8 28 {sh/2-30+4}" stroke="#4b4945" stroke-width="1.6" fill="none" marker-end="url(#ah)"/>')
            anchor="end"
        for k,l in enumerate(lines):
            out.append(f'<text class="hand" x="{tx}" y="{ty+k*27}" text-anchor="{anchor}" font-family="Caveat" font-size="21" fill="#4b4945">{l}</text>')
    # flag on top step
    x,y=coords[6]
    out.append(f'<path d="M{x+sw-26} {y-4} v-54" stroke="#2b2a27" stroke-width="2.5"/><path d="M{x+sw-26} {y-58} h40 l-10 10 10 10 h-40 z" fill="#c25a4a" stroke="#2b2a27" stroke-width="2"/>')
    out.append('</svg>')
    return "".join(out)

body = header("manager-ops-kernel","seven-stage-cell","kernel notes · sheet 1 of 3 · Nov 2026",
  "A MANAGER'S AUTOMATION, ONE CELL AT A TIME · KERNEL NOTES",
  "The Seven-Stage Cell",
  "How one unit of manager automation runs on any agent harness, and you only press send.",
  ["trigger","gather","diff","write","gate","land","record","/check","/run","/verify-skills","/gen-cron"], GHOST)

glance = "".join(f'<div class="check"><b>✓</b><div>{t}</div></div>' for t in [
 "Verbs are public,<br>nouns are private",
 "Writers never fetch,<br>gatherers never write",
 "Nothing lands<br>ungated",
 "Record it, or it<br>did not happen",
 "Private work has<br>one exit: the ledger",
 "Dry run before<br>every live run"])

principles = "".join(f'<div class="pr"><i></i><strong>{a}</strong><span>{b}</span></div>' for a,b in [
 ("Skills write","Voice and structure live in SKILL.md files, shared by every harness."),
 ("Tools fetch","A role map turns docs.read into whatever your company runs."),
 ("Files remember","Evidence cache, append-only ledger. No daemon, no database."),
 ("You click once","Every output is a draft. Send, approve or discard.")])

iso = """<svg class="solid" data-name="iso" viewBox="0 0 220 120" width="110" height="60">
<g stroke="#2b2a27" stroke-width="1.6" stroke-linejoin="round">
<path d="M20 70 l40 -22 40 22 -40 22z" fill="#a9bedb"/><path d="M20 70 v22 l40 22 v-22z" fill="#8ea6c9"/><path d="M60 92 l40 -22 v22 l-40 22z" fill="#c9d6ea"/>
<path d="M70 42 l40 -22 40 22 -40 22z" fill="#a9c7a1"/><path d="M70 42 v22 l40 22 v-22z" fill="#8fb088"/><path d="M110 64 l40 -22 v22 l-40 22z" fill="#d6e5d1"/>
<path d="M120 80 l30 -16 30 16 -30 16z" fill="#e3c98b"/><path d="M120 80 v18 l30 16 v-18z" fill="#cfb374"/><path d="M150 96 l30 -16 v18 l-30 16z" fill="#efdfb4"/>
</g></svg>"""

tmpl = "".join(f'<div class="field"><em style="background:{c}">{k}</em><div>{v}</div></div>' for k,v,c in [
 ("TRIGGER","A cron expression, or an event the heartbeat watches for.","var(--lilac2)"),
 ("SOURCES","Roles, never tool names: docs.read, tasks.list, mail.search.","var(--sage2)"),
 ("WRITER","The skill that turns evidence.json into a draft.","var(--sand2)"),
 ("GATE","The critic, the doc type, min 2 and max 5 passes, a coverage bar.","var(--blue2)"),
 ("SINK","Where the draft waits for you, plus a dry_run_path.","var(--peach2)"),
 ("LEDGER","The fields one run records. The hub reads only these.","var(--lilac2)")])

cmds = "".join(f'<div class="cmd"><code>{a}</code><div>{b}</div></div>' for a,b in [
 ("kernel check","Graph and cells against the six invariants."),
 ("kernel run --dry-run","Fixture in, files out, nothing published."),
 ("kernel verify-skills","One skill copy, identical in every harness dir."),
 ("kernel gen-cron","Crontab lines, or Bot schedules, for every cell.")])

example = """<div class="mono" style="font-size:12px;line-height:1.6">
<span style="color:var(--rose)">ID:</span> program-update<br>
<span style="color:var(--rose)">TRIGGER:</span> 29 8 * * 1-5<br>
<span style="color:var(--rose)">SOURCES:</span> docs.read, tasks.list, mail.search<br>
<span style="color:var(--rose)">WRITER:</span> write-exec-update<br>
<span style="color:var(--rose)">GATE:</span> validate-writing, exec-update, 2..5<br>
<span style="color:var(--rose)">SINK:</span> chat.draft in the leadership channel<br>
<span style="color:var(--rose)">LEDGER:</span> overall, red sections, green-by dates</div>"""

body += f"""
<div class="card" style="left:36px;top:286px;width:300px;height:344px">
 <div class="abs k2" style="left:20px;top:18px">rules of the road</div>
 <div class="abs" style="left:20px;top:48px;width:262px">{glance}</div>
</div>
<div class="card" style="left:36px;top:646px;width:300px;height:374px">
 <div class="abs k2" style="left:20px;top:18px">who does what</div>
 <div class="abs" style="left:20px;top:46px;width:262px">{principles}</div>
 <div class="abs" style="left:160px;top:310px">{iso}</div>
</div>
<div class="card" style="left:352px;top:286px;width:812px;height:734px">
 <div class="abs k2" style="left:22px;top:18px">the cell · seven stages, one loop, every scale</div>
 <div class="abs mono" style="left:22px;top:40px;font-size:13.5px">trigger → gather → diff → write → gate → land → record. Section, document, bot, crew: same shape.</div>
 {ladder()}
</div>
<div class="card" style="left:36px;top:1036px;width:1128px;height:396px">
 <div class="abs" style="left:22px;top:16px;font-size:19px"><span class="mono" style="font-weight:700">cell.json</span> <span class="small" style="font-size:15px">one file per unit of automation. Copy it, change the nouns, keep the verbs.</span></div>
 <div class="btn" style="right:22px;top:14px">cells/*.json ↗</div>
 <div class="abs kicker" style="left:22px;top:60px">the six fields</div>
 <div class="abs small" style="left:22px;top:82px;width:520px">Use this for anything you write on a cadence: status updates, review packs, 1:1 prep, digests.</div>
 <div class="abs" style="left:22px;top:126px;width:520px">{tmpl}</div>
 <div class="abs" style="left:570px;top:60px;width:1px;height:316px;background:var(--line)"></div>
 <div class="abs kicker" style="left:596px;top:60px">the four verbs</div>
 <div class="abs" style="left:596px;top:86px;width:520px">{cmds}</div>
 <div class="abs kicker" style="left:596px;top:222px">a real cell, abridged</div>
 <div class="abs" style="left:596px;top:242px;width:520px">{example}</div>
</div>
""" + footer("Writing lives in skills (open source). Plumbing lives in the kernel (open source).<br>Tool names, doc ids, rating scales and people live in your own private repo.",
             "github.com/ivikash/manager-ops-kernel · built with Kiro Crew")

open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"poster1.html"),"w").write(page(body,"The Seven-Stage Cell"))
print("poster1.html written")
