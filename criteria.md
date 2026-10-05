# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1 **before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something a person could plainly observe. "Retrieval works" is an opinion. "For at least 4 of my 5 test questions, the top results include a chunk containing the answer" is a criterion.

Under each one, write a sentence or two on **why that target** and not a stricter or looser one. A reason that says something about your corpus or your pipeline earns credit; "80% seemed reasonable" does not.

> Missing your own targets next unit costs you nothing. Setting a target so easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that contains the answer.

**Why this target:**  
My `campus_life` corpus covers many different topics, including housing, dining, classes, and registration. Because the questions cover different topics, I expect retrieval to be reliable, but I do not expect every question to be a perfect match. Getting at least 4 out of 5 shows that the system can find useful information across different campus topics while still allowing one question to be more difficult.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**  
The system uses retrieved campus documents to answer questions, so a user should be able to see where the information came from. I chose every answer instead of 4 out of 5 because the retrieved documents are already available to the generation step. If the system gives an answer, I expect it to identify at least one source every time so the answer can be checked.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate stops it and the system returns "I don't have enough information about that" — in at least 4 of 5 tries.

**Why this target:**  
The `campus_life` corpus is about student and campus life, so the system should not try to answer unrelated general-knowledge questions using campus documents. I chose 4 out of 5 because similarity search may occasionally find an accidental match between an unrelated question and a document. The gate should still reject most questions that are clearly outside the corpus.

---

## 4. Sampled chunks are complete and understandable on their own

For at least 4 of 5 sampled chunks, the chunk should contain a complete thought and be understandable without needing to read another chunk before or after it.

**Why this target:**  
The `campus_life` documents are short posts that usually focus on one main topic, so keeping the important information together is important for retrieval. I chose 4 out of 5 because most short posts should work well as standalone chunks, but I want to allow for one post that may depend more on context or contain information that is harder to understand by itself.

---

## 5. The named source actually supports the answer

For at least 4 of my 5 test questions that receive an answer, at least one source named by the system should contain information that directly supports the answer.

**Why this target:**  
Simply naming a source is not enough if that source does not support what the system says. I want the source attribution to be useful so a user can check the document and find evidence for the answer. I chose 4 out of 5 because retrieval and generation may not always select the best supporting document, but the source should be correct for most of the test questions.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->