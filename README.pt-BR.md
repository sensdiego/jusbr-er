# JusBR-ER

![Task](https://img.shields.io/badge/tarefa-entity%20resolution-1f6feb)
![Language](https://img.shields.io/badge/idioma-portugues%20brasileiro-2e8b57)
![Dataset](https://img.shields.io/badge/dataset-1%2C071%20pares-0a7ea4)
![Labels](https://img.shields.io/badge/rotulos-530%20merge%20%7C%20541%20no__merge-6f42c1)
![Licensing](https://img.shields.io/badge/licenciamento-dados%20CC%20BY--NC--SA%204.0%20%7C%20codigo%20MIT-8b0000)

O repositorio publico do **JusBR-ER**, um benchmark para entity resolution de
conceitos juridicos em portugues brasileiro.

O JusBR-ER contem 1.071 pares rotulados de conceitos juridicos brasileiros,
validados por advogado em exercicio (OAB/PR 96.036), cobrindo sinonimos,
variantes de escrita, armadilhas antonimicas e distincao genero-especie.

Idioma: `pt-BR` | [English](README.md)

## Snapshot do Repositorio

| Campo | Valor |
|-------|-------|
| Tarefa | Entity resolution de conceitos juridicos |
| Idioma | Portugues brasileiro |
| Total de pares | 1.071 |
| Pares positivos | 530 `merge` |
| Pares negativos | 541 `no_merge` |
| Validador | Advogado em exercicio, OAB/PR 96.036 |
| Versao | 1.0 |

## Conteudo do Repositorio

| Ativo | Descricao |
|-------|-----------|
| [`jusbr_er_v1.json`](jusbr_er_v1.json) | Dataset principal do benchmark |
| [`synonym_dict_full.json`](synonym_dict_full.json) | Dicionario validado de sinonimos |
| [`synonym_dict_sample.json`](synonym_dict_sample.json) | Amostra reduzida de pares sinonimicos |
| [`eval_baseline.py`](eval_baseline.py) | Script standalone de avaliacao baseline |
| [`annotation_guidelines.md`](annotation_guidelines.md) | Diretrizes de anotacao e casos borderline |

## O Que o Benchmark Cobre

O JusBR-ER foi desenhado para matching de conceitos juridicos, e nao apenas
para similaridade textual generica.

Ele inclui:

- sinonimos tecnicos
- variantes de escrita
- conceitos juridicos parecidos que devem permanecer separados
- armadilhas de antonimia e oposicao
- relacoes de genero-especie e categorias irmas

## Formato do Dataset

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

## Taxonomia de Rotulos

| Tipo (pt-BR) | Gloss em ingles | Merge? |
|--------------|-----------------|:------:|
| `identico` | identical | Yes |
| `sinonimo` | synonym | Yes |
| `variante` | writing variant | Yes |
| `genero_especie` | genus-species | No |
| `especies_mesmo_genero` | same-genus siblings | No |
| `antonimo_complementar` | complementary antonym | No |
| `sem_relacao` | unrelated | No |

## Snapshot do Baseline

| Configuracao | Precision | Recall | F1 |
|--------------|:---------:|:------:|:--:|
| Threshold JW 0.95 | 92.1% | 10.9% | 19.6% |
| Threshold JW 0.88 (default) | 50.2% | 24.1% | 32.6% |
| Threshold JW 0.70 | 55.6% | 81.9% | 66.3% |
| Bloqueio por embedding + Claude Sonnet 4.6 | - | - | 85.9% |

## Quick Start

Rodar o baseline standalone:

```bash
python eval_baseline.py --dataset jusbr_er_v1.json
```

Rodar sweep de threshold:

```bash
python eval_baseline.py --dataset jusbr_er_v1.json --sweep
```

Nao ha dependencias externas. Python 3.8+ e suficiente.

## Uso e Licenciamento

O repositorio usa um modelo de licenciamento separado:

- dataset e diretrizes de anotacao: CC BY-NC-SA 4.0
- dicionario de sinonimos: CC BY-NC-SA 4.0
- codigo de avaliacao: MIT

Uso academico e de pesquisa esta liberado. Uso comercial depende de
autorizacao: diego@sens.legal

## Citacao

```bibtex
@inproceedings{sens2026jusbrer,
  title={JusBR-ER: A Benchmark for Entity Resolution of Legal Concepts in Brazilian Portuguese},
  author={Sens, Diego},
  booktitle={Proceedings of the Natural Legal Language Processing Workshop (NLLP)},
  year={2026},
  url={https://github.com/sensdiego/jusbr-er}
}
```

## Contato

Diego Sens — diego@sens.legal — [sens.legal](https://sens.legal)
