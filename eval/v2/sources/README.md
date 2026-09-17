# Evaluation-book sources

Evaluation V2 uses Project Gutenberg eBook #113, *The Secret Garden*, as a zero-tuning second-book holdout.

The canonical source is pinned in `secret_garden.json`. Large source/PDF artifacts stay under the gitignored `eval/.cache/` directory.

The canonical Gutenberg text is the semantic source of truth. The generated PDF validates the same parser path used by the application. Coverage is assessed with deterministic, ordered token normalization because base PDF fonts and extraction can change typography without losing words; raw punctuation or regex-hit counts are not an equivalence contract.

```sh
backend/.venv/bin/python scripts/evaluation/prepare_secret_garden.py
backend/.venv/bin/python scripts/evaluation/prepare_secret_garden.py --offline
backend/.venv/bin/python scripts/evaluation/verify_v2_source_consistency.py
```

The first command downloads the pinned canonical text when necessary. The offline command regenerates the text-layer PDF and repeats deterministic coverage checks without network access. A source hash change stops the script for manual review.
