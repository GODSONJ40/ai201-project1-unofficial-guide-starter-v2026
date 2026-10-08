# The Unofficial Guide

A retrieval-augmented generation (RAG) project for answering questions using a selected collection of documents. The system loads documents, divides them into chunks, embeds and indexes the chunks, retrieves relevant information, checks whether the question is supported, and generates an answer with sources.

This README covers Unit 1 (building the system) and Unit 2 (testing and improving it).

## The corpora

The starter includes three project corpora and one separate classroom practice corpus. They have different document shapes, which matters when choosing a chunking strategy.

| Corpus | Documents | Characters | Description |
|---|---:|---:|---|
| `campus_life` | 88 | 27,908 | Short student-life posts about housing, dining, classes, and campus rules |
| `advice_threads` | 23 | 12,490 | Question-and-answer threads with multiple replies |
| `city_guides` | 14 | 28,958 | Longer travel guides divided into sections |
| `practice` | 28 | 15,901 | Separate in-class practice corpus; not used for this project |

I selected **`campus_life`** because most documents are short enough to keep as complete, understandable chunks. The average document length is about 317 characters. The useful information is usually contained in a sentence or short paragraph.

To use another corpus, change `CORPUS` in `config.py`, set `AI201_CORPUS` in `.env`, or pass `--corpus NAME` on the command line. Rebuild the index after switching corpora.

## What This Does

The RAG pipeline has five stages:

1. **Loading:** Read the selected corpus of text documents.
2. **Chunking:** Divide documents into pieces that can be retrieved and understood.
3. **Embedding and indexing:** Turn chunks into vectors and store them in Chroma.
4. **Retrieval and relevance gate:** Retrieve likely matches and refuse questions without sufficiently close evidence.
5. **Generation:** Answer using retrieved context and name the supporting sources.

The project uses the `all-MiniLM-L6-v2` embedding model through Chroma's bundled ONNX embedding function. Chroma uses **cosine distance**, where a lower distance means a closer match. The relevance cutoff is **0.6**, and the system retrieves up to **five chunks** per question.

### Running the project

From the project folder, activate the virtual environment and run:

```cmd
.venv\Scripts\activate
python test.py
python app.py index
python app.py ask "How much does it cost to do laundry at Innisfree Hall?"
python app.py chunks -n 5
python app.py retrieve "What is the capital of Mongolia?"
```

Do not commit the `.env` file or API keys.

## Chunking Strategy

The selected corpus contains **88 short posts**, so `chunker.py::split_documents` keeps each post as one complete chunk, with no overlap. This produced **88 chunks**. Keeping the posts intact preserves the title, facts, and context together instead of cutting through a sentence or explanation. The `fallback_split` function remains available for other document shapes.

I also checked `advice_threads` as a comparison corpus; it produced 23 chunks. I kept `campus_life` for the graded project.

## Sample Chunks

These five chunks were printed by `python app.py chunks -n 5`. Each was produced by `chunker.py::split_documents`. They were also used to assess whether chunks were understandable on their own.

### Chunk 1 — `admin_add_drop_deadline.txt#0`

```text
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

### Chunk 2 — `course_biol_160.txt#0`

```text
BIOL 160 Cell Biology

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

### Chunk 3 — `course_hist_118_workload.txt#0`

```text
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

### Chunk 4 — `dining_pellew_dining_hall_followup.txt#0`

```text
Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.
```

### Chunk 5 — `housing_innisfree_hall.txt#0`

```text
Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.
```

All five chunks have enough context to answer a relevant question without reading adjacent chunks.

## Sample Answer

**Question:** How much does it cost to do laundry at Innisfree Hall?

**Actual baseline answer** (produced by `generate.py::answer_from_chunks`, using `store.py::search`):

> At Innisfree Hall, laundry costs $1.75 for a wash and $1.75 for a dry (housing_innisfree_hall.txt and housing_innisfree_hall_laundry.txt).

The answer gives the correct price and names supporting source documents.

## Unit 2 — Testing a RAG System

I tested the original system before changing retrieval, then tested it again after adding hybrid search. Both evaluations used the same `campus_life` corpus, 88 indexed chunks, five in-scope questions, five out-of-scope questions, top-k of 5, and a relevance cutoff of 0.6.

Each in-scope question was answered **three times with caching off**. The relevance-gate checks are deterministic and were performed once per out-of-scope question. Because `scorer.py` did not exist, I manually checked the actual answers and their named sources against the original acceptance criteria.

### Run Log — Before

