from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

@dataclass
class Bundle:
    experiments: pd.DataFrame
    evidence: list[dict]
    graph_nodes: list[dict]
    graph_edges: list[dict]
    materials: list[dict]
    investigations: pd.DataFrame
    config: dict
    quality: pd.DataFrame
    discovery_eval: pd.DataFrame
    missingness: pd.DataFrame
    unit_audit: pd.DataFrame

@st.cache_data(show_spinner=False)
def load_bundle() -> Bundle:
    required = ["experiments.csv", "evidence.json", "knowledge_graph.json", "app_config.json"]
    missing = [f for f in required if not (DATA_DIR / f).exists()]
    if missing:
        raise FileNotFoundError(f"Missing exported data files in {DATA_DIR}: {', '.join(missing)}")
    experiments = pd.read_csv(DATA_DIR / "experiments.csv", low_memory=False)
    with open(DATA_DIR / "evidence.json", encoding="utf-8") as f: evidence = json.load(f)
    with open(DATA_DIR / "knowledge_graph.json", encoding="utf-8") as f: graph = json.load(f)
    with open(DATA_DIR / "materials.json", encoding="utf-8") as f: materials = json.load(f)
    with open(DATA_DIR / "app_config.json", encoding="utf-8") as f: config = json.load(f)
    with open(DATA_DIR / "investigations.csv", encoding="utf-8") as f: investigations = pd.read_csv(f)
    def optional_csv(name):
        p=DATA_DIR/name
        return pd.read_csv(p) if p.exists() else pd.DataFrame()
    return Bundle(experiments, evidence, graph.get("nodes", []), graph.get("edges", []), materials,
                  investigations, config, optional_csv("quality_checks.csv"), optional_csv("discovery_evaluation.csv"),
                  optional_csv("missingness_audit.csv"), optional_csv("unit_audit.csv"))

def family_name(accession: str, config: dict) -> str:
    return config.get("investigation_families", {}).get(str(accession), {}).get("name", str(accession))

def source_url(accession: str, config: dict) -> str:
    return config.get("source_urls", {}).get(str(accession), "https://psi.nasa.gov/")

def safe_numeric(df: pd.DataFrame, col: str) -> pd.Series:
    if col not in df: return pd.Series(index=df.index, dtype="float64")
    return pd.to_numeric(df[col], errors="coerce")
