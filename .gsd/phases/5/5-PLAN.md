---
phase: 5
plan: 1
wave: 1
---

# Plan 5.1: Evaluation Script & Mean Recall@10 Benchmarking

## Objective
Generate an evaluation script that traverses the target `Gen_AI Dataset.xlsx` training parameters, automatically triggering the Python RAG engine against expected benchmarks to calculate the Mean Recall@10 validation score, and output the tuned test results.

## Context
- .gsd/SPEC.md
- src/balancer.py
- src/app.py
- Expected mapping dataset: `Gen_AI Dataset.xlsx` 

## Tasks

<task type="auto">
  <name>Scaffold Python Evaluation Logic Structure</name>
  <files>src/evaluate.py</files>
  <action>
    - Create an autonomous Python module `src/evaluate.py` using `pandas` and `openpyxl`.
    - Check for the existence of `data/Gen_AI Dataset.xlsx` (or its CSV equivalent depending on the physical local environment mount) at runtime.
    - If the file is missing, halt gracefully and print a requirement requesting the dataset path.
    - Traverse the Dataset `Query` structure. For every query payload, invoke the internal `get_balanced_recommendations()` proxy.
    - Measure if the specific target truth URL resides inside the `Top 10` Assessment_url results payload matrix natively.
  </action>
  <verify>cat src/evaluate.py</verify>
  <done>Evaluation parsing scripts created encapsulating `pandas` DataFrame read integrations successfully.</done>
</task>

<task type="checkpoint:human-verify">
  <name>Execute Validation Test and Measure Mean Recall@10</name>
  <files>src/evaluate.py</files>
  <action>
    - Using `source venv/bin/activate`, execute the evaluation tests natively across the entire domain dataset.
    - Print evaluation metrics in CLI specifying standard Mean Recall@10 accuracy properties (e.g. `Hits: 8/10`, `Recall: 80%`).
    - Capture the analytical predictions pushing data to `data/results.csv` logging exactly `Query` and the produced dynamic AI `Assessment_url`.
  </action>
  <verify>python src/evaluate.py</verify>
  <done>Evaluation script runs perfectly against the targeted parameter outputs yielding the final statistical validation metrics into `results.csv`.</done>
</task>

## Success Criteria
- [ ] Evaluation `evaluate.py` script traverses an Excel dataset dynamically.
- [ ] Analytical execution proves and emits Mean Recall@10 validation percentage scores.
- [ ] CSV Output is rendered completely reflecting evaluation criteria.
