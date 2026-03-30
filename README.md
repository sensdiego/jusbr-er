# JusBR-ER

![Task](https://img.shields.io/badge/task-entity%20resolution-1f6feb)
![Language](https://img.shields.io/badge/language-Brazilian%20Portuguese-2e8b57)
![Dataset](https://img.shields.io/badge/dataset-1%2C071%20pairs-0a7ea4)
![Labels](https://img.shields.io/badge/labels-530%20merge%20%7C%20541%20no__merge-6f42c1)
![Licensing](https://img.shields.io/badge/licensing-data%20CC%20BY--NC--SA%204.0%20%7C%20code%20MIT-8b0000)

The public benchmark repository for **JusBR-ER**, a benchmark for entity
resolution of legal concepts in Brazilian Portuguese.

JusBR-ER contains 1,071 labeled pairs of Brazilian legal concepts validated by
a practicing lawyer (OAB/PR 96,036), covering synonyms, writing variants,
antonym traps, and genus-species distinctions.

Language: [pt-BR](README.pt-BR.md) | `English`

## Repository Snapshot

| Field | Value |
|-------|-------|
| Task | Entity resolution of legal concepts |
| Language | Brazilian Portuguese |
| Total pairs | 1,071 |
| Positive pairs | 530 `merge` |
| Negative pairs | 541 `no_merge` |
| Validator | Practicing lawyer, OAB/PR 96,036 |
| Version | 1.0 |

## Repository Contents

| Asset | Description |
|-------|-------------|
| [`jusbr_er_v1.json`](jusbr_er_v1.json) | Main benchmark dataset |
| [`synonym_dict_full.json`](synonym_dict_full.json) | Validated synonym dictionary |
| [`synonym_dict_sample.json`](synonym_dict_sample.json) | Sample subset of synonym pairs |
| [`eval_baseline.py`](eval_baseline.py) | Standalone baseline evaluation script |
| [`annotation_guidelines.md`](annotation_guidelines.md) | Annotation guidelines and borderline rulings |

## What The Benchmark Covers

JusBR-ER is designed for legal concept matching, not just generic string
similarity.

It includes:

- technical synonyms
- writing variants
- legal concepts that look similar but should stay separate
- antonym and opposition traps
- genus-species and sibling-category distinctions

## Dataset Format

```json
{
  "metadata": {
    "name": "JusBR-ER",
    "version": "1.0"
  },
  "pairs": [
    {
      "pair_id": 87,
      "entity_a": "Periculum in mora",
      "entity_b": "Perigo de dano",
      "decision": "merge",
      "relationship_type": "sinonimo"
    }
  ]
}
```

## Label Taxonomy

| Type (pt-BR) | English gloss | Merge? |
|--------------|---------------|:------:|
| `identico` | identical | Yes |
| `sinonimo` | synonym | Yes |
| `variante` | writing variant | Yes |
| `genero_especie` | genus-species | No |
| `especies_mesmo_genero` | same-genus siblings | No |
| `antonimo_complementar` | complementary antonym | No |
| `sem_relacao` | unrelated | No |

## Baseline Snapshot

| Setting | Precision | Recall | F1 |
|---------|:---------:|:------:|:--:|
| JW threshold 0.95 | 92.1% | 10.9% | 19.6% |
| JW threshold 0.88 (default) | 50.2% | 24.1% | 32.6% |
| JW threshold 0.70 | 55.6% | 81.9% | 66.3% |
| Embedding-first blocking + Claude Sonnet 4.6 | - | - | 85.9% |

## Quick Start

Run the standalone baseline:

```bash
python eval_baseline.py --dataset jusbr_er_v1.json
```

Run the threshold sweep:

```bash
python eval_baseline.py --dataset jusbr_er_v1.json --sweep
```

No external dependencies are required. Python 3.8+ is enough.

## Usage And Licensing

The repository uses a split licensing model:

- dataset and annotation guidelines: CC BY-NC-SA 4.0
- synonym dictionary: CC BY-NC-SA 4.0
- evaluation code: MIT

Free for academic and research use. Commercial use requires authorization:
diego@sens.legal

## Citation

```bibtex
@inproceedings{sens2026jusbrer,
  title={JusBR-ER: A Benchmark for Entity Resolution of Legal Concepts in Brazilian Portuguese},
  author={Sens, Diego},
  booktitle={Proceedings of the Natural Legal Language Processing Workshop (NLLP)},
  year={2026},
  url={https://github.com/sensdiego/jusbr-er}
}
```

## Contact

Diego Sens — diego@sens.legal — [sens.legal](https://sens.legal)
