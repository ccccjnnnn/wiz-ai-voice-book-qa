# Evaluation V2 — Owner Ground-Truth Review

> **CANDIDATE ONLY. Codex-generated annotation is not golden ground truth.**
> No case in this file has been run through production retrieval or QA. The dataset becomes
> `owner_reviewed` and later `frozen` only after the project owner checks the original text.

## Review minimum

For every case, verify the proposed status and reference answer. For answered cases, check each
claim against its exact span and preceding/following text. For no-answer cases, inspect every
plausible whole-document match. Edit or reject any case whose wording, context, or search coverage
is not defensible. Do not approve a split as a batch based only on counts.

## Summary

- Total candidates: **98**
- Lifecycle: **candidate**
- Human verified: **false**
- Retrieval/QA executed: **no**
- Fact families: **77**
- Replaced TEST cases: **23**

### By proposed split

| Split | Count |
|---|---:|
| `alice_dev_regression` | 60 |
| `alice_final_test` | 20 |
| `secret_garden_holdout` | 18 |

### By category

| Category | Count |
|---|---:|
| `local_context_reasoning` | 20 |
| `paraphrase_vocabulary_mismatch` | 7 |
| `contrastive_distractor` | 9 |
| `unanswerable_false_premise` | 8 |
| `ambiguous_underspecified` | 7 |
| `voice_like_noisy_text` | 9 |
| `multi_fact_single_context` | 10 |
| `direct_factual_single_source` | 23 |
| `multi_source_multi_fact` | 5 |

### By status / book / difficulty

| Dimension | Value | Count |
|---|---|---:|
| expected_status | `answered` | 83 |
| expected_status | `insufficient_evidence` | 8 |
| expected_status | `ambiguous` | 7 |
| source_book | `alice_in_wonderland` | 80 |
| source_book | `the_secret_garden` | 18 |
| difficulty | `hard` | 32 |
| difficulty | `medium` | 55 |
| difficulty | `easy` | 11 |
| review_tier | `DEEP_REVIEW` | 64 |
| review_tier | `FAST_CONFIRM` | 34 |

### Repair audit

- Removed TEST IDs: `at061`, `at062`, `at063`, `at064`, `at065`, `at066`, `at067`, `at069`, `at070`, `at071`, `at072`, `at074`, `at077`, `at078`, `at079`, `at080`, `at101`, `at103`, `at105`, `at107`, `at108`, `at111`, `at116`
- Replacement TEST IDs: `at102`, `at104`, `at106`, `at109`, `at110`, `at112`, `at113`, `at114`, `at115`, `at117`, `at118`, `at119`, `at120`, `at121`, `at122`, `at123`
- Cases moved between splits: **none**
- Annotation/category/negative/ambiguity repairs: `at075`, `at076`, `av044`, `av046`, `av047`, `av048`, `av049`, `av050`, `av051`, `av052`, `av053`, `av055`, `av057`, `c001`, `c002`, `c003`, `c004`, `c005`, `c006`, `q002`, `q007`, `q010`, `q011`, `q013`, `q018`, `q022`, `q023`, `q026`, `q027`, `sg085`, `sg086`, `sg087`, `sg094`, `sg095`, `sg096`, `sg097`, `sg098`, `sg099`
- Evidence context repackaged: **all 100 cases**
- Rejected Astra semantic findings and source reasoning: see `AUDIT_REPAIR_LOG.md`


### Needs owner attention

Every case requires an owner decision before freeze. All TEST and holdout cases are explicitly flagged for full review.

72 cases carry the explicit attention flag: `av037`, `av038`, `av039`, `av040`, `av044`, `av045`, `av046`, `av047`, `av048`, `av049`, `av050`, `av051`, `av052`, `av053`, `c001`, `c002`, `c003`, `c004`, `c005`, `c006`, `q009`, `q011`, `q013`, `q016`, `q018`, `q021`, `q022`, `q023`, `q024`, `q026`, `q027`, `q028`, `q029`, `q030`, `at068`, `at073`, `at075`, `at076`, `at102`, `at104`, `at106`, `at109`, `at110`, `at112`, `at113`, `at114`, `at115`, `at117`, `at118`, `at119`, `at120`, `at121`, `at122`, `at123`, `sg081`, `sg082`, `sg083`, `sg084`, `sg085`, `sg086`, `sg087`, `sg088`, `sg089`, `sg090`, `sg091`, `sg092`, `sg093`, `sg094`, `sg095`, `sg098`, `sg099`, `sg100`

Unresolved BLOCKED cases: **0**.

## Index by category

- **local_context_reasoning:** `av037`, `av038`, `av039`, `av040`, `av052`, `q011`, `q018`, `q021`, `q022`, `q023`, `at102`, `at113`, `at114`, `at119`, `at123`, `sg087`, `sg088`, `sg089`, `sg090`, `sg091`
- **paraphrase_vocabulary_mismatch:** `av041`, `av042`, `av043`, `q017`, `q020`, `sg092`, `sg093`
- **contrastive_distractor:** `av044`, `av045`, `c006`, `q013`, `at073`, `at110`, `at112`, `sg094`, `sg095`
- **unanswerable_false_premise:** `av046`, `av047`, `av048`, `av049`, `c001`, `c002`, `at075`, `at076`
- **ambiguous_underspecified:** `av050`, `av051`, `av053`, `c003`, `c004`, `sg098`, `sg099`
- **voice_like_noisy_text:** `av054`, `av055`, `av056`, `av057`, `av058`, `av059`, `av060`, `at104`, `sg100`
- **multi_fact_single_context:** `c005`, `q016`, `q024`, `q027`, `at106`, `at115`, `at118`, `at120`, `at121`, `sg085`
- **direct_factual_single_source:** `q001`, `q002`, `q003`, `q004`, `q005`, `q006`, `q007`, `q008`, `q010`, `q012`, `q014`, `q015`, `q019`, `q025`, `q030`, `at068`, `at109`, `at117`, `at122`, `sg081`, `sg082`, `sg083`, `sg084`
- **multi_source_multi_fact:** `q009`, `q026`, `q028`, `q029`, `sg086`

## Index by proposed split

- **alice_dev_regression:** `av037`, `av038`, `av039`, `av040`, `av041`, `av042`, `av043`, `av044`, `av045`, `av046`, `av047`, `av048`, `av049`, `av050`, `av051`, `av052`, `av053`, `av054`, `av055`, `av056`, `av057`, `av058`, `av059`, `av060`, `c001`, `c002`, `c003`, `c004`, `c005`, `c006`, `q001`, `q002`, `q003`, `q004`, `q005`, `q006`, `q007`, `q008`, `q009`, `q010`, `q011`, `q012`, `q013`, `q014`, `q015`, `q016`, `q017`, `q018`, `q019`, `q020`, `q021`, `q022`, `q023`, `q024`, `q025`, `q026`, `q027`, `q028`, `q029`, `q030`
- **alice_final_test:** `at068`, `at073`, `at075`, `at076`, `at102`, `at104`, `at106`, `at109`, `at110`, `at112`, `at113`, `at114`, `at115`, `at117`, `at118`, `at119`, `at120`, `at121`, `at122`, `at123`
- **secret_garden_holdout:** `sg081`, `sg082`, `sg083`, `sg084`, `sg085`, `sg086`, `sg087`, `sg088`, `sg089`, `sg090`, `sg091`, `sg092`, `sg093`, `sg094`, `sg095`, `sg098`, `sg099`, `sg100`

# alice_dev_regression

<details>
<summary><strong>av037</strong> · local_context_reasoning · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** In the tea-party scene, who does the Hatter mean by “he” in “he won’t do a thing I ask”?

**Proposed status:** `answered`

**Proposed reference answer:** He means Time.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `fact_av037`

**Evidence event:** `event_alice_hatter_time_quarrel`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** `q023`

**Tags:** `coreference`, `speaker_identity`

### Required claims and original context

#### C1: The pronoun “he” refers to the personified Time.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 53, "chapter": "7", "pdf_block": 5}`

**Exact supporting span:**

```text
If you knew Time as well as I do
```

**Preceding context:**

```text
‘Have you guessed the riddle yet?’ the Hatter said, turning to Alice again. ‘No, I give it up,’ Alice replied: ‘what’s the answer?’ ‘I haven’t the slightest idea,’ said the Hatter. ‘Nor I,’ said the March Hare. Alice sighed wearily. ‘I think you might do something better with the time,’ she said, ‘than waste it in asking riddles that have no answers.’
```

**Supporting paragraph/context:**

```text
‘If you knew Time as well as I do,’ said the Hatter, ‘you wouldn’t talk about wasting IT. It’s HIM.’
```

**Following context:**

```text
‘I don’t know what you mean,’ said Alice. ‘Of course you don’t!’ the Hatter said, tossing his head contemptuously. ‘I dare say you never even spoke to Time!’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The pronoun “he” refers to the personified Time.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 54, "chapter": "7", "pdf_block": 6}`

**Exact supporting span:**

```text
he won’t do a thing I ask
```

**Preceding context:**

```text
‘Well, I’d hardly ﬁnished the ﬁrst verse,’ said the Hatter, ‘when the Queen jumped up and bawled out, “He’s murdering the time! Oﬀwith his head!”’
```

**Supporting paragraph/context:**

```text
‘How dreadfully savage!’ exclaimed Alice. ‘And ever since that,’ the Hatter went on in a mournful tone, ‘he won’t do a thing I ask! It’s always six o’clock now.’
```

**Following context:**

```text
A bright idea came into Alice’s head. ‘Is that the reason so many tea- things are put out here?’ she asked.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The pronoun “he” refers to the personified Time.

**Codex annotation notes:** Linked to q023: distinct target claim, shared source event; fact-family IDs are not independent-event counts.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av038</strong> · local_context_reasoning · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** When the Duchess suddenly shouted “Pig!”, whom was she addressing?

**Proposed status:** `answered`

**Proposed reference answer:** She was addressing the baby, not Alice.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_av038`

**Evidence event:** `event_fact_av038`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `negation`, `speaker_identity`

### Required claims and original context

#### C1: The Duchess addressed the word to the baby.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 45, "chapter": "6", "pdf_block": 3}`

**Exact supporting span:**

```text
it was addressed to the baby, and not to her
```

**Preceding context:**

```text
‘Please would you tell me,’ said Alice, a little timidly, for she was not quite sure whether it was good manners for her to speak ﬁrst, ‘why your cat grins like that?’
```

**Supporting paragraph/context:**

```text
‘It’s a Cheshire cat,’ said the Duchess, ‘and that’s why. Pig!’ She said the last word with such sudden violence that Alice quite jumped; but she saw in another moment that it was addressed to the baby, and not to her, so she took courage, and went on again:–
```

**Following context:**

```text
‘I didn’t know that Cheshire cats always grinned; in fact, I didn’t know that cats COULD grin.’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The Duchess addressed the word to the baby.

**Codex annotation notes:** _none_

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av039</strong> · local_context_reasoning · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** Did the Pigeon accept Alice’s claim that she was a little girl? Why?

**Proposed status:** `answered`

**Proposed reference answer:** No. The Pigeon insisted she was a serpent because of her unusual neck and her admission that little girls eat eggs.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `fact_av039`

**Evidence event:** `event_alice_pigeon_serpent_reasoning`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** `q018`

**Tags:** `character_belief`, `negation`

### Required claims and original context

#### C1: The Pigeon rejected Alice’s little-girl claim because of her neck.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 41, "chapter": "5", "pdf_block": 11}`

**Exact supporting span:**

```text
never ONE with such a
```

**Preceding context:**

```text
‘I–I’m a little girl,’ said Alice, rather doubtfully, as she remembered the number of changes she had gone through that day.
```

**Supporting paragraph/context:**

```text
‘A likely story indeed!’ said the Pigeon in a tone of the deepest contempt. ‘I’ve seen a good many little girls in my time, but never ONE with such a
```

**Following context:**

```text
neck as that! No, no! You’re a serpent; and there’s no use denying it. I suppose you’ll be telling me next that you never tasted an egg!’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The Pigeon rejected Alice’s little-girl claim because of her neck.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 42, "chapter": "5", "pdf_block": 1}`

**Exact supporting span:**

```text
neck as that! No, no! You’re a serpent
```

**Preceding context:**

```text
‘A likely story indeed!’ said the Pigeon in a tone of the deepest contempt. ‘I’ve seen a good many little girls in my time, but never ONE with such a
```

**Supporting paragraph/context:**

```text
neck as that! No, no! You’re a serpent; and there’s no use denying it. I suppose you’ll be telling me next that you never tasted an egg!’
```

**Following context:**

```text
‘I HAVE tasted eggs, certainly,’ said Alice, who was a very truthful child; ‘but little girls eat eggs quite as much as serpents do, you know.’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The Pigeon rejected Alice’s little-girl claim because of her neck.

#### C2: The Pigeon connected egg-eating with being a serpent.

**Evidence E3 location:** `{"book": "alice_in_wonderland", "page": 42, "chapter": "5", "pdf_block": 2}`

**Exact supporting span:**

```text
little girls eat eggs quite as much as serpents do
```

**Preceding context:**

```text
neck as that! No, no! You’re a serpent; and there’s no use denying it. I suppose you’ll be telling me next that you never tasted an egg!’
```

**Supporting paragraph/context:**

```text
‘I HAVE tasted eggs, certainly,’ said Alice, who was a very truthful child; ‘but little girls eat eggs quite as much as serpents do, you know.’
```

**Following context:**

```text
‘I don’t believe it,’ said the Pigeon; ‘but if they do, why then they’re a kind of serpent, that’s all I can say.’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The Pigeon connected egg-eating with being a serpent.

**Codex annotation notes:** Linked to q018: distinct target claim, shared source event; fact-family IDs are not independent-event counts.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av040</strong> · local_context_reasoning · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** Who supplied the sleepy answer “Treacle” during the cook’s testimony?

**Proposed status:** `answered`

**Proposed reference answer:** The Dormouse did.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `alice_cook_witness`

**Evidence event:** `event_alice_cook_witness`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `meta_cook_witness` / `none`

**Related cases:** `q029`, `av060`

**Tags:** `speaker_identity`

### Required claims and original context

#### C1: The sleepy voice belonged to the Dormouse.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 85, "chapter": "11", "pdf_block": 8}`

**Exact supporting span:**

```text
‘Treacle,’ said a sleepy voice behind her
```

**Preceding context:**

```text
‘Well, if I must, I must,’ the King said, with a melancholy air, and, after folding his arms and frowning at the cook till his eyes were nearly out of sight, he said in a deep voice, ‘What are tarts made of?’
```

**Supporting paragraph/context:**

```text
‘Pepper, mostly,’ said the cook. ‘Treacle,’ said a sleepy voice behind her. ‘Collar that Dormouse,’ the Queen shrieked out. ‘Behead that Dormouse! Turn that Dormouse out of court! Suppress him! Pinch him! Oﬀwith his whiskers!’
```

**Following context:**

```text
For some minutes the whole court was in confusion, getting the Dormouse turned out, and, by the time they had settled down again, the cook had disappeared.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The sleepy voice belonged to the Dormouse.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 85, "chapter": "11", "pdf_block": 8}`

**Exact supporting span:**

```text
Collar that Dormouse
```

**Preceding context:**

```text
‘Well, if I must, I must,’ the King said, with a melancholy air, and, after folding his arms and frowning at the cook till his eyes were nearly out of sight, he said in a deep voice, ‘What are tarts made of?’
```

**Supporting paragraph/context:**

```text
‘Pepper, mostly,’ said the cook. ‘Treacle,’ said a sleepy voice behind her. ‘Collar that Dormouse,’ the Queen shrieked out. ‘Behead that Dormouse! Turn that Dormouse out of court! Suppress him! Pinch him! Oﬀwith his whiskers!’
```

**Following context:**

```text
For some minutes the whole court was in confusion, getting the Dormouse turned out, and, by the time they had settled down again, the cook had disappeared.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The sleepy voice belonged to the Dormouse.

**Codex annotation notes:** _none_

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av041</strong> · paraphrase_vocabulary_mismatch · answered · FAST_CONFIRM</summary>

**Question:** What object made Alice dwindle until she nearly disappeared?

**Proposed status:** `answered`

**Proposed reference answer:** The fan she was holding.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `alice_fan_shrinking`

**Evidence event:** `event_alice_fan_shrinking`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** `q010`

**Tags:** `metamorphic`, `paraphrase`

### Required claims and original context

#### C1: The fan caused the shrinking.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 21, "chapter": "2", "pdf_block": 4}`

**Exact supporting span:**

```text
cause of this was the fan she was holding
```

**Preceding context:**

```text
‘I’m sure those are not the right words,’ said poor Alice, and her eyes ﬁlled with tears again as she went on, ‘I must be Mabel after all, and I shall have to go and live in that poky little house, and have next to no toys to play with, and oh! ever so many lessons to learn! No, I’ve made up my mind about it; if I’m Mabel, I’ll stay down here! It’ll be no use their putting their heads down and saying “Come up again, dear!” I shall only look up and say “Who am I then? Tell me that ﬁrst, and then, if I like being that person, I’ll come up: if not, I’ll stay down here till I’m somebody else”–but, oh dear!’ cried Alice, with a sudden burst of tears, ‘I do wish they WOULD put their heads down! I am so VERY tired of being all alone here!’
```

**Supporting paragraph/context:**

```text
As she said this she looked down at her hands, and was surprised to see that she had put on one of the Rabbit’s little white kid gloves while she was talking. ‘How CAN I have done that?’ she thought. ‘I must be growing small again.’ She got up and went to the table to measure herself by it, and found that, as nearly as she could guess, she was now about two feet high, and was going on shrinking rapidly: she soon found out that the cause of this was the fan she was holding, and she dropped it hastily, just in time to avoid shrinking away altogether.
```

**Following context:**

```text
‘That WAS a narrow escape!’ said Alice, a good deal frightened at the sudden change, but very glad to ﬁnd herself still in existence; ‘and now for the garden!’ and she ran with all speed back to the little door: but, alas! the little door was shut again, and the little golden key was lying on the glass table as before, ‘and things are worse than ever,’ thought the poor child, ‘for I never was so small as this before, never! And I declare it’s too bad, that it is!’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The fan caused the shrinking.

**Codex annotation notes:** Paraphrase pair with historical q010.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av042</strong> · paraphrase_vocabulary_mismatch · answered · FAST_CONFIRM</summary>

**Question:** What living figures acted as wickets in the Queen’s croquet match?

**Proposed status:** `answered`

**Proposed reference answer:** Soldiers doubled over on their hands and feet to form the arches.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `alice_croquet_equipment`

**Evidence event:** `event_alice_croquet_equipment`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `meta_croquet_equipment` / `none`

**Related cases:** `q024`

**Tags:** `metamorphic`, `paraphrase`

### Required claims and original context

#### C1: Soldiers formed the croquet arches/wickets.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 62, "chapter": "8", "pdf_block": 3}`

**Exact supporting span:**

```text
soldiers had to double themselves up and to stand on their hands and feet, to make the arches
```

**Preceding context:**

```text
‘She boxed the Queen’s ears–’ the Rabbit began. Alice gave a little scream of laughter. ‘Oh, hush!’ the Rabbit whispered in a frightened tone. ‘The Queen will hear you! You see, she came rather late, and the Queen said–’
```

**Supporting paragraph/context:**

```text
‘Get to your places!’ shouted the Queen in a voice of thunder, and peo- ple began running about in all directions, tumbling up against each other; however, they got settled down in a minute or two, and the game began. Alice thought she had never seen such a curious croquet-ground in her life; it was all ridges and furrows; the balls were live hedgehogs, the mallets live ﬂamingoes, and the soldiers had to double themselves up and to stand on their hands and feet, to make the arches.
```

**Following context:**

```text
The chief diﬃculty Alice found at ﬁrst was in managing her ﬂamingo: she succeeded in getting its body tucked away, comfortably enough, under her arm, with its legs hanging down, but generally, just as she had got its neck nicely straightened out, and was going to give the hedgehog a blow with its head, it WOULD twist itself round and look up in her face, with such a puzzled expression that she could not help bursting out laughing: and when she had got its head down, and was going to begin again, it was very provoking to ﬁnd that the hedgehog had unrolled itself, and was in the act of crawling away: besides all this, there was generally a ridge or furrow in the way wherever she wanted to send the hedgehog to, and, as the doubled-up soldiers were always getting up and walking oﬀto other parts of the ground, Alice soon came to the conclusion that it was a very diﬃcult game indeed.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Soldiers formed the croquet arches/wickets.

**Codex annotation notes:** Paraphrase pair with historical q024.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av043</strong> · paraphrase_vocabulary_mismatch · answered · FAST_CONFIRM</summary>

**Question:** Which two residents did the Cat describe as insane?

**Proposed status:** `answered`

**Proposed reference answer:** The Hatter and the March Hare.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `alice_cat_mad_directions`

**Evidence event:** `event_alice_cat_mad_directions`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `meta_cat_mad` / `none`

**Related cases:** `q020`

**Tags:** `metamorphic`, `paraphrase`

### Required claims and original context

#### C1: The Cat named the Hatter and March Hare and said both were mad.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 48, "chapter": "6", "pdf_block": 2}`

**Exact supporting span:**

```text
lives a Hatter
```

**Preceding context:**

```text
‘–so long as I get SOMEWHERE,’ Alice added as an explanation. ‘Oh, you’re sure to do that,’ said the Cat, ‘if you only walk long enough.’ Alice felt that this could not be denied, so she tried another question. ‘What sort of people live about here?’
```

**Supporting paragraph/context:**

```text
‘In THAT direction,’ the Cat said, waving its right paw round, ‘lives a Hatter: and in THAT direction,’ waving the other paw, ‘lives a March Hare. Visit either you like: they’re both mad.’
```

**Following context:**

```text
‘But I don’t want to go among mad people,’ Alice remarked. ‘Oh, you can’t help that,’ said the Cat: ‘we’re all mad here. I’m mad. You’re mad.’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The Cat named the Hatter and March Hare and said both were mad.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 48, "chapter": "6", "pdf_block": 2}`

**Exact supporting span:**

```text
lives a March Hare
```

**Preceding context:**

```text
‘–so long as I get SOMEWHERE,’ Alice added as an explanation. ‘Oh, you’re sure to do that,’ said the Cat, ‘if you only walk long enough.’ Alice felt that this could not be denied, so she tried another question. ‘What sort of people live about here?’
```

**Supporting paragraph/context:**

```text
‘In THAT direction,’ the Cat said, waving its right paw round, ‘lives a Hatter: and in THAT direction,’ waving the other paw, ‘lives a March Hare. Visit either you like: they’re both mad.’
```

**Following context:**

```text
‘But I don’t want to go among mad people,’ Alice remarked. ‘Oh, you can’t help that,’ said the Cat: ‘we’re all mad here. I’m mad. You’re mad.’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The Cat named the Hatter and March Hare and said both were mad.

**Evidence E3 location:** `{"book": "alice_in_wonderland", "page": 48, "chapter": "6", "pdf_block": 2}`

**Exact supporting span:**

```text
they’re both mad
```

**Preceding context:**

```text
‘–so long as I get SOMEWHERE,’ Alice added as an explanation. ‘Oh, you’re sure to do that,’ said the Cat, ‘if you only walk long enough.’ Alice felt that this could not be denied, so she tried another question. ‘What sort of people live about here?’
```

**Supporting paragraph/context:**

```text
‘In THAT direction,’ the Cat said, waving its right paw round, ‘lives a Hatter: and in THAT direction,’ waving the other paw, ‘lives a March Hare. Visit either you like: they’re both mad.’
```

**Following context:**

```text
‘But I don’t want to go among mad people,’ Alice remarked. ‘Oh, you can’t help that,’ said the Cat: ‘we’re all mad here. I’m mad. You’re mad.’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The Cat named the Hatter and March Hare and said both were mad.

**Codex annotation notes:** _none_

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av044</strong> · contrastive_distractor · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** Did Alice receive the same kind of prize as the other Caucus-race participants?

**Proposed status:** `answered`

**Proposed reference answer:** No. The others received comfits, while Alice received a thimble.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `alice_caucus_prizes`

**Evidence event:** `event_alice_caucus_prizes`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `contrast_caucus_prizes`

**Related cases:** `q013`, `c006`

**Tags:** `contrastive_pair`, `relation_reversal`

### Required claims and original context

#### C1: The others received comfits.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 27, "chapter": "3", "pdf_block": 3}`

**Exact supporting span:**

```text
handed them round as prizes
```

**Preceding context:**

```text
‘But who is to give the prizes?’ quite a chorus of voices asked. ‘Why, SHE, of course,’ said the Dodo, pointing to Alice with one ﬁnger; and the whole party at once crowded round her, calling out in a confused way, ‘Prizes! Prizes!’
```

**Supporting paragraph/context:**

```text
Alice had no idea what to do, and in despair she put her hand in her pocket, and pulled out a box of comﬁts, (luckily the salt water had not got into it), and handed them round as prizes. There was exactly one a-piece all round.
```

**Following context:**

```text
‘But she must have a prize herself, you know,’ said the Mouse. ‘Of course,’ the Dodo replied very gravely. ‘What else have you got in your pocket?’ he went on, turning to Alice.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The others received comfits.

#### C2: Alice received a thimble.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 27, "chapter": "3", "pdf_block": 6}`

**Exact supporting span:**

```text
took the thimble
```

**Preceding context:**

```text
‘Only a thimble,’ said Alice sadly. ‘Hand it over here,’ said the Dodo. Then they all crowded round her once more, while the Dodo solemnly pre- sented the thimble, saying ‘We beg your acceptance of this elegant thimble’; and, when it had ﬁnished this short speech, they all cheered.
```

**Supporting paragraph/context:**

```text
Alice thought the whole thing very absurd, but they all looked so grave that she did not dare to laugh; and, as she could not think of anything to say, she simply bowed, and took the thimble, looking as solemn as she could.
```

**Following context:**

```text
The next thing was to eat the comﬁts: this caused some noise and confu- sion, as the large birds complained that they could not taste theirs, and the small ones choked and had to be patted on the back. However, it was over at last, and they sat down again in a ring, and begged the Mouse to tell them something more.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Alice received a thimble.

**Codex annotation notes:** Contrastive q013-family case; evidence now points to Alice actually taking the thimble rather than a line-broken extraction fragment.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av045</strong> · contrastive_distractor · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** Who offered Alice wine, and who then admitted there was none?

**Proposed status:** `answered`

**Proposed reference answer:** The March Hare did both.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `alice_tea_party_wine`

**Evidence event:** `event_alice_tea_party_wine`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `contrast_tea_wine`

**Related cases:** `q022`

**Tags:** `speaker_identity`, `who_did_what`

### Required claims and original context

#### C1: The March Hare offered wine.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 51, "chapter": "7", "pdf_block": 4}`

**Exact supporting span:**

```text
Have some wine
```

**Preceding context:**

```text
The table was a large one, but the three were all crowded together at one corner of it: ‘No room! No room!’ they cried out when they saw Alice coming. ‘There’s PLENTY of room!’ said Alice indignantly, and she sat down in a large arm-chair at one end of the table.
```

**Supporting paragraph/context:**

```text
‘Have some wine,’ the March Hare said in an encouraging tone. Alice looked all round the table, but there was nothing on it but tea. ‘I don’t see any wine,’ she remarked.
```

**Following context:**

```text
‘There isn’t any,’ said the March Hare. ‘Then it wasn’t very civil of you to oﬀer it,’ said Alice angrily. ‘It wasn’t very civil of you to sit down without being invited,’ said the March Hare.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The March Hare offered wine.

#### C2: The March Hare said there was none.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 51, "chapter": "7", "pdf_block": 5}`

**Exact supporting span:**

```text
There isn’t any,’ said the March Hare
```

**Preceding context:**

```text
‘Have some wine,’ the March Hare said in an encouraging tone. Alice looked all round the table, but there was nothing on it but tea. ‘I don’t see any wine,’ she remarked.
```

**Supporting paragraph/context:**

```text
‘There isn’t any,’ said the March Hare. ‘Then it wasn’t very civil of you to oﬀer it,’ said Alice angrily. ‘It wasn’t very civil of you to sit down without being invited,’ said the March Hare.
```

**Following context:**

```text
‘I didn’t know it was YOUR table,’ said Alice; ‘it’s laid for a great many more than three.’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The March Hare said there was none.

**Codex annotation notes:** _none_

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av046</strong> · unanswerable_false_premise · insufficient_evidence · DEEP_REVIEW — needs owner attention</summary>

**Question:** What was the White Rabbit’s first name?

**Proposed status:** `insufficient_evidence`

**Proposed reference answer:** No supporting evidence was found in the reviewed text of the exact evaluation book after targeted whole-document verification.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `fact_av046`

**Evidence event:** `event_fact_av046`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `whole_document_negative_check`

### Whole-document negative verification

**Scope:** complete text content of Alice PDF SHA-256 49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e

**Entity aliases:** `White Rabbit`, `Rabbit`, `herald`

**Negative terms:** `White Rabbit first name`, `Rabbit named`, `Rabbit called`

**Relation variants:** `his name is`, `called the Rabbit`, `named Rabbit`

**Morphological variants:** `name`, `named`, `names`, `called`

**Semantic variants:** `personal name of the White Rabbit`, `what is the Rabbit called`

**Plausible counterexamples:** `Mary Ann`, `Bill`, `Pat`

**Counterexample disposition:** Mary Ann is the Rabbit's housemaid; Bill and Pat are other characters, not names for the Rabbit.

#### Search: `first/name relation`

- Pattern: `\b(?:first name|named|called)\b`
- All matches reviewed: `true`
- Assessment: No hit names the White Rabbit.

Source matches (15):
- page 23: ard as it could go, and making quite a commotion in the pool as it went. So she called softly after it, ‘Mouse dear! Do come back again, and we won’t talk about cats or dogs either, if you don’t like them!’
- page 25: be said. At last the Mouse, who seemed to be a person of authority among them, called out, ‘Sit down, all of you, and listen to me! I’LL soon make you dry enough!’ They all sat down at once, in a large rin
- page 26: ad been running half an hour or so, and were quite dry again, the Dodo suddenly called out ‘The race is over!’ and they all crowded round it, panting, and asking, ‘But who has won?’ This question the Dodo c
- page 29: he Mouse only growled in reply. ‘Please come back and finish your story!’ Alice called after it; and the others all joined in chorus, ‘Yes, please do!’ but the Mouse only shook its head impatiently, and wal
- page 29: eally must be getting home; the night-air doesn’t suit my throat!’ and a Canary called out in a trembling voice to its children,
- page 31: completely. Very soon the Rabbit noticed Alice, as she went hunting about, and called out to her in an angry tone, ‘Why, Mary Ann, what ARE you doing out here? Run home this moment, and fetch me a pair of
- page 34: d the others. ‘We must burn the house down!’ said the Rabbit’s voice; and Alice called
- page 38: a VERY unpleasant state of mind, she turned away. ‘Come back!’ the Caterpillar called after her. ‘I’ve something important to say!’ This sounded promising, certainly: Alice turned and came back again. ‘Kee
- page 43: n because he was in livery: otherwise, judging by his face only, she would have called him a fish)–and rapped loudly at the door with his knuckles. It was opened by another footman in livery, with a round f
- page 60: ER 8. THE QUEEN’S CROQUET-GROUND had been anxiously looking across the garden, called out ‘The Queen! The Queen!’ and the three gardeners instantly threw themselves flat upon their faces. There was a sound
- page 63: member where.’ ‘Well, it must be removed,’ said the King very decidedly, and he called the Queen, who was passing at the moment, ‘My dear! I wish you would have this cat removed!’ The Queen had only one way
- page 71: Tortoise–’ ‘Why did you call him Tortoise, if he wasn’t one?’ Alice asked. ‘We called him Tortoise because he taught us,’ said the Mock Turtle angrily: ‘really you are very dull!’ ‘You ought to be ashamed
- page 72: and so on.’ ‘What a curious plan!’ exclaimed Alice. ‘That’s the reason they’re called lessons,’ the Gryphon remarked: ‘because they lessen from day to day.’ This was quite a new idea to Alice, and she thou
- page 75: tell you more than that, if you like,’ said the Gryphon. ‘Do you know why it’s called a whiting?’ ‘I never thought about it,’ said Alice. ‘Why?’ ‘IT DOES THE BOOTS AND SHOES.’ the Gryphon replied very sole
- page 82: ess,’ said the King; and the White Rabbit blew three blasts on the trumpet, and called out, ‘First witness!’ The first witness was the Hatter. He came in with a teacup in one hand and a piece of bread-and-b

#### Search: `White Rabbit`

- Pattern: `\bWhite Rabbit\b`
- All matches reviewed: `true`
- Assessment: Entity mentions use a title, not a first name.

Source matches (21):
- page 13: uld be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her. There was nothing so VERY remarkable in that; nor did Alice think it so VERY much out
- page 15: up, but it was all dark overhead; before her was another long passage, and the White Rabbit was still in sight, hurrying down it. There was not a moment to be lost: away went Alice like the wind, and was just in
- page 20: the distance, and she hastily dried her eyes to see what was coming. It was the White Rabbit returning, splendidly dressed, with a pair of white kid gloves in one hand and a large fan in the other: he came trotti
- page 31: Chapter 4 The Rabbit Sends in a Little Bill It was the White Rabbit, trotting slowly back again, and looking anxiously about as it went, as if it had lost something; and she heard it mutt
- page 60: t came the guests, mostly Kings and Queens, and among them Alice recognised the White Rabbit: it was talking in a hurried nervous manner, smiling at everything that was said, and went by without noticing her. The
- page 61: s–it’s a very fine day!’ said a timid voice at her side. She was walking by the White Rabbit, who was peeping anxiously into her face. ‘Very,’ said Alice: ‘–where’s the Duchess?’ ‘Hush! Hush!’ said the Rabbit in
- page 76: So Alice began telling them her adventures from the time when she first saw the White Rabbit. She was a little nervous about it just at first, the two creatures got so close to her, one on each side, and opened t
- page 81: in chains, with a soldier on each side to guard him; and near the King was the White Rabbit, with a trumpet in one hand, and a scroll of parchment in the other. In the very middle of the court was a table, with
- page 82: ings!’ Alice began in a loud, indignant voice, but she stopped hastily, for the White Rabbit cried out, ‘Silence in the court!’ and the King put on his spectacles and looked anxiously round, to make out who was t
- page 82: no mark on the slate. ‘Herald, read the accusation!’ said the King. On this the White Rabbit blew three blasts on the trumpet, and then unrolled the parchment scroll, and read as follows:– ‘The Queen of Hearts,
- page 82: eat deal to come before that!’ ‘Call the first witness,’ said the King; and the White Rabbit blew three blasts on the trumpet, and called out, ‘First witness!’ The first witness was the Hatter. He came in with a
- page 85: ence,’ said the King. ‘Shan’t,’ said the cook. The King looked anxiously at the White Rabbit, who said in a low voice, ‘Your Majesty must cross-examine THIS witness.’ ‘Well, if I must, I must,’ the King said, wit
- page 85: s-examine the next witness. It quite makes my forehead ache!’ Alice watched the White Rabbit as he fumbled over the list, feeling very curious to see what the next witness would be like, ‘–for they haven’t got mu
- page 85: n’t got much evidence YET,’ she said to herself. Imagine her surprise, when the White Rabbit read out, at the top of his shrill little voice, the name ‘Alice!’
- page 88: the jury. They were just beginning to write this down on their slates, when the White Rabbit interrupted: ‘UNimportant, your Majesty means, of course,’ he said in a very respectful tone, but frowning and making f
- page 88: picked up.’ ‘What’s in it?’ said the Queen. ‘I haven’t opened it yet,’ said the White Rabbit, ‘but it seems to be a letter, written by the prisoner to–to somebody.’ ‘It must have been that,’ said the King, ‘unles
- page 88: it directed to?’ said one of the jurymen. ‘It isn’t directed at all,’ said the White Rabbit; ‘in fact, there’s nothing written on the OUTSIDE.’ He unfolded the paper as he spoke, and added ‘It isn’t a letter, af
- page 89: ‘No, they’re not,’ said the White Rabbit, ‘and that’s the queerest thing about it.’ (The jury all looked puzzled.) ‘He must have imitated somebody else’s hand,’
- page 89: ‘Why, you don’t even know what they’re about!’ ‘Read them,’ said the King. The White Rabbit put on his spectacles. ‘Where shall I begin, please your Majesty?’ he asked. ‘Begin at the beginning,’ the King said gr
- page 89: ely, ‘and go on till you come to the end: then stop.’ These were the verses the White Rabbit read:– ‘They told me you had been to her, And mentioned me to him: She gave me a good character, But said I could not
- page 91: eatures of her little sister’s dream. The long grass rustled at her feet as the White Rabbit hurried by–the

#### Search: `W. RABBIT`

- Pattern: `W\.\s*RABBIT`
- All matches reviewed: `true`
- Assessment: The doorplate supplies only an initial and surname/title.

Source matches (1):
- page 31: neat little house, on the door of which was a bright brass plate with the name ‘W. RABBIT’ engraved upon it. She went in without knocking, and hurried upstairs, in great fear lest she should meet the real Mary

**Bounded conclusion:** No supporting evidence was found in the reviewed book text after targeted whole-document verification.. This is not mathematical proof of absence.

**Codex annotation notes:** _none_

**Annotation confidence / review tier:** `needs_owner_review` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av047</strong> · unanswerable_false_premise · insufficient_evidence · DEEP_REVIEW — needs owner attention</summary>

**Question:** What was the Duchess’s baby named?

**Proposed status:** `insufficient_evidence`

**Proposed reference answer:** No supporting evidence was found in the reviewed text of the exact evaluation book after targeted whole-document verification.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `fact_av047`

**Evidence event:** `event_fact_av047`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `whole_document_negative_check`

### Whole-document negative verification

**Scope:** complete text content of Alice PDF SHA-256 49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e

**Entity aliases:** `Duchess's baby`, `baby`, `child`, `pig`

