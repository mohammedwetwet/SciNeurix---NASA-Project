from pathlib import Path
import streamlit as st
from src.data import load_bundle
from app_pages import overview, knowledge_graph, discovery, research_assistant, insight_lab

ROOT = Path(__file__).parent
st.set_page_config(page_title="SciNeurix | NASA Combustion Research", page_icon="✦", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root{--ink:#eaf2fb;--muted:#9bb0c5;--bg:#071321;--panel:#0d2032;--line:rgba(151,183,211,.17);--cyan:#53d5d1;--orange:#ffb36b}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.stApp{background:radial-gradient(ellipse at 80% -10%,rgba(32,107,133,.22),transparent 38%),#071321;color:var(--ink)}
.block-container{padding-top:1.5rem;padding-bottom:3.2rem;max-width:1480px}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0b1d2d,#081522);border-right:1px solid var(--line)}
[data-testid="stSidebar"] *{color:#eaf2fb}
[data-testid="stSidebar"] .stCaption{color:#9bb0c5}
h1,h2,h3{font-family:'Space Grotesk',sans-serif;letter-spacing:-.035em}
h1{font-size:2.35rem!important}
h2{font-size:1.55rem!important}
p,.stMarkdown{color:#d7e3ef}
.eyebrow{font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;color:var(--cyan);font-weight:700}
.hero-panel{padding:1.5rem 1.7rem;border:1px solid var(--line);border-radius:22px;background:linear-gradient(120deg,rgba(15,43,62,.96),rgba(11,29,45,.86));margin-bottom:1rem}
.hero-panel h1{margin:.35rem 0 .4rem}
.subtle{color:var(--muted)!important;font-size:.95rem;line-height:1.6}
div[data-testid="stMetric"]{background:linear-gradient(145deg,rgba(23,52,73,.82),rgba(12,31,48,.88));border:1px solid var(--line);padding:15px 17px;border-radius:16px}
div[data-testid="stMetric"] label{color:#a9bed0!important}
div[data-testid="stMetric"] [data-testid="stMetricValue"]{color:#f3f8fc}
.stButton>button,.stLinkButton>a{border-radius:11px!important;font-weight:700!important;border:1px solid rgba(83,213,209,.35)!important}
.stButton>button[kind="primary"]{background:linear-gradient(90deg,#147d87,#23a8a0)!important}
div[data-testid="stVerticalBlockBorderWrapper"]{border-color:var(--line)!important;border-radius:17px!important;background:rgba(13,32,50,.55)}
[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:12px;overflow:hidden}
hr{border-color:var(--line)!important}
.stAlert{border-radius:14px}
[data-testid="stTabs"] button{font-weight:650}
</style>
""", unsafe_allow_html=True)

bundle = load_bundle()
with st.sidebar:
    st.markdown("<div style='font-family:Space Grotesk;font-size:1.55rem;font-weight:700'>✦ SciNeurix</div><div style='color:#8fa9bf;font-size:.8rem'>NASA COMBUSTION RESEARCH INTELLIGENCE</div>",unsafe_allow_html=True)
    st.divider()
    st.markdown("**AI CONNECTION**")
    st.caption("Optional · Key is held in this session only.")
    st.text_input("Google AI API key",type="password",key="user_gemini_key",placeholder="Paste your API key")
    if st.session_state.get("user_gemini_key","").strip():
        st.success("AI connection key added")
    else:
        st.info("Evidence retrieval works without an API key.")
    st.divider()
    st.markdown("**DATA SNAPSHOT**")
    st.metric("Experiment records",f"{len(bundle.experiments):,}")
    st.metric("Evidence records",f"{len(bundle.evidence):,}")
    st.metric("Graph connections",f"{len(bundle.graph_edges):,}")
    st.caption("PSI-25 · PSI-69 · PSI-107")
    st.divider()
    st.caption("A research exploration tool — not a fire prediction system.")

pages = [
    st.Page(overview.render,title="Overview",url_path="overview",icon=":material/dashboard:",default=True),
    st.Page(knowledge_graph.render,title="Knowledge Engine",url_path="knowledge-engine",icon=":material/hub:"),
    st.Page(discovery.render,title="Experiment Discovery",url_path="experiment-discovery",icon=":material/travel_explore:"),
    st.Page(research_assistant.render,title="AI Research Assistant",url_path="research-assistant",icon=":material/psychology:"),
    st.Page(insight_lab.render,title="Insight Lab",url_path="insight-lab",icon=":material/science:"),
]
st.navigation(pages).run()
