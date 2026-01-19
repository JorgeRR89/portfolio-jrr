import streamlit as st

st.set_page_config(
    page_title="Portfolio JRR",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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
    --fg: rgba(255,255,255,.92);
    --fg2: rgba(255,255,255,.78);
    --line: rgba(255,255,255,.12);
  }
  html, body{margin:0; padding:0; height:100%; background:#000;
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;}
  .stage{position:relative; width:100vw; height:100vh; overflow:hidden; background:#000;}
  #react{position:absolute; inset:0; width:100%; height:100%; z-index:2; mix-blend-mode:screen; opacity:.95;}
  .vignette{
    position:absolute; inset:0; z-index:3; pointer-events:none;
    background:
      radial-gradient(1100px 650px at 50% 45%, rgba(0,0,0,0) 0%, rgba(0,0,0,.52) 72%, rgba(0,0,0,.78) 100%),
      linear-gradient(to bottom, rgba(0,0,0,.45), rgba(0,0,0,.72));
  }
  .nav{
    position:absolute; top:0; left:0; right:0; z-index:5;
    display:flex; align-items:center; justify-content:space-between;
    padding: var(--pad-y) var(--pad-x);
  }
  .brand{display:flex; align-items:center; gap:12px; color:var(--fg);
    font-weight:700; letter-spacing:.3px; font-size:16px;}
  .menu{display:flex; align-items:center; gap:10px;}
  .menu a{
    text-decoration:none; color:var(--fg2); font-size:13px;
    padding:9px 12px; border-radius:999px; border:1px solid transparent;
    transition:.18s ease; background:transparent;
  }
  .menu a:hover{color:var(--fg); border-color:var(--line); background:rgba(255,255,255,.04);}
  .hero{
    position:absolute; inset:0; z-index:6;
    display:grid; place-items:center; padding:0 18px; text-align:center;
  }
  .title{
    color:var(--fg); margin:0; font-weight:700; letter-spacing:-0.02em;
    font-size:clamp(34px, 5.2vw, 72px); line-height:1.02;
    text-shadow:0 20px 50px rgba(0,0,0,.55);
  }
  .subtitle{
    margin:14px auto 0; color:var(--fg2); max-width:860px;
    font-size:clamp(14px, 1.55vw, 18px); line-height:1.45;
  }
  .cta{margin-top:22px; display:flex; gap:10px; justify-content:center; flex-wrap:wrap;}
  .pill{
    display:inline-flex; align-items:center; text-decoration:none; color:var(--fg);
    font-size:13px; padding:10px 14px; border-radius:999px;
    border:1px solid var(--line); background:rgba(255,255,255,.04);
    transition:.18s ease;
  }
  .pill:hover{transform:translateY(-1px); background:rgba(255,255,255,.07);}
  .foot{
    position:absolute; left:0; right:0; bottom:0; z-index:7;
    padding:18px var(--pad-x); color:rgba(255,255,255,.55);
    font-size:12px; display:flex; justify-content:space-between; gap:12px;
  }
  @media (max-width:640px){
    :root{--pad-x:18px; --pad-y:16px;}
    .menu a{padding:8px 10px;}
    .foot{flex-direction:column; align-items:flex-start;}
  }
</style>
</head>

<body>
  <div class="stage">
    <canvas id="react"></canvas>
    <div class="vignette"></div>

    <div class="nav">
      <div class="brand">Portfolio JRR</div>
      <div class="menu">
        <a href="./About_Me" target="_self">About</a>
        <a href="./Projects" target="_self">Projects</a>
        <a href="./Lab" target="_self">Lab</a>
        <a href="./Contact" target="_self">Contact</a>
      </div>
    </div>

    <div class="hero">
      <d
