# Text2EF — Natural Language to Entity Framework

**Text2EF** advances the Text2SQL task by generating **Entity Framework (ORM)** queries
instead of raw SQL, so natural-language questions map onto the object-oriented data-access
layer developers actually use. It was developed as an MSc thesis at the University of
Bucharest, Faculty of Mathematics and Computer Science (2024).

## Results

Evaluated on the [Spider](https://yale-lily.github.io/spider) text-to-SQL benchmark:

| Metric | Result |
|---|---|
| Spider queries successfully converted to Entity Framework (via SQL2EF) | **87%** |
| Query accuracy — base LLaMA 3 (8B) | 31.26% |
| Query accuracy — fine-tuned LLaMA 3 (8B) | **51.46%** |
| Relative improvement from fine-tuning | **≈ 65%** |

Accuracy is measured by **execution correctness**: the generated Entity Framework query is
compiled and run, and its result set is compared against the gold query — across the 787
evaluation examples in `evaluation/`. The gain was achieved **without extensive prompt
engineering**, purely through dataset construction and fine-tuning.

## How it works

1. **SQL2EF** (`sql2ef/`) — a Rust pipeline that translates Spider's SQL queries into
   equivalent Entity Framework (LINQ) queries, handling schema mapping, aliasing,
   projections, filtering, joins, keywords, and grouping.
2. **Dataset generation** (`merge_datasets.py`, `entity-framework/`) — builds a
   natural-language → Entity Framework training set from the converted queries.
3. **Fine-tuning** (`llama/`) — fine-tunes LLaMA 3 (8B) on the generated dataset using
   [Unsloth](https://github.com/unslothai/unsloth).
4. **Evaluation** (`evaluation/`) — compiles and executes each generated query against the
   target database and records pass / build-failure / execution-failure status.

## Repository structure

| Path | Purpose |
|---|---|
| `sql2ef/` | Rust SQL → Entity Framework conversion pipeline |
| `entity-framework/` | Entity Framework project and query-testing harness |
| `llama/` | LLaMA 3 fine-tuning and inference |
| `evaluation/` | Execution-based evaluation and result files |
| `merge_datasets.py` | Dataset assembly |
| `Rusu_Andrei-Cristian_Masters_Thesis.pdf` | Full thesis (methodology, experiments, analysis) |

## Thesis

The complete methodology, experiments, and error analysis are in
[`Rusu_Andrei-Cristian_Masters_Thesis.pdf`](./Rusu_Andrei-Cristian_Masters_Thesis.pdf).

**Author:** Rusu Andrei-Cristian · **Scientific coordinator:** Păduraru Ciprian Ionuț
