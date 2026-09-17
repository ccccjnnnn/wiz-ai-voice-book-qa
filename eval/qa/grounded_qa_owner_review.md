# Grounded QA Owner Review: Contextual Evidence

**Purpose:** final human semantic sign-off against the frozen QA outputs, using only the locally parsed page/chunk data.

**Review state:** all owner fields are intentionally blank. This document does not change any evaluation result, score, prompt, retrieval output, or frozen configuration.

## What this review does and does not establish

- **Citation contract validity is not semantic citation correctness.** A syntactically valid source ID can still point to text that does not support the claim.
- **Matching a canonical page label is not semantic citation correctness.** Duplicate, adjacent, or alternate valid passages can occur on other pages, while a labeled page can still be semantically wrong.
- **Retrieval absence is not document absence.** A fact missing from top-k evidence cannot justify `insufficient_evidence` by itself.
- **Isolated sentence support is not contextual support.** Pronouns, speaker identity, negation, quotation, hypotheticals, mistaken statements, and scene boundaries must be checked in surrounding text.

For each answered case, every material answer claim maps to one or more cited source IDs and exact source substrings. Each source context block is shown once per case and names the claims it supports; that cross-reference supplies the full cited chunk and its immediate predecessor/successor for every mapped claim without duplicating the same book text repeatedly.

## Whole-document negative verification protocol

Use this whenever the system returns `insufficient_evidence` for a user question:

**Two-layer meaning:** the runtime status means the answer is not supportable from the evidence made available to the model. It must not be presented as proof that the fact is absent from the book. A stronger owner statement—“no support found in the parsed book”—requires the independent whole-document procedure below. If that check is not run or finds a plausible hit, user-facing wording should remain “I could not find enough evidence,” not “the book does not contain it.”

1. Verify the local parse is reviewable: document state is `ready`, expected pages are present, and no stored page is empty.
2. Search **all parsed pages**, independently of retrieval rank, for the key entity, requested relation, exact phrase, morphological variants, and reasonable lexical synonyms/paraphrases.
3. Inspect every narrow-term hit in its original page context. For broad/noisy terms, record every hit location and inspect all hits; do not infer support from keyword overlap.
4. Check entity–relation co-occurrence, negation, speaker, quotation, and whether the hit actually supplies the requested value.
5. Conclude only one of: **no supporting evidence found in parsed book** or **potentially present / needs manual inspection**. A parsed-text search is strong review evidence, not mathematical proof of absence; OCR gaps, extraction defects, images, and unanticipated wording remain possible failure modes.
6. If any plausible support is found, do not sign off the no-answer. Escalate to manual inspection of the page and adjacent pages, then add the case to regression coverage.

### Local corpus coverage used for this review

- Document: `alice-in-wonderland.pdf` (`a6c315f78fbb4c5cb9f16f08f28aed38`)
- Ingestion status: `ready`
- Stored pages: 92 / declared 92; empty stored pages: 0
- Stored chunks: 148 / declared 148
- Parsed page characters: 155,319
- Search boundary: extracted text only. Images/OCR and facts absent from the uploaded edition are outside this check.

## Frozen-input provenance

| Frozen file | SHA-256 at review time |
|---|---|
| `eval/qa/grounded_qa_dev.json` | `95e2374839949f342647faa24c8a63bd2ab8a9c93108df1a4823cc235aff60eb` |
| `eval/qa/grounded_qa_challenge.json` | `dda39fbc20dcde4fe8a4abcab77eac91601323ccf7498e3351088a7a2c4a1e24` |
| `eval/qa/grounded_qa_test.json` | `a5d8e964214f930fa92ad5923615f92a5847267c83735ad9f18ecda70a91f4a3` |
| `eval/qa/grounded_qa_config.json` | `50084cc36e55e2a7b7b46c14f40640323e5e1bf8e3f8e43ff0c6fef8864940e5` |

## Owner-attention flags from context

- **q027:** the full cited chunk includes “retire in same order,” but the generated answer omits that action. This is the same completeness issue already marked partial in the prior assisted review; it is not a new contradiction.
- No surrounding context reviewed here newly contradicts or weakens the other prior assisted assessments. Owner sign-off remains required for every case below.

# DEV cases

## q001

**Question:** Who wrote Alice's Adventures in Wonderland?

**Reference answer:** Lewis Carroll.

**Final generated answer:** Lewis Carroll wrote Alice's Adventures in Wonderland.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** Lewis Carroll is the author of Alice’s Adventures in Wonderland.
- **Source ID(s):** `S2`
- **Cited page(s):** S2: 8, 9, 10, 11
- **Exact supporting span(s):**
  - `S2`:

```text
ALICE’S ADVENTURES IN
WONDERLAND

Lewis Carroll
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S2 context — supports claim(s) C1

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00010`
- Cited page(s): 8, 9, 10, 11
- Parsed chunk page range: 8–11

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00009` (pages 8–8)

```text
achine readable binary, compressed, mark-up, or proprietary form, including any form resulting from conversion by word pro- cessing or hypertext software, but only so long as *EITHER*:

(a) The etext, when displayed, is clearly readable, and does *not* contain characters other than those intended by the author of the work, although tilde, asterisk (*) and underline ( ) characters may be used to convey punctuation intended by the author, and additional characters may be used to indicate hypertext links; OR

(b) The etext may be readily converted by the reader at no expense into plain ASCII, EBCDIC or equivalent form by the program that displays the etext (as is the case, for instance, with most word processors); OR

(c) You provide, or agree to also provide on request at no additional cost, fee or expense, a copy of the etext in its original plain ASCII form (or in EBCDIC or other equivalent proprietary form).

2. Honor the etext refund and replacement provisions of this “Small Print!” statement.

3. Pay a trademark license fee to the Project of 20net profits you derive calculated using the method you already use to calculate your applicable taxes. If you don’t derive profits, no ro
```

**Full original cited chunk:**

```text
Project of 20net profits you derive calculated using the method you already use to calculate your applicable taxes. If you don’t derive profits, no royalty is due. Royalties are payable to “Project Gutenberg Association/Carnegie-Mellon University” within the 60 days following each date you prepare (or were legally required to prepare) your annual (or equivalent periodic) tax return.

WHAT IF YOU *WANT* TO SEND MONEY EVEN IF YOU DON’T
HAVE TO?

The Project gratefully accepts contributions in money, time, scanning machines, OCR software, public domain etexts, royalty free copyright licenses, and every other sort of contribution you can think of. Money should be paid to “Project Gutenberg Association / Carnegie-Mellon University”.
We are planning on making some changes in our donation structure in
2000, so you might want to email me, hart@pobox.com beforehand.
*END THE SMALL PRINT! FOR PUBLIC DOMAIN ETEXTS*
Ver.04.29.93*END*

ALICE’S ADVENTURES IN
WONDERLAND

Lewis Carroll

THE MILLENNIUM FULCRUM EDITION 3.0

Contents

1 Down the Rabbit-Hole 13

2 The Pool of Tears 19

3 A Caucus-Race and a Long Tale 25

4 The Rabbit Sends in a Little Bill 31

5 Advice from a Caterpillar 37

6 Pig and
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00011` (pages 11–13)

```text
Hole 13

2 The Pool of Tears 19

3 A Caucus-Race and a Long Tale 25

4 The Rabbit Sends in a Little Bill 31

5 Advice from a Caterpillar 37

6 Pig and Pepper 43

7 A Mad Tea-Party 51

8 The Queen’s Croquet-Ground 59

9 The Mock Turtle’s Story 67

10 The Lobster Quadrille 73

11 Who Stole the Tarts? 81

12 Alice’s Evidence 87

12 CONTENTS

Chapter 1

