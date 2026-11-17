import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
from src.data import load_bundle, safe_numeric, family_name, source_url

CONDITION_LABELS={
 "std_oxygen_percent_numeric":"Oxygen concentration (%)",
 "std_airflow_numeric":"Airflow / flow rate (source-normalized field)",
 "std_droplet_initial_diameter_mm":"Initial droplet diameter (mm)",
 "std_flame_extinction_diameter_mm":"Flame extinction diameter (mm)",
 "std_burning_rate_source_value":"Burning-rate source value",
 "Fuel Rate (mg/s)":"Fuel rate (mg/s)",
 "Air Rate (cm/s)":"Air rate (cm/s)",
 "Nozzle (mm)":"Nozzle diameter (mm)",
 "Droplet initial diameter; mm":"Initial droplet diameter (mm)",
 "Burn time; s":"Burn time (s)",
 "Visible flame extinction diameter; mm":"Visible flame extinction diameter (mm)",
 "Burning rate; mm":"Burning rate (mm)",
 "Calibrated  initial O2 % by vol ":"Initial oxygen concentration (%)",
 "Fan display":"Fan display (source value)",
 "Air display":"Air display (source value)"
}
OUTCOME_LABELS={
 "std_initial_co_numeric":"Initial CO",
 "std_final_co_numeric":"Final CO",
 "std_initial_co2_numeric":"Initial CO₂",
 "std_final_co2_numeric":"Final CO₂",
 "std_burn_time_numeric":"Burn time",
 "std_droplet_initial_diameter_mm":"Initial droplet diameter",
 "std_flame_extinction_diameter_mm":"Flame extinction diameter",
 "std_burning_rate_source_value":"Burning-rate source value",
 "Burn time; s":"Burn time (s)",
 "Visible flame extinction diameter; mm":"Flame extinction diameter (mm)",
 "Burning rate; mm":"Burning rate (mm)",
 "Fuel Rate (mg/s)":"Fuel rate (mg/s)",
 "Air Rate (cm/s)":"Air rate (cm/s)"
}

def label(c):
    return CONDITION_LABELS.get(c,OUTCOME_LABELS.get(c,c.replace("std_","").replace("_numeric","").replace("_"," ").strip().title()))

