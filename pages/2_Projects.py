import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Projects", page_icon="🛰️", layout="wide", initial_sidebar_state="collapsed")

# --- CSS + HTML en un iframe (robusto: no se convierte a "code block") ---
cards = [
    ("Bancos & Seguros", "Riesgo, fraude, scoring, churn, KPIs.", "/2a_Bancos_Seguros", "🏦"),
    ("Energía", "Optimización, confiabilidad, mantenimiento, forecasting.", "/2b_Energia", "⚡"),
    ("Entretenimiento", "Audiencias, recomendación, NLP, visión.", "/3c_Entretenimiento", "🎬"),
    ("Manufactura", "Calidad, visión artificial, gemelos digitales.", "/2d_Manufactura", "🏭"),
    ("Marketing", "Segmentación, atribución, LTV, performance.", "/2e_Marketing", "📈"),
    ("Política", "Opinión pública, escenarios, señales, OSINT.", "/2f_Politica", "🏛️"),
    ("Transporte", "Rutas, demanda, optimización, simulación.", "/2g_Transporte", "🚚"),
    ("Coming soon", "New industries under construction.", "#", "✨"),
]

cards_html = ""
for title, desc, href, icon in cards:
    open_text = "OPEN →" if href != "#" else "COMING SOON"
    # target="_top" hace que navegue en la página principal (no dentro del iframe)
    link = f'<a class="cardlink" href="{href}" target="_top"></a>' if href != "#" else ""
    cards_html += f"""
<div class="industry-card">
  {link}
  <div class="industry-top"></div>
  <div class="industry-icon">{icon}</div>
  <div class="industry-body">
    <div class="industry-title">{title}</div>
    <div class="industry-desc">{desc}</div>
    <div class="industry-open">{open_text}</div>
  </div>
</div>
"""

html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
  body {{
    margin: 0;
    font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial;
    background: transparent;
    color: white;
  }}
  .wrap {{
    max-width: 1300px;
    margin: 0 auto;
    padding: 48px 56px 80px 56px;
  }}
  h1 {{
    margin: 0 0 8px 0;
    font-size: 44px;
    font-weight: 900;
  }}
  .sub {{
    opacity: .7;
    margin: 0 0 28px 0;
    font-size: 14px;
  }}

  .industry-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 22px;
  }}

  .industry-card {{
    position: relative;
    height: 240px;
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.10);
    background: rgba(255,255,255,0.035);
    backdrop-filter: blur(10px);
    overflow: hidden;
    transition: transform .2s ease, border-color .2s ease, background .2s ease;
  }}
  .industry-card:hover {{
    transform: translateY(-6px);
    border-color: rgba(0,180,255,0.45);
    background: rgba(0,180,255,0.08);
  }}

  .industry-top {{
    height: 92px;
    background:
      radial-gradient(circle at 25% 25%, rgba(0,180,255,0.28), rgba(0,0,0,0) 60%),
      radial-gradient(circle at 85% 10%, rgba(0,120,255,0.18), rgba(0,0,0,0) 55%),
      linear-gradient(180deg, rgba(255,255,255,0.05), rgba(0,0,0,0));
    border-bottom: 1px solid rgba(255,255,255,0.08);
  }}

  .industry-icon {{
    position: absolute;
    top: 54px;
    left: 16px;
    width: 46px;
    height: 46px;
    border-radius: 14px;
    background: rgba(0,0,0,0.45);
    border: 1px solid rgba(255,255,255,0.12);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    z-index: 2;
  }}

  .industry-body {{
    padding: 16px;
  }}
  .industry-title {{
    font-size: 18px;
    font-weight: 900;
    margin: 2px 0 10px 0;
  }}
  .industry-desc {{
    font-size: 13px;
    line-height: 1.35;
    opacity: .72;
    margin: 0;
  }}
  .industry-open {{
    position: absolute;
    bottom: 14px;
    right: 16px;
    font-size: 12px;
    opacity: .85;
  }}

  .cardlink {{
    position: absolute;
    inset: 0;
    z-index: 5;
    text-decoration: none;
  }}

  @media (max-width: 1200px) {{
    .industry-grid {{ grid-template-columns: repeat(2, 1fr); }}
  }}
  @media (max-width: 650px) {{
    .wrap {{ padding: 28px 18px 60px 18px; }}
    .industry-grid {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>
  <div class="wrap">
    <h1>Projects</h1>
    <p class="sub">Industries · Applied Data Science · AI Systems</p>
    <div class="industry-grid">
      {cards_html}
    </div>
  </div>
</body>
</html>
"""

# altura suficiente para 2 filas (ajústala si cambias height de cards)
components.html(html, height=720, scrolling=False)