Down the Rabbit-Hole

Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, ‘and what is the use of a book,’ thought Alice ‘without pictures or conversation?’
So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.
There was nothing so VERY remarkable in that; nor did Alice think it so
VERY much out of the way to hear the Rabbit say to itself, ‘Oh dear! Oh dear! I shall be late!’ (when she thought it over afterwards, it occurred to her that she
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q004

**Question:** What was disappointing about the orange marmalade jar?

**Reference answer:** It was empty.

**Final generated answer:** The orange marmalade jar was empty.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** The orange marmalade jar was empty.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 13, 14
- **Exact supporting span(s):**
  - `S1`:

```text
to her great disappointment it was empty
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S1 context — supports claim(s) C1

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00013`
- Cited page(s): 13, 14
- Parsed chunk page range: 13–14

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00012` (pages 13–14)

```text
t of the way to hear the Rabbit say to itself, ‘Oh dear! Oh dear! I shall be late!’ (when she thought it over afterwards, it occurred to her that she ought to have wondered at this, but at the time it all seemed quite natural); but when the Rabbit actually TOOK A WATCH OUT OF
ITS WAISTCOAT- POCKET, and looked at it, and then hurried on, Alice started to her feet, for it flashed across her mind that she had never before seen a rabbit with either a waistcoat-pocket, or a watch to take out of it, and burning with curiosity, she ran across the field after it, and fortunately was just in time to see it pop down a large rabbit-hole under the hedge.
In another moment down went Alice after it, never once considering how in the world she was to get out again.
The rabbit-hole went straight on like a tunnel for some way, and then dipped suddenly down, so suddenly that Alice had not a moment to think about stopping herself before she found herself falling down a very deep well.
Either the well was very deep, or she fell very slowly, for she had plenty of time as she went down to look about her and to wonder what was going

14 CHAPTER 1. DOWN THE RABBIT-HOLE

to happen next. First, she tried to
```

**Full original cited chunk:**

```text
lenty of time as she went down to look about her and to wonder what was going

14 CHAPTER 1. DOWN THE RABBIT-HOLE

to happen next. First, she tried to look down and make out what she was coming to, but it was too dark to see anything; then she looked at the sides of the well, and noticed that they were filled with cupboards and bookshelves; here and there she saw maps and pictures hung upon pegs. She took down a jar from one of the shelves as she passed; it was labelled ‘ORANGE
MARMALADE’, but to her great disappointment it was empty: she did not like to drop the jar for fear of killing somebody, so managed to put it into one of the cupboards as she fell past it.
‘Well!’ thought Alice to herself, ‘after such a fall as this, I shall think nothing of tumbling down stairs! How brave they’ll all think me at home!
Why, I wouldn’t say anything about it, even if I fell offthe top of the house!’
(Which was very likely true.)
Down, down, down. Would the fall NEVER come to an end! ‘I wonder how many miles I’ve fallen by this time?’ she said aloud. ‘I must be getting somewhere near the centre of the earth. Let me see: that would be four thousand miles down, I think–’ (for, you see, Alice had
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00014` (pages 14–14)

```text
ud. ‘I must be getting somewhere near the centre of the earth. Let me see: that would be four thousand miles down, I think–’ (for, you see, Alice had learnt several things of this sort in her lessons in the schoolroom, and though this was not a VERY good opportunity for showing offher knowledge, as there was no one to listen to her, still it was good practice to say it over) ‘–yes, that’s about the right distance–but then I wonder what Latitude or Longitude I’ve got to?’ (Alice had no idea what Latitude was, or Longitude either, but thought they were nice grand words to say.)
Presently she began again. ‘I wonder if I shall fall right THROUGH the earth! How funny it’ll seem to come out among the people that walk with their heads downward! The Antipathies, I think–’ (she was rather glad there
WAS no one listening, this time, as it didn’t sound at all the right word) ‘–but I shall have to ask them what the name of the country is, you know.
Please, Ma’am, is this New Zealand or Australia?’ (and she tried to curtsey as she spoke–fancy CURTSEYING as you’re falling through the air! Do you think you could manage it?) ‘And what an ignorant little girl she’ll think me for asking! No, it’ll n
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q005

**Question:** What was the name of Alice's cat?

**Reference answer:** Dinah.

**Final generated answer:** Alice's cat was named Dinah.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** Alice’s cat was named Dinah.
- **Source ID(s):** `S4`
- **Cited page(s):** S4: 14, 15
- **Exact supporting span(s):**
  - `S4`:

```text
Dinah was the cat
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S4 context — supports claim(s) C1

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00015`
- Cited page(s): 14, 15
- Parsed chunk page range: 14–15

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00014` (pages 14–14)

```text
ud. ‘I must be getting somewhere near the centre of the earth. Let me see: that would be four thousand miles down, I think–’ (for, you see, Alice had learnt several things of this sort in her lessons in the schoolroom, and though this was not a VERY good opportunity for showing offher knowledge, as there was no one to listen to her, still it was good practice to say it over) ‘–yes, that’s about the right distance–but then I wonder what Latitude or Longitude I’ve got to?’ (Alice had no idea what Latitude was, or Longitude either, but thought they were nice grand words to say.)
Presently she began again. ‘I wonder if I shall fall right THROUGH the earth! How funny it’ll seem to come out among the people that walk with their heads downward! The Antipathies, I think–’ (she was rather glad there
WAS no one listening, this time, as it didn’t sound at all the right word) ‘–but I shall have to ask them what the name of the country is, you know.
Please, Ma’am, is this New Zealand or Australia?’ (and she tried to curtsey as she spoke–fancy CURTSEYING as you’re falling through the air! Do you think you could manage it?) ‘And what an ignorant little girl she’ll think me for asking! No, it’ll n
```

**Full original cited chunk:**

```text
SEYING as you’re falling through the air! Do you think you could manage it?) ‘And what an ignorant little girl she’ll think me for asking! No, it’ll never do to ask: perhaps I shall see it written up somewhere.’
Down, down, down. There was nothing else to do, so Alice soon began talking again. ‘Dinah’ll miss me very much to-night, I should think!’ (Dinah was the cat.) ‘I hope they’ll remember her saucer of milk at tea-time. Dinah my dear! I wish you were down here with me! There are no mice in the air, I’m afraid, but you might catch a bat, and that’s very like a mouse, you know. But do cats eat bats, I wonder?’ And here Alice began to get rather

sleepy, and went on saying to herself, in a dreamy sort of way, ‘Do cats eat bats? Do cats eat bats?’ and sometimes, ‘Do bats eat cats?’ for, you see, as she couldn’t answer either question, it didn’t much matter which way she put it. She felt that she was dozing off, and had just begun to dream that she was walking hand in hand with Dinah, and saying to her very earnestly,
‘Now, Dinah, tell me the truth: did you ever eat a bat?’ when suddenly, thump! thump! down she came upon a heap of sticks and dry leaves, and the fall was over.
Alice
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00016` (pages 15–15)

```text
me the truth: did you ever eat a bat?’ when suddenly, thump! thump! down she came upon a heap of sticks and dry leaves, and the fall was over.
Alice was not a bit hurt, and she jumped up on to her feet in a moment:
she looked up, but it was all dark overhead; before her was another long passage, and the White Rabbit was still in sight, hurrying down it. There was not a moment to be lost: away went Alice like the wind, and was just in time to hear it say, as it turned a corner, ‘Oh my ears and whiskers, how late it’s getting!’ She was close behind it when she turned the corner, but the Rabbit was no longer to be seen: she found herself in a long, low hall, which was lit up by a row of lamps hanging from the roof.
There were doors all round the hall, but they were all locked; and when
Alice had been all the way down one side and up the other, trying every door, she walked sadly down the middle, wondering how she was ever to get out again.
Suddenly she came upon a little three-legged table, all made of solid glass;
there was nothing on it except a tiny golden key, and Alice’s first thought was that it might belong to one of the doors of the hall; but, alas! either the locks were too
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q007

**Question:** Which foods did Alice say the DRINK ME bottle tasted like?

**Reference answer:** Cherry tart, custard, pineapple, roast turkey, toffee, and hot buttered toast.

**Final generated answer:** Alice said the bottle tasted like cherry-tart, custard, pine-apple, roast turkey, toffee, and hot buttered toast.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** Alice said the bottle tasted like cherry-tart, custard, pine-apple, roast turkey, toffee, and hot buttered toast.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 16
- **Exact supporting span(s):**
  - `S1`:

```text
mixed flavour of cherrytart, custard, pine-apple, roast turkey, toffee, and hot buttered toast
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S1 context — supports claim(s) C1

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00019`
- Cited page(s): 16
- Parsed chunk page range: 16–16

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00018` (pages 15–16)

```text
many out-of-the-way things had happened lately, that Alice had begun to think that very few things indeed were really impossible.

16 CHAPTER 1. DOWN THE RABBIT-HOLE

There seemed to be no use in waiting by the little door, so she went back to the table, half hoping she might find another key on it, or at any rate a book of rules for shutting people up like telescopes: this time she found a little bottle on it, (‘which certainly was not here before,’ said Alice,) and round the neck of the bottle was a paper label, with the words ‘DRINK ME’ beautifully printed on it in large letters.
It was all very well to say ‘Drink me,’ but the wise little Alice was not going to do THAT in a hurry. ‘No, I’ll look first,’ she said, ‘and see whether it’s marked “poison” or not’; for she had read several nice little histories about children who had got burnt, and eaten up by wild beasts and other unpleasant things, all because they WOULD not remember the simple rules their friends had taught them: such as, that a red-hot poker will burn you if you hold it too long; and that if you cut your finger VERY deeply with a knife, it usually bleeds; and she had never forgotten that, if you drink much from a
```

**Full original cited chunk:**

```text
it too long; and that if you cut your finger VERY deeply with a knife, it usually bleeds; and she had never forgotten that, if you drink much from a bottle marked ‘poison,’ it is almost certain to disagree with you, sooner or later.
However, this bottle was NOT marked ‘poison,’ so Alice ventured to taste it, and finding it very nice, (it had, in fact, a sort of mixed flavour of cherrytart, custard, pine-apple, roast turkey, toffee, and hot buttered toast,) she very soon finished it off.
‘What a curious feeling!’ said Alice; ‘I must be shutting up like a telescope.’
And so it was indeed: she was now only ten inches high, and her face brightened up at the thought that she was now the right size for going through the little door into that lovely garden. First, however, she waited for a few minutes to see if she was going to shrink any further: she felt a little nervous about this; ‘for it might end, you know,’ said Alice to herself, ‘in my going out altogether, like a candle. I wonder what I should be like then?’ And she tried to fancy what the flame of a candle is like after the candle is blown out, for she could not remember ever having seen such a thing.
After a while, finding tha
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00020` (pages 16–17)

```text
what the flame of a candle is like after the candle is blown out, for she could not remember ever having seen such a thing.
After a while, finding that nothing more happened, she decided on going into the garden at once; but, alas for poor Alice! when she got to the door, she found she had forgotten the little golden key, and when she went back to the table for it, she found she could not possibly reach it: she could see it quite plainly through the glass, and she tried her best to climb up one of the legs of the table, but it was too slippery; and when she had tired herself out with trying, the poor little thing sat down and cried.
‘Come, there’s no use in crying like that!’ said Alice to herself, rather

sharply; ‘I advise you to leave offthis minute!’ She generally gave herself very good advice, (though she very seldom followed it), and sometimes she scolded herself so severely as to bring tears into her eyes; and once she remembered trying to box her own ears for having cheated herself in a game of croquet she was playing against herself, for this curious child was very fond of pretending to be two people. ‘But it’s no use now,’ thought poor Alice, ‘to pretend to be two people!
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q008

**Question:** What words were marked in currants on the cake?

**Reference answer:** EAT ME.

**Final generated answer:** The words marked in currants on the cake were 'EAT ME'.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** The cake was marked “EAT ME” in currants.
- **Source ID(s):** `S3`
- **Cited page(s):** S3: 17, 18, 19
- **Exact supporting span(s):**
  - `S3`:

```text
words ‘EAT ME’ were beautifully marked in currants
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S3 context — supports claim(s) C1

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00021`
- Cited page(s): 17, 18, 19
- Parsed chunk page range: 17–19

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00020` (pages 16–17)

```text
what the flame of a candle is like after the candle is blown out, for she could not remember ever having seen such a thing.
After a while, finding that nothing more happened, she decided on going into the garden at once; but, alas for poor Alice! when she got to the door, she found she had forgotten the little golden key, and when she went back to the table for it, she found she could not possibly reach it: she could see it quite plainly through the glass, and she tried her best to climb up one of the legs of the table, but it was too slippery; and when she had tired herself out with trying, the poor little thing sat down and cried.
‘Come, there’s no use in crying like that!’ said Alice to herself, rather

sharply; ‘I advise you to leave offthis minute!’ She generally gave herself very good advice, (though she very seldom followed it), and sometimes she scolded herself so severely as to bring tears into her eyes; and once she remembered trying to box her own ears for having cheated herself in a game of croquet she was playing against herself, for this curious child was very fond of pretending to be two people. ‘But it’s no use now,’ thought poor Alice, ‘to pretend to be two people!
```

**Full original cited chunk:**

```text
herself, for this curious child was very fond of pretending to be two people. ‘But it’s no use now,’ thought poor Alice, ‘to pretend to be two people! Why, there’s hardly enough of me left to make ONE respectable person!’
Soon her eye fell on a little glass box that was lying under the table: she opened it, and found in it a very small cake, on which the words ‘EAT ME’ were beautifully marked in currants. ‘Well, I’ll eat it,’ said Alice, ‘and if it makes me grow larger, I can reach the key; and if it makes me grow smaller,
I can creep under the door; so either way I’ll get into the garden, and I don’t care which happens!’
She ate a little bit, and said anxiously to herself, ‘Which way? Which way?’, holding her hand on the top of her head to feel which way it was growing, and she was quite surprised to find that she remained the same size: to be sure, this generally happens when one eats cake, but Alice had got so much into the way of expecting nothing but out-of-the-way things to happen, that it seemed quite dull and stupid for life to go on in the common way.
So she set to work, and very soon finished offthe cake.

18 CHAPTER 1. DOWN THE RABBIT-HOLE

Chapter 2

The Pool of Tears
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00022` (pages 17–19)

```text
o go on in the common way.
So she set to work, and very soon finished offthe cake.

18 CHAPTER 1. DOWN THE RABBIT-HOLE

Chapter 2

The Pool of Tears

‘Curiouser and curiouser!’ cried Alice (she was so much surprised, that for the moment she quite forgot how to speak good English); ‘now I’m opening out like the largest telescope that ever was! Good-bye, feet!’ (for when she looked down at her feet, they seemed to be almost out of sight, they were getting so far off). ‘Oh, my poor little feet, I wonder who will put on your shoes and stockings for you now, dears? I’m sure I shan’t be able! I shall be a great deal too far offto trouble myself about you: you must manage the best way you can; –but I must be kind to them,’ thought Alice, ‘or perhaps they won’t walk the way I want to go! Let me see: I’ll give them a new pair of boots every Christmas.’
And she went on planning to herself how she would manage it. ‘They must go by the carrier,’ she thought; ‘and how funny it’ll seem, sending presents to one’s own feet! And how odd the directions will look!

ALICE’S RIGHT FOOT, ESQ.
HEARTHRUG,
NEAR THE FENDER,
(WITH ALICE’S LOVE).

Oh dear, what nonsense I’m talking!’
Just then her head struck
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q009

**Question:** How tall did Alice become, and how deep was the pool of tears?

**Reference answer:** Alice became more than nine feet tall, and the pool was about four inches deep.

**Final generated answer:** Alice became more than nine feet high, and the pool of tears was about four inches deep.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** Alice became more than nine feet high.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 19, 20
- **Exact supporting span(s):**
  - `S1`:

```text
more than nine feet high
```

#### Claim C2

- **Claim text:** The pool of tears was about four inches deep.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 19, 20
- **Exact supporting span(s):**
  - `S1`:

```text
about four inches deep
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S1 context — supports claim(s) C1, C2

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00023`
- Cited page(s): 19, 20
- Parsed chunk page range: 19–20

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00022` (pages 17–19)

```text
o go on in the common way.
So she set to work, and very soon finished offthe cake.

18 CHAPTER 1. DOWN THE RABBIT-HOLE

Chapter 2

The Pool of Tears

‘Curiouser and curiouser!’ cried Alice (she was so much surprised, that for the moment she quite forgot how to speak good English); ‘now I’m opening out like the largest telescope that ever was! Good-bye, feet!’ (for when she looked down at her feet, they seemed to be almost out of sight, they were getting so far off). ‘Oh, my poor little feet, I wonder who will put on your shoes and stockings for you now, dears? I’m sure I shan’t be able! I shall be a great deal too far offto trouble myself about you: you must manage the best way you can; –but I must be kind to them,’ thought Alice, ‘or perhaps they won’t walk the way I want to go! Let me see: I’ll give them a new pair of boots every Christmas.’
And she went on planning to herself how she would manage it. ‘They must go by the carrier,’ she thought; ‘and how funny it’ll seem, sending presents to one’s own feet! And how odd the directions will look!

ALICE’S RIGHT FOOT, ESQ.
HEARTHRUG,
NEAR THE FENDER,
(WITH ALICE’S LOVE).

Oh dear, what nonsense I’m talking!’
Just then her head struck
```

**Full original cited chunk:**

```text
will look!

ALICE’S RIGHT FOOT, ESQ.
HEARTHRUG,
NEAR THE FENDER,
(WITH ALICE’S LOVE).

Oh dear, what nonsense I’m talking!’
Just then her head struck against the roof of the hall: in fact she was now more than nine feet high, and she at once took up the little golden key and hurried offto the garden door.
Poor Alice! It was as much as she could do, lying down on one side, to look through into the garden with one eye; but to get through was more hopeless than ever: she sat down and began to cry again.

20 CHAPTER 2. THE POOL OF TEARS

‘You ought to be ashamed of yourself,’ said Alice, ‘a great girl like you,’ (she might well say this), ‘to go on crying in this way! Stop this moment,
I tell you!’ But she went on all the same, shedding gallons of tears, until there was a large pool all round her, about four inches deep and reaching half down the hall.

After a time she heard a little pattering of feet in the distance, and she hastily dried her eyes to see what was coming. It was the White Rabbit returning, splendidly dressed, with a pair of white kid gloves in one hand and a large fan in the other: he came trotting along in a great hurry, muttering to himself as he came, ‘Oh! the Duc
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00024` (pages 20–20)

```text
r of white kid gloves in one hand and a large fan in the other: he came trotting along in a great hurry, muttering to himself as he came, ‘Oh! the Duchess, the Duchess! Oh! won’t she be savage if I’ve kept her waiting!’ Alice felt so desperate that she was ready to ask help of any one; so, when the Rabbit came near her, she began, in a low, timid voice, ‘If you please, sir–’ The Rabbit started violently, dropped the white kid gloves and the fan, and skurried away into the darkness as hard as he could go.

Alice took up the fan and gloves, and, as the hall was very hot, she kept fanning herself all the time she went on talking: ‘Dear, dear! How queer everything is to-day! And yesterday things went on just as usual. I wonder if
I’ve been changed in the night? Let me think: was I the same when I got up this morning? I almost think I can remember feeling a little different. But if
I’m not the same, the next question is, Who in the world am I? Ah, THAT’S the great puzzle!’ And she began thinking over all the children she knew that were of the same age as herself, to see if she could have been changed for any of them.

‘I’m sure I’m not Ada,’ she said, ‘for her hair goes in such long rin
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q010

**Question:** What caused Alice to keep shrinking after she noticed that she had put on one of the Rabbit's gloves?

**Reference answer:** The Rabbit's fan she was holding.

**Final generated answer:** The fan she was holding caused Alice to keep shrinking.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** The fan Alice was holding caused her to keep shrinking.
- **Source ID(s):** `S2`
- **Cited page(s):** S2: 21, 22
- **Exact supporting span(s):**
  - `S2`:

```text
cause of this was the fan she was holding
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S2 context — supports claim(s) C1

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00027`
- Cited page(s): 21, 22
- Parsed chunk page range: 21–22

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00026` (pages 21–21)

```text
mprove his shining tail,
And pour the waters of the Nile
On every golden scale!

‘How cheerfully he seems to grin,
How neatly spread his claws,
And welcome little fishes in
With gently smiling jaws!’

‘I’m sure those are not the right words,’ said poor Alice, and her eyes filled with tears again as she went on, ‘I must be Mabel after all, and I shall have to go and live in that poky little house, and have next to no toys to play with, and oh! ever so many lessons to learn! No, I’ve made up my mind about it; if I’m Mabel, I’ll stay down here! It’ll be no use their putting their heads down and saying “Come up again, dear!” I shall only look up and say
“Who am I then? Tell me that first, and then, if I like being that person, I’ll come up: if not, I’ll stay down here till I’m somebody else”–but, oh dear!’ cried Alice, with a sudden burst of tears, ‘I do wish they WOULD put their heads down! I am so VERY tired of being all alone here!’
As she said this she looked down at her hands, and was surprised to see that she had put on one of the Rabbit’s little white kid gloves while she was talking. ‘How CAN I have done that?’ she thought. ‘I must be growing small again.’ She got up and went t
```

**Full original cited chunk:**

```text
abbit’s little white kid gloves while she was talking. ‘How CAN I have done that?’ she thought. ‘I must be growing small again.’ She got up and went to the table to measure herself by it, and found that, as nearly as she could guess, she was now about two feet high, and was going on shrinking rapidly: she soon found out that the cause of this was the fan she was holding, and she dropped it hastily, just in time to avoid shrinking away altogether.
‘That WAS a narrow escape!’ said Alice, a good deal frightened at the sudden change, but very glad to find herself still in existence; ‘and now for the garden!’ and she ran with all speed back to the little door: but, alas! the little door was shut again, and the little golden key was lying on the glass table as before, ‘and things are worse than ever,’ thought the poor child, ‘for
I never was so small as this before, never! And I declare it’s too bad, that it is!’
As she said these words her foot slipped, and in another moment, splash!
she was up to her chin in salt water. Her first idea was that she had somehow fallen into the sea, ‘and in that case I can go back by railway,’ she said to

22 CHAPTER 2. THE POOL OF TEARS

herself. (Alice
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00028` (pages 21–22)

```text
that she had somehow fallen into the sea, ‘and in that case I can go back by railway,’ she said to

22 CHAPTER 2. THE POOL OF TEARS

herself. (Alice had been to the seaside once in her life, and had come to the general conclusion, that wherever you go to on the English coast you find a number of bathing machines in the sea, some children digging in the sand with wooden spades, then a row of lodging houses, and behind them a railway station.) However, she soon made out that she was in the pool of tears which she had wept when she was nine feet high.
‘I wish I hadn’t cried so much!’ said Alice, as she swam about, trying to find her way out. ‘I shall be punished for it now, I suppose, by being drowned in my own tears! That WILL be a queer thing, to be sure! However, everything is queer to-day.’
Just then she heard something splashing about in the pool a little way off, and she swam nearer to make out what it was: at first she thought it must be a walrus or hippopotamus, but then she remembered how small she was now, and she soon made out that it was only a mouse that had slipped in like herself.
‘Would it be of any use, now,’ thought Alice, ‘to speak to this mouse?
Everything is so o
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q011

**Question:** Why did Alice address the Mouse in French?

**Reference answer:** She remembered that a French mouse had come over with William the Conqueror.

**Final generated answer:** Alice addressed the Mouse in French because she thought it might not understand English and speculated that it was a French mouse that had come over with William the Conqueror.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** Alice spoke French because she thought the Mouse might not understand English and might be a French mouse that came with William the Conqueror.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 22
- **Exact supporting span(s):**
  - `S1`:

```text
Perhaps it doesn’t understand English
```
  - `S1`:

```text
French mouse, come over with William the Conqueror
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S1 context — supports claim(s) C1

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00029`
- Cited page(s): 22
- Parsed chunk page range: 22–22

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00028` (pages 21–22)

```text
that she had somehow fallen into the sea, ‘and in that case I can go back by railway,’ she said to

22 CHAPTER 2. THE POOL OF TEARS

herself. (Alice had been to the seaside once in her life, and had come to the general conclusion, that wherever you go to on the English coast you find a number of bathing machines in the sea, some children digging in the sand with wooden spades, then a row of lodging houses, and behind them a railway station.) However, she soon made out that she was in the pool of tears which she had wept when she was nine feet high.
‘I wish I hadn’t cried so much!’ said Alice, as she swam about, trying to find her way out. ‘I shall be punished for it now, I suppose, by being drowned in my own tears! That WILL be a queer thing, to be sure! However, everything is queer to-day.’
Just then she heard something splashing about in the pool a little way off, and she swam nearer to make out what it was: at first she thought it must be a walrus or hippopotamus, but then she remembered how small she was now, and she soon made out that it was only a mouse that had slipped in like herself.
‘Would it be of any use, now,’ thought Alice, ‘to speak to this mouse?
Everything is so o
```

**Full original cited chunk:**

```text
t that it was only a mouse that had slipped in like herself.
‘Would it be of any use, now,’ thought Alice, ‘to speak to this mouse?
Everything is so out-of-the-way down here, that I should think very likely it can talk: at any rate, there’s no harm in trying.’ So she began: ‘O Mouse, do you know the way out of this pool? I am very tired of swimming about here, O Mouse!’ (Alice thought this must be the right way of speaking to a mouse: she had never done such a thing before, but she remembered having seen in her brother’s Latin Grammar, ‘A mouse–of a mouse–to a mouse–a mouse–O mouse!’) The Mouse looked at her rather inquisitively, and seemed to her to wink with one of its little eyes, but it said nothing.
‘Perhaps it doesn’t understand English,’ thought Alice; ‘I daresay it’s a
French mouse, come over with William the Conqueror.’ (For, with all her knowledge of history, Alice had no very clear notion how long ago anything had happened.) So she began again: ‘Ou est ma chatte?’ which was the first sentence in her French lesson-book. The Mouse gave a sudden leap out of the water, and seemed to quiver all over with fright. ‘Oh, I beg your pardon!’ cried Alice hastily, afraid that she ha
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00030` (pages 22–23)

```text
Mouse gave a sudden leap out of the water, and seemed to quiver all over with fright. ‘Oh, I beg your pardon!’ cried Alice hastily, afraid that she had hurt the poor animal’s feelings. ‘I quite forgot you didn’t like cats.’
‘Not like cats!’ cried the Mouse, in a shrill, passionate voice. ‘Would
YOU like cats if you were me?’
‘Well, perhaps not,’ said Alice in a soothing tone: ‘don’t be angry about it. And yet I wish I could show you our cat Dinah: I think you’d take a fancy to cats if you could only see her. She is such a dear quiet thing,’ Alice went on, half to herself, as she swam lazily about in the pool, ‘and she sits

purring so nicely by the fire, licking her paws and washing her face–and she is such a nice soft thing to nurse–and she’s such a capital one for catching mice–oh, I beg your pardon!’ cried Alice again, for this time the Mouse was bristling all over, and she felt certain it must be really offended. ‘We won’t talk about her any more if you’d rather not.’
‘We indeed!’ cried the Mouse, who was trembling down to the end of his tail. ‘As if I would talk on such a subject! Our family always HATED cats:
nasty, low, vulgar things! Don’t let me hear the name again!’
‘I wo
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q013

**Question:** What prizes did Alice and the other racers receive after the Caucus-race?

**Reference answer:** The others received comfits from Alice, and Alice received her own thimble from the Dodo.

**Final generated answer:** The other racers each received a comfit. Alice received a thimble.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** Each of the other racers received one comfit.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 26, 27
- **Exact supporting span(s):**
  - `S1`:

```text
handed them round as prizes
```
  - `S1`:

```text
There was exactly one a-piece all round
```

#### Claim C2

- **Claim text:** Alice received a thimble.
- **Source ID(s):** `S2`
- **Cited page(s):** S2: 27
- **Exact supporting span(s):**
  - `S2`:

```text
presented the thimble
```
  - `S2`:

```text
acceptance of this elegant thimble
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S1 context — supports claim(s) C1

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00036`
- Cited page(s): 26, 27
- Parsed chunk page range: 26–27

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00035` (pages 26–26)

```text
all.’
‘In that case,’ said the Dodo solemnly, rising to its feet, ‘I move that the meeting adjourn, for the immediate adoption of more energetic remedies–’
‘Speak English!’ said the Eaglet. ‘I don’t know the meaning of half those long words, and, what’s more, I don’t believe you do either!’ And the Eaglet bent down its head to hide a smile: some of the other birds tittered audibly.
‘What I was going to say,’ said the Dodo in an offended tone, ‘was, that the best thing to get us dry would be a Caucus-race.’
‘What IS a Caucus-race?’ said Alice; not that she wanted much to know, but the Dodo had paused as if it thought that SOMEBODY ought to speak, and no one else seemed inclined to say anything.
‘Why,’ said the Dodo, ‘the best way to explain it is to do it.’ (And, as you might like to try the thing yourself, some winter day, I will tell you how the Dodo managed it.)
First it marked out a race-course, in a sort of circle, (‘the exact shape doesn’t matter,’ it said,) and then all the party were placed along the course, here and there. There was no ‘One, two, three, and away,’ but they began running when they liked, and left offwhen they liked, so that it was not easy to know when the r
```

**Full original cited chunk:**

```text
re was no ‘One, two, three, and away,’ but they began running when they liked, and left offwhen they liked, so that it was not easy to know when the race was over. However, when they had been running half an hour or so, and were quite dry again, the Dodo suddenly called out ‘The race is over!’ and they all crowded round it, panting, and asking, ‘But who has won?’
This question the Dodo could not answer without a great deal of thought,

and it sat for a long time with one finger pressed upon its forehead (the position in which you usually see Shakespeare, in the pictures of him), while the rest waited in silence. At last the Dodo said, ‘EVERYBODY has won, and all must have prizes.’
‘But who is to give the prizes?’ quite a chorus of voices asked.
‘Why, SHE, of course,’ said the Dodo, pointing to Alice with one finger;
and the whole party at once crowded round her, calling out in a confused way, ‘Prizes! Prizes!’
Alice had no idea what to do, and in despair she put her hand in her pocket, and pulled out a box of comfits, (luckily the salt water had not got into it), and handed them round as prizes. There was exactly one a-piece all round.
‘But she must have a prize herself, you know,’
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00037` (pages 27–27)

```text
t water had not got into it), and handed them round as prizes. There was exactly one a-piece all round.
‘But she must have a prize herself, you know,’ said the Mouse.
‘Of course,’ the Dodo replied very gravely. ‘What else have you got in your pocket?’ he went on, turning to Alice.
‘Only a thimble,’ said Alice sadly.
‘Hand it over here,’ said the Dodo.
Then they all crowded round her once more, while the Dodo solemnly presented the thimble, saying ‘We beg your acceptance of this elegant thimble’;
and, when it had finished this short speech, they all cheered.
Alice thought the whole thing very absurd, but they all looked so grave that she did not dare to laugh; and, as she could not think of anything to say, she simply bowed, and took the thimble, looking as solemn as she could.
The next thing was to eat the comfits: this caused some noise and confusion, as the large birds complained that they could not taste theirs, and the small ones choked and had to be patted on the back. However, it was over at last, and they sat down again in a ring, and begged the Mouse to tell them something more.
‘You promised to tell me your history, you know,’ said Alice, ‘and why it is you hate–C and D,’
```

#### S2 context — supports claim(s) C2

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00037`
- Cited page(s): 27
- Parsed chunk page range: 27–27

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00036` (pages 26–27)

```text
re was no ‘One, two, three, and away,’ but they began running when they liked, and left offwhen they liked, so that it was not easy to know when the race was over. However, when they had been running half an hour or so, and were quite dry again, the Dodo suddenly called out ‘The race is over!’ and they all crowded round it, panting, and asking, ‘But who has won?’
This question the Dodo could not answer without a great deal of thought,

and it sat for a long time with one finger pressed upon its forehead (the position in which you usually see Shakespeare, in the pictures of him), while the rest waited in silence. At last the Dodo said, ‘EVERYBODY has won, and all must have prizes.’
‘But who is to give the prizes?’ quite a chorus of voices asked.
‘Why, SHE, of course,’ said the Dodo, pointing to Alice with one finger;
and the whole party at once crowded round her, calling out in a confused way, ‘Prizes! Prizes!’
Alice had no idea what to do, and in despair she put her hand in her pocket, and pulled out a box of comfits, (luckily the salt water had not got into it), and handed them round as prizes. There was exactly one a-piece all round.
‘But she must have a prize herself, you know,’
```

**Full original cited chunk:**

```text
t water had not got into it), and handed them round as prizes. There was exactly one a-piece all round.
‘But she must have a prize herself, you know,’ said the Mouse.
‘Of course,’ the Dodo replied very gravely. ‘What else have you got in your pocket?’ he went on, turning to Alice.
‘Only a thimble,’ said Alice sadly.
‘Hand it over here,’ said the Dodo.
Then they all crowded round her once more, while the Dodo solemnly presented the thimble, saying ‘We beg your acceptance of this elegant thimble’;
and, when it had finished this short speech, they all cheered.
Alice thought the whole thing very absurd, but they all looked so grave that she did not dare to laugh; and, as she could not think of anything to say, she simply bowed, and took the thimble, looking as solemn as she could.
The next thing was to eat the comfits: this caused some noise and confusion, as the large birds complained that they could not taste theirs, and the small ones choked and had to be patted on the back. However, it was over at last, and they sat down again in a ring, and begged the Mouse to tell them something more.
‘You promised to tell me your history, you know,’ said Alice, ‘and why it is you hate–C and D,’
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00038` (pages 27–29)

```text
ng, and begged the Mouse to tell them something more.
‘You promised to tell me your history, you know,’ said Alice, ‘and why it is you hate–C and D,’ she added in a whisper, half afraid that it would be offended again.
‘Mine is a long and a sad tale!’ said the Mouse, turning to Alice, and sighing.
‘It IS a long tail, certainly,’ said Alice, looking down with wonder at the
Mouse’s tail; ‘but why do you call it sad?’ And she kept on puzzling about it while the Mouse was speaking, so that her idea of the tale was something like this:–

28 CHAPTER 3. A CAUCUS-RACE AND A LONG TALE

‘Fury said to a mouse, That he met in the house,
“Let us both go to law: I will prosecute
YOU. –Come,
I’ll take no denial; We must have a trial: For really this morning I’ve nothing to do.”
Said the mouse to the cur, “Such a trial, dear Sir,
With
no jury or judge, would be wasting our breath.”
“I’ll be judge, I’ll be jury,”
Said
cunning old Fury:
“I’ll try the whole

cause, and condemn you to death.”’

‘You are not attending!’ said the Mouse to Alice severely. ‘What are you thinking of?’
‘I beg your pardon,’ said Alice very humbly: ‘you had got to the fifth bend, I think?’
‘I had NOT!’ cried the Mouse, sharpl
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q014

**Question:** What did the White Rabbit order 'Mary Ann' to fetch?

**Reference answer:** A pair of gloves and a fan.

**Final generated answer:** The White Rabbit ordered 'Mary Ann' to fetch a pair of gloves and a fan.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** The White Rabbit ordered “Mary Ann” to fetch a pair of gloves and a fan.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 31, 32
- **Exact supporting span(s):**
  - `S1`:

```text
Run home this moment, and fetch me a pair of gloves and a fan
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S1 context — supports claim(s) C1

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00042`
- Cited page(s): 31, 32
- Parsed chunk page range: 31–32

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00041` (pages 30–31)

```text
here, and I’m sure she’s the best cat in the world! Oh, my dear Dinah! I wonder if I shall ever see you any more!’ And here poor Alice began to cry again, for she felt very lonely and low-spirited. In a little while, however, she again heard a little pattering of footsteps in the distance, and she looked up eagerly, half hoping that the
Mouse had changed his mind, and was coming back to finish his story.

Chapter 4

The Rabbit Sends in a Little
Bill

It was the White Rabbit, trotting slowly back again, and looking anxiously about as it went, as if it had lost something; and she heard it muttering to itself ‘The Duchess! The Duchess! Oh my dear paws! Oh my fur and whiskers! She’ll get me executed, as sure as ferrets are ferrets! Where CAN I have dropped them, I wonder?’ Alice guessed in a moment that it was looking for the fan and the pair of white kid gloves, and she very good-naturedly began hunting about for them, but they were nowhere to be seen–everything seemed to have changed since her swim in the pool, and the great hall, with the glass table and the little door, had vanished completely.
Very soon the Rabbit noticed Alice, as she went hunting about, and called out to her in
```

**Full original cited chunk:**

```text
the glass table and the little door, had vanished completely.
Very soon the Rabbit noticed Alice, as she went hunting about, and called out to her in an angry tone, ‘Why, Mary Ann, what ARE you doing out here?
Run home this moment, and fetch me a pair of gloves and a fan! Quick, now!’
And Alice was so much frightened that she ran offat once in the direction it pointed to, without trying to explain the mistake it had made.
‘He took me for his housemaid,’ she said to herself as she ran. ‘How surprised he’ll be when he finds out who I am! But I’d better take him his fan and gloves–that is, if I can find them.’ As she said this, she came upon a neat little house, on the door of which was a bright brass plate with the name ‘W. RABBIT’ engraved upon it. She went in without knocking, and hurried upstairs, in great fear lest she should meet the real Mary Ann, and be turned out of the house before she had found the fan and gloves.
‘How queer it seems,’ Alice said to herself, ‘to be going messages for a rabbit! I suppose Dinah’ll be sending me on messages next!’ And she began

32 CHAPTER 4. THE RABBIT SENDS IN A LITTLE BILL

fancying the sort of thing that would happen: ‘“Miss Alice! Come h
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00043` (pages 31–32)

```text
on messages next!’ And she began

32 CHAPTER 4. THE RABBIT SENDS IN A LITTLE BILL

