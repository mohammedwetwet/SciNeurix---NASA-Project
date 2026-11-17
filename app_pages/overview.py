import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from src.data import load_bundle, family_name

def render():
    b=load_bundle(); d=b.experiments
    st.markdown("<div class='eyebrow'>NASA PSI · RESEARCH WORKSPACE</div>",unsafe_allow_html=True)
    st.markdown("<div class='hero-panel'><h1>Turn combustion data into research direction.</h1><p class='subtle'>SciNeurix connects NASA experiment records, helps researchers discover comparable evidence, and explores new experimental conditions using what has already been observed.</p></div>",unsafe_allow_html=True)
    hero=Path(__file__).resolve().parents[1]/"assets/images/sci_neurix_hero.svg"
    st.image(str(hero),use_container_width=True)
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Experiment records",f"{len(d):,}")
    c2.metric("Knowledge nodes",f"{len(b.graph_nodes):,}")
    c3.metric("Graph relationships",f"{len(b.graph_edges):,}")
    c4.metric("Evidence records",f"{len(b.evidence):,}")
    st.markdown("## Three NASA investigations. Three distinct experiment families.")
    cards=st.columns(3)
    for col,acc in zip(cards,["PSI-25","PSI-69","PSI-107"]):
        info=b.config.get("investigation_families",{}).get(acc,{})
        count=int(d["_source_accession"].astype(str).eq(acc).sum())
        with col:
            with st.container(border=True):
                st.markdown(f"<div class='eyebrow'>{acc}</div><h2>{info.get('name',acc)}</h2><p class='subtle'>{info.get('description','')}</p>",unsafe_allow_html=True)
                st.metric("Indexed records",count)
                st.link_button("Open NASA investigation ↗",b.config.get("source_urls",{}).get(acc,"https://psi.nasa.gov/"),use_container_width=True)
    st.markdown("## From raw records to a research workflow")
    flow=st.columns(4)
    steps=[("01 · CONNECT","Link investigations, materials, conditions and evidence."),("02 · DISCOVER","Filter and inspect experiments inside a single family."),("03 · COMPARE","Review observed measurements and data coverage."),("04 · EXPLORE","Find historical experiments closest to a proposed scenario.")]
    for col,(title,desc) in zip(flow,steps):
        with col:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.write(desc)
    st.markdown("## Dataset coverage")
    counts=d.groupby("_source_accession").size().rename("Records").reset_index()
    counts["Investigation"]=counts["_source_accession"].map(lambda x:family_name(x,b.config))
    fig=px.bar(counts,x="Investigation",y="Records",color="Investigation",text="Records")
    fig.update_layout(showlegend=False,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#dce9f5",margin=dict(l=5,r=5,t=15,b=5),yaxis_title="Number of records")
    st.plotly_chart(fig,use_container_width=True)
    st.warning("Scientific guardrail: BASS-II, FLEX and SPICE use different experimental setups. SciNeurix does not pool them into one dataset or infer causal effects between unrelated measurements.")
