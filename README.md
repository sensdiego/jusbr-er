# JusBR-ER: A Benchmark for Entity Resolution of Legal Concepts in Brazilian Portuguese

The first benchmark for entity resolution of legal concepts. 1,071 pairs of Brazilian legal concepts validated by a practicing lawyer (OAB/PR 96,036), covering synonyms, writing variants, antonym traps, and genus-species distinctions.

## Contents

| File | Description |
|------|-------------|
| `jusbr_er_v1.json` | Benchmark dataset: 1,071 labeled pairs (530 merge / 541 no_merge) |
| `synonym_dict_full.json` | Validated synonym dictionary: 487 legal concept pairs |
| `synonym_dict_sample.json` | Sample of 100 synonym pairs |
| `eval_baseline.py` | Standalone baseline evaluation (JW + qualifier guard, no dependencies) |
| `annotation_guidelines.md` | Annotation guidelines with borderline rulings |

## Quick Start

```bash
# Run JW baseline with qualifier guard
python eval_baseline.py --dataset jusbr_er_v1.json

# Threshold sweep
python eval_baseline.py --dataset jusbr_er_v1.json --sweep
```

No external dependencies required. Python 3.8+ only.

## Dataset Format

```json
{
  "metadata": { "name": "JusBR-ER", "version": "1.0", ... },
  "pairs": [
    {
      "pair_id": 87,
      "entity_a": "Periculum in mora",
      "entity_b": "Perigo de dano",
      "decision": "merge",
      "relationship_type": "sinonimo"
    },
    ...
  ]
}
```

### Relationship Types

| Type (pt-BR) | Type (EN) | Merge? |
|------|------|:------:|
| `identico` | identical | Yes |
| `sinonimo` | synonym | Yes |
| `variante` | writing variant | Yes |
| `genero_especie` | genus-species | No |
| `especies_mesmo_genero` | same-genus siblings | No |
| `antonimo_complementar` | complementary antonym | No |
| `sem_relacao` | unrelated | No |

## Baseline Results

| JW Threshold | Precision | Recall | F1 |
|:---:|:---:|:---:|:---:|
| 0.95 | 92.1% | 10.9% | 19.6% |
| 0.88 (default) | 50.2% | 24.1% | 32.6% |
| 0.70 | 55.6% | 81.9% | 66.3% |

With embedding-first blocking (BGE-M3 cosine >= 0.70) + Claude Sonnet 4.6: **F1 = 85.9%**

## License

- **Dataset and annotation guidelines:** CC BY-NC-SA 4.0
- **Synonym dictionary:** CC BY-NC-SA 4.0
- **Evaluation code:** MIT

Free for academic and research use. Commercial use requires authorization: diego@sens.legal

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