def render():
    b=load_bundle(); data=b.experiments.copy()
    st.markdown("<div class='eyebrow'>WORKFLOW 04 · EXPLORE HISTORICAL EVIDENCE</div>",unsafe_allow_html=True)
    st.title("Fire-Safety Insight Lab")
    st.markdown("<p class='subtle'>A researcher can describe a proposed experimental scenario, then find the closest historical NASA experiments and inspect what was actually measured. This helps assess whether existing evidence is relevant, what it can tell us, and where new experiments may be needed.</p>",unsafe_allow_html=True)
    st.image(str(Path(__file__).resolve().parents[1]/"assets/images/scenario_lab.svg"),use_container_width=True)
    st.markdown("<div class='hero-panel'><h2>From a research question to evidence-backed scenario exploration</h2><p class='subtle'>Define conditions → retrieve the nearest observed experiments → compare measured outcomes → identify evidence gaps before planning a new test.</p></div>",unsafe_allow_html=True)
    st.markdown("### 1 · Choose the experiment family")
    accessions=sorted(data["_source_accession"].dropna().astype(str).unique())
    acc=st.selectbox("NASA investigation",accessions,format_func=lambda x:f"{family_name(x,b.config)} · {x}",key="insight_acc")
    family=data[data["_source_accession"].astype(str).eq(acc)].copy()
    st.caption(b.config.get("investigation_families",{}).get(acc,{}).get("description",""))
    material_col="std_fuel_material_clean"
    materials=sorted(family[material_col].dropna().astype(str).unique()) if material_col in family else []
    fuel=st.selectbox("Fuel / material",["All available materials"]+materials,key="insight_fuel")
    if fuel!="All available materials" and material_col in family:
        family=family[family[material_col].astype(str).eq(fuel)]
    st.markdown("### 2 · Describe your proposed scenario")
    st.caption("Choose up to two conditions that exist in this investigation's records. The app searches observed experiments near your targets; it does not generate a synthetic experiment.")
    candidates=[]
    preferred=["std_oxygen_percent_numeric","std_airflow_numeric","std_droplet_initial_diameter_mm","std_flame_extinction_diameter_mm","std_burning_rate_source_value","Fuel Rate (mg/s)","Air Rate (cm/s)","Nozzle (mm)","Droplet initial diameter; mm","Visible flame extinction diameter; mm","Burning rate; mm","Burn time; s","Calibrated  initial O2 % by vol ","Fan display","Air display"]
    for c in preferred:
        if c in family.columns:
            vals=safe_numeric(family,c).dropna()
            if len(vals)>=5 and vals.nunique()>1:
                candidates.append(c)
    if not candidates:
        st.error("This investigation does not contain enough populated numeric operating-condition fields for scenario matching.")
        return
    c1,c2=st.columns(2)
    with c1:
        cond1=st.selectbox("Condition A",candidates,format_func=label,key="insight_cond1")
    remaining=[x for x in candidates if x!=cond1]
    with c2:
        cond2=st.selectbox("Condition B (optional)",["None"]+remaining,format_func=lambda x:"No second condition" if x=="None" else label(x),key="insight_cond2")
    conditions=[cond1]+([cond2] if cond2!="None" else [])
    target_values={}; tolerances={}
    for idx,col in enumerate(conditions):
        vals=safe_numeric(family,col).dropna()
        lo,hi=float(vals.min()),float(vals.max())
        median=float(vals.median())
        a,bcol=st.columns([1.2,1])
        with a:
            target_values[col]=st.number_input(f"Target · {label(col)}",min_value=lo,max_value=hi,value=median,step=max((hi-lo)/100,0.01),key=f"target_{col}")
        with bcol:
            default_tol=max((hi-lo)*0.08,0.01)
            tolerances[col]=st.number_input(f"Allowed difference",min_value=0.0,max_value=max(hi-lo,0.01),value=min(default_tol,max(hi-lo,0.01)),step=max((hi-lo)/100,0.01),key=f"tol_{col}")
    st.markdown("### 3 · Retrieve comparable historical experiments")
    result=family.copy()
    result["_scenario_distance"]=0.0
    for col in conditions:
        values=safe_numeric(result,col)
        gap=(values-target_values[col]).abs()
        scale=max(tolerances[col],(safe_numeric(family,col).max()-safe_numeric(family,col).min())*0.01,1e-9)
        result["_scenario_distance"]+=gap.fillna(np.inf)/scale
        result[f"gap_{col}"]=gap
    matched=result.copy()
    for col in conditions:
        matched=matched[matched[f"gap_{col}"].le(tolerances[col])]
    matched=matched.sort_values("_scenario_distance")
    nearest=result.replace([np.inf,-np.inf],np.nan).dropna(subset=["_scenario_distance"]).sort_values("_scenario_distance").head(10)
    k1,k2,k3=st.columns(3)
    k1.metric("Records in selected family",f"{len(family):,}")
    k2.metric("Within your tolerances",f"{len(matched):,}")
    k3.metric("Closest records shown",f"{min(len(nearest),10):,}")
    st.caption("A record is considered a match only when every selected condition falls inside its stated tolerance. Missing condition values cannot count as a match.")
    with st.expander("See how matching works"):
        st.write("For each selected condition, SciNeurix calculates the absolute difference between the target and the recorded value. A record is included in the matched set only if all differences are within the tolerances you selected. The nearest-record ranking is a retrieval aid, not a physical similarity model.")
    st.image(str(Path(__file__).resolve().parents[1]/"assets/images/evidence_compare.svg"),use_container_width=True)
    st.markdown("### 4 · Compare observed measurements")
    outcomes=[c for c in ["std_initial_co_numeric","std_final_co_numeric","std_initial_co2_numeric","std_final_co2_numeric","std_burn_time_numeric","std_droplet_initial_diameter_mm","std_flame_extinction_diameter_mm","std_burning_rate_source_value","Burn time; s","Visible flame extinction diameter; mm","Burning rate; mm","Fuel Rate (mg/s)","Air Rate (cm/s)"] if c in family and safe_numeric(family,c).notna().sum()>=5 and c not in conditions]
    if outcomes:
        outcome=st.selectbox("Measured outcome to inspect",outcomes,format_func=label,key="insight_outcome")
        observed=safe_numeric(family,outcome)
        matched_values=safe_numeric(matched,outcome).dropna()
        all_values=observed.dropna()
        coverage=100*observed.notna().mean() if len(observed) else 0
        a,bcol,c=st.columns(3)
        a.metric("Outcome data coverage",f"{coverage:.1f}%")
        bcol.metric("Matched observations",f"{len(matched_values):,}")
        c.metric("Family median (observed)",f"{all_values.median():.4g}" if len(all_values) else "N/A")
        if len(matched_values):
            comparison=pd.DataFrame([
                {"Evidence group":"Matched historical records","Count":len(matched_values),"Mean":matched_values.mean(),"Median":matched_values.median(),"Min":matched_values.min(),"Max":matched_values.max()},
                {"Evidence group":"All records in this family","Count":len(all_values),"Mean":all_values.mean(),"Median":all_values.median(),"Min":all_values.min(),"Max":all_values.max()}
            ])
            st.dataframe(comparison.round(4),use_container_width=True,hide_index=True)
            plot=pd.DataFrame({"Measured value":pd.concat([matched_values.rename("Matched historical records"),all_values.rename("All family records")]),"Evidence group":["Matched historical records"]*len(matched_values)+["All family records"]*len(all_values)})
            fig=px.box(plot,x="Evidence group",y="Measured value",color="Evidence group",points="all",title=f"Observed {label(outcome)} · matched records vs full investigation")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#dce9f5",showlegend=False)
            st.plotly_chart(fig,use_container_width=True)
            st.caption("This comparison is descriptive. The full-family group includes the matched records, so it is a context reference, not an independent control group.")
        else:
            st.warning("No outcome values are available among records matching all selected conditions. This is a useful evidence-coverage gap; try reviewing the nearest records or changing the tolerances.")
    else:
        st.info("No sufficiently populated outcome field is available for this selected family and filter combination.")
    st.markdown("### 5 · Inspect the evidence behind the scenario")
    if len(matched):
        cols=[c for c in ["_experiment_key","std_fuel_material","_source_accession"]+conditions+["std_initial_co_numeric","std_final_co_numeric","std_burn_time_numeric","std_droplet_initial_diameter_mm","std_flame_extinction_diameter_mm","std_burning_rate_source_value","_source_filename","_source_row_number"] if c in matched.columns]
        st.dataframe(matched[cols].head(100),use_container_width=True,hide_index=True)
    else:
        st.warning("No experiment meets every target tolerance. The closest observed records are shown below so you can inspect how far the archive is from your proposed conditions.")
        if len(nearest):
            cols=[c for c in ["_experiment_key","std_fuel_material","_source_accession"]+conditions+["_scenario_distance","_source_filename","_source_row_number"] if c in nearest.columns]
            st.dataframe(nearest[cols],use_container_width=True,hide_index=True)
    st.link_button(f"Open official NASA {acc} investigation ↗",source_url(acc,b.config))
    st.markdown("### What this can tell a researcher")
    st.markdown("""
- **Evidence availability:** Are there historical tests close to the proposed conditions?
- **Observed outcomes:** What values were actually recorded in those nearby tests?
- **Research planning:** Which combinations of conditions have little or no coverage and may deserve further investigation?
- **Traceability:** Which NASA investigation and source rows support the comparison?
""")
    st.error("Scientific boundary: this is evidence-based scenario retrieval, not a validated combustion simulator, causal analysis, or prediction model. Nearby records may still differ in apparatus, geometry, fuel preparation, measurement methods and other uncontrolled conditions. A new scenario's outcome cannot be inferred from these comparisons.")
