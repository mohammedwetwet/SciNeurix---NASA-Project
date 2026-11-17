# SciNeurix — NASA Combustion Research Intelligence

SciNeurix is an evidence-first research workspace built on exported NASA Physical Sciences Informatics (PSI) combustion investigation records. It helps a researcher move through a practical workflow: connect records, discover relevant experiments, inspect evidence, and explore how a proposed scenario relates to historical observations.

## What problem does it address?

Combustion research datasets are often distributed across investigation collections, files, tables and metadata. Finding relevant historical experiments and understanding whether two records are comparable can take time. SciNeurix organizes the included records and provides tools to:

1. Trace relationships among investigations, experiment records, materials, conditions and evidence.
2. Filter the records within a selected investigation family.
3. Retrieve source evidence to support a research question.
4. Describe a proposed scenario and find historical records with similar recorded conditions.
5. Compare measured outcomes in the retrieved records and identify where the archive has little or no coverage.

This supports literature/data exploration and early experiment planning. It does not replace domain expertise or experimental validation.

## Included NASA collections

The supplied dataset export contains **872 experiment rows**:

| NASA accession | Investigation | Records | Experimental family |
|---|---|---:|---|
| PSI-25 | BASS-II | 129 | Solid-fuel flame growth, spread and extinction in low-velocity forced flow |
| PSI-69 | FLEX | 274 | Liquid-droplet burning and flame extinguishment |
| PSI-107 | SPICE | 469 | Nonbuoyant jet diffusion flames and smoke-point/co-flow conditions |

The bundle also includes an exported knowledge graph, evidence records, investigation metadata and quality/missingness/unit audit files. Counts refer to the included project export, not necessarily the full live NASA repository.

## Main modules

### 1. Overview
Shows dataset coverage, the three investigation families and the end-to-end research workflow.

### 2. Combustion Knowledge Engine
Explores exported graph nodes and relationships. The graph is a navigational representation of dataset relationships, not a causal scientific model.

### 3. Intelligent Experiment Discovery
Filters records within one NASA investigation by fuel/material and available operating conditions. It displays original record identifiers, source file/row provenance and available measurements.

### 4. Evidence-Based AI Research Assistant
Retrieves evidence records first, then optionally uses a Google GenAI model to draft a response using only retrieved evidence. Source records are displayed for inspection. If no relevant evidence is retrieved, generation is skipped. If the API is unavailable, the app uses an evidence-only response.

### 5. Fire-Safety Insight Lab
This is the main scenario-exploration module:
- Select one investigation family and (optionally) a fuel/material.
- Choose one or two numeric conditions actually present in that family's records.
- Enter target values and tolerances.
- Retrieve experiments whose recorded values fall within every selected tolerance.
- If no record matches, inspect the nearest available historical records.
- Compare the measured outcome distribution in the matched records with the full investigation-family distribution.
- Review outcome data coverage and source provenance.

**How to explain its value:** it helps researchers assess whether the existing archive contains experiments near a proposed set of conditions, what was measured in those historical experiments, and which combinations have weak or missing coverage. That can inform the design of a follow-up experiment. It does not calculate what would happen in a new experiment.

## Scientific safeguards

- BASS-II, FLEX and SPICE are different experimental families. The app does not combine their measurements into one pooled comparison.
- Comparisons are kept within the selected investigation.
- A missing value is not zero.
- A nearby record is not automatically an exact match; the user sets the condition tolerances.
- The full-family distribution includes matched records, so it is context rather than an independent control group.
- Similar recorded conditions do not establish causation.
- Insight Lab is not a validated combustion simulator, physical model or prediction engine.
- Source accession, file and row identifiers are retained wherever available.

## Run locally (Windows / VS Code)

Python 3.11 is recommended.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Open `http://localhost:8501`.

## Google API key

The API key field is in the left sidebar. Paste your own Google AI Studio API key there if you want generated answers. It is stored in Streamlit session state for the current session and is not written to project files. Do not show the key in a screen recording or commit it to GitHub.

You may also configure `GEMINI_API_KEY` using Streamlit secrets or an environment variable for deployment. The model fallback list is in `src/agents/llm.py`. Model availability and quotas depend on the Google project and current provider access. The app remains usable in evidence-only mode.

## Project structure

```text
SciNeurix/
├── app.py
├── app_pages/
│   ├── overview.py
│   ├── knowledge_graph.py
│   ├── discovery.py
│   ├── research_assistant.py
│   └── insight_lab.py
├── src/
│   ├── data.py
│   └── agents/
├── assets/images/
├── data/
├── .streamlit/config.toml
├── .env.example
├── requirements.txt
├── README.md
└── DEMO_GUIDE.md
```

## Known limitations

This is a research prototype. Scenario matching currently uses numeric fields available in the selected investigation and user-defined absolute tolerances. It does not adjust for every possible experimental confounder, learn a physical response surface, estimate uncertainty for a new experiment, or establish causal effects. A domain researcher should inspect the original NASA source and experimental setup before using a retrieved comparison to justify a new test.
