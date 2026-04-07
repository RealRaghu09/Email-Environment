# Email Auto-Triage (Simple)

This small project demonstrates a simple Email Auto-Triage system with a
hand-written environment, a baseline agent, and a training/runner script.

Requirements
- Python 3.8+
- (Optional) `openenv` if you want to adapt the environment to a specific
  OpenEnv API — the included `EmailTriageEnv` is framework-agnostic.

Run

From the repository root (where this README sits):

```bash
python -m email_triage.train
```

What it does
- Loads a sample dataset of 10 emails (`dataset.py`).
- Uses a `RuleAgent` (keyword-based) to classify priority and category.
- Prints per-email predictions and overall accuracy.
- Saves `results.csv` under the `email_triage` folder.

Extending
- Replace `RuleAgent` with a machine-learning model that implements
  `choose_action(email)` and returns an action index.
- Add richer reward shaping or multi-step episodes if desired.