**Command:** `python run_eval.py --label before`  
**Date:** October 7, 2026  
**Raw evidence:** `results/run_2026-10-07_2310_before.md`  
**Produced by:** `run_eval.py::main`  
**Retrieval:** `store.py::search`  
**Chunking:** `chunker.py::split_documents`

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | At least 4/5 questions | 5/5 | 5/5 | 5/5 | MET |
| 2. Every generated answer names a source | 5/5 answers | 5/5 | 5/5 | 5/5 | MET |
| 3. Relevance gate refuses out-of-scope questions | At least 4/5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks are complete and understandable | At least 4/5 chunks | 5/5 | 5/5 | 5/5 | MET |
| 5. Named sources directly support the answers | At least 4/5 answers | 5/5 | 5/5 | 5/5 | MET |

For Criteria 3 and 4, the same deterministic gate check and fixed chunk sample were used in the three columns; these are **not** three independent model generations.

#### Actual output — before

The following are the actual answers from run 1, not rewritten summaries. Runs 2 and 3 are preserved in the raw results file.

**Innisfree Hall laundry:**

```text
At Innisfree Hall, laundry costs $1.75 for a wash and $1.75 for a dry (housing_innisfree_hall.txt and housing_innisfree_hall_laundry.txt).
```

**HIST 118 reading:**

```text
Students should expect about 120 pages of reading each week in HIST 118 (Source: course_hist_118.txt and course_hist_118_workload.txt).
```

**BIOL 160 unit tests:**

```text
There are four unit tests in BIOL 160 (Source: `course_biol_160.txt` and `course_biol_160_exams.txt`).
```

**Pellew Dining Hall wait:**

```text
The wait time at Pellew Dining Hall during peak hours is 12 to 18 minutes (dining_pellew_dining_hall.txt, dining_pellew_dining_hall_followup.txt).
```

**Course add deadline:**

```text
You can add a course through the end of the second week (admin_add_drop_deadline.txt).
```

**Gate evidence:** `run_eval.py::check_out_of_scope` refused all five unrelated questions:

| Out-of-scope question | Best distance | Gate |
|---|---:|---|
| Capital of Mongolia | 0.825 | Refused |
| Changing oil in a diesel engine | 0.934 | Refused |
| Winner of the 1994 World Cup | 0.886 | Refused |
| Ibuprofen dosage for a headache | 0.844 | Refused |
| Writing a Rust `for` loop | 0.896 | Refused |

**Chunk evidence:** `app.py::cmd_chunks` printed five complete posts from `chunker.py::split_documents`; the full text and sources are shown in **Sample Chunks** above.

### Verdicts

All five original acceptance criteria were **MET** in the baseline. The retrieved chunks contained the answers to all five questions. All 15 generated answers named sources, and at least one named source supported each answer. The gate refused all five unrelated questions. All five sampled chunks were understandable by themselves.

I did not lower or rewrite the original targets in `criteria.md` to fit the results.

### Diagnoses

There were no confirmed misses against the five acceptance criteria, so I did not invent a failed criterion. The small, focused corpus and complete-post chunks helped the original system retrieve the necessary facts.

One limitation of the test design is that the five questions contain clear course codes, building names, or campus rules, and the answers appear directly in the documents. A harder test set could include paraphrases, ambiguous questions, and questions that need evidence from more than one document.

I chose to investigate the **retrieval stage**, because semantic similarity alone may not always prioritize exact names and identifiers. This was a possible improvement area, not a proven baseline failure.

### The Improvement

I changed **one pipeline component**: `store.py::search`.

Before, retrieval ranked chunks using only Chroma's semantic similarity. After, retrieval combined semantic ranking with BM25 keyword ranking using **Reciprocal Rank Fusion (RRF)**. I kept the original cosine distances on each result so `gate.py::check` could continue applying the same 0.6 relevance cutoff.

I did **not** change the corpus, chunker, embedding model, five questions, top-k, or cutoff. This makes the before-and-after comparison a test of retrieval ranking.

### Run Log — After

**Command:** `python run_eval.py --label after`  
**Date:** October 8, 2026, 00:07  
**Raw evidence:** The timestamped `*_after.md` file in `results/`  
**Produced by:** `run_eval.py::main`  
**Retrieval:** `store.py::search` with semantic + BM25 ranking  
**Chunking:** `chunker.py::split_documents`

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | At least 4/5 questions | 5/5 | 5/5 | 5/5 | MET |
| 2. Every generated answer names a source | 5/5 answers | 5/5 | 5/5 | 5/5 | MET |
| 3. Relevance gate refuses out-of-scope questions | At least 4/5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks are complete and understandable | At least 4/5 chunks | 5/5 | 5/5 | 5/5 | MET |
| 5. Named sources directly support the answers | At least 4/5 answers | 5/5 | 5/5 | 5/5 | MET |