**Negative terms:** `baby name`, `child named`, `Duchess called baby`

**Relation variants:** `named the baby`, `baby's name`, `called her child`

**Morphological variants:** `name`, `named`, `called`, `calls`

**Semantic variants:** `personal name of the Duchess's child`

**Plausible counterexamples:** `The Duchess shouts ‘Pig!’ at the baby`

**Counterexample disposition:** ‘Pig!’ is an address/insult that anticipates the transformation, not an established personal name.

#### Search: `baby name relation`

- Pattern: `\b(?:baby|child).{0,40}(?:name|named|called)\b`
- All matches reviewed: `true`
- Assessment: No naming assertion.

Source matches (0):
- none

#### Search: `Duchess and baby`

- Pattern: `\b(?:Duchess|baby)\b`
- All matches reviewed: `true`
- Assessment: Mentions describe the scene but do not name the child.

Source matches (56):
- page 20: came trotting along in a great hurry, muttering to himself as he came, ‘Oh! the Duchess, the Duchess! Oh! won’t she be savage if I’ve kept her waiting!’ Alice felt so desperate that she was ready to ask help
- page 20: along in a great hurry, muttering to himself as he came, ‘Oh! the Duchess, the Duchess! Oh! won’t she be savage if I’ve kept her waiting!’ Alice felt so desperate that she was ready to ask help of any one;
- page 31: it went, as if it had lost something; and she heard it muttering to itself ‘The Duchess! The Duchess! Oh my dear paws! Oh my fur and whiskers! She’ll get me executed, as sure as ferrets are ferrets! Where CA
- page 31: f it had lost something; and she heard it muttering to itself ‘The Duchess! The Duchess! Oh my dear paws! Oh my fur and whiskers! She’ll get me executed, as sure as ferrets are ferrets! Where CAN I have drop
- page 43: mself, and this he handed over to the other, saying, in a solemn tone, ‘For the Duchess. An invitation from the Queen to play croquet.’ The Frog-Footman repeated, in the same solemn tone, only changing the o
- page 43: hanging the order of the words a little, ‘From the Queen. An invitation for the Duchess to play croquet.’ Then they both bowed low, and their curls got entangled together. Alice laughed so much at this, that
- page 44: ht into a large kitchen, which was full of smoke from one end to the other: the Duchess was sitting on a three-legged stool in the middle, nursing a baby; the cook was leaning over the fire, stirring a large
- page 44: other: the Duchess was sitting on a three-legged stool in the middle, nursing a baby; the cook was leaning over the fire, stirring a large cauldron which seemed to be full of soup. ‘There’s certainly too
- page 44: she could for sneezing. There was certainly too much of it in the air. Even the Duchess sneezed occasionally; and as for the baby, it was sneezing and howling alternately without a moment’s pause. The only t
- page 44: oo much of it in the air. Even the Duchess sneezed occasionally; and as for the baby, it was sneezing and howling alternately without a moment’s pause. The only things in the kitchen that did not
- page 45: to speak first, ‘why your cat grins like that?’ ‘It’s a Cheshire cat,’ said the Duchess, ‘and that’s why. Pig!’ She said the last word with such sudden violence that Alice quite jumped; but she saw in anothe
- page 45: Alice quite jumped; but she saw in another moment that it was addressed to the baby, and not to her, so she took courage, and went on again:– ‘I didn’t know that Cheshire cats always grinned; in fact, I
- page 45: grinned; in fact, I didn’t know that cats COULD grin.’ ‘They all can,’ said the Duchess; ‘and most of ’em do.’ ‘I don’t know of any that do,’ Alice said very politely, feeling quite pleased to have got into
- page 45: quite pleased to have got into a conversation. ‘You don’t know much,’ said the Duchess; ‘and that’s a fact.’ Alice did not at all like the tone of this remark, and thought it would be as well to introduce s
- page 45: ffthe fire, and at once set to work throwing everything within her reach at the Duchess and the baby –the fire-irons came first; then followed a shower of saucepans, plates, and dishes. The Duchess took no n
- page 45: at once set to work throwing everything within her reach at the Duchess and the baby –the fire-irons came first; then followed a shower of saucepans, plates, and dishes. The Duchess took no notice of them
- page 45: -irons came first; then followed a shower of saucepans, plates, and dishes. The Duchess took no notice of them even when they hit her; and the baby was howling so much already, that it was quite impossible t
- page 45: and dishes. The Duchess took no notice of them even when they hit her; and the baby was howling so much already, that it was quite impossible to say whether the blows hurt it or not. ‘Oh, PLEASE mind wha
- page 45: , and very nearly carried it off. ‘If everybody minded their own business,’ the Duchess said in a hoarse growl, ‘the world would go round a deal faster than it does.’ ‘Which would NOT be an advantage,’ said
- page 45: takes twenty-four hours to turn round on its axis–’ ‘Talking of axes,’ said the Duchess, ‘chop offher head!’ Alice glanced rather anxiously at the cook, to see if she meant to take the hint; but the cook was
- page 46: 46 CHAPTER 6. PIG AND PEPPER ‘Oh, don’t bother ME,’ said the Duchess; ‘I never could abide figures!’ And with that she began nursing her child again, singing a sort of lullaby to it as she
- page 46: it to annoy, Because he knows it teases.’ CHORUS. (In which the cook and the baby joined):– ‘Wow! wow! wow!’ While the Duchess sang the second verse of the song, she kept tossing the baby violently u
- page 46: CHORUS. (In which the cook and the baby joined):– ‘Wow! wow! wow!’ While the Duchess sang the second verse of the song, she kept tossing the baby violently up and down, and the poor little thing howled so
- page 46: ow!’ While the Duchess sang the second verse of the song, she kept tossing the baby violently up and down, and the poor little thing howled so, that Alice could hardly hear the words:– ‘I speak severely
- page 46: !’ CHORUS. ‘Wow! wow! wow!’ ‘Here! you may nurse it a bit, if you like!’ the Duchess said to Alice, flinging the baby at her as she spoke. ‘I must go and get ready to play croquet with the Queen,’ and she
- page 46: ! you may nurse it a bit, if you like!’ the Duchess said to Alice, flinging the baby at her as she spoke. ‘I must go and get ready to play croquet with the Queen,’ and she hurried out of the room. The coo
- page 46: frying-pan after her as she went out, but it just missed her. Alice caught the baby with some difficulty, as it was a queer- shaped little creature, and held out its arms and legs in all directions, ‘jus
- page 47: runt,’ said Alice; ‘that’s not at all a proper way of expressing yourself.’ The baby grunted again, and Alice looked very anxiously into its face to see what was the matter with it. There could be no doub
- page 47: like a snout than a real nose; also its eyes were getting extremely small for a baby: altogether Alice did not like the look of the thing at all. ‘But perhaps it was only sobbing,’ she thought, and looked
- page 48: where it had been, it suddenly appeared again. ‘By-the-bye, what became of the baby?’ said the Cat. ‘I’d nearly forgotten to ask.’ ‘It turned into a pig,’ Alice quietly said, just as if it had come back
- page 61: bit, who was peeping anxiously into her face. ‘Very,’ said Alice: ‘–where’s the Duchess?’ ‘Hush! Hush!’ said the Rabbit in a low, hurried tone. He looked anxiously over his shoulder as he spoke, and then rai
- page 64: e and anxious.) Alice could think of nothing else to say but ‘It belongs to the Duchess: you’d better ask HER about it.’ ‘She’s in prison,’ the Queen said to the executioner: ‘fetch her here.’ And the execut
- page 64: fading away the moment he was gone, and, by the time he had come back with the Duchess, it had entirely disappeared; so the
- page 67: ‘You can’t think how glad I am to see you again, you dear old thing!’ said the Duchess, as she tucked her arm affectionately into Alice’s, and they walked offtogether. Alice was very glad to find her in suc
- page 67: he pepper that had made her so savage when they met in the kitchen. ‘When I’M a Duchess,’ she said to herself, (not in a very hopeful tone though), ‘I won’t have any pepper in my kitchen AT ALL. Soup does ve
- page 67: hen they wouldn’t be so stingy about it, you know–’ She had quite forgotten the Duchess by this time, and was a little startled when she heard her voice close to her ear. ‘You’re thinking about something, my
- page 67: ‘Perhaps it hasn’t one,’ Alice ventured to remark. ‘Tut, tut, child!’ said the Duchess. ‘Everything’s got a moral, if only you can find it.’ And she squeezed herself up closer to Alice’s side as she spoke.
- page 67: she spoke. Alice did not much like keeping so close to her: first, because the Duchess was VERY ugly; and secondly, because she was exactly the right height to rest her chin upon Alice’s shoulder, and it wa
- page 68: PTER 9. THE MOCK TURTLE’S STORY the conversation a little. ‘’Tis so,’ said the Duchess: ‘and the moral of that is–”Oh, ’tis love, ’tis love, that makes the world go round!”’ ‘Somebody said,’ Alice whispered
- page 68: minding their own business!’ ‘Ah, well! It means much the same thing,’ said the Duchess, digging her sharp little chin into Alice’s shoulder as she added, ‘and the moral of THAT is– “Take care of the sense,
- page 68: elf. ‘I dare say you’re wondering why I don’t put my arm round your waist,’ the Duchess said after a pause: ‘the reason is, that I’m doubtful about the temper of your flamingo. Shall I try the experiment?’ ‘
- page 68: not feeling at all anxious to have the experiment tried. ‘Very true,’ said the Duchess: ‘flamingoes and mustard both bite. And the moral of that is– “Birds of a feather flock together.”’ ‘Only mustard isn’t
- page 68: her.”’ ‘Only mustard isn’t a bird,’ Alice remarked. ‘Right, as usual,’ said the Duchess: ‘what a clear way you have of putting things!’ ‘It’s a mineral, I THINK,’ said Alice. ‘Of course it is,’ said the Duch
- page 68: ing things!’ ‘It’s a mineral, I THINK,’ said Alice. ‘Of course it is,’ said the Duchess, who seemed ready to agree to everything that Alice said; ‘there’s a large mustard-mine near here. And the moral of tha
- page 68: table. It doesn’t look like one, but it is.’ ‘I quite agree with you,’ said the Duchess; ‘and the moral of that is– “Be what you would seem to be”–or if you’d like it put more simply– “Never imagine yourself
- page 68: follow it as you say it.’ ‘That’s nothing to what I could say if I chose,’ the Duchess replied, in a pleased tone. ‘Pray don’t trouble yourself to say it any longer than that,’ said Alice. ‘Oh, don’t talk a
- page 68: it any longer than that,’ said Alice. ‘Oh, don’t talk about trouble!’ said the Duchess. ‘I make you a present of everything I’ve said as yet.’
- page 69: s like that!’ But she did not venture to say it out loud. ‘Thinking again?’ the Duchess asked, with another dig of her sharp little chin. ‘I’ve a right to think,’ said Alice sharply, for she was beginning to
- page 69: he was beginning to feel a little worried. ‘Just about as much right,’ said the Duchess, ‘as pigs have to fly; and the m–’ But here, to Alice’s great surprise, the Duchess’s voice died away, even in the midd
- page 69: ess, ‘as pigs have to fly; and the m–’ But here, to Alice’s great surprise, the Duchess’s voice died away, even in the middle of her favourite word ‘moral,’ and the arm that was linked into hers began to tre
- page 69: her arms folded, frowning like a thunderstorm. ‘A fine day, your Majesty!’ the Duchess began in a low, weak voice. ‘Now, I give you fair warning,’ shouted the Queen, stamping on the ground as she spoke; ‘ei
- page 69: r your head must be off, and that in about half no time! Take your choice!’ The Duchess took her choice, and was gone in a moment. ‘Let’s go on with the game,’ the Queen said to Alice; and Alice was too much
- page 85: t to the door. ‘Call the next witness!’ said the King. The next witness was the Duchess’s cook. She carried the pepper-box in her hand, and Alice guessed who it was, even before she got into the court, by th
- page 92: of the Queen ordering offher unfortunate guests to execution–once more the pig-baby was sneezing on the Duchess’s knee, while plates and dishes crashed around it–once more the shriek of the Gryphon, the
- page 92: fher unfortunate guests to execution–once more the pig-baby was sneezing on the Duchess’s knee, while plates and dishes crashed around it–once more the shriek of the Gryphon, the squeaking of the Lizard’s sl
- page 92: the Queen’s shrill cries to the voice of the shepherd boy–and the sneeze of the baby, the shriek of the Gryphon, and all the other queer noises, would change (she knew) to the confused clamour of the busy

**Bounded conclusion:** No supporting evidence was found in the reviewed book text after targeted whole-document verification.. This is not mathematical proof of absence.

**Codex annotation notes:** _none_

**Annotation confidence / review tier:** `needs_owner_review` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av048</strong> · unanswerable_false_premise · insufficient_evidence · DEEP_REVIEW — needs owner attention</summary>

**Question:** In what exact calendar year do the Wonderland events occur?

**Proposed status:** `insufficient_evidence`

**Proposed reference answer:** No supporting evidence was found in the reviewed text of the exact evaluation book after targeted whole-document verification.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `fact_av048`

**Evidence event:** `event_fact_av048`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `whole_document_negative_check`

### Whole-document negative verification

**Scope:** complete text content of Alice PDF SHA-256 49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e

**Entity aliases:** `Alice`, `Wonderland`, `the events`, `that day`

**Negative terms:** `calendar year`, `in 18xx`, `in 19xx`, `year of the story`

**Relation variants:** `events occurred in`, `year was`, `dated`

**Morphological variants:** `year`, `years`, `date`, `dated`

**Semantic variants:** `when exactly does the story take place`

**Plausible counterexamples:** `Project Gutenberg release/copyright years in front matter`, `story-relative references such as yesterday`

**Counterexample disposition:** Metadata years describe the electronic edition, while story-relative time does not identify a calendar year.

#### Search: `four-digit years`

- Pattern: `\b(?:17|18|19|20)\d{2}\b`
- All matches reviewed: `true`
- Assessment: Numeric years occur in Gutenberg front matter, not the story chronology.

Source matches (7):
- page 2: Project Gutenberg Etext of Alice in Wonderland [Originally released in January, 1991] Copyright laws are changing all over the world, be sure to check the copyright laws for your country before posting th
- page 2: Vanilla Electronic Texts Etexts Readable By Both Humans and By Computers, Since 1971 These Etexts Prepared By Hundreds of Volunteers and Donations Information on contacting Project Gutenberg to get Etexts
- page 4: this year as we release thirty-six text files per month, or 432 more Etexts in 1999 for a total of 2000+. If these reach just 10total should reach over 200 billion Etexts given away this year. The Goal o
- page 4: ease thirty-six text files per month, or 432 more Etexts in 1999 for a total of 2000+. If these reach just 10total should reach over 200 billion Etexts given away this year. The Goal of Project Gutenberg
- page 4: l of Project Gutenberg is to Give Away One Trillion Etext Files by December 31, 2001. [10,000 x 100,000,000 = 1 Trillion] This is ten thousand titles each to one hundred million readers, which is only 5%
- page 4: ed rates of production, we will reach only one-third of that goal by the end of 2001, or about 3,333 Etexts unless we manage to get some real funding; currently our funding is mostly from Michael Hart’s s
- page 9: niversity”. We are planning on making some changes in our donation structure in 2000, so you might want to email me, hart@pobox.com beforehand. *END THE SMALL PRINT! FOR PUBLIC DOMAIN ETEXTS* Ver.04.29.93

#### Search: `year/date`

- Pattern: `\b(?:year|date)\b`
- All matches reviewed: `true`
- Assessment: Story hits do not establish a calendar year.

Source matches (9):
- page 3: ght of the last day of the month of any such announcement. The official release date of all Project Gutenberg Etexts is at Midnight, Central Time, of the last day of the stated month. A preliminary versio
- page 3: n, comment and editing by those who wish to do so. To be sure you have an up to date first edition [xxxxx10x.xxx] please check file sizes in the first week of the next month. Since our ftp program has a b
- page 3: eek of the next month. Since our ftp program has a bug in it that scrambles the date [tried to fix and failed] a look at the file size will have to do, but we will try to see a new copy has at least one b
- page 4: inally estimated at one dollar then we produce $2 million dollars per hour this year as we release thirty-six text files per month, or 432 more Etexts in 1999 for a total of 2000+. If these reach just 10t
- page 4: f these reach just 10total should reach over 200 billion Etexts given away this year. The Goal of Project Gutenberg is to Give Away One Trillion Etext Files by December 31, 2001. [10,000 x 100,000,000 = 1
- page 5: get or mget [to get files. . . set bin for zip files] GET GUTINDEX.?? [to get a year’s listing of books, e.g., GUTINDEX.99] GET GUTINDEX.ALL [to get a listing of ALL books]
- page 8: nberg Association/Carnegie-Mellon University” within the 60 days following each date you prepare (or were legally required to prepare) your annual (or equivalent periodic) tax return.
- page 52: ck it is!’ ‘Why should it?’ muttered the Hatter. ‘Does YOUR watch tell you what year it is?’ ‘Of course not,’ Alice replied very readily: ‘but that’s because it stays the same year for such a long time to
- page 52: course not,’ Alice replied very readily: ‘but that’s because it stays the same year for such a long time together.’

**Bounded conclusion:** No supporting evidence was found in the reviewed book text after targeted whole-document verification.. This is not mathematical proof of absence.

**Codex annotation notes:** Negative verification is bounded whole-document review, not mathematical proof of absence; absolute_absence_claimed remains false.

**Annotation confidence / review tier:** `needs_owner_review` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av049</strong> · unanswerable_false_premise · insufficient_evidence · DEEP_REVIEW — needs owner attention</summary>

**Question:** What is Alice’s sister’s personal name?

**Proposed status:** `insufficient_evidence`

**Proposed reference answer:** No supporting evidence was found in the reviewed text of the exact evaluation book after targeted whole-document verification.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `fact_av049`

**Evidence event:** `event_fact_av049`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `whole_document_negative_check`

### Whole-document negative verification

**Scope:** complete text content of Alice PDF SHA-256 49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e

**Entity aliases:** `Alice's sister`, `her sister`, `the sister`

**Negative terms:** `Alice sister name`, `sister named`, `sister called`

**Relation variants:** `her name was`, `called her sister`, `sister's name`

**Morphological variants:** `name`, `named`, `called`

**Semantic variants:** `personal name of Alice's sister`

**Plausible counterexamples:** `Ada`, `Mabel`, `Dinah`

**Counterexample disposition:** Ada and Mabel are children Alice compares herself with; Dinah is her cat. None names the sister.

#### Search: `sister name relation`

- Pattern: `\bsister.{0,40}(?:name|named|called)\b`
- All matches reviewed: `true`
- Assessment: No naming assertion.

Source matches (0):
- none

#### Search: `sister mentions`

- Pattern: `\bsister\b`
- All matches reviewed: `true`
- Assessment: All mentions use the kinship term without a personal name.

Source matches (9):
- page 13: Down the Rabbit-Hole Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had
- page 13: nk, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, ‘and what is the use of a book,’ thought Alice ‘without pic
- page 91: them off, and found herself lying on the bank, with her head in the lap of her sister, who was gently brushing away some dead leaves that had fluttered down from the trees upon her face. ‘Wake up, Alice de
- page 91: ad fluttered down from the trees upon her face. ‘Wake up, Alice dear!’ said her sister; ‘Why, what a long sleep you’ve had!’ ‘Oh, I’ve had such a curious dream!’ said Alice, and she told her sister, as well
- page 91: you’ve had!’ ‘Oh, I’ve had such a curious dream!’ said Alice, and she told her sister, as well as she could remember them, all these strange Adventures of hers that you have just been reading about; and wh
- page 91: s of hers that you have just been reading about; and when she had finished, her sister kissed her, and said, ‘It WAS a curious dream, dear, certainly: but now run in to your tea; it’s getting late.’ So Alic
- page 91: g while she ran, as well she might, what a wonderful dream it had been. But her sister sat still just as she left her, leaning her head on her hand, watching the setting sun, and thinking of little Alice an
- page 91: en, the whole place around her became alive the strange creatures of her little sister’s dream. The long grass rustled at her feet as the White Rabbit hurried by–the
- page 92: Mock Turtle’s heavy sobs. Lastly, she pictured to herself how this same little sister of hers would, in the after-time, be herself a grown woman; and how she would keep, through all her riper years, the si

**Bounded conclusion:** No supporting evidence was found in the reviewed book text after targeted whole-document verification.. This is not mathematical proof of absence.

**Codex annotation notes:** _none_

**Annotation confidence / review tier:** `needs_owner_review` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av050</strong> · ambiguous_underspecified · ambiguous · DEEP_REVIEW — needs owner attention</summary>

**Question:** What happened after Alice ate a small piece?

**Proposed status:** `ambiguous`

**Proposed reference answer:** Clarification is required because several small pieces cause different size changes.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_av050`

**Evidence event:** `event_fact_av050`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `ambiguity`

### Ambiguity rationale

**Type:** `book_dependent_multiple_events`

A ‘small piece’ could mean a pebble-cake that makes Alice shrink or a piece from either side of the mushroom, whose effects differ.

**Minimal clarification:** Do you mean a pebble-cake or a piece of the mushroom, and if the mushroom, which side?

**Plausible referent E1 — `{"book": "alice_in_wonderland", "page": 35, "chapter": "4", "pdf_block": 5}`**

```text
So she swallowed one of the cakes, and was delighted to ﬁnd that she began shrinking directly. As soon as she was small enough to get through the door, she ran out of the house, and found quite a crowd of little animals and birds waiting outside. The poor little Lizard, Bill, was in the middle, being held up by two guinea-pigs, who were giving it something out of a bottle. They all made a rush at Alice the moment she appeared; but she ran oﬀas hard as she could, and soon found herself safe in a thick wood.
```

**Plausible referent E2 — `{"book": "alice_in_wonderland", "page": 42, "chapter": "5", "pdf_block": 6}`**

```text
‘Well, be oﬀ, then!’ said the Pigeon in a sulky tone, as it settled down again into its nest. Alice crouched down among the trees as well as she could, for her neck kept getting entangled among the branches, and every now and then she had to stop and untwist it. After a while she remembered that she still held the pieces of mushroom in her hands, and she set to work very carefully, nibbling ﬁrst at one and then at the other, and growing sometimes taller and sometimes shorter, until she had succeeded in bringing herself down to her usual height.
```

**Codex annotation notes:** Both candidate interpretations are distinct book events; mushroom-size change is narrator-described.

**Annotation confidence / review tier:** `needs_owner_review` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av051</strong> · ambiguous_underspecified · ambiguous · DEEP_REVIEW — needs owner attention</summary>

**Question:** Why was Alice angry?

**Proposed status:** `ambiguous`

**Proposed reference answer:** The question needs the scene because Alice becomes angry more than once.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_av051`

**Evidence event:** `event_fact_av051`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `ambiguity`

### Ambiguity rationale

**Type:** `book_dependent_multiple_events`

Different scenes give different reasons for Alice’s anger.

**Minimal clarification:** Which scene or conversation do you mean?

**Plausible referent A1 — `{"book": "alice_in_wonderland", "page": 51, "chapter": "7", "pdf_block": 5}`**

```text
‘There isn’t any,’ said the March Hare. ‘Then it wasn’t very civil of you to oﬀer it,’ said Alice angrily. ‘It wasn’t very civil of you to sit down without being invited,’ said the March Hare.
```

**Plausible referent A2 — `{"book": "alice_in_wonderland", "page": 55, "chapter": "7", "pdf_block": 10}`**

```text
‘There’s no such thing!’ Alice was beginning very angrily, but the Hatter and the March Hare went ‘Sh! sh!’ and the Dormouse sulkily remarked, ‘If you can’t be civil, you’d better ﬁnish the story for yourself.’
```

**Codex annotation notes:** The anger labels are narrator descriptions attached to two different tea-party moments.

**Annotation confidence / review tier:** `needs_owner_review` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av052</strong> · local_context_reasoning · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** What did Alice do after the White Rabbit dropped his gloves and fan and ran away?

**Proposed status:** `answered`

**Proposed reference answer:** She picked up the fan and gloves, kept fanning herself, and began wondering whether she had changed.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_av052`

**Evidence event:** `event_fact_av052`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `sequence_context`

### Required claims and original context

#### C1: Alice picked up the fan and gloves.

**Evidence A1 location:** `{"book": "alice_in_wonderland", "page": 20, "chapter": "2", "pdf_block": 2}`

**Exact supporting span:**

```text
Alice took up the fan and gloves
```

**Preceding context:**

```text
After a time she heard a little pattering of feet in the distance, and she hastily dried her eyes to see what was coming. It was the White Rabbit returning, splendidly dressed, with a pair of white kid gloves in one hand and a large fan in the other: he came trotting along in a great hurry, muttering to himself as he came, ‘Oh! the Duchess, the Duchess! Oh! won’t she be savage if I’ve kept her waiting!’ Alice felt so desperate that she was ready to ask help of any one; so, when the Rabbit came near her, she began, in a low, timid voice, ‘If you please, sir–’ The Rabbit started violently, dropped the white kid gloves and the fan, and skurried away into the darkness as hard as he could go.
```

**Supporting paragraph/context:**

```text
Alice took up the fan and gloves, and, as the hall was very hot, she kept fanning herself all the time she went on talking: ‘Dear, dear! How queer everything is to-day! And yesterday things went on just as usual. I wonder if I’ve been changed in the night? Let me think: was I the same when I got up this morning? I almost think I can remember feeling a little diﬀerent. But if I’m not the same, the next question is, Who in the world am I? Ah, THAT’S the great puzzle!’ And she began thinking over all the children she knew that were of the same age as herself, to see if she could have been changed for any of them.
```

**Following context:**

```text

```

**Context incomplete:** `false`

**Why it supports this claim:** The narrator states what Alice did immediately after the Rabbit fled: she picked up the fan and gloves, fanned herself, and started questioning whether she had changed.

#### C2: She fanned herself and wondered whether she had changed.

**Evidence A1 location:** `{"book": "alice_in_wonderland", "page": 20, "chapter": "2", "pdf_block": 2}`

**Exact supporting span:**

```text
Alice took up the fan and gloves
```

**Preceding context:**

```text
After a time she heard a little pattering of feet in the distance, and she hastily dried her eyes to see what was coming. It was the White Rabbit returning, splendidly dressed, with a pair of white kid gloves in one hand and a large fan in the other: he came trotting along in a great hurry, muttering to himself as he came, ‘Oh! the Duchess, the Duchess! Oh! won’t she be savage if I’ve kept her waiting!’ Alice felt so desperate that she was ready to ask help of any one; so, when the Rabbit came near her, she began, in a low, timid voice, ‘If you please, sir–’ The Rabbit started violently, dropped the white kid gloves and the fan, and skurried away into the darkness as hard as he could go.
```

**Supporting paragraph/context:**

```text
Alice took up the fan and gloves, and, as the hall was very hot, she kept fanning herself all the time she went on talking: ‘Dear, dear! How queer everything is to-day! And yesterday things went on just as usual. I wonder if I’ve been changed in the night? Let me think: was I the same when I got up this morning? I almost think I can remember feeling a little diﬀerent. But if I’m not the same, the next question is, Who in the world am I? Ah, THAT’S the great puzzle!’ And she began thinking over all the children she knew that were of the same age as herself, to see if she could have been changed for any of them.
```

**Following context:**

```text

```

**Context incomplete:** `false`

**Why it supports this claim:** The narrator states what Alice did immediately after the Rabbit fled: she picked up the fan and gloves, fanned herself, and started questioning whether she had changed.

**Codex annotation notes:** Former ambiguity candidate repaired: prior A1/A2 duplicated the same Rabbit departure, so the case is now an answered local-context sequence rather than artificial ambiguity.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av053</strong> · ambiguous_underspecified · ambiguous · DEEP_REVIEW — needs owner attention</summary>

**Question:** What happened to the cards?

**Proposed status:** `ambiguous`

**Proposed reference answer:** Clarification is required because ‘the cards’ can refer to the card gardeners or the whole pack at the end.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_av053`

**Evidence event:** `event_fact_av053`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `ambiguity`

### Ambiguity rationale

**Type:** `book_dependent_multiple_referents`

‘The cards’ can refer to the card gardeners in the croquet-ground scene or the whole pack that later flies at Alice.

**Minimal clarification:** Do you mean the card gardeners at the croquet ground or the whole pack at the end of the trial?

**Plausible referent E1 — `{"book": "alice_in_wonderland", "page": 60, "chapter": "8", "pdf_block": 1}`**

```text
had been anxiously looking across the garden, called out ‘The Queen! The Queen!’ and the three gardeners instantly threw themselves ﬂat upon their faces. There was a sound of many footsteps, and Alice looked round, eager to see the Queen.
```

**Plausible referent E2 — `{"book": "alice_in_wonderland", "page": 91, "chapter": "12", "pdf_block": 6}`**

```text
At this the whole pack rose up into the air, and came ﬂying down upon her: she gave a little scream, half of fright and half of anger, and tried to beat them oﬀ, and found herself lying on the bank, with her head in the lap of her sister, who was gently brushing away some dead leaves that had ﬂuttered down from the trees upon her face.
```

**Codex annotation notes:** Stale garden-related plausible_referents metadata was replaced with the two card referents actually evidenced.

**Annotation confidence / review tier:** `needs_owner_review` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av054</strong> · voice_like_noisy_text · answered · FAST_CONFIRM</summary>

**Question:** Um, what color were the white rabbits eyes?

**Proposed status:** `answered`

**Proposed reference answer:** The White Rabbit’s eyes were pink.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `alice_rabbit_eye_color`

**Evidence event:** `event_alice_rabbit_eye_color`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `meta_rabbit_eyes` / `none`

**Related cases:** `q003`

**Tags:** `metamorphic`, `voice_like`

### Required claims and original context

#### C1: The White Rabbit’s eyes were pink.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 13, "chapter": "1", "pdf_block": 3}`

**Exact supporting span:**

```text
White Rabbit with pink eyes
```

**Preceding context:**

```text
Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, ‘and what is the use of a book,’ thought Alice ‘without pictures or conversation?’
```

**Supporting paragraph/context:**

```text
So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.
```

**Following context:**

```text
There was nothing so VERY remarkable in that; nor did Alice think it so VERY much out of the way to hear the Rabbit say to itself, ‘Oh dear! Oh dear! I shall be late!’ (when she thought it over afterwards, it occurred to her that she ought to have wondered at this, but at the time it all seemed quite natural); but when the Rabbit actually TOOK A WATCH OUT OF ITS WAISTCOAT- POCKET, and looked at it, and then hurried on, Alice started to her feet, for it ﬂashed across her mind that she had never before seen a rabbit with either a waistcoat-pocket, or a watch to take out of it, and burning with curiosity, she ran across the ﬁeld after it, and fortunately was just in time to see it pop down a large rabbit-hole under the hedge.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The White Rabbit’s eyes were pink.

**Codex annotation notes:** Voice-like text pair with historical q003.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av055</strong> · voice_like_noisy_text · answered · FAST_CONFIRM</summary>

**Question:** when the rabbit mistook alice for mary ann he wanted his gloves and what else

**Proposed status:** `answered`

**Proposed reference answer:** His fan.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `alice_rabbit_mary_ann_errand`

**Evidence event:** `event_alice_rabbit_mary_ann_errand`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** `q014`, `q015`

**Tags:** `metamorphic`, `voice_like`

### Required claims and original context

#### C1: The Rabbit ordered the person he called Mary Ann to fetch gloves and a fan.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 31, "chapter": "4", "pdf_block": 3}`

**Exact supporting span:**

```text
fetch me a pair of gloves and a fan
```

**Preceding context:**

```text
It was the White Rabbit, trotting slowly back again, and looking anxiously about as it went, as if it had lost something; and she heard it muttering to itself ‘The Duchess! The Duchess! Oh my dear paws! Oh my fur and whiskers! She’ll get me executed, as sure as ferrets are ferrets! Where CAN I have dropped them, I wonder?’ Alice guessed in a moment that it was looking for the fan and the pair of white kid gloves, and she very good-naturedly began hunting about for them, but they were nowhere to be seen–everything seemed to have changed since her swim in the pool, and the great hall, with the glass table and the little door, had vanished completely.
```

**Supporting paragraph/context:**

```text
Very soon the Rabbit noticed Alice, as she went hunting about, and called out to her in an angry tone, ‘Why, Mary Ann, what ARE you doing out here? Run home this moment, and fetch me a pair of gloves and a fan! Quick, now!’ And Alice was so much frightened that she ran oﬀat once in the direction it pointed to, without trying to explain the mistake it had made.
```

**Following context:**

```text
‘He took me for his housemaid,’ she said to herself as she ran. ‘How surprised he’ll be when he ﬁnds out who I am! But I’d better take him his fan and gloves–that is, if I can ﬁnd them.’ As she said this, she came upon a neat little house, on the door of which was a bright brass plate with the name ‘W. RABBIT’ engraved upon it. She went in without knocking, and hurried upstairs, in great fear lest she should meet the real Mary Ann, and be turned out of the house before she had found the fan and gloves.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The Rabbit ordered the person he called Mary Ann to fetch gloves and a fan.

**Codex annotation notes:** Rewritten as realistic punctuation-free spoken text while retaining the q014 fact family.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av056</strong> · voice_like_noisy_text · answered · FAST_CONFIRM</summary>

**Question:** How deep was, like, the tears pool?

**Proposed status:** `answered`

**Proposed reference answer:** About four inches deep.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `alice_height_pool_depth`

**Evidence event:** `event_alice_height_pool_depth`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `meta_height_pool` / `none`

**Related cases:** `q009`, `c005`

**Tags:** `metamorphic`, `voice_like`

### Required claims and original context

#### C1: About four inches deep.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 20, "chapter": "2", "pdf_block": 1}`

**Exact supporting span:**

```text
about four inches deep
```

**Preceding context:**

```text
Poor Alice! It was as much as she could do, lying down on one side, to look through into the garden with one eye; but to get through was more hopeless than ever: she sat down and began to cry again.
```

**Supporting paragraph/context:**

```text
‘You ought to be ashamed of yourself,’ said Alice, ‘a great girl like you,’ (she might well say this), ‘to go on crying in this way! Stop this moment, I tell you!’ But she went on all the same, shedding gallons of tears, until there was a large pool all round her, about four inches deep and reaching half down the hall.
```

**Following context:**

```text
After a time she heard a little pattering of feet in the distance, and she hastily dried her eyes to see what was coming. It was the White Rabbit returning, splendidly dressed, with a pair of white kid gloves in one hand and a large fan in the other: he came trotting along in a great hurry, muttering to himself as he came, ‘Oh! the Duchess, the Duchess! Oh! won’t she be savage if I’ve kept her waiting!’ Alice felt so desperate that she was ready to ask help of any one; so, when the Rabbit came near her, she began, in a low, timid voice, ‘If you please, sir–’ The Rabbit started violently, dropped the white kid gloves and the fan, and skurried away into the darkness as hard as he could go.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: About four inches deep.

**Codex annotation notes:** Voice-like text pair with historical q009.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av057</strong> · voice_like_noisy_text · answered · FAST_CONFIRM</summary>

**Question:** uh who was accused of stealing the queen’s tarts again

**Proposed status:** `answered`

**Proposed reference answer:** The Knave of Hearts was accused of stealing them.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_av057`

**Evidence event:** `event_alice_tart_trial_opening`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** `q028`

**Tags:** `metamorphic`, `voice_like`

### Required claims and original context

#### C1: The court accusation names the Knave of Hearts as the alleged thief.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 82, "chapter": "11", "pdf_block": 7}`

**Exact supporting span:**

```text
The Knave of Hearts, he stole those tarts
```

**Preceding context:**

```text
‘Herald, read the accusation!’ said the King. On this the White Rabbit blew three blasts on the trumpet, and then unrolled the parchment scroll, and read as follows:–
```

**Supporting paragraph/context:**

```text
‘The Queen of Hearts, she made some tarts, All on a summer day: The Knave of Hearts, he stole those tarts, And took them quite away!’
```

**Following context:**

```text
‘Consider your verdict,’ the King said to the jury. ‘Not yet, not yet!’ the Rabbit hastily interrupted. ‘There’s a great deal to come before that!’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The court accusation names the Knave of Hearts as the alleged thief.

**Codex annotation notes:** The answer now preserves accusation status rather than treating the charge as proven fact. Linked to q028: distinct target claim, shared source event; fact-family IDs are not independent-event counts.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av058</strong> · voice_like_noisy_text · answered · FAST_CONFIRM</summary>

**Question:** Did the little cake say eat me?

**Proposed status:** `answered`

**Proposed reference answer:** Yes. “EAT ME” was marked on it in currants.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `alice_eat_me_cake_label`

**Evidence event:** `event_alice_eat_me_cake_label`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `meta_eat_me` / `none`

**Related cases:** `q008`

**Tags:** `metamorphic`, `voice_like`

### Required claims and original context

#### C1: Yes. “EAT ME” was marked on it in currants.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 17, "chapter": "1", "pdf_block": 2}`

**Exact supporting span:**

```text
words ‘EAT ME’ were beautifully marked in currants
```

**Preceding context:**

```text
sharply; ‘I advise you to leave oﬀthis minute!’ She generally gave herself very good advice, (though she very seldom followed it), and sometimes she scolded herself so severely as to bring tears into her eyes; and once she remembered trying to box her own ears for having cheated herself in a game of croquet she was playing against herself, for this curious child was very fond of pretending to be two people. ‘But it’s no use now,’ thought poor Alice, ‘to pretend to be two people! Why, there’s hardly enough of me left to make ONE respectable person!’
```

**Supporting paragraph/context:**

```text
Soon her eye fell on a little glass box that was lying under the table: she opened it, and found in it a very small cake, on which the words ‘EAT ME’ were beautifully marked in currants. ‘Well, I’ll eat it,’ said Alice, ‘and if it makes me grow larger, I can reach the key; and if it makes me grow smaller, I can creep under the door; so either way I’ll get into the garden, and I don’t care which happens!’
```

**Following context:**

```text
She ate a little bit, and said anxiously to herself, ‘Which way? Which way?’, holding her hand on the top of her head to feel which way it was growing, and she was quite surprised to ﬁnd that she remained the same size: to be sure, this generally happens when one eats cake, but Alice had got so much into the way of expecting nothing but out-of-the-way things to happen, that it seemed quite dull and stupid for life to go on in the common way.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Yes. “EAT ME” was marked on it in currants.

**Codex annotation notes:** Voice-like text pair with historical q008.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av059</strong> · voice_like_noisy_text · answered · FAST_CONFIRM</summary>

**Question:** Uh what do the two mushroom sides do?

**Proposed status:** `answered`

**Proposed reference answer:** One makes Alice grow taller and the other makes her grow shorter.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `alice_mushroom_sides`

**Evidence event:** `event_alice_mushroom_sides`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `meta_mushroom` / `none`

**Related cases:** `q017`

**Tags:** `metamorphic`, `voice_like`

### Required claims and original context

#### C1: One makes Alice grow taller and the other makes her grow shorter.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 40, "chapter": "5", "pdf_block": 6}`

**Exact supporting span:**

```text
One side will make you grow taller, and the other side will make you grow shorter
```

**Preceding context:**

```text
‘You’ll get used to it in time,’ said the Caterpillar; and it put the hookah into its mouth and began smoking again.
```

**Supporting paragraph/context:**

```text
This time Alice waited patiently until it chose to speak again. In a minute or two the Caterpillar took the hookah out of its mouth and yawned once or twice, and shook itself. Then it got down oﬀthe mushroom, and crawled away in the grass, merely remarking as it went, ‘One side will make you grow taller, and the other side will make you grow shorter.’
```

**Following context:**

```text
‘One side of WHAT? The other side of WHAT?’ thought Alice to herself. ‘Of the mushroom,’ said the Caterpillar, just as if she had asked it aloud; and in another moment it was out of sight.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: One makes Alice grow taller and the other makes her grow shorter.

**Codex annotation notes:** Voice-like text pair with historical q017.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>av060</strong> · voice_like_noisy_text · answered · FAST_CONFIRM</summary>

**Question:** Who came after the hatter as the witness, was it the cook?

**Proposed status:** `answered`

**Proposed reference answer:** Yes. The next witness was the Duchess’s cook.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `alice_cook_witness`

**Evidence event:** `event_alice_cook_witness`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `meta_cook_witness` / `none`

**Related cases:** `q029`, `av040`

**Tags:** `metamorphic`, `voice_like`

### Required claims and original context

#### C1: Yes. The next witness was the Duchess’s cook.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 85, "chapter": "11", "pdf_block": 5}`

**Exact supporting span:**

```text
next witness was the Duchess’s cook
```

**Preceding context:**

```text
‘–and just take his head oﬀoutside,’ the Queen added to one of the oﬃcers: but the Hatter was out of sight before the oﬃcer could get to the door.
```

**Supporting paragraph/context:**

```text
‘Call the next witness!’ said the King. The next witness was the Duchess’s cook. She carried the pepper-box in her hand, and Alice guessed who it was, even before she got into the court, by the way the people near the door began sneezing all at once.
```

**Following context:**

```text
‘Give your evidence,’ said the King. ‘Shan’t,’ said the cook. The King looked anxiously at the White Rabbit, who said in a low voice, ‘Your Majesty must cross-examine THIS witness.’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Yes. The next witness was the Duchess’s cook.

**Codex annotation notes:** Voice-like text pair with historical q029.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>c001</strong> · unanswerable_false_premise · insufficient_evidence · DEEP_REVIEW — historical, needs owner attention</summary>

**Question:** What was Alice's exact home street address?

**Proposed status:** `insufficient_evidence`

**Proposed reference answer:** No supporting evidence was found in the reviewed text of the exact evaluation book after targeted whole-document verification.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `fact_c001`

**Evidence event:** `event_fact_c001`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `historical_case`, `phase4_reuse`, `whole_document_negative_check`

### Whole-document negative verification

**Scope:** complete text content of Alice PDF SHA-256 49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e

**Entity aliases:** `Alice`, `Alice's home`, `her house`

**Negative terms:** `Alice street address`, `home address`, `postal address`

**Relation variants:** `lives at`, `resides at`, `address is`, `home in`

**Morphological variants:** `address`, `addresses`, `addressed`, `residence`, `street`

**Semantic variants:** `where exactly does Alice live`, `house number and street`

**Plausible counterexamples:** `The mock address to ALICE'S RIGHT FOOT`, `mentions of Alice's home and Dinah`

**Counterexample disposition:** The foot address is a joke addressed to her foot, and home references contain no street or house number.

#### Search: `street/home address`

- Pattern: `\b(?:street|home)\s+address\b`
- All matches reviewed: `true`
- Assessment: No direct address relation.

Source matches (0):
- none

#### Search: `address variants`

- Pattern: `\baddress\w*\b`
- All matches reviewed: `true`
- Assessment: Hits are speech verbs, not postal locations.

Source matches (3):
- page 29: ce of an oyster!’ ‘I wish I had our Dinah here, I know I do!’ said Alice aloud, addressing nobody in particular. ‘She’d soon fetch it back!’ ‘And who is Dinah, if I might venture to ask the question?’ said the
- page 37: time in silence: at last the Caterpillar took the hookah out of its mouth, and addressed her in a languid, sleepy voice. ‘Who are YOU?’ said the Caterpillar. This was not an encouraging opening for a conversa
- page 45: den violence that Alice quite jumped; but she saw in another moment that it was addressed to the baby, and not to her, so she took courage, and went on again:– ‘I didn’t know that Cheshire cats always grinned;

#### Search: `street/residence`

- Pattern: `\b(?:streets?|residence)\b`
- All matches reviewed: `true`
- Assessment: No residential location is supplied.

Source matches (0):
- none

**Bounded conclusion:** No supporting evidence was found in the reviewed book text after targeted whole-document verification.. This is not mathematical proof of absence.

**Codex annotation notes:** A plausible biographical detail that the story does not supply; tests refusal to fill a gap from world knowledge. Negative verification is bounded whole-document review, not mathematical proof of absence; absolute_absence_claimed remains false.

**Annotation confidence / review tier:** `needs_owner_review` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>c002</strong> · unanswerable_false_premise · insufficient_evidence · DEEP_REVIEW — historical, needs owner attention</summary>

**Question:** What was the Queen of Hearts' date of birth?

**Proposed status:** `insufficient_evidence`

**Proposed reference answer:** No supporting evidence was found in the reviewed text of the exact evaluation book after targeted whole-document verification.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `fact_c002`

**Evidence event:** `event_fact_c002`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `historical_case`, `phase4_reuse`, `whole_document_negative_check`

### Whole-document negative verification

**Scope:** complete text content of Alice PDF SHA-256 49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e

**Entity aliases:** `Queen of Hearts`, `Queen`, `her Majesty`

**Negative terms:** `Queen date of birth`, `Queen birthday`, `Queen age`

**Relation variants:** `was born`, `birthday is`, `years old`, `age of the Queen`

**Morphological variants:** `born`, `birth`, `birthday`, `age`, `aged`

**Semantic variants:** `when was the Queen born`, `how old is the Queen`

**Plausible counterexamples:** `birthday-present discussion`, `ages of Alice/Lory`, `edition years in the PDF front matter`

**Counterexample disposition:** None relates a birth date or age to the Queen of Hearts; front-matter years are not story chronology.

#### Search: `birth-date variants`

- Pattern: `\b(?:date of birth|birth date|born)\b`
- All matches reviewed: `true`
- Assessment: No birth-date assertion.

Source matches (0):
- none

#### Search: `birthday/age`

- Pattern: `\b(?:birthday|age|years? old)\b`
- All matches reviewed: `true`
- Assessment: Hits concern other people or birthday presents, not the Queen’s birth date.

Source matches (5):
- page 20: e!’ And she began thinking over all the children she knew that were of the same age as herself, to see if she could have been changed for any of them. ‘I’m sure I’m not Ada,’ she said, ‘for her hair goe
- page 25: without knowing how old it was, and, as the Lory positively refused to tell its age, there was no more to be said. At last the Mouse, who seemed to be a person of authority among them, called out, ‘Sit d
- page 38: e very white; And yet you incessantly stand on your head– Do you think, at your age, it is right?’ ‘In my youth,’ Father William replied to his son, ‘I feared it might injure the brain; But, now that I’
- page 69: ‘A cheap sort of present!’ thought Alice. ‘I’m glad they don’t give birthday presents like that!’ But she did not venture to say it out loud. ‘Thinking again?’ the Duchess asked, with another dig
- page 81: roud of it: for she thought, and rightly too, that very few little girls of her age knew the meaning of it at all. However, ‘jury-men’ would have done just as well. The twelve jurors were all writing ver

#### Search: `Queen of Hearts`

- Pattern: `\bQueen of Hearts\b`
- All matches reviewed: `true`
- Assessment: Entity scenes do not supply a birth date.

Source matches (4):
- page 53: th his tea spoon at the March Hare,) ‘–it was at the great concert given by the Queen of Hearts, and I had to sing “Twinkle, twinkle, little bat!
- page 60: imson velvet cushion; and, last of all this grand procession, came THE KING AND QUEEN OF HEARTS. Alice was rather doubtful whether she ought not to lie down on her face like the three gardeners, but she could not re
- page 81: Chapter 11 Who Stole the Tarts? The King and Queen of Hearts were seated on their throne when they arrived, with a great crowd assembled about them–all sorts of little birds and be
- page 82: he trumpet, and then unrolled the parchment scroll, and read as follows:– ‘The Queen of Hearts, she made some tarts, All on a summer day: The Knave of Hearts, he stole those tarts, And took them quite away!’ ‘Cons

**Bounded conclusion:** No supporting evidence was found in the reviewed book text after targeted whole-document verification.. This is not mathematical proof of absence.

**Codex annotation notes:** Tests a confident-sounding unsupported request about a real character. Negative verification is bounded whole-document review, not mathematical proof of absence; absolute_absence_claimed remains false.

**Annotation confidence / review tier:** `needs_owner_review` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>c003</strong> · ambiguous_underspecified · ambiguous · DEEP_REVIEW — historical, needs owner attention</summary>

**Question:** What happened after Alice changed size?

**Proposed status:** `ambiguous`

**Proposed reference answer:** The question needs the particular size change or scene because Alice changes size several times.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_c003`

**Evidence event:** `event_fact_c003`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `ambiguity`, `historical_case`

### Ambiguity rationale

**Type:** `book_dependent_multiple_events`

Alice changes size in several distinct scenes.

**Minimal clarification:** Which size-change scene do you mean?

**Plausible referent A1 — `{"book": "alice_in_wonderland", "page": 16, "chapter": "1", "pdf_block": 5}`**

```text
And so it was indeed: she was now only ten inches high, and her face brightened up at the thought that she was now the right size for going through the little door into that lovely garden. First, however, she waited for a few minutes to see if she was going to shrink any further: she felt a little nervous about this; ‘for it might end, you know,’ said Alice to herself, ‘in my going out altogether, like a candle. I wonder what I should be like then?’ And she tried to fancy what the ﬂame of a candle is like after the candle is blown out, for she could not remember ever having seen such a thing.
```

**Plausible referent A2 — `{"book": "alice_in_wonderland", "page": 21, "chapter": "2", "pdf_block": 4}`**

```text
As she said this she looked down at her hands, and was surprised to see that she had put on one of the Rabbit’s little white kid gloves while she was talking. ‘How CAN I have done that?’ she thought. ‘I must be growing small again.’ She got up and went to the table to measure herself by it, and found that, as nearly as she could guess, she was now about two feet high, and was going on shrinking rapidly: she soon found out that the cause of this was the fan she was holding, and she dropped it hastily, just in time to avoid shrinking away altogether.
```

**Plausible referent A3 — `{"book": "alice_in_wonderland", "page": 42, "chapter": "5", "pdf_block": 6}`**

```text
‘Well, be oﬀ, then!’ said the Pigeon in a sulky tone, as it settled down again into its nest. Alice crouched down among the trees as well as she could, for her neck kept getting entangled among the branches, and every now and then she had to stop and untwist it. After a while she remembered that she still held the pieces of mushroom in her hands, and she set to work very carefully, nibbling ﬁrst at one and then at the other, and growing sometimes taller and sometimes shorter, until she had succeeded in bringing herself down to her usual height.
```

**Codex annotation notes:** Alice changes size repeatedly; a useful answer requires a scene or cause.

**Annotation confidence / review tier:** `needs_owner_review` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>c004</strong> · ambiguous_underspecified · ambiguous · DEEP_REVIEW — historical, needs owner attention</summary>

**Question:** What happened next?

**Proposed status:** `ambiguous`

**Proposed reference answer:** The question needs the event or passage to continue from because the book contains many possible next events.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_c004`

**Evidence event:** `event_fact_c004`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `ambiguity`, `historical_case`

### Ambiguity rationale

**Type:** `missing_conversational_referent`

No prior conversational event is supplied; “next” has no unique referent.

**Minimal clarification:** Which event or passage should I continue from?

**Codex annotation notes:** A realistic voice follow-up without conversation memory; tests whether the system asks which event or passage to continue from.

**Annotation confidence / review tier:** `needs_owner_review` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>c005</strong> · multi_fact_single_context · answered · DEEP_REVIEW — historical, needs owner attention</summary>

**Question:** How tall did Alice become before the pool formed, and how deep was the pool?

**Proposed status:** `answered`

**Proposed reference answer:** Alice became more than nine feet tall, and the pool was about four inches deep.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `alice_height_pool_depth`

**Evidence event:** `event_alice_height_pool_depth`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `meta_height_pool` / `none`

**Related cases:** `q009`, `av056`

**Tags:** `contrastive_pair`, `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: Alice became more than nine feet tall.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 19, "chapter": "2", "pdf_block": 8}`

**Exact supporting span:**

```text
more than nine feet high
```

**Preceding context:**

```text
And she went on planning to herself how she would manage it. ‘They must go by the carrier,’ she thought; ‘and how funny it’ll seem, sending presents to one’s own feet! And how odd the directions will look!
```

**Supporting paragraph/context:**

```text
Oh dear, what nonsense I’m talking!’ Just then her head struck against the roof of the hall: in fact she was now more than nine feet high, and she at once took up the little golden key and hurried oﬀto the garden door.
```

**Following context:**

```text
Poor Alice! It was as much as she could do, lying down on one side, to look through into the garden with one eye; but to get through was more hopeless than ever: she sat down and began to cry again.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Alice became more than nine feet tall.

#### C2: The pool was about four inches deep.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 20, "chapter": "2", "pdf_block": 1}`

**Exact supporting span:**

```text
about four inches deep
```

**Preceding context:**

```text
Poor Alice! It was as much as she could do, lying down on one side, to look through into the garden with one eye; but to get through was more hopeless than ever: she sat down and began to cry again.
```

**Supporting paragraph/context:**

```text
‘You ought to be ashamed of yourself,’ said Alice, ‘a great girl like you,’ (she might well say this), ‘to go on crying in this way! Stop this moment, I tell you!’ But she went on all the same, shedding gallons of tears, until there was a large pool all round her, about four inches deep and reaching half down the hall.
```

**Following context:**

```text
After a time she heard a little pattering of feet in the distance, and she hastily dried her eyes to see what was coming. It was the White Rabbit returning, splendidly dressed, with a pair of white kid gloves in one hand and a large fan in the other: he came trotting along in a great hurry, muttering to himself as he came, ‘Oh! the Duchess, the Duchess! Oh! won’t she be savage if I’ve kept her waiting!’ Alice felt so desperate that she was ready to ask help of any one; so, when the Rabbit came near her, she began, in a low, timid voice, ‘If you please, sir–’ The Rabbit started violently, dropped the white kid gloves and the fan, and skurried away into the darkness as hard as he could go.
```

**Context incomplete:** `false`

**Why it supports this claim:** The narrator states that the pool around Alice was about four inches deep.

**Codex annotation notes:** Metamorphic restatement of q009. Both numeric facts belong to one continuous growth-and-tears sequence; the four-inch depth is narrator description.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>c006</strong> · contrastive_distractor · answered · DEEP_REVIEW — historical, needs owner attention</summary>

**Question:** After the Caucus-race, what did the other racers receive and what did Alice receive?

**Proposed status:** `answered`

**Proposed reference answer:** The others received comfits from Alice, while Alice received her own thimble from the Dodo.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `alice_caucus_prizes`

**Evidence event:** `event_alice_caucus_prizes`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `meta_caucus_prizes` / `contrast_caucus_prizes`

**Related cases:** `q013`, `av044`

**Tags:** `contrastive_pair`, `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: The others received comfits.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 27, "chapter": "3", "pdf_block": 3}`

**Exact supporting span:**

```text
handed them round as prizes
```

**Preceding context:**

```text
‘But who is to give the prizes?’ quite a chorus of voices asked. ‘Why, SHE, of course,’ said the Dodo, pointing to Alice with one ﬁnger; and the whole party at once crowded round her, calling out in a confused way, ‘Prizes! Prizes!’
```

**Supporting paragraph/context:**

```text
Alice had no idea what to do, and in despair she put her hand in her pocket, and pulled out a box of comﬁts, (luckily the salt water had not got into it), and handed them round as prizes. There was exactly one a-piece all round.
```

**Following context:**

```text
‘But she must have a prize herself, you know,’ said the Mouse. ‘Of course,’ the Dodo replied very gravely. ‘What else have you got in your pocket?’ he went on, turning to Alice.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The others received comfits.

#### C2: Alice received a thimble.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 27, "chapter": "3", "pdf_block": 5}`

**Exact supporting span:**

```text
acceptance of this elegant thimble
```

**Preceding context:**

```text
‘But she must have a prize herself, you know,’ said the Mouse. ‘Of course,’ the Dodo replied very gravely. ‘What else have you got in your pocket?’ he went on, turning to Alice.
```

**Supporting paragraph/context:**

```text
‘Only a thimble,’ said Alice sadly. ‘Hand it over here,’ said the Dodo. Then they all crowded round her once more, while the Dodo solemnly pre- sented the thimble, saying ‘We beg your acceptance of this elegant thimble’; and, when it had ﬁnished this short speech, they all cheered.
```

**Following context:**

```text
Alice thought the whole thing very absurd, but they all looked so grave that she did not dare to laugh; and, as she could not think of anything to say, she simply bowed, and took the thimble, looking as solemn as she could.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Alice received a thimble.

**Codex annotation notes:** Useful contrastive/metamorphic member of the q013 prize family; not independent breadth.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q001</strong> · direct_factual_single_source · answered · FAST_CONFIRM — historical</summary>

**Question:** Who wrote Alice's Adventures in Wonderland?

**Proposed status:** `answered`

**Proposed reference answer:** Lewis Carroll.

**Book / difficulty:** `alice_in_wonderland` / `easy`

**Fact family:** `fact_q001`

**Evidence event:** `event_fact_q001`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `historical_case`, `known_bad_case`, `phase4_reuse`

### Required claims and original context

#### C1: Lewis Carroll.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 1, "chapter": null, "pdf_block": 1}`

**Exact supporting span:**

```text
Lewis Carroll
```

**Preceding context:**

```text
Alice in Wonderland
```

**Supporting paragraph/context:**

```text
Lewis Carroll
```

**Following context:**

```text
This is the Project Gutenberg Etext of Alice in Wonderland [Originally released in January, 1991] Copyright laws are changing all over the world, be sure to check the copyright laws for your country before posting these ﬁles!! Please take a look at the important information in this header. We encourage you to keep this ﬁle on your own disk, keeping an electronic path open for the next readers. Do not remove this. It must legally be the ﬁrst thing seem when opening the book. In fact, our legal advisors said we can’t even change margins. Welcome To The World of Free Plain Vanilla Electronic Texts Etexts Readable By Both Humans and By Computers, Since 1971 These Etexts Prepared By Hundreds of Volunteers and Donations Information on contacting Project Gutenberg to get Etexts, and further information is included below. We need your donations.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Lewis Carroll.

**Codex annotation notes:** Reused historical Phase-4 case; proposed V2 classification does not change its old result.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q002</strong> · direct_factual_single_source · answered · FAST_CONFIRM — historical</summary>

**Question:** How many chapters are listed, and what is the final chapter called?

**Proposed status:** `answered`

**Proposed reference answer:** There are twelve chapters; the final chapter is Alice's Evidence.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_q002`

**Evidence event:** `event_fact_q002`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: The contents list has twelve chapters and names chapter twelve ‘Alice’s Evidence.’

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 11, "chapter": null, "pdf_block": 12}`

**Exact supporting span:**

```text
12 Alice’s Evidence
```

**Preceding context:**

```text
11 Who Stole the Tarts? 81
```

**Supporting paragraph/context:**

```text
12 Alice’s Evidence 87
```

**Following context:**

```text
Down the Rabbit-Hole
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The contents list has twelve chapters and names chapter twelve ‘Alice’s Evidence.’

**Codex annotation notes:** Both requested values are explicit in one contents entry, so this is one local evidence unit rather than multi-source evidence.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q003</strong> · direct_factual_single_source · answered · FAST_CONFIRM — historical</summary>

**Question:** What color were the White Rabbit's eyes?

**Proposed status:** `answered`

**Proposed reference answer:** Pink.

**Book / difficulty:** `alice_in_wonderland` / `easy`

**Fact family:** `alice_rabbit_eye_color`

**Evidence event:** `event_alice_rabbit_eye_color`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `meta_rabbit_eyes` / `none`

**Related cases:** `av054`

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: Pink.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 13, "chapter": "1", "pdf_block": 3}`

**Exact supporting span:**

```text
White Rabbit with pink eyes
```

**Preceding context:**

```text
Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, ‘and what is the use of a book,’ thought Alice ‘without pictures or conversation?’
```

**Supporting paragraph/context:**

```text
So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.
```

**Following context:**

```text
There was nothing so VERY remarkable in that; nor did Alice think it so VERY much out of the way to hear the Rabbit say to itself, ‘Oh dear! Oh dear! I shall be late!’ (when she thought it over afterwards, it occurred to her that she ought to have wondered at this, but at the time it all seemed quite natural); but when the Rabbit actually TOOK A WATCH OUT OF ITS WAISTCOAT- POCKET, and looked at it, and then hurried on, Alice started to her feet, for it ﬂashed across her mind that she had never before seen a rabbit with either a waistcoat-pocket, or a watch to take out of it, and burning with curiosity, she ran across the ﬁeld after it, and fortunately was just in time to see it pop down a large rabbit-hole under the hedge.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Pink.

**Codex annotation notes:** Reused historical Phase-4 case; proposed V2 classification does not change its old result.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q004</strong> · direct_factual_single_source · answered · FAST_CONFIRM — historical</summary>

**Question:** What was disappointing about the orange marmalade jar?

**Proposed status:** `answered`

**Proposed reference answer:** It was empty.

**Book / difficulty:** `alice_in_wonderland` / `easy`

**Fact family:** `fact_q004`

**Evidence event:** `event_fact_q004`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: It was empty.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 14, "chapter": "1", "pdf_block": 1}`

**Exact supporting span:**

```text
to her great disappointment it was empty
```

**Preceding context:**

```text
Either the well was very deep, or she fell very slowly, for she had plenty of time as she went down to look about her and to wonder what was going
```

**Supporting paragraph/context:**

```text
to happen next. First, she tried to look down and make out what she was coming to, but it was too dark to see anything; then she looked at the sides of the well, and noticed that they were ﬁlled with cupboards and book- shelves; here and there she saw maps and pictures hung upon pegs. She took down a jar from one of the shelves as she passed; it was labelled ‘ORANGE MARMALADE’, but to her great disappointment it was empty: she did not like to drop the jar for fear of killing somebody, so managed to put it into one of the cupboards as she fell past it.
```

**Following context:**

```text
‘Well!’ thought Alice to herself, ‘after such a fall as this, I shall think nothing of tumbling down stairs! How brave they’ll all think me at home! Why, I wouldn’t say anything about it, even if I fell oﬀthe top of the house!’ (Which was very likely true.)
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: It was empty.

**Codex annotation notes:** Reused historical Phase-4 case; proposed V2 classification does not change its old result.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q005</strong> · direct_factual_single_source · answered · FAST_CONFIRM — historical</summary>

**Question:** What was the name of Alice's cat?

**Proposed status:** `answered`

**Proposed reference answer:** Dinah.

**Book / difficulty:** `alice_in_wonderland` / `easy`

**Fact family:** `fact_q005`

**Evidence event:** `event_fact_q005`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: Dinah.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 14, "chapter": "1", "pdf_block": 5}`

**Exact supporting span:**

```text
Dinah was the cat
```

**Preceding context:**

```text
Presently she began again. ‘I wonder if I shall fall right THROUGH the earth! How funny it’ll seem to come out among the people that walk with their heads downward! The Antipathies, I think–’ (she was rather glad there WAS no one listening, this time, as it didn’t sound at all the right word) ‘–but I shall have to ask them what the name of the country is, you know. Please, Ma’am, is this New Zealand or Australia?’ (and she tried to curtsey as she spoke–fancy CURTSEYING as you’re falling through the air! Do you think you could manage it?) ‘And what an ignorant little girl she’ll think me for asking! No, it’ll never do to ask: perhaps I shall see it written up somewhere.’
```

**Supporting paragraph/context:**

```text
Down, down, down. There was nothing else to do, so Alice soon began talking again. ‘Dinah’ll miss me very much to-night, I should think!’ (Dinah was the cat.) ‘I hope they’ll remember her saucer of milk at tea-time. Dinah my dear! I wish you were down here with me! There are no mice in the air, I’m afraid, but you might catch a bat, and that’s very like a mouse, you know. But do cats eat bats, I wonder?’ And here Alice began to get rather
```

**Following context:**

```text
sleepy, and went on saying to herself, in a dreamy sort of way, ‘Do cats eat bats? Do cats eat bats?’ and sometimes, ‘Do bats eat cats?’ for, you see, as she couldn’t answer either question, it didn’t much matter which way she put it. She felt that she was dozing oﬀ, and had just begun to dream that she was walking hand in hand with Dinah, and saying to her very earnestly, ‘Now, Dinah, tell me the truth: did you ever eat a bat?’ when suddenly, thump! thump! down she came upon a heap of sticks and dry leaves, and the fall was over.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Dinah.

**Codex annotation notes:** Reused historical Phase-4 case; proposed V2 classification does not change its old result.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q006</strong> · direct_factual_single_source · answered · FAST_CONFIRM — historical</summary>

**Question:** Approximately how tall was the little door Alice found?

**Proposed status:** `answered`

**Proposed reference answer:** About fifteen inches high.

**Book / difficulty:** `alice_in_wonderland` / `easy`

**Fact family:** `fact_q006`

**Evidence event:** `event_fact_q006`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: About fifteen inches high.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 15, "chapter": "1", "pdf_block": 4}`

**Exact supporting span:**

```text
little door about fifteen inches high
```

**Preceding context:**

```text
There were doors all round the hall, but they were all locked; and when Alice had been all the way down one side and up the other, trying every door, she walked sadly down the middle, wondering how she was ever to get out again.
```

**Supporting paragraph/context:**

```text
Suddenly she came upon a little three-legged table, all made of solid glass; there was nothing on it except a tiny golden key, and Alice’s ﬁrst thought was that it might belong to one of the doors of the hall; but, alas! either the locks were too large, or the key was too small, but at any rate it would not open any of them. However, on the second time round, she came upon a low curtain she had not noticed before, and behind it was a little door about ﬁfteen inches high: she tried the little golden key in the lock, and to her great delight it ﬁtted!
```

**Following context:**

```text
Alice opened the door and found that it led into a small passage, not much larger than a rat-hole: she knelt down and looked along the passage into the loveliest garden you ever saw. How she longed to get out of that dark hall, and wander about among those beds of bright ﬂowers and those cool fountains, but she could not even get her head though the doorway; ‘and even if my head would go through,’ thought poor Alice, ‘it would be of very little use without my shoulders. Oh, how I wish I could shut up like a telescope! I think I could, if I only know how to begin.’ For, you see, so many out-of-the-way things had happened lately, that Alice had begun to think that very few things indeed were really impossible.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: About fifteen inches high.

**Codex annotation notes:** Reused historical Phase-4 case; proposed V2 classification does not change its old result.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q007</strong> · direct_factual_single_source · answered · FAST_CONFIRM — historical</summary>

**Question:** Which foods did the DRINK ME bottle taste like?

**Proposed status:** `answered`

**Proposed reference answer:** Cherry tart, custard, pineapple, roast turkey, toffee, and hot buttered toast.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_q007`

**Evidence event:** `event_fact_q007`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: The bottle’s mixed flavor contains all six listed foods.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 16, "chapter": "1", "pdf_block": 3}`

**Exact supporting span:**

```text
mixed ﬂavour of cherry- tart, custard, pine-apple, roast turkey, toﬀee, and hot buttered toast
```

**Preceding context:**

```text
It was all very well to say ‘Drink me,’ but the wise little Alice was not going to do THAT in a hurry. ‘No, I’ll look ﬁrst,’ she said, ‘and see whether it’s marked “poison” or not’; for she had read several nice little histories about children who had got burnt, and eaten up by wild beasts and other unpleasant things, all because they WOULD not remember the simple rules their friends had taught them: such as, that a red-hot poker will burn you if you hold it too long; and that if you cut your ﬁnger VERY deeply with a knife, it usually bleeds; and she had never forgotten that, if you drink much from a bottle marked ‘poison,’ it is almost certain to disagree with you, sooner or later.
```

**Supporting paragraph/context:**

```text
However, this bottle was NOT marked ‘poison,’ so Alice ventured to taste it, and ﬁnding it very nice, (it had, in fact, a sort of mixed ﬂavour of cherry- tart, custard, pine-apple, roast turkey, toﬀee, and hot buttered toast,) she very soon ﬁnished it oﬀ.
```

**Following context:**

```text
‘What a curious feeling!’ said Alice; ‘I must be shutting up like a tele- scope.’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The bottle’s mixed flavor contains all six listed foods.

**Codex annotation notes:** The six-food flavour list is narrator description, not dialogue by Alice. The normalized answer preserves all six foods.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q008</strong> · direct_factual_single_source · answered · FAST_CONFIRM — historical</summary>

**Question:** What words were marked in currants on the cake?

**Proposed status:** `answered`

**Proposed reference answer:** EAT ME.

**Book / difficulty:** `alice_in_wonderland` / `easy`

**Fact family:** `alice_eat_me_cake_label`

**Evidence event:** `event_alice_eat_me_cake_label`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `meta_eat_me` / `none`

**Related cases:** `av058`

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: EAT ME.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 17, "chapter": "1", "pdf_block": 2}`

**Exact supporting span:**

```text
words ‘EAT ME’ were beautifully marked in currants
```

**Preceding context:**

```text
sharply; ‘I advise you to leave oﬀthis minute!’ She generally gave herself very good advice, (though she very seldom followed it), and sometimes she scolded herself so severely as to bring tears into her eyes; and once she remembered trying to box her own ears for having cheated herself in a game of croquet she was playing against herself, for this curious child was very fond of pretending to be two people. ‘But it’s no use now,’ thought poor Alice, ‘to pretend to be two people! Why, there’s hardly enough of me left to make ONE respectable person!’
```

**Supporting paragraph/context:**

```text
Soon her eye fell on a little glass box that was lying under the table: she opened it, and found in it a very small cake, on which the words ‘EAT ME’ were beautifully marked in currants. ‘Well, I’ll eat it,’ said Alice, ‘and if it makes me grow larger, I can reach the key; and if it makes me grow smaller, I can creep under the door; so either way I’ll get into the garden, and I don’t care which happens!’
```

**Following context:**

```text
She ate a little bit, and said anxiously to herself, ‘Which way? Which way?’, holding her hand on the top of her head to feel which way it was growing, and she was quite surprised to ﬁnd that she remained the same size: to be sure, this generally happens when one eats cake, but Alice had got so much into the way of expecting nothing but out-of-the-way things to happen, that it seemed quite dull and stupid for life to go on in the common way.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: EAT ME.

**Codex annotation notes:** Reused historical Phase-4 case; proposed V2 classification does not change its old result.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q009</strong> · multi_source_multi_fact · answered · DEEP_REVIEW — historical, needs owner attention</summary>

**Question:** How tall did Alice become, and how deep was the pool of tears?

**Proposed status:** `answered`

**Proposed reference answer:** Alice became more than nine feet tall, and the pool was about four inches deep.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `alice_height_pool_depth`

**Evidence event:** `event_alice_height_pool_depth`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `meta_height_pool` / `none`

**Related cases:** `c005`, `av056`

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: Alice became more than nine feet tall.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 19, "chapter": "2", "pdf_block": 8}`

**Exact supporting span:**

```text
more than nine feet high
```

**Preceding context:**

```text
And she went on planning to herself how she would manage it. ‘They must go by the carrier,’ she thought; ‘and how funny it’ll seem, sending presents to one’s own feet! And how odd the directions will look!
```

**Supporting paragraph/context:**

```text
Oh dear, what nonsense I’m talking!’ Just then her head struck against the roof of the hall: in fact she was now more than nine feet high, and she at once took up the little golden key and hurried oﬀto the garden door.
```

**Following context:**

```text
Poor Alice! It was as much as she could do, lying down on one side, to look through into the garden with one eye; but to get through was more hopeless than ever: she sat down and began to cry again.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Alice became more than nine feet tall.

#### C2: The pool was about four inches deep.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 20, "chapter": "2", "pdf_block": 1}`

**Exact supporting span:**

```text
about four inches deep
```

**Preceding context:**

```text
Poor Alice! It was as much as she could do, lying down on one side, to look through into the garden with one eye; but to get through was more hopeless than ever: she sat down and began to cry again.
```

**Supporting paragraph/context:**

```text
‘You ought to be ashamed of yourself,’ said Alice, ‘a great girl like you,’ (she might well say this), ‘to go on crying in this way! Stop this moment, I tell you!’ But she went on all the same, shedding gallons of tears, until there was a large pool all round her, about four inches deep and reaching half down the hall.
```

**Following context:**

```text
After a time she heard a little pattering of feet in the distance, and she hastily dried her eyes to see what was coming. It was the White Rabbit returning, splendidly dressed, with a pair of white kid gloves in one hand and a large fan in the other: he came trotting along in a great hurry, muttering to himself as he came, ‘Oh! the Duchess, the Duchess! Oh! won’t she be savage if I’ve kept her waiting!’ Alice felt so desperate that she was ready to ask help of any one; so, when the Rabbit came near her, she began, in a low, timid voice, ‘If you please, sir–’ The Rabbit started violently, dropped the white kid gloves and the fan, and skurried away into the darkness as hard as he could go.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The pool was about four inches deep.

**Codex annotation notes:** Reused historical Phase-4 case; proposed V2 classification does not change its old result.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q010</strong> · direct_factual_single_source · answered · FAST_CONFIRM — historical</summary>

**Question:** What caused Alice to start shrinking while she was thinking about whether she had become Mabel?

**Proposed status:** `answered`

**Proposed reference answer:** The White Rabbit’s fan she was holding caused her to shrink.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `alice_fan_shrinking`

**Evidence event:** `event_alice_fan_shrinking`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** `av041`

**Tags:** `historical_case`, `known_bad_case`, `phase4_reuse`

### Required claims and original context

#### C1: The fan in Alice’s hand caused the shrinking.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 21, "chapter": "2", "pdf_block": 4}`

**Exact supporting span:**

```text
cause of this was the fan she was holding
```

**Preceding context:**

```text
‘I’m sure those are not the right words,’ said poor Alice, and her eyes ﬁlled with tears again as she went on, ‘I must be Mabel after all, and I shall have to go and live in that poky little house, and have next to no toys to play with, and oh! ever so many lessons to learn! No, I’ve made up my mind about it; if I’m Mabel, I’ll stay down here! It’ll be no use their putting their heads down and saying “Come up again, dear!” I shall only look up and say “Who am I then? Tell me that ﬁrst, and then, if I like being that person, I’ll come up: if not, I’ll stay down here till I’m somebody else”–but, oh dear!’ cried Alice, with a sudden burst of tears, ‘I do wish they WOULD put their heads down! I am so VERY tired of being all alone here!’
```

**Supporting paragraph/context:**

```text
As she said this she looked down at her hands, and was surprised to see that she had put on one of the Rabbit’s little white kid gloves while she was talking. ‘How CAN I have done that?’ she thought. ‘I must be growing small again.’ She got up and went to the table to measure herself by it, and found that, as nearly as she could guess, she was now about two feet high, and was going on shrinking rapidly: she soon found out that the cause of this was the fan she was holding, and she dropped it hastily, just in time to avoid shrinking away altogether.
```

**Following context:**

```text
‘That WAS a narrow escape!’ said Alice, a good deal frightened at the sudden change, but very glad to ﬁnd herself still in existence; ‘and now for the garden!’ and she ran with all speed back to the little door: but, alas! the little door was shut again, and the little golden key was lying on the glass table as before, ‘and things are worse than ever,’ thought the poor child, ‘for I never was so small as this before, never! And I declare it’s too bad, that it is!’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The fan in Alice’s hand caused the shrinking.

**Codex annotation notes:** 4.75B removes the old false chronology: Alice had not met or spoken to the Mouse yet.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q011</strong> · local_context_reasoning · answered · DEEP_REVIEW — historical, needs owner attention</summary>

**Question:** Why did Alice address the Mouse in French?

**Proposed status:** `answered`

**Proposed reference answer:** Alice guessed that the Mouse might not understand English and might be a French mouse that had come with William the Conqueror, so she tried the first sentence from her French lesson-book.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `fact_q011`

**Evidence event:** `event_fact_q011`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: Alice guessed, rather than knew, that the Mouse might be French.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 22, "chapter": "2", "pdf_block": 5}`

**Exact supporting span:**

```text
French mouse, come over with William the Conqueror
```

**Preceding context:**

```text
‘Would it be of any use, now,’ thought Alice, ‘to speak to this mouse? Everything is so out-of-the-way down here, that I should think very likely it can talk: at any rate, there’s no harm in trying.’ So she began: ‘O Mouse, do you know the way out of this pool? I am very tired of swimming about here, O Mouse!’ (Alice thought this must be the right way of speaking to a mouse: she had never done such a thing before, but she remembered having seen in her brother’s Latin Grammar, ‘A mouse–of a mouse–to a mouse–a mouse–O mouse!’) The Mouse looked at her rather inquisitively, and seemed to her to wink with one of its little eyes, but it said nothing.
```

**Supporting paragraph/context:**

```text
‘Perhaps it doesn’t understand English,’ thought Alice; ‘I daresay it’s a French mouse, come over with William the Conqueror.’ (For, with all her knowledge of history, Alice had no very clear notion how long ago anything had happened.) So she began again: ‘Ou est ma chatte?’ which was the ﬁrst sentence in her French lesson-book. The Mouse gave a sudden leap out of the water, and seemed to quiver all over with fright. ‘Oh, I beg your pardon!’ cried Alice hastily, afraid that she had hurt the poor animal’s feelings. ‘I quite forgot you didn’t like cats.’
```

**Following context:**

```text
‘Not like cats!’ cried the Mouse, in a shrill, passionate voice. ‘Would YOU like cats if you were me?’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Alice guessed, rather than knew, that the Mouse might be French.; She therefore tried a sentence from her French lesson-book.

#### C2: She therefore tried a sentence from her French lesson-book.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 22, "chapter": "2", "pdf_block": 5}`

**Exact supporting span:**

```text
French mouse, come over with William the Conqueror
```

**Preceding context:**

```text
‘Would it be of any use, now,’ thought Alice, ‘to speak to this mouse? Everything is so out-of-the-way down here, that I should think very likely it can talk: at any rate, there’s no harm in trying.’ So she began: ‘O Mouse, do you know the way out of this pool? I am very tired of swimming about here, O Mouse!’ (Alice thought this must be the right way of speaking to a mouse: she had never done such a thing before, but she remembered having seen in her brother’s Latin Grammar, ‘A mouse–of a mouse–to a mouse–a mouse–O mouse!’) The Mouse looked at her rather inquisitively, and seemed to her to wink with one of its little eyes, but it said nothing.
```

**Supporting paragraph/context:**

```text
‘Perhaps it doesn’t understand English,’ thought Alice; ‘I daresay it’s a French mouse, come over with William the Conqueror.’ (For, with all her knowledge of history, Alice had no very clear notion how long ago anything had happened.) So she began again: ‘Ou est ma chatte?’ which was the ﬁrst sentence in her French lesson-book. The Mouse gave a sudden leap out of the water, and seemed to quiver all over with fright. ‘Oh, I beg your pardon!’ cried Alice hastily, afraid that she had hurt the poor animal’s feelings. ‘I quite forgot you didn’t like cats.’
```

**Following context:**

```text
‘Not like cats!’ cried the Mouse, in a shrill, passionate voice. ‘Would YOU like cats if you were me?’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Alice guessed, rather than knew, that the Mouse might be French.; She therefore tried a sentence from her French lesson-book.

**Codex annotation notes:** The repair preserves Alice’s uncertain belief and avoids presenting it as narrator fact.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q012</strong> · direct_factual_single_source · answered · FAST_CONFIRM — historical</summary>

**Question:** What activity did the Dodo recommend to get everyone dry?

**Proposed status:** `answered`

**Proposed reference answer:** A Caucus-race.

**Book / difficulty:** `alice_in_wonderland` / `easy`

**Fact family:** `fact_q012`

**Evidence event:** `event_fact_q012`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: A Caucus-race.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 26, "chapter": "3", "pdf_block": 8}`

**Exact supporting span:**

```text
best thing to get us dry would be a Caucus-race
```

**Preceding context:**

```text
‘Speak English!’ said the Eaglet. ‘I don’t know the meaning of half those long words, and, what’s more, I don’t believe you do either!’ And the Eaglet bent down its head to hide a smile: some of the other birds tittered audibly.
```

**Supporting paragraph/context:**

```text
‘What I was going to say,’ said the Dodo in an oﬀended tone, ‘was, that the best thing to get us dry would be a Caucus-race.’
```

**Following context:**

```text
‘What IS a Caucus-race?’ said Alice; not that she wanted much to know, but the Dodo had paused as if it thought that SOMEBODY ought to speak, and no one else seemed inclined to say anything.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: A Caucus-race.

**Codex annotation notes:** Reused historical Phase-4 case; proposed V2 classification does not change its old result.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q013</strong> · contrastive_distractor · answered · DEEP_REVIEW — historical, needs owner attention</summary>

**Question:** What prizes did Alice and the other racers receive after the Caucus-race?

**Proposed status:** `answered`

**Proposed reference answer:** The others received comfits from Alice, and Alice received her own thimble from the Dodo.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `alice_caucus_prizes`

**Evidence event:** `event_alice_caucus_prizes`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `meta_caucus_prizes` / `contrast_caucus_prizes`

**Related cases:** `c006`, `av044`

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: The others received comfits.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 27, "chapter": "3", "pdf_block": 3}`

**Exact supporting span:**

```text
handed them round as prizes
```

**Preceding context:**

```text
‘But who is to give the prizes?’ quite a chorus of voices asked. ‘Why, SHE, of course,’ said the Dodo, pointing to Alice with one ﬁnger; and the whole party at once crowded round her, calling out in a confused way, ‘Prizes! Prizes!’
```

**Supporting paragraph/context:**

```text
Alice had no idea what to do, and in despair she put her hand in her pocket, and pulled out a box of comﬁts, (luckily the salt water had not got into it), and handed them round as prizes. There was exactly one a-piece all round.
```

**Following context:**

```text
‘But she must have a prize herself, you know,’ said the Mouse. ‘Of course,’ the Dodo replied very gravely. ‘What else have you got in your pocket?’ he went on, turning to Alice.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The others received comfits.

#### C2: Alice received a thimble.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 27, "chapter": "3", "pdf_block": 5}`

**Exact supporting span:**

```text
acceptance of this elegant thimble
```

**Preceding context:**

```text
‘But she must have a prize herself, you know,’ said the Mouse. ‘Of course,’ the Dodo replied very gravely. ‘What else have you got in your pocket?’ he went on, turning to Alice.
```

**Supporting paragraph/context:**

```text
‘Only a thimble,’ said Alice sadly. ‘Hand it over here,’ said the Dodo. Then they all crowded round her once more, while the Dodo solemnly pre- sented the thimble, saying ‘We beg your acceptance of this elegant thimble’; and, when it had ﬁnished this short speech, they all cheered.
```

**Following context:**

```text
Alice thought the whole thing very absurd, but they all looked so grave that she did not dare to laugh; and, as she could not think of anything to say, she simply bowed, and took the thimble, looking as solemn as she could.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Alice received a thimble.

**Codex annotation notes:** The diagnostic distinction is other racers’ comfits versus Alice’s returned thimble; all evidence is one local scene.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q014</strong> · direct_factual_single_source · answered · FAST_CONFIRM — historical</summary>

**Question:** What did the White Rabbit order 'Mary Ann' to fetch?

**Proposed status:** `answered`

**Proposed reference answer:** A pair of gloves and a fan.

**Book / difficulty:** `alice_in_wonderland` / `easy`

**Fact family:** `alice_rabbit_mary_ann_errand`

**Evidence event:** `event_alice_rabbit_mary_ann_errand`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** `q015`, `av055`

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: A pair of gloves and a fan.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 31, "chapter": "4", "pdf_block": 3}`

**Exact supporting span:**

```text
Run home this moment, and fetch me a pair of gloves and a fan
```

**Preceding context:**

```text
It was the White Rabbit, trotting slowly back again, and looking anxiously about as it went, as if it had lost something; and she heard it muttering to itself ‘The Duchess! The Duchess! Oh my dear paws! Oh my fur and whiskers! She’ll get me executed, as sure as ferrets are ferrets! Where CAN I have dropped them, I wonder?’ Alice guessed in a moment that it was looking for the fan and the pair of white kid gloves, and she very good-naturedly began hunting about for them, but they were nowhere to be seen–everything seemed to have changed since her swim in the pool, and the great hall, with the glass table and the little door, had vanished completely.
```

**Supporting paragraph/context:**

```text
Very soon the Rabbit noticed Alice, as she went hunting about, and called out to her in an angry tone, ‘Why, Mary Ann, what ARE you doing out here? Run home this moment, and fetch me a pair of gloves and a fan! Quick, now!’ And Alice was so much frightened that she ran oﬀat once in the direction it pointed to, without trying to explain the mistake it had made.
```

**Following context:**

```text
‘He took me for his housemaid,’ she said to herself as she ran. ‘How surprised he’ll be when he ﬁnds out who I am! But I’d better take him his fan and gloves–that is, if I can ﬁnd them.’ As she said this, she came upon a neat little house, on the door of which was a bright brass plate with the name ‘W. RABBIT’ engraved upon it. She went in without knocking, and hurried upstairs, in great fear lest she should meet the real Mary Ann, and be turned out of the house before she had found the fan and gloves.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: A pair of gloves and a fan.

**Codex annotation notes:** Reused historical Phase-4 case; proposed V2 classification does not change its old result.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q015</strong> · direct_factual_single_source · answered · FAST_CONFIRM — historical</summary>

**Question:** What name was engraved on the brass plate at the Rabbit's house?

**Proposed status:** `answered`

**Proposed reference answer:** W. RABBIT.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `alice_rabbit_mary_ann_errand`

**Evidence event:** `event_alice_rabbit_mary_ann_errand`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** `q014`, `av055`

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: W. RABBIT.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 31, "chapter": "4", "pdf_block": 4}`

**Exact supporting span:**

```text
name ‘W. RABBIT’ engraved upon it
```

**Preceding context:**

```text
Very soon the Rabbit noticed Alice, as she went hunting about, and called out to her in an angry tone, ‘Why, Mary Ann, what ARE you doing out here? Run home this moment, and fetch me a pair of gloves and a fan! Quick, now!’ And Alice was so much frightened that she ran oﬀat once in the direction it pointed to, without trying to explain the mistake it had made.
```

**Supporting paragraph/context:**

```text
‘He took me for his housemaid,’ she said to herself as she ran. ‘How surprised he’ll be when he ﬁnds out who I am! But I’d better take him his fan and gloves–that is, if I can ﬁnd them.’ As she said this, she came upon a neat little house, on the door of which was a bright brass plate with the name ‘W. RABBIT’ engraved upon it. She went in without knocking, and hurried upstairs, in great fear lest she should meet the real Mary Ann, and be turned out of the house before she had found the fan and gloves.
```

**Following context:**

```text
‘How queer it seems,’ Alice said to herself, ‘to be going messages for a rabbit! I suppose Dinah’ll be sending me on messages next!’ And she began
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: W. RABBIT.

**Codex annotation notes:** Reused historical Phase-4 case; proposed V2 classification does not change its old result.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q016</strong> · multi_fact_single_context · answered · DEEP_REVIEW — historical, needs owner attention</summary>

**Question:** What did the pebbles thrown through the window become, and what happened when Alice ate one?

**Proposed status:** `answered`

**Proposed reference answer:** They became little cakes, and eating one made Alice shrink.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_q016`

**Evidence event:** `event_fact_q016`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: The pebbles became cakes.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 35, "chapter": "4", "pdf_block": 4}`

**Exact supporting span:**

```text
pebbles were all turning into little cakes
```

**Preceding context:**

```text
‘A barrowful of WHAT?’ thought Alice; but she had not long to doubt, for the next moment a shower of little pebbles came rattling in at the window, and some of them hit her in the face. ‘I’ll put a stop to this,’ she said to herself, and shouted out, ‘You’d better not do that again!’ which produced another dead silence.
```

**Supporting paragraph/context:**

```text
Alice noticed with some surprise that the pebbles were all turning into little cakes as they lay on the ﬂoor, and a bright idea came into her head. ‘If I eat one of these cakes,’ she thought, ‘it’s sure to make SOME change in my size; and as it can’t possibly make me larger, it must make me smaller, I suppose.’
```

**Following context:**

```text
So she swallowed one of the cakes, and was delighted to ﬁnd that she began shrinking directly. As soon as she was small enough to get through the door, she ran out of the house, and found quite a crowd of little animals and birds waiting outside. The poor little Lizard, Bill, was in the middle, being held up by two guinea-pigs, who were giving it something out of a bottle. They all made a rush at Alice the moment she appeared; but she ran oﬀas hard as she could, and soon found herself safe in a thick wood.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The pebbles became cakes.

#### C2: Eating one made Alice shrink.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 35, "chapter": "4", "pdf_block": 5}`

**Exact supporting span:**

```text
began shrinking directly
```

**Preceding context:**

```text
Alice noticed with some surprise that the pebbles were all turning into little cakes as they lay on the ﬂoor, and a bright idea came into her head. ‘If I eat one of these cakes,’ she thought, ‘it’s sure to make SOME change in my size; and as it can’t possibly make me larger, it must make me smaller, I suppose.’
```

**Supporting paragraph/context:**

```text
So she swallowed one of the cakes, and was delighted to ﬁnd that she began shrinking directly. As soon as she was small enough to get through the door, she ran out of the house, and found quite a crowd of little animals and birds waiting outside. The poor little Lizard, Bill, was in the middle, being held up by two guinea-pigs, who were giving it something out of a bottle. They all made a rush at Alice the moment she appeared; but she ran oﬀas hard as she could, and soon found herself safe in a thick wood.
```

**Following context:**

```text
‘The ﬁrst thing I’ve got to do,’ said Alice to herself, as she wandered about in the wood, ‘is to grow to my right size again; and the second thing is to ﬁnd my way into that lovely garden. I think that will be the best plan.’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Eating one made Alice shrink.

**Codex annotation notes:** Reused historical Phase-4 case; proposed V2 classification does not change its old result. Reclassified from multi-source: the answer components belong to one continuous local event/context.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q017</strong> · paraphrase_vocabulary_mismatch · answered · FAST_CONFIRM — historical</summary>

**Question:** What different effects did the two sides of the mushroom have?

**Proposed status:** `answered`

**Proposed reference answer:** One side made Alice grow taller and the other made her grow shorter.

**Book / difficulty:** `alice_in_wonderland` / `easy`

**Fact family:** `alice_mushroom_sides`

**Evidence event:** `event_alice_mushroom_sides`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `meta_mushroom` / `none`

**Related cases:** `av059`

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: One side made Alice grow taller and the other made her grow shorter.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 40, "chapter": "5", "pdf_block": 6}`

**Exact supporting span:**

```text
One side will make you grow taller, and the other side will make you grow shorter
```

**Preceding context:**

```text
‘You’ll get used to it in time,’ said the Caterpillar; and it put the hookah into its mouth and began smoking again.
```

**Supporting paragraph/context:**

```text
This time Alice waited patiently until it chose to speak again. In a minute or two the Caterpillar took the hookah out of its mouth and yawned once or twice, and shook itself. Then it got down oﬀthe mushroom, and crawled away in the grass, merely remarking as it went, ‘One side will make you grow taller, and the other side will make you grow shorter.’
```

**Following context:**

```text
‘One side of WHAT? The other side of WHAT?’ thought Alice to herself. ‘Of the mushroom,’ said the Caterpillar, just as if she had asked it aloud; and in another moment it was out of sight.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: One side made Alice grow taller and the other made her grow shorter.

**Codex annotation notes:** Reused historical Phase-4 case; proposed V2 classification does not change its old result.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q018</strong> · local_context_reasoning · answered · DEEP_REVIEW — historical, needs owner attention</summary>

**Question:** Why did the Pigeon call Alice a serpent?

**Proposed status:** `answered`

**Proposed reference answer:** The Pigeon was guarding its eggs against serpents and, seeing Alice’s unusually long neck, insisted she was a serpent. When Alice said little girls eat eggs too, the Pigeon replied conditionally that if that were true, little girls were a kind of serpent.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `fact_q018`

**Evidence event:** `event_alice_pigeon_serpent_reasoning`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** `av039`

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: The Pigeon was watching its eggs for serpents and treated Alice’s unusually long neck as a reason to call her a serpent.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 41, "chapter": "5", "pdf_block": 6}`

**Exact supporting span:**

```text
As if it wasn’t trouble enough hatching the eggs
```

**Preceding context:**

```text
Alice was more and more puzzled, but she thought there was no use in saying anything more till the Pigeon had ﬁnished.
```

**Supporting paragraph/context:**

```text
‘As if it wasn’t trouble enough hatching the eggs,’ said the Pigeon; ‘but I must be on the look-out for serpents night and day! Why, I haven’t had a wink of sleep these three weeks!’
```

**Following context:**

```text
‘I’m very sorry you’ve been annoyed,’ said Alice, who was beginning to see its meaning.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The Pigeon was exhausted from guarding its eggs against serpents.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 42, "chapter": "5", "pdf_block": 2}`

**Exact supporting span:**

```text
No, no! You’re a serpent; and there’s no use denying it.
```

**Preceding context:**

```text
The Pigeon challenges Alice’s claim that she is a little girl and focuses on her altered appearance.
```

**Supporting paragraph/context:**

```text
neck as that! No, no! You’re a serpent; and there’s no use denying it. I suppose you’ll be telling me next that you never tasted an egg!’ ‘I HAVE tasted eggs, certainly,’ said Alice, who was a very truthful child; ‘but little girls eat eggs quite as much as serpents do, you know.’ ‘I don’t believe it,’ said the Pigeon; ‘but if they do, why then they’re a kind of serpent, that’s all I can say.’
```

**Following context:**

```text
The exchange continues with the Pigeon accusing Alice of looking for eggs.
```

**Context incomplete:** `false`

**Why it supports this claim:** The continuous dialogue shows the Pigeon’s long-neck accusation and later conditional egg-based reasoning; both are character beliefs, not narrator facts.

#### C2: After Alice said little girls eat eggs, the Pigeon said conditionally that if girls do eat eggs, they are a kind of serpent.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 42, "chapter": "5", "pdf_block": 2}`

**Exact supporting span:**

```text
No, no! You’re a serpent; and there’s no use denying it.
```

**Preceding context:**

```text
The Pigeon challenges Alice’s claim that she is a little girl and focuses on her altered appearance.
```

**Supporting paragraph/context:**

```text
neck as that! No, no! You’re a serpent; and there’s no use denying it. I suppose you’ll be telling me next that you never tasted an egg!’ ‘I HAVE tasted eggs, certainly,’ said Alice, who was a very truthful child; ‘but little girls eat eggs quite as much as serpents do, you know.’ ‘I don’t believe it,’ said the Pigeon; ‘but if they do, why then they’re a kind of serpent, that’s all I can say.’
```

**Following context:**

```text
The exchange continues with the Pigeon accusing Alice of looking for eggs.
```

**Context incomplete:** `false`

**Why it supports this claim:** The continuous dialogue shows the Pigeon’s long-neck accusation and later conditional egg-based reasoning; both are character beliefs, not narrator facts.

**Codex annotation notes:** Preserves chronology and epistemic status: long-neck suspicion first, then conditional reasoning about girls eating eggs. Linked to av039: distinct target claim, shared source event; fact-family IDs are not independent-event counts.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q019</strong> · direct_factual_single_source · answered · FAST_CONFIRM — historical</summary>

**Question:** What invitation did the Fish-Footman deliver to the Duchess?

**Proposed status:** `answered`

**Proposed reference answer:** An invitation from the Queen to play croquet.

**Book / difficulty:** `alice_in_wonderland` / `easy`

**Fact family:** `fact_q019`

**Evidence event:** `event_fact_q019`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: An invitation from the Queen to play croquet.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 43, "chapter": "6", "pdf_block": 3}`

**Exact supporting span:**

```text
An invitation from the Queen to play croquet
```

**Preceding context:**

```text
For a minute or two she stood looking at the house, and wondering what to do next, when suddenly a footman in livery came running out of the wood–(she considered him to be a footman because he was in livery: otherwise, judging by his face only, she would have called him a ﬁsh)–and rapped loudly at the door with his knuckles. It was opened by another footman in livery, with a round face, and large eyes like a frog; and both footmen, Alice noticed, had powdered hair that curled all over their heads. She felt very curious to know what it was all about, and crept a little way out of the wood to listen.
```

**Supporting paragraph/context:**

```text
The Fish-Footman began by producing from under his arm a great let- ter, nearly as large as himself, and this he handed over to the other, saying, in a solemn tone, ‘For the Duchess. An invitation from the Queen to play croquet.’ The Frog-Footman repeated, in the same solemn tone, only chang- ing the order of the words a little, ‘From the Queen. An invitation for the Duchess to play croquet.’
```

**Following context:**

```text
Then they both bowed low, and their curls got entangled together. Alice laughed so much at this, that she had to run back into the wood for fear of their hearing her; and when she next peeped out the Fish-Footman was gone, and the other was sitting on the ground near the door, staring stupidly up into the sky.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: An invitation from the Queen to play croquet.

**Codex annotation notes:** Reused historical Phase-4 case; proposed V2 classification does not change its old result.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q020</strong> · paraphrase_vocabulary_mismatch · answered · FAST_CONFIRM — historical</summary>

**Question:** Which two residents did the Cheshire Cat direct Alice toward, and what did it say about them?

**Proposed status:** `answered`

**Proposed reference answer:** The Hatter and the March Hare; the Cat said they were both mad.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `alice_cat_mad_directions`

**Evidence event:** `event_alice_cat_mad_directions`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `meta_cat_mad` / `none`

**Related cases:** `av043`

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: The Hatter and the March Hare; the Cat said they were both mad.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 48, "chapter": "6", "pdf_block": 2}`

**Exact supporting span:**

```text
Hatter:
```

**Preceding context:**

```text
‘–so long as I get SOMEWHERE,’ Alice added as an explanation. ‘Oh, you’re sure to do that,’ said the Cat, ‘if you only walk long enough.’ Alice felt that this could not be denied, so she tried another question. ‘What sort of people live about here?’
```

**Supporting paragraph/context:**

```text
‘In THAT direction,’ the Cat said, waving its right paw round, ‘lives a Hatter: and in THAT direction,’ waving the other paw, ‘lives a March Hare. Visit either you like: they’re both mad.’
```

**Following context:**

```text
‘But I don’t want to go among mad people,’ Alice remarked. ‘Oh, you can’t help that,’ said the Cat: ‘we’re all mad here. I’m mad. You’re mad.’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The Hatter and the March Hare; the Cat said they were both mad.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 48, "chapter": "6", "pdf_block": 2}`

**Exact supporting span:**

```text
lives a March Hare
```

**Preceding context:**

```text
‘–so long as I get SOMEWHERE,’ Alice added as an explanation. ‘Oh, you’re sure to do that,’ said the Cat, ‘if you only walk long enough.’ Alice felt that this could not be denied, so she tried another question. ‘What sort of people live about here?’
```

**Supporting paragraph/context:**

```text
‘In THAT direction,’ the Cat said, waving its right paw round, ‘lives a Hatter: and in THAT direction,’ waving the other paw, ‘lives a March Hare. Visit either you like: they’re both mad.’
```

**Following context:**

```text
‘But I don’t want to go among mad people,’ Alice remarked. ‘Oh, you can’t help that,’ said the Cat: ‘we’re all mad here. I’m mad. You’re mad.’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The Hatter and the March Hare; the Cat said they were both mad.

**Evidence E3 location:** `{"book": "alice_in_wonderland", "page": 48, "chapter": "6", "pdf_block": 2}`

**Exact supporting span:**

```text
they’re both mad
```

**Preceding context:**

```text
‘–so long as I get SOMEWHERE,’ Alice added as an explanation. ‘Oh, you’re sure to do that,’ said the Cat, ‘if you only walk long enough.’ Alice felt that this could not be denied, so she tried another question. ‘What sort of people live about here?’
```

**Supporting paragraph/context:**

```text
‘In THAT direction,’ the Cat said, waving its right paw round, ‘lives a Hatter: and in THAT direction,’ waving the other paw, ‘lives a March Hare. Visit either you like: they’re both mad.’
```

**Following context:**

```text
‘But I don’t want to go among mad people,’ Alice remarked. ‘Oh, you can’t help that,’ said the Cat: ‘we’re all mad here. I’m mad. You’re mad.’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The Hatter and the March Hare; the Cat said they were both mad.

**Codex annotation notes:** Reused historical Phase-4 case; proposed V2 classification does not change its old result.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q021</strong> · local_context_reasoning · answered · DEEP_REVIEW — historical, needs owner attention</summary>

**Question:** What did the Duchess's baby turn into?

**Proposed status:** `answered`

**Proposed reference answer:** A pig.

**Book / difficulty:** `alice_in_wonderland` / `easy`

**Fact family:** `fact_q021`

**Evidence event:** `event_fact_q021`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `historical_case`, `known_bad_case`, `phase4_reuse`

### Required claims and original context

#### C1: A pig.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 48, "chapter": "6", "pdf_block": 9}`

**Exact supporting span:**

```text
It turned into a pig
```

**Preceding context:**

```text
‘By-the-bye, what became of the baby?’ said the Cat. ‘I’d nearly forgot- ten to ask.’
```

**Supporting paragraph/context:**

```text
‘It turned into a pig,’ Alice quietly said, just as if it had come back in a natural way.
```

**Following context:**

```text
‘I thought it would,’ said the Cat, and vanished again. Alice waited a little, half expecting to see it again, but it did not appear, and after a minute or two she walked on in the direction in which the March Hare was said to live. ‘I’ve seen hatters before,’ she said to herself; ‘the March Hare will be much the most interesting, and perhaps as this is May it won’t be raving mad–at least not so mad as it was in March.’ As she said
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: A pig.

**Codex annotation notes:** Reused historical Phase-4 case; proposed V2 classification does not change its old result.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q022</strong> · local_context_reasoning · answered · DEEP_REVIEW — historical, needs owner attention</summary>

**Question:** Who was at the tea table, and what beverage did the March Hare falsely offer Alice?

**Proposed status:** `answered`

**Proposed reference answer:** The March Hare, Hatter, and Dormouse were there; the March Hare offered wine even though there was none.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `alice_tea_party_wine`

**Evidence event:** `event_alice_tea_party_wine`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `contrast_tea_wine`

**Related cases:** `av045`

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: The March Hare, Hatter, and Dormouse were at the table.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 51, "chapter": "7", "pdf_block": 2}`

**Exact supporting span:**

```text
Hatter were having tea
```

**Preceding context:**

```text
A Mad Tea-Party
```

**Supporting paragraph/context:**

```text
There was a table set out under a tree in front of the house, and the March Hare and the Hatter were having tea at it: a Dormouse was sitting between them, fast asleep, and the other two were using it as a cushion, resting their elbows on it, and talking over its head. ‘Very uncomfortable for the Dormouse,’ thought Alice; ‘only, as it’s asleep, I suppose it doesn’t mind.’
```

**Following context:**

```text
The table was a large one, but the three were all crowded together at one corner of it: ‘No room! No room!’ they cried out when they saw Alice coming. ‘There’s PLENTY of room!’ said Alice indignantly, and she sat down in a large arm-chair at one end of the table.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The March Hare, Hatter, and Dormouse were at the table.

#### C2: The March Hare offered wine although there was none.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 51, "chapter": "7", "pdf_block": 5}`

**Exact supporting span:**

```text
There isn’t any
```

**Preceding context:**

```text
‘Have some wine,’ the March Hare said in an encouraging tone. Alice looked all round the table, but there was nothing on it but tea. ‘I don’t see any wine,’ she remarked.
```

**Supporting paragraph/context:**

```text
‘There isn’t any,’ said the March Hare. ‘Then it wasn’t very civil of you to oﬀer it,’ said Alice angrily. ‘It wasn’t very civil of you to sit down without being invited,’ said the March Hare.
```

**Following context:**

```text
‘I didn’t know it was YOUR table,’ said Alice; ‘it’s laid for a great many more than three.’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The March Hare offered wine although there was none.

**Codex annotation notes:** The wine answer requires resolving an offer against the following admission that no wine existed; it is one local dialogue, not multi-source.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q023</strong> · local_context_reasoning · answered · DEEP_REVIEW — historical, needs owner attention</summary>

**Question:** Why was it always tea-time at the Hatter's table?

**Proposed status:** `answered`

**Proposed reference answer:** The Hatter said he and Time had quarreled. After the concert incident, Time would no longer do anything the Hatter asked, so it stayed six o’clock and therefore was always tea-time.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_q023`

**Evidence event:** `event_alice_hatter_time_quarrel`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** `av037`

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: The Hatter said he had quarreled with Time and that afterward Time would no longer do what he asked.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 54, "chapter": "7", "pdf_block": 6}`

**Exact supporting span:**

```text
It’s always six o’clock now
```

**Preceding context:**

```text
The Hatter personifies Time and says that if one stays on good terms with him, Time can move or hold the clock as requested. When Alice asks whether that is how the Hatter manages, he says no and explains that they quarrelled last March.
```

**Supporting paragraph/context:**

```text
The Hatter says that at the concert the Queen cried, ‘He’s murdering the time! Off with his head!’ He continues that ever since then, Time ‘won’t do a thing I ask! It’s always six o’clock now.’
```

**Following context:**

```text
A bright idea came into Alice’s head. ‘Is that the reason so many tea- things are put out here?’ she asked.
```

**Context incomplete:** `false`

**Why it supports this claim:** The expanded context resolves ‘he’ as Time and supplies the quarrel to non-cooperation to six-o’clock causal chain.

#### C2: The Hatter said it stayed six o’clock and confirmed that this was why it was always tea-time.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 54, "chapter": "7", "pdf_block": 6}`

**Exact supporting span:**

```text
It’s always six o’clock now
```

**Preceding context:**

```text
The Hatter personifies Time and says that if one stays on good terms with him, Time can move or hold the clock as requested. When Alice asks whether that is how the Hatter manages, he says no and explains that they quarrelled last March.
```

**Supporting paragraph/context:**

```text
The Hatter says that at the concert the Queen cried, ‘He’s murdering the time! Off with his head!’ He continues that ever since then, Time ‘won’t do a thing I ask! It’s always six o’clock now.’
```

**Following context:**

```text
A bright idea came into Alice’s head. ‘Is that the reason so many tea- things are put out here?’ she asked.
```

**Context incomplete:** `false`

**Why it supports this claim:** The expanded context resolves ‘he’ as Time and supplies the quarrel to non-cooperation to six-o’clock causal chain.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 54, "chapter": "7", "pdf_block": 8}`

**Exact supporting span:**

```text
it’s always tea-time
```

**Preceding context:**

```text
A bright idea came into Alice’s head. ‘Is that the reason so many tea- things are put out here?’ she asked.
```

**Supporting paragraph/context:**

```text
‘Yes, that’s it,’ said the Hatter with a sigh: ‘it’s always tea-time, and we’ve no time to wash the things between whiles.’
```

**Following context:**

```text
‘Then you keep moving round, I suppose?’ said Alice. ‘Exactly so,’ said the Hatter: ‘as the things get used up.’ ‘But what happens when you come to the beginning again?’ Alice ven- tured to ask.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The time remained six o’clock, which made it perpetually tea-time.

**Codex annotation notes:** Evidence now includes the Time antecedent and causal chain through permanent six o’clock and tea-time. Linked to av037: distinct target claim, shared source event; fact-family IDs are not independent-event counts.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q024</strong> · multi_fact_single_context · answered · DEEP_REVIEW — historical, needs owner attention</summary>

**Question:** What served as the balls, mallets, and arches in the Queen's croquet game?

**Proposed status:** `answered`

**Proposed reference answer:** Hedgehogs were the balls, flamingoes were the mallets, and soldiers bent over to form the arches.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `alice_croquet_equipment`

**Evidence event:** `event_alice_croquet_equipment`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `meta_croquet_equipment` / `none`

**Related cases:** `av042`

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: Hedgehogs were the balls.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 62, "chapter": "8", "pdf_block": 3}`

**Exact supporting span:**

```text
balls were live hedgehogs
```

**Preceding context:**

```text
‘She boxed the Queen’s ears–’ the Rabbit began. Alice gave a little scream of laughter. ‘Oh, hush!’ the Rabbit whispered in a frightened tone. ‘The Queen will hear you! You see, she came rather late, and the Queen said–’
```

**Supporting paragraph/context:**

```text
‘Get to your places!’ shouted the Queen in a voice of thunder, and peo- ple began running about in all directions, tumbling up against each other; however, they got settled down in a minute or two, and the game began. Alice thought she had never seen such a curious croquet-ground in her life; it was all ridges and furrows; the balls were live hedgehogs, the mallets live ﬂamingoes, and the soldiers had to double themselves up and to stand on their hands and feet, to make the arches.
```

**Following context:**

```text
The chief diﬃculty Alice found at ﬁrst was in managing her ﬂamingo: she succeeded in getting its body tucked away, comfortably enough, under her arm, with its legs hanging down, but generally, just as she had got its neck nicely straightened out, and was going to give the hedgehog a blow with its head, it WOULD twist itself round and look up in her face, with such a puzzled expression that she could not help bursting out laughing: and when she had got its head down, and was going to begin again, it was very provoking to ﬁnd that the hedgehog had unrolled itself, and was in the act of crawling away: besides all this, there was generally a ridge or furrow in the way wherever she wanted to send the hedgehog to, and, as the doubled-up soldiers were always getting up and walking oﬀto other parts of the ground, Alice soon came to the conclusion that it was a very diﬃcult game indeed.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Hedgehogs were the balls.

#### C2: Flamingoes were the mallets.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 62, "chapter": "8", "pdf_block": 3}`

**Exact supporting span:**

```text
mallets live flamingoes
```

**Preceding context:**

```text
‘She boxed the Queen’s ears–’ the Rabbit began. Alice gave a little scream of laughter. ‘Oh, hush!’ the Rabbit whispered in a frightened tone. ‘The Queen will hear you! You see, she came rather late, and the Queen said–’
```

**Supporting paragraph/context:**

```text
‘Get to your places!’ shouted the Queen in a voice of thunder, and peo- ple began running about in all directions, tumbling up against each other; however, they got settled down in a minute or two, and the game began. Alice thought she had never seen such a curious croquet-ground in her life; it was all ridges and furrows; the balls were live hedgehogs, the mallets live ﬂamingoes, and the soldiers had to double themselves up and to stand on their hands and feet, to make the arches.
```

**Following context:**

```text
The chief diﬃculty Alice found at ﬁrst was in managing her ﬂamingo: she succeeded in getting its body tucked away, comfortably enough, under her arm, with its legs hanging down, but generally, just as she had got its neck nicely straightened out, and was going to give the hedgehog a blow with its head, it WOULD twist itself round and look up in her face, with such a puzzled expression that she could not help bursting out laughing: and when she had got its head down, and was going to begin again, it was very provoking to ﬁnd that the hedgehog had unrolled itself, and was in the act of crawling away: besides all this, there was generally a ridge or furrow in the way wherever she wanted to send the hedgehog to, and, as the doubled-up soldiers were always getting up and walking oﬀto other parts of the ground, Alice soon came to the conclusion that it was a very diﬃcult game indeed.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Flamingoes were the mallets.

#### C3: Soldiers formed the arches.

**Evidence E3 location:** `{"book": "alice_in_wonderland", "page": 62, "chapter": "8", "pdf_block": 3}`

**Exact supporting span:**

```text
make the arches
```

**Preceding context:**

```text
‘She boxed the Queen’s ears–’ the Rabbit began. Alice gave a little scream of laughter. ‘Oh, hush!’ the Rabbit whispered in a frightened tone. ‘The Queen will hear you! You see, she came rather late, and the Queen said–’
```

**Supporting paragraph/context:**

```text
‘Get to your places!’ shouted the Queen in a voice of thunder, and peo- ple began running about in all directions, tumbling up against each other; however, they got settled down in a minute or two, and the game began. Alice thought she had never seen such a curious croquet-ground in her life; it was all ridges and furrows; the balls were live hedgehogs, the mallets live ﬂamingoes, and the soldiers had to double themselves up and to stand on their hands and feet, to make the arches.
```

**Following context:**

```text
The chief diﬃculty Alice found at ﬁrst was in managing her ﬂamingo: she succeeded in getting its body tucked away, comfortably enough, under her arm, with its legs hanging down, but generally, just as she had got its neck nicely straightened out, and was going to give the hedgehog a blow with its head, it WOULD twist itself round and look up in her face, with such a puzzled expression that she could not help bursting out laughing: and when she had got its head down, and was going to begin again, it was very provoking to ﬁnd that the hedgehog had unrolled itself, and was in the act of crawling away: besides all this, there was generally a ridge or furrow in the way wherever she wanted to send the hedgehog to, and, as the doubled-up soldiers were always getting up and walking oﬀto other parts of the ground, Alice soon came to the conclusion that it was a very diﬃcult game indeed.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Soldiers formed the arches.

**Codex annotation notes:** Reused historical Phase-4 case; proposed V2 classification does not change its old result. All three croquet-equipment facts occur in the same narrator sentence; this is not multi-source evidence.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q025</strong> · direct_factual_single_source · answered · FAST_CONFIRM — historical</summary>

**Question:** According to the Duchess, under what condition does everything have a moral?

**Proposed status:** `answered`

**Proposed reference answer:** If only you can find it.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_q025`

**Evidence event:** `event_fact_q025`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: If only you can find it.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 67, "chapter": "9", "pdf_block": 6}`

**Exact supporting span:**

```text
Everything’s got a moral, if only you can find it
```

**Preceding context:**

```text
She had quite forgotten the Duchess by this time, and was a little startled when she heard her voice close to her ear. ‘You’re thinking about something, my dear, and that makes you forget to talk. I can’t tell you just now what the moral of that is, but I shall remember it in a bit.’
```

**Supporting paragraph/context:**

```text
‘Perhaps it hasn’t one,’ Alice ventured to remark. ‘Tut, tut, child!’ said the Duchess. ‘Everything’s got a moral, if only you can ﬁnd it.’ And she squeezed herself up closer to Alice’s side as she spoke.
```

**Following context:**

```text
Alice did not much like keeping so close to her: ﬁrst, because the Duchess was VERY ugly; and secondly, because she was exactly the right height to rest her chin upon Alice’s shoulder, and it was an uncomfortably sharp chin. However, she did not like to be rude, so she bore it as well as she could.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: If only you can find it.

**Codex annotation notes:** Reused historical Phase-4 case; proposed V2 classification does not change its old result.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q026</strong> · multi_source_multi_fact · answered · DEEP_REVIEW — historical, needs owner attention</summary>

**Question:** Which oddly named subjects did the Mock Turtle list in the regular course and in the Drawling-master’s lessons?

**Proposed status:** `answered`

**Proposed reference answer:** Reeling, Writhing, Ambition, Distraction, Uglification, Derision, Mystery (ancient and modern), Seaography, Drawling, Stretching, and Fainting in Coils.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `fact_q026`

**Evidence event:** `event_fact_q026`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: The regular course began with Reeling, Writhing, Ambition, Distraction, Uglification, and Derision.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 71, "chapter": "9", "pdf_block": 9}`

**Exact supporting span:**

```text
Reeling and Writhing, of course, to begin with
```

**Preceding context:**

```text
‘I couldn’t aﬀord to learn it.’ said the Mock Turtle with a sigh. ‘I only took the regular course.’
```

**Supporting paragraph/context:**

```text
‘What was that?’ inquired Alice. ‘Reeling and Writhing, of course, to begin with,’ the Mock Turtle replied; ‘and then the diﬀerent branches of Arithmetic– Ambition, Distraction, Ugli- ﬁcation, and Derision.’
```

**Following context:**

```text
‘I never heard of “Ugliﬁcation,”’ Alice ventured to say. ‘What is it?’ The Gryphon lifted up both its paws in surprise. ‘What! Never heard of uglifying!’ it exclaimed. ‘You know what to beautify is, I suppose?’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The regular course began with Reeling, Writhing, and four punning arithmetic branches.

#### C2: The packaged later passage lists Mystery, Seaography, Drawling, Stretching, and Fainting in Coils.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 72, "chapter": "9", "pdf_block": 3}`

**Exact supporting span:**

```text
Mystery, ancient and modern, with Seaography
```

**Preceding context:**

```text
Alice did not feel encouraged to ask any more questions about it, so she turned to the Mock Turtle, and said ‘What else had you to learn?’
```

**Supporting paragraph/context:**

```text
‘Well, there was Mystery,’ the Mock Turtle replied, counting oﬀthe sub- jects on his ﬂappers, ‘–Mystery, ancient and modern, with Seaography: then Drawling–the Drawling-master was an old conger-eel, that used to come once a week: HE taught us Drawling, Stretching, and Fainting in Coils.’
```

**Following context:**

```text
‘What was THAT like?’ said Alice. ‘Well, I can’t show it you myself,’ the Mock Turtle said: ‘I’m too stiﬀ. And the Gryphon never learnt it.’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited passage explicitly lists Mystery, Seaography, Drawling, Stretching, and Fainting in Coils.

**Codex annotation notes:** Question/reference narrowed to what packaged E1/E2 explicitly support; no unsupported Laughing/Grief claim is made.

**Annotation confidence / review tier:** `high` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q027</strong> · multi_fact_single_context · answered · DEEP_REVIEW — historical, needs owner attention</summary>

**Question:** What final actions complete the first figure of the Lobster Quadrille?

**Proposed status:** `answered`

**Proposed reference answer:** After changing lobsters and retiring, the dancers throw the lobsters out to sea, swim after them, turn a somersault, change lobsters again, and return to land; that completes the first figure.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `fact_q027`

**Evidence event:** `event_fact_q027`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `historical_case`, `known_bad_case`, `phase4_reuse`

### Required claims and original context

#### C1: They change lobsters and retire, then throw the lobsters to sea, swim after them, and somersault.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 73, "chapter": "10", "pdf_block": 5}`

**Exact supporting span:**

```text
change lobsters, and retire in same order
```

**Preceding context:**

```text
‘No, indeed,’ said Alice. ‘What sort of a dance is it?’ ‘Why,’ said the Gryphon, ‘you ﬁrst form into a line along the sea-shore–’ ‘Two lines!’ cried the Mock Turtle. ‘Seals, turtles, salmon, and so on; then, when you’ve cleared all the jelly-ﬁsh out of the way–’
```

**Supporting paragraph/context:**

```text
‘THAT generally takes some time,’ interrupted the Gryphon. ‘–you advance twice–’ ‘Each with a lobster as a partner!’ cried the Gryphon. ‘Of course,’ the Mock Turtle said: ‘advance twice, set to partners–’ ‘–change lobsters, and retire in same order,’ continued the Gryphon. ‘Then, you know,’ the Mock Turtle went on, ‘you throw the–’ ‘The lobsters!’ shouted the Gryphon, with a bound into the air. ‘–as far out to sea as you can–’ ‘Swim after them!’ screamed the Gryphon. ‘Turn a somersault in the sea!’ cried the Mock Turtle, capering wildly about.
```

**Following context:**

```text
‘Change lobsters again!’ yelled the Gryphon at the top of its voice. ‘Back to land again, and that’s all the ﬁrst ﬁgure,’ said the Mock Turtle, suddenly dropping his voice; and the two creatures, who had been jumping about like mad things all this time, sat down again very sadly and quietly, and looked at Alice.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: They change lobsters and retire, then throw the lobsters to sea, swim after them, and somersault.

#### C2: They change lobsters again and return to land to finish the first figure.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 74, "chapter": "10", "pdf_block": 1}`

**Exact supporting span:**

```text
Back to land again, and that’s all the first figure
```

**Preceding context:**

```text
‘THAT generally takes some time,’ interrupted the Gryphon. ‘–you advance twice–’ ‘Each with a lobster as a partner!’ cried the Gryphon. ‘Of course,’ the Mock Turtle said: ‘advance twice, set to partners–’ ‘–change lobsters, and retire in same order,’ continued the Gryphon. ‘Then, you know,’ the Mock Turtle went on, ‘you throw the–’ ‘The lobsters!’ shouted the Gryphon, with a bound into the air. ‘–as far out to sea as you can–’ ‘Swim after them!’ screamed the Gryphon. ‘Turn a somersault in the sea!’ cried the Mock Turtle, capering wildly about.
```

**Supporting paragraph/context:**

```text
‘Change lobsters again!’ yelled the Gryphon at the top of its voice. ‘Back to land again, and that’s all the ﬁrst ﬁgure,’ said the Mock Turtle, suddenly dropping his voice; and the two creatures, who had been jumping about like mad things all this time, sat down again very sadly and quietly, and looked at Alice.
```

**Following context:**

```text
‘It must be a very pretty dance,’ said Alice timidly. ‘Would you like to see a little of it?’ said the Mock Turtle. ‘Very much indeed,’ said Alice. ‘Come, let’s try the ﬁrst ﬁgure!’ said the Mock Turtle to the Gryphon. ‘We can do without lobsters, you know. Which shall sing?’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: They change lobsters again and return to land to finish the first figure.

**Codex annotation notes:** The old answer omitted throw/swim/somersault/change-again steps; the repaired answer covers the complete ending sequence. Reclassified from multi-source: the answer components belong to one continuous local event/context.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q028</strong> · multi_source_multi_fact · answered · DEEP_REVIEW — historical, needs owner attention</summary>

**Question:** What was the Knave of Hearts accused of, and who was called as the first witness?

**Proposed status:** `answered`

**Proposed reference answer:** He was accused of stealing the Queen's tarts, and the Hatter was the first witness.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_q028`

**Evidence event:** `event_alice_tart_trial_opening`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** `av057`

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: The Knave was accused of stealing the tarts.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 82, "chapter": "11", "pdf_block": 7}`

**Exact supporting span:**

```text
The Knave of Hearts, he stole those tarts
```

**Preceding context:**

```text
‘Herald, read the accusation!’ said the King. On this the White Rabbit blew three blasts on the trumpet, and then unrolled the parchment scroll, and read as follows:–
```

**Supporting paragraph/context:**

```text
‘The Queen of Hearts, she made some tarts, All on a summer day: The Knave of Hearts, he stole those tarts, And took them quite away!’
```

**Following context:**

```text
‘Consider your verdict,’ the King said to the jury. ‘Not yet, not yet!’ the Rabbit hastily interrupted. ‘There’s a great deal to come before that!’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The Knave was accused of stealing the tarts.

#### C2: The Hatter was first witness.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 82, "chapter": "11", "pdf_block": 10}`

**Exact supporting span:**

```text
The first witness was the Hatter
```

**Preceding context:**

```text
‘Call the ﬁrst witness,’ said the King; and the White Rabbit blew three blasts on the trumpet, and called out, ‘First witness!’
```

**Supporting paragraph/context:**

```text
The ﬁrst witness was the Hatter. He came in with a teacup in one hand and a piece of bread-and-butter in the other. ‘I beg pardon, your Majesty,’ he began, ‘for bringing these in: but I hadn’t quite ﬁnished my tea when I was sent for.’
```

**Following context:**

```text
‘You ought to have ﬁnished,’ said the King. ‘When did you begin?’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The Hatter was first witness.

**Codex annotation notes:** Reused historical Phase-4 case; proposed V2 classification does not change its old result. Linked to av057: distinct target claim, shared source event; fact-family IDs are not independent-event counts.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q029</strong> · multi_source_multi_fact · answered · DEEP_REVIEW — historical, needs owner attention</summary>

**Question:** Who was the next witness after the Hatter, and what did she say the tarts were mostly made of?

**Proposed status:** `answered`

**Proposed reference answer:** The Duchess's cook; she said the tarts were mostly made of pepper.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `alice_cook_witness`

**Evidence event:** `event_alice_cook_witness`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `meta_cook_witness` / `none`

**Related cases:** `av040`, `av060`

**Tags:** `historical_case`, `phase4_reuse`

### Required claims and original context

#### C1: The next witness was the Duchess’s cook.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 85, "chapter": "11", "pdf_block": 5}`

**Exact supporting span:**

```text
next witness was the Duchess’s cook
```

**Preceding context:**

```text
‘–and just take his head oﬀoutside,’ the Queen added to one of the oﬃcers: but the Hatter was out of sight before the oﬃcer could get to the door.
```

**Supporting paragraph/context:**

```text
‘Call the next witness!’ said the King. The next witness was the Duchess’s cook. She carried the pepper-box in her hand, and Alice guessed who it was, even before she got into the court, by the way the people near the door began sneezing all at once.
```

**Following context:**

```text
‘Give your evidence,’ said the King. ‘Shan’t,’ said the cook. The King looked anxiously at the White Rabbit, who said in a low voice, ‘Your Majesty must cross-examine THIS witness.’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The next witness was the Duchess’s cook.

#### C2: She said the tarts were mostly pepper.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 85, "chapter": "11", "pdf_block": 8}`

**Exact supporting span:**

```text
Pepper, mostly
```

**Preceding context:**

```text
‘Well, if I must, I must,’ the King said, with a melancholy air, and, after folding his arms and frowning at the cook till his eyes were nearly out of sight, he said in a deep voice, ‘What are tarts made of?’
```

**Supporting paragraph/context:**

```text
‘Pepper, mostly,’ said the cook. ‘Treacle,’ said a sleepy voice behind her. ‘Collar that Dormouse,’ the Queen shrieked out. ‘Behead that Dormouse! Turn that Dormouse out of court! Suppress him! Pinch him! Oﬀwith his whiskers!’
```

**Following context:**

```text
For some minutes the whole court was in confusion, getting the Dormouse turned out, and, by the time they had settled down again, the cook had disappeared.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: She said the tarts were mostly pepper.

**Codex annotation notes:** Reused historical Phase-4 case; proposed V2 classification does not change its old result.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>q030</strong> · direct_factual_single_source · answered · DEEP_REVIEW — historical, needs owner attention</summary>

**Question:** Under Rule Forty-two, which people had to leave the court?

**Proposed status:** `answered`

**Proposed reference answer:** All persons more than a mile high.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_q030`

**Evidence event:** `event_fact_q030`

**Development exposure:** `development_material`

**Exposure review:** This case and its reviewer-facing context are development-visible.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `character_statement`, `historical_case`, `known_bad_case`, `phase4_reuse`, `rule_content`

### Required claims and original context

#### C1: All persons more than a mile high.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 88, "chapter": "12", "pdf_block": 4}`

**Exact supporting span:**

```text
more than a mile high
```

**Preceding context:**

```text
Some of the jury wrote it down ‘important,’ and some ‘unimportant.’ Alice could see this, as she was near enough to look over their slates; ‘but it doesn’t matter a bit,’ she thought to herself.
```

**Supporting paragraph/context:**

```text
At this moment the King, who had been for some time busily writing in his note-book, cackled out ‘Silence!’ and read out from his book, ‘Rule Forty-two. ALL PERSONS MORE THAN A MILE HIGH TO LEAVE THE COURT.’
```

**Following context:**

```text
Everybody looked at Alice. ‘I’M not a mile high,’ said Alice. ‘You are,’ said the King. ‘Nearly two miles high,’ added the Queen. ‘Well, I shan’t go, at any rate,’ said Alice: ‘besides, that’s not a regular rule: you invented it just now.’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: All persons more than a mile high.

**Codex annotation notes:** Direct question about the content of the King’s stated Rule Forty-two. It is not a contrastive item; the evidence establishes what the King read out, not the legitimacy of the rule.

**Annotation confidence / review tier:** `high` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>


# alice_final_test

<details>
<summary><strong>at068</strong> · direct_factual_single_source · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** In the Mouse’s long tale, who proposes taking the Mouse to law?

**Proposed status:** `answered`

**Proposed reference answer:** Fury does.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_at068`

**Evidence event:** `event_fact_at068`

**Development exposure:** `no_known_development_exposure`

**Exposure review:** Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `speaker_identity`

### Required claims and original context

#### C1: Fury proposes taking the Mouse to law.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 28, "chapter": "3", "pdf_block": 1}`

**Exact supporting span:**

```text
Let us both go to law: I will prosecute you
```

**Preceding context:**

```text
‘It IS a long tail, certainly,’ said Alice, looking down with wonder at the Mouse’s tail; ‘but why do you call it sad?’ And she kept on puzzling about it while the Mouse was speaking, so that her idea of the tale was something like this:–
```

**Supporting paragraph/context:**

```text
‘Fury said to a mouse, That he met in the house, “Let us both go to law: I will prosecute you. Come, I’ll take no denial; We must have a trial: For really this morning I’ve nothing to do.” Said the mouse to the cur, “Such a trial, dear sir, With no jury or judge, would be wasting our breath.” “I’ll be judge, I’ll be jury,” Said cunning old Fury: “I’ll try the whole cause, and condemn you to death.”’
```

**Following context:**

```text
The Mouse then rebukes Alice for not attending to the tale.
```

**Context incomplete:** `false`

**Why it supports this claim:** The restored poem text explicitly has Fury propose going to law and prosecuting the Mouse.

**Codex annotation notes:** Retained TEST case. Evidence restored far enough to contain the proposition being scored.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>at073</strong> · contrastive_distractor · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** Did the Hatter say the hat he wore belonged to him?

**Proposed status:** `answered`

**Proposed reference answer:** No. He said it was not his and that he kept hats to sell.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_at073`

**Evidence event:** `event_fact_at073`

**Development exposure:** `no_known_development_exposure`

**Exposure review:** Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `false_premise`, `negation`

### Required claims and original context

#### C1: The Hatter denied owning it.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 83, "chapter": "11", "pdf_block": 3}`

**Exact supporting span:**

```text
It isn’t mine
```

**Preceding context:**

```text
‘Fifteenth,’ said the March Hare. ‘Sixteenth,’ added the Dormouse. ‘Write that down,’ the King said to the jury, and the jury eagerly wrote down all three dates on their slates, and then added them up, and reduced the answer to shillings and pence.
```

**Supporting paragraph/context:**

```text
‘Take oﬀyour hat,’ the King said to the Hatter. ‘It isn’t mine,’ said the Hatter. ‘Stolen!’ the King exclaimed, turning to the jury, who instantly made a memorandum of the fact.
```

**Following context:**

```text
‘I keep them to sell,’ the Hatter added as an explanation; ‘I’ve none of my own. I’m a hatter.’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The Hatter denied owning it.

#### C2: He said he kept hats to sell.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 83, "chapter": "11", "pdf_block": 4}`

**Exact supporting span:**

```text
I keep them to sell
```

**Preceding context:**

```text
‘Take oﬀyour hat,’ the King said to the Hatter. ‘It isn’t mine,’ said the Hatter. ‘Stolen!’ the King exclaimed, turning to the jury, who instantly made a memorandum of the fact.
```

**Supporting paragraph/context:**

```text
‘I keep them to sell,’ the Hatter added as an explanation; ‘I’ve none of my own. I’m a hatter.’
```

**Following context:**