fancying the sort of thing that would happen: ‘“Miss Alice! Come here directly, and get ready for your walk!” “Coming in a minute, nurse! But I’ve got to see that the mouse doesn’t get out.” Only I don’t think,’ Alice went on, ‘that they’d let Dinah stop in the house if it began ordering people about like that!’
By this time she had found her way into a tidy little room with a table in the window, and on it (as she had hoped) a fan and two or three pairs of tiny white kid gloves: she took up the fan and a pair of the gloves, and was just going to leave the room, when her eye fell upon a little bottle that stood near the looking- glass. There was no label this time with the words
‘DRINK ME,’ but nevertheless she uncorked it and put it to her lips. ‘I know
SOMETHING interesting is sure to happen,’ she said to herself, ‘whenever
I eat or drink anything; so I’ll just see what this bottle does. I do hope it’ll make me grow large again, for really I’m quite tired of being such a tiny little thing!’
It did so indeed, and much sooner than she had expected: before she had drunk half the bottle, she found her
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q016

**Question:** What did the pebbles thrown through the window become, and what happened when Alice ate one?

**Reference answer:** They became little cakes, and eating one made Alice shrink.

**Final generated answer:** The pebbles turned into little cakes. When Alice ate one, she began shrinking directly.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** The pebbles turned into little cakes.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 34, 35
- **Exact supporting span(s):**
  - `S1`:

```text
pebbles were all turning into little cakes
```

#### Claim C2

- **Claim text:** After Alice ate one of the cakes, she began shrinking immediately.
- **Source ID(s):** `S5`
- **Cited page(s):** S5: 35
- **Exact supporting span(s):**
  - `S5`:

```text
began shrinking directly
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S1 context — supports claim(s) C1

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00050`
- Cited page(s): 34, 35
- Parsed chunk page range: 34–35

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00049` (pages 34–34)

```text
the chimney!’
‘Oh! So Bill’s got to come down the chimney, has he?’ said Alice to herself. ‘Shy, they seem to put everything upon Bill! I wouldn’t be in Bill’s place for a good deal: this fireplace is narrow, to be sure; but I THINK I can kick a little!’
She drew her foot as far down the chimney as she could, and waited till she heard a little animal (she couldn’t guess of what sort it was) scratching and scrambling about in the chimney close above her: then, saying to herself
‘This is Bill,’ she gave one sharp kick, and waited to see what would happen next.
The first thing she heard was a general chorus of ‘There goes Bill!’ then the Rabbit’s voice along–‘Catch him, you by the hedge!’ then silence, and then another confusion of voices–‘Hold up his head–Brandy now–Don’t choke him–How was it, old fellow? What happened to you? Tell us all about it!’
Last came a little feeble, squeaking voice, (‘That’s Bill,’ thought Alice,)
‘Well, I hardly know–No more, thank ye; I’m better now–but I’m a deal too flustered to tell you–all I know is, something comes at me like a Jack-in-thebox, and up I goes like a sky-rocket!’
‘So you did, old fellow!’ said the others.
‘We must burn the house down!’
```

**Full original cited chunk:**

```text
ething comes at me like a Jack-in-thebox, and up I goes like a sky-rocket!’
‘So you did, old fellow!’ said the others.
‘We must burn the house down!’ said the Rabbit’s voice; and Alice called

out as loud as she could, ‘If you do. I’ll set Dinah at you!’
There was a dead silence instantly, and Alice thought to herself, ‘I wonder what they WILL do next! If they had any sense, they’d take the roof off.’
After a minute or two, they began moving about again, and Alice heard the
Rabbit say, ‘A barrowful will do, to begin with.’
‘A barrowful of WHAT?’ thought Alice; but she had not long to doubt, for the next moment a shower of little pebbles came rattling in at the window, and some of them hit her in the face. ‘I’ll put a stop to this,’ she said to herself, and shouted out, ‘You’d better not do that again!’ which produced another dead silence.
Alice noticed with some surprise that the pebbles were all turning into little cakes as they lay on the floor, and a bright idea came into her head.
‘If I eat one of these cakes,’ she thought, ‘it’s sure to make SOME change in my size; and as it can’t possibly make me larger, it must make me smaller,
I suppose.’
So she swallowed one of the cakes,
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00051` (pages 35–35)

```text
sure to make SOME change in my size; and as it can’t possibly make me larger, it must make me smaller,
I suppose.’
So she swallowed one of the cakes, and was delighted to find that she began shrinking directly. As soon as she was small enough to get through the door, she ran out of the house, and found quite a crowd of little animals and birds waiting outside. The poor little Lizard, Bill, was in the middle, being held up by two guinea-pigs, who were giving it something out of a bottle. They all made a rush at Alice the moment she appeared; but she ran offas hard as she could, and soon found herself safe in a thick wood.
‘The first thing I’ve got to do,’ said Alice to herself, as she wandered about in the wood, ‘is to grow to my right size again; and the second thing is to find my way into that lovely garden. I think that will be the best plan.’
It sounded an excellent plan, no doubt, and very neatly and simply arranged; the only difficulty was, that she had not the smallest idea how to set about it; and while she was peering about anxiously among the trees, a little sharp bark just over her head made her look up in a great hurry.
An enormous puppy was looking down at her with larg
```

#### S5 context — supports claim(s) C2

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00051`
- Cited page(s): 35
- Parsed chunk page range: 35–35

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00050` (pages 34–35)

```text
ething comes at me like a Jack-in-thebox, and up I goes like a sky-rocket!’
‘So you did, old fellow!’ said the others.
‘We must burn the house down!’ said the Rabbit’s voice; and Alice called

out as loud as she could, ‘If you do. I’ll set Dinah at you!’
There was a dead silence instantly, and Alice thought to herself, ‘I wonder what they WILL do next! If they had any sense, they’d take the roof off.’
After a minute or two, they began moving about again, and Alice heard the
Rabbit say, ‘A barrowful will do, to begin with.’
‘A barrowful of WHAT?’ thought Alice; but she had not long to doubt, for the next moment a shower of little pebbles came rattling in at the window, and some of them hit her in the face. ‘I’ll put a stop to this,’ she said to herself, and shouted out, ‘You’d better not do that again!’ which produced another dead silence.
Alice noticed with some surprise that the pebbles were all turning into little cakes as they lay on the floor, and a bright idea came into her head.
‘If I eat one of these cakes,’ she thought, ‘it’s sure to make SOME change in my size; and as it can’t possibly make me larger, it must make me smaller,
I suppose.’
So she swallowed one of the cakes,
```

**Full original cited chunk:**

```text
sure to make SOME change in my size; and as it can’t possibly make me larger, it must make me smaller,
I suppose.’
So she swallowed one of the cakes, and was delighted to find that she began shrinking directly. As soon as she was small enough to get through the door, she ran out of the house, and found quite a crowd of little animals and birds waiting outside. The poor little Lizard, Bill, was in the middle, being held up by two guinea-pigs, who were giving it something out of a bottle. They all made a rush at Alice the moment she appeared; but she ran offas hard as she could, and soon found herself safe in a thick wood.
‘The first thing I’ve got to do,’ said Alice to herself, as she wandered about in the wood, ‘is to grow to my right size again; and the second thing is to find my way into that lovely garden. I think that will be the best plan.’
It sounded an excellent plan, no doubt, and very neatly and simply arranged; the only difficulty was, that she had not the smallest idea how to set about it; and while she was peering about anxiously among the trees, a little sharp bark just over her head made her look up in a great hurry.
An enormous puppy was looking down at her with larg
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00052` (pages 35–36)

```text
xiously among the trees, a little sharp bark just over her head made her look up in a great hurry.
An enormous puppy was looking down at her with large round eyes, and feebly stretching out one paw, trying to touch her. ‘Poor little thing!’ said
Alice, in a coaxing tone, and she tried hard to whistle to it; but she was terribly frightened all the time at the thought that it might be hungry, in which case it would be very likely to eat her up in spite of all her coaxing.
Hardly knowing what she did, she picked up a little bit of stick, and held it out to the puppy; whereupon the puppy jumped into the air offall its feet at once, with a yelp of delight, and rushed at the stick, and made believe to worry it; then Alice dodged behind a great thistle, to keep herself from being

36 CHAPTER 4. THE RABBIT SENDS IN A LITTLE BILL

run over; and the moment she appeared on the other side, the puppy made another rush at the stick, and tumbled head over heels in its hurry to get hold of it; then Alice, thinking it was very like having a game of play with a cart-horse, and expecting every moment to be trampled under its feet, ran round the thistle again; then the puppy began a series of short ch
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q017

**Question:** What different effects did the two sides of the mushroom have?

**Reference answer:** One side made Alice grow taller and the other made her grow shorter.

**Final generated answer:** One side of the mushroom makes you grow taller, and the other side makes you grow shorter.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** One side of the mushroom made Alice grow taller and the other made her grow shorter.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 40
- **Exact supporting span(s):**
  - `S1`:

```text
One side will make you grow taller, and the other side will make you grow shorter
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S1 context — supports claim(s) C1

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00060`
- Cited page(s): 40
- Parsed chunk page range: 40–40

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00059` (pages 39–40)

```text
ak.
‘What size do you want to be?’ it asked.
‘Oh, I’m not particular as to size,’ Alice hastily replied; ‘only one doesn’t like changing so often, you know.’
‘I DON’T know,’ said the Caterpillar.

40 CHAPTER 5. ADVICE FROM A CATERPILLAR

Alice said nothing: she had never been so much contradicted in her life before, and she felt that she was losing her temper.
‘Are you content now?’ said the Caterpillar.
‘Well, I should like to be a LITTLE larger, sir, if you wouldn’t mind,’ said Alice: ‘three inches is such a wretched height to be.’
‘It is a very good height indeed!’ said the Caterpillar angrily, rearing itself upright as it spoke (it was exactly three inches high).
‘But I’m not used to it!’ pleaded poor Alice in a piteous tone. And she thought of herself, ‘I wish the creatures wouldn’t be so easily offended!’
‘You’ll get used to it in time,’ said the Caterpillar; and it put the hookah into its mouth and began smoking again.
This time Alice waited patiently until it chose to speak again. In a minute or two the Caterpillar took the hookah out of its mouth and yawned once or twice, and shook itself. Then it got down offthe mushroom, and crawled away in the grass, merely remarking as
```

**Full original cited chunk:**

```text
okah out of its mouth and yawned once or twice, and shook itself. Then it got down offthe mushroom, and crawled away in the grass, merely remarking as it went, ‘One side will make you grow taller, and the other side will make you grow shorter.’
‘One side of WHAT? The other side of WHAT?’ thought Alice to herself.
‘Of the mushroom,’ said the Caterpillar, just as if she had asked it aloud;
and in another moment it was out of sight.
Alice remained looking thoughtfully at the mushroom for a minute, trying to make out which were the two sides of it; and as it was perfectly round, she found this a very difficult question. However, at last she stretched her arms round it as far as they would go, and broke offa bit of the edge with each hand.
‘And now which is which?’ she said to herself, and nibbled a little of the right-hand bit to try the effect: the next moment she felt a violent blow underneath her chin: it had struck her foot!
She was a good deal frightened by this very sudden change, but she felt that there was no time to be lost, as she was shrinking rapidly; so she set to work at once to eat some of the other bit. Her chin was pressed so closely against her foot, that there was ha
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00061` (pages 40–41)

```text
he was shrinking rapidly; so she set to work at once to eat some of the other bit. Her chin was pressed so closely against her foot, that there was hardly room to open her mouth; but she did it at last, and managed to swallow a morsel of the lefthand bit.
‘Come, my head’s free at last!’ said Alice in a tone of delight, which changed into alarm in another moment, when she found that her shoulders were nowhere to be found: all she could see, when she looked down, was an immense length of neck, which seemed to rise like a stalk out of a sea of green leaves that lay far below her.
‘What CAN all that green stuffbe?’ said Alice. ‘And where HAVE my

shoulders got to? And oh, my poor hands, how is it I can’t see you?’ She was moving them about as she spoke, but no result seemed to follow, except a little shaking among the distant green leaves.
As there seemed to be no chance of getting her hands up to her head, she tried to get her head down to them, and was delighted to find that her neck would bend about easily in any direction, like a serpent. She had just succeeded in curving it down into a graceful zigzag, and was going to dive in among the leaves, which she found to be nothing but th
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q019

**Question:** What invitation did the Fish-Footman deliver to the Duchess?

**Reference answer:** An invitation from the Queen to play croquet.

**Final generated answer:** An invitation from the Queen to play croquet.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** The Fish-Footman delivered an invitation from the Queen to play croquet.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 43
- **Exact supporting span(s):**
  - `S1`:

```text
An invitation from the Queen to play croquet
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S1 context — supports claim(s) C1

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00066`
- Cited page(s): 43
- Parsed chunk page range: 43–43

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00065` (pages 42–43)

```text
en at the other, and growing sometimes taller and sometimes shorter, until she had succeeded in bringing herself down to her usual height.
It was so long since she had been anything near the right size, that it felt quite strange at first; but she got used to it in a few minutes, and began talking to herself, as usual. ‘Come, there’s half my plan done now! How puzzling all these changes are! I’m never sure what I’m going to be, from one minute to another! However, I’ve got back to my right size: the next thing is, to get into that beautiful garden–how IS that to be done, I wonder?’
As she said this, she came suddenly upon an open place, with a little house in it about four feet high. ‘Whoever lives there,’ thought Alice, ‘it’ll never do to come upon them THIS size: why, I should frighten them out of their wits!’ So she began nibbling at the righthand bit again, and did not venture to go near the house till she had brought herself down to nine inches high.

Chapter 6

Pig and Pepper

