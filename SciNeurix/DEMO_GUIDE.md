# SciNeurix — Demo & Video Guide

## The core message

**SciNeurix helps researchers move from a proposed combustion scenario to relevant historical NASA evidence.** It connects records, retrieves comparable experiments, compares observed measurements and highlights data-coverage gaps. It does not predict the result of a new experiment.

## 3-minute walkthrough

### 1. Overview — 20 seconds
**Show:** the three NASA collections and dataset metrics.

**Say:** “SciNeurix organizes 872 exported experiment records from three NASA PSI investigations. These are different experimental families, so the platform keeps them separate instead of mixing measurements that may not be comparable.”

### 2. Knowledge Engine — 25 seconds
**Show:** relationship map, filter and relationship table.

**Say:** “The Knowledge Engine makes the dataset easier to navigate. It connects investigation records with materials, conditions and evidence, so the researcher can inspect how information is organized and trace it back to the exported records.”

### 3. Experiment Discovery — 30 seconds
**Show:** select one family, choose material and condition range, inspect record table and measurement distribution.

**Say:** “Instead of manually searching large tables, the researcher filters one investigation by fuel and operating conditions, then inspects the measurements that are actually available. Source file and row identifiers remain visible.”

### 4. AI Research Assistant — 35 seconds
**Ask:** “What evidence is available in BASS-II about oxygen concentration and flame behavior?”

**Say:** “The assistant retrieves evidence first. If relevant evidence is found, the model can summarize only that retrieved material and show the supporting NASA sources. If no evidence is retrieved or the model is unavailable, it does not invent an answer.”

### 5. Insight Lab — 55 seconds (the main feature)
**Show:**
1. Select BASS-II, FLEX or SPICE.
2. Select a fuel/material if relevant.
3. Select one or two available conditions.
4. Enter target values and tolerances.
5. Show matched record count.
6. Select an outcome and show the comparison chart.
7. Show the source records or nearest records if no match exists.

**Say:** “This is the main research-planning workflow. Imagine a researcher wants to explore a new combination of experimental conditions. They enter the target conditions here. SciNeurix searches the same NASA investigation for historical experiments that fall within the selected tolerances. It then shows what those experiments actually measured and how much outcome data is available. If there are no close matches, that itself is useful: it reveals a coverage gap in the current dataset. The researcher can use this evidence to decide whether a follow-up experiment may be worth investigating.”

**Important honest qualification:** “The platform does not simulate a new experiment or predict its outcome. It retrieves nearby historical evidence. A researcher must still review differences in apparatus, geometry, fuel preparation and measurement methods.”

### Closing — 10 seconds
“SciNeurix turns disconnected experiment records into a traceable research workflow — from discovery to evidence comparison and more informed experiment planning.”

## 30-second version

- **0–4s · Overview:** “SciNeurix turns NASA combustion experiment records into a connected research workspace.”
- **4–8s · Knowledge Engine:** “It links investigations, experiment records, materials, conditions and evidence.”
- **8–12s · Discovery:** “Researchers can find relevant experiments and inspect their actual measurements.”
- **12–23s · Insight Lab:** “They can define a proposed scenario, retrieve historical experiments near those conditions, compare observed outcomes and identify where the dataset has little coverage.”
- **23–30s · Close:** “It does not guess what a new experiment will do. It helps researchers make better-informed decisions using existing NASA evidence.”

## Suggested Insight Lab demo scenario

Pick one investigation and use values inside the observed data range. Do not choose a condition that is unavailable in that investigation. The page shows the actual min/max values implicitly through the number input bounds. If you get zero matches, widen the tolerance slightly or show the nearest records as a coverage-gap example.

## Recording checklist

- Run the app and open all five pages before recording.
- Prepare the AI question and test it once; do not expose the API key.
- Preselect a meaningful Insight Lab family, material, condition and outcome.
- Use browser zoom 90–100%.
- Avoid long waits; if AI is slow, show evidence-only mode honestly.
- Do not call the Insight Lab a simulator, digital twin, predictor or validated fire-safety model.
