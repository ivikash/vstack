from common import *

# ---------- layer bands (three repositories) ----------
LAYERS = [
 ("L1 · skills","Leadership-Writing-Skills","public · MIT","write-talent-card · write-work-summary · write-promo-doc · write-exec-update · validate-writing · rewrite · house-rules.md · org-profile defaults","var(--sage2)","var(--sage)"),
 ("L2-L4 · kernel","manager-ops-kernel","public · MIT","cells/*.json · graph.json · six invariants · evidence cache + ledger schemas · runners for Claude Code, Codex, Kiro CLI, Kiro Crew","var(--blue2)","var(--blue)"),
 ("L0 · nouns","your-org-private","private","tools.json (role → real MCP tool) · org-profile.md (what principles, ratings, levels are called) · rubrics · cell configs with real doc ids and channels","var(--peach2)","var(--peach)"),
]
def layers():
    out=[]
    y=54
    for tag,name,vis,desc,fill,edge in LAYERS:
        out.append(f'''<div class="abs solid" data-name="layer-{tag[:2]}" style="left:22px;top:{y}px;width:1082px;height:84px;background:{fill};border:1.5px solid #2b2a27;border-radius:10px">
  <div class="abs mono" style="left:14px;top:10px;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute)">{tag}</div>
  <div class="abs" style="left:14px;top:28px;font-family:Playfair;font-weight:800;font-size:19px">{name}</div>
  <div class="abs mono" style="left:300px;top:12px;font-size:11px;padding:2px 8px;border-radius:999px;border:1.3px solid #2b2a27;background:#fff">{vis}</div>
  <div class="abs mono" style="left:300px;top:38px;width:760px;font-size:11px;line-height:1.3;color:#3b3a36">{desc}</div>
  <div class="abs" style="right:-1px;top:-1px;width:14px;height:84px;background:{edge};border-radius:0 10px 10px 0"></div>
</div>''')
        y+=94
    out.append('<div class="abs hand" style="left:22px;top:340px;width:1082px;font-size:20px">Verbs are public: how to gather, diff, write, gate, land, record. Nouns are private: which tool, which doc, which rubric, which person.</div>')
    return "".join(out)

