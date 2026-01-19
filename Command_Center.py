import base64
from pathlib import Path
from string import Template

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
LOGO_PATH = ASSETS / "DS.png"

MAX_VIDEO_MB = 7.0  # si pesa más, desactivamos video para que NO se caiga


def b64_file(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8") if path.exists() else ""


def pick_video() -> tuple[Path | None, str]:
    if VIDEO_WEBM.exists():
        return VIDEO_WEBM, "video/webm"
    if VIDEO_MP4.exists():
        return VIDEO_MP4, "video/mp4"
    return None, ""


video_path, video_mime = pick_video()
logo_b64 = b64_file(LOGO_PATH)

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

if video_path:
    size_mb = video_path.stat().st_size / (1024 * 1024)
    if size_mb <= MAX_VIDEO_MB:
        video_b64 = b64_file(video_path)
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

html = Template(r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<style>
  :root {
    --pad-x: 28px;
    --pad-y: 22px;
    --fg: rgba(255,255,255,.92);
    --fg2: rgba(255,255,255,.76);
    --line: rgba(255,255,255,.12);
  }

  html, body {
    margin:0; padding:0; height:100%; background:#000;
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
  }

  .stage {
    position:relative; width:100vw; height:100vh; overflow:hidden; background:#000;
  }

  .bgvideo {
    position:absolute; inset:0; width:100%; height:100%;
    object-fit:cover;
    filter: brightness(.55) contrast(1.05) saturate(1.05);
    transform: scale(1.02);
    z-index: 1;
  }

  .bgsolid {
    position:absolute; inset:0;
    background: radial-gradient(900px 500px at 50% 40%, rgba(255,255,255,.06), rgba(0,0,0,.95));
    z-index: 1;
  }

  #react {
    position:absolute; inset:0; width:100%; height:100%;
    z-index:2;
    mix-blend-mode: screen;
    opacity: .95;
  }

  .vignette {
    position:absolute; inset:0; z-index:3;
    pointer-events:none;
    background:
      radial-gradient(1100px 650px at 50% 45%, rgba(0,0,0,0) 0%, rgba(0,0,0,.52) 72%, rgba(0,0,0,.78) 100%),
      linear-gradient(to bottom, rgba(0,0,0,.35), rgba(0,0,0,.72));
  }

  .nav {
    position:absolute; top:0; left:0; right:0; z-index:5;
    display:flex; align-items:center; justify-content:space-between;
    padding: var(--pad-y) var(--pad-x);
  }

  .brand {
    display:flex; align-items:center; gap:12px;
    color: var(--fg);
    font-weight:700;
    letter-spacing:.3px;
    font-size:16px;
  }

  .brand img {
    width: 34px; height: 34px;
    border-radius: 10px;
    object-fit: cover;
    box-shadow: 0 10px 28px rgba(0,0,0,.35);
  }

  .menu {
    display:flex; align-items:center; gap:10px;
  }

  .menu a {
    text-decoration:none;
    color: var(--fg2);
    font-size: 13px;
    padding: 9px 12px;
    border-radius: 999px;
    border: 1px solid transparent;
    transition: .18s ease;
  }
  .menu a:hover {
    color: var(--fg);
    border-color: var(--line);
    background: rgba(255,255,255,.04);
    backdrop-filter: blur(8px);
  }

  .hero {
    position:absolute; inset:0; z-index:6;
    display:grid; place-items:center;
    padding: 0 18px;
    text-align:center;
  }

  .terminal {
    display:inline-block;
    padding: 18px 22px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,.10);
    background: rgba(0,0,0,.28);
    backdrop-filter: blur(12px);
    box-shadow: 0 25px 65px rgba(0,0,0,.45);
    max-width: 980px;
    animation: floaty 6.2s ease-in-out infinite;
  }

  .terminal .line {
    display:flex;
    gap: 10px;
    justify-content:center;
    align-items: baseline;
  }

  #typed{
    color: rgba(255,255,255,.94);
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    font-size: clamp(44px, 6.2vw, 96px);
    font-weight: 750;
    letter-spacing: -0.03em;
    line-height: 1.03;
    white-space: pre-wrap;
    text-align: center;
    text-shadow:
      0 0 18px rgba(255,255,255,.10),
      0 0 42px rgba(255,255,255,.08),
      0 18px 60px rgba(0,0,0,.55);
    filter: blur(10px);
    opacity: 0;
    transform: translateY(10px);
    animation: reveal 900ms ease forwards;
    animation-delay: 250ms;
  }

  #typed.pulse{
    animation: reveal 900ms ease forwards, glowPulse 680ms ease-in-out 1;
  }

  .cursor{
    display:inline-block;
    width: 14px;
    height: 1.05em;
    transform: translateY(8px);
    background: rgba(255,255,255,.88);
    margin-left: 10px;
    border-radius: 3px;
    animation: blink 900ms steps(1) infinite;
    box-shadow: 0 0 18px rgba(255,255,255,.18);
  }

  @keyframes blink{ 50%{ opacity:0; } }

  @keyframes reveal{
    to{
      filter: blur(0px);
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes glowPulse{
    0%{
      text-shadow:
        0 0 18px rgba(255,255,255,.10),
        0 0 42px rgba(255,255,255,.08),
        0 18px 60px rgba(0,0,0,.55);
      transform: scale(1);
    }
    50%{
      text-shadow:
        0 0 26px rgba(255,255,255,.18),
        0 0 68px rgba(255,255,255,.14),
        0 24px 70px rgba(0,0,0,.55);
      transform: scale(1.01);
    }
    100%{
      text-shadow:
        0 0 18px rgba(255,255,255,.10),
        0 0 42px rgba(255,255,255,.08),
        0 18px 60px rgba(0,0,0,.55);
      transform: scale(1);
    }
  }

  @keyframes floaty{
    0%   { transform: translateY(0px); }
    50%  { transform: translateY(-6px); }
    100% { transform: translateY(0px); }
  }

  .subtitle {
    margin-top: 14px;
    color: rgba(255,255,255,.68);
    font-size: 13px;
  }

  .foot {
    position:absolute; left:0; right:0; bottom:0; z-index:7;
    padding: 18px var(--pad-x);
    color: rgba(255,255,255,.55);
    font-size: 12px;
    display:flex; justify-content:space-between; gap: 12px;
  }

  @media (max-width: 640px) {
    :root { --pad-x: 18px; --pad-y: 16px; }
    .terminal { padding: 16px 16px; border-radius: 16px; }
    #typed{ font-size: clamp(34px, 9vw, 64px); }
  }
</style>
</head>

<body>
  <div class="stage">
    $video_tag
    <canvas id="react"></canvas>
    <div class="vignette"></div>

    <div class="nav">
      <div class="brand">
        $brand_img
        <div>Portfolio JRR</div>
      </div>
      <div class="menu">
        <a href="./About_Me" target="_self">About</a>
        <a href="./Projects" target="_self">Projects</a>
        <a href="./Lab" target="_self">Lab</a>
        <a href="./Contact" target="_self">Contact</a>
      </div>
    </div>

    <div class="hero">
      <div class="terminal">
        <div class="line">
          <span id="typed"></span><span class="cursor"></span>
        </div>
        <div class="subtitle">Move your cursor — reactive field</div>
      </div>
    </div>

    <div class="foot">
      <div>antigravity-inspired</div>
      <div>© JorgeRR89</div>
    </div>
  </div>

<script>
(() => {
  const typedEl = document.getElementById('typed');
  const text = "welcome to my LAB";

  const startDelay = 950;
  const minDelay = 65;
  const maxDelay = 115;

  function sleep(ms){ return new Promise(r => setTimeout(r, ms)); }

  async function typeText(){
    await sleep(startDelay);
    typedEl.textContent = "";
    for (let i = 0; i < text.length; i++){
      typedEl.textContent += text[i];
      const jitter = Math.floor(minDelay + Math.random() * (maxDelay - minDelay));
      await sleep(jitter);
    }
    typedEl.classList.add("pulse");
  }
  typeText();

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
  const N = Math.min(160, Math.floor((w*h)/11000));
  const particles = [];

  function init() {
    particles.length = 0;
    for (let i=0;i<N;i++) {
      particles.push({
        x: rand(0,w), y: rand(0,h),
        vx: rand(-0.25,0.25), vy: rand(-0.25,0.25),
        r: rand(0.9, 2.1),
        a: rand(0.12, 0.52),
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

    ctx.globalCompositeOperation = 'source-over';
    ctx.fillStyle = 'rgba(0,0,0,0.14)';
    ctx.fillRect(0,0,w,h);

    ctx.globalCompositeOperation = 'lighter';
    ctx.lineWidth = 1;
    ctx.strokeStyle = 'rgba(255,255,255,0.25)';
    ctx.fillStyle = 'rgba(255,255,255,0.85)';

    const px = pointer.x, py = pointer.y;
    const forceRadius = Math.max(140, Math.min(280, Math.sqrt(w*w+h*h)*0.15));

    for (const p of particles) {
      p.vx += Math.cos(t + p.phase) * 0.002;
      p.vy += Math.sin(t + p.phase) * 0.002;

      const dx = p.x - px, dy = p.y - py;
      const dist = Math.sqrt(dx*dx + dy*dy) + 0.001;

      if (dist < forceRadius) {
        const k = (1 - dist/forceRadius);
        const repel = 0.05 * k;
        const swirl = 0.02 * k;
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

    const maxLink = 110;
    for (let i=0;i<particles.length;i++) {
      const a = particles[i];
      for (let j=i+1;j<particles.length;j++) {
        const b = particles[j];
        const dx = a.x-b.x, dy = a.y-b.y;
        const d2 = dx*dx + dy*dy;
        if (d2 < maxLink*maxLink) {
          const d = Math.sqrt(d2);
          const alpha = (1 - d/maxLink) * 0.22;
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
""").substitute(
    video_tag=video_tag,
    brand_img=brand_img,
)

st.components.v1.html(html, height=920, scrolling=False)
