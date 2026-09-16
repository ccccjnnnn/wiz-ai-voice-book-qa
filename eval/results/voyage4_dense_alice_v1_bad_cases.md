# Dense retrieval bad cases

- Dataset: `alice-in-wonderland-v1`
- Model: `voyage-4`
- Failure threshold: top 5 chunks
- Failed questions: 2 / 30

This report attributes likely causes for inspection; it does not apply automatic fixes.

## q010: bad_chunk_boundary

**Question:** What caused Alice to start shrinking while she was talking to the Mouse?

**Expected pages:** 21

**Reason:** expected page retrieved but one or more evidence phrases are outside selected chunks

| Rank | Chunk | Pages | Cosine score |
|---:|---|---|---:|
| 1 | `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00060` | 40 | 0.598821 |
| 2 | `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00029` | 22 | 0.592546 |
| 3 | `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00019` | 16 | 0.591335 |
| 4 | `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00028` | 21, 22 | 0.589562 |
| 5 | `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00043` | 31, 32 | 0.589402 |
| 6 | `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00026` | 21 | 0.576703 |
| 7 | `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00050` | 34, 35 | 0.575924 |
| 8 | `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00051` | 35 | 0.573709 |
| 9 | `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00027` | 21, 22 | 0.568508 |
| 10 | `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00089` | 56 | 0.556644 |

## q021: insufficient_retrieval_depth

**Question:** What did the Duchess's baby turn into?

**Expected pages:** 48

**Reason:** missing expected page first appears at rank 8

| Rank | Chunk | Pages | Cosine score |
|---:|---|---|---:|
| 1 | `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00072` | 46 | 0.471659 |
| 2 | `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00071` | 45, 46 | 0.420311 |
| 3 | `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00070` | 45 | 0.395930 |
| 4 | `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00069` | 44, 45 | 0.378390 |
| 5 | `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00104` | 64, 65, 66, 67 | 0.376184 |
| 6 | `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00073` | 46, 47 | 0.371741 |
| 7 | `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00074` | 47 | 0.365144 |
| 8 | `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00077` | 48, 49 | 0.358624 |
| 9 | `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00024` | 20 | 0.354418 |
| 10 | `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00108` | 68, 69 | 0.347433 |