For a minute or two she stood looking at the house, and wondering what to do next, when suddenly a footman in livery came running out of the wood–(she considered him to be a footman because he was in li
```

**Full original cited chunk:**

```text
and wondering what to do next, when suddenly a footman in livery came running out of the wood–(she considered him to be a footman because he was in livery: otherwise, judging by his face only, she would have called him a fish)–and rapped loudly at the door with his knuckles. It was opened by another footman in livery, with a round face, and large eyes like a frog; and both footmen, Alice noticed, had powdered hair that curled all over their heads. She felt very curious to know what it was all about, and crept a little way out of the wood to listen.
The Fish-Footman began by producing from under his arm a great letter, nearly as large as himself, and this he handed over to the other, saying, in a solemn tone, ‘For the Duchess. An invitation from the Queen to play croquet.’ The Frog-Footman repeated, in the same solemn tone, only changing the order of the words a little, ‘From the Queen. An invitation for the
Duchess to play croquet.’
Then they both bowed low, and their curls got entangled together.
Alice laughed so much at this, that she had to run back into the wood for fear of their hearing her; and when she next peeped out the Fish-Footman was gone, and the other was sitting on t
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00067` (pages 43–44)

```text
he had to run back into the wood for fear of their hearing her; and when she next peeped out the Fish-Footman was gone, and the other was sitting on the ground near the door, staring stupidly up into the sky.
Alice went timidly up to the door, and knocked.
‘There’s no sort of use in knocking,’ said the Footman, ‘and that for two reasons. First, because I’m on the same side of the door as you are;
secondly, because they’re making such a noise inside, no one could possibly hear you.’ And certainly there was a most extraordinary noise going on within–a constant howling and sneezing, and every now and then a great

44 CHAPTER 6. PIG AND PEPPER

crash, as if a dish or kettle had been broken to pieces.
‘Please, then,’ said Alice, ‘how am I to get in?’
‘There might be some sense in your knocking,’ the Footman went on without attending to her, ‘if we had the door between us. For instance, if you were INSIDE, you might knock, and I could let you out, you know.’
He was looking up into the sky all the time he was speaking, and this Alice thought decidedly uncivil. ‘But perhaps he can’t help it,’ she said to herself;
‘his eyes are so VERY nearly at the top of his head. But at any rate he might
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q021

**Question:** What did the Duchess's baby turn into?

**Reference answer:** A pig.

**Final generated answer:** The Duchess's baby turned into a pig.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** The Duchess’s baby turned into a pig.
- **Source ID(s):** `S7`, `S8`
- **Cited page(s):** S7: 47; S8: 48, 49
- **Exact supporting span(s):**
  - `S7`:

```text
it was neither more nor less than a pig
```
  - `S8`:

```text
It turned into a pig
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S7 context — supports claim(s) C1

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00074`
- Cited page(s): 47
- Parsed chunk page range: 47–47

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00073` (pages 46–47)

```text
ulty, as it was a queer- shaped little creature, and held out its arms and legs in all directions, ‘just like a star-fish,’ thought Alice. The poor little thing was snorting like a steam-engine when she caught it, and kept doubling itself up and straightening itself out again, so that altogether, for the first minute or two, it was as much as she could do to hold it.
As soon as she had made out the proper way of nursing it, (which was to twist it up into a sort of knot, and then keep tight hold of its right ear and

left foot, so as to prevent its undoing itself,) she carried it out into the open air. ‘IF I don’t take this child away with me,’ thought Alice, ‘they’re sure to kill it in a day or two: wouldn’t it be murder to leave it behind?’ She said the last words out loud, and the little thing grunted in reply (it had left off sneezing by this time). ‘Don’t grunt,’ said Alice; ‘that’s not at all a proper way of expressing yourself.’
The baby grunted again, and Alice looked very anxiously into its face to see what was the matter with it. There could be no doubt that it had a
VERY turn-up nose, much more like a snout than a real nose; also its eyes were getting extremely small for
```

**Full original cited chunk:**

```text
it. There could be no doubt that it had a
VERY turn-up nose, much more like a snout than a real nose; also its eyes were getting extremely small for a baby: altogether Alice did not like the look of the thing at all. ‘But perhaps it was only sobbing,’ she thought, and looked into its eyes again, to see if there were any tears.
No, there were no tears. ‘If you’re going to turn into a pig, my dear,’ said Alice, seriously, ‘I’ll have nothing more to do with you. Mind now!’ The poor little thing sobbed again (or grunted, it was impossible to say which), and they went on for some while in silence.
Alice was just beginning to think to herself, ‘Now, what am I to do with this creature when I get it home?’ when it grunted again, so violently, that she looked down into its face in some alarm. This time there could be NO mistake about it: it was neither more nor less than a pig, and she felt that it would be quite absurd for her to carry it further.
So she set the little creature down, and felt quite relieved to see it trot away quietly into the wood. ‘If it had grown up,’ she said to herself, ‘it would have made a dreadfully ugly child: but it makes rather a handsome pig, I think.’ And she
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00075` (pages 47–48)

```text
he wood. ‘If it had grown up,’ she said to herself, ‘it would have made a dreadfully ugly child: but it makes rather a handsome pig, I think.’ And she began thinking over other children she knew, who might do very well as pigs, and was just saying to herself, ‘if one only knew the right way to change them–’ when she was a little startled by seeing the Cheshire
Cat sitting on a bough of a tree a few yards off.
The Cat only grinned when it saw Alice. It looked good- natured, she thought: still it had VERY long claws and a great many teeth, so she felt that it ought to be treated with respect.
‘Cheshire Puss,’ she began, rather timidly, as she did not at all know whether it would like the name: however, it only grinned a little wider.
‘Come, it’s pleased so far,’ thought Alice, and she went on. ‘Would you tell me, please, which way I ought to go from here?’
‘That depends a good deal on where you want to get to,’ said the Cat.
‘I don’t much care where–’ said Alice.
‘Then it doesn’t matter which way you go,’ said the Cat.

48 CHAPTER 6. PIG AND PEPPER

‘–so long as I get SOMEWHERE,’ Alice added as an explanation.
‘Oh, you’re sure to do that,’ said the Cat, ‘if you only walk long enough.
```

#### S8 context — supports claim(s) C1

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00077`
- Cited page(s): 48, 49
- Parsed chunk page range: 48–49

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00076` (pages 48–48)

```text
G AND PEPPER

‘–so long as I get SOMEWHERE,’ Alice added as an explanation.
‘Oh, you’re sure to do that,’ said the Cat, ‘if you only walk long enough.’
Alice felt that this could not be denied, so she tried another question.
‘What sort of people live about here?’
‘In THAT direction,’ the Cat said, waving its right paw round, ‘lives a
Hatter: and in THAT direction,’ waving the other paw, ‘lives a March Hare.
Visit either you like: they’re both mad.’
‘But I don’t want to go among mad people,’ Alice remarked.
‘Oh, you can’t help that,’ said the Cat: ‘we’re all mad here. I’m mad.
You’re mad.’
‘How do you know I’m mad?’ said Alice.
‘You must be,’ said the Cat, ‘or you wouldn’t have come here.’
Alice didn’t think that proved it at all; however, she went on ‘And how do you know that you’re mad?’
‘To begin with,’ said the Cat, ‘a dog’s not mad. You grant that?’
‘I suppose so,’ said Alice.
‘Well, then,’ the Cat went on, ‘you see, a dog growls when it’s angry, and wags its tail when it’s pleased. Now I growl when I’m pleased, and wag my tail when I’m angry. Therefore I’m mad.’
‘I call it purring, not growling,’ said Alice.
‘Call it what you like,’ said the Cat. ‘Do you play croquet with the
```

**Full original cited chunk:**

```text
en I’m angry. Therefore I’m mad.’
‘I call it purring, not growling,’ said Alice.
‘Call it what you like,’ said the Cat. ‘Do you play croquet with the Queen to-day?’
‘I should like it very much,’ said Alice, ‘but I haven’t been invited yet.’
‘You’ll see me there,’ said the Cat, and vanished.
Alice was not much surprised at this, she was getting so used to queer things happening. While she was looking at the place where it had been, it suddenly appeared again.
‘By-the-bye, what became of the baby?’ said the Cat. ‘I’d nearly forgotten to ask.’
‘It turned into a pig,’ Alice quietly said, just as if it had come back in a natural way.
‘I thought it would,’ said the Cat, and vanished again.
Alice waited a little, half expecting to see it again, but it did not appear, and after a minute or two she walked on in the direction in which the March
Hare was said to live. ‘I’ve seen hatters before,’ she said to herself; ‘the
March Hare will be much the most interesting, and perhaps as this is May it won’t be raving mad–at least not so mad as it was in March.’ As she said

this, she looked up, and there was the Cat again, sitting on a branch of a tree.
‘Did you say pig, or fig?’ said the Cat.
‘I s
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00078` (pages 48–51)

```text
in March.’ As she said

this, she looked up, and there was the Cat again, sitting on a branch of a tree.
‘Did you say pig, or fig?’ said the Cat.
‘I said pig,’ replied Alice; ‘and I wish you wouldn’t keep appearing and vanishing so suddenly: you make one quite giddy.’
‘All right,’ said the Cat; and this time it vanished quite slowly, beginning with the end of the tail, and ending with the grin, which remained some time after the rest of it had gone.
‘Well! I’ve often seen a cat without a grin,’ thought Alice; ‘but a grin without a cat! It’s the most curious thing I ever saw in my life!’
She had not gone much farther before she came in sight of the house of the
March Hare: she thought it must be the right house, because the chimneys were shaped like ears and the roof was thatched with fur. It was so large a house, that she did not like to go nearer till she had nibbled some more of the lefthand bit of mushroom, and raised herself to about two feet high:
even then she walked up towards it rather timidly, saying to herself ‘Suppose it should be raving mad after all! I almost wish I’d gone to see the Hatter instead!’

50 CHAPTER 6. PIG AND PEPPER

Chapter 7

A Mad Tea-Party

There was
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q022

**Question:** Who was at the tea table, and what beverage did the March Hare falsely offer Alice?

**Reference answer:** The March Hare, Hatter, and Dormouse were there; the March Hare offered wine even though there was none.

**Final generated answer:** The March Hare, the Hatter, and the Dormouse were at the tea table. The March Hare falsely offered Alice wine.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** The March Hare, the Hatter, and the Dormouse were at the tea table.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 49, 50, 51
- **Exact supporting span(s):**
  - `S1`:

```text
Hare and the Hatter were having tea
```
  - `S1`:

```text
a Dormouse was sitting between them
```

#### Claim C2

- **Claim text:** The March Hare offered Alice wine even though there was none.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 49, 50, 51
- **Exact supporting span(s):**
  - `S1`:

```text
Have some wine
```
  - `S1`:

```text
There isn’t any
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S1 context — supports claim(s) C1, C2

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00079`
- Cited page(s): 49, 50, 51
- Parsed chunk page range: 49–51

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00078` (pages 48–51)

```text
in March.’ As she said

this, she looked up, and there was the Cat again, sitting on a branch of a tree.
‘Did you say pig, or fig?’ said the Cat.
‘I said pig,’ replied Alice; ‘and I wish you wouldn’t keep appearing and vanishing so suddenly: you make one quite giddy.’
‘All right,’ said the Cat; and this time it vanished quite slowly, beginning with the end of the tail, and ending with the grin, which remained some time after the rest of it had gone.
‘Well! I’ve often seen a cat without a grin,’ thought Alice; ‘but a grin without a cat! It’s the most curious thing I ever saw in my life!’
She had not gone much farther before she came in sight of the house of the
March Hare: she thought it must be the right house, because the chimneys were shaped like ears and the roof was thatched with fur. It was so large a house, that she did not like to go nearer till she had nibbled some more of the lefthand bit of mushroom, and raised herself to about two feet high:
even then she walked up towards it rather timidly, saying to herself ‘Suppose it should be raving mad after all! I almost wish I’d gone to see the Hatter instead!’

50 CHAPTER 6. PIG AND PEPPER

Chapter 7

A Mad Tea-Party

There was
```

**Full original cited chunk:**

```text
ould be raving mad after all! I almost wish I’d gone to see the Hatter instead!’

50 CHAPTER 6. PIG AND PEPPER

Chapter 7

A Mad Tea-Party

There was a table set out under a tree in front of the house, and the March
Hare and the Hatter were having tea at it: a Dormouse was sitting between them, fast asleep, and the other two were using it as a cushion, resting their elbows on it, and talking over its head. ‘Very uncomfortable for the
Dormouse,’ thought Alice; ‘only, as it’s asleep, I suppose it doesn’t mind.’
The table was a large one, but the three were all crowded together at one corner of it: ‘No room! No room!’ they cried out when they saw Alice coming. ‘There’s PLENTY of room!’ said Alice indignantly, and she sat down in a large arm-chair at one end of the table.
‘Have some wine,’ the March Hare said in an encouraging tone.
Alice looked all round the table, but there was nothing on it but tea. ‘I don’t see any wine,’ she remarked.
‘There isn’t any,’ said the March Hare.
‘Then it wasn’t very civil of you to offer it,’ said Alice angrily.
‘It wasn’t very civil of you to sit down without being invited,’ said the
March Hare.
‘I didn’t know it was YOUR table,’ said Alice; ‘it’s lai
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00080` (pages 51–52)

```text
ngrily.
‘It wasn’t very civil of you to sit down without being invited,’ said the
March Hare.
‘I didn’t know it was YOUR table,’ said Alice; ‘it’s laid for a great many more than three.’
‘Your hair wants cutting,’ said the Hatter. He had been looking at Alice for some time with great curiosity, and this was his first speech.
‘You should learn not to make personal remarks,’ Alice said with some severity; ‘it’s very rude.’
The Hatter opened his eyes very wide on hearing this; but all he SAID was, ‘Why is a raven like a writing-desk?’

52 CHAPTER 7. A MAD TEA-PARTY

‘Come, we shall have some fun now!’ thought Alice. ‘I’m glad they’ve begun asking riddles.–I believe I can guess that,’ she added aloud.
‘Do you mean that you think you can find out the answer to it?’ said the
March Hare.
‘Exactly so,’ said Alice.
‘Then you should say what you mean,’ the March Hare went on.
‘I do,’ Alice hastily replied; ‘at least–at least I mean what I say–that’s the same thing, you know.’
‘Not the same thing a bit!’ said the Hatter. ‘You might just as well say that “I see what I eat” is the same thing as “I eat what I see”!’
‘You might just as well say,’ added the March Hare, ‘that “I like what I get” is
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q023

**Question:** Why was it always tea-time at the Hatter's table?

**Reference answer:** Time had stopped at six o'clock, so it was always tea-time.

**Final generated answer:** It was always tea-time because the Hatter had quarreled with Time. After the Hatter sang at the Queen's concert, she accused him of murdering time and ordered his execution. Since then, Time refuses to do anything for the Hatter, leaving the clock stuck at six o'clock, which is tea-time.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** The Hatter had quarrelled with Time.
- **Source ID(s):** `S2`
- **Cited page(s):** S2: 53, 54
- **Exact supporting span(s):**
  - `S2`:

```text
We quarrelled last March
```

#### Claim C2

- **Claim text:** At the Queen’s concert, the Queen accused the Hatter of murdering time and ordered his execution.
- **Source ID(s):** `S2`, `S1`
- **Cited page(s):** S2: 53, 54; S1: 54
- **Exact supporting span(s):**
  - `S2`:

```text
great concert given by the Queen of Hearts
```
  - `S1`:

```text
He’s murdering the time! Offwith his head!
```

#### Claim C3

- **Claim text:** After that, Time would do nothing for the Hatter, so the clock remained at six o’clock and it was always tea-time.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 54
- **Exact supporting span(s):**
  - `S1`:

```text
he won’t do a thing I ask! It’s always six o’clock now
```
  - `S1`:

```text
it’s always tea-time
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S2 context — supports claim(s) C1, C2

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00084`
- Cited page(s): 53, 54
- Parsed chunk page range: 53–54

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00083` (pages 53–53)

```text
upon its nose.
The Dormouse shook its head impatiently, and said, without opening its eyes, ‘Of course, of course; just what I was going to remark myself.’
‘Have you guessed the riddle yet?’ the Hatter said, turning to Alice again.
‘No, I give it up,’ Alice replied: ‘what’s the answer?’
‘I haven’t the slightest idea,’ said the Hatter.
‘Nor I,’ said the March Hare.
Alice sighed wearily. ‘I think you might do something better with the time,’ she said, ‘than waste it in asking riddles that have no answers.’
‘If you knew Time as well as I do,’ said the Hatter, ‘you wouldn’t talk about wasting IT. It’s HIM.’
‘I don’t know what you mean,’ said Alice.
‘Of course you don’t!’ the Hatter said, tossing his head contemptuously.
‘I dare say you never even spoke to Time!’
‘Perhaps not,’ Alice cautiously replied: ‘but I know I have to beat time when I learn music.’
‘Ah! that accounts for it,’ said the Hatter. ‘He won’t stand beating. Now, if you only kept on good terms with him, he’d do almost anything you liked with the clock. For instance, suppose it were nine o’clock in the morning, just time to begin lessons: you’d only have to whisper a hint to Time, and round goes the clock in a twinkling!
```

**Full original cited chunk:**

```text
e it were nine o’clock in the morning, just time to begin lessons: you’d only have to whisper a hint to Time, and round goes the clock in a twinkling! Half-past one, time for dinner!’
(‘I only wish it was,’ the March Hare said to itself in a whisper.)
‘That would be grand, certainly,’ said Alice thoughtfully: ‘but then–I shouldn’t be hungry for it, you know.’
‘Not at first, perhaps,’ said the Hatter: ‘but you could keep it to half-past one as long as you liked.’
‘Is that the way YOU manage?’ Alice asked.
The Hatter shook his head mournfully. ‘Not I!’ he replied. ‘We quarrelled last March–just before HE went mad, you know–’ (pointing with his tea spoon at the March Hare,) ‘–it was at the great concert given by the Queen of Hearts, and I had to sing

“Twinkle, twinkle, little bat!

54 CHAPTER 7. A MAD TEA-PARTY

How I wonder what you’re at!”

You know the song, perhaps?’
‘I’ve heard something like it,’ said Alice.
‘It goes on, you know,’ the Hatter continued, ‘in this way:–

“Up above the world you fly,
Like a tea-tray in the sky.
Twinkle, twinkle–”’

Here the Dormouse shook itself, and began singing in its sleep ‘Twinkle, twinkle, twinkle, twinkle–’ and went on so long that they had
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00085` (pages 54–54)

```text
le, twinkle–”’

Here the Dormouse shook itself, and began singing in its sleep ‘Twinkle, twinkle, twinkle, twinkle–’ and went on so long that they had to pinch it to make it stop.
‘Well, I’d hardly finished the first verse,’ said the Hatter, ‘when the Queen jumped up and bawled out, “He’s murdering the time! Offwith his head!”’
‘How dreadfully savage!’ exclaimed Alice.
‘And ever since that,’ the Hatter went on in a mournful tone, ‘he won’t do a thing I ask! It’s always six o’clock now.’
A bright idea came into Alice’s head. ‘Is that the reason so many teathings are put out here?’ she asked.
‘Yes, that’s it,’ said the Hatter with a sigh: ‘it’s always tea-time, and we’ve no time to wash the things between whiles.’
‘Then you keep moving round, I suppose?’ said Alice.
‘Exactly so,’ said the Hatter: ‘as the things get used up.’
‘But what happens when you come to the beginning again?’ Alice ventured to ask.
‘Suppose we change the subject,’ the March Hare interrupted, yawning.
‘I’m getting tired of this. I vote the young lady tells us a story.’
‘I’m afraid I don’t know one,’ said Alice, rather alarmed at the proposal.
‘Then the Dormouse shall!’ they both cried. ‘Wake up, Dormouse!’ And th
```

#### S1 context — supports claim(s) C2, C3

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00085`
- Cited page(s): 54
- Parsed chunk page range: 54–54

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00084` (pages 53–54)

```text
e it were nine o’clock in the morning, just time to begin lessons: you’d only have to whisper a hint to Time, and round goes the clock in a twinkling! Half-past one, time for dinner!’
(‘I only wish it was,’ the March Hare said to itself in a whisper.)
‘That would be grand, certainly,’ said Alice thoughtfully: ‘but then–I shouldn’t be hungry for it, you know.’
‘Not at first, perhaps,’ said the Hatter: ‘but you could keep it to half-past one as long as you liked.’
‘Is that the way YOU manage?’ Alice asked.
The Hatter shook his head mournfully. ‘Not I!’ he replied. ‘We quarrelled last March–just before HE went mad, you know–’ (pointing with his tea spoon at the March Hare,) ‘–it was at the great concert given by the Queen of Hearts, and I had to sing

“Twinkle, twinkle, little bat!

54 CHAPTER 7. A MAD TEA-PARTY

How I wonder what you’re at!”

You know the song, perhaps?’
‘I’ve heard something like it,’ said Alice.
‘It goes on, you know,’ the Hatter continued, ‘in this way:–

“Up above the world you fly,
Like a tea-tray in the sky.
Twinkle, twinkle–”’

Here the Dormouse shook itself, and began singing in its sleep ‘Twinkle, twinkle, twinkle, twinkle–’ and went on so long that they had
```

**Full original cited chunk:**

```text
le, twinkle–”’

Here the Dormouse shook itself, and began singing in its sleep ‘Twinkle, twinkle, twinkle, twinkle–’ and went on so long that they had to pinch it to make it stop.
‘Well, I’d hardly finished the first verse,’ said the Hatter, ‘when the Queen jumped up and bawled out, “He’s murdering the time! Offwith his head!”’
‘How dreadfully savage!’ exclaimed Alice.
‘And ever since that,’ the Hatter went on in a mournful tone, ‘he won’t do a thing I ask! It’s always six o’clock now.’
A bright idea came into Alice’s head. ‘Is that the reason so many teathings are put out here?’ she asked.
‘Yes, that’s it,’ said the Hatter with a sigh: ‘it’s always tea-time, and we’ve no time to wash the things between whiles.’
‘Then you keep moving round, I suppose?’ said Alice.
‘Exactly so,’ said the Hatter: ‘as the things get used up.’
‘But what happens when you come to the beginning again?’ Alice ventured to ask.
‘Suppose we change the subject,’ the March Hare interrupted, yawning.
‘I’m getting tired of this. I vote the young lady tells us a story.’
‘I’m afraid I don’t know one,’ said Alice, rather alarmed at the proposal.
‘Then the Dormouse shall!’ they both cried. ‘Wake up, Dormouse!’ And th
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00086` (pages 54–55)

```text
y.’
‘I’m afraid I don’t know one,’ said Alice, rather alarmed at the proposal.
‘Then the Dormouse shall!’ they both cried. ‘Wake up, Dormouse!’ And they pinched it on both sides at once.
The Dormouse slowly opened his eyes. ‘I wasn’t asleep,’ he said in a hoarse, feeble voice: ‘I heard every word you fellows were saying.’
‘Tell us a story!’ said the March Hare.
‘Yes, please do!’ pleaded Alice.
‘And be quick about it,’ added the Hatter, ‘or you’ll be asleep again before it’s done.’

‘Once upon a time there were three little sisters,’ the Dormouse began in a great hurry; ‘and their names were Elsie, Lacie, and Tillie; and they lived at the bottom of a well–’
‘What did they live on?’ said Alice, who always took a great interest in questions of eating and drinking.
‘They lived on treacle,’ said the Dormouse, after thinking a minute or two.
‘They couldn’t have done that, you know,’ Alice gently remarked; ‘they’d have been ill.’
‘So they were,’ said the Dormouse; ‘VERY ill.’
Alice tried to fancy to herself what such an extraordinary ways of living would be like, but it puzzled her too much, so she went on: ‘But why did they live at the bottom of a well?’
‘Take some more tea,’ the March H
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q025

**Question:** According to the Duchess, under what condition does everything have a moral?

**Reference answer:** If only you can find it.

**Final generated answer:** According to the Duchess, everything has a moral if only you can find it.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** According to the Duchess, everything has a moral if one can find it.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 67, 68
- **Exact supporting span(s):**
  - `S1`:

```text
Everything’s got a moral, if only you can find it
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S1 context — supports claim(s) C1

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00105`
- Cited page(s): 67, 68
- Parsed chunk page range: 67–68

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00104` (pages 64–67)

```text
t he was gone, and, by the time he had come back with the Duchess, it had entirely disappeared; so the

King and the executioner ran wildly up and down looking for it, while the rest of the party went back to the game.

66 CHAPTER 8. THE QUEEN’S CROQUET-GROUND

Chapter 9

The Mock Turtle’s Story

‘You can’t think how glad I am to see you again, you dear old thing!’ said the
Duchess, as she tucked her arm affectionately into Alice’s, and they walked offtogether.
Alice was very glad to find her in such a pleasant temper, and thought to herself that perhaps it was only the pepper that had made her so savage when they met in the kitchen.
‘When I’M a Duchess,’ she said to herself, (not in a very hopeful tone though), ‘I won’t have any pepper in my kitchen AT ALL. Soup does very well without–Maybe it’s always pepper that makes people hot-tempered,’ she went on, very much pleased at having found out a new kind of rule, ‘and vinegar that makes them sour–and camomile that makes them bitter–and– and barley-sugar and such things that make children sweet-tempered. I only wish people knew that: then they wouldn’t be so stingy about it, you know–’
She had quite forgotten the Duchess by this time
```

**Full original cited chunk:**

```text
en sweet-tempered. I only wish people knew that: then they wouldn’t be so stingy about it, you know–’
She had quite forgotten the Duchess by this time, and was a little startled when she heard her voice close to her ear. ‘You’re thinking about something, my dear, and that makes you forget to talk. I can’t tell you just now what the moral of that is, but I shall remember it in a bit.’
‘Perhaps it hasn’t one,’ Alice ventured to remark.
‘Tut, tut, child!’ said the Duchess. ‘Everything’s got a moral, if only you can find it.’ And she squeezed herself up closer to Alice’s side as she spoke.
Alice did not much like keeping so close to her: first, because the Duchess was VERY ugly; and secondly, because she was exactly the right height to rest her chin upon Alice’s shoulder, and it was an uncomfortably sharp chin.
However, she did not like to be rude, so she bore it as well as she could.
‘The game’s going on rather better now,’ she said, by way of keeping up

68 CHAPTER 9. THE MOCK TURTLE’S STORY

the conversation a little.
‘’Tis so,’ said the Duchess: ‘and the moral of that is–”Oh, ’tis love, ’tis love, that makes the world go round!”’
‘Somebody said,’ Alice whispered, ‘that it’s done by
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00106` (pages 68–68)

```text
he Duchess: ‘and the moral of that is–”Oh, ’tis love, ’tis love, that makes the world go round!”’
‘Somebody said,’ Alice whispered, ‘that it’s done by everybody minding their own business!’
‘Ah, well! It means much the same thing,’ said the Duchess, digging her sharp little chin into Alice’s shoulder as she added, ‘and the moral of THAT is– “Take care of the sense, and the sounds will take care of themselves.”’
‘How fond she is of finding morals in things!’ Alice thought to herself.
‘I dare say you’re wondering why I don’t put my arm round your waist,’ the Duchess said after a pause: ‘the reason is, that I’m doubtful about the temper of your flamingo. Shall I try the experiment?’
‘HE might bite,’ Alice cautiously replied, not feeling at all anxious to have the experiment tried.
‘Very true,’ said the Duchess: ‘flamingoes and mustard both bite. And the moral of that is– “Birds of a feather flock together.”’
‘Only mustard isn’t a bird,’ Alice remarked.
‘Right, as usual,’ said the Duchess: ‘what a clear way you have of putting things!’
‘It’s a mineral, I THINK,’ said Alice.
‘Of course it is,’ said the Duchess, who seemed ready to agree to everything that Alice said; ‘there’s a large mu
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q026

**Question:** Which oddly named subjects did the Mock Turtle say were taught at school?

**Reference answer:** Reeling and Writhing, plus Ambition, Distraction, Uglification, and Derision.

**Final generated answer:** The Mock Turtle listed the following oddly named subjects: Reeling and Writhing; the branches of Arithmetic known as Ambition, Distraction, Uglification, and Derision; Mystery (ancient and modern); Seaography; Drawling; Stretching; Fainting in Coils; and Laughing and Grief.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** The school subjects included Reeling and Writhing.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 71, 72
- **Exact supporting span(s):**
  - `S1`:

```text
Reeling and Writhing
```

#### Claim C2

- **Claim text:** The arithmetic branches were Ambition, Distraction, Uglification, and Derision.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 71, 72
- **Exact supporting span(s):**
  - `S1`:

```text
Ambition, Distraction, Uglification, and Derision
```

#### Claim C3

- **Claim text:** Other named subjects were Mystery, Seaography, Drawling, Stretching, Fainting in Coils, Laughing, and Grief.
- **Source ID(s):** `S1`, `S3`
- **Cited page(s):** S1: 71, 72; S3: 72
- **Exact supporting span(s):**
  - `S1`:

```text
there was Mystery
```
  - `S1`:

```text
with Seaography
```
  - `S3`:

```text
HE taught us Drawling, Stretching, and Fainting in Coils
```
  - `S3`:

```text
Laughing and Grief
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S1 context — supports claim(s) C1, C2, C3

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00114`
- Cited page(s): 71, 72
- Parsed chunk page range: 71–72

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00113` (pages 71–71)

```text
yourself for asking such a simple question,’ added the Gryphon; and then they both sat silent and looked at poor Alice, who felt ready to sink into the earth. At last the Gryphon said to the Mock
Turtle, ‘Drive on, old fellow! Don’t be all day about it!’ and he went on in these words:
‘Yes, we went to school in the sea, though you mayn’t believe it–’
‘I never said I didn’t!’ interrupted Alice.
‘You did,’ said the Mock Turtle.
‘Hold your tongue!’ added the Gryphon, before Alice could speak again.
The Mock Turtle went on.
‘We had the best of educations–in fact, we went to school every day–’
‘I’VE been to a day-school, too,’ said Alice; ‘you needn’t be so proud as all that.’
‘With extras?’ asked the Mock Turtle a little anxiously.
‘Yes,’ said Alice, ‘we learned French and music.’
‘And washing?’ said the Mock Turtle.
‘Certainly not!’ said Alice indignantly.
‘Ah! then yours wasn’t a really good school,’ said the Mock Turtle in a tone of great relief. ‘Now at OURS they had at the end of the bill, “French, music, AND WASHING–extra.”’
‘You couldn’t have wanted it much,’ said Alice; ‘living at the bottom of the sea.’
‘I couldn’t afford to learn it.’ said the Mock Turtle with a sigh. ‘I only
```

**Full original cited chunk:**

```text
uldn’t have wanted it much,’ said Alice; ‘living at the bottom of the sea.’
‘I couldn’t afford to learn it.’ said the Mock Turtle with a sigh. ‘I only took the regular course.’
‘What was that?’ inquired Alice.
‘Reeling and Writhing, of course, to begin with,’ the Mock Turtle replied;
‘and then the different branches of Arithmetic– Ambition, Distraction, Uglification, and Derision.’
‘I never heard of “Uglification,”’ Alice ventured to say. ‘What is it?’
The Gryphon lifted up both its paws in surprise. ‘What! Never heard of uglifying!’ it exclaimed. ‘You know what to beautify is, I suppose?’
‘Yes,’ said Alice doubtfully: ‘it means–to–make–anything–prettier.’

72 CHAPTER 9. THE MOCK TURTLE’S STORY

‘Well, then,’ the Gryphon went on, ‘if you don’t know what to uglify is, you ARE a simpleton.’
Alice did not feel encouraged to ask any more questions about it, so she turned to the Mock Turtle, and said ‘What else had you to learn?’
‘Well, there was Mystery,’ the Mock Turtle replied, counting offthe subjects on his flappers, ‘–Mystery, ancient and modern, with Seaography: then
Drawling–the Drawling-master was an old conger-eel, that used to come once a week: HE taught us Drawling, Stretchi
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00115` (pages 72–72)

```text
t and modern, with Seaography: then
Drawling–the Drawling-master was an old conger-eel, that used to come once a week: HE taught us Drawling, Stretching, and Fainting in Coils.’
‘What was THAT like?’ said Alice.
‘Well, I can’t show it you myself,’ the Mock Turtle said: ‘I’m too stiff.
And the Gryphon never learnt it.’
‘Hadn’t time,’ said the Gryphon: ‘I went to the Classics master, though.
He was an old crab, HE was.’
‘I never went to him,’ the Mock Turtle said with a sigh: ‘he taught
Laughing and Grief, they used to say.’
‘So he did, so he did,’ said the Gryphon, sighing in his turn; and both creatures hid their faces in their paws.
‘And how many hours a day did you do lessons?’ said Alice, in a hurry to change the subject.
‘Ten hours the first day,’ said the Mock Turtle: ‘nine the next, and so on.’
‘What a curious plan!’ exclaimed Alice.
‘That’s the reason they’re called lessons,’ the Gryphon remarked: ‘because they lessen from day to day.’
This was quite a new idea to Alice, and she thought it over a little before she made her next remark. ‘Then the eleventh day must have been a holiday?’
‘Of course it was,’ said the Mock Turtle.
‘And how did you manage on the twelfth?’ Alice we
```

#### S3 context — supports claim(s) C3

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00115`
- Cited page(s): 72
- Parsed chunk page range: 72–72

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00114` (pages 71–72)

```text
uldn’t have wanted it much,’ said Alice; ‘living at the bottom of the sea.’
‘I couldn’t afford to learn it.’ said the Mock Turtle with a sigh. ‘I only took the regular course.’
‘What was that?’ inquired Alice.
‘Reeling and Writhing, of course, to begin with,’ the Mock Turtle replied;
‘and then the different branches of Arithmetic– Ambition, Distraction, Uglification, and Derision.’
‘I never heard of “Uglification,”’ Alice ventured to say. ‘What is it?’
The Gryphon lifted up both its paws in surprise. ‘What! Never heard of uglifying!’ it exclaimed. ‘You know what to beautify is, I suppose?’
‘Yes,’ said Alice doubtfully: ‘it means–to–make–anything–prettier.’

72 CHAPTER 9. THE MOCK TURTLE’S STORY

‘Well, then,’ the Gryphon went on, ‘if you don’t know what to uglify is, you ARE a simpleton.’
Alice did not feel encouraged to ask any more questions about it, so she turned to the Mock Turtle, and said ‘What else had you to learn?’
‘Well, there was Mystery,’ the Mock Turtle replied, counting offthe subjects on his flappers, ‘–Mystery, ancient and modern, with Seaography: then
Drawling–the Drawling-master was an old conger-eel, that used to come once a week: HE taught us Drawling, Stretchi
```

**Full original cited chunk:**

```text
t and modern, with Seaography: then
Drawling–the Drawling-master was an old conger-eel, that used to come once a week: HE taught us Drawling, Stretching, and Fainting in Coils.’
‘What was THAT like?’ said Alice.
‘Well, I can’t show it you myself,’ the Mock Turtle said: ‘I’m too stiff.
And the Gryphon never learnt it.’
‘Hadn’t time,’ said the Gryphon: ‘I went to the Classics master, though.
He was an old crab, HE was.’
‘I never went to him,’ the Mock Turtle said with a sigh: ‘he taught
Laughing and Grief, they used to say.’
‘So he did, so he did,’ said the Gryphon, sighing in his turn; and both creatures hid their faces in their paws.
‘And how many hours a day did you do lessons?’ said Alice, in a hurry to change the subject.
‘Ten hours the first day,’ said the Mock Turtle: ‘nine the next, and so on.’
‘What a curious plan!’ exclaimed Alice.
‘That’s the reason they’re called lessons,’ the Gryphon remarked: ‘because they lessen from day to day.’
This was quite a new idea to Alice, and she thought it over a little before she made her next remark. ‘Then the eleventh day must have been a holiday?’
‘Of course it was,’ said the Mock Turtle.
‘And how did you manage on the twelfth?’ Alice we
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00116` (pages 72–73)

```text
remark. ‘Then the eleventh day must have been a holiday?’
‘Of course it was,’ said the Mock Turtle.
‘And how did you manage on the twelfth?’ Alice went on eagerly.
‘That’s enough about lessons,’ the Gryphon interrupted in a very decided tone: ‘tell her something about the games now.’

Chapter 10

The Lobster Quadrille

The Mock Turtle sighed deeply, and drew the back of one flapper across his eyes. He looked at Alice, and tried to speak, but for a minute or two sobs choked his voice. ‘Same as if he had a bone in his throat,’ said the Gryphon:
and it set to work shaking him and punching him in the back. At last the
Mock Turtle recovered his voice, and, with tears running down his cheeks, he went on again:–
‘You may not have lived much under the sea–’ (‘I haven’t,’ said Alice)– ‘and perhaps you were never even introduced to a lobster–’ (Alice began to say ‘I once tasted–’ but checked herself hastily, and said ‘No, never’) ‘–so you can have no idea what a delightful thing a Lobster Quadrille is!’
‘No, indeed,’ said Alice. ‘What sort of a dance is it?’
‘Why,’ said the Gryphon, ‘you first form into a line along the sea-shore–’
‘Two lines!’ cried the Mock Turtle. ‘Seals, turtles, salmon
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q028

**Question:** What was the Knave of Hearts accused of, and who was called as the first witness?

**Reference answer:** He was accused of stealing the Queen's tarts, and the Hatter was the first witness.

**Final generated answer:** The Knave of Hearts was accused of stealing the tarts made by the Queen of Hearts. The first witness called was the Hatter.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** The Knave of Hearts was accused of stealing the Queen of Hearts’ tarts.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 82, 83
- **Exact supporting span(s):**
  - `S1`:

```text
The Knave of Hearts, he stole those tarts
```

#### Claim C2

- **Claim text:** The Hatter was called as the first witness.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 82, 83
- **Exact supporting span(s):**
  - `S1`:

```text
The first witness was the Hatter
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S1 context — supports claim(s) C1, C2

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00130`
- Cited page(s): 82, 83
- Parsed chunk page range: 82–83

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00129` (pages 82–82)

```text
on whispered in reply, ‘for fear they should forget them before the end of the trial.’
‘Stupid things!’ Alice began in a loud, indignant voice, but she stopped hastily, for the White Rabbit cried out, ‘Silence in the court!’ and the King put on his spectacles and looked anxiously round, to make out who was talking.
Alice could see, as well as if she were looking over their shoulders, that all the jurors were writing down ‘stupid things!’ on their slates, and she could even make out that one of them didn’t know how to spell ‘stupid,’ and that he had to ask his neighbour to tell him. ‘A nice muddle their slates’ll be in before the trial’s over!’ thought Alice.
One of the jurors had a pencil that squeaked. This of course, Alice could not stand, and she went round the court and got behind him, and very soon found an opportunity of taking it away. She did it so quickly that the poor little juror (it was Bill, the Lizard) could not make out at all what had become of it; so, after hunting all about for it, he was obliged to write with one finger for the rest of the day; and this was of very little use, as it left no mark on the slate.
‘Herald, read the accusation!’ said the King.
On this
```

**Full original cited chunk:**

```text
nger for the rest of the day; and this was of very little use, as it left no mark on the slate.
‘Herald, read the accusation!’ said the King.
On this the White Rabbit blew three blasts on the trumpet, and then unrolled the parchment scroll, and read as follows:–

‘The Queen of Hearts, she made some tarts,
All on a summer day:
The Knave of Hearts, he stole those tarts,
And took them quite away!’

‘Consider your verdict,’ the King said to the jury.
‘Not yet, not yet!’ the Rabbit hastily interrupted. ‘There’s a great deal to come before that!’
‘Call the first witness,’ said the King; and the White Rabbit blew three blasts on the trumpet, and called out, ‘First witness!’
The first witness was the Hatter. He came in with a teacup in one hand and a piece of bread-and-butter in the other. ‘I beg pardon, your Majesty,’ he began, ‘for bringing these in: but I hadn’t quite finished my tea when I was sent for.’
‘You ought to have finished,’ said the King. ‘When did you begin?’

The Hatter looked at the March Hare, who had followed him into the court, arm-in-arm with the Dormouse. ‘Fourteenth of March, I think it was,’ he said.
‘Fifteenth,’ said the March Hare.
‘Sixteenth,’ added the Dormouse.
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00131` (pages 83–83)

```text
ourt, arm-in-arm with the Dormouse. ‘Fourteenth of March, I think it was,’ he said.
‘Fifteenth,’ said the March Hare.
‘Sixteenth,’ added the Dormouse.
‘Write that down,’ the King said to the jury, and the jury eagerly wrote down all three dates on their slates, and then added them up, and reduced the answer to shillings and pence.
‘Take offyour hat,’ the King said to the Hatter.
‘It isn’t mine,’ said the Hatter.
‘Stolen!’ the King exclaimed, turning to the jury, who instantly made a memorandum of the fact.
‘I keep them to sell,’ the Hatter added as an explanation; ‘I’ve none of my own. I’m a hatter.’
Here the Queen put on her spectacles, and began staring at the Hatter, who turned pale and fidgeted.
‘Give your evidence,’ said the King; ‘and don’t be nervous, or I’ll have you executed on the spot.’
This did not seem to encourage the witness at all: he kept shifting from one foot to the other, looking uneasily at the Queen, and in his confusion he bit a large piece out of his teacup instead of the bread-and-butter.
Just at this moment Alice felt a very curious sensation, which puzzled her a good deal until she made out what it was: she was beginning to grow larger again, and she thou
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q030

**Question:** Under Rule Forty-two, which people had to leave the court?

**Reference answer:** All persons more than a mile high.

**Final generated answer:** Under Rule Forty-two, all persons more than a mile high had to leave the court.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** Rule Forty-two required all persons more than a mile high to leave the court.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 88
- **Exact supporting span(s):**
  - `S1`:

```text
ALL PERSONS MORE THAN A MILE HIGH TO LEAVE THE
COURT
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S1 context — supports claim(s) C1

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00139`
- Cited page(s): 88
- Parsed chunk page range: 88–88

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00138` (pages 87–88)

```text
he had put the
Lizard in head downwards, and the poor little thing was waving its tail about in a melancholy way, being quite unable to move. She soon got it out again, and put it right; ‘not that it signifies much,’ she said to herself; ‘I should think it would be QUITE as much use in the trial one way up as the other.’
As soon as the jury had a little recovered from the shock of being upset, and their slates and pencils had been found and handed back to them, they set to work very diligently to write out a history of the accident, all except the Lizard, who seemed too much overcome to do anything but sit with its mouth open, gazing up into the roof of the court.
‘What do you know about this business?’ the King said to Alice.
‘Nothing,’ said Alice.

88 CHAPTER 12. ALICE’S EVIDENCE

‘Nothing WHATEVER?’ persisted the King.
‘Nothing whatever,’ said Alice.
‘That’s very important,’ the King said, turning to the jury. They were just beginning to write this down on their slates, when the White Rabbit interrupted: ‘UNimportant, your Majesty means, of course,’ he said in a very respectful tone, but frowning and making faces at him as he spoke.
‘UNimportant, of course, I meant,’ the King ha
```

**Full original cited chunk:**

```text
means, of course,’ he said in a very respectful tone, but frowning and making faces at him as he spoke.
‘UNimportant, of course, I meant,’ the King hastily said, and went on to himself in an undertone, ‘important–unimportant– unimportant–important–’ as if he were trying which word sounded best.
Some of the jury wrote it down ‘important,’ and some ‘unimportant.’
Alice could see this, as she was near enough to look over their slates; ‘but it doesn’t matter a bit,’ she thought to herself.
At this moment the King, who had been for some time busily writing in his note-book, cackled out ‘Silence!’ and read out from his book, ‘Rule
Forty-two. ALL PERSONS MORE THAN A MILE HIGH TO LEAVE THE
COURT.’
Everybody looked at Alice.
‘I’M not a mile high,’ said Alice.
‘You are,’ said the King.
‘Nearly two miles high,’ added the Queen.
‘Well, I shan’t go, at any rate,’ said Alice: ‘besides, that’s not a regular rule: you invented it just now.’
‘It’s the oldest rule in the book,’ said the King.
‘Then it ought to be Number One,’ said Alice.
The King turned pale, and shut his note-book hastily. ‘Consider your verdict,’ he said to the jury, in a low, trembling voice.
‘There’s more evidence to come yet, p
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00140` (pages 88–89)

```text
d pale, and shut his note-book hastily. ‘Consider your verdict,’ he said to the jury, in a low, trembling voice.
‘There’s more evidence to come yet, please your Majesty,’ said the White
Rabbit, jumping up in a great hurry; ‘this paper has just been picked up.’
‘What’s in it?’ said the Queen.
‘I haven’t opened it yet,’ said the White Rabbit, ‘but it seems to be a letter, written by the prisoner to–to somebody.’
‘It must have been that,’ said the King, ‘unless it was written to nobody, which isn’t usual, you know.’
‘Who is it directed to?’ said one of the jurymen.
‘It isn’t directed at all,’ said the White Rabbit; ‘in fact, there’s nothing written on the OUTSIDE.’ He unfolded the paper as he spoke, and added ‘It isn’t a letter, after all: it’s a set of verses.’
‘Are they in the prisoner’s handwriting?’ asked another of the jurymen.

‘No, they’re not,’ said the White Rabbit, ‘and that’s the queerest thing about it.’ (The jury all looked puzzled.)
‘He must have imitated somebody else’s hand,’ said the King. (The jury all brightened up again.)
‘Please your Majesty,’ said the Knave, ‘I didn’t write it, and they can’t prove I did: there’s no name signed at the end.’
‘If you didn’t sign it
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

# Reliability challenge cases

## c001

**Question:** What was Alice's exact home street address?

**Reference answer:** The uploaded book does not provide Alice's street address.

**Final generated answer:** The provided text does not contain Alice's exact home street address.

**Final status:** `insufficient_evidence`

### Whole-document negative check

**Method:** exhaustive regex/lexical scan over every stored parsed page, independent of retrieval output, followed by semantic inspection of all recorded hits and their page context.

| Search term / variant | Hit count | Parsed page location(s) | Semantic inspection |
|---|---:|---|---|
| `street address` | 0 | none | Exact requested relation; no match. |
| `home address` | 0 | none | Direct paraphrase; no match. |
| `street` / `streets` | 0 | none | Address component; no match. |
| `road` / `avenue` / `lane` | 0 | none | Street-name variants; no match. |
| `postal` | 0 | none | Postal-address variant; no match. |
| `residence` | 0 | none | Residence synonym; no match. |
| `where Alice lives` | 0 | none | Natural-language paraphrase; no match. |
| `lives at` / `live at` | 2 | 55 | Two hits concern the treacle-well, not Alice’s residence. |
| `address*` | 3 | 29, 37, 45 | All hits are verbs meaning “speak to”; none is a postal address. |
| `home` | 5 | 14, 29, 31, 32, 47 | All hits are generic destinations/feelings; none names a street. |
| `house` / `houses` | 19 | 14, 21, 22, 23, 28, 31, 32, 33, 34, 35, 42, 43, 44, 49, 51 | All hits were inspected; they refer to generic or other characters’ houses and give no Alice street address. |
| `lodging` | 1 | 22 | The sole hit describes generic English seaside lodging houses. |
| `near the fender` | 1 | 19 | Imagined comic directions to Alice’s foot, explicitly called nonsense; not Alice’s home address. |

#### Exact excerpts for potentially misleading hits

**`lives at` / `live at`**

- Page 55: “an extraordinary ways of living would be like, but it puzzled her too much, so she went on: ‘But why did they live at the bottom of a well?’ ‘Take some more tea,’ the March Hare said to Alice, very earnestly. ‘I’ve had nothing yet,’ Alice replied in an offended tone, ‘so I can’t take mo”
- Page 55: “f to some tea and bread-and-butter, and then turned to the Dormouse, and repeated her question. ‘Why did they live at the bottom of a well?’ The Dormouse again took a minute or two to think about it, and then said, ‘It was a treacle-well.’ ‘There’s no such thing!’ Alice was beginning ve”

**`address*`**

- Page 29: “ou’re enough to try the patience of an oyster!’ ‘I wish I had our Dinah here, I know I do!’ said Alice aloud, addressing nobody in particular. ‘She’d soon fetch it back!’ ‘And who is Dinah, if I might venture to ask the question?’ said the Lory. Alice replied eagerly, for she was always re”
- Page 37: “looked at each other for some time in silence: at last the Caterpillar took the hookah out of its mouth, and addressed her in a languid, sleepy voice. ‘Who are YOU?’ said the Caterpillar. This was not an encouraging opening for a conversation. Alice replied, rather shyly, ‘I–I hardly kno”
- Page 45: “id the last word with such sudden violence that Alice quite jumped; but she saw in another moment that it was addressed to the baby, and not to her, so she took courage, and went on again:– ‘I didn’t know that Cheshire cats always grinned; in fact, I didn’t know that cats COULD grin.’ ‘Th”

**`home`**

- Page 14: “‘after such a fall as this, I shall think nothing of tumbling down stairs! How brave they’ll all think me at home! Why, I wouldn’t say anything about it, even if I fell offthe top of the house!’ (Which was very likely true.) Down, down, down. Would the fall NEVER come to an end! ‘I”
- Page 29: “ried offat once: one old Magpie began wrapping itself up very carefully, remarking, ‘I really must be getting home; the night-air doesn’t suit my throat!’ and a Canary called out in a trembling voice to its children,”
- Page 31: “went hunting about, and called out to her in an angry tone, ‘Why, Mary Ann, what ARE you doing out here? Run home this moment, and fetch me a pair of gloves and a fan! Quick, now!’ And Alice was so much frightened that she ran offat once in the direction it pointed to, without tryin”
- Page 32: “t of chance of her ever getting out of the room again, no wonder she felt unhappy. ‘It was much pleasanter at home,’ thought poor Alice, ‘when one wasn’t always growing larger and smaller, and being ordered about by mice and rabbits. I almost wish I hadn’t gone down that rabbit-hole–”
- Page 47: “silence. Alice was just beginning to think to herself, ‘Now, what am I to do with this creature when I get it home?’ when it grunted again, so violently, that she looked down into its face in some alarm. This time there could be NO mistake about it: it was neither more nor less than”

**`near the fender`**

- Page 19: “ending presents to one’s own feet! And how odd the directions will look! ALICE’S RIGHT FOOT, ESQ. HEARTHRUG, NEAR THE FENDER, (WITH ALICE’S LOVE). Oh dear, what nonsense I’m talking!’ Just then her head struck against the roof of the hall: in fact she was now more than nine feet high, and she”

**Entity/relation check:** occurrences of “Alice” were not treated as evidence by themselves. None of the address/residence variants supplies a street name, house number, postal location, or statement of where Alice lives. The “HEARTHRUG, NEAR THE FENDER” passage is Alice imagining how to address a parcel to her foot and immediately calling it nonsense.

**Conclusion:** no supporting evidence found in parsed book.

This conclusion is limited to the complete locally stored text layer described above. It is not a mathematical proof that no edition, image, OCR layer, or unforeseen paraphrase could contain the fact.

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## c002

**Question:** What was the Queen of Hearts' date of birth?

**Reference answer:** The uploaded book does not provide the Queen of Hearts' date of birth.

**Final generated answer:** The provided texts do not contain information regarding the Queen of Hearts' date of birth.

**Final status:** `insufficient_evidence`

### Whole-document negative check

**Method:** exhaustive regex/lexical scan over every stored parsed page, independent of retrieval output, followed by semantic inspection of all recorded hits and their page context.

| Search term / variant | Hit count | Parsed page location(s) | Semantic inspection |
|---|---:|---|---|
| `date of birth` | 0 | none | Exact requested relation; no match. |
| `birth date` | 0 | none | Direct paraphrase; no match. |
| `born` | 0 | none | Morphological/biographical variant; no match. |
| `birth` | 0 | none | Biographical key term; no standalone match. |
| `birthday` | 1 | 69 | One hit discusses birthday presents generally; it does not state anyone’s birth date. |
| `age` | 4 | 20, 25, 38, 81 | Four hits concern Alice, the Lory, Father William, or jurors; none concerns the Queen’s age. |
| `years old` | 0 | none | Age paraphrase; no match. |
| `date` / `dates` | 6 | 3, 8, 83 | Broad date terms occur only in front matter and the Hatter trial; none states a birth date. |
| `year` / `years` | 7 | 4, 5, 52, 92 | Broad year terms occur in front matter, a watch discussion, and narration; none concerns the Queen’s birth. |
| `anniversary` | 0 | none | Date/celebration variant; no match. |
| `Queen of Hearts` | 4 | 53, 60, 81, 82 | Entity-only matches identify scenes/concert/trial/tarts, never a date of birth. |

#### Exact excerpts for potentially misleading hits

**`birthday`**

- Page 69: “‘A cheap sort of present!’ thought Alice. ‘I’m glad they don’t give birthday presents like that!’ But she did not venture to say it out loud. ‘Thinking again?’ the Duchess asked, with another dig of her sharp little chin. ‘I’ve a right to think,’”

**`age`**

- Page 20: “I? Ah, THAT’S the great puzzle!’ And she began thinking over all the children she knew that were of the same age as herself, to see if she could have been changed for any of them. ‘I’m sure I’m not Ada,’ she said, ‘for her hair goes in such long ringlets, and mine doesn’t go in ri”
- Page 25: “nd this Alice would not allow without knowing how old it was, and, as the Lory positively refused to tell its age, there was no more to be said. At last the Mouse, who seemed to be a person of authority among them, called out, ‘Sit down, all of you, and listen to me! I’LL soon make”
- Page 38: “said, ‘And your hair has become very white; And yet you incessantly stand on your head– Do you think, at your age, it is right?’ ‘In my youth,’ Father William replied to his son, ‘I feared it might injure the brain; But, now that I’m perfectly sure I have none, Why, I do it again a”
- Page 81: “ver to herself, being rather proud of it: for she thought, and rightly too, that very few little girls of her age knew the meaning of it at all. However, ‘jury-men’ would have done just as well. The twelve jurors were all writing very busily on slates. ‘What are they doing?’ Alice w”

**`Queen of Hearts`**

- Page 53: “t mad, you know–’ (pointing with his tea spoon at the March Hare,) ‘–it was at the great concert given by the Queen of Hearts, and I had to sing “Twinkle, twinkle, little bat!”
- Page 60: “rying the King’s crown on a crimson velvet cushion; and, last of all this grand procession, came THE KING AND QUEEN OF HEARTS. Alice was rather doubtful whether she ought not to lie down on her face like the three gardeners, but she could not remember ever having heard of such a rule at process”
- Page 81: “Chapter 11 Who Stole the Tarts? The King and Queen of Hearts were seated on their throne when they arrived, with a great crowd assembled about them–all sorts of little birds and beasts, as well as the whole pack of cards: the Knav”
- Page 82: “Rabbit blew three blasts on the trumpet, and then unrolled the parchment scroll, and read as follows:– ‘The Queen of Hearts, she made some tarts, All on a summer day: The Knave of Hearts, he stole those tarts, And took them quite away!’ ‘Consider your verdict,’ the King said to the jury. ‘No”

**Entity/relation check:** all four exact “Queen of Hearts” locations (pages 53, 60, 81, 82) were inspected. None co-occurs with a birth-date assertion. The only “birthday” hit (page 69) is a general comment about birthday presents, and the four whole-word “age” hits concern other subjects.

**Conclusion:** no supporting evidence found in parsed book.

This conclusion is limited to the complete locally stored text layer described above. It is not a mathematical proof that no edition, image, OCR layer, or unforeseen paraphrase could contain the fact.

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## c003

**Question:** What happened after Alice changed size?

**Reference answer:** The question needs the particular size change or scene because Alice changes size several times.

**Final generated answer:** [blank]

**Final status:** `ambiguous`

**Generated clarification:** Which specific instance of Alice changing size are you referring to?

### Ambiguity rationale

The phrase “changed size” does not identify a unique event. The book contains multiple distinct size changes with different causes, scenes, and subsequent events. Choosing one would add an unsupported conversational assumption.

**Contextual evidence for multiple plausible referents/events:**

- **Bottle/corridor size change:** `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00019`, page range 16–16

```text
ne-apple, roast turkey, toffee, and hot buttered toast,) she very soon finished it off.
‘What a curious feeling!’ said Alice; ‘I must be shutting up like a telescope.’
And so it was indeed: she was now only ten inches high, and her face brightened up at the thought that she was now the right size for going through the little door into that lovely garden. First, however, she waited for a few minutes to see if
```

- **Rabbit-fan size change:** `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00027`, page range 21–22

```text
’ she thought. ‘I must be growing small again.’ She got up and went to the table to measure herself by it, and found that, as nearly as she could guess, she was now about two feet high, and was going on shrinking rapidly: she soon found out that the cause of this was the fan she was holding, and she dropped it hastily, just in time to avoid shrinking away altogether.
‘That WAS a narrow escape!’ said Alice,
```

- **Mushroom-controlled size changes:** `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00064`, page range 42–42

```text
op and untwist it. After a while she remembered that she still held the pieces of mushroom in her hands, and she set to work very carefully, nibbling first at one and then at the other, and growing sometimes taller and sometimes shorter, until she had succeeded in bringing herself down to her usual height.
It was so l
```

- **Courtroom size change:** `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00132`, page range 83–84

```text
lice felt a very curious sensation, which puzzled her a good deal until she made out what it was: she was beginning to grow larger again, and she thought at first she would get up and leave the court;
but on second thoughts she decided to remain where she was as long as there was room for her.
‘I wish you wouldn’t squeeze so
```

**Conclusion:** the question needs the particular size change or scene before “after” has a unique referent.

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## c004

**Question:** What happened next?

**Reference answer:** The question needs the event or passage to continue from because the book contains many possible next events.

**Final generated answer:** [blank]

**Final status:** `ambiguous`

**Generated clarification:** Which specific event or scene are you referring to?

### Ambiguity rationale

“Next” is a conversational pointer. No prior event, passage, scene, or previous turn is supplied in this isolated case, so there is no determinate starting point from which to continue.

**Book evidence:** none is needed to establish this ambiguity. The missing information is conversational state, not a disputed fact in the book.

**Conclusion:** ask the user which event or passage they want continued.

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## c005

**Question:** How tall did Alice become before the pool formed, and how deep did she say the pool was?

**Reference answer:** Alice became more than nine feet tall, and she said the pool was about four inches deep.

**Final generated answer:** Alice became more than nine feet tall, and she said the pool was about four inches deep.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** Alice became more than nine feet tall.
- **Source ID(s):** `S3`
- **Cited page(s):** S3: 19, 20
- **Exact supporting span(s):**
  - `S3`:

```text
more than nine feet high
```

#### Claim C2

- **Claim text:** Alice said the pool was about four inches deep.
- **Source ID(s):** `S3`
- **Cited page(s):** S3: 19, 20
- **Exact supporting span(s):**
  - `S3`:

```text
about four inches deep
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S3 context — supports claim(s) C1, C2

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00023`
- Cited page(s): 19, 20
- Parsed chunk page range: 19–20

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00022` (pages 17–19)

```text
o go on in the common way.
So she set to work, and very soon finished offthe cake.

18 CHAPTER 1. DOWN THE RABBIT-HOLE

Chapter 2

The Pool of Tears

‘Curiouser and curiouser!’ cried Alice (she was so much surprised, that for the moment she quite forgot how to speak good English); ‘now I’m opening out like the largest telescope that ever was! Good-bye, feet!’ (for when she looked down at her feet, they seemed to be almost out of sight, they were getting so far off). ‘Oh, my poor little feet, I wonder who will put on your shoes and stockings for you now, dears? I’m sure I shan’t be able! I shall be a great deal too far offto trouble myself about you: you must manage the best way you can; –but I must be kind to them,’ thought Alice, ‘or perhaps they won’t walk the way I want to go! Let me see: I’ll give them a new pair of boots every Christmas.’
And she went on planning to herself how she would manage it. ‘They must go by the carrier,’ she thought; ‘and how funny it’ll seem, sending presents to one’s own feet! And how odd the directions will look!

ALICE’S RIGHT FOOT, ESQ.
HEARTHRUG,
NEAR THE FENDER,
(WITH ALICE’S LOVE).

Oh dear, what nonsense I’m talking!’
Just then her head struck
```

**Full original cited chunk:**

```text
will look!

ALICE’S RIGHT FOOT, ESQ.
HEARTHRUG,
NEAR THE FENDER,
(WITH ALICE’S LOVE).

Oh dear, what nonsense I’m talking!’
Just then her head struck against the roof of the hall: in fact she was now more than nine feet high, and she at once took up the little golden key and hurried offto the garden door.
Poor Alice! It was as much as she could do, lying down on one side, to look through into the garden with one eye; but to get through was more hopeless than ever: she sat down and began to cry again.

20 CHAPTER 2. THE POOL OF TEARS

‘You ought to be ashamed of yourself,’ said Alice, ‘a great girl like you,’ (she might well say this), ‘to go on crying in this way! Stop this moment,
I tell you!’ But she went on all the same, shedding gallons of tears, until there was a large pool all round her, about four inches deep and reaching half down the hall.

After a time she heard a little pattering of feet in the distance, and she hastily dried her eyes to see what was coming. It was the White Rabbit returning, splendidly dressed, with a pair of white kid gloves in one hand and a large fan in the other: he came trotting along in a great hurry, muttering to himself as he came, ‘Oh! the Duc
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00024` (pages 20–20)

```text
r of white kid gloves in one hand and a large fan in the other: he came trotting along in a great hurry, muttering to himself as he came, ‘Oh! the Duchess, the Duchess! Oh! won’t she be savage if I’ve kept her waiting!’ Alice felt so desperate that she was ready to ask help of any one; so, when the Rabbit came near her, she began, in a low, timid voice, ‘If you please, sir–’ The Rabbit started violently, dropped the white kid gloves and the fan, and skurried away into the darkness as hard as he could go.

Alice took up the fan and gloves, and, as the hall was very hot, she kept fanning herself all the time she went on talking: ‘Dear, dear! How queer everything is to-day! And yesterday things went on just as usual. I wonder if
I’ve been changed in the night? Let me think: was I the same when I got up this morning? I almost think I can remember feeling a little different. But if
I’m not the same, the next question is, Who in the world am I? Ah, THAT’S the great puzzle!’ And she began thinking over all the children she knew that were of the same age as herself, to see if she could have been changed for any of them.

‘I’m sure I’m not Ada,’ she said, ‘for her hair goes in such long rin
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## c006

**Question:** After the Caucus-race, what did the other racers receive and what did Alice receive?

**Reference answer:** The others received comfits from Alice, while Alice received her own thimble from the Dodo.

**Final generated answer:** The other racers received comfits, and Alice received a thimble.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** The other racers received comfits.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 26, 27
- **Exact supporting span(s):**
  - `S1`:

```text
handed them round as prizes
```

#### Claim C2

- **Claim text:** Alice received a thimble.
- **Source ID(s):** `S3`
- **Cited page(s):** S3: 27
- **Exact supporting span(s):**
  - `S3`:

```text
presented the thimble
```
  - `S3`:

```text
acceptance of this elegant thimble
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S1 context — supports claim(s) C1

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00036`
- Cited page(s): 26, 27
- Parsed chunk page range: 26–27

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00035` (pages 26–26)

```text
all.’
‘In that case,’ said the Dodo solemnly, rising to its feet, ‘I move that the meeting adjourn, for the immediate adoption of more energetic remedies–’
‘Speak English!’ said the Eaglet. ‘I don’t know the meaning of half those long words, and, what’s more, I don’t believe you do either!’ And the Eaglet bent down its head to hide a smile: some of the other birds tittered audibly.
‘What I was going to say,’ said the Dodo in an offended tone, ‘was, that the best thing to get us dry would be a Caucus-race.’
‘What IS a Caucus-race?’ said Alice; not that she wanted much to know, but the Dodo had paused as if it thought that SOMEBODY ought to speak, and no one else seemed inclined to say anything.
‘Why,’ said the Dodo, ‘the best way to explain it is to do it.’ (And, as you might like to try the thing yourself, some winter day, I will tell you how the Dodo managed it.)
First it marked out a race-course, in a sort of circle, (‘the exact shape doesn’t matter,’ it said,) and then all the party were placed along the course, here and there. There was no ‘One, two, three, and away,’ but they began running when they liked, and left offwhen they liked, so that it was not easy to know when the r
```

**Full original cited chunk:**

```text
re was no ‘One, two, three, and away,’ but they began running when they liked, and left offwhen they liked, so that it was not easy to know when the race was over. However, when they had been running half an hour or so, and were quite dry again, the Dodo suddenly called out ‘The race is over!’ and they all crowded round it, panting, and asking, ‘But who has won?’
This question the Dodo could not answer without a great deal of thought,

and it sat for a long time with one finger pressed upon its forehead (the position in which you usually see Shakespeare, in the pictures of him), while the rest waited in silence. At last the Dodo said, ‘EVERYBODY has won, and all must have prizes.’
‘But who is to give the prizes?’ quite a chorus of voices asked.
‘Why, SHE, of course,’ said the Dodo, pointing to Alice with one finger;
and the whole party at once crowded round her, calling out in a confused way, ‘Prizes! Prizes!’
Alice had no idea what to do, and in despair she put her hand in her pocket, and pulled out a box of comfits, (luckily the salt water had not got into it), and handed them round as prizes. There was exactly one a-piece all round.
‘But she must have a prize herself, you know,’
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00037` (pages 27–27)

```text
t water had not got into it), and handed them round as prizes. There was exactly one a-piece all round.
‘But she must have a prize herself, you know,’ said the Mouse.
‘Of course,’ the Dodo replied very gravely. ‘What else have you got in your pocket?’ he went on, turning to Alice.
‘Only a thimble,’ said Alice sadly.
‘Hand it over here,’ said the Dodo.
Then they all crowded round her once more, while the Dodo solemnly presented the thimble, saying ‘We beg your acceptance of this elegant thimble’;
and, when it had finished this short speech, they all cheered.
Alice thought the whole thing very absurd, but they all looked so grave that she did not dare to laugh; and, as she could not think of anything to say, she simply bowed, and took the thimble, looking as solemn as she could.
The next thing was to eat the comfits: this caused some noise and confusion, as the large birds complained that they could not taste theirs, and the small ones choked and had to be patted on the back. However, it was over at last, and they sat down again in a ring, and begged the Mouse to tell them something more.
‘You promised to tell me your history, you know,’ said Alice, ‘and why it is you hate–C and D,’
```

#### S3 context — supports claim(s) C2

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00037`
- Cited page(s): 27
- Parsed chunk page range: 27–27

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00036` (pages 26–27)

```text
re was no ‘One, two, three, and away,’ but they began running when they liked, and left offwhen they liked, so that it was not easy to know when the race was over. However, when they had been running half an hour or so, and were quite dry again, the Dodo suddenly called out ‘The race is over!’ and they all crowded round it, panting, and asking, ‘But who has won?’
This question the Dodo could not answer without a great deal of thought,

