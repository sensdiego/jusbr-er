# Annotation Guidelines — Entity Resolution de Conceitos Jurídicos

**Versão:** 1.0 (aprovado por Diego em 2026-03-20)
**Validador:** Diego Sens, OAB/PR 96036
**Contexto:** Pares de entidades do knowledge graph Valter (STJ + TJPR + TJSP)

---

## 1. Objetivo

Decidir se dois nomes de entidade no knowledge graph referem-se **ao mesmo conceito
jurídico** e, portanto, devem ser representados como um único nó.

A validação é feita em **duas passadas**:

- **Pass 1 (binária):** "São a mesma coisa? Sim ou não." → `merge` ou `no_merge`
- **Pass 2 (classificação):** "Qual é a relação entre eles?" → um dos 7 tipos abaixo

Pass 1 é suficiente para calibrar thresholds e comparar modelos. Pass 2 enriquece
o dataset para o paper e para a representação tipada do grafo.

---

## 2. Regra de Decisão Binária (Pass 1)

### merge

Marque `merge` se as duas entidades **devem ser um único nó** no grafo de conhecimento.
A pergunta-chave é: "Um advogado pesquisando por A ficaria satisfeito encontrando
resultados de B?"

Critério prático: se você estivesse organizando as ementas em pastas, A e B iriam
na **mesma pasta**.

### no_merge

Marque `no_merge` se as duas entidades representam **conceitos distintos** que merecem
nós separados, mesmo que sejam da mesma área jurídica ou compartilhem palavras.

---

## 3. Taxonomia de Relações (Pass 2)

### 3.1 Relações que resultam em MERGE

#### `identico` — Nomes idênticos (após normalização)

O mesmo texto, possivelmente com diferenças de acentuação, capitalização ou abreviatura.

| | Entidade A | Entidade B | Decisão |
|---|---|---|---|
| Claro | Tempestividade do recurso | Tempestividade do recurso | merge |
| Claro | Inversão do ônus da prova | Inversão do ônus da prova | merge |

#### `sinonimo` — Sinônimo técnico

Dois nomes diferentes para o **mesmo conceito jurídico**. Um advogado usa os dois
termos de forma intercambiável no mesmo contexto.

| | Entidade A | Entidade B | Decisão |
|---|---|---|---|
| Claro | Reexame de matéria fática | Reexame de matéria fático-probatória | merge |
| Claro | Ônus probatório | Ônus da prova | merge |
| Borderline | Periculum in mora | Perigo de dano | merge? |
| Borderline | Fumus boni iuris | Probabilidade do direito | merge? |

> **Nota sobre latin/português:** Termos latinos e suas traduções portuguesas
> consagradas pelo CPC/2015 são sinônimos se usados no mesmo contexto processual.
> "Periculum in mora" e "perigo de dano" referem-se ao mesmo requisito da tutela
> de urgência após o CPC/2015 (art. 300). Decidir como `merge`.

#### `variante` — Variante textual

O mesmo conceito expresso com palavras ligeiramente diferentes — abreviatura,
reordenação, preposição diferente, referência normativa equivalente.

| | Entidade A | Entidade B | Decisão |
|---|---|---|---|
| Claro | Prescrição quinquenal | Prazo prescricional quinquenal | merge |
| Claro | Violação ao art. 535 do CPC/1973 | Ofensa ao art. 535 do CPC | merge |
| Claro | Vedação ao reexame de provas no recurso especial | Vedação ao reexame de fatos e provas em recurso especial | merge |

> **Nota sobre artigos de lei:** "Art. 535 do CPC/1973" e "Art. 535 do CPC" são
> o mesmo dispositivo (CPC/1973 é o único que tem art. 535 com essa função).
> Diferenças de formato de referência normativa não fazem conceitos distintos.

### 3.2 Relações que resultam em NO_MERGE

#### `genero_especie` — Gênero/espécie

Um conceito é caso particular (espécie) do outro (gênero), ou um é mais amplo
e contém o outro.

| | Entidade A | Entidade B | Decisão |
|---|---|---|---|
| Claro | Responsabilidade civil | Responsabilidade civil do Estado | no_merge |
| Claro | Tutela provisória | Tutela de urgência | no_merge |
| Borderline | Tutela de urgência | Tutela antecipada | no_merge? |

> **Nota sobre tutela:** "Tutela de urgência" (gênero, art. 300 CPC) engloba
> "tutela antecipada" (espécie satisfativa) e "tutela cautelar" (espécie
> conservativa). São conceitos distintos — no_merge, tipo `genero_especie`.

#### `especies_mesmo_genero` — Espécies do mesmo gênero

Dois conceitos que pertencem à mesma família mas representam categorias distintas
e mutuamente exclusivas.

| | Entidade A | Entidade B | Decisão |
|---|---|---|---|
| Claro | Prescrição intercorrente | Prescrição quinquenal | no_merge |
| Claro | Aplicação da Súmula 284/STF | Aplicação da Súmula 7/STJ | no_merge |
| Claro | Nulidade da citação | Nulidade do julgado | no_merge |

#### `antonimo_complementar` — Antônimo ou complementar

Conceitos que formam um par oposto ou complementar — a presença de um implica
a exclusão do outro.

| | Entidade A | Entidade B | Decisão |
|---|---|---|---|
| Claro | Boa-fé objetiva | Boa-fé subjetiva | no_merge |
| Claro | Dano moral | Dano material | no_merge |
| Claro | Presunção relativa de má-fé do devedor | Presunção relativa de má-fé do terceiro adquirente | no_merge |

> **Regra prática:** Se os nomes diferem apenas por um qualificador oposto
> (objetivo/subjetivo, moral/material, absoluta/relativa, direta/indireta),
> são antônimos complementares → `no_merge`.

#### `sem_relacao` — Sem relação semântica

Conceitos que não têm relação semântica significativa, mesmo que compartilhem
palavras por acaso.

| | Entidade A | Entidade B | Decisão |
|---|---|---|---|
| Claro | Alegação de nulidade da citação | Nulidade do julgado | no_merge |
| Claro | Boa-fé do adquirente | Presunção relativa de má-fé do terceiro adquirente | no_merge |

---

## 4. Borderline Cases — Para Decisão do Diego

Os seguintes pares exigem ruling explícito para estabelecer precedente:

### 4.1 "Tutela de urgência" vs "Tutela antecipada"

- **Opção A:** `merge` (sinônimo) — no uso coloquial, advogados usam como sinônimos
- **Opção B:** `no_merge` (gênero/espécie) — tecnicamente, tutela de urgência é
  gênero que inclui antecipada e cautelar
- **Recomendação:** `no_merge` (`genero_especie`) — o grafo deve preservar a
  distinção técnica do CPC/2015

**Diego decide:** `no_merge` (`genero_especie`) ✓

### 4.2 "Responsabilidade civil" vs "Responsabilidade civil do Estado"

- **Opção A:** `merge` — mesma base conceitual
- **Opção B:** `no_merge` (gênero/espécie) — responsabilidade civil é gênero,
  a do Estado é espécie com regime jurídico próprio (art. 37, §6º, CF)
- **Recomendação:** `no_merge` (`genero_especie`)

**Diego decide:** `no_merge` (`genero_especie`) ✓

### 4.3 "Fumus boni iuris" vs "Probabilidade do direito"

- **Opção A:** `merge` (sinônimo) — CPC/2015 substituiu o termo latino pelo
  português; no contexto de tutela de urgência, são o mesmo requisito
- **Opção B:** `no_merge` — termos de diplomas diferentes, com nuances doutrinárias
- **Recomendação:** `merge` (`sinonimo`) — no contexto prático do STJ/TJs,
  são usados como sinônimos para o mesmo requisito processual

**Diego decide:** `merge` (`sinonimo`) ✓

### 4.4 "Ofensa ao art. 535" vs "Violação ao art. 535"

- **Opção A:** `merge` (variante) — "ofensa" e "violação" são sinônimos neste
  contexto recursal
- **Opção B:** `no_merge` — termos distintos
- **Recomendação:** `merge` (`variante`) — são variações textuais do mesmo
  argumento recursal

**Diego decide:** `merge` (`variante`) ✓

---

## 5. Uso do Campo "Notes"

Use o campo `notes` nos seguintes casos:

1. **Dúvida na decisão:** "Poderia ser gênero/espécie, optei por sinônimo porque..."
2. **Contexto necessário:** "Esse par depende da vara — em vara cível é sinônimo,
   em vara de fazenda não"
3. **Erro no dado:** "Entidade B parece ter sido extraída incorretamente"
4. **Caso novo:** "Padrão não coberto pelas guidelines — decidir regra"

Não é necessário preencher notes para decisões óbvias.

---

## 6. Instruções de Preenchimento

### Pass 1 (merge/no_merge)

1. Leia as duas entidades
2. Pergunte: "Um advogado pesquisando A ficaria satisfeito com resultados de B?"
3. Se sim → `merge`. Se não → `no_merge`
4. Na dúvida, use `notes` para registrar a hesitação
5. Tempo estimado: ~5-8 segundos por par

### Pass 2 (relationship type)

1. A decisão binária já está feita — apenas classifique o tipo
2. Para `merge`: escolha entre `identico`, `sinonimo`, `variante`
3. Para `no_merge`: escolha entre `genero_especie`, `especies_mesmo_genero`,
   `antonimo_complementar`, `sem_relacao`
4. Tempo estimado: ~5 segundos por par

### Formato da tabela (Pass 1)

```
| # | Entidade A | Entidade B | Confiança | Decisão |
|---|-----------|-----------|:---------:|---------|
| 1 | Ônus probatório | Ônus da prova | 0.92 | merge |
| 2 | Boa-fé objetiva | Boa-fé subjetiva | 0.87 | no_merge |
```

### Formato da tabela (Pass 2)

```
| # | Entidade A | Entidade B | Decisão | Tipo | Notes |
|---|-----------|-----------|---------|------|-------|
| 1 | Ônus probatório | Ônus da prova | merge | sinonimo | |
| 2 | Boa-fé objetiva | Boa-fé subjetiva | no_merge | antonimo_complementar | |
```

---

## 7. Regra Especial: Equivalência CPC/1973 ↔ CPC/2015

Artigos do CPC/1973 e seus correspondentes no CPC/2015 (ex: art. 535 ↔ art. 1.022)
foram classificados como **merge** neste benchmark para fins de entity resolution
no knowledge graph, porque o advogado pesquisando um encontra valor no outro.

**Ressalva importante:** O CPC/1973 deixou de valer com a entrada em vigor do
CPC/2015 (18/03/2016). Menções ao CPC/1973 têm aplicabilidade limitada:
- Aplicam-se a fatos e atos processuais praticados sob a vigência do código antigo
- Regras de direito intertemporal (art. 1.046 CPC/2015) definem qual código se aplica
- Em produção, o pipeline pode querer distinguir contextos temporais

Para o benchmark: merge (mesma tese jurídica, diplomas diferentes).
Para produção: considerar flag de regime temporal no nó do grafo.

## 8. Regras de Consistência

1. **Transitividade:** Se A=B e B=C, então A=C. Se ao validar você encontrar
   um par que contradiz decisões anteriores, marque em `notes`.
2. **Simetria:** A decisão para (A, B) é a mesma que para (B, A).
3. **Contexto do STJ:** Em caso de dúvida, considere o uso predominante no
   STJ (Corte de uniformização), não usos regionais excepcionais.
4. **CPC/2015 prevalece:** Para termos que mudaram com o CPC/2015, considere
   a terminologia atual como canônica, mas mantenha sinônimos com o termo antigo.

---

*Guideline aprovado por Diego Sens em: 2026-03-20*
