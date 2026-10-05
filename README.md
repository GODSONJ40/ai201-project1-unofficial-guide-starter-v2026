# The Unofficial Guide

**Name:** Kimberly Edme
**Corpus:** `campus_life`

---

# Unit 1

## What This Does

The Unofficial Guide is a RAG system that answers questions using information from the `campus_life` corpus. I chose this corpus because it contains information about different parts of student life, including housing, dining, classes, registration, transportation, campus jobs, and other student resources. The system searches the documents for information related to a question and uses the information it finds to create an answer. It also uses a relevance gate so it can refuse questions when the documents do not have enough information to answer them.

## Chunking Strategy

**Chunk size:** 1 complete document / post per chunk
**Overlap:** none

The `campus_life` corpus contains 88 short documents. When I looked through the documents, I noticed that most of them are short and focus on one main topic. Important information is usually found in one sentence or a short paragraph. Because the documents are already short, most of them can stay together as one complete chunk without splitting important information into different pieces.

The current chunking results produced 88 chunks from 88 documents. Looking at the five sample chunks, each chunk can be understood without needing to read another chunk before or after it. For example, the Innisfree Hall chunk keeps the room setup, air conditioning, laundry cost, and noise information together. This makes sense for this corpus because the individual documents are already small.

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::fallback_split`

```text
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160.txt#0` — produced by: `chunker.py::fallback_split`

```text
BIOL 160 Cell Biology

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3** — source: `course_hist_118_workload.txt#0` — produced by: `chunker.py::fallback_split`

```text
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `dining_pellew_dining_hall_followup.txt#0` — produced by: `chunker.py::fallback_split`

```text
Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_innisfree_hall.txt#0` — produced by: `chunker.py::fallback_split`

```text
Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.
```

## Sample Answer

**Question:** Is the housing lottery random?

**Answer:**

```text
ClientError: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}
```

**My relevance cutoff:** To be finalized after testing all ten questions.

The current relevance cutoff is `0.6`. When I tested the question, "is the housing lottery random?", the best retrieval distance was `0.254`, which passed the current `0.6` cutoff. This showed that the retrieval part of the RAG system was finding a close match for the question.

I will choose the final relevance cutoff after comparing five questions that the `campus_life` corpus can answer with five questions that are clearly outside the corpus. Lower distances mean the retrieved information is a closer match. I will compare the two groups and choose a cutoff in the gap between the relevant and unrelated questions.

| Question | In corpus? | Best distance |
|---|---|---:|
| Is the housing lottery random? | Yes | 0.254 |
| [Test question 2] | Yes | [ACTUAL DISTANCE] |
| [Test question 3] | Yes | [ACTUAL DISTANCE] |
| [Test question 4] | Yes | [ACTUAL DISTANCE] |
| [Test question 5] | Yes | [ACTUAL DISTANCE] |
| [Out-of-scope question 1] | No | [ACTUAL DISTANCE] |
| [Out-of-scope question 2] | No | [ACTUAL DISTANCE] |
| [Out-of-scope question 3] | No | [ACTUAL DISTANCE] |
| [Out-of-scope question 4] | No | [ACTUAL DISTANCE] |
| [Out-of-scope question 5] | No | [ACTUAL DISTANCE] |

## How I Used AI

**1.** I used AI to help troubleshoot my Gemini API connection. My RAG system was retrieving information, but the model call returned an `API_KEY_INVALID` error. AI helped me use a safe command to check what API key my project was loading without showing the complete key. The result showed that the loaded value was only 13 characters long, started with `your`, and ended with `here`. This helped me discover that the program was still reading the placeholder API key instead of my actual Gemini API key. I used that information to correct the API key in my `.env` file.

**2.** I used AI to help me understand the output from my chunking command. I ran `python app.py chunks -n 5` myself and gave AI the actual results. AI helped me review whether the chunks could be understood by themselves and organize the real chunk text, source files, and `chunker.py::fallback_split` function into the README. I kept the actual results produced by my program instead of using made-up chunk results.
<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