and it sat for a long time with one finger pressed upon its forehead (the position in which you usually see Shakespeare, in the pictures of him), while the rest waited in silence. At last the Dodo said, ‘EVERYBODY has won, and all must have prizes.’
‘But who is to give the prizes?’ quite a chorus of voices asked.
‘Why, SHE, of course,’ said the Dodo, pointing to Alice with one finger;
and the whole party at once crowded round her, calling out in a confused way, ‘Prizes! Prizes!’
Alice had no idea what to do, and in despair she put her hand in her pocket, and pulled out a box of comfits, (luckily the salt water had not got into it), and handed them round as prizes. There was exactly one a-piece all round.
‘But she must have a prize herself, you know,’
```

**Full original cited chunk:**

```text
t water had not got into it), and handed them round as prizes. There was exactly one a-piece all round.
‘But she must have a prize herself, you know,’ said the Mouse.
‘Of course,’ the Dodo replied very gravely. ‘What else have you got in your pocket?’ he went on, turning to Alice.
‘Only a thimble,’ said Alice sadly.
‘Hand it over here,’ said the Dodo.
Then they all crowded round her once more, while the Dodo solemnly presented the thimble, saying ‘We beg your acceptance of this elegant thimble’;
and, when it had finished this short speech, they all cheered.
Alice thought the whole thing very absurd, but they all looked so grave that she did not dare to laugh; and, as she could not think of anything to say, she simply bowed, and took the thimble, looking as solemn as she could.
The next thing was to eat the comfits: this caused some noise and confusion, as the large birds complained that they could not taste theirs, and the small ones choked and had to be patted on the back. However, it was over at last, and they sat down again in a ring, and begged the Mouse to tell them something more.
‘You promised to tell me your history, you know,’ said Alice, ‘and why it is you hate–C and D,’
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00038` (pages 27–29)

```text
ng, and begged the Mouse to tell them something more.
‘You promised to tell me your history, you know,’ said Alice, ‘and why it is you hate–C and D,’ she added in a whisper, half afraid that it would be offended again.
‘Mine is a long and a sad tale!’ said the Mouse, turning to Alice, and sighing.
‘It IS a long tail, certainly,’ said Alice, looking down with wonder at the
Mouse’s tail; ‘but why do you call it sad?’ And she kept on puzzling about it while the Mouse was speaking, so that her idea of the tale was something like this:–