```text
Here the Queen put on her spectacles, and began staring at the Hatter, who turned pale and ﬁdgeted.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: He said he kept hats to sell.

**Codex annotation notes:** Retained TEST contrast: the Hatter says the hat is merchandise, not his own property.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>at075</strong> · unanswerable_false_premise · insufficient_evidence · DEEP_REVIEW — needs owner attention</summary>

**Question:** How old was the White Rabbit?

**Proposed status:** `insufficient_evidence`

**Proposed reference answer:** No supporting evidence was found in the reviewed text of the exact evaluation book after targeted whole-document verification.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `fact_at075`

**Evidence event:** `event_fact_at075`

**Development exposure:** `no_known_development_exposure`

**Exposure review:** Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `whole_document_negative_check`

### Whole-document negative verification

**Scope:** complete text content of Alice PDF SHA-256 49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e

**Entity aliases:** `White Rabbit`, `Rabbit`, `herald`

**Negative terms:** `White Rabbit age`, `Rabbit years old`, `old Rabbit`

**Relation variants:** `was aged`, `how old`, `years of age`, `born`

**Morphological variants:** `age`, `aged`, `old`, `older`, `born`

**Semantic variants:** `the Rabbit's numerical age`

**Plausible counterexamples:** `Lory says it is older`, `Father William poem`, `Alice's age-related comparisons`

**Counterexample disposition:** Age language concerns other characters and never supplies the White Rabbit's age.

#### Search: `Rabbit-age relation`

- Pattern: `\b(?:White Rabbit|Rabbit).{0,60}(?:age|years? old)\b`
- All matches reviewed: `true`
- Assessment: No age assertion.

Source matches (0):
- none

#### Search: `age terms`

- Pattern: `\b(?:age|years? old)\b`
- All matches reviewed: `true`
- Assessment: Hits concern other characters or general narration.

Source matches (4):
- page 20: e!’ And she began thinking over all the children she knew that were of the same age as herself, to see if she could have been changed for any of them. ‘I’m sure I’m not Ada,’ she said, ‘for her hair goe
- page 25: without knowing how old it was, and, as the Lory positively refused to tell its age, there was no more to be said. At last the Mouse, who seemed to be a person of authority among them, called out, ‘Sit d
- page 38: e very white; And yet you incessantly stand on your head– Do you think, at your age, it is right?’ ‘In my youth,’ Father William replied to his son, ‘I feared it might injure the brain; But, now that I’
- page 81: roud of it: for she thought, and rightly too, that very few little girls of her age knew the meaning of it at all. However, ‘jury-men’ would have done just as well. The twelve jurors were all writing ver

**Bounded conclusion:** No supporting evidence was found in the reviewed book text after targeted whole-document verification.. This is not mathematical proof of absence.

**Codex annotation notes:** Retained independent TEST negative about the White Rabbit’s age. Negative verification is bounded whole-document review, not mathematical proof of absence; absolute_absence_claimed remains false.

**Annotation confidence / review tier:** `needs_owner_review` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>at076</strong> · unanswerable_false_premise · insufficient_evidence · DEEP_REVIEW — needs owner attention</summary>

**Question:** What was the King of Hearts’ first name?

**Proposed status:** `insufficient_evidence`

**Proposed reference answer:** No supporting evidence was found in the reviewed text of the exact evaluation book after targeted whole-document verification.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `fact_at076`

**Evidence event:** `event_fact_at076`

**Development exposure:** `no_known_development_exposure`

**Exposure review:** Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `whole_document_negative_check`

### Whole-document negative verification

**Scope:** complete text content of Alice PDF SHA-256 49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e

**Entity aliases:** `King of Hearts`, `King`, `his Majesty`, `judge`

**Negative terms:** `King first name`, `King named`, `King called`

**Relation variants:** `his name is`, `personal name`, `called the King`

**Morphological variants:** `name`, `named`, `called`

**Semantic variants:** `given name of the King of Hearts`

**Plausible counterexamples:** `William the Conqueror`, `King as title/judge`

**Counterexample disposition:** William belongs to the Mouse's history lesson; ‘King’ is a title and no personal name is provided.

#### Search: `first/name relation`

- Pattern: `\b(?:King of Hearts|King).{0,60}(?:first name|named|called)\b`
- All matches reviewed: `true`
- Assessment: No naming assertion.

Source matches (1):
- page 63: in some book, but I don’t remember where.’ ‘Well, it must be removed,’ said the King very decidedly, and he called the Queen, who was passing at the moment, ‘My dear! I wish you would have this cat removed!’ The Queen had only one way

#### Search: `King of Hearts`

- Pattern: `\bKing(?: of Hearts)?\b`
- All matches reviewed: `true`
- Assessment: Entity mentions use only the title.

Source matches (63):
- page 60: d went by without noticing her. Then followed the Knave of Hearts, carrying the King’s crown on a crimson velvet cushion; and, last of all this grand procession, came THE KING AND QUEEN OF HEARTS. Alice w
- page 60: n on a crimson velvet cushion; and, last of all this grand procession, came THE KING AND QUEEN OF HEARTS. Alice was rather doubtful whether she ought not to lie down on her face like the three gardeners,
- page 61: silent. The King laid his hand upon her arm, and timidly said ‘Consider, my dear: she is only a child!’ The Queen turned angrily away fr
- page 61: oud voice, and the three gardeners instantly jumped up, and began bowing to the King, the Queen, the royal children, and everybody else. ‘Leave offthat!’ screamed the Queen. ‘You make me giddy.’ And then,
- page 63: g the game.’ The Queen smiled and passed on. ‘Who ARE you talking to?’ said the King, going up to Alice, and looking at the Cat’s head with great curiosity. ‘It’s a friend of mine–a Cheshire Cat,’ said Al
- page 63: ice: ‘allow me to introduce it.’ ‘I don’t like the look of it at all,’ said the King: ‘however, it may kiss my hand if it likes.’ ‘I’d rather not,’ the Cat remarked. ‘Don’t be impertinent,’ said the King,
- page 63: it likes.’ ‘I’d rather not,’ the Cat remarked. ‘Don’t be impertinent,’ said the King, ‘and don’t look at me like that!’ He got behind Alice as he spoke. ‘A cat may look at a king,’ said Alice. ‘I’ve read
- page 63: ’t look at me like that!’ He got behind Alice as he spoke. ‘A cat may look at a king,’ said Alice. ‘I’ve read that in some book, but I don’t remember where.’ ‘Well, it must be removed,’ said the King very
- page 63: in some book, but I don’t remember where.’ ‘Well, it must be removed,’ said the King very decidedly, and he called the Queen, who was passing at the moment, ‘My dear! I wish you would have this cat remove
- page 63: said, without even looking round. ‘I’ll fetch the executioner myself,’ said the King eagerly, and he hurried off.
- page 64: d collected round it: there was a dispute going on between the executioner, the King, and the Queen, who were all talking at once, while all the rest were quite silent, and looked very uncomfortable. The
- page 64: o do such a thing before, and he wasn’t going to begin at HIS time of life. The King’s argument was, that anything that had a head could be beheaded, and that you weren’t to talk nonsense. The Queen’s arg
- page 65: King and the executioner ran wildly up and down looking for it, while the rest of the party went back to the game.
- page 69: f half an hour or so there were no arches left, and all the players, except the King, the Queen, and Alice, were in custody and under sentence of execution. Then the Queen left off, quite out of breath, a
- page 69: and he shall tell you his history,’ As they walked offtogether, Alice heard the King say in a low voice, to the company generally, ‘You are all pardoned.’ ‘Come, THAT’S a good
- page 81: Chapter 11 Who Stole the Tarts? The King and Queen of Hearts were seated on their throne when they arrived, with a great crowd assembled about them–all sorts of
- page 81: before them, in chains, with a soldier on each side to guard him; and near the King was the White Rabbit, with a trumpet in one hand, and a scroll of parchment in the other. In the very middle of the cou
- page 81: she said to herself, ‘because of his great wig.’ The judge, by the way, was the King; and as he wore his crown over the wig, (look at the frontispiece if you want to see how he did it,) he did not look at
- page 82: topped hastily, for the White Rabbit cried out, ‘Silence in the court!’ and the King put on his spectacles and looked anxiously round, to make out who was talking. Alice could see, as well as if she were
- page 82: e use, as it left no mark on the slate. ‘Herald, read the accusation!’ said the King. On this the White Rabbit blew three blasts on the trumpet, and then unrolled the parchment scroll, and read as follows
- page 82: he stole those tarts, And took them quite away!’ ‘Consider your verdict,’ the King said to the jury. ‘Not yet, not yet!’ the Rabbit hastily interrupted. ‘There’s a great deal to come before that!’ ‘Call
- page 82: ‘There’s a great deal to come before that!’ ‘Call the first witness,’ said the King; and the White Rabbit blew three blasts on the trumpet, and called out, ‘First witness!’ The first witness was the Hatt
- page 82: te finished my tea when I was sent for.’ ‘You ought to have finished,’ said the King. ‘When did you begin?’
- page 83: ,’ said the March Hare. ‘Sixteenth,’ added the Dormouse. ‘Write that down,’ the King said to the jury, and the jury eagerly wrote down all three dates on their slates, and then added them up, and reduced
- page 83: them up, and reduced the answer to shillings and pence. ‘Take offyour hat,’ the King said to the Hatter. ‘It isn’t mine,’ said the Hatter. ‘Stolen!’ the King exclaimed, turning to the jury, who instantly
- page 83: ,’ the King said to the Hatter. ‘It isn’t mine,’ said the Hatter. ‘Stolen!’ the King exclaimed, turning to the jury, who instantly made a memorandum of the fact. ‘I keep them to sell,’ the Hatter added as
- page 83: ing at the Hatter, who turned pale and fidgeted. ‘Give your evidence,’ said the King; ‘and don’t be nervous, or I’ll have you executed on the spot.’ This did not seem to encourage the witness at all: he k
- page 84: Hatter trembled so, that he shook both his shoes off. ‘Give your evidence,’ the King repeated angrily, ‘or I’ll have you executed, whether you’re nervous or not.’ ‘I’m a poor man, your Majesty,’ the Hatte
- page 84: ng so thin–and the twinkling of the tea–’ ‘The twinkling of the what?’ said the King. ‘It began with the tea,’ the Hatter replied. ‘Of course twinkling begins with a T!’ said the King sharply. ‘Do you tak
- page 84: h the tea,’ the Hatter replied. ‘Of course twinkling begins with a T!’ said the King sharply. ‘Do you take me for a dunce? Go on!’ ‘I’m a poor man,’ the Hatter went on, ‘and most things twinkled after tha
- page 84: d!’ said the Hatter. ‘I deny it!’ said the March Hare. ‘He denies it,’ said the King: ‘leave out that part.’ ‘Well, at any rate, the Dormouse said–’ the Hatter went on, looking anxiously round to see if h
- page 84: ed. ‘That I can’t remember,’ said the Hatter. ‘You MUST remember,’ remarked the King, ‘or I’ll have you executed.’ The miserable Hatter dropped his teacup and bread-and-butter, and went down on one knee.
- page 84: I’m a poor man, your Majesty,’ he began. ‘You’re a very poor speaker,’ said the King. Here one of the guinea-pigs cheered, and was immediately suppressed by the officers of the court. (As that is rather a
- page 84: till now.’ ‘If that’s all you know about it, you may stand down,’ continued the King.
- page 85: r,’ said the Hatter: ‘I’m on the floor, as it is.’ ‘Then you may SIT down,’ the King replied. Here the other guinea-pig cheered, and was suppressed. ‘Come, that finished the guinea-pigs!’ thought Alice. ‘
- page 85: look at the Queen, who was reading the list of singers. ‘You may go,’ said the King, and the Hatter hurriedly left the court, without even waiting to put his shoes on. ‘–and just take his head offoutside
- page 85: ght before the officer could get to the door. ‘Call the next witness!’ said the King. The next witness was the Duchess’s cook. She carried the pepper-box in her hand, and Alice guessed who it was, even be
- page 85: people near the door began sneezing all at once. ‘Give your evidence,’ said the King. ‘Shan’t,’ said the cook. The King looked anxiously at the White Rabbit, who said in a low voice, ‘Your Majesty must cr
- page 85: all at once. ‘Give your evidence,’ said the King. ‘Shan’t,’ said the cook. The King looked anxiously at the White Rabbit, who said in a low voice, ‘Your Majesty must cross-examine THIS witness.’ ‘Well, i
- page 85: ‘Your Majesty must cross-examine THIS witness.’ ‘Well, if I must, I must,’ the King said, with a melancholy air, and, after folding his arms and frowning at the cook till his eyes were nearly out of sigh
- page 85: e they had settled down again, the cook had disappeared. ‘Never mind!’ said the King, with an air of great relief. ‘Call the next witness.’ And he added in an undertone to the Queen, ‘Really, my dear, YOU
- page 87: back into the jury-box, or they would die. ‘The trial cannot proceed,’ said the King in a very grave voice, ‘until all the jurymen are back in their proper places– ALL,’ he repeated with great emphasis, l
- page 87: zing up into the roof of the court. ‘What do you know about this business?’ the King said to Alice. ‘Nothing,’ said Alice.
- page 88: 88 CHAPTER 12. ALICE’S EVIDENCE ‘Nothing WHATEVER?’ persisted the King. ‘Nothing whatever,’ said Alice. ‘That’s very important,’ the King said, turning to the jury. They were just beginning
- page 88: ersisted the King. ‘Nothing whatever,’ said Alice. ‘That’s very important,’ the King said, turning to the jury. They were just beginning to write this down on their slates, when the White Rabbit interrupt
- page 88: ing and making faces at him as he spoke. ‘UNimportant, of course, I meant,’ the King hastily said, and went on to himself in an undertone, ‘important–unimportant– unimportant–important–’ as if he were try
- page 88: ates; ‘but it doesn’t matter a bit,’ she thought to herself. At this moment the King, who had been for some time busily writing in his note-book, cackled out ‘Silence!’ and read out from his book, ‘Rule F
- page 88: erybody looked at Alice. ‘I’M not a mile high,’ said Alice. ‘You are,’ said the King. ‘Nearly two miles high,’ added the Queen. ‘Well, I shan’t go, at any rate,’ said Alice: ‘besides, that’s not a regular
- page 88: r rule: you invented it just now.’ ‘It’s the oldest rule in the book,’ said the King. ‘Then it ought to be Number One,’ said Alice. The King turned pale, and shut his note-book hastily. ‘Consider your ver
- page 88: in the book,’ said the King. ‘Then it ought to be Number One,’ said Alice. The King turned pale, and shut his note-book hastily. ‘Consider your verdict,’ he said to the jury, in a low, trembling voice. ‘
- page 88: er, written by the prisoner to–to somebody.’ ‘It must have been that,’ said the King, ‘unless it was written to nobody, which isn’t usual, you know.’ ‘Who is it directed to?’ said one of the jurymen. ‘It
- page 89: ury all looked puzzled.) ‘He must have imitated somebody else’s hand,’ said the King. (The jury all brightened up again.) ‘Please your Majesty,’ said the Knave, ‘I didn’t write it, and they can’t prove I
- page 89: ve I did: there’s no name signed at the end.’ ‘If you didn’t sign it,’ said the King, ‘that only makes the matter worse. You MUST have meant some mischief, or else you’d have signed your name like an hone
- page 89: s a general clapping of hands at this: it was the first really clever thing the King had said that day. ‘That PROVES his guilt,’ said the Queen. ‘It proves nothing of the sort!’ said Alice. ‘Why, you don’
- page 89: aid Alice. ‘Why, you don’t even know what they’re about!’ ‘Read them,’ said the King. The White Rabbit put on his spectacles. ‘Where shall I begin, please your Majesty?’ he asked. ‘Begin at the beginning,
- page 89: re shall I begin, please your Majesty?’ he asked. ‘Begin at the beginning,’ the King said gravely, ‘and go on till you come to the end: then stop.’ These were the verses the White Rabbit read:– ‘They tol
- page 90: d me.’ ‘That’s the most important piece of evidence we’ve heard yet,’ said the King, rubbing his hands; ‘so now let the jury–’ ‘If any one of them can explain it,’ said Alice, (she had grown so large in
- page 90: of them attempted to explain the paper. ‘If there’s no meaning in it,’ said the King, ‘that saves a world of trouble, you know, as we needn’t try to find any. And yet I don’t know,’ he went on, spreading
- page 90: ainly did NOT, being made entirely of cardboard.) ‘All right, so far,’ said the King, and he went on muttering over the verses to himself: ‘“WE KNOW IT TO BE TRUE–” that’s the jury, of course– “I GAVE HER
- page 90: HEY ALL RETURNED FROM HIM TO YOU,”’ said Alice. ‘Why, there they are!’ said the King triumphantly, pointing to the tarts on the table. ‘Nothing can be clearer than THAT. Then again– “BEFORE SHE HAD THIS F
- page 91: ‘Then the words don’t FIT you,’ said the King, looking round the court with a smile. There was a dead silence. ‘It’s a pun!’ the King added in an offended tone, and
- page 91: oking round the court with a smile. There was a dead silence. ‘It’s a pun!’ the King added in an offended tone, and everybody laughed, ‘Let the jury consider their verdict,’ the King said, for about the t
- page 91: ffended tone, and everybody laughed, ‘Let the jury consider their verdict,’ the King said, for about the twentieth time that day. ‘No, no!’ said the Queen. ‘Sentence first–verdict afterwards.’ ‘Stuffand n

**Bounded conclusion:** No supporting evidence was found in the reviewed book text after targeted whole-document verification.. This is not mathematical proof of absence.

**Codex annotation notes:** Retained independent TEST negative about the King’s personal name.

**Annotation confidence / review tier:** `needs_owner_review` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>at102</strong> · local_context_reasoning · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** Why did the Mouse leave after Alice said it had reached the fifth bend?

**Proposed status:** `answered`

**Proposed reference answer:** The Mouse cried ‘I had NOT!’; Alice interpreted the sound as ‘A knot!’, offered to undo it, and the Mouse called her talk nonsense and insulting before walking away.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `fact_at102`

**Evidence event:** `event_fact_at102`

**Development exposure:** `no_known_development_exposure`

**Exposure review:** Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** _none_

### Required claims and original context

#### C1: The Mouse said ‘I had NOT!’ and Alice interpreted it as ‘A knot!’, offering to undo it.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 29, "chapter": "3", "pdf_block": 6}`

**Exact supporting span:**

```text
‘I had NOT!’ cried the Mouse
```

**Preceding context:**

```text
‘I beg your pardon,’ said Alice very humbly: ‘you had got to the ﬁfth bend, I think?’
```

**Supporting paragraph/context:**

```text
‘I had NOT!’ cried the Mouse, sharply and very angrily. ‘A knot!’ said Alice, always ready to make herself useful, and looking anxiously about her. ‘Oh, do let me help to undo it!’
```

**Following context:**

```text
‘I shall do nothing of the sort,’ said the Mouse, getting up and walking away. ‘You insult me by talking such nonsense!’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Alice mistook ‘not’ for ‘knot’ and offered to undo it.

#### C2: The Mouse called Alice’s talk nonsense and insulting and walked away.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 29, "chapter": "3", "pdf_block": 7}`

**Exact supporting span:**

```text
You insult me by talking such nonsense
```

**Preceding context:**

```text
‘I had NOT!’ cried the Mouse, sharply and very angrily. ‘A knot!’ said Alice, always ready to make herself useful, and looking anxiously about her. ‘Oh, do let me help to undo it!’
```

**Supporting paragraph/context:**

```text
‘I shall do nothing of the sort,’ said the Mouse, getting up and walking away. ‘You insult me by talking such nonsense!’
```

**Following context:**

```text
‘I didn’t mean it!’ pleaded poor Alice. ‘But you’re so easily oﬀended, you know!’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The Mouse treated the misunderstanding as an insult and left.

**Codex annotation notes:** Speaker attribution fixed: the Mouse says ‘NOT’; Alice supplies ‘A knot!’.

**Annotation confidence / review tier:** `high` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>at104</strong> · voice_like_noisy_text · answered · FAST_CONFIRM — needs owner attention</summary>

**Question:** at the rabbit house when alice drank that unlabeled bottle did she get bigger or smaller

**Proposed status:** `answered`

**Proposed reference answer:** She grew bigger, until her head pressed against the ceiling and she could not get through the door.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_at104`

**Evidence event:** `event_fact_at104`

**Development exposure:** `no_known_development_exposure`

**Exposure review:** Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `punctuation_loss`, `conversational_wording`

### Required claims and original context

#### C1: The unlabeled bottle made Alice grow larger inside the Rabbit’s house.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 32, "chapter": "4", "pdf_block": 3}`

**Exact supporting span:**

```text
before she had drunk half the bottle, she found her head pressing against the ceiling
```

**Preceding context:**

```text
By this time she had found her way into a tidy little room with a table in the window, and on it (as she had hoped) a fan and two or three pairs of tiny white kid gloves: she took up the fan and a pair of the gloves, and was just going to leave the room, when her eye fell upon a little bottle that stood near the looking- glass. There was no label this time with the words ‘DRINK ME,’ but nevertheless she uncorked it and put it to her lips. ‘I know SOMETHING interesting is sure to happen,’ she said to herself, ‘whenever I eat or drink anything; so I’ll just see what this bottle does. I do hope it’ll make me grow large again, for really I’m quite tired of being such a tiny little thing!’
```

**Supporting paragraph/context:**

```text
It did so indeed, and much sooner than she had expected: before she had drunk half the bottle, she found her head pressing against the ceiling, and had to stoop to save her neck from being broken. She hastily put down the bottle, saying to herself ‘That’s quite enough–I hope I shan’t grow any more–As it is, I can’t get out at the door–I do wish I hadn’t drunk quite so much!’
```

**Following context:**

```text
Alas! it was too late to wish that! She went on growing, and growing, and very soon had to kneel down on the ﬂoor: in another minute there was not even room for this, and she tried the eﬀect of lying down with one elbow against the door, and the other arm curled round her head. Still she went on growing, and, as a last resource, she put one arm out of the window, and one foot up the chimney, and said to herself ‘Now I can do no more, whatever happens. What WILL become of me?’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The unlabeled bottle made Alice grow larger inside the Rabbit’s house.

**Codex annotation notes:** Realistic punctuation-free spoken-text form; new fact family.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>at106</strong> · multi_fact_single_context · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** How did Alice distract the enormous puppy and get away?

**Proposed status:** `answered`

**Proposed reference answer:** She held out a stick and dodged around a thistle while the puppy charged; when it tired and sat panting, she ran away.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `fact_at106`

**Evidence event:** `event_fact_at106`

**Development exposure:** `no_known_development_exposure`

**Exposure review:** Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** _none_

### Required claims and original context

#### C1: Alice distracted the puppy with a stick and the thistle.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 35, "chapter": "4", "pdf_block": 9}`

**Exact supporting span:**

```text
she picked up a little bit of stick, and held it out to the puppy
```

**Preceding context:**

```text
An enormous puppy was looking down at her with large round eyes, and feebly stretching out one paw, trying to touch her. ‘Poor little thing!’ said Alice, in a coaxing tone, and she tried hard to whistle to it; but she was terribly frightened all the time at the thought that it might be hungry, in which case it would be very likely to eat her up in spite of all her coaxing.
```

**Supporting paragraph/context:**

```text
Hardly knowing what she did, she picked up a little bit of stick, and held it out to the puppy; whereupon the puppy jumped into the air oﬀall its feet at once, with a yelp of delight, and rushed at the stick, and made believe to worry it; then Alice dodged behind a great thistle, to keep herself from being
```

**Following context:**

```text
run over; and the moment she appeared on the other side, the puppy made another rush at the stick, and tumbled head over heels in its hurry to get hold of it; then Alice, thinking it was very like having a game of play with a cart-horse, and expecting every moment to be trampled under its feet, ran round the thistle again; then the puppy began a series of short charges at the stick, running a very little way forwards each time and a long way back, and barking hoarsely all the while, till at last it sat down a good way oﬀ, panting, with its tongue hanging out of its mouth, and its great eyes half shut.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Alice distracted the puppy with a stick and the thistle.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 36, "chapter": "4", "pdf_block": 1}`

**Exact supporting span:**

```text
ran round the thistle again
```

**Preceding context:**

```text
Hardly knowing what she did, she picked up a little bit of stick, and held it out to the puppy; whereupon the puppy jumped into the air oﬀall its feet at once, with a yelp of delight, and rushed at the stick, and made believe to worry it; then Alice dodged behind a great thistle, to keep herself from being
```

**Supporting paragraph/context:**

```text
run over; and the moment she appeared on the other side, the puppy made another rush at the stick, and tumbled head over heels in its hurry to get hold of it; then Alice, thinking it was very like having a game of play with a cart-horse, and expecting every moment to be trampled under its feet, ran round the thistle again; then the puppy began a series of short charges at the stick, running a very little way forwards each time and a long way back, and barking hoarsely all the while, till at last it sat down a good way oﬀ, panting, with its tongue hanging out of its mouth, and its great eyes half shut.
```

**Following context:**

```text
This seemed to Alice a good opportunity for making her escape; so she set oﬀat once, and ran till she was quite tired and out of breath, and till the puppy’s bark sounded quite faint in the distance.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Alice distracted the puppy with a stick and the thistle.; She escaped when the puppy became tired and stopped at a distance.

#### C2: She escaped when the puppy became tired and stopped at a distance.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 36, "chapter": "4", "pdf_block": 1}`

**Exact supporting span:**

```text
ran round the thistle again
```

**Preceding context:**

```text
Hardly knowing what she did, she picked up a little bit of stick, and held it out to the puppy; whereupon the puppy jumped into the air oﬀall its feet at once, with a yelp of delight, and rushed at the stick, and made believe to worry it; then Alice dodged behind a great thistle, to keep herself from being
```

**Supporting paragraph/context:**

```text
run over; and the moment she appeared on the other side, the puppy made another rush at the stick, and tumbled head over heels in its hurry to get hold of it; then Alice, thinking it was very like having a game of play with a cart-horse, and expecting every moment to be trampled under its feet, ran round the thistle again; then the puppy began a series of short charges at the stick, running a very little way forwards each time and a long way back, and barking hoarsely all the while, till at last it sat down a good way oﬀ, panting, with its tongue hanging out of its mouth, and its great eyes half shut.
```

**Following context:**

```text
This seemed to Alice a good opportunity for making her escape; so she set oﬀat once, and ran till she was quite tired and out of breath, and till the puppy’s bark sounded quite faint in the distance.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Alice distracted the puppy with a stick and the thistle.; She escaped when the puppy became tired and stopped at a distance.

**Evidence E3 location:** `{"book": "alice_in_wonderland", "page": 36, "chapter": "4", "pdf_block": 2}`

**Exact supporting span:**

```text
This seemed to Alice a good opportunity for making her escape
```

**Preceding context:**

```text
run over; and the moment she appeared on the other side, the puppy made another rush at the stick, and tumbled head over heels in its hurry to get hold of it; then Alice, thinking it was very like having a game of play with a cart-horse, and expecting every moment to be trampled under its feet, ran round the thistle again; then the puppy began a series of short charges at the stick, running a very little way forwards each time and a long way back, and barking hoarsely all the while, till at last it sat down a good way oﬀ, panting, with its tongue hanging out of its mouth, and its great eyes half shut.
```

**Supporting paragraph/context:**

```text
This seemed to Alice a good opportunity for making her escape; so she set oﬀat once, and ran till she was quite tired and out of breath, and till the puppy’s bark sounded quite faint in the distance.
```

**Following context:**

```text
‘And yet what a dear little puppy it was!’ said Alice, as she leant against a buttercup to rest herself, and fanned herself with one of the leaves: ‘I should have liked teaching it tricks very much, if–if I’d only been the right size to do it! Oh dear! I’d nearly forgotten that I’ve got to grow up again! Let me see–how IS it to be managed? I suppose I ought to eat or drink something or other; but the great question is, what?’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: She escaped when the puppy became tired and stopped at a distance.

**Codex annotation notes:** Cross-page action sequence with distinct setup and outcome evidence. Reclassified from multi-source: the answer components belong to one continuous local event/context.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>at109</strong> · direct_factual_single_source · answered · FAST_CONFIRM — needs owner attention</summary>

**Question:** In what order did the Cheshire Cat disappear when Alice asked it to vanish more slowly?

**Proposed status:** `answered`

**Proposed reference answer:** It disappeared from the end of its tail first, with the grin remaining last.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_at109`

**Evidence event:** `event_fact_at109`

**Development exposure:** `no_known_development_exposure`

**Exposure review:** Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** _none_

### Required claims and original context

#### C1: The tail disappeared first and the grin remained until last.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 49, "chapter": "6", "pdf_block": 3}`

**Exact supporting span:**

```text
beginning with the end of the tail, and ending with the grin
```

**Preceding context:**

```text
‘Did you say pig, or ﬁg?’ said the Cat. ‘I said pig,’ replied Alice; ‘and I wish you wouldn’t keep appearing and vanishing so suddenly: you make one quite giddy.’
```

**Supporting paragraph/context:**

```text
‘All right,’ said the Cat; and this time it vanished quite slowly, beginning with the end of the tail, and ending with the grin, which remained some time after the rest of it had gone.
```

**Following context:**

```text
‘Well! I’ve often seen a cat without a grin,’ thought Alice; ‘but a grin without a cat! It’s the most curious thing I ever saw in my life!’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The tail disappeared first and the grin remained until last.

**Codex annotation notes:** New chronology fact from a previously unexposed paragraph.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>at110</strong> · contrastive_distractor · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** Could the executioner behead the Cheshire Cat’s visible head, according to both sides of the dispute?

**Proposed status:** `answered`

**Proposed reference answer:** They disagreed: the executioner said a head could not be cut off without a body, while the King said anything with a head could be beheaded.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `fact_at110`

**Evidence event:** `event_fact_at110`

**Development exposure:** `no_known_development_exposure`

**Exposure review:** Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** _none_

### Required claims and original context

#### C1: The executioner said a body was required.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 64, "chapter": "8", "pdf_block": 6}`

**Exact supporting span:**

```text
you couldn’t cut oﬀa head unless there was a body to cut it oﬀfrom
```

**Preceding context:**

```text
The moment Alice appeared, she was appealed to by all three to settle the question, and they repeated their arguments to her, though, as they all spoke at once, she found it very hard indeed to make out exactly what they said.
```

**Supporting paragraph/context:**

```text
The executioner’s argument was, that you couldn’t cut oﬀa head unless there was a body to cut it oﬀfrom: that he had never had to do such a thing before, and he wasn’t going to begin at HIS time of life.
```

**Following context:**

```text
The King’s argument was, that anything that had a head could be be- headed, and that you weren’t to talk nonsense.
```

**Context incomplete:** `false`

**Why it supports this claim:** The narrator reports the executioner’s position that beheading requires a body.

#### C2: The King argued that possessing a head was sufficient.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 64, "chapter": "8", "pdf_block": 7}`

**Exact supporting span:**

```text
anything that had a head could be be- headed
```

**Preceding context:**

```text
The executioner’s argument was, that you couldn’t cut oﬀa head unless there was a body to cut it oﬀfrom: that he had never had to do such a thing before, and he wasn’t going to begin at HIS time of life.
```

**Supporting paragraph/context:**

```text
The King’s argument was, that anything that had a head could be be- headed, and that you weren’t to talk nonsense.
```

**Following context:**

```text
The Queen’s argument was, that if something wasn’t done about it in less than no time she’d have everybody executed, all round. (It was this last remark that had made the whole party look so grave and anxious.)
```

**Context incomplete:** `false`

**Why it supports this claim:** The narrator reports the King’s opposing position that having a head is sufficient for beheading.

**Codex annotation notes:** Competing propositions from two sides remain distinct. Exact spans now contain the propositions themselves; epistemic status records that narration reports each argument, not that either argument is objectively true.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>at112</strong> · contrastive_distractor · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** Did the Gryphon agree that the Queen’s execution orders were actually carried out?

**Proposed status:** `answered`

**Proposed reference answer:** No. After the Queen left, the Gryphon said it was all her fancy and that nobody was ever executed.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `fact_at112`

**Evidence event:** `event_fact_at112`

**Development exposure:** `no_known_development_exposure`

**Exposure review:** Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** _none_

### Required claims and original context

#### C1: The Gryphon denied that the Queen’s threatened executions were carried out.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 70, "chapter": "9", "pdf_block": 4}`

**Exact supporting span:**

```text
It’s all her fancy, that: they never executes nobody
```

**Preceding context:**

```text
The Gryphon sat up and rubbed its eyes: then it watched the Queen till she was out of sight: then it chuckled. ‘What fun!’ said the Gryphon, half to itself, half to Alice.
```

**Supporting paragraph/context:**

```text
‘What IS the fun?’ said Alice. ‘Why, SHE,’ said the Gryphon. ‘It’s all her fancy, that: they never executes nobody, you know. Come on!’
```

**Following context:**

```text
‘Everybody says “come on!” here,’ thought Alice, as she went slowly after it: ‘I never was so ordered about in all my life, never!’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The Gryphon denied that the Queen’s threatened executions were carried out.

**Codex annotation notes:** The answer must preserve that this is the Gryphon’s assertion, not omniscient narration.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>at113</strong> · local_context_reasoning · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** According to the Gryphon, how did the whitings’ tails become stuck in their mouths?

**Proposed status:** `answered`

**Proposed reference answer:** They went with the lobsters, were thrown into the sea, fell a long way, and got their tails stuck in their mouths.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `fact_at113`

**Evidence event:** `event_fact_at113`

**Development exposure:** `no_known_development_exposure`

**Exposure review:** Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** _none_

### Required claims and original context

#### C1: The Gryphon gives a chain of events from joining the dance through the fall to the stuck tails.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 75, "chapter": "10", "pdf_block": 8}`

**Exact supporting span:**

```text
they WOULD go with the lobsters to the dance. So they got thrown out to sea
```

**Preceding context:**

```text
‘You’re wrong about the crumbs,’ said the Mock Turtle: ‘crumbs would all wash oﬀin the sea. But they HAVE their tails in their mouths; and the reason is–’ here the Mock Turtle yawned and shut his eyes.–‘Tell her about the reason and all that,’ he said to the Gryphon.
```

**Supporting paragraph/context:**

```text
‘The reason is,’ said the Gryphon, ‘that they WOULD go with the lobsters to the dance. So they got thrown out to sea. So they had to fall a long way. So they got their tails fast in their mouths. So they couldn’t get them out again. That’s all.’
```

**Following context:**

```text
‘Thank you,’ said Alice, ‘it’s very interesting. I never knew so much about a whiting before.’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The Gryphon gives a chain of events from joining the dance through the fall to the stuck tails.

**Codex annotation notes:** Preserves the source as the Gryphon’s fanciful explanation.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>at114</strong> · local_context_reasoning · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** When the Mock Turtle asked what a traveling fish’s ‘porpoise’ was, which word did Alice think he meant?

**Proposed status:** `answered`

**Proposed reference answer:** Purpose.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_at114`

**Evidence event:** `event_fact_at114`

**Development exposure:** `no_known_development_exposure`

**Exposure review:** Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** _none_

### Required claims and original context

#### C1: Alice interpreted ‘porpoise’ as the word ‘purpose.’

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 76, "chapter": "10", "pdf_block": 4}`

**Exact supporting span:**

```text
‘Don’t you mean “purpose”?’ said Alice
```

**Preceding context:**

```text
‘Wouldn’t it really?’ said Alice in a tone of great surprise. ‘Of course not,’ said the Mock Turtle: ‘why, if a ﬁsh came to ME, and told me he was going a journey, I should say “With what porpoise?”’
```

**Supporting paragraph/context:**

```text
‘Don’t you mean “purpose”?’ said Alice. ‘I mean what I say,’ the Mock Turtle replied in an oﬀended tone. And the Gryphon added ‘Come, let’s hear some of YOUR adventures.’
```

**Following context:**

```text
‘I could tell you my adventures–beginning from this morning,’ said Alice a little timidly: ‘but it’s no use going back to yesterday, because I was a diﬀerent person then.’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Alice interpreted ‘porpoise’ as the word ‘purpose.’

**Codex annotation notes:** A speaker-attributed homophone test from an unexposed passage.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>at115</strong> · multi_fact_single_context · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** Which song was interrupted, and what interrupted it?

**Proposed status:** `answered`

**Proposed reference answer:** The Mock Turtle’s ‘Turtle Soup’ song was interrupted by a distant cry that the trial was beginning.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_at115`

**Evidence event:** `event_fact_at115`

**Development exposure:** `no_known_development_exposure`

**Exposure review:** Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** _none_

### Required claims and original context

#### C1: The song was ‘Turtle Soup.’

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 78, "chapter": "10", "pdf_block": 4}`

**Exact supporting span:**

```text
Sing her “Turtle Soup,” will you
```

**Preceding context:**

```text
‘Shall we try another ﬁgure of the Lobster Quadrille?’ the Gryphon went on. ‘Or would you like the Mock Turtle to sing you a song?’
```

**Supporting paragraph/context:**

```text
‘Oh, a song, please, if the Mock Turtle would be so kind,’ Alice replied, so eagerly that the Gryphon said, in a rather oﬀended tone, ‘Hm! No accounting for tastes! Sing her “Turtle Soup,” will you, old fellow?’
```

**Following context:**

```text
The Mock Turtle sighed deeply, and began, in a voice sometimes choked with sobs, to sing this:–
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The song was ‘Turtle Soup.’

#### C2: A cry announcing the trial interrupted it.

**Evidence E2 location:** `{"book": "alice_in_wonderland", "page": 78, "chapter": "10", "pdf_block": 8}`

**Exact supporting span:**

```text
a cry of ‘The trial’s beginning!’ was heard in the distance
```

**Preceding context:**

```text
‘Beautiful Soup! Who cares for ﬁsh, Game, or any other dish? Who would not give all else for two Pennyworth only of beautiful Soup? Pennyworth only of beautiful Soup? Beau–ootiful Soo–oop! Beau–ootiful Soo–oop! Soo–oop of the e–e–evening, Beautiful, beauti–FUL SOUP!’
```

**Supporting paragraph/context:**

```text
‘Chorus again!’ cried the Gryphon, and the Mock Turtle had just begun to repeat it, when a cry of ‘The trial’s beginning!’ was heard in the distance.
```

**Following context:**

```text
‘Come on!’ cried the Gryphon, and, taking Alice by the hand, it hurried oﬀ, without waiting for the end of the song.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: A cry announcing the trial interrupted it.

**Codex annotation notes:** Two material facts in one continuous scene; intentionally not labeled multi-source.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>at117</strong> · direct_factual_single_source · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** What did Pat claim he was digging for when the White Rabbit called him?

**Proposed status:** `answered`

**Proposed reference answer:** Apples.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_at117`

**Evidence event:** `event_at117`

**Development exposure:** `no_known_development_exposure`

**Exposure review:** Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** _none_

### Required claims and original context

#### C1: Pat claimed that he was digging for apples.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 33, "chapter": "4", "pdf_block": 8}`

**Exact supporting span:**

```text
Digging for apples, yer honour
```

**Preceding context:**

```text
‘THAT you won’t’ thought Alice, and, after waiting till she fancied she heard the Rabbit just under the window, she suddenly spread out her hand, and made a snatch in the air. She did not get hold of anything, but she heard a little shriek and a fall, and a crash of broken glass, from which she concluded that it was just possible it had fallen into a cucumber-frame, or something of the sort.
```

**Supporting paragraph/context:**

```text
Next came an angry voice–the Rabbit’s–‘Pat! Pat! Where are you?’ And then a voice she had never heard before, ‘Sure then I’m here! Digging for apples, yer honour!’
```

**Following context:**

```text
‘Digging for apples, indeed!’ said the Rabbit angrily. ‘Here! Come and help me out of THIS!’ (Sounds of more broken glass.)
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Pat claimed that he was digging for apples.

**Codex annotation notes:** Replacement TEST fact from a source unit not exposed by DEV evidence or review excerpts.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>at118</strong> · multi_fact_single_context · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** Why did Alice take Bill the Lizard’s pencil, and how did he write afterward?

**Proposed status:** `answered`

**Proposed reference answer:** The pencil squeaked, so Alice took it; Bill then tried to write with one finger, which left no mark.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `fact_at118`

**Evidence event:** `event_at118`

**Development exposure:** `no_known_development_exposure`

**Exposure review:** Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** _none_

### Required claims and original context

#### C1: Alice took the pencil because it squeaked.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 82, "chapter": "11", "pdf_block": 5}`

**Exact supporting span:**

```text
One of the jurors had a pencil that squeaked
```

**Preceding context:**

```text
Alice could see, as well as if she were looking over their shoulders, that all the jurors were writing down ‘stupid things!’ on their slates, and she could even make out that one of them didn’t know how to spell ‘stupid,’ and that he had to ask his neighbour to tell him. ‘A nice muddle their slates’ll be in before the trial’s over!’ thought Alice.
```

**Supporting paragraph/context:**

```text
One of the jurors had a pencil that squeaked. This of course, Alice could not stand, and she went round the court and got behind him, and very soon found an opportunity of taking it away. She did it so quickly that the poor little juror (it was Bill, the Lizard) could not make out at all what had become of it; so, after hunting all about for it, he was obliged to write with one ﬁnger for the rest of the day; and this was of very little use, as it left no mark on the slate.
```

**Following context:**

```text
‘Herald, read the accusation!’ said the King. On this the White Rabbit blew three blasts on the trumpet, and then unrolled the parchment scroll, and read as follows:–
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Alice took the pencil because it squeaked.; Bill then wrote with one finger, which left no mark.

#### C2: Bill then wrote with one finger, which left no mark.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 82, "chapter": "11", "pdf_block": 5}`

**Exact supporting span:**

```text
One of the jurors had a pencil that squeaked
```

**Preceding context:**

```text
Alice could see, as well as if she were looking over their shoulders, that all the jurors were writing down ‘stupid things!’ on their slates, and she could even make out that one of them didn’t know how to spell ‘stupid,’ and that he had to ask his neighbour to tell him. ‘A nice muddle their slates’ll be in before the trial’s over!’ thought Alice.
```

**Supporting paragraph/context:**

```text
One of the jurors had a pencil that squeaked. This of course, Alice could not stand, and she went round the court and got behind him, and very soon found an opportunity of taking it away. She did it so quickly that the poor little juror (it was Bill, the Lizard) could not make out at all what had become of it; so, after hunting all about for it, he was obliged to write with one ﬁnger for the rest of the day; and this was of very little use, as it left no mark on the slate.
```

**Following context:**

```text
‘Herald, read the accusation!’ said the King. On this the White Rabbit blew three blasts on the trumpet, and then unrolled the parchment scroll, and read as follows:–
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Alice took the pencil because it squeaked.; Bill then wrote with one finger, which left no mark.

**Codex annotation notes:** Replacement TEST case with two facts in one continuous, previously unexposed local event.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>at119</strong> · local_context_reasoning · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** How did the court officers ‘suppress’ a cheering guinea-pig?

**Proposed status:** `answered`

**Proposed reference answer:** They put it head-first into a tied canvas bag and sat on it.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `fact_at119`

**Evidence event:** `event_at119`

**Development exposure:** `no_known_development_exposure`

**Exposure review:** Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** _none_

### Required claims and original context

#### C1: The officers put the guinea-pig head-first into a tied canvas bag and sat on it.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 84, "chapter": "11", "pdf_block": 8}`

**Exact supporting span:**

```text
into this they slipped the guinea-pig, head first, and then sat upon it
```

**Preceding context:**

```text
‘After that,’ continued the Hatter, ‘I cut some more bread- and-butter–’ ‘But what did the Dormouse say?’ one of the jury asked. ‘That I can’t remember,’ said the Hatter. ‘You MUST remember,’ remarked the King, ‘or I’ll have you executed.’ The miserable Hatter dropped his teacup and bread-and-butter, and went down on one knee. ‘I’m a poor man, your Majesty,’ he began.
```

**Supporting paragraph/context:**

```text
‘You’re a very poor speaker,’ said the King. Here one of the guinea-pigs cheered, and was immediately suppressed by the oﬃcers of the court. (As that is rather a hard word, I will just explain to you how it was done. They had a large canvas bag, which tied up at the mouth with strings: into this they slipped the guinea-pig, head ﬁrst, and then sat upon it.)
```

**Following context:**

```text
‘I’m glad I’ve seen that done,’ thought Alice. ‘I’ve so often read in the newspapers, at the end of trials, “There was some attempts at applause, which was immediately suppressed by the oﬃcers of the court,” and I never understood what it meant till now.’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The officers put the guinea-pig head-first into a tied canvas bag and sat on it.

**Codex annotation notes:** Replacement TEST meaning-in-context case from a court event not exposed in DEV.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>at120</strong> · multi_fact_single_context · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** What accident did Alice cause when she jumped up after being called as a witness?

**Proposed status:** `answered`

**Proposed reference answer:** She tipped over the jury-box with her skirt and spilled the jurors onto the crowd below.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_at120`

**Evidence event:** `event_at120`

**Development exposure:** `no_known_development_exposure`

**Exposure review:** Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** _none_

### Required claims and original context

#### C1: Alice tipped over the jury-box with her skirt.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 87, "chapter": "12", "pdf_block": 2}`

**Exact supporting span:**

```text
she tipped over the jury-box with the edge of her skirt
```

**Preceding context:**

```text
Alice’s Evidence
```

**Supporting paragraph/context:**

```text
‘Here!’ cried Alice, quite forgetting in the ﬂurry of the moment how large she had grown in the last few minutes, and she jumped up in such a hurry that she tipped over the jury-box with the edge of her skirt, upsetting all the jurymen on to the heads of the crowd below, and there they lay sprawling about, reminding her very much of a globe of goldﬁsh she had accidentally upset the week before.
```

**Following context:**

```text
‘Oh, I BEG your pardon!’ she exclaimed in a tone of great dismay, and began picking them up again as quickly as she could, for the accident of the goldﬁsh kept running in her head, and she had a vague sort of idea that they must be collected at once and put back into the jury-box, or they would die.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Alice tipped over the jury-box with her skirt.; The jurors fell onto the crowd below.

#### C2: The jurors fell onto the crowd below.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 87, "chapter": "12", "pdf_block": 2}`

**Exact supporting span:**

```text
she tipped over the jury-box with the edge of her skirt
```

**Preceding context:**

```text
Alice’s Evidence
```

**Supporting paragraph/context:**

```text
‘Here!’ cried Alice, quite forgetting in the ﬂurry of the moment how large she had grown in the last few minutes, and she jumped up in such a hurry that she tipped over the jury-box with the edge of her skirt, upsetting all the jurymen on to the heads of the crowd below, and there they lay sprawling about, reminding her very much of a globe of goldﬁsh she had accidentally upset the week before.
```

**Following context:**

```text
‘Oh, I BEG your pardon!’ she exclaimed in a tone of great dismay, and began picking them up again as quickly as she could, for the accident of the goldﬁsh kept running in her head, and she had a vague sort of idea that they must be collected at once and put back into the jury-box, or they would die.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Alice tipped over the jury-box with her skirt.; The jurors fell onto the crowd below.

**Codex annotation notes:** Replacement TEST event from a source unit not used by DEV evidence or ambiguity material.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>at121</strong> · multi_fact_single_context · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** What did the Queen throw at the Lizard after denying that she had fits, and how did he use it?

**Proposed status:** `answered`

**Proposed reference answer:** She threw an inkstand; the Lizard used the ink dripping down his face to resume writing.

**Book / difficulty:** `alice_in_wonderland` / `hard`

**Fact family:** `fact_at121`

**Evidence event:** `event_at121`

**Development exposure:** `no_known_development_exposure`

**Exposure review:** Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** _none_

### Required claims and original context

#### C1: The Queen threw an inkstand at the Lizard.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 90, "chapter": "12", "pdf_block": 11}`

**Exact supporting span:**

```text
throwing an inkstand at the Lizard
```

**Preceding context:**

```text
‘Why, there they are!’ said the King triumphantly, pointing to the tarts on the table. ‘Nothing can be clearer than THAT. Then again– “BEFORE SHE HAD THIS FIT–” you never had ﬁts, my dear, I think?’ he said to the Queen.
```

**Supporting paragraph/context:**

```text
‘Never!’ said the Queen furiously, throwing an inkstand at the Lizard as she spoke. (The unfortunate little Bill had left oﬀwriting on his slate with one ﬁnger, as he found it made no mark; but he now hastily began again, using the ink, that was trickling down his face, as long as it lasted.)
```

**Following context:**

```text
‘Then the words don’t FIT you,’ said the King, looking round the court with a smile. There was a dead silence.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The Queen threw an inkstand at the Lizard.; The Lizard used the dripping ink to write again.

#### C2: The Lizard used the dripping ink to write again.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 90, "chapter": "12", "pdf_block": 11}`

**Exact supporting span:**

```text
throwing an inkstand at the Lizard
```

**Preceding context:**

```text
‘Why, there they are!’ said the King triumphantly, pointing to the tarts on the table. ‘Nothing can be clearer than THAT. Then again– “BEFORE SHE HAD THIS FIT–” you never had ﬁts, my dear, I think?’ he said to the Queen.
```

**Supporting paragraph/context:**

```text
‘Never!’ said the Queen furiously, throwing an inkstand at the Lizard as she spoke. (The unfortunate little Bill had left oﬀwriting on his slate with one ﬁnger, as he found it made no mark; but he now hastily began again, using the ink, that was trickling down his face, as long as it lasted.)
```

**Following context:**

```text
‘Then the words don’t FIT you,’ said the King, looking round the court with a smile. There was a dead silence.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The Queen threw an inkstand at the Lizard.; The Lizard used the dripping ink to write again.

**Codex annotation notes:** Replacement TEST cause-and-use relation from a previously unexposed paragraph.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>at122</strong> · direct_factual_single_source · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** What did the Mock Turtle say he had once been?

**Proposed status:** `answered`

**Proposed reference answer:** A real turtle.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_at122`

**Evidence event:** `event_at122`

**Development exposure:** `no_known_development_exposure`

**Exposure review:** Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** _none_

### Required claims and original context

#### C1: The Mock Turtle said that he had once been a real turtle.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 70, "chapter": "9", "pdf_block": 11}`

**Exact supporting span:**

```text
I was a real Turtle
```

**Preceding context:**

```text
So they sat down, and nobody spoke for some minutes. Alice thought to herself, ‘I don’t see how he can EVEN ﬁnish, if he doesn’t begin.’ But she waited patiently.
```

**Supporting paragraph/context:**

```text
‘Once,’ said the Mock Turtle at last, with a deep sigh, ‘I was a real Turtle.’ These words were followed by a very long silence, broken only by an occasional exclamation of ‘Hjckrrh!’ from the Gryphon, and the constant heavy sobbing of the Mock Turtle. Alice was very nearly getting up and saying, ‘Thank you, sir, for your interesting story,’ but she could not help thinking there MUST be more to come, so she sat still and said nothing.
```

**Following context:**

```text
‘When we were little,’ the Mock Turtle went on at last, more calmly, though still sobbing a little now and then, ‘we went to school in the sea. The master was an old Turtle–we used to call him Tortoise–’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The Mock Turtle said that he had once been a real turtle.

**Codex annotation notes:** Replacement TEST speaker-attributed fact from an unexposed paragraph.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>at123</strong> · local_context_reasoning · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** Why did Alice say there was no use going back to yesterday when telling her adventures?

**Proposed status:** `answered`

**Proposed reference answer:** Because she said she had been a different person yesterday.

**Book / difficulty:** `alice_in_wonderland` / `medium`

**Fact family:** `fact_at123`

**Evidence event:** `event_at123`

**Development exposure:** `no_known_development_exposure`

**Exposure review:** Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** _none_

### Required claims and original context

#### C1: Alice said yesterday was not useful because she had been a different person then.

**Evidence E1 location:** `{"book": "alice_in_wonderland", "page": 76, "chapter": "10", "pdf_block": 5}`

**Exact supporting span:**

```text
it’s no use going back to yesterday, because I was a different person then
```

**Preceding context:**

```text
‘Don’t you mean “purpose”?’ said Alice. ‘I mean what I say,’ the Mock Turtle replied in an oﬀended tone. And the Gryphon added ‘Come, let’s hear some of YOUR adventures.’
```

**Supporting paragraph/context:**

```text
‘I could tell you my adventures–beginning from this morning,’ said Alice a little timidly: ‘but it’s no use going back to yesterday, because I was a diﬀerent person then.’
```

**Following context:**

```text
‘Explain all that,’ said the Mock Turtle. ‘No, no! The adventures ﬁrst,’ said the Gryphon in an impatient tone: ‘explanations take such a dreadful time.’
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Alice said yesterday was not useful because she had been a different person then.

**Codex annotation notes:** Replacement TEST rationale from an unexposed dialogue unit.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>


# secret_garden_holdout

<details>
<summary><strong>sg081</strong> · direct_factual_single_source · answered · FAST_CONFIRM — needs owner attention</summary>

**Question:** In which country was Mary Lennox born?

**Proposed status:** `answered`

**Proposed reference answer:** India.

**Book / difficulty:** `the_secret_garden` / `medium`

**Fact family:** `fact_sg081`

**Evidence event:** `event_fact_sg081`

**Development exposure:** `not_applicable_different_book`

**Exposure review:** Secret Garden is a separate-book holdout.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** _none_

### Required claims and original context

#### C1: Mary was born in India.

**Evidence E1 location:** `{"book": "the_secret_garden", "canonical_line": 49, "chapter": null, "generated_pdf_pages": [1]}`

**Exact supporting span:**

```text
she had been born in India
```

**Preceding context:**

```text
CHAPTER I. THERE IS NO ONE LEFT
```

**Supporting paragraph/context:**

```text
When Mary Lennox was sent to Misselthwaite Manor to live with her uncle everybody said she was the most disagreeable-looking child ever seen. It was true, too. She had a little thin face and a little thin body, thin light hair and a sour expression. Her hair was yellow, and her face was yellow because she had been born in India and had always been ill in one way or another. Her father had held a position under the English Government and had always been busy and ill himself, and her mother had been a great beauty who cared only to go to parties and amuse herself with gay people. She had not wanted a little girl at all, and when Mary was born she handed her over to the care of an Ayah, who was made to understand that if she wished to please the Mem Sahib she must keep the child out of sight as much as possible. So when she was a sickly, fretful, ugly little baby she was kept out of the way, and when she became a sickly, fretful, toddling thing she was kept out of the way also. She never remembered seeing familiarly anything but the dark faces of her Ayah and the other native servants, and as they always obeyed her and gave her her own way in everything, because the Mem Sahib would be angry if she was disturbed by her crying, by the time she was six years old she was as tyrannical and selfish a little pig as ever lived. The young English governess who came to teach her to read and write disliked her so much that she gave up her place in three months, and when other governesses came to try to fill it they always went away in a shorter time than the first one. So if Mary had not chosen to really want to know how to read books she would never have learned her letters at all.
```

**Following context:**

```text
One frightfully hot morning, when she was about nine years old, she awakened feeling very cross, and she became crosser still when she saw that the servant who stood by her bedside was not her Ayah.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Mary was born in India.

**Codex annotation notes:** Holdout item: full owner review remains mandatory.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>sg082</strong> · direct_factual_single_source · answered · FAST_CONFIRM — needs owner attention</summary>

**Question:** What was the name of the manor where Mary was sent to live?

**Proposed status:** `answered`

**Proposed reference answer:** Misselthwaite Manor.

**Book / difficulty:** `the_secret_garden` / `medium`

**Fact family:** `secret_manor_destination`

**Evidence event:** `event_secret_manor_destination`

**Development exposure:** `not_applicable_different_book`

**Exposure review:** Secret Garden is a separate-book holdout.

**Metamorphic / contrastive group:** `meta_secret_destination` / `none`

**Related cases:** `sg100`

**Tags:** _none_

### Required claims and original context

#### C1: The manor was Misselthwaite Manor.

**Evidence E1 location:** `{"book": "the_secret_garden", "canonical_line": 49, "chapter": null, "generated_pdf_pages": [1]}`

**Exact supporting span:**

```text
sent to Misselthwaite Manor to live with her uncle
```

**Preceding context:**

```text
CHAPTER I. THERE IS NO ONE LEFT
```

**Supporting paragraph/context:**

```text
When Mary Lennox was sent to Misselthwaite Manor to live with her uncle everybody said she was the most disagreeable-looking child ever seen. It was true, too. She had a little thin face and a little thin body, thin light hair and a sour expression. Her hair was yellow, and her face was yellow because she had been born in India and had always been ill in one way or another. Her father had held a position under the English Government and had always been busy and ill himself, and her mother had been a great beauty who cared only to go to parties and amuse herself with gay people. She had not wanted a little girl at all, and when Mary was born she handed her over to the care of an Ayah, who was made to understand that if she wished to please the Mem Sahib she must keep the child out of sight as much as possible. So when she was a sickly, fretful, ugly little baby she was kept out of the way, and when she became a sickly, fretful, toddling thing she was kept out of the way also. She never remembered seeing familiarly anything but the dark faces of her Ayah and the other native servants, and as they always obeyed her and gave her her own way in everything, because the Mem Sahib would be angry if she was disturbed by her crying, by the time she was six years old she was as tyrannical and selfish a little pig as ever lived. The young English governess who came to teach her to read and write disliked her so much that she gave up her place in three months, and when other governesses came to try to fill it they always went away in a shorter time than the first one. So if Mary had not chosen to really want to know how to read books she would never have learned her letters at all.
```

**Following context:**

```text
One frightfully hot morning, when she was about nine years old, she awakened feeling very cross, and she became crosser still when she saw that the servant who stood by her bedside was not her Ayah.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The manor was Misselthwaite Manor.

**Codex annotation notes:** Holdout item: full owner review remains mandatory.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>sg083</strong> · direct_factual_single_source · answered · FAST_CONFIRM — needs owner attention</summary>

**Question:** What was the name of Dickon’s mother?

**Proposed status:** `answered`

**Proposed reference answer:** Susan Sowerby.

**Book / difficulty:** `the_secret_garden` / `medium`

**Fact family:** `fact_sg083`

**Evidence event:** `event_fact_sg083`

**Development exposure:** `not_applicable_different_book`

**Exposure review:** Secret Garden is a separate-book holdout.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** _none_

### Required claims and original context

#### C1: The woman is identified as Susan Sowerby.

**Evidence E1 location:** `{"book": "the_secret_garden", "canonical_line": 8906, "chapter": null, "generated_pdf_pages": [129]}`

**Exact supporting span:**

```text
Susan Sowerby got up at last
```

**Preceding context:**

```text
One of the things they talked of was the visit they were to make to her cottage. They planned it all. They were to drive over the moor and lunch out of doors among the heather. They would see all the twelve children and Dickon’s garden and would not come back until they were tired.
```

**Supporting paragraph/context:**

```text
Susan Sowerby got up at last to return to the house and Mrs. Medlock. It was time for Colin to be wheeled back also. But before he got into his chair he stood quite close to Susan and fixed his eyes on her with a kind of bewildered adoration and he suddenly caught hold of the fold of her blue cloak and held it fast.
```

**Following context:**

```text
“You are just what I—what I wanted,” he said. “I wish you were my mother—as well as Dickon’s!”
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The woman is identified as Susan Sowerby.

#### C2: Colin identifies her as Dickon’s mother.

**Evidence E2 location:** `{"book": "the_secret_garden", "canonical_line": 8912, "chapter": null, "generated_pdf_pages": [129]}`

**Exact supporting span:**

```text
I wish you were my mother—as well as Dickon’s
```

**Preceding context:**

```text
Susan Sowerby got up at last to return to the house and Mrs. Medlock. It was time for Colin to be wheeled back also. But before he got into his chair he stood quite close to Susan and fixed his eyes on her with a kind of bewildered adoration and he suddenly caught hold of the fold of her blue cloak and held it fast.
```

**Supporting paragraph/context:**

```text
“You are just what I—what I wanted,” he said. “I wish you were my mother—as well as Dickon’s!”
```

**Following context:**

```text
All at once Susan Sowerby bent down and drew him with her warm arms close against the bosom under the blue cloak—as if he had been Dickon’s brother. The quick mist swept over her eyes.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Colin identifies her as Dickon’s mother.

**Codex annotation notes:** Holdout item: full owner review remains mandatory.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>sg084</strong> · direct_factual_single_source · answered · FAST_CONFIRM — needs owner attention</summary>

**Question:** Approximately how many rooms did Misselthwaite Manor have?

**Proposed status:** `answered`

**Proposed reference answer:** About one hundred rooms.

**Book / difficulty:** `the_secret_garden` / `medium`

**Fact family:** `fact_sg084`

**Evidence event:** `event_fact_sg084`

**Development exposure:** `not_applicable_different_book`

**Exposure review:** Secret Garden is a separate-book holdout.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** _none_

### Required claims and original context

#### C1: The house had nearly one hundred rooms.

**Evidence E1 location:** `{"book": "the_secret_garden", "canonical_line": 440, "chapter": null, "generated_pdf_pages": [7]}`

**Exact supporting span:**

```text
there’s near a hundred rooms in it
```

**Preceding context:**

```text
Mary said nothing at all, and Mrs. Medlock looked rather discomfited by her apparent indifference, but, after taking a breath, she went on.
```

**Supporting paragraph/context:**

```text
“Not but that it’s a grand big place in a gloomy way, and Mr. Craven’s proud of it in his way—and that’s gloomy enough, too. The house is six hundred years old and it’s on the edge of the moor, and there’s near a hundred rooms in it, though most of them’s shut up and locked. And there’s pictures and fine old furniture and things that’s been there for ages, and there’s a big park round it and gardens and trees with branches trailing to the ground—some of them.” She paused and took another breath. “But there’s nothing else,” she ended suddenly.
```

**Following context:**

```text
Mary had begun to listen in spite of herself. It all sounded so unlike India, and anything new rather attracted her. But she did not intend to look as if she were interested. That was one of her unhappy, disagreeable ways. So she sat still.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The house had nearly one hundred rooms.

**Codex annotation notes:** Holdout item: full owner review remains mandatory.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>sg085</strong> · multi_fact_single_context · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** Why was Mary left alone in the bungalow, and what happened to the remaining servants?

**Proposed status:** `answered`

**Proposed reference answer:** Mary’s parents had died, and the few servants who survived left the bungalow without remembering her, leaving her alone.

**Book / difficulty:** `the_secret_garden` / `hard`

**Fact family:** `secret_india_cholera`

**Evidence event:** `event_secret_india_cholera`

**Development exposure:** `not_applicable_different_book`

**Exposure review:** Secret Garden is a separate-book holdout.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** `sg089`, `sg093`

**Tags:** _none_

### Required claims and original context

#### C1: Mary’s father and mother had died and been carried away.

**Evidence E1 location:** `{"book": "the_secret_garden", "canonical_line": 227, "chapter": null, "generated_pdf_pages": [4]}`

**Exact supporting span:**

```text
the few native servants who had not died also had left the house as quickly as they could get out of it, none of them even remembering that there was a Missie Sahib
```

**Preceding context:**

```text
“Poor little kid!” he said. “There is nobody left to come.”
```

**Supporting paragraph/context:**

```text
It was in that strange and sudden way that Mary found out that she had neither father nor mother left; that they had died and been carried away in the night, and that the few native servants who had not died also had left the house as quickly as they could get out of it, none of them even remembering that there was a Missie Sahib. That was why the place was so quiet. It was true that there was no one in the bungalow but herself and the little rustling snake.
```

**Following context:**

```text
CHAPTER II. MISTRESS MARY QUITE CONTRARY
```

**Context incomplete:** `false`

**Why it supports this claim:** This narrator passage states that Mary’s parents were gone and that surviving servants left without remembering her.

#### C2: The few servants who had not died left the house without remembering Mary.

**Evidence E1 location:** `{"book": "the_secret_garden", "canonical_line": 227, "chapter": null, "generated_pdf_pages": [4]}`

**Exact supporting span:**

```text
the few native servants who had not died also had left the house as quickly as they could get out of it, none of them even remembering that there was a Missie Sahib
```

**Preceding context:**

```text
“Poor little kid!” he said. “There is nobody left to come.”
```

**Supporting paragraph/context:**

```text
It was in that strange and sudden way that Mary found out that she had neither father nor mother left; that they had died and been carried away in the night, and that the few native servants who had not died also had left the house as quickly as they could get out of it, none of them even remembering that there was a Missie Sahib. That was why the place was so quiet. It was true that there was no one in the bungalow but herself and the little rustling snake.
```

**Following context:**

```text
CHAPTER II. MISTRESS MARY QUITE CONTRARY
```

**Context incomplete:** `false`

**Why it supports this claim:** This narrator passage states that Mary’s parents were gone and that surviving servants left without remembering her.

**Codex annotation notes:** Unsupported cholera/panic causality removed from this package; duplicate copies of the same paragraph are not counted as multi-source evidence.

**Annotation confidence / review tier:** `high` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>sg086</strong> · multi_source_multi_fact · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** How did Mary obtain access to the locked garden?

**Proposed status:** `answered`

**Proposed reference answer:** Mary found the buried key in freshly turned soil, discovered the ivy-covered door when wind moved the ivy, and used the key to unlock it.

**Book / difficulty:** `the_secret_garden` / `hard`

**Fact family:** `secret_garden_access`

**Evidence event:** `event_secret_garden_access`

**Development exposure:** `not_applicable_different_book`

**Exposure review:** Secret Garden is a separate-book holdout.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** `sg092`

**Tags:** `temporal_order`

### Required claims and original context

#### C1: Mary found an old key buried in freshly turned soil.

**Evidence E1 location:** `{"book": "the_secret_garden", "canonical_line": 2053, "chapter": null, "generated_pdf_pages": [30]}`

**Exact supporting span:**

```text
it was an old key which looked as if it had been buried a long time
```

**Preceding context:**

```text
The flower-bed was not quite bare. It was bare of flowers because the perennial plants had been cut down for their winter rest, but there were tall shrubs and low ones which grew together at the back of the bed, and as the robin hopped about under them she saw him hop over a small pile of freshly turned up earth. He stopped on it to look for a worm. The earth had been turned up because a dog had been trying to dig up a mole and he had scratched quite a deep hole.
```

**Supporting paragraph/context:**

```text
Mary looked at it, not really knowing why the hole was there, and as she looked she saw something almost buried in the newly-turned soil. It was something like a ring of rusty iron or brass and when the robin flew up into a tree nearby she put out her hand and picked the ring up. It was more than a ring, however; it was an old key which looked as if it had been buried a long time.
```

**Following context:**

```text
Mistress Mary stood up and looked at it with an almost frightened face as it hung from her finger.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Mary found an old key buried in freshly turned soil.

#### C2: Wind shifted the ivy and revealed the door knob.

**Evidence E2 location:** `{"book": "the_secret_garden", "canonical_line": 2319, "chapter": null, "generated_pdf_pages": [34]}`

**Exact supporting span:**

```text
the gust of wind swung aside some loose ivy trails
```

**Preceding context:**

```text
Mary Lennox had heard a great deal about Magic in her Ayah’s stories, and she always said that what happened almost at that moment was Magic.
```

**Supporting paragraph/context:**

```text
One of the nice little gusts of wind rushed down the walk, and it was a stronger one than the rest. It was strong enough to wave the branches of the trees, and it was more than strong enough to sway the trailing sprays of untrimmed ivy hanging from the wall. Mary had stepped close to the robin, and suddenly the gust of wind swung aside some loose ivy trails, and more suddenly still she jumped toward it and caught it in her hand. This she did because she had seen something under it—a round knob which had been covered by the leaves hanging over it. It was the knob of a door.
```

**Following context:**