# ---------- flow graph ----------
def flow():
    W,H=1082,470
    o=[f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="position:absolute;left:22px;top:52px;overflow:visible">']
    o.append('<defs><marker id="a2" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0 0 L9 4.5 L0 9 z" fill="#2b2a27"/></marker></defs>')
    bw,bh=92,74
    def box(name,x,y,title,sub,fill,w=bw,h=bh,dash=""):
        o.append(f'<rect class="solid" data-name="{name}" x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{fill}" stroke="#2b2a27" stroke-width="1.6" {dash}/>')
        o.append(f'<text x="{x+w/2}" y="{y+26}" text-anchor="middle" font-family="Playfair" font-weight="800" font-size="16" fill="#2b2a27">{title}</text>')
        for k,l in enumerate(sub):
            o.append(f'<text x="{x+w/2}" y="{y+44+k*14}" text-anchor="middle" font-family="Plex" font-size="10" fill="#3b3a36">{l}</text>')
    def arrow(name,x1,y1,x2,y2,label=None,ly=-8):
        o.append(f'<path class="edge" data-name="{name}" d="M{x1} {y1} L{x2} {y2}" stroke="#2b2a27" stroke-width="1.6" fill="none" marker-end="url(#a2)"/>')
        if label:
            o.append(f'<text x="{(x1+x2)/2}" y="{min(y1,y2)+ly}" text-anchor="middle" font-family="Plex" font-size="9" fill="var(--mute)">{label}</text>')
    gap=42
    cols=[14+i*(bw+gap) for i in range(6)]   # S C W G D L
    lanes=[("team",64,"var(--sage2)","Team · program, ops"),("hr",254,"var(--peach2)","Private · people, talent")]
    for lane,y,fill,label in lanes:
        # lane background
        lx,ly_,lw,lh=4,y-34,cols[5]+bw+10,bh+56
        dash='stroke-dasharray="7 5"' if lane=="hr" else ""
        o.append(f'<rect x="{lx}" y="{ly_}" width="{lw}" height="{lh}" rx="14" fill="rgba(255,255,255,.45)" stroke="#8a867d" stroke-width="1.3" {dash}/>')
        o.append(f'<text x="{lx+12}" y="{ly_+18}" font-family="Plex" font-size="11" letter-spacing="1.5" fill="var(--mute)">{label.upper()}</text>')
        S=["status docs","task tracker","mail, chat"] if lane=="team" else ["1:1 notes","review packs","hiring loops"]
        box(f"{lane}-S",cols[0],y,"Sources",S,"#fff")
        box(f"{lane}-C",cols[1],y,"Cache",["evidence.json","content hash","per entity"],fill)
        box(f"{lane}-W",cols[2],y,"Writer",["a skill","no tools","pure"],"var(--sand2)")
        box(f"{lane}-G",cols[3],y,"Gate",["critic loop","2 to 5 passes","no invention"],"var(--blue2)")
        box(f"{lane}-D",cols[4],y,"Draft",["waits for","your one click","never sent"],"var(--lilac2)")
        box(f"{lane}-L",cols[5],y,"Ledger",["append-only","what landed","where, when"],"#fff")
        for i,(a,b) in enumerate(zip(cols,cols[1:])):
            arrow(f"{lane}-e{i}",a+bw,y+bh/2,b,y+bh/2,["reads","writes","gates","lands","records"][i],ly=-14)
        # gate -> writer fix loop (curve above)
        gx=cols[3]+bw/2; wx=cols[2]+bw/2
        o.append(f'<path class="edge" data-name="{lane}-loop" d="M{gx} {y} C{gx} {y-26} {wx} {y-26} {wx} {y}" stroke="#c25a4a" stroke-width="1.5" fill="none" stroke-dasharray="4 3" marker-end="url(#a2)"/>')
        o.append(f'<text x="{(gx+wx)/2}" y="{y-25}" text-anchor="middle" font-family="Caveat" font-size="17" fill="#c25a4a">fix, re-run</text>')
    # privacy cut label under hr lane
    o.append(f'<text class="hand" x="{14}" y="{254+bh+42}" font-family="Caveat" font-size="18" fill="#4b4945">privacy cut: only drafts and sanitised ledger lines leave this lane. No rating, no candidate, no promo field.</text>')
    # hub
    hx=cols[5]+bw+46; hy=122; hw=140; hh=138
    box("hub",hx,hy,"Chief of Staff",["reads ledgers only","never sources","one digest a day","07:00, your channel"],"var(--sage2)",w=hw,h=hh)
    # ledger -> hub arrows: team L right-mid to hub left (upper), hr L right-mid up to hub left (lower)
    o.append(f'<path class="edge" data-name="team-L-hub" d="M{cols[5]+bw} {64+bh/2} L{hx} {hy+40}" stroke="#2b2a27" stroke-width="1.6" fill="none" marker-end="url(#a2)"/>')
    o.append(f'<path class="edge" data-name="hr-L-hub" d="M{cols[5]+bw} {254+bh/2} L{hx} {hy+hh-40}" stroke="#2b2a27" stroke-width="1.6" fill="none" marker-end="url(#a2)"/>')
    # hub -> you
    box("you",hx+hw+36,hy+hh/2-40,"You",["send, approve","or discard"],"#fff",w=86,h=80)
    arrow("hub-you",hx+hw,hy+hh/2,hx+hw+36,hy+hh/2)
    ly=404
    o.append(f'<text x="14" y="{ly}" font-family="Plex" font-size="10.5" letter-spacing="1.5" fill="var(--mute)">NODE TYPES</text>')
    items=[("S","source, read-only","#fff"),("C","cache","var(--sage2)"),("W","writer, pure skill","var(--sand2)"),("G","gate, pure critic","var(--blue2)"),("D","draft sink","var(--lilac2)"),("L","ledger, append-only","#fff"),("B","bot, memory partition","var(--sage2)")]
    x=110
    for k,lab,f in items:
        o.append(f'<rect x="{x}" y="{ly-13}" width="18" height="18" rx="4" fill="{f}" stroke="#2b2a27" stroke-width="1.3"/>')
        o.append(f'<text x="{x+9}" y="{ly}" text-anchor="middle" font-family="Plex" font-weight="700" font-size="10.5" fill="#2b2a27">{k}</text>')
        o.append(f'<text x="{x+24}" y="{ly}" font-family="Plex" font-size="10.5" fill="#3b3a36">{lab}</text>')
        x+=24+len(lab)*6.4+16
    o.append(f'<text x="14" y="{ly+26}" font-family="Plex" font-size="10.5" letter-spacing="1.5" fill="var(--mute)">EDGE TYPES</text>')
    o.append(f'<text x="110" y="{ly+26}" font-family="Plex" font-size="10.5" fill="#3b3a36">reads · writes · gates · lands · records · delegates. Only D and L nodes may have an edge out of the private lane.</text>')
    o.append('</svg>')
    return "".join(o)

# ---------- harness fan-out ----------
def harness():
    W,H=1082,170
    o=[f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="position:absolute;left:22px;top:44px;overflow:visible">']
    o.append('<defs><marker id="a3" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0 0 L9 4.5 L0 9 z" fill="#2b2a27"/></marker></defs>')
    kx,ky,kw,kh=W/2-170,0,340,46
    o.append(f'<rect class="solid" data-name="kernel-run" x="{kx}" y="{ky}" width="{kw}" height="{kh}" rx="9" fill="#2b2a27"/>')
    o.append(f'<text x="{W/2}" y="{ky+29}" text-anchor="middle" font-family="Plex" font-weight="700" font-size="15" fill="#faf7f1">kernel run cell.json --harness …</text>')
    names=[("Claude Code","claude -p","OS cron"),("Codex","codex exec","OS cron"),("Kiro CLI","kiro-cli chat --no-interactive","OS cron"),("Kiro Crew","Bot + cron_add / heartbeat","native, per Bot")]
    cw,ch=236,70; gap=(W-4*cw)/3
    for i,(n,cmd,sched) in enumerate(names):
        x=i*(cw+gap); y=96
        o.append(f'<rect class="solid" data-name="h-{i}" x="{x}" y="{y}" width="{cw}" height="{ch}" rx="9" fill="#fff" stroke="#2b2a27" stroke-width="1.6"/>')
        o.append(f'<text x="{x+14}" y="{y+24}" font-family="Playfair" font-weight="800" font-size="16" fill="#2b2a27">{n}</text>')
        o.append(f'<text x="{x+14}" y="{y+43}" font-family="Plex" font-size="10.5" fill="#3b3a36">{cmd}</text>')
        o.append(f'<text x="{x+14}" y="{y+59}" font-family="Plex" font-size="10.5" fill="var(--mute)">schedule: {sched}</text>')
        o.append(f'<path class="edge" data-name="fan-{i}" d="M{W/2 + (i-1.5)*40} {ky+kh} L{x+cw/2} {y}" stroke="#2b2a27" stroke-width="1.5" fill="none" marker-end="url(#a3)"/>')
    o.append('</svg>')
    return "".join(o)

body = header("manager-ops-kernel","architecture","field notes · A4 · Nov 2026",
  "GRAPH ENGINEERING FOR A MANAGER'S WEEK · KERNEL NOTES",
  "One Graph, Four Harnesses",
  "Same skills, same cells, same files. Only the runner changes.",
  ["sources","cache","writer","gate","draft","ledger","hub","privacy cut","4 harnesses"], GHOST)

body += f"""
<div class="card" style="left:36px;top:286px;width:1128px;height:380px">
 <div class="abs k2" style="left:22px;top:18px">three repositories · the public / private line</div>
 {layers()}
</div>
<div class="card" style="left:36px;top:682px;width:1128px;height:486px">
 <div class="abs k2" style="left:22px;top:18px">the flow · typed nodes, typed edges, six invariants checked by kernel check</div>
 {flow()}
</div>
<div class="card" style="left:36px;top:1184px;width:1128px;height:240px">
 <div class="abs k2" style="left:22px;top:18px">runs on · one thin adapter per harness, about ten lines each</div>
 {harness()}
</div>
""" + footer("Six invariants: every wake is a DAG · writers never fetch · one gate before every sink<br>· every sink records · the private lane has one exit · every cell has a dry run.",
             "github.com/ivikash/manager-ops-kernel · built with Kiro Crew")

open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"poster2.html"),"w").write(page(body,"One Graph, Four Harnesses"))
print("poster2.html written")