28 CHAPTER 3. A CAUCUS-RACE AND A LONG TALE

‘Fury said to a mouse, That he met in the house,
“Let us both go to law: I will prosecute
YOU. –Come,
I’ll take no denial; We must have a trial: For really this morning I’ve nothing to do.”
Said the mouse to the cur, “Such a trial, dear Sir,
With
no jury or judge, would be wasting our breath.”
“I’ll be judge, I’ll be jury,”
Said
cunning old Fury:
“I’ll try the whole

cause, and condemn you to death.”’

‘You are not attending!’ said the Mouse to Alice severely. ‘What are you thinking of?’
‘I beg your pardon,’ said Alice very humbly: ‘you had got to the fifth bend, I think?’
‘I had NOT!’ cried the Mouse, sharpl
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

# TEST cases

## q002

**Question:** How many chapters are listed, and what is the final chapter called?

**Reference answer:** There are twelve chapters; the final chapter is Alice's Evidence.

**Final generated answer:** There are 12 chapters listed, and the final chapter is called "Alice’s Evidence".

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** The contents list has twelve chapters.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 11, 12, 13
- **Exact supporting span(s):**
  - `S1`:

```text
12 Alice’s Evidence 87
```

#### Claim C2

- **Claim text:** The final chapter is “Alice’s Evidence.”
- **Source ID(s):** `S1`, `S2`
- **Cited page(s):** S1: 11, 12, 13; S2: 85, 86, 87
- **Exact supporting span(s):**
  - `S1`:

```text
12 Alice’s Evidence 87
```
  - `S2`:

```text
Chapter 12

Alice’s Evidence
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S1 context — supports claim(s) C1, C2

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00011`
- Cited page(s): 11, 12, 13
- Parsed chunk page range: 11–13

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00010` (pages 8–11)

```text
Project of 20net profits you derive calculated using the method you already use to calculate your applicable taxes. If you don’t derive profits, no royalty is due. Royalties are payable to “Project Gutenberg Association/Carnegie-Mellon University” within the 60 days following each date you prepare (or were legally required to prepare) your annual (or equivalent periodic) tax return.

WHAT IF YOU *WANT* TO SEND MONEY EVEN IF YOU DON’T
HAVE TO?

The Project gratefully accepts contributions in money, time, scanning machines, OCR software, public domain etexts, royalty free copyright licenses, and every other sort of contribution you can think of. Money should be paid to “Project Gutenberg Association / Carnegie-Mellon University”.
We are planning on making some changes in our donation structure in
2000, so you might want to email me, hart@pobox.com beforehand.
*END THE SMALL PRINT! FOR PUBLIC DOMAIN ETEXTS*
Ver.04.29.93*END*

ALICE’S ADVENTURES IN
WONDERLAND

Lewis Carroll

THE MILLENNIUM FULCRUM EDITION 3.0

Contents

1 Down the Rabbit-Hole 13

2 The Pool of Tears 19

3 A Caucus-Race and a Long Tale 25

4 The Rabbit Sends in a Little Bill 31

5 Advice from a Caterpillar 37

6 Pig and
```

**Full original cited chunk:**

```text
Hole 13

2 The Pool of Tears 19

3 A Caucus-Race and a Long Tale 25

4 The Rabbit Sends in a Little Bill 31

5 Advice from a Caterpillar 37

6 Pig and Pepper 43

7 A Mad Tea-Party 51

8 The Queen’s Croquet-Ground 59

9 The Mock Turtle’s Story 67

10 The Lobster Quadrille 73

11 Who Stole the Tarts? 81

12 Alice’s Evidence 87

12 CONTENTS

Chapter 1