```text
She put her hands under the leaves and began to pull and push them aside. Thick as the ivy hung, it nearly all was a loose and swinging curtain, though some had crept over wood and iron. Mary’s heart began to thump and her hands to shake a little in her delight and excitement. The robin kept singing and twittering away and tilting his head on one side, as if he were as excited as she was. What was this under her hands which was square and made of iron and which her fingers found a hole in?
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Wind shifted the ivy and revealed the door knob.

#### C3: The key fitted the lock and opened the door.

**Evidence E3 location:** `{"book": "the_secret_garden", "canonical_line": 2338, "chapter": null, "generated_pdf_pages": [34]}`

**Exact supporting span:**

```text
drew out the key and found it fitted the keyhole
```

**Preceding context:**

```text
She put her hands under the leaves and began to pull and push them aside. Thick as the ivy hung, it nearly all was a loose and swinging curtain, though some had crept over wood and iron. Mary’s heart began to thump and her hands to shake a little in her delight and excitement. The robin kept singing and twittering away and tilting his head on one side, as if he were as excited as she was. What was this under her hands which was square and made of iron and which her fingers found a hole in?
```

**Supporting paragraph/context:**

```text
It was the lock of the door which had been closed ten years and she put her hand in her pocket, drew out the key and found it fitted the keyhole. She put the key in and turned it. It took two hands to do it, but it did turn.
```

**Following context:**

```text
And then she took a long breath and looked behind her up the long walk to see if anyone was coming. No one was coming. No one ever did come, it seemed, and she took another long breath, because she could not help it, and she held back the swinging curtain of ivy and pushed back the door which opened slowly—slowly.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The key fitted the lock and opened the door.

**Codex annotation notes:** Consolidates duplicate spans while preserving the three independently necessary access steps. Holdout item: full owner review remains mandatory.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>sg087</strong> · local_context_reasoning · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** How were Colin and Mary related, and who was Colin’s father?

**Proposed status:** `answered`

**Proposed reference answer:** They were cousins; Colin’s father was Mary’s uncle, Mr. Craven.

**Book / difficulty:** `the_secret_garden` / `hard`

**Fact family:** `secret_craven_relationship`

**Evidence event:** `event_secret_craven_relationship`

**Development exposure:** `not_applicable_different_book`

**Exposure review:** Secret Garden is a separate-book holdout.

**Metamorphic / contrastive group:** `none` / `contrast_craven_relationship`

**Related cases:** `sg095`

**Tags:** `relationship_inference`

### Required claims and original context

#### C1: Mary identifies Mr. Craven as her uncle.

**Evidence E1 location:** `{"book": "the_secret_garden", "canonical_line": 3973, "chapter": null, "generated_pdf_pages": [58]}`

**Exact supporting span:**

```text
Mr. Craven is my uncle
```

**Preceding context:**

```text
“I am Colin Craven. Who are you?”
```

**Supporting paragraph/context:**

```text
“I am Mary Lennox. Mr. Craven is my uncle.”
```

**Following context:**

```text
“He is my father,” said the boy.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Mary identifies Mr. Craven as her uncle.

#### C2: Colin identifies the same man as his father, making Mary and Colin cousins.

**Evidence E2 location:** `{"book": "the_secret_garden", "canonical_line": 3975, "chapter": null, "generated_pdf_pages": [58]}`

**Exact supporting span:**

```text
He is my father
```

**Preceding context:**

```text
“I am Mary Lennox. Mr. Craven is my uncle.”
```

**Supporting paragraph/context:**

```text
“He is my father,” said the boy.
```

**Following context:**

```text
“Your father!” gasped Mary. “No one ever told me he had a boy! Why didn’t they?”
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Colin identifies the same man as his father, making Mary and Colin cousins.

**Codex annotation notes:** The cousin relation is inferred from one continuous exchange; it is not distributed multi-source evidence. Holdout item: full owner review remains mandatory.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>sg088</strong> · local_context_reasoning · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** Who is “he” when Mrs. Medlock says, “He’s not going to trouble himself about you”?

**Proposed status:** `answered`

**Proposed reference answer:** Mr. Archibald Craven.

**Book / difficulty:** `the_secret_garden` / `medium`

**Fact family:** `fact_sg088`

**Evidence event:** `event_fact_sg088`

**Development exposure:** `not_applicable_different_book`

**Exposure review:** Secret Garden is a separate-book holdout.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `coreference`

### Required claims and original context

#### C1: The pronoun refers to Mr. Craven.

**Evidence E1 location:** `{"book": "the_secret_garden", "canonical_line": 440, "chapter": null, "generated_pdf_pages": [7]}`

**Exact supporting span:**

```text
Mr. Craven’s proud of it in his way
```

**Preceding context:**

```text
Mary said nothing at all, and Mrs. Medlock looked rather discomfited by her apparent indifference, but, after taking a breath, she went on.
```

**Supporting paragraph/context:**

```text
“Not but that it’s a grand big place in a gloomy way, and Mr. Craven’s proud of it in his way—and that’s gloomy enough, too. The house is six hundred years old and it’s on the edge of the moor, and there’s near a hundred rooms in it, though most of them’s shut up and locked. And there’s pictures and fine old furniture and things that’s been there for ages, and there’s a big park round it and gardens and trees with branches trailing to the ground—some of them.” She paused and took another breath. “But there’s nothing else,” she ended suddenly.
```

**Following context:**

```text
Mrs. Medlock is describing Misselthwaite Manor and explicitly names Mr. Craven. The conversation continues with Mary reacting to what she hears; no competing male referent is introduced before Mrs. Medlock says, ‘He’s not going to trouble himself about you.’
```

**Context incomplete:** `false`

**Why it supports this claim:** Mrs. Medlock explicitly names Mr. Craven in the continuing discourse.

**Evidence E2 location:** `{"book": "the_secret_garden", "canonical_line": 464, "chapter": null, "generated_pdf_pages": [7]}`

**Exact supporting span:**

```text
_He’s_ not going to trouble himself about you
```

**Preceding context:**

```text
Mrs. Medlock is describing Misselthwaite Manor and explicitly names Mr. Craven. The conversation continues with Mary reacting to what she hears; no competing male referent is introduced before Mrs. Medlock says, ‘He’s not going to trouble himself about you.’
```

**Supporting paragraph/context:**

```text
“You are right enough there,” said Mrs. Medlock. “It doesn’t. What you’re to be kept at Misselthwaite Manor for I don’t know, unless because it’s the easiest way. _He’s_ not going to trouble himself about you, that’s sure and certain. He never troubles himself about no one.”
```

**Following context:**

```text
She stopped herself as if she had just remembered something in time.
```

**Context incomplete:** `false`

**Why it supports this claim:** No competing male referent intervenes between Mr. Craven and Mrs. Medlock’s ‘He’.

**Codex annotation notes:** Answer remains Mr. Archibald Craven; reviewer-visible coreference bridge and speech-type metadata repaired.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>sg089</strong> · local_context_reasoning · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** Who says, “There is nobody left to come” after Mary asks why nobody comes?

**Proposed status:** `answered`

**Proposed reference answer:** The young man named Barney.

**Book / difficulty:** `the_secret_garden` / `medium`

**Fact family:** `secret_india_cholera`

**Evidence event:** `event_secret_india_cholera`

**Development exposure:** `not_applicable_different_book`

**Exposure review:** Secret Garden is a separate-book holdout.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** `sg085`, `sg093`

**Tags:** `speaker_identity`

### Required claims and original context

#### C1: The speaker is identified immediately before the quotation as Barney.

**Evidence E1 location:** `{"book": "the_secret_garden", "canonical_line": 222, "chapter": null, "generated_pdf_pages": [4]}`

**Exact supporting span:**

```text
young man whose name was Barney
```

**Preceding context:**

```text
“Why was I forgotten?” Mary said, stamping her foot. “Why does nobody come?”
```

**Supporting paragraph/context:**

```text
The young man whose name was Barney looked at her very sadly. Mary even thought she saw him wink his eyes as if to wink tears away.
```

**Following context:**

```text
“Poor little kid!” he said. “There is nobody left to come.”
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The speaker is identified immediately before the quotation as Barney.

**Evidence E2 location:** `{"book": "the_secret_garden", "canonical_line": 225, "chapter": null, "generated_pdf_pages": [4]}`

**Exact supporting span:**

```text
There is nobody left to come
```

**Preceding context:**

```text
The young man whose name was Barney looked at her very sadly. Mary even thought she saw him wink his eyes as if to wink tears away.
```

**Supporting paragraph/context:**

```text
“Poor little kid!” he said. “There is nobody left to come.”
```

**Following context:**

```text
It was in that strange and sudden way that Mary found out that she had neither father nor mother left; that they had died and been carried away in the night, and that the few native servants who had not died also had left the house as quickly as they could get out of it, none of them even remembering that there was a Missie Sahib. That was why the place was so quiet. It was true that there was no one in the bungalow but herself and the little rustling snake.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The speaker is identified immediately before the quotation as Barney.

**Codex annotation notes:** Holdout item: full owner review remains mandatory.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>sg090</strong> · local_context_reasoning · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** Whose garden does Martha mean when she says, “It was her garden”?

**Proposed status:** `answered`

**Proposed reference answer:** Mrs. Craven’s—the late wife of Mr. Craven.

**Book / difficulty:** `the_secret_garden` / `medium`

**Fact family:** `secret_garden_history`

**Evidence event:** `event_secret_garden_history`

**Development exposure:** `not_applicable_different_book`

**Exposure review:** Secret Garden is a separate-book holdout.

**Metamorphic / contrastive group:** `none` / `contrast_garden_history`

**Related cases:** `sg094`

**Tags:** `coreference`, `temporal_context`

### Required claims and original context

#### C1: The antecedent is Mr. Craven’s wife.

**Evidence E1 location:** `{"book": "the_secret_garden", "canonical_line": 1025, "chapter": null, "generated_pdf_pages": [15]}`

**Exact supporting span:**

```text
Mr. Craven had it shut when his wife died so sudden
```

**Preceding context:**

```text
“Why?” asked Mary in spite of herself. Here was another locked door added to the hundred in the strange house.
```

**Supporting paragraph/context:**

```text
“Mr. Craven had it shut when his wife died so sudden. He won’t let no one go inside. It was her garden. He locked th’ door an’ dug a hole and buried th’ key. There’s Mrs. Medlock’s bell ringing—I must run.”
```

**Following context:**

```text
After she was gone Mary turned down the walk which led to the door in the shrubbery. She could not help thinking about the garden which no one had been into for ten years. She wondered what it would look like and whether there were any flowers still alive in it. When she had passed through the shrubbery gate she found herself in great gardens, with wide lawns and winding walks with clipped borders. There were trees, and flower-beds, and evergreens clipped into strange shapes, and a large pool with an old gray fountain in its midst. But the flower-beds were bare and wintry and the fountain was not playing. This was not the garden which was shut up. How could a garden be shut up? You could always walk into a garden.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The antecedent is Mr. Craven’s wife.

**Evidence E2 location:** `{"book": "the_secret_garden", "canonical_line": 1025, "chapter": null, "generated_pdf_pages": [15]}`

**Exact supporting span:**

```text
It was her garden
```

**Preceding context:**

```text
“Why?” asked Mary in spite of herself. Here was another locked door added to the hundred in the strange house.
```

**Supporting paragraph/context:**

```text
“Mr. Craven had it shut when his wife died so sudden. He won’t let no one go inside. It was her garden. He locked th’ door an’ dug a hole and buried th’ key. There’s Mrs. Medlock’s bell ringing—I must run.”
```

**Following context:**

```text
After she was gone Mary turned down the walk which led to the door in the shrubbery. She could not help thinking about the garden which no one had been into for ten years. She wondered what it would look like and whether there were any flowers still alive in it. When she had passed through the shrubbery gate she found herself in great gardens, with wide lawns and winding walks with clipped borders. There were trees, and flower-beds, and evergreens clipped into strange shapes, and a large pool with an old gray fountain in its midst. But the flower-beds were bare and wintry and the fountain was not playing. This was not the garden which was shut up. How could a garden be shut up? You could always walk into a garden.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The antecedent is Mr. Craven’s wife.

**Codex annotation notes:** Holdout item: full owner review remains mandatory.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>sg091</strong> · local_context_reasoning · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** Who chants that “The Magic is in me,” and is the line narration or dialogue?

**Proposed status:** `answered`

**Proposed reference answer:** Colin chants it; it is dialogue spoken by him.

**Book / difficulty:** `the_secret_garden` / `medium`

**Fact family:** `fact_sg091`

**Evidence event:** `event_fact_sg091`

**Development exposure:** `not_applicable_different_book`

**Exposure review:** Secret Garden is a separate-book holdout.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `quote_vs_narrator`, `speaker_identity`

### Required claims and original context

#### C1: Colin announces he will chant and then speaks the line.

**Evidence E1 location:** `{"book": "the_secret_garden", "canonical_line": 7759, "chapter": null, "generated_pdf_pages": [112]}`

**Exact supporting span:**

```text
Then I will chant,” he said
```

**Preceding context:**

```text
No one smiled. They were all too much in earnest. Colin’s face was not even crossed by a shadow. He was thinking only of the Magic.
```

**Supporting paragraph/context:**

```text
“Then I will chant,” he said. And he began, looking like a strange boy spirit. “The sun is shining—the sun is shining. That is the Magic. The flowers are growing—the roots are stirring. That is the Magic. Being alive is the Magic—being strong is the Magic. The Magic is in me—the Magic is in me. It is in me—it is in me. It’s in everyone of us. It’s in Ben Weatherstaff’s back. Magic! Magic! Come and help!”
```

**Following context:**

```text
He said it a great many times—not a thousand times but quite a goodly number. Mary listened entranced. She felt as if it were at once queer and beautiful and she wanted him to go on and on. Ben Weatherstaff began to feel soothed into a sort of dream which was quite agreeable. The humming of the bees in the blossoms mingled with the chanting voice and drowsily melted into a doze. Dickon sat cross-legged with his rabbit asleep on his arm and a hand resting on the lamb’s back. Soot had pushed away a squirrel and huddled close to him on his shoulder, the gray film dropped over his eyes. At last Colin stopped.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Colin announces he will chant and then speaks the line.

**Evidence E2 location:** `{"book": "the_secret_garden", "canonical_line": 7759, "chapter": null, "generated_pdf_pages": [112]}`

**Exact supporting span:**

```text
The Magic is in me—the Magic is in me
```

**Preceding context:**

```text
No one smiled. They were all too much in earnest. Colin’s face was not even crossed by a shadow. He was thinking only of the Magic.
```

**Supporting paragraph/context:**

```text
“Then I will chant,” he said. And he began, looking like a strange boy spirit. “The sun is shining—the sun is shining. That is the Magic. The flowers are growing—the roots are stirring. That is the Magic. Being alive is the Magic—being strong is the Magic. The Magic is in me—the Magic is in me. It is in me—it is in me. It’s in everyone of us. It’s in Ben Weatherstaff’s back. Magic! Magic! Come and help!”
```

**Following context:**

```text
He said it a great many times—not a thousand times but quite a goodly number. Mary listened entranced. She felt as if it were at once queer and beautiful and she wanted him to go on and on. Ben Weatherstaff began to feel soothed into a sort of dream which was quite agreeable. The humming of the bees in the blossoms mingled with the chanting voice and drowsily melted into a doze. Dickon sat cross-legged with his rabbit asleep on his arm and a hand resting on the lamb’s back. Soot had pushed away a squirrel and huddled close to him on his shoulder, the gray film dropped over his eyes. At last Colin stopped.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Colin announces he will chant and then speaks the line.

**Codex annotation notes:** Holdout item: full owner review remains mandatory.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>sg092</strong> · paraphrase_vocabulary_mismatch · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** What entrance was concealed by a curtain of ivy?

**Proposed status:** `answered`

**Proposed reference answer:** The door to the secret garden.

**Book / difficulty:** `the_secret_garden` / `medium`

**Fact family:** `secret_garden_access`

**Evidence event:** `event_secret_garden_access`

**Development exposure:** `not_applicable_different_book`

**Exposure review:** Secret Garden is a separate-book holdout.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** `sg086`

**Tags:** `paraphrase`

### Required claims and original context

#### C1: The ivy concealed the garden door.

**Evidence E1 location:** `{"book": "the_secret_garden", "canonical_line": 2319, "chapter": null, "generated_pdf_pages": [34]}`

**Exact supporting span:**

```text
gust of wind swung aside some loose ivy trails
```

**Preceding context:**

```text
Mary Lennox had heard a great deal about Magic in her Ayah’s stories, and she always said that what happened almost at that moment was Magic.
```

**Supporting paragraph/context:**

```text
One of the nice little gusts of wind rushed down the walk, and it was a stronger one than the rest. It was strong enough to wave the branches of the trees, and it was more than strong enough to sway the trailing sprays of untrimmed ivy hanging from the wall. Mary had stepped close to the robin, and suddenly the gust of wind swung aside some loose ivy trails, and more suddenly still she jumped toward it and caught it in her hand. This she did because she had seen something under it—a round knob which had been covered by the leaves hanging over it. It was the knob of a door.
```

**Following context:**

```text
Mary pulls the ivy aside, finds the door’s lock, uses the buried key, turns it, pushes the door open, slips through, closes it behind her, and is then standing inside the secret garden.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The ivy concealed the garden door.

**Evidence E2 location:** `{"book": "the_secret_garden", "canonical_line": 2319, "chapter": null, "generated_pdf_pages": [34]}`

**Exact supporting span:**

```text
It was the knob of a door
```

**Preceding context:**

```text
Mary Lennox had heard a great deal about Magic in her Ayah’s stories, and she always said that what happened almost at that moment was Magic.
```

**Supporting paragraph/context:**

```text
One of the nice little gusts of wind rushed down the walk, and it was a stronger one than the rest. It was strong enough to wave the branches of the trees, and it was more than strong enough to sway the trailing sprays of untrimmed ivy hanging from the wall. Mary had stepped close to the robin, and suddenly the gust of wind swung aside some loose ivy trails, and more suddenly still she jumped toward it and caught it in her hand. This she did because she had seen something under it—a round knob which had been covered by the leaves hanging over it. It was the knob of a door.
```

**Following context:**

```text
Mary pulls the ivy aside, finds the door’s lock, uses the buried key, turns it, pushes the door open, slips through, closes it behind her, and is then standing inside the secret garden.
```

**Context incomplete:** `false`

**Why it supports this claim:** The extended continuous scene connects the ivy-covered door directly to Mary entering and standing inside the secret garden.

**Codex annotation notes:** Answer preserved; evidence package extended through Mary’s arrival inside the secret garden.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>sg093</strong> · paraphrase_vocabulary_mismatch · answered · FAST_CONFIRM — needs owner attention</summary>

**Question:** What epidemic explains the deaths and panic at Mary’s home in India?

**Proposed status:** `answered`

**Proposed reference answer:** Cholera.

**Book / difficulty:** `the_secret_garden` / `medium`

**Fact family:** `secret_india_cholera`

**Evidence event:** `event_secret_india_cholera`

**Development exposure:** `not_applicable_different_book`

**Exposure review:** Secret Garden is a separate-book holdout.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** `sg085`, `sg089`

**Tags:** `paraphrase`

### Required claims and original context

#### C1: The outbreak was cholera.

**Evidence E1 location:** `{"book": "the_secret_garden", "canonical_line": 139, "chapter": null, "generated_pdf_pages": [2]}`

**Exact supporting span:**

```text
The cholera had broken out in its most fatal form
```

**Preceding context:**

```text
“I did not know!” the Mem Sahib cried. “Come with me! Come with me!” and she turned and ran into the house.
```

**Supporting paragraph/context:**

```text
After that appalling things happened, and the mysteriousness of the morning was explained to Mary. The cholera had broken out in its most fatal form and people were dying like flies. The Ayah had been taken ill in the night, and it was because she had just died that the servants had wailed in the huts. Before the next day three other servants were dead and others had run away in terror. There was panic on every side, and dying people in all the bungalows.
```

**Following context:**

```text
During the confusion and bewilderment of the second day Mary hid herself in the nursery and was forgotten by everyone. Nobody thought of her, nobody wanted her, and strange things happened of which she knew nothing. Mary alternately cried and slept through the hours. She only knew that people were ill and that she heard mysterious and frightening sounds. Once she crept into the dining-room and found it empty, though a partly finished meal was on the table and chairs and plates looked as if they had been hastily pushed back when the diners rose suddenly for some reason. The child ate some fruit and biscuits, and being thirsty she drank a glass of wine which stood nearly filled. It was sweet, and she did not know how strong it was. Very soon it made her intensely drowsy, and she went back to her nursery and shut herself in again, frightened by cries she heard in the huts and by the hurrying sound of feet. The wine made her so sleepy that she could scarcely keep her eyes open and she lay down on her bed and knew nothing more for a long time.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: The outbreak was cholera.

**Codex annotation notes:** Holdout item: full owner review remains mandatory.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>sg094</strong> · contrastive_distractor · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** Did Mr. Craven close the garden because he had always disliked his wife?

**Proposed status:** `answered`

**Proposed reference answer:** No. Martha says he closed it after his wife died and that it had been her garden; later narration describes her eyes as ones he had adored.

**Book / difficulty:** `the_secret_garden` / `medium`

**Fact family:** `secret_garden_history`

**Evidence event:** `event_secret_garden_history`

**Development exposure:** `not_applicable_different_book`

**Exposure review:** Secret Garden is a separate-book holdout.

**Metamorphic / contrastive group:** `none` / `contrast_garden_history`

**Related cases:** `sg090`

**Tags:** `false_premise`, `negation`

### Required claims and original context

#### C1: Martha reports that he closed the garden after his wife’s sudden death and that it was her garden.

**Evidence E1 location:** `{"book": "the_secret_garden", "canonical_line": 1025, "chapter": null, "generated_pdf_pages": [15]}`

**Exact supporting span:**

```text
Mr. Craven had it shut when his wife died so sudden
```

**Preceding context:**

```text
“Why?” asked Mary in spite of herself. Here was another locked door added to the hundred in the strange house.
```

**Supporting paragraph/context:**

```text
“Mr. Craven had it shut when his wife died so sudden. He won’t let no one go inside. It was her garden. He locked th’ door an’ dug a hole and buried th’ key. There’s Mrs. Medlock’s bell ringing—I must run.”
```

**Following context:**

```text
After she was gone Mary turned down the walk which led to the door in the shrubbery. She could not help thinking about the garden which no one had been into for ten years. She wondered what it would look like and whether there were any flowers still alive in it. When she had passed through the shrubbery gate she found herself in great gardens, with wide lawns and winding walks with clipped borders. There were trees, and flower-beds, and evergreens clipped into strange shapes, and a large pool with an old gray fountain in its midst. But the flower-beds were bare and wintry and the fountain was not playing. This was not the garden which was shut up. How could a garden be shut up? You could always walk into a garden.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Martha reports that he closed the garden after his wife’s sudden death and that it was her garden.

#### C2: Later narration says he had adored his wife’s eyes, contradicting the premise that he had always disliked her.

**Evidence E2 location:** `{"book": "the_secret_garden", "canonical_line": 9164, "chapter": null, "generated_pdf_pages": [133]}`

**Exact supporting span:**

```text
the happy eyes he had adored
```

**Preceding context:**

```text
In a few days he was in Yorkshire again, and on his long railroad journey he found himself thinking of his boy as he had never thought in all the ten years past. During those years he had only wished to forget him. Now, though he did not intend to think about him, memories of him constantly drifted into his mind. He remembered the black days when he had raved like a madman because the child was alive and the mother was dead. He had refused to see it, and when he had gone to look at it at last it had been, such a weak wretched thing that everyone had been sure it would die in a few days. But to the surprise of those who took care of it the days passed and it lived and then everyone believed it would be a deformed and crippled creature.
```

**Supporting paragraph/context:**

```text
He had not meant to be a bad father, but he had not felt like a father at all. He had supplied doctors and nurses and luxuries, but he had shrunk from the mere thought of the boy and had buried himself in his own misery. The first time after a year’s absence he returned to Misselthwaite and the small miserable looking thing languidly and indifferently lifted to his face the great gray eyes with black lashes round them, so like and yet so horribly unlike the happy eyes he had adored, he could not bear the sight of them and turned away pale as death. After that he scarcely ever saw him except when he was asleep, and all he knew of him was that he was a confirmed invalid, with a vicious, hysterical, half-insane temper. He could only be kept from furies dangerous to himself by being given his own way in every detail.
```

**Following context:**

```text
All this was not an uplifting thing to recall, but as the train whirled him through mountain passes and golden plains the man who was “coming alive” began to think in a new way and he thought long and steadily and deeply.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Later narration says he had adored his wife’s eyes, contradicting the premise that he had always disliked her.

**Codex annotation notes:** The prior evidence explained closure but did not refute ‘always disliked’; later narrator evidence now does. Holdout item: full owner review remains mandatory.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>sg095</strong> · contrastive_distractor · answered · DEEP_REVIEW — needs owner attention</summary>

**Question:** Was Colin Mr. Craven’s nephew, like Mary was his niece?

**Proposed status:** `answered`

**Proposed reference answer:** No. Colin was Mr. Craven’s son; Mary was his niece and therefore Colin’s cousin.

**Book / difficulty:** `the_secret_garden` / `medium`

**Fact family:** `secret_craven_relationship`

**Evidence event:** `event_secret_craven_relationship`

**Development exposure:** `not_applicable_different_book`

**Exposure review:** Secret Garden is a separate-book holdout.

**Metamorphic / contrastive group:** `none` / `contrast_craven_relationship`

**Related cases:** `sg087`

**Tags:** `relationship_reversal`

### Required claims and original context

#### C1: Mary identifies Mr. Craven as her uncle, so she is his niece.

**Evidence E1 location:** `{"book": "the_secret_garden", "canonical_line": 3973, "chapter": null, "generated_pdf_pages": [58]}`

**Exact supporting span:**

```text
Mr. Craven is my uncle
```

**Preceding context:**

```text
“I am Colin Craven. Who are you?”
```

**Supporting paragraph/context:**

```text
“I am Mary Lennox. Mr. Craven is my uncle.”
```

**Following context:**

```text
“He is my father,” said the boy.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Mary identifies Mr. Craven as her uncle, so she is his niece.

#### C2: Colin identifies Mr. Craven as his father, so Colin is his son rather than nephew and is Mary’s cousin.

**Evidence E2 location:** `{"book": "the_secret_garden", "canonical_line": 3975, "chapter": null, "generated_pdf_pages": [58]}`

**Exact supporting span:**

```text
He is my father
```

**Preceding context:**

```text
“I am Mary Lennox. Mr. Craven is my uncle.”
```

**Supporting paragraph/context:**

```text
“He is my father,” said the boy.
```

**Following context:**

```text
“Your father!” gasped Mary. “No one ever told me he had a boy! Why didn’t they?”
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Colin identifies Mr. Craven as his father, so Colin is his son rather than nephew and is Mary’s cousin.

**Codex annotation notes:** The repaired claims now cover every relation stated in the reference answer. Holdout item: full owner review remains mandatory.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>sg098</strong> · ambiguous_underspecified · ambiguous · DEEP_REVIEW — needs owner attention</summary>

**Question:** What did Mary see when a covering moved aside?

**Proposed status:** `ambiguous`

**Proposed reference answer:** Clarification is required: moving ivy exposed a door knob, while drawing back the silk curtain uncovered a picture of Colin’s mother.

**Book / difficulty:** `the_secret_garden` / `medium`

**Fact family:** `fact_sg098`

**Evidence event:** `event_fact_sg098`

**Development exposure:** `not_applicable_different_book`

**Exposure review:** Secret Garden is a separate-book holdout.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `ambiguity`

### Ambiguity rationale

**Type:** `book_dependent_multiple_referents`

Two separate scenes involve a covering moving aside: ivy reveals a door knob, while a silk curtain reveals a portrait.

**Minimal clarification:** Do you mean the ivy in the garden or the silk curtain in Colin’s room?

**Plausible referent A2 — `{"book": "the_secret_garden", "canonical_line": 2319, "chapter": null, "generated_pdf_pages": [34]}`**

```text
One of the nice little gusts of wind rushed down the walk, and it was a stronger one than the rest. It was strong enough to wave the branches of the trees, and it was more than strong enough to sway the trailing sprays of untrimmed ivy hanging from the wall. Mary had stepped close to the robin, and suddenly the gust of wind swung aside some loose ivy trails, and more suddenly still she jumped toward it and caught it in her hand. This she did because she had seen something under it—a round knob which had been covered by the leaves hanging over it. It was the knob of a door.
```

**Plausible referent A3 — `{"book": "the_secret_garden", "canonical_line": 4297, "chapter": null, "generated_pdf_pages": [63]}`**

```text
Mary got up, much mystified, and found the cord. When she pulled it the silk curtain ran back on rings and when it ran back it uncovered a picture. It was the picture of a girl with a laughing face. She had bright hair tied up with a blue ribbon and her gay, lovely eyes were exactly like Colin’s unhappy ones, agate gray and looking twice as big as they really were because of the black lashes all round them.
```

**Codex annotation notes:** Repaired ambiguity: the former version incorrectly treated a curtain/portrait passage as a door discovery. The new wording is supported by two genuinely distinct uncovering events.

**Annotation confidence / review tier:** `medium` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>sg099</strong> · ambiguous_underspecified · ambiguous · DEEP_REVIEW — needs owner attention</summary>

**Question:** Why was Colin upset?

**Proposed status:** `ambiguous`

**Proposed reference answer:** The question needs the particular scene.

**Book / difficulty:** `the_secret_garden` / `medium`

**Fact family:** `fact_sg099`

**Evidence event:** `event_fact_sg099`

**Development exposure:** `not_applicable_different_book`

**Exposure review:** Secret Garden is a separate-book holdout.

**Metamorphic / contrastive group:** `none` / `none`

**Related cases:** _none_

**Tags:** `ambiguity`

### Ambiguity rationale

**Type:** `book_dependent_multiple_events`

Colin becomes upset for different reasons in several scenes, including secrecy, illness fears, and conflict with Mary.

**Minimal clarification:** Which Colin scene or outburst do you mean?

**Plausible referent A1 — `{"book": "the_secret_garden", "canonical_line": 4309, "chapter": null, "generated_pdf_pages": [63]}`**

```text
“If she had lived I believe I should not have been ill always,” he grumbled. “I dare say I should have lived, too. And my father would not have hated to look at me. I dare say I should have had a strong back. Draw the curtain again.”
```

**Plausible referent A2 — `{"book": "the_secret_garden", "canonical_line": 5410, "chapter": null, "generated_pdf_pages": [78]}`**

```text
They were a nice agreeable pair as they glared at each other. If they had been two little street boys they would have sprung at each other and had a rough-and-tumble fight. As it was, they did the next thing to it.
```

**Plausible referent A3 — `{"book": "the_secret_garden", "canonical_line": 5196, "chapter": null, "generated_pdf_pages": [75]}`**

```text
“Colin’s so afraid of it himself that he won’t sit up,” said Mary. “He says he’s always thinking that if he should feel a lump coming he should go crazy and scream himself to death.”
```

**Codex annotation notes:** Holdout item: full owner review remains mandatory. Speech-vs-narration epistemic labels were separated for the three distinct upset scenes.

**Annotation confidence / review tier:** `needs_owner_review` / `DEEP_REVIEW`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>

<details>
<summary><strong>sg100</strong> · voice_like_noisy_text · answered · FAST_CONFIRM — needs owner attention</summary>

**Question:** Um, what was the place Mary got sent to live called?

**Proposed status:** `answered`

**Proposed reference answer:** Misselthwaite Manor.

**Book / difficulty:** `the_secret_garden` / `medium`

**Fact family:** `secret_manor_destination`

**Evidence event:** `event_secret_manor_destination`

**Development exposure:** `not_applicable_different_book`

**Exposure review:** Secret Garden is a separate-book holdout.

**Metamorphic / contrastive group:** `meta_secret_destination` / `none`

**Related cases:** `sg082`

**Tags:** `metamorphic`, `voice_like`

### Required claims and original context

#### C1: Mary was sent to Misselthwaite Manor.

**Evidence E1 location:** `{"book": "the_secret_garden", "canonical_line": 49, "chapter": null, "generated_pdf_pages": [1]}`

**Exact supporting span:**

```text
sent to Misselthwaite Manor to live with her uncle
```

**Preceding context:**

```text
CHAPTER I. THERE IS NO ONE LEFT
```

**Supporting paragraph/context:**

```text
When Mary Lennox was sent to Misselthwaite Manor to live with her uncle everybody said she was the most disagreeable-looking child ever seen. It was true, too. She had a little thin face and a little thin body, thin light hair and a sour expression. Her hair was yellow, and her face was yellow because she had been born in India and had always been ill in one way or another. Her father had held a position under the English Government and had always been busy and ill himself, and her mother had been a great beauty who cared only to go to parties and amuse herself with gay people. She had not wanted a little girl at all, and when Mary was born she handed her over to the care of an Ayah, who was made to understand that if she wished to please the Mem Sahib she must keep the child out of sight as much as possible. So when she was a sickly, fretful, ugly little baby she was kept out of the way, and when she became a sickly, fretful, toddling thing she was kept out of the way also. She never remembered seeing familiarly anything but the dark faces of her Ayah and the other native servants, and as they always obeyed her and gave her her own way in everything, because the Mem Sahib would be angry if she was disturbed by her crying, by the time she was six years old she was as tyrannical and selfish a little pig as ever lived. The young English governess who came to teach her to read and write disliked her so much that she gave up her place in three months, and when other governesses came to try to fill it they always went away in a shorter time than the first one. So if Mary had not chosen to really want to know how to read books she would never have learned her letters at all.
```

**Following context:**

```text
One frightfully hot morning, when she was about nine years old, she awakened feeling very cross, and she became crosser still when she saw that the servant who stood by her bedside was not her Ayah.
```

**Context incomplete:** `false`

**Why it supports this claim:** The cited span and its adjacent discourse support: Mary was sent to Misselthwaite Manor.

**Codex annotation notes:** Holdout item: full owner review remains mandatory.

**Annotation confidence / review tier:** `high` / `FAST_CONFIRM`

Owner ground-truth decision:  
[ ] APPROVE  
[ ] EDIT  
[ ] REJECT  

Owner note:

</details>