As in the before table, Criteria 3 and 4 were deterministic checks, not separate generated answers.

#### Actual output — after

The following are the actual answers from run 1. Runs 2 and 3 are preserved in the raw after-results file.

**Innisfree Hall laundry:**

```text
It costs $1.75 to wash and $1.75 to dry at Innisfree Hall (from *housing_innisfree_hall_laundry.txt* and *housing_innisfree_hall.txt*).
```

**HIST 118 reading:**

```text
Students should expect about 120 pages of reading each week in HIST 118 (Source: course_hist_118.txt and course_hist_118_workload.txt).
```

**BIOL 160 unit tests:**

```text
There are four unit tests in BIOL 160 (from `course_biol_160.txt`, `course_biol_160_exams.txt`).
```

**Pellew Dining Hall wait:**

```text
The wait time at Pellew Dining Hall during peak hours is 12 to 18 minutes.

Source: `dining_pellew_dining_hall.txt` (also mentioned in `dining_pellew_dining_hall_followup.txt`)
```

**Course add deadline:**

```text
You can add a course through the end of the second week (admin_add_drop_deadline.txt).
```

**Gate evidence:** `run_eval.py::check_out_of_scope` again refused all five unrelated questions:

| Out-of-scope question | Best distance | Gate |
|---|---:|---|
| Capital of Mongolia | 0.869 | Refused |
| Changing oil in a diesel engine | 0.934 | Refused |
| Winner of the 1994 World Cup | 0.886 | Refused |
| Ibuprofen dosage for a headache | 0.860 | Refused |
| Writing a Rust `for` loop | 0.900 | Refused |

The five original chunks were unchanged because the chunking strategy was not modified.

### Before and After Comparison

| Measurement | Before | After |
|---|---|---|
| In-scope questions with correct answers | 5/5 in each run | 5/5 in each run |
| Answers naming sources | 5/5 in each run | 5/5 in each run |
| Out-of-scope refusals | 5/5 | 5/5 |
| Standalone sampled chunks | 5/5 | 5/5 |
| Answers supported by named sources | 5/5 in each run | 5/5 in each run |

Hybrid retrieval changed which documents appeared in the top five, but **did not improve the measured scores** because the original system already met every target. Some newly retrieved documents were not closely related to the question. For example, the BIOL 160 search included `housing_tamsin_court.txt`, and the course add-deadline search included `transit_shuttle.txt`.

This experiment shows a change in ranking, **not a demonstrated gain in answer quality**.

### What's Still Broken

No acceptance criterion failed in these tests, but there are still limitations:

- The five in-scope questions are a small sample and may be easier than real student questions.
- Hybrid search sometimes includes unrelated chunks in the top five, which could distract generation on harder questions.
- The relevance gate uses the minimum cosine distance among the returned chunks. Hybrid ranking can change which chunks are returned, so it can also affect the gate's decision.
- BM25 is built from the indexed documents during each search; this may be inefficient for a much larger corpus.

I stopped after one measured change to keep the experiment focused and avoid making unsupported claims about improvement.

### What I'd Do Differently

I would build a larger test set with harder paraphrases, questions needing multiple sources, and questions with similar-looking but incorrect documents. I would also measure **retrieval precision**, not just whether one correct chunk appeared in the top five.

I would test different fusion settings only in a separate experiment. I would also consider precomputing the BM25 index rather than rebuilding it for every question.

The main lesson is that a more complicated retrieval method is not automatically better. Testing before and after the change made it possible to report the result accurately.

## How I Used AI

I used AI assistance to understand the RAG pipeline, review code changes, interpret the evaluation output, and organize the README. I ran the commands in my own project environment and used the actual generated answers, retrieved sources, and test logs as evidence. The reported scores are based on those observed results, not invented test runs.

## Project Files and Evidence

| File | Purpose |
|---|---|
| `config.py` | Corpus, embedding, top-k, and cutoff settings |
| `chunker.py` | Complete-post chunking |
| `store.py` | Chroma indexing and hybrid retrieval |
| `gate.py` | Relevance decision using cosine distances |
| `generate.py` | Grounded answer generation |
| `questions.py` | In-scope and out-of-scope test questions |
| `criteria.md` | Original five acceptance criteria |
| `run_eval.py` | Repeated evaluation and raw result logs |
| `results/` | Before and after evidence files |

The project uses the same repository for both units. The raw results files should be committed alongside the README so the evaluation can be checked independently.