Down the Rabbit-Hole

Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, ‘and what is the use of a book,’ thought Alice ‘without pictures or conversation?’
So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.
There was nothing so VERY remarkable in that; nor did Alice think it so
VERY much out of the way to hear the Rabbit say to itself, ‘Oh dear! Oh dear! I shall be late!’ (when she thought it over afterwards, it occurred to her that she
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00012` (pages 13–14)

```text
t of the way to hear the Rabbit say to itself, ‘Oh dear! Oh dear! I shall be late!’ (when she thought it over afterwards, it occurred to her that she ought to have wondered at this, but at the time it all seemed quite natural); but when the Rabbit actually TOOK A WATCH OUT OF
ITS WAISTCOAT- POCKET, and looked at it, and then hurried on, Alice started to her feet, for it flashed across her mind that she had never before seen a rabbit with either a waistcoat-pocket, or a watch to take out of it, and burning with curiosity, she ran across the field after it, and fortunately was just in time to see it pop down a large rabbit-hole under the hedge.
In another moment down went Alice after it, never once considering how in the world she was to get out again.
The rabbit-hole went straight on like a tunnel for some way, and then dipped suddenly down, so suddenly that Alice had not a moment to think about stopping herself before she found herself falling down a very deep well.
Either the well was very deep, or she fell very slowly, for she had plenty of time as she went down to look about her and to wonder what was going

14 CHAPTER 1. DOWN THE RABBIT-HOLE

to happen next. First, she tried to
```

#### S2 context — supports claim(s) C2

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00137`
- Cited page(s): 85, 86, 87
- Parsed chunk page range: 85–87

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00136` (pages 85–87)

```text
id, with a melancholy air, and, after folding his arms and frowning at the cook till his eyes were nearly out of sight, he said in a deep voice, ‘What are tarts made of?’
‘Pepper, mostly,’ said the cook.
‘Treacle,’ said a sleepy voice behind her.
‘Collar that Dormouse,’ the Queen shrieked out. ‘Behead that Dormouse!
Turn that Dormouse out of court! Suppress him! Pinch him! Offwith his whiskers!’
For some minutes the whole court was in confusion, getting the Dormouse turned out, and, by the time they had settled down again, the cook had disappeared.
‘Never mind!’ said the King, with an air of great relief. ‘Call the next witness.’ And he added in an undertone to the Queen, ‘Really, my dear, YOU must cross-examine the next witness. It quite makes my forehead ache!’
Alice watched the White Rabbit as he fumbled over the list, feeling very curious to see what the next witness would be like, ‘–for they haven’t got much evidence YET,’ she said to herself. Imagine her surprise, when the
White Rabbit read out, at the top of his shrill little voice, the name ‘Alice!’

86 CHAPTER 11. WHO STOLE THE TARTS?

Chapter 12

Alice’s Evidence

‘Here!’ cried Alice, quite forgetting in the flurry of the
```

**Full original cited chunk:**

```text
oice, the name ‘Alice!’

86 CHAPTER 11. WHO STOLE THE TARTS?

Chapter 12

Alice’s Evidence

‘Here!’ cried Alice, quite forgetting in the flurry of the moment how large she had grown in the last few minutes, and she jumped up in such a hurry that she tipped over the jury-box with the edge of her skirt, upsetting all the jurymen on to the heads of the crowd below, and there they lay sprawling about, reminding her very much of a globe of goldfish she had accidentally upset the week before.
‘Oh, I BEG your pardon!’ she exclaimed in a tone of great dismay, and began picking them up again as quickly as she could, for the accident of the goldfish kept running in her head, and she had a vague sort of idea that they must be collected at once and put back into the jury-box, or they would die.
‘The trial cannot proceed,’ said the King in a very grave voice, ‘until all the jurymen are back in their proper places– ALL,’ he repeated with great emphasis, looking hard at Alice as he said do.
Alice looked at the jury-box, and saw that, in her haste, she had put the
Lizard in head downwards, and the poor little thing was waving its tail about in a melancholy way, being quite unable to move. She soon
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00138` (pages 87–88)

```text
he had put the
Lizard in head downwards, and the poor little thing was waving its tail about in a melancholy way, being quite unable to move. She soon got it out again, and put it right; ‘not that it signifies much,’ she said to herself; ‘I should think it would be QUITE as much use in the trial one way up as the other.’
As soon as the jury had a little recovered from the shock of being upset, and their slates and pencils had been found and handed back to them, they set to work very diligently to write out a history of the accident, all except the Lizard, who seemed too much overcome to do anything but sit with its mouth open, gazing up into the roof of the court.
‘What do you know about this business?’ the King said to Alice.
‘Nothing,’ said Alice.

88 CHAPTER 12. ALICE’S EVIDENCE

‘Nothing WHATEVER?’ persisted the King.
‘Nothing whatever,’ said Alice.
‘That’s very important,’ the King said, turning to the jury. They were just beginning to write this down on their slates, when the White Rabbit interrupted: ‘UNimportant, your Majesty means, of course,’ he said in a very respectful tone, but frowning and making faces at him as he spoke.
‘UNimportant, of course, I meant,’ the King ha
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q003

**Question:** What color were the White Rabbit's eyes?

**Reference answer:** Pink.

**Final generated answer:** The White Rabbit's eyes were pink.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** The White Rabbit’s eyes were pink.
- **Source ID(s):** `S3`
- **Cited page(s):** S3: 11, 12, 13
- **Exact supporting span(s):**
  - `S3`:

```text
White Rabbit with pink eyes
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S3 context — supports claim(s) C1

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00011`
- Cited page(s): 11, 12, 13
- Parsed chunk page range: 11–13

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00010` (pages 8–11)

```text
Project of 20net profits you derive calculated using the method you already use to calculate your applicable taxes. If you don’t derive profits, no royalty is due. Royalties are payable to “Project Gutenberg Association/Carnegie-Mellon University” within the 60 days following each date you prepare (or were legally required to prepare) your annual (or equivalent periodic) tax return.

WHAT IF YOU *WANT* TO SEND MONEY EVEN IF YOU DON’T
HAVE TO?

The Project gratefully accepts contributions in money, time, scanning machines, OCR software, public domain etexts, royalty free copyright licenses, and every other sort of contribution you can think of. Money should be paid to “Project Gutenberg Association / Carnegie-Mellon University”.
We are planning on making some changes in our donation structure in
2000, so you might want to email me, hart@pobox.com beforehand.
*END THE SMALL PRINT! FOR PUBLIC DOMAIN ETEXTS*
Ver.04.29.93*END*

ALICE’S ADVENTURES IN
WONDERLAND

Lewis Carroll

THE MILLENNIUM FULCRUM EDITION 3.0

Contents

1 Down the Rabbit-Hole 13

2 The Pool of Tears 19

3 A Caucus-Race and a Long Tale 25

4 The Rabbit Sends in a Little Bill 31

5 Advice from a Caterpillar 37

6 Pig and
```

**Full original cited chunk:**

```text
Hole 13

2 The Pool of Tears 19

3 A Caucus-Race and a Long Tale 25

4 The Rabbit Sends in a Little Bill 31

5 Advice from a Caterpillar 37

6 Pig and Pepper 43

7 A Mad Tea-Party 51

8 The Queen’s Croquet-Ground 59

9 The Mock Turtle’s Story 67

10 The Lobster Quadrille 73

11 Who Stole the Tarts? 81

12 Alice’s Evidence 87

12 CONTENTS

Chapter 1

Down the Rabbit-Hole

Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, ‘and what is the use of a book,’ thought Alice ‘without pictures or conversation?’
So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.
There was nothing so VERY remarkable in that; nor did Alice think it so
VERY much out of the way to hear the Rabbit say to itself, ‘Oh dear! Oh dear! I shall be late!’ (when she thought it over afterwards, it occurred to her that she
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00012` (pages 13–14)

```text
t of the way to hear the Rabbit say to itself, ‘Oh dear! Oh dear! I shall be late!’ (when she thought it over afterwards, it occurred to her that she ought to have wondered at this, but at the time it all seemed quite natural); but when the Rabbit actually TOOK A WATCH OUT OF
ITS WAISTCOAT- POCKET, and looked at it, and then hurried on, Alice started to her feet, for it flashed across her mind that she had never before seen a rabbit with either a waistcoat-pocket, or a watch to take out of it, and burning with curiosity, she ran across the field after it, and fortunately was just in time to see it pop down a large rabbit-hole under the hedge.
In another moment down went Alice after it, never once considering how in the world she was to get out again.
The rabbit-hole went straight on like a tunnel for some way, and then dipped suddenly down, so suddenly that Alice had not a moment to think about stopping herself before she found herself falling down a very deep well.
Either the well was very deep, or she fell very slowly, for she had plenty of time as she went down to look about her and to wonder what was going

14 CHAPTER 1. DOWN THE RABBIT-HOLE

to happen next. First, she tried to
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q006

**Question:** Approximately how tall was the little door Alice found?

**Reference answer:** About fifteen inches high.

**Final generated answer:** The little door was about fifteen inches high.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** The little door was about fifteen inches high.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 15, 16
- **Exact supporting span(s):**
  - `S1`:

```text
little door about fifteen inches high
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S1 context — supports claim(s) C1

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00017`
- Cited page(s): 15, 16
- Parsed chunk page range: 15–16

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00016` (pages 15–15)

```text
me the truth: did you ever eat a bat?’ when suddenly, thump! thump! down she came upon a heap of sticks and dry leaves, and the fall was over.
Alice was not a bit hurt, and she jumped up on to her feet in a moment:
she looked up, but it was all dark overhead; before her was another long passage, and the White Rabbit was still in sight, hurrying down it. There was not a moment to be lost: away went Alice like the wind, and was just in time to hear it say, as it turned a corner, ‘Oh my ears and whiskers, how late it’s getting!’ She was close behind it when she turned the corner, but the Rabbit was no longer to be seen: she found herself in a long, low hall, which was lit up by a row of lamps hanging from the roof.
There were doors all round the hall, but they were all locked; and when
Alice had been all the way down one side and up the other, trying every door, she walked sadly down the middle, wondering how she was ever to get out again.
Suddenly she came upon a little three-legged table, all made of solid glass;
there was nothing on it except a tiny golden key, and Alice’s first thought was that it might belong to one of the doors of the hall; but, alas! either the locks were too
```

**Full original cited chunk:**

```text
it except a tiny golden key, and Alice’s first thought was that it might belong to one of the doors of the hall; but, alas! either the locks were too large, or the key was too small, but at any rate it would not open any of them. However, on the second time round, she came upon a low curtain she had not noticed before, and behind it was a little door about fifteen inches high: she tried the little golden key in the lock, and to her great delight it fitted!
Alice opened the door and found that it led into a small passage, not much larger than a rat-hole: she knelt down and looked along the passage into the loveliest garden you ever saw. How she longed to get out of that dark hall, and wander about among those beds of bright flowers and those cool fountains, but she could not even get her head though the doorway;
‘and even if my head would go through,’ thought poor Alice, ‘it would be of very little use without my shoulders. Oh, how I wish I could shut up like a telescope! I think I could, if I only know how to begin.’ For, you see, so many out-of-the-way things had happened lately, that Alice had begun to think that very few things indeed were really impossible.

16 CHAPTER 1. DOWN
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00018` (pages 15–16)

```text
many out-of-the-way things had happened lately, that Alice had begun to think that very few things indeed were really impossible.

16 CHAPTER 1. DOWN THE RABBIT-HOLE

There seemed to be no use in waiting by the little door, so she went back to the table, half hoping she might find another key on it, or at any rate a book of rules for shutting people up like telescopes: this time she found a little bottle on it, (‘which certainly was not here before,’ said Alice,) and round the neck of the bottle was a paper label, with the words ‘DRINK ME’ beautifully printed on it in large letters.
It was all very well to say ‘Drink me,’ but the wise little Alice was not going to do THAT in a hurry. ‘No, I’ll look first,’ she said, ‘and see whether it’s marked “poison” or not’; for she had read several nice little histories about children who had got burnt, and eaten up by wild beasts and other unpleasant things, all because they WOULD not remember the simple rules their friends had taught them: such as, that a red-hot poker will burn you if you hold it too long; and that if you cut your finger VERY deeply with a knife, it usually bleeds; and she had never forgotten that, if you drink much from a
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q012

**Question:** What activity did the Dodo recommend to get everyone dry?

**Reference answer:** A Caucus-race.

**Final generated answer:** The Dodo recommended a Caucus-race.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** The Dodo recommended a Caucus-race.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 26
- **Exact supporting span(s):**
  - `S1`:

```text
best thing to get us dry would be a Caucus-race
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S1 context — supports claim(s) C1

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00035`
- Cited page(s): 26
- Parsed chunk page range: 26–26

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00034` (pages 25–26)

```text
the Lory, with a shiver.
‘I beg your pardon!’ said the Mouse, frowning, but very politely: ‘Did you speak?’
‘Not I!’ said the Lory hastily.

26 CHAPTER 3. A CAUCUS-RACE AND A LONG TALE

‘I thought you did,’ said the Mouse. ‘–I proceed. “Edwin and Morcar, the earls of Mercia and Northumbria, declared for him: and even Stigand, the patriotic archbishop of Canterbury, found it advisable–”’
‘Found WHAT?’ said the Duck.
‘Found IT,’ the Mouse replied rather crossly: ‘of course you know what “it” means.’
‘I know what “it” means well enough, when I find a thing,’ said the Duck:
‘it’s generally a frog or a worm. The question is, what did the archbishop find?’
The Mouse did not notice this question, but hurriedly went on, ‘“–found it advisable to go with Edgar Atheling to meet William and offer him the crown. William’s conduct at first was moderate. But the insolence of his
Normans–” How are you getting on now, my dear?’ it continued, turning to
Alice as it spoke.
‘As wet as ever,’ said Alice in a melancholy tone: ‘it doesn’t seem to dry me at all.’
‘In that case,’ said the Dodo solemnly, rising to its feet, ‘I move that the meeting adjourn, for the immediate adoption of more energetic remed
```

**Full original cited chunk:**

```text
all.’
‘In that case,’ said the Dodo solemnly, rising to its feet, ‘I move that the meeting adjourn, for the immediate adoption of more energetic remedies–’
‘Speak English!’ said the Eaglet. ‘I don’t know the meaning of half those long words, and, what’s more, I don’t believe you do either!’ And the Eaglet bent down its head to hide a smile: some of the other birds tittered audibly.
‘What I was going to say,’ said the Dodo in an offended tone, ‘was, that the best thing to get us dry would be a Caucus-race.’
‘What IS a Caucus-race?’ said Alice; not that she wanted much to know, but the Dodo had paused as if it thought that SOMEBODY ought to speak, and no one else seemed inclined to say anything.
‘Why,’ said the Dodo, ‘the best way to explain it is to do it.’ (And, as you might like to try the thing yourself, some winter day, I will tell you how the Dodo managed it.)
First it marked out a race-course, in a sort of circle, (‘the exact shape doesn’t matter,’ it said,) and then all the party were placed along the course, here and there. There was no ‘One, two, three, and away,’ but they began running when they liked, and left offwhen they liked, so that it was not easy to know when the r
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00036` (pages 26–27)

```text
re was no ‘One, two, three, and away,’ but they began running when they liked, and left offwhen they liked, so that it was not easy to know when the race was over. However, when they had been running half an hour or so, and were quite dry again, the Dodo suddenly called out ‘The race is over!’ and they all crowded round it, panting, and asking, ‘But who has won?’
This question the Dodo could not answer without a great deal of thought,

and it sat for a long time with one finger pressed upon its forehead (the position in which you usually see Shakespeare, in the pictures of him), while the rest waited in silence. At last the Dodo said, ‘EVERYBODY has won, and all must have prizes.’
‘But who is to give the prizes?’ quite a chorus of voices asked.
‘Why, SHE, of course,’ said the Dodo, pointing to Alice with one finger;
and the whole party at once crowded round her, calling out in a confused way, ‘Prizes! Prizes!’
Alice had no idea what to do, and in despair she put her hand in her pocket, and pulled out a box of comfits, (luckily the salt water had not got into it), and handed them round as prizes. There was exactly one a-piece all round.
‘But she must have a prize herself, you know,’
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q015

**Question:** What name was engraved on the brass plate at the Rabbit's house?

**Reference answer:** W. RABBIT.

**Final generated answer:** W. RABBIT

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** The brass plate was engraved “W. RABBIT.”
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 31, 32
- **Exact supporting span(s):**
  - `S1`:

```text
name ‘W. RABBIT’ engraved upon it
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S1 context — supports claim(s) C1

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00042`
- Cited page(s): 31, 32
- Parsed chunk page range: 31–32

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00041` (pages 30–31)

```text
here, and I’m sure she’s the best cat in the world! Oh, my dear Dinah! I wonder if I shall ever see you any more!’ And here poor Alice began to cry again, for she felt very lonely and low-spirited. In a little while, however, she again heard a little pattering of footsteps in the distance, and she looked up eagerly, half hoping that the
Mouse had changed his mind, and was coming back to finish his story.

Chapter 4

The Rabbit Sends in a Little
Bill

It was the White Rabbit, trotting slowly back again, and looking anxiously about as it went, as if it had lost something; and she heard it muttering to itself ‘The Duchess! The Duchess! Oh my dear paws! Oh my fur and whiskers! She’ll get me executed, as sure as ferrets are ferrets! Where CAN I have dropped them, I wonder?’ Alice guessed in a moment that it was looking for the fan and the pair of white kid gloves, and she very good-naturedly began hunting about for them, but they were nowhere to be seen–everything seemed to have changed since her swim in the pool, and the great hall, with the glass table and the little door, had vanished completely.
Very soon the Rabbit noticed Alice, as she went hunting about, and called out to her in
```

**Full original cited chunk:**

```text
the glass table and the little door, had vanished completely.
Very soon the Rabbit noticed Alice, as she went hunting about, and called out to her in an angry tone, ‘Why, Mary Ann, what ARE you doing out here?
Run home this moment, and fetch me a pair of gloves and a fan! Quick, now!’
And Alice was so much frightened that she ran offat once in the direction it pointed to, without trying to explain the mistake it had made.
‘He took me for his housemaid,’ she said to herself as she ran. ‘How surprised he’ll be when he finds out who I am! But I’d better take him his fan and gloves–that is, if I can find them.’ As she said this, she came upon a neat little house, on the door of which was a bright brass plate with the name ‘W. RABBIT’ engraved upon it. She went in without knocking, and hurried upstairs, in great fear lest she should meet the real Mary Ann, and be turned out of the house before she had found the fan and gloves.
‘How queer it seems,’ Alice said to herself, ‘to be going messages for a rabbit! I suppose Dinah’ll be sending me on messages next!’ And she began

32 CHAPTER 4. THE RABBIT SENDS IN A LITTLE BILL

fancying the sort of thing that would happen: ‘“Miss Alice! Come h
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00043` (pages 31–32)

```text
on messages next!’ And she began

32 CHAPTER 4. THE RABBIT SENDS IN A LITTLE BILL

fancying the sort of thing that would happen: ‘“Miss Alice! Come here directly, and get ready for your walk!” “Coming in a minute, nurse! But I’ve got to see that the mouse doesn’t get out.” Only I don’t think,’ Alice went on, ‘that they’d let Dinah stop in the house if it began ordering people about like that!’
By this time she had found her way into a tidy little room with a table in the window, and on it (as she had hoped) a fan and two or three pairs of tiny white kid gloves: she took up the fan and a pair of the gloves, and was just going to leave the room, when her eye fell upon a little bottle that stood near the looking- glass. There was no label this time with the words
‘DRINK ME,’ but nevertheless she uncorked it and put it to her lips. ‘I know
SOMETHING interesting is sure to happen,’ she said to herself, ‘whenever
I eat or drink anything; so I’ll just see what this bottle does. I do hope it’ll make me grow large again, for really I’m quite tired of being such a tiny little thing!’
It did so indeed, and much sooner than she had expected: before she had drunk half the bottle, she found her
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q018

**Question:** Why did the Pigeon call Alice a serpent?

**Reference answer:** The Pigeon was guarding eggs and concluded that Alice was a serpent because Alice admitted that little girls eat eggs too.

**Final generated answer:** The Pigeon called Alice a serpent because her neck had grown very long, causing her to appear like a serpent wriggling down from the sky. The Pigeon believed Alice was looking for eggs and stated that any creature with such a neck that ate eggs must be a serpent.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** The Pigeon treated Alice’s long neck and skyward appearance as serpent-like.
- **Source ID(s):** `S2`
- **Cited page(s):** S2: 41, 42
- **Exact supporting span(s):**
  - `S2`:

```text
come wriggling down from the sky
```
  - `S2`:

```text
never ONE with such a
```
  - `S2`:

```text
neck as that! No, no! You’re a serpent
```

#### Claim C2

- **Claim text:** The Pigeon believed Alice was looking for eggs and reasoned that an egg-eating, long-necked creature was a serpent.
- **Source ID(s):** `S2`, `S3`
- **Cited page(s):** S2: 41, 42; S3: 42
- **Exact supporting span(s):**
  - `S2`:

```text
little girls eat eggs quite as much as serpents do
```
  - `S3`:

```text
You’re looking for eggs, I know THAT well enough
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S2 context — supports claim(s) C1, C2

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00063`
- Cited page(s): 41, 42
- Parsed chunk page range: 41–42

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00062` (pages 41–41)

```text
ent. She had just succeeded in curving it down into a graceful zigzag, and was going to dive in among the leaves, which she found to be nothing but the tops of the trees under which she had been wandering, when a sharp hiss made her draw back in a hurry: a large pigeon had flown into her face, and was beating her violently with its wings.
‘Serpent!’ screamed the Pigeon.
‘I’m NOT a serpent!’ said Alice indignantly. ‘Let me alone!’
‘Serpent, I say again!’ repeated the Pigeon, but in a more subdued tone, and added with a kind of sob, ‘I’ve tried every way, and nothing seems to suit them!’
‘I haven’t the least idea what you’re talking about,’ said Alice.
‘I’ve tried the roots of trees, and I’ve tried banks, and I’ve tried hedges,’ the Pigeon went on, without attending to her; ‘but those serpents! There’s no pleasing them!’
Alice was more and more puzzled, but she thought there was no use in saying anything more till the Pigeon had finished.
‘As if it wasn’t trouble enough hatching the eggs,’ said the Pigeon; ‘but
I must be on the look-out for serpents night and day! Why, I haven’t had a wink of sleep these three weeks!’
‘I’m very sorry you’ve been annoyed,’ said Alice, who was beginnin
```

**Full original cited chunk:**

```text
for serpents night and day! Why, I haven’t had a wink of sleep these three weeks!’
‘I’m very sorry you’ve been annoyed,’ said Alice, who was beginning to see its meaning.
‘And just as I’d taken the highest tree in the wood,’ continued the Pigeon, raising its voice to a shriek, ‘and just as I was thinking I should be free of them at last, they must needs come wriggling down from the sky! Ugh,
Serpent!’
‘But I’m NOT a serpent, I tell you!’ said Alice. ‘I’m a–I’m a–’
‘Well! WHAT are you?’ said the Pigeon. ‘I can see you’re trying to invent something!’
‘I–I’m a little girl,’ said Alice, rather doubtfully, as she remembered the number of changes she had gone through that day.
‘A likely story indeed!’ said the Pigeon in a tone of the deepest contempt.
‘I’ve seen a good many little girls in my time, but never ONE with such a

42 CHAPTER 5. ADVICE FROM A CATERPILLAR

neck as that! No, no! You’re a serpent; and there’s no use denying it. I suppose you’ll be telling me next that you never tasted an egg!’
‘I HAVE tasted eggs, certainly,’ said Alice, who was a very truthful child;
‘but little girls eat eggs quite as much as serpents do, you know.’
‘I don’t believe it,’ said the Pigeon; ‘but i
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00064` (pages 42–42)

```text
lice, who was a very truthful child;
‘but little girls eat eggs quite as much as serpents do, you know.’
‘I don’t believe it,’ said the Pigeon; ‘but if they do, why then they’re a kind of serpent, that’s all I can say.’
This was such a new idea to Alice, that she was quite silent for a minute or two, which gave the Pigeon the opportunity of adding, ‘You’re looking for eggs, I know THAT well enough; and what does it matter to me whether you’re a little girl or a serpent?’
‘It matters a good deal to ME,’ said Alice hastily; ‘but I’m not looking for eggs, as it happens; and if I was, I shouldn’t want YOURS: I don’t like them raw.’
‘Well, be off, then!’ said the Pigeon in a sulky tone, as it settled down again into its nest. Alice crouched down among the trees as well as she could, for her neck kept getting entangled among the branches, and every now and then she had to stop and untwist it. After a while she remembered that she still held the pieces of mushroom in her hands, and she set to work very carefully, nibbling first at one and then at the other, and growing sometimes taller and sometimes shorter, until she had succeeded in bringing herself down to her usual height.
It was so l
```

#### S3 context — supports claim(s) C2

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00064`
- Cited page(s): 42
- Parsed chunk page range: 42–42

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00063` (pages 41–42)

```text
for serpents night and day! Why, I haven’t had a wink of sleep these three weeks!’
‘I’m very sorry you’ve been annoyed,’ said Alice, who was beginning to see its meaning.
‘And just as I’d taken the highest tree in the wood,’ continued the Pigeon, raising its voice to a shriek, ‘and just as I was thinking I should be free of them at last, they must needs come wriggling down from the sky! Ugh,
Serpent!’
‘But I’m NOT a serpent, I tell you!’ said Alice. ‘I’m a–I’m a–’
‘Well! WHAT are you?’ said the Pigeon. ‘I can see you’re trying to invent something!’
‘I–I’m a little girl,’ said Alice, rather doubtfully, as she remembered the number of changes she had gone through that day.
‘A likely story indeed!’ said the Pigeon in a tone of the deepest contempt.
‘I’ve seen a good many little girls in my time, but never ONE with such a

42 CHAPTER 5. ADVICE FROM A CATERPILLAR

neck as that! No, no! You’re a serpent; and there’s no use denying it. I suppose you’ll be telling me next that you never tasted an egg!’
‘I HAVE tasted eggs, certainly,’ said Alice, who was a very truthful child;
‘but little girls eat eggs quite as much as serpents do, you know.’
‘I don’t believe it,’ said the Pigeon; ‘but i
```

**Full original cited chunk:**

```text
lice, who was a very truthful child;
‘but little girls eat eggs quite as much as serpents do, you know.’
‘I don’t believe it,’ said the Pigeon; ‘but if they do, why then they’re a kind of serpent, that’s all I can say.’
This was such a new idea to Alice, that she was quite silent for a minute or two, which gave the Pigeon the opportunity of adding, ‘You’re looking for eggs, I know THAT well enough; and what does it matter to me whether you’re a little girl or a serpent?’
‘It matters a good deal to ME,’ said Alice hastily; ‘but I’m not looking for eggs, as it happens; and if I was, I shouldn’t want YOURS: I don’t like them raw.’
‘Well, be off, then!’ said the Pigeon in a sulky tone, as it settled down again into its nest. Alice crouched down among the trees as well as she could, for her neck kept getting entangled among the branches, and every now and then she had to stop and untwist it. After a while she remembered that she still held the pieces of mushroom in her hands, and she set to work very carefully, nibbling first at one and then at the other, and growing sometimes taller and sometimes shorter, until she had succeeded in bringing herself down to her usual height.
It was so l
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00065` (pages 42–43)

```text
en at the other, and growing sometimes taller and sometimes shorter, until she had succeeded in bringing herself down to her usual height.
It was so long since she had been anything near the right size, that it felt quite strange at first; but she got used to it in a few minutes, and began talking to herself, as usual. ‘Come, there’s half my plan done now! How puzzling all these changes are! I’m never sure what I’m going to be, from one minute to another! However, I’ve got back to my right size: the next thing is, to get into that beautiful garden–how IS that to be done, I wonder?’
As she said this, she came suddenly upon an open place, with a little house in it about four feet high. ‘Whoever lives there,’ thought Alice, ‘it’ll never do to come upon them THIS size: why, I should frighten them out of their wits!’ So she began nibbling at the righthand bit again, and did not venture to go near the house till she had brought herself down to nine inches high.

Chapter 6

Pig and Pepper

For a minute or two she stood looking at the house, and wondering what to do next, when suddenly a footman in livery came running out of the wood–(she considered him to be a footman because he was in li
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q020

**Question:** Which two residents did the Cheshire Cat direct Alice toward, and what did it say about them?

**Reference answer:** The Hatter and the March Hare; the Cat said they were both mad.

**Final generated answer:** The Cheshire Cat directed Alice toward a Hatter and a March Hare, stating that they are both mad.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** The Cheshire Cat directed Alice toward a Hatter and a March Hare.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 48
- **Exact supporting span(s):**
  - `S1`:

```text
lives a
Hatter:
```
  - `S1`:

```text
lives a March Hare
```

#### Claim C2

- **Claim text:** The Cheshire Cat said both were mad.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 48
- **Exact supporting span(s):**
  - `S1`:

```text
they’re both mad
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S1 context — supports claim(s) C1, C2

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00076`
- Cited page(s): 48
- Parsed chunk page range: 48–48

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00075` (pages 47–48)

```text
he wood. ‘If it had grown up,’ she said to herself, ‘it would have made a dreadfully ugly child: but it makes rather a handsome pig, I think.’ And she began thinking over other children she knew, who might do very well as pigs, and was just saying to herself, ‘if one only knew the right way to change them–’ when she was a little startled by seeing the Cheshire
Cat sitting on a bough of a tree a few yards off.
The Cat only grinned when it saw Alice. It looked good- natured, she thought: still it had VERY long claws and a great many teeth, so she felt that it ought to be treated with respect.
‘Cheshire Puss,’ she began, rather timidly, as she did not at all know whether it would like the name: however, it only grinned a little wider.
‘Come, it’s pleased so far,’ thought Alice, and she went on. ‘Would you tell me, please, which way I ought to go from here?’
‘That depends a good deal on where you want to get to,’ said the Cat.
‘I don’t much care where–’ said Alice.
‘Then it doesn’t matter which way you go,’ said the Cat.

48 CHAPTER 6. PIG AND PEPPER

‘–so long as I get SOMEWHERE,’ Alice added as an explanation.
‘Oh, you’re sure to do that,’ said the Cat, ‘if you only walk long enough.
```

**Full original cited chunk:**

```text
G AND PEPPER

‘–so long as I get SOMEWHERE,’ Alice added as an explanation.
‘Oh, you’re sure to do that,’ said the Cat, ‘if you only walk long enough.’
Alice felt that this could not be denied, so she tried another question.
‘What sort of people live about here?’
‘In THAT direction,’ the Cat said, waving its right paw round, ‘lives a
Hatter: and in THAT direction,’ waving the other paw, ‘lives a March Hare.
Visit either you like: they’re both mad.’
‘But I don’t want to go among mad people,’ Alice remarked.
‘Oh, you can’t help that,’ said the Cat: ‘we’re all mad here. I’m mad.
You’re mad.’
‘How do you know I’m mad?’ said Alice.
‘You must be,’ said the Cat, ‘or you wouldn’t have come here.’
Alice didn’t think that proved it at all; however, she went on ‘And how do you know that you’re mad?’
‘To begin with,’ said the Cat, ‘a dog’s not mad. You grant that?’
‘I suppose so,’ said Alice.
‘Well, then,’ the Cat went on, ‘you see, a dog growls when it’s angry, and wags its tail when it’s pleased. Now I growl when I’m pleased, and wag my tail when I’m angry. Therefore I’m mad.’
‘I call it purring, not growling,’ said Alice.
‘Call it what you like,’ said the Cat. ‘Do you play croquet with the
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00077` (pages 48–49)

```text
en I’m angry. Therefore I’m mad.’
‘I call it purring, not growling,’ said Alice.
‘Call it what you like,’ said the Cat. ‘Do you play croquet with the Queen to-day?’
‘I should like it very much,’ said Alice, ‘but I haven’t been invited yet.’
‘You’ll see me there,’ said the Cat, and vanished.
Alice was not much surprised at this, she was getting so used to queer things happening. While she was looking at the place where it had been, it suddenly appeared again.
‘By-the-bye, what became of the baby?’ said the Cat. ‘I’d nearly forgotten to ask.’
‘It turned into a pig,’ Alice quietly said, just as if it had come back in a natural way.
‘I thought it would,’ said the Cat, and vanished again.
Alice waited a little, half expecting to see it again, but it did not appear, and after a minute or two she walked on in the direction in which the March
Hare was said to live. ‘I’ve seen hatters before,’ she said to herself; ‘the
March Hare will be much the most interesting, and perhaps as this is May it won’t be raving mad–at least not so mad as it was in March.’ As she said

this, she looked up, and there was the Cat again, sitting on a branch of a tree.
‘Did you say pig, or fig?’ said the Cat.
‘I s
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q024

**Question:** What served as the balls, mallets, and arches in the Queen's croquet game?

**Reference answer:** Hedgehogs were the balls, flamingoes were the mallets, and soldiers bent over to form the arches.

**Final generated answer:** In the Queen's croquet game, live hedgehogs served as the balls, live flamingoes served as the mallets, and soldiers who doubled themselves up and stood on their hands and feet served as the arches.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** Live hedgehogs served as the croquet balls.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 61, 62
- **Exact supporting span(s):**
  - `S1`:

```text
balls were live hedgehogs
```

#### Claim C2

- **Claim text:** Live flamingoes served as the mallets.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 61, 62
- **Exact supporting span(s):**
  - `S1`:

```text
mallets live flamingoes
```

#### Claim C3

- **Claim text:** Soldiers doubled over on their hands and feet to form the arches.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 61, 62
- **Exact supporting span(s):**
  - `S1`:

```text
soldiers had to double themselves up and to stand on their hands and feet, to make the arches
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S1 context — supports claim(s) C1, C2, C3

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00097`
- Cited page(s): 61, 62
- Parsed chunk page range: 61–62

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00096` (pages 61–62)

```text
d she put them into a large flower-pot that stood near. The three soldiers wandered about for a minute or two, looking for them, and then quietly marched offafter the others.
‘Are their heads off?’ shouted the Queen.
‘Their heads are gone, if it please your Majesty!’ the soldiers shouted in reply.
‘That’s right!’ shouted the Queen. ‘Can you play croquet?’
The soldiers were silent, and looked at Alice, as the question was evidently meant for her.
‘Yes!’ shouted Alice.
‘Come on, then!’ roared the Queen, and Alice joined the procession, wondering very much what would happen next.
‘It’s–it’s a very fine day!’ said a timid voice at her side. She was walking by the White Rabbit, who was peeping anxiously into her face.
‘Very,’ said Alice: ‘–where’s the Duchess?’
‘Hush! Hush!’ said the Rabbit in a low, hurried tone. He looked anxiously over his shoulder as he spoke, and then raised himself upon tiptoe, put his mouth close to her ear, and whispered ‘She’s under sentence of execution.’
‘What for?’ said Alice.
‘Did you say “What a pity!”?’ the Rabbit asked.

62 CHAPTER 8. THE QUEEN’S CROQUET-GROUND

‘No, I didn’t,’ said Alice: ‘I don’t think it’s at all a pity. I said “What for?”’
‘She boxed
```

**Full original cited chunk:**

```text
Rabbit asked.

62 CHAPTER 8. THE QUEEN’S CROQUET-GROUND

‘No, I didn’t,’ said Alice: ‘I don’t think it’s at all a pity. I said “What for?”’
‘She boxed the Queen’s ears–’ the Rabbit began. Alice gave a little scream of laughter. ‘Oh, hush!’ the Rabbit whispered in a frightened tone. ‘The
Queen will hear you! You see, she came rather late, and the Queen said–’
‘Get to your places!’ shouted the Queen in a voice of thunder, and people began running about in all directions, tumbling up against each other;
however, they got settled down in a minute or two, and the game began.
Alice thought she had never seen such a curious croquet-ground in her life;
it was all ridges and furrows; the balls were live hedgehogs, the mallets live flamingoes, and the soldiers had to double themselves up and to stand on their hands and feet, to make the arches.
The chief difficulty Alice found at first was in managing her flamingo:
she succeeded in getting its body tucked away, comfortably enough, under her arm, with its legs hanging down, but generally, just as she had got its neck nicely straightened out, and was going to give the hedgehog a blow with its head, it WOULD twist itself round and look up in he
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00098` (pages 62–62)

```text
s she had got its neck nicely straightened out, and was going to give the hedgehog a blow with its head, it WOULD twist itself round and look up in her face, with such a puzzled expression that she could not help bursting out laughing: and when she had got its head down, and was going to begin again, it was very provoking to find that the hedgehog had unrolled itself, and was in the act of crawling away: besides all this, there was generally a ridge or furrow in the way wherever she wanted to send the hedgehog to, and, as the doubled-up soldiers were always getting up and walking offto other parts of the ground,
Alice soon came to the conclusion that it was a very difficult game indeed.
The players all played at once without waiting for turns, quarrelling all the while, and fighting for the hedgehogs; and in a very short time the Queen was in a furious passion, and went stamping about, and shouting ‘Offwith his head!’ or ‘Offwith her head!’ about once in a minute.
Alice began to feel very uneasy: to be sure, she had not as yet had any dispute with the Queen, but she knew that it might happen any minute, ‘and then,’ thought she, ‘what would become of me? They’re dreadfully fond of b
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q027

**Question:** What final actions complete the first figure of the Lobster Quadrille?

**Reference answer:** The dancers change lobsters and retire in the same order, then return to land to finish the first figure.

**Final generated answer:** The final actions that complete the first figure of the Lobster Quadrille are changing lobsters again and returning to land.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** The dancers changed lobsters again.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 73, 74
- **Exact supporting span(s):**
  - `S1`:

```text
Change lobsters again!
```

#### Claim C2

- **Claim text:** The dancers returned to land to complete the first figure.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 73, 74
- **Exact supporting span(s):**
  - `S1`:

```text
Back to land again, and that’s all the first figure
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S1 context — supports claim(s) C1, C2

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00117`
- Cited page(s): 73, 74
- Parsed chunk page range: 73–74

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00116` (pages 72–73)

```text
remark. ‘Then the eleventh day must have been a holiday?’
‘Of course it was,’ said the Mock Turtle.
‘And how did you manage on the twelfth?’ Alice went on eagerly.
‘That’s enough about lessons,’ the Gryphon interrupted in a very decided tone: ‘tell her something about the games now.’

Chapter 10

The Lobster Quadrille

The Mock Turtle sighed deeply, and drew the back of one flapper across his eyes. He looked at Alice, and tried to speak, but for a minute or two sobs choked his voice. ‘Same as if he had a bone in his throat,’ said the Gryphon:
and it set to work shaking him and punching him in the back. At last the
Mock Turtle recovered his voice, and, with tears running down his cheeks, he went on again:–
‘You may not have lived much under the sea–’ (‘I haven’t,’ said Alice)– ‘and perhaps you were never even introduced to a lobster–’ (Alice began to say ‘I once tasted–’ but checked herself hastily, and said ‘No, never’) ‘–so you can have no idea what a delightful thing a Lobster Quadrille is!’
‘No, indeed,’ said Alice. ‘What sort of a dance is it?’
‘Why,’ said the Gryphon, ‘you first form into a line along the sea-shore–’
‘Two lines!’ cried the Mock Turtle. ‘Seals, turtles, salmon
```

**Full original cited chunk:**

```text
a dance is it?’
‘Why,’ said the Gryphon, ‘you first form into a line along the sea-shore–’
‘Two lines!’ cried the Mock Turtle. ‘Seals, turtles, salmon, and so on;
then, when you’ve cleared all the jelly-fish out of the way–’
‘THAT generally takes some time,’ interrupted the Gryphon.
‘–you advance twice–’
‘Each with a lobster as a partner!’ cried the Gryphon.
‘Of course,’ the Mock Turtle said: ‘advance twice, set to partners–’ ‘–change lobsters, and retire in same order,’ continued the Gryphon.
‘Then, you know,’ the Mock Turtle went on, ‘you throw the–’
‘The lobsters!’ shouted the Gryphon, with a bound into the air.
‘–as far out to sea as you can–’
‘Swim after them!’ screamed the Gryphon.
‘Turn a somersault in the sea!’ cried the Mock Turtle, capering wildly about.

74 CHAPTER 10. THE LOBSTER QUADRILLE

‘Change lobsters again!’ yelled the Gryphon at the top of its voice.
‘Back to land again, and that’s all the first figure,’ said the Mock Turtle, suddenly dropping his voice; and the two creatures, who had been jumping about like mad things all this time, sat down again very sadly and quietly, and looked at Alice.
‘It must be a very pretty dance,’ said Alice timidly.
‘Would you like
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00118` (pages 74–74)

```text
ings all this time, sat down again very sadly and quietly, and looked at Alice.
‘It must be a very pretty dance,’ said Alice timidly.
‘Would you like to see a little of it?’ said the Mock Turtle.
‘Very much indeed,’ said Alice.
‘Come, let’s try the first figure!’ said the Mock Turtle to the Gryphon.
‘We can do without lobsters, you know. Which shall sing?’
‘Oh, YOU sing,’ said the Gryphon. ‘I’ve forgotten the words.’
So they began solemnly dancing round and round Alice, every now and then treading on her toes when they passed too close, and waving their forepaws to mark the time, while the Mock Turtle sang this, very slowly and sadly:–

‘“Will you walk a little faster?” said a whiting to a snail.
“There’s a porpoise close behind us, and he’s treading on my tail.
See how eagerly the lobsters and the turtles all advance!
They are waiting on the shingle–will you come and join the dance?
Will you, won’t you, will you, won’t you, will you join the dance?
Will you, won’t you, will you, won’t you, won’t you join the dance?
“You can really have no notion how delightful it will be
When they take us up and throw us, with the lobsters, out to sea!”
But the snail replied “Too far, too far!” an
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:

## q029

**Question:** Who was the next witness after the Hatter, and what did she say the tarts were mostly made of?

**Reference answer:** The Duchess's cook; she said the tarts were mostly made of pepper.

**Final generated answer:** The next witness after the Hatter was the Duchess's cook. She said the tarts were made of pepper, mostly.

**Final status:** `answered`

### Material claim map

#### Claim C1

- **Claim text:** The witness after the Hatter was the Duchess’s cook.
- **Source ID(s):** `S3`
- **Cited page(s):** S3: 85
- **Exact supporting span(s):**
  - `S3`:

```text
next witness was the Duchess’s cook
```

#### Claim C2

- **Claim text:** The cook said the tarts were made mostly of pepper.
- **Source ID(s):** `S1`
- **Cited page(s):** S1: 85, 86, 87
- **Exact supporting span(s):**
  - `S1`:

```text
Pepper, mostly
```

### Full cited chunks with local surrounding context

Immediate adjacent chunks are included verbatim. Fixed-size overlap may repeat text; no relevance summary has been invented.

#### S3 context — supports claim(s) C1

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00135`
- Cited page(s): 85
- Parsed chunk page range: 85–85

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00134` (pages 84–85)

```text
‘But what did the Dormouse say?’ one of the jury asked.
‘That I can’t remember,’ said the Hatter.
‘You MUST remember,’ remarked the King, ‘or I’ll have you executed.’
The miserable Hatter dropped his teacup and bread-and-butter, and went down on one knee. ‘I’m a poor man, your Majesty,’ he began.
‘You’re a very poor speaker,’ said the King.
Here one of the guinea-pigs cheered, and was immediately suppressed by the officers of the court. (As that is rather a hard word, I will just explain to you how it was done. They had a large canvas bag, which tied up at the mouth with strings: into this they slipped the guinea-pig, head first, and then sat upon it.)
‘I’m glad I’ve seen that done,’ thought Alice. ‘I’ve so often read in the newspapers, at the end of trials, “There was some attempts at applause, which was immediately suppressed by the officers of the court,” and I never understood what it meant till now.’
‘If that’s all you know about it, you may stand down,’ continued the
King.

‘I can’t go no lower,’ said the Hatter: ‘I’m on the floor, as it is.’
‘Then you may SIT down,’ the King replied.
Here the other guinea-pig cheered, and was suppressed.
‘Come, that finished the guinea-pigs
```

**Full original cited chunk:**

```text
oor, as it is.’
‘Then you may SIT down,’ the King replied.
Here the other guinea-pig cheered, and was suppressed.
‘Come, that finished the guinea-pigs!’ thought Alice. ‘Now we shall get on better.’
‘I’d rather finish my tea,’ said the Hatter, with an anxious look at the
Queen, who was reading the list of singers.
‘You may go,’ said the King, and the Hatter hurriedly left the court, without even waiting to put his shoes on.
‘–and just take his head offoutside,’ the Queen added to one of the officers: but the Hatter was out of sight before the officer could get to the door.
‘Call the next witness!’ said the King.
The next witness was the Duchess’s cook. She carried the pepper-box in her hand, and Alice guessed who it was, even before she got into the court, by the way the people near the door began sneezing all at once.
‘Give your evidence,’ said the King.
‘Shan’t,’ said the cook.
The King looked anxiously at the White Rabbit, who said in a low voice,
‘Your Majesty must cross-examine THIS witness.’
‘Well, if I must, I must,’ the King said, with a melancholy air, and, after folding his arms and frowning at the cook till his eyes were nearly out of sight, he said in a deep voice, ‘What
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00136` (pages 85–87)

```text
id, with a melancholy air, and, after folding his arms and frowning at the cook till his eyes were nearly out of sight, he said in a deep voice, ‘What are tarts made of?’
‘Pepper, mostly,’ said the cook.
‘Treacle,’ said a sleepy voice behind her.
‘Collar that Dormouse,’ the Queen shrieked out. ‘Behead that Dormouse!
Turn that Dormouse out of court! Suppress him! Pinch him! Offwith his whiskers!’
For some minutes the whole court was in confusion, getting the Dormouse turned out, and, by the time they had settled down again, the cook had disappeared.
‘Never mind!’ said the King, with an air of great relief. ‘Call the next witness.’ And he added in an undertone to the Queen, ‘Really, my dear, YOU must cross-examine the next witness. It quite makes my forehead ache!’
Alice watched the White Rabbit as he fumbled over the list, feeling very curious to see what the next witness would be like, ‘–for they haven’t got much evidence YET,’ she said to herself. Imagine her surprise, when the
White Rabbit read out, at the top of his shrill little voice, the name ‘Alice!’

86 CHAPTER 11. WHO STOLE THE TARTS?

Chapter 12

Alice’s Evidence

‘Here!’ cried Alice, quite forgetting in the flurry of the
```

#### S1 context — supports claim(s) C2

- Chunk ID: `a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00136`
- Cited page(s): 85, 86, 87
- Parsed chunk page range: 85–87

**Preceding local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00135` (pages 85–85)

```text
oor, as it is.’
‘Then you may SIT down,’ the King replied.
Here the other guinea-pig cheered, and was suppressed.
‘Come, that finished the guinea-pigs!’ thought Alice. ‘Now we shall get on better.’
‘I’d rather finish my tea,’ said the Hatter, with an anxious look at the
Queen, who was reading the list of singers.
‘You may go,’ said the King, and the Hatter hurriedly left the court, without even waiting to put his shoes on.
‘–and just take his head offoutside,’ the Queen added to one of the officers: but the Hatter was out of sight before the officer could get to the door.
‘Call the next witness!’ said the King.
The next witness was the Duchess’s cook. She carried the pepper-box in her hand, and Alice guessed who it was, even before she got into the court, by the way the people near the door began sneezing all at once.
‘Give your evidence,’ said the King.
‘Shan’t,’ said the cook.
The King looked anxiously at the White Rabbit, who said in a low voice,
‘Your Majesty must cross-examine THIS witness.’
‘Well, if I must, I must,’ the King said, with a melancholy air, and, after folding his arms and frowning at the cook till his eyes were nearly out of sight, he said in a deep voice, ‘What
```

**Full original cited chunk:**

```text
id, with a melancholy air, and, after folding his arms and frowning at the cook till his eyes were nearly out of sight, he said in a deep voice, ‘What are tarts made of?’
‘Pepper, mostly,’ said the cook.
‘Treacle,’ said a sleepy voice behind her.
‘Collar that Dormouse,’ the Queen shrieked out. ‘Behead that Dormouse!
Turn that Dormouse out of court! Suppress him! Pinch him! Offwith his whiskers!’
For some minutes the whole court was in confusion, getting the Dormouse turned out, and, by the time they had settled down again, the cook had disappeared.
‘Never mind!’ said the King, with an air of great relief. ‘Call the next witness.’ And he added in an undertone to the Queen, ‘Really, my dear, YOU must cross-examine the next witness. It quite makes my forehead ache!’
Alice watched the White Rabbit as he fumbled over the list, feeling very curious to see what the next witness would be like, ‘–for they haven’t got much evidence YET,’ she said to herself. Imagine her surprise, when the
White Rabbit read out, at the top of his shrill little voice, the name ‘Alice!’

86 CHAPTER 11. WHO STOLE THE TARTS?

Chapter 12

Alice’s Evidence

‘Here!’ cried Alice, quite forgetting in the flurry of the
```

**Following local chunk:**

`a6c315f78fbb4c5cb9f16f08f28aed38:chunk:00137` (pages 85–87)

```text
oice, the name ‘Alice!’

86 CHAPTER 11. WHO STOLE THE TARTS?

Chapter 12

Alice’s Evidence

‘Here!’ cried Alice, quite forgetting in the flurry of the moment how large she had grown in the last few minutes, and she jumped up in such a hurry that she tipped over the jury-box with the edge of her skirt, upsetting all the jurymen on to the heads of the crowd below, and there they lay sprawling about, reminding her very much of a globe of goldfish she had accidentally upset the week before.
‘Oh, I BEG your pardon!’ she exclaimed in a tone of great dismay, and began picking them up again as quickly as she could, for the accident of the goldfish kept running in her head, and she had a vague sort of idea that they must be collected at once and put back into the jury-box, or they would die.
‘The trial cannot proceed,’ said the King in a very grave voice, ‘until all the jurymen are back in their proper places– ALL,’ he repeated with great emphasis, looking hard at Alice as he said do.
Alice looked at the jury-box, and saw that, in her haste, she had put the
Lizard in head downwards, and the poor little thing was waving its tail about in a melancholy way, being quite unable to move. She soon
```

### Owner sign-off

Owner correctness: [ ] 0 [ ] 1 [ ] 2  
Owner completeness: [ ] 0 [ ] 1 [ ] 2  
Owner groundedness: [ ] 0 [ ] 1 [ ] 2  
Owner citation/context check: [ ] PASS [ ] PARTIAL [ ] FAIL  
Owner note:
