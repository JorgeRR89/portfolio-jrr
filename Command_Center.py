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
VIDEO_PATH = ASSETS / "Data.mp4"   # tu video corto
LOGO_PATH = ASSETS / "DS.png"      # tu logo


def b64_file(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8") if path.exists() else ""


video_b64 = b64_file(VIDEO_PATH)
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

if not video_b64:
    st.error("No encuentro assets/data.mp4. Verifica la ruta.")
    st.stop()

brand_img = f"<img alt='logo' src='data:image/png;base64,{logo_b64}' />" if logo_b64 else ""

html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<style>
  :root {{
    --pad-x: 28px;
    --pad-y: 22px;
    --fg: rgba(255,255,255,.92);
    --fg2: rgba(255,255,255,.78);
    --line: rgba(255,255,255,.12);
    --glass: rgba(0,0,0,.22);
  }}

  html, body {{
    margin:0; padding:0;
    height:100%;
    background:#000;
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
  }}

  .stage {{
    position: relative;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    background:#000;
  }}

  /* Video background */
  .bgvideo {{
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
    object-fit: cover;
    filter: brightness(.55) contrast(1.05) saturate(1.05);
    transform: scale(1.02);
  }}

  /* Canvas reactive layer */
  #react {{
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
    z-index: 2;
    mix-blend-mode: screen;        /* “glow” */
    opacity: .95;
  }}

  /* Soft vignette + gradient */
  .vignette {{
    position:absolute;
    inset:0;
    z-index: 3;
    background:
      radial-gradient(1200px 700px at 50% 45%, rgba(0,0,0,0) 0%, rgba(0,0,0,.45) 72%, rgba(0,0,0,.72) 100%),
      linear-gradient(to bottom, rgba(0,0,0,.35), rgba(0,0,0,.55));
    pointer-events:none;
  }}

  /* Top nav */
  .nav {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    z-index: 5;
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding: var(--pad-y) var(--pad-x);
  }}

  .brand {{
    display:flex;
    align-items:center;
    gap: 12px;
    color: var(--fg);
    font-weight: 700;
    letter-spacing: .3px;
    font-size: 16px;
  }}

  .brand img {{
    width: 34px;
    height: 34px;
    border-radius: 10px;
    object-fit: cover;
    box-shadow: 0 10px 28px rgba(0,0,0,.35);
  }}

  .menu {{
    display:flex;
    align-items:center;
    gap: 10px;
  }}

  .menu a {{
    text-decoration:none;
    color: var(--fg2);
    font-size: 13px;
    padding: 9px 12px;
    border-radius: 999px;
    border: 1px solid transparent;
    transition: .18s ease;
    background: transparent;
  }}
  .menu a:hover {{
    color: var(--fg);
    border-color: var(--line);
    background: rgba(0,0,0,.22);
    backdrop-filter: blur(8px);
  }}

  /* Center hero */
  .hero {{
    position:absolute;
    inset:0;
    z-index: 6;
    display:grid;
    place-items:center;
    padding: 0 18px;
    text-align:center;
  }}

  .title {{
    color: var(--fg);
    margin: 0;
    font-weight: 700;
    letter-spacing: -0.02em;
    font-size: clamp(34px, 5.2vw, 72px);
    line-height: 1.02;
    text-shadow: 0 20px 50px rgba(0,0,0,.55);
  }}

  .subtitle {{
    margin: 14px auto 0;
    color: var(--fg2);
    max-width: 860px;
    font-size: clamp(14px, 1.55vw, 18px);
    line-height: 1.45;
  }}

  .cta {{
    margin-top: 22px;
    display:flex;
    gap: 10px;
    justify-content:center;
    flex-wrap: wrap;
  }}

  .pill {{
    display:inline-flex;
    align-items:center;
    gap: 10px;
    text-decoration:none;
    color: var(--fg);
    font-size: 13px;
    padding: 10px 14px;
    border-radius: 999px;
    border: 1px solid var(--line);
    background: rgba(0,0,0,.26);
    backdrop-filter: blur(10px);
    transition: .18s ease;
  }}
  .pill:hover {{
    transform: translateY(-1px);
    background: rgba(0,0,0,.36);
  }}

  /* Small hint bottom */
  .foot {{
    position:absolute;
    left: 0;
    right:0;
    bottom: 0;
    z-index: 7;
    padding: 18px var(--pad-x);
    color: rgba(255,255,255,.55);
    font-size: 12px;
    display:flex;
    justify-content:space-between;
    gap: 12px;
  }}

  /* Mobile tweaks */
  @media (max-width: 640px) {{
    :root {{ --pad-x: 18px; --pad-y: 16px; }}
    .menu a {{ padding: 8px 10px; }}
    .foot {{ flex-direction: column; align-items: flex-start; }}
  }}
</style>
</head>

<body>
  <div class="stage">
    <video class="bgvideo" autoplay muted loop playsinline>
      <source src="data:video/mp4;base64,{video_b64}" type="video/mp4" />
    </video>

    <canvas id="react"></canvas>
    <div class="vignette"></div>

    <div class="nav">
      <div class="brand">
        {brand_img}
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
      <div>
        <h1 class="title">Welcome to my lab</h1>
        <p class="subtitle">
          Data Science • Engineering • Automation — proyectos con código, métricas y ejecución real.
        </p>

        <div class="cta">
          <a class="pill" href="./Projects" target="_self">Explorar Projects →</a>
          <a class="pill" href="./Lab" target="_self">Entrar al Lab →</a>
        </div>
      </div>
    </div>

    <div class="foot">
      <div>Move your cursor — reactive field</div>
      <div>© JorgeRR89</div>
    </div>
  </div>

<script>
(() => {{
  const canvas = document.getElementById('react');
  const ctx = canvas.getContext('2d', {{ alpha: true }});

  let w = 0, h = 0, dpr = Math.max(1, window.devicePixelRatio || 1);

  function resize() {{
    w = Math.floor(window.innerWidth);
    h = Math.floor(window.innerHeight);
    dpr = Math.max(1, window.devicePixelRatio || 1);
    canvas.width = Math.floor(w * dpr);
    canvas.height = Math.floor(h * dpr);
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }}
  window.addEventListener('resize', resize);
  resize();

  // Pointer
  const pointer = {{
    x: w*0.5, y: h*0.45,
    vx: 0, vy: 0,
    active: false
  }};

  function onMove(e) {{
    const x = (e.touches ? e.touches[0].clientX : e.clientX);
    const y = (e.touches ? e.touches[0].clientY : e.clientY);
    pointer.vx = x - pointer.x;
    pointer.vy = y - pointer.y;
    pointer.x = x;
    pointer.y = y;
    pointer.active = true;
  }}
  window.addEventListener('mousemove', onMove, {{ passive:true }});
  window.addEventListener('touchmove', onMove, {{ passive:true }});
  window.addEventListener('touchstart', onMove, {{ passive:true }});

  // Particles — “antigravity-ish” reactive field
  const N = Math.min(140, Math.floor((w*h) / 12000)); // auto-scale
  const particles = [];
  const rand = (a,b)=> a + Math.random()*(b-a);

  function init() {{
    particles.length = 0;
    for (let i=0;i<N;i++) {{
      particles.push({{
        x: rand(0,w), y: rand(0,h),
        vx: rand(-0.25,0.25), vy: rand(-0.25,0.25),
        r: rand(0.9, 2.2),
        a: rand(0.15, 0.55),
        phase: rand(0, Math.PI*2)
      }});
    }}
  }}
  init();

  // Draw helpers
  function drawLine(x1,y1,x2,y2,alpha) {{
    ctx.globalAlpha = alpha;
    ctx.beginPath();
    ctx.moveTo(x1,y1);
    ctx.lineTo(x2,y2);
    ctx.stroke();
  }}

  let t = 0;
  function frame() {{
    t += 0.016;

    // Clear with subtle trail
    ctx.globalCompositeOperation = 'source-over';
    ctx.fillStyle = 'rgba(0,0,0,0.10)';
    ctx.fillRect(0,0,w,h);

    // Styling: white glow-ish
    ctx.lineWidth = 1;
    ctx.strokeStyle = 'rgba(255,255,255,0.25)';
    ctx.fillStyle = 'rgba(255,255,255,0.85)';
    ctx.globalCompositeOperation = 'lighter';

    // Gentle drift + pointer force
    const px = pointer.x, py = pointer.y;
    const forceRadius = Math.max(140, Math.min(260, Math.sqrt(w*w+h*h)*0.14));

    for (const p of particles) {{
      // background flow
      p.vx += Math.cos(t + p.phase) * 0.002;
      p.vy += Math.sin(t + p.phase) * 0.002;

      // pointer interaction (repel + swirl)
      const dx = p.x - px;
      const dy = p.y - py;
      const dist = Math.sqrt(dx*dx + dy*dy) + 0.001;

      if (dist < forceRadius) {{
        const k = (1 - dist/forceRadius);
        const repel = 0.045 * k;
        const swirl = 0.018 * k;

        p.vx += (dx/dist) * repel + (-dy/dist) * swirl;
        p.vy += (dy/dist) * repel + ( dx/dist) * swirl;
      }}

      // damping
      p.vx *= 0.985;
      p.vy *= 0.985;

      // integrate
      p.x += p.vx;
      p.y += p.vy;

      // wrap edges
      if (p.x < -20) p.x = w+20;
      if (p.x > w+20) p.x = -20;
      if (p.y < -20) p.y = h+20;
      if (p.y > h+20) p.y = -20;
    }}

    // Connect close particles
    const maxLink = 105;
    for (let i=0;i<particles.length;i++) {{
      const a = particles[i];
      for (let j=i+1;j<particles.length;j++) {{
        const b = particles[j];
        const dx = a.x-b.x, dy=a.y-b.y;
        const d2 = dx*dx + dy*dy;
        if (d2 < maxLink*maxLink) {{
          const d = Math.sqrt(d2);
          const alpha = (1 - d/maxLink) * 0.22;
          drawLine(a.x,a.y,b.x,b.y,alpha);
        }}
      }}
    }}

    // Draw particles
    for (const p of particles) {{
      ctx.globalAlpha = p.a;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI*2);
      ctx.fill();
    }}

    requestAnimationFrame(frame);
  }}
  frame();

}})();
</script>
</body>
</html>
"""

st.components.v1.html(html, height=900, scrolling=False)
