import streamlit as st
from src.data import load_bundle
from src.agents.llm import answer_question

def render():
    b = load_bundle()
    st.title("Evidence-Based AI Research Assistant")
    st.caption("Ask a scientific question. SciNeurix retrieves source evidence first, then optionally uses your API key to draft a grounded answer.")
    st.markdown("Use a focused question about an investigation, fuel, operating condition, or measured variable.")
    with st.form("research_form"):
        question = st.text_area("Research question", placeholder="What do BASS-II experiments report about oxygen concentration and combustion behavior?", height=120)
        top_k = st.slider("Evidence sources", 3, 10, 6)
        submitted = st.form_submit_button("Search evidence and answer", type="primary", use_container_width=True)
    if submitted:
        if not question.strip():
            st.warning("Enter a research question first.")
        else:
            with st.spinner("Retrieving NASA evidence..."):
                result = answer_question(question, b.evidence, top_k, api_key=st.session_state.get("user_gemini_key", ""))
            st.session_state["research_result"] = result
    result = st.session_state.get("research_result")
    if result:
        st.divider()
        mode = result.get("mode", "Evidence-only fallback")
        if mode.startswith("AI-generated"):
            st.success(f"AI-assisted answer · {result.get('model')}")
        else:
            st.info("Evidence-only mode · No generated model answer was used")
        st.markdown(result["answer"])
        if result.get("errors"):
            with st.expander("Connection details"):
                st.write("\n".join(result["errors"]))
        st.subheader("Sources used")
        citations = result.get("citations", [])
        if citations:
            for c in citations:
                label = f"{c.get('title') or 'NASA source'} · {c.get('accession') or 'NASA'} · {c.get('evidence_id') or ''}"
                if c.get("url"):
                    st.markdown(f"- [{label}]({c['url']})")
                else:
                    st.write(f"- {label}")
        else:
            st.warning("No directly relevant evidence was retrieved.")
        with st.expander("Inspect retrieved evidence"):
            for r in result.get("hits", []):
                st.markdown(f"**{r.get('evidence_id')} — {r.get('title')}**")
                st.write(r.get("text", ""))
                if r.get("url"):
                    st.link_button("Open NASA source", r["url"])
    st.caption("Scientific safeguard: retrieved records are not proof of causation. Unsupported values and conclusions are not inferred.")
