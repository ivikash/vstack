"""Shared chrome for the two posters: fonts, palette, header, footer, validator."""
import os
FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")

CSS = f"""
@font-face{{font-family:Playfair;src:url(file://{FONTS}/Playfair.ttf)}}
@font-face{{font-family:Caveat;src:url(file://{FONTS}/Caveat.ttf)}}
@font-face{{font-family:Plex;src:url(file://{FONTS}/PlexMono.ttf)}}
@font-face{{font-family:Plex;src:url(file://{FONTS}/PlexMonoBold.ttf);font-weight:700}}
@font-face{{font-family:Inter;src:url(file://{FONTS}/Inter.ttf)}}
:root{{
 --paper:#f3eee5; --card:#faf7f1; --ink:#2b2a27; --mute:#6d6a63; --line:#d9d2c5;
 --rose:#c25a4a; --sage:#a9c7a1; --sage2:#dfeadb; --blue:#a9bedb; --blue2:#dde6f3;
 --sand:#e3c98b; --sand2:#f4e9cf; --lilac:#c3bddc; --lilac2:#e9e6f3; --peach:#e9b9a3; --peach2:#f8e3d8;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:var(--paper);width:1200px;height:1500px;overflow:hidden;color:var(--ink);font-family:Inter,sans-serif}}
.page{{position:relative;width:1200px;height:1500px;background:
  radial-gradient(circle at 1px 1px, rgba(0,0,0,.055) 1px, transparent 1.6px) 0 0/22px 22px, var(--paper)}}
.card{{position:absolute;background:var(--card);border:1.5px solid var(--line);border-radius:18px;box-shadow:0 1px 0 rgba(0,0,0,.03)}}
.mono{{font-family:Plex,monospace}}
.kicker{{font-family:Plex,monospace;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--rose)}}
.k2{{font-family:Plex,monospace;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}}
.title{{font-family:Playfair,serif;font-weight:800;font-size:58px;line-height:1.02;letter-spacing:-.01em}}
.sub{{display:inline-block;background:#e6dfd2;border-radius:6px;padding:4px 10px;font-family:Plex,monospace;font-size:17px}}
.pill{{display:inline-block;border:1.3px solid var(--line);border-radius:999px;padding:4px 11px;font-family:Plex,monospace;font-size:12.5px;background:#fff;margin:0 6px 6px 0}}
.hand{{font-family:Caveat,cursive;font-size:21px;color:#4b4945;line-height:1.05}}
.small{{font-size:13.5px;color:var(--mute);line-height:1.4}}
.abs{{position:absolute}}
.check{{display:flex;gap:10px;align-items:flex-start;font-family:Plex,monospace;font-size:13.5px;line-height:1.35;margin-bottom:12px}}
.check b{{display:inline-block;width:18px;height:18px;border:1.5px solid #7fa877;border-radius:4px;color:#5e8f57;font-size:13px;text-align:center;line-height:16px;flex:none;margin-top:1px}}
.pr{{margin-bottom:14px;font-size:13.5px;line-height:1.35}}
.pr i{{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--peach);margin-right:8px;vertical-align:middle}}
.pr strong{{font-weight:700}}
.pr span{{display:block;color:var(--mute);margin-left:16px}}
.field{{display:flex;gap:12px;align-items:flex-start;margin-bottom:9px;font-size:13px;line-height:1.35}}
.field em{{font-style:normal;font-family:Plex,monospace;font-weight:700;font-size:12px;letter-spacing:.06em;flex:none;width:112px;padding:4px 8px;border-radius:5px}}
.cmd{{display:flex;gap:12px;align-items:flex-start;margin-bottom:8px;font-size:13px}}
.cmd code{{font-family:Plex,monospace;font-size:12px;border:1.3px solid var(--line);background:#fff;border-radius:6px;padding:3px 8px;flex:none;width:235px;white-space:nowrap}}
.btn{{position:absolute;border:1.5px solid var(--ink);border-radius:8px;padding:5px 12px;font-size:13px;background:#fff}}
"""

