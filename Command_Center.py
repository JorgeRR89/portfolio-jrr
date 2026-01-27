from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Portfolio JRR",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"

VIDEO_WEBM = ASSETS / "Data.webm"
VIDEO_MP4 = ASSETS / "Data.mp4"
LOGO_PATH = ASSETS / "wizard_FN.png"

MAX_VIDEO_MB = 10.0  # si pesa más, desactivamos video para que NO se caiga


# =========================
# ROUTER (navegación robusta)
# =========================
GO_TO_PAGE = {
    "about": "pages/1_About_Me.py",
    "projects": "pages/2_Projects.py",
    "lab": "pages/Lab.py",
    "contact": "pages/3_Contact.py",
}

go = st.query_params.get("go", None)
if go in GO_TO_PAGE:
    # Limpia el query param para que no se quede “pegado” en otras páginas
    st.query_params.clear()
    st.switch_page(GO_TO_PAGE[go])


# =========================
# CACHES (performance)
# =========================
@st.cache_data(show_spinner=False)
def b64_file_cached(path_str: str) -> str:
    path = Path(path_str)
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode("utf-8")


@st.cache_data(show_spinner=False)
def pick_video_cached(webm_str: str, mp4_str: str) -> tuple[str, str]:
    webm = Path(webm_str)
    mp4 = Path(mp4_str)
    if webm.exists():
        return str(webm), "video/webm"
    if mp4.exists():
        return str(mp4), "video/mp4"
    return "", ""


video_path_str, video_mime = pick_video_cached(str(VIDEO_WEBM), str(VIDEO_MP4))
logo_b64 = b64_file_cached(str(LOGO_PATH))

# Limpia UI Streamlit
st.markdown(
    """
<style>
header[data-testid="stHeader"] {display:none;}
footer {visibility:hidden;}
.block-container { padding: 0 !important; max-width: 100% !important; }
section.main > div { padding: 0 !important; }
</style>
""",
    unsafe_allow_html=True,
)

video_b64 = ""
video_enabled = False
if video_path_str:
    vp = Path(video_path_str)
    size_mb = vp.stat().st_size / (1024 * 1024)
    if size_mb <= MAX_VIDEO_MB:
        video_b64 = b64_file_cached(video_path_str)
        video_enabled = bool(video_b64)

brand_img = f"<img alt='logo' src='data:image/png;base64,{logo_b64}' />" if logo_b64 else ""

if video_enabled:
    video_tag = f"""
    <video class="bgvideo" autoplay muted loop playsinline>
      <source src="data:{video_mime};base64,{video_b64}" type="{video_mime}">
    </video>
    """
else:
    video_tag = """<div class="bgsolid"></div>"""

html = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<style>
  :root{
    --pad-x: 28px;
    --pad-y: 22px;
    --fg: rgba(255,255,255,.94);
    --line: rgba(255,255,255,.12);
  }

  html, body{
    margin:0; padding:0; height:100%; background:#000;
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial;
  }

  .stage{ position:relative; width:100vw; height:100vh; overflow:hidden; background:#000; }

  .bgvideo{
    position:absolute; inset:0; width:100%; height:100%;
    object-fit:cover;
    filter: brightness(.55) contrast(1.06) saturate(1.05);
    transform: scale(1.02);
    z-index: 1;
  }

  .bgsolid{
    position:absolute; inset:0;
    background: radial-gradient(900px 500px at 50% 40%, rgba(255,255,255,.06), rgba(0,0,0,.95));
    z-index: 1;
  }

  #react{
    position:absolute; inset:0; width:100%; height:100%;
    z-index:2;
    mix-blend-mode: screen;
    opacity: .92;
    filter: blur(.2px);
  }

  .vignette{
    position:absolute; inset:0; z-index:3; pointer-events:none;
    background:
      radial-gradient(1200px 720px at 50% 45%, rgba(0,0,0,0) 0%, rgba(0,0,0,.54) 72%, rgba(0,0,0,.82) 100%),
      linear-gradient(to bottom, rgba(0,0,0,.30), rgba(0,0,0,.70));
  }

  .nav{
    position:absolute; top:0; left:0; right:0; z-index:6;
    display:flex; align-items:center; justify-content:space-between;
    padding: var(--pad-y) var(--pad-x);
    opacity: 0;
    transform: translateY(-10px);
    pointer-events: none;
    transition: opacity 700ms ease, transform 700ms ease;
  }
  .nav.show{
    opacity: 1;
    transform: translateY(0);
    pointer-events: auto;
  }

  .brand{
    display:flex; align-items:center; gap:12px;
    color: rgba(255,255,255,.92);
    font-weight:700;
    letter-spacing:.3px;
    font-size:16px;
  }

  .brand img{
    width: 34px; height: 34px;
    border-radius: 10px;
    object-fit: cover;
    box-shadow: 0 10px 28px rgba(0,0,0,.35);
  }

  .menu{ display:flex; align-items:center; gap:10px; }

  .menu a{
    text-decoration:none;
    color: rgba(255,255,255,.74);
    font-size: 13px;
    padding: 9px 12px;
    border-radius: 999px;
    border: 1px solid transparent;
    transition: .18s ease;
  }
  .menu a:hover{
    color: rgba(255,255,255,.92);
    border-color: var(--line);
    background: rgba(255,255,255,.04);
    backdrop-filter: blur(10px);
  }

  .hero{
    position:absolute; inset:0; z-index:5;
    display:grid; place-items:center;
    padding: 0 18px;
    text-align:center;
  }

  .headline{
    display:flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 14px;
    line-height: 1;
  }

  #typed{
    color: var(--fg);
    font-size: clamp(54px, 7.0vw, 112px);
    font-weight: 300;
    letter-spacing: -0.04em;
    line-height: 1;
    white-space: pre-wrap;
    text-shadow:
      0 0 12px rgba(255,255,255,.08),
      0 0 40px rgba(255,255,255,.06),
      0 18px 65px rgba(0,0,0,.58);

    opacity: 0;
    filter: blur(14px);
    transform: translateY(10px) scale(0.995);
    animation: reveal 900ms ease forwards;
    animation-delay: 220ms;
  }

  #typed.finalFocus{ animation: reveal 900ms ease forwards, microFocus 520ms ease-in-out 1; }
  #typed.glowPulse{ animation: reveal 900ms ease forwards, microFocus 520ms ease-in-out 1, glowPulse 650ms ease-in-out 1; }

  .typedWrap{ position: relative; display: inline-block; line-height: 1; }

  .cursor{
    position: absolute;
    left: calc(100% + 14px);
    bottom: 0;
    width: 0;
    border-left: 3px solid rgba(255,255,255,.92);
    border-radius: 2px;
    filter: drop-shadow(0 0 10px rgba(255,255,255,.22))
            drop-shadow(0 0 18px rgba(255,255,255,.10));
    opacity: 1;
    animation: caretBlink 1.6s steps(1) infinite;
    transform-origin: bottom;
  }
  .cursor.typing{ opacity: 0 !important; animation: none !important; }
  .cursor.ready{
    animation:
      caretBlink 1.6s steps(1) infinite,
      caretFloat 1.6s ease-in-out infinite,
      caretIn 260ms cubic-bezier(.22,1.2,.36,1) 1;
  }

  @keyframes caretBlink{ 0%,49%{opacity:1} 50%,100%{opacity:0} }
  @keyframes caretFloat{ 0%{transform:translateY(0)} 50%{transform:translateY(-0.06em)} 100%{transform:translateY(0)} }
  @keyframes caretIn{ 0%{opacity:0;transform:translateY(0.20em) scaleY(0.7)} 60%{opacity:1;transform:translateY(-0.02em) scaleY(1.05)} 100%{opacity:1;transform:translateY(0) scaleY(1)} }

  @keyframes reveal{ to{ opacity:1; filter: blur(0px); transform: translateY(0) scale(1);} }
  @keyframes microFocus{ 0%{filter:blur(1px);transform:scale(1)} 50%{filter:blur(2.2px);transform:scale(1.018)} 100%{filter:blur(0px);transform:scale(1)} }
  @keyframes glowPulse{
    0%{ text-shadow: 0 0 12px rgba(255,255,255,.08), 0 0 40px rgba(255,255,255,.06), 0 18px 65px rgba(0,0,0,.58); }
    50%{ text-shadow: 0 0 22px rgba(255,255,255,.16), 0 0 72px rgba(255,255,255,.12), 0 24px 78px rgba(0,0,0,.58); }
    100%{ text-shadow: 0 0 12px rgba(255,255,255,.08), 0 0 40px rgba(255,255,255,.06), 0 18px 65px rgba(0,0,0,.58); }
  }

  .subline{
    color: rgba(255,255,255,.78);
    font-weight: 300;
    letter-spacing: 0.02em;
    font-size: clamp(16px, 1.6vw, 22px);
    opacity: 0;
    transform: translateY(10px);
    filter: blur(6px);
    transition: opacity 700ms ease, transform 700ms ease, filter 700ms ease;
    text-shadow: 0 0 16px rgba(255,255,255,.06), 0 18px 65px rgba(0,0,0,.58);
  }
  .subline.show{ opacity: 1; transform: translateY(0); filter: blur(0px); }

  .foot{
    position:absolute; left:0; right:0; bottom:0; z-index:7;
    padding: 18px var(--pad-x);
    color: rgba(255,255,255,.55);
    font-size: 12px;
    display:flex; justify-content:space-between; gap: 12px;
    pointer-events:none;
  }

  @media (max-width: 640px){
    .cursor{ border-left-width: 2px; }
  }
