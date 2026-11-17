import re

def parse_research_intent(question: str) -> dict:
    q=question.lower()
    accessions={"bass-ii":"PSI-25","bass ii":"PSI-25","psi-25":"PSI-25","flex":"PSI-69","psi-69":"PSI-69","spice":"PSI-107","psi-107":"PSI-107"}
    accession=next((v for k,v in accessions.items() if k in q),None)
    materials=[m for m in ["pmma","methanol","methane","ethylene","propylene","propane","heptane","nomex"] if m in q]
    oxygen=re.search(r"(?:oxygen|o2)\s*(?:of|at|=|:)?\s*(\d+(?:\.\d+)?)\s*%?",q)
    return {"accession":accession,"materials":materials,"oxygen_percent":float(oxygen.group(1)) if oxygen else None}
