import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from .retrieval import retrieve_evidence, deterministic_answer
from .query_planning import parse_research_intent

MODEL_ORDER = ["gemma-4-26b-a4b-it", "gemini-2.5-flash-lite", "gemini-2.5-flash"]

def _api_key():
    try:
        return st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
    except Exception:
        return os.getenv("GEMINI_API_KEY", "")

def answer_question(question, evidence, top_k=6, api_key=None):
    intent = parse_research_intent(question)
    hits = retrieve_evidence(evidence, question, top_k=top_k, accession=intent.get('accession'))
    citations = [{"evidence_id":r.get("evidence_id"),"title":r.get("title"),"url":r.get("url"),"accession":r.get("accession")} for r in hits]
    key = (api_key or _api_key() or '').strip()
    if not hits:
        return {"answer": deterministic_answer(question, hits), "mode": "Evidence-only fallback", "model": None, "citations": [], "hits": [], "errors": ["No directly relevant source evidence was retrieved; generation was skipped."]}
    if key:
        try:
            from google import genai
            from google.genai import types
            client=genai.Client(api_key=key)
            packet="\n\n".join(f"[{r.get('evidence_id')}] {r.get('title')} | {r.get('url')}\n{r.get('text')}" for r in hits)
            prompt=f"""You are SciNeurix, a cautious scientific research assistant. Use only the evidence below. Never invent measurements, sources, or conclusions. Distinguish reported observations from interpretation. State missing evidence and limitations. Do not pool different investigation families.\n\nReturn: Scientific answer; Experimental evidence; Measured values (only if explicitly present); Limitations.\n\nQuestion: {question}\n\nEvidence:\n{packet}"""
            errors=[]
            for model in MODEL_ORDER:
                try:
                    response=client.models.generate_content(model=model, contents=prompt,
                        config=types.GenerateContentConfig(temperature=0.1, max_output_tokens=900))
                    if response.text:
                        return {"answer":response.text,"mode":"AI-generated with retrieved evidence","model":model,"citations":citations,"hits":hits}
                except Exception as exc:
                    errors.append(f"{model}: {str(exc)[:180]}")
        except Exception as exc:
            errors=[str(exc)[:250]]
    else:
        errors=["GEMINI_API_KEY is not configured."]
    return {"answer":deterministic_answer(question,hits),"mode":"Evidence-only fallback","model":None,"citations":citations,"hits":hits,"errors":errors}
