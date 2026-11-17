import re
from collections import Counter

def tokens(text):
    return re.findall(r"[a-z0-9]+", str(text).lower())

def retrieve_evidence(records, query, top_k=6, accession=None):
    q = Counter(tokens(query))
    scored=[]
    for item in records:
        if accession and item.get("accession") not in (None, accession):
            continue
        body = " ".join([str(item.get(k,"")) for k in ("title","text","category","accession")])
        words=Counter(tokens(body))
        score=sum(min(count, words[t]) for t,count in q.items())
        if score: scored.append((score,item))
    scored.sort(key=lambda x:x[0], reverse=True)
    return [x[1] for x in scored[:top_k]]

def deterministic_answer(question, records):
    if not records:
        return "I could not retrieve directly relevant evidence from the indexed NASA records. Please narrow the question to an investigation, material, or measured variable."
    lines=["The following summary is based only on retrieved source records:", ""]
    for i,r in enumerate(records,1):
        text=str(r.get("text", "")).strip()
        lines.append(f"{i}. **{r.get('title','NASA source')}** — {text[:850]}")
    lines += ["", "**Limitations:** This is a retrieval-based summary, not a new experimental result. It does not establish causation or support values not present in the cited records."]
    return "\n\n".join(lines)