</style>
</head>

<body>
  <div class="stage">
    __VIDEO_TAG__
    <canvas id="react"></canvas>
    <div class="vignette"></div>

    <div class="nav" id="topnav">
      <div class="brand">
        __BRAND_IMG__
        <div>Portfolio JRR</div>
      </div>

      <!-- ✅ LINKS ROBUSTOS: query param -->
      <div class="menu">
        <a href="?go=about">About me</a>
        <a href="?go=projects">Projects</a>
        <a href="?go=lab">Lab</a>
        <a href="?go=contact">Contact</a>
      </div>
    </div>

    <div class="hero">
      <div class="headline">
        <span class="typedWrap" id="wrap">
          <span id="typed"></span>
          <span class="cursor" id="caret"></span>
        </span>

        <div class="subline" id="subline">Keep it simple.</div>
      </div>
    </div>

    <div class="foot">
      <div>Move your cursor — reactive field</div>
      <div>© JorgeRR89</div>
    </div>
  </div>

<script>
(() => {
  // ===== Typing =====
  const typedEl = document.getElementById('typed');
  const caret = document.getElementById('caret');
  const nav = document.getElementById('topnav');
  const sub = document.getElementById('subline');

  const text = "welcome to my LAB";
  const startDelay = 980;
  const minDelay = 85;
  const maxDelay = 150;

  function sleep(ms){ return new Promise(r => setTimeout(r, ms)); }

  function syncCaretSize(){
    const cs = window.getComputedStyle(typedEl);
    const fontSize = parseFloat(cs.fontSize) || 64;
    const caretH = Math.round(fontSize * 0.92);
    caret.style.height = caretH + "px";
  }
  window.addEventListener("resize", syncCaretSize);

  async function typeText(){
    await sleep(startDelay);

    caret.classList.add("typing");
    caret.classList.remove("ready");

    typedEl.textContent = "";
    syncCaretSize();

    for (let i = 0; i < text.length; i++){
      typedEl.textContent += text[i];
      syncCaretSize();
      const jitter = Math.floor(minDelay + Math.random() * (maxDelay - minDelay));
      await sleep(jitter);
    }

    typedEl.classList.add("finalFocus");
    await sleep(520);
    typedEl.classList.add("glowPulse");

    syncCaretSize();

    caret.classList.remove("typing");
    caret.classList.add("ready");

    await sleep(140);
    sub.classList.add("show");

    await sleep(200);
    nav.classList.add("show");
  }
  typeText();

  // ===== Reactive field (breathing) =====
  const canvas = document.getElementById('react');
  const ctx = canvas.getContext('2d', { alpha: true });

  let w = 0, h = 0, dpr = Math.max(1, window.devicePixelRatio || 1);

  function resize() {
    w = Math.floor(window.innerWidth);
    h = Math.floor(window.innerHeight);
    dpr = Math.max(1, window.devicePixelRatio || 1);
    canvas.width = Math.floor(w * dpr);
    canvas.height = Math.floor(h * dpr);
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  window.addEventListener('resize', resize);
  resize();

  const pointer = { x: w*0.5, y: h*0.45 };
  function onMove(e) {
    const x = (e.touches ? e.touches[0].clientX : e.clientX);
    const y = (e.touches ? e.touches[0].clientY : e.clientY);
    pointer.x = x;
    pointer.y = y;
  }
  window.addEventListener('mousemove', onMove, { passive:true });
  window.addEventListener('touchmove', onMove, { passive:true });
  window.addEventListener('touchstart', onMove, { passive:true });

  const rand = (a,b)=> a + Math.random()*(b-a);

  // ✅ un poco menos costoso (igual se ve pro)
  const N = Math.min(130, Math.floor((w*h)/12000));
  const particles = [];

  function init() {
    particles.length = 0;
    for (let i=0;i<N;i++) {
      particles.push({
        x: rand(0,w), y: rand(0,h),
        vx: rand(-0.22,0.22), vy: rand(-0.22,0.22),
        r: rand(0.9, 2.0),
        a: rand(0.10, 0.50),
        phase: rand(0, Math.PI*2)
      });
    }
  }
  init();

  function drawLine(x1,y1,x2,y2,alpha) {
    ctx.globalAlpha = alpha;
    ctx.beginPath();
    ctx.moveTo(x1,y1);
    ctx.lineTo(x2,y2);
    ctx.stroke();
  }

  let t = 0;
  function frame() {
    t += 0.016;

    const breathe = 0.90 + 0.10 * Math.sin(t * 0.85);
    canvas.style.opacity = String(breathe);
    canvas.style.filter = `blur(${0.15 + 0.25*(1-breathe)}px)`;

    ctx.globalCompositeOperation = 'source-over';
    ctx.fillStyle = 'rgba(0,0,0,0.14)';
    ctx.fillRect(0,0,w,h);

    ctx.globalCompositeOperation = 'lighter';
    ctx.lineWidth = 1;
    ctx.strokeStyle = 'rgba(255,255,255,0.25)';
    ctx.fillStyle = 'rgba(255,255,255,0.85)';

    const px = pointer.x, py = pointer.y;
    const forceRadius = Math.max(140, Math.min(290, Math.sqrt(w*w+h*h)*0.16));

    for (const p of particles) {
      p.vx += Math.cos(t + p.phase) * 0.002;
      p.vy += Math.sin(t + p.phase) * 0.002;

      const dx = p.x - px, dy = p.y - py;
      const dist = Math.sqrt(dx*dx + dy*dy) + 0.001;

      if (dist < forceRadius) {
        const k = (1 - dist/forceRadius);
        const repel = 0.052 * k;
        const swirl = 0.020 * k;
        p.vx += (dx/dist) * repel + (-dy/dist) * swirl;
        p.vy += (dy/dist) * repel + ( dx/dist) * swirl;
      }

      p.vx *= 0.985;
      p.vy *= 0.985;
      p.x += p.vx;
      p.y += p.vy;

      if (p.x < -20) p.x = w+20;
      if (p.x > w+20) p.x = -20;
      if (p.y < -20) p.y = h+20;
      if (p.y > h+20) p.y = -20;
    }

    const maxLink = 108;
    for (let i=0;i<particles.length;i++) {
      const a = particles[i];
      for (let j=i+1;j<particles.length;j++) {
        const b = particles[j];
        const dx = a.x-b.x, dy = a.y-b.y;
        const d2 = dx*dx + dy*dy;
        if (d2 < maxLink*maxLink) {
          const d = Math.sqrt(d2);
          const alpha = (1 - d/maxLink) * (0.18 + 0.06*Math.sin(t*0.7));
          drawLine(a.x,a.y,b.x,b.y,alpha);
        }
      }
    }

    for (const p of particles) {
      ctx.globalAlpha = p.a;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI*2);
      ctx.fill();
    }

    requestAnimationFrame(frame);
  }
  frame();
})();
</script>
</body>
</html>
"""

html = html.replace("__VIDEO_TAG__", video_tag).replace("__BRAND_IMG__", brand_img)
st.components.v1.html(html, height=920, scrolling=False)