VALIDATOR = """
<script>
function rects(sel){return [...document.querySelectorAll(sel)].map(e=>({e,r:e.getBoundingClientRect()}))}
function inter(a,b){return a.left<b.right-1&&b.left<a.right-1&&a.top<b.bottom-1&&b.top<a.bottom-1}
function contains(a,b){return a.left<=b.left+1&&a.right>=b.right-1&&a.top<=b.top+1&&a.bottom>=b.bottom-1}
function anc(x,y){return x.contains(y)||y.contains(x)}
function segInter(p,q,r,s){const d=(q.x-p.x)*(s.y-r.y)-(q.y-p.y)*(s.x-r.x);if(Math.abs(d)<1e-9)return false;
 const t=((r.x-p.x)*(s.y-r.y)-(r.y-p.y)*(s.x-r.x))/d,u=((r.x-p.x)*(q.y-p.y)-(r.y-p.y)*(q.x-p.x))/d;return t>0.02&&t<0.98&&u>0.02&&u<0.98}
function poly(path){const L=path.getTotalLength();const pts=[];const n=Math.max(8,Math.ceil(L/6));const m=path.ownerSVGElement.getScreenCTM();
 for(let i=0;i<=n;i++){const p=path.getPointAtLength(L*i/n);const q=p.matrixTransform(m);pts.push({x:q.x,y:q.y})}return pts}
function validate(){
 const out={textOverlaps:[],edgeCrossings:[],edgeHitsBox:[],textOutside:[]};
 // text leaves: elements with direct text and no element children, plus SVG text
 const leaves=[...document.querySelectorAll('.page *')].filter(e=>{
   if(e.closest('svg')&&e.tagName.toLowerCase()!=='text')return false;
   if(e.tagName.toLowerCase()==='text')return true;
   return [...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim().length>0)});
 const L=leaves.map(e=>({e,r:e.getBoundingClientRect()}));
 for(let i=0;i<L.length;i++)for(let j=i+1;j<L.length;j++){
   const a=L[i],b=L[j];if(anc(a.e,b.e))continue;
   if(inter(a.r,b.r))out.textOverlaps.push([a.e.textContent.trim().slice(0,40),b.e.textContent.trim().slice(0,40)])}
 // text must stay inside its card
 out.overflow=[];for(const t of L){const c=t.e.closest('.card');if(c&&!contains(c.getBoundingClientRect(),t.r))out.overflow.push(t.e.textContent.trim().slice(0,40))}
 // solid boxes vs text: text must be inside or fully outside
 const boxes=rects('.solid');
 for(const t of L){for(const b of boxes){if(anc(t.e,b.e))continue;if(inter(t.r,b.r)&&!contains(b.r,t.r))out.textOutside.push([t.e.textContent.trim().slice(0,40),b.e.getAttribute('data-name')||b.e.className.baseVal||b.e.className])}}
 // edges
 const edges=[...document.querySelectorAll('.edge')].map(p=>({p,pts:poly(p)}));
 for(let i=0;i<edges.length;i++)for(let j=i+1;j<edges.length;j++){
   const A=edges[i].pts,B=edges[j].pts;let hit=false;
   for(let a=0;a<A.length-1&&!hit;a++)for(let b=0;b<B.length-1;b++){if(segInter(A[a],A[a+1],B[b],B[b+1])){hit=true;break}}
   if(hit)out.edgeCrossings.push([edges[i].p.getAttribute('data-name'),edges[j].p.getAttribute('data-name')])}
 for(const e of edges){const n=e.pts.length;for(let k=Math.floor(n*0.08);k<Math.floor(n*0.92);k++){const p=e.pts[k];
   for(const b of boxes){const r=b.r;if(p.x>r.left+2&&p.x<r.right-2&&p.y>r.top+2&&p.y<r.bottom-2){out.edgeHitsBox.push([e.p.getAttribute('data-name'),b.e.getAttribute('data-name')]);break}}
   for(const t of L){const r=t.r;if(t.e.closest('.hand')||t.e.classList.contains('hand'))continue;if(p.x>r.left+1&&p.x<r.right-1&&p.y>r.top+1&&p.y<r.bottom-1){out.edgeHitsBox.push([e.p.getAttribute('data-name'),'text:'+t.e.textContent.trim().slice(0,30)]);break}}}}
 out.edgeHitsBox=[...new Set(out.edgeHitsBox.map(JSON.stringify))].map(JSON.parse);
 out.counts={leaves:L.length,boxes:boxes.length,edges:edges.length};
 return out}
window.__validate=validate;
</script>
"""

