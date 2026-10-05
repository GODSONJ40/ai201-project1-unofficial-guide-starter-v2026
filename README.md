# The Unofficial Guide

**Name:** Godson JEAN
**Corpus:** `campus_life`

---

# Unit 1

## What This Does

The Unofficial Guide is a RAG system that answers questions using information from the campus_life corpus. I chose this corpus because it contains information about different parts of student life, including housing, dining, classes, registration, transportation, campus jobs, and other student resources.

The system searches the documents for information related to a question and uses the information it finds to create an answer. It also uses a relevance gate so it can refuse questions when the documents do not have enough information to answer them.

## Chunking Strategy

**Chunk size:** 1 complete document / post per chunk
**Overlap:** none

The campus_life corpus contains 88 short documents. When I looked through the documents, I noticed that most of them are short and focus on one main topic. Important information is usually found in one sentence or a short paragraph.

Because the documents are already short, I decided to keep each complete document or post together as one chunk instead of splitting it into fixed-size pieces. I did not use overlap because each short post already contains enough context to stand on its own.

After indexing the corpus with this strategy, the system loaded 88 documents containing 27,908 characters and produced 88 chunks. The average chunk was 317 characters, the shortest was 178 characters, and the longest was 549 characters.

Looking at the sample chunks below, each chunk can be understood without needing to read another chunk before or after it. This strategy keeps related information together while avoiding unnecessary overlap.

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

**Question:** How much does it cost to do laundry at Innisfree Hall?

**Answer:**

```text
ClientError: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}
```

**My relevance cutoff:**  0.6

I tested five questions that should be answered by the campus_life corpus and five questions that are clearly outside the corpus.

The highest best distance for an in-scope question was 0.3701. The lowest best distance for an out-of-scope question was 0.8246. This created a clear gap between the relevant and unrelated questions.

I kept the relevance cutoff at 0.6 because it falls inside this gap. All five in-scope questions had best distances below 0.6, so they passed the relevance gate. All five out-of-scope questions had best distances above 0.6, so the system refused them.

This means the cutoff successfully separated all 5 in-scope questions from all 5 out-of-scope questions in my Milestone 4 testing.

| Question | In corpus? | Best distance |
|---|---|---:|
| How much does it cost to do laundry at Innisfree Hall? | Yes | 0.1817 |
| What is the number of pages of reading should students expect each week in HIST 118? | Yes | 0.3622 |
| What is the total unit tests are there in BIOL 160? | Yes | 0.2819 |
| How long would someone wait at Pellew Dining Hall during peak hours? | Yes | 0.1875 |
| When is the last day to add a course? | Yes | 0.3701 |
| What is the capital of Mongolia? | No | 0.8246 |
| How do I change the oil in a diesel engine? | No | 0.9340 |
| Who won the 1994 World Cup? | No | 0.8859 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8442 |
| How do I write a for loop in Rust? | No | 0.8960 |

The in-scope distances ranged from 0.1817 to 0.3701, while the out-of-scope distances ranged from 0.8246 to 0.9340. Since lower distances represent closer matches, these results support using 0.6 as my relevance cutoff.

## How I Used AI

1. API troubleshooting

I used AI to help troubleshoot my Gemini API connection. My RAG system was retrieving information correctly, but the model call returned an API_KEY_INVALID error.

AI helped me use a safe command to check which API key the project was loading without displaying the complete key. The test showed that the loaded value was only 13 characters long and was still the placeholder value. This helped me identify that the program was reading the placeholder API key instead of a valid Gemini API key.

I used the troubleshooting information to identify what needed to be corrected in my .env file. I did not share the complete API key.

2. Chunking strategy

I used AI while reviewing the starter chunking strategy and the actual structure of my campus_life corpus. The corpus contained 88 short documents, and the starter fixed-size chunker also produced 88 chunks because most documents were already shorter than the default window.

After reviewing the documents and sample chunks, I decided that a better intentional strategy for this corpus was to keep each complete short post as one chunk with no overlap. I changed split_documents() to implement this strategy.

I then ran the index again myself and verified that the final implementation produced 88 chunks with an average length of 317 characters, a shortest chunk of 178 characters, and a longest chunk of 549 characters.

I also ran python app.py chunks -n 5 and used the actual output from my program for the five Sample Chunks above instead of creating made-up examples.

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
