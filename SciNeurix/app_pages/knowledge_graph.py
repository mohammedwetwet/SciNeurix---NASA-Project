import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
from src.data import load_bundle

def render():
    b=load_bundle(); nodes=b.graph_nodes; edges=b.graph_edges
    st.markdown("<div class='eyebrow'>WORKFLOW 01 · CONNECT THE EVIDENCE</div>",unsafe_allow_html=True)
    st.title("Combustion Knowledge Engine")
    st.markdown("<p class='subtle'>The knowledge graph organizes NASA investigation records and their relationships. It gives researchers a way to move from an investigation to the records and concepts connected to it, while keeping source provenance visible.</p>",unsafe_allow_html=True)
    a,bm,c=st.columns(3); a.metric("Knowledge nodes",f"{len(nodes):,}"); bm.metric("Relationships",f"{len(edges):,}"); c.metric("Node categories",len({n.get("node_type","unknown") for n in nodes}))
    types=sorted({n.get("node_type","unknown") for n in nodes})
    chosen=st.multiselect("Node categories",types,default=[x for x in types if x in {"investigation","fuel_material","operating_condition"}])
    accessions=sorted({str(n.get("accession")) for n in nodes if n.get("accession")})
    acc=st.selectbox("Investigation scope",["All"]+accessions)
    filtered=[n for n in nodes if n.get("node_type") in chosen and (acc=="All" or str(n.get("accession"))==acc)]
    filtered_ids={n.get("id") for n in filtered}
    related=[e for e in edges if e.get("source") in filtered_ids or e.get("target") in filtered_ids]
    st.markdown("### Relationship map")
    if filtered and related:
        # Build a bounded, readable sample of the exported graph.
        sample_edges=related[:100]
        graph=nx.Graph()
        for e in sample_edges:
            graph.add_edge(e.get("source"),e.get("target"),relation=e.get("relation","related_to"))
        positions=nx.spring_layout(graph,seed=17,k=0.7,iterations=35)
        node_lookup={n.get("id"):n for n in nodes}
        edge_x=[]; edge_y=[]
        for u,v in graph.edges():
            x0,y0=positions[u]; x1,y1=positions[v]
            edge_x += [x0,x1,None]; edge_y += [y0,y1,None]
        edge_trace=go.Scatter(x=edge_x,y=edge_y,mode="lines",line=dict(width=1,color="rgba(100,180,200,.32)"),hoverinfo="none")
        xs=[]; ys=[]; labels=[]; hovers=[]; colors=[]
        for node in graph.nodes():
            x,y=positions[node]; item=node_lookup.get(node,{})
            xs.append(x); ys.append(y)
            labels.append(str(item.get("name") or item.get("title") or item.get("node_type","node"))[:22])
            hovers.append(f"{item.get('node_type','node')}<br>{item.get('name') or item.get('title') or node}<br>{item.get('accession','')}")
            colors.append("#ffb36b" if item.get("node_type")=="investigation" else "#53d5d1" if item.get("node_type")=="fuel_material" else "#7395bd")
        node_trace=go.Scatter(x=xs,y=ys,mode="markers+text",text=labels,textposition="top center",hovertext=hovers,hoverinfo="text",marker=dict(size=15,color=colors,line=dict(width=1,color="#d8edf5")))
        fig=go.Figure([edge_trace,node_trace])
        fig.update_layout(height=520,showlegend=False,margin=dict(l=5,r=5,t=5,b=5),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#dce9f5",xaxis=dict(visible=False),yaxis=dict(visible=False))
        st.plotly_chart(fig,use_container_width=True)
        st.caption(f"Visual sample: {len(graph.nodes):,} nodes and {len(graph.edges):,} relationships from the exported graph. The complete graph remains available in the data files.")
    else:
        st.info("No graph relationships match these filters. Try a broader node category or investigation scope.")
    st.markdown("### Inspect graph records")
    if filtered:
        frame=pd.DataFrame([{k:n.get(k) for k in ("id","node_type","name","title","accession","parameter","value","experiment_key","url")} for n in filtered])
        st.dataframe(frame.head(500),use_container_width=True,hide_index=True)
    st.markdown("### Inspect exported relationships")
    if related:
        lookup={n.get("id"):str(n.get("name") or n.get("title") or n.get("id")) for n in nodes}
        rel=pd.DataFrame([{"From":lookup.get(e.get("source"),e.get("source")),"Relationship":e.get("relation","related_to"),"To":lookup.get(e.get("target"),e.get("target"))} for e in related[:500]])
        st.dataframe(rel,use_container_width=True,hide_index=True)
    st.warning("Graph edges describe exported data relationships. They are not proof of physical causation or experimentally validated mechanisms.")