def header(crumb_repo, crumb_page, right, kicker, title_html, subtitle, pills, avatar_svg):
    pills_html = "".join(f'<span class="pill">{p}</span>' for p in pills)
    return f"""
<div class="abs mono" style="left:40px;top:26px;font-size:16px;color:var(--mute)"><span style="display:inline-block;width:18px;height:18px;border:1.5px solid var(--line);border-radius:50%;vertical-align:-3px;margin-right:8px;background:#fff"></span>{crumb_repo} / <b style="color:var(--ink)">{crumb_page}</b></div>
<div class="abs mono" style="right:40px;top:28px;font-size:12.5px;letter-spacing:.12em;color:var(--mute)">{right}</div>
<div class="card" style="left:36px;top:62px;width:1128px;height:206px">
  <div class="abs" style="left:18px;top:18px;width:168px;height:168px;border-radius:14px;background:var(--lilac2);border:1.5px solid var(--line);overflow:hidden">{avatar_svg}</div>
  <div class="abs kicker" style="left:210px;top:22px">{kicker}</div>
  <div class="abs title" style="left:208px;top:44px;width:880px">{title_html}</div>
  <div class="abs" style="left:210px;top:118px"><span class="sub">{subtitle}</span></div>
  <div class="abs" style="left:210px;top:160px;width:890px">{pills_html}</div>
</div>"""

def footer(left, right):
    return f"""
<div class="abs mono" style="left:40px;top:1446px;width:640px;font-size:11.5px;line-height:1.5;color:var(--mute)">{left}</div>
<div class="abs mono" style="right:40px;top:1455px;width:420px;text-align:right;font-size:11.5px;color:var(--mute)">{right}</div>"""

GHOST = """<svg viewBox="0 0 168 168" width="168" height="168">
<ellipse cx="84" cy="150" rx="40" ry="7" fill="rgba(0,0,0,.08)"/>
<path d="M44 150 V86 a40 40 0 0 1 80 0 V150 l-13 -11 -13 11 -14 -11 -14 11 -13 -11 z" fill="#fff" stroke="#2b2a27" stroke-width="3" stroke-linejoin="round"/>
<circle cx="70" cy="86" r="5" fill="#2b2a27"/><circle cx="98" cy="86" r="5" fill="#2b2a27"/>
<path d="M74 104 q10 8 20 0" stroke="#2b2a27" stroke-width="3" fill="none" stroke-linecap="round"/>
<path d="M120 60 l14 -14 M128 70 l16 -4 M112 52 l4 -16" stroke="#c25a4a" stroke-width="3" stroke-linecap="round"/>
<rect x="28" y="118" width="22" height="26" rx="3" fill="#dfeadb" stroke="#2b2a27" stroke-width="2.5"/>
<path d="M33 126 h12 M33 132 h12 M33 138 h8" stroke="#2b2a27" stroke-width="2" stroke-linecap="round"/>
</svg>"""

def page(body, title):
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head>
<body><div class="page">{body}</div>{VALIDATOR}</body></html>"""
