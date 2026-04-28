---
name: model-card
description: Generate a model card for an ML model — purpose, training data, performance metrics, limitations, and responsible AI considerations.
domain: data-ml
requires_script: false
---

## Usage

Invoke with `/model-card` then provide:
- Model name and what it predicts/classifies
- Training data description (sources, size, date range)
- Performance metrics (accuracy, F1, AUC, RMSE, etc.)
- Known limitations or failure modes
- Intended and out-of-scope uses

Partial information is fine — the skill will mark missing sections `[TBD]` and prompt for them.

## Output

A model card document in Markdown, suitable for publishing to Confluence, the ML registry, or the repo.

```markdown
# Model Card: <Model Name>

**Version:** 1.0.0
**Owner:** [team]
**Last updated:** YYYY-MM-DD
**Status:** Production | Staging | Deprecated

---

## Model Overview

| Field | Value |
|-------|-------|
| Task | Binary classification |
| Input | Customer transaction features (15 numeric, 3 categorical) |
| Output | Probability of churn (0–1) + binary label (threshold: 0.5) |
| Framework | scikit-learn 1.4, XGBoost 2.0 |
| Inference latency | ~12ms per record (CPU) |

## Intended Use

**Primary use case:** Identify customers at high risk of churn for proactive retention campaigns.

**Out-of-scope uses:**
- Predicting churn for enterprise/B2B accounts (trained only on B2C data)
- Real-time serving at <5ms latency (not optimised for this)
- Any use involving protected characteristics as features

## Training Data

| Attribute | Value |
|-----------|-------|
| Source | CRM transaction history |
| Date range | Jan 2022 – Dec 2024 |
| Size | 2.1M records |
| Label | Churned within 90 days of observation date |
| Class balance | 12% positive (churned), 88% negative |

**Preprocessing:** Missing values imputed with column median; categorical features one-hot encoded.

## Performance Metrics

Evaluated on held-out test set (20% stratified split):

| Metric | Value |
|--------|-------|
| AUC-ROC | 0.847 |
| F1 Score (threshold 0.5) | 0.71 |
| Precision | 0.74 |
| Recall | 0.68 |
| Accuracy | 0.89 |

**Slice performance:** Lower recall observed for customers with <3 months tenure (recall: 0.51). See [evaluation report](link).

## Limitations & Known Issues

- Underperforms for new customers (< 3 months tenure) — insufficient signal
- Seasonal bias: trained on data from COVID-period may not generalise to current behaviour
- Requires re-training every 6 months to avoid drift (last training: YYYY-MM-DD)

## Responsible AI

- **Fairness:** No protected characteristics (age, gender, ethnicity) used as features
- **Explainability:** SHAP values available per prediction; top 3 features returned with each inference
- **Privacy:** Model trained on anonymised data; no PII in features
- **Monitoring:** Drift detection on feature distributions weekly; alert threshold: PSI > 0.2

## Inference & Deployment

- **Endpoint:** [Azure ML endpoint URL or internal link]
- **Input schema:** [link to schema docs]
- **Batch vs real-time:** Both supported
- **Retraining schedule:** Every 6 months, or when PSI drift alert fires

## References

- Training notebook: [link]
- Evaluation report: [link]
- Feature engineering doc: [link]
```

## Steps

1. Identify model name, task type, and owner
2. Populate the overview table (input/output schema, framework, latency if known)
3. Document intended and out-of-scope uses — be specific about what the model should NOT be used for
4. Describe training data: sources, size, date range, label definition, class balance
5. List all performance metrics; flag if slice performance differs significantly from overall
6. Document known limitations — be honest; this is a safety document
7. Fill in the responsible AI section (fairness, explainability, privacy, monitoring)
8. Mark anything unknown as `[TBD]` and prompt the user to fill it in before publishing
