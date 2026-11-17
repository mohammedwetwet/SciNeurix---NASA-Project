import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from src.data import load_bundle, safe_numeric, family_name, source_url

def render():
    b=load_bundle(); d=b.experiments.copy()
    st.markdown("<div class='eyebrow'>WORKFLOW 02 · FIND RELEVANT RECORDS</div>",unsafe_allow_html=True)
    st.title("Intelligent Experiment Discovery")
    st.markdown("<p class='subtle'>Move from a broad NASA collection to a focused set of experiments. Filter by investigation, fuel and available operating conditions, then inspect the actual measurements and source provenance.</p>",unsafe_allow_html=True)
    st.image(str(Path(__file__).resolve().parents[1]/"assets/images/experiment_discovery.svg"),use_container_width=True)
    accessions=sorted(d["_source_accession"].dropna().astype(str).unique())
    acc=st.selectbox("1 · Select one investigation family",accessions,format_func=lambda x:f"{family_name(x,b.config)} · {x}")
    subset=d[d["_source_accession"].astype(str).eq(acc)].copy()
    material_col="std_fuel_material_clean"
    materials=sorted(subset[material_col].dropna().astype(str).unique())
    material=st.selectbox("2 · Fuel / material",["All available materials"]+materials)
    if material!="All available materials": subset=subset[subset[material_col].astype(str).eq(material)]
    condition_options=[c for c in ["std_oxygen_percent_numeric","std_airflow_numeric","std_droplet_initial_diameter_mm","std_flame_extinction_diameter_mm","std_burning_rate_source_value"] if c in subset and safe_numeric(subset,c).notna().sum()>=5]
    if condition_options:
        label=lambda c:c.replace("std_","").replace("_numeric","").replace("_"," ").replace("mm","(mm)").replace("percent","(%)").title()
        condition=st.selectbox("3 · Operating condition to narrow by",["No additional condition"]+condition_options,format_func=lambda x:"No additional condition" if x=="No additional condition" else label(x))
        if condition!="No additional condition":
            vals=safe_numeric(subset,condition).dropna()
            lo,hi=float(vals.min()),float(vals.max())
            if lo<hi:
                rng=st.slider(f"{label(condition)} range",lo,hi,(lo,hi))
                v=safe_numeric(subset,condition)
                subset=subset[v.between(*rng)|v.isna()]
    c1,c2=st.columns(2)
    c1.metric("Matching records",f"{len(subset):,}")
    c2.metric("Records with material identified",f"{subset[material_col].notna().sum():,}")
    st.caption("Records with missing values are retained where relevant and remain visibly missing; they are never silently converted to zero.")
    display_cols=[c for c in ["_experiment_key","_source_accession","std_fuel_material","std_oxygen_percent_numeric","std_airflow_numeric","std_droplet_initial_diameter_mm","std_flame_extinction_diameter_mm","std_burning_rate_source_value","std_initial_co_numeric","std_final_co_numeric","std_initial_co2_numeric","std_final_co2_numeric","std_burn_time_numeric","_source_filename","_source_row_number"] if c in subset]
    st.markdown("### Retrieved experiment records")
    st.dataframe(subset[display_cols].head(250),use_container_width=True,hide_index=True)
    measurements=[c for c in ["std_initial_co_numeric","std_final_co_numeric","std_initial_co2_numeric","std_final_co2_numeric","std_airflow_numeric","std_burn_time_numeric","std_droplet_initial_diameter_mm","std_flame_extinction_diameter_mm","std_burning_rate_source_value"] if c in subset and safe_numeric(subset,c).notna().sum()>=3]
    if measurements:
        st.markdown("### Explore an observed measurement")
        measure=st.selectbox("Measurement",measurements,format_func=lambda x:x.replace("std_","").replace("_numeric","").replace("_"," ").title())
        plot=subset.copy(); plot["_value"]=safe_numeric(plot,measure)
        plot=plot.dropna(subset=["_value"])
        if not plot.empty:
            fig=px.histogram(plot,x="_value",nbins=25,labels={"_value":measure.replace("std_","").replace("_numeric","").replace("_"," ").title()})
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#dce9f5")
            st.plotly_chart(fig,use_container_width=True)
            st.caption(f"Distribution of {len(plot)} non-missing observations in the filtered records. This is descriptive, not a causal relationship.")
    st.link_button(f"Open official NASA {acc} investigation ↗",source_url(acc,b.config))
    st.info("Good comparison practice: compare records from the same investigation family and check whether fuel, geometry, airflow, apparatus and measurement definitions are compatible.")
