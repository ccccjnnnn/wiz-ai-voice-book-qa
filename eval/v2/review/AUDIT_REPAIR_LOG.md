# Evaluation V2 independent audit and repair log

## Status and method

This is an offline source audit of a **candidate** dataset. Astra findings were treated as hypotheses. Each verdict below was reached by checking the exact Alice PDF or the pinned Project Gutenberg *Secret Garden* text, then checking the locally generated PDF only as parser-coverage evidence. No retrieval, QA model, or external provider was run.

Verdicts mean:

- **CONFIRMED:** the reported defect materially affected correctness, independence, category, or reviewability.
- **PARTIALLY_CONFIRMED:** the answer fact was sound, but wording, evidence packaging, category, confidence, or representation handling needed repair.
- **REJECTED:** the source did not support the alleged semantic defect. Context packaging may still have been improved.

All quoted fragments below are exact source spans. Full preceding/supporting/following paragraphs and source locations are in `OWNER_GROUND_TRUTH_REVIEW.md`.

## Flagged annotation findings

| Case | Astra claim tested | Source inspected and exact relevant context | Verdict | Reasoning and action | Result |
|---|---|---|---|---|---|
| `q010` | The old question/answer had false chronology involving the Mouse. | Alice PDF pp. 20–21: “I must be Mabel after all”; “cause of this was the fan she was holding.” | **CONFIRMED** | Alice was thinking about Mabel and had not yet spoken to the Mouse. Rewrote the question and mapped the cause directly to the fan. | answered / direct factual / DEV |
| `q011` | French-Mouse reasoning was stated too categorically. | p. 23: “perhaps it doesn’t understand English”; “French mouse, come over with William the Conqueror.” | **PARTIALLY_CONFIRMED** | The causal answer was right, but it is Alice’s guess. Reference and claims now preserve uncertainty and speaker attribution. | answered / local context / DEV |
| `av057` | “Knave stole the tarts” treated an accusation as proven fact. | p. 79 charge: “The Knave of Hearts, he stole those tarts.” | **CONFIRMED** | This is the court accusation. Question/reference/claim now say “accused” and “alleged thief.” | answered / voice-like / DEV |
| `q027` | The first-figure answer was incomplete. | pp. 73–74: “change lobsters, and retire”; “throw the lobsters out to sea”; “turn a somersault”; “Back to land again.” | **CONFIRMED** | Added the omitted throw, swim, somersault, second change, and return steps with two evidence units. | answered / multi-source multi-fact / DEV |
| `q007` | The six-food answer or its support was unreliable. | p. 16: “mixed ﬂavour of cherry- tart, custard, pine-apple, roast turkey, toﬀee, and hot buttered toast.” | **PARTIALLY_CONFIRMED** | All six foods are correct. The defect was extraction-exact span spelling/line-hyphenation. Preserved the normalized answer and stored the literal extracted span. | answered / direct factual / DEV |
| `c005` | Multiple evidence IDs overstated independent breadth. | pp. 18 and 22: “more than nine feet high”; “about four inches deep.” | **CONFIRMED** | It genuinely needs two numeric facts on adjacent pages, but is a metamorphic restatement of `q009`, not independent coverage. Kept in DEV and linked by fact/metamorphic family. | answered / multi-source multi-fact / DEV |
| `q018` | The Pigeon’s belief was presented as narrator truth. | pp. 41–42: “trouble enough hatching the eggs”; “little girls eat eggs quite as much as serpents do.” | **CONFIRMED** | Reference and claims now identify this as the Pigeon’s conclusion. | answered / local context / DEV |
| `q023` | The causal chain for permanent tea-time was incomplete. | pp. 54–55: the Hatter says he quarreled with Time; “It’s always six o’clock now”; “it’s always tea-time.” | **CONFIRMED** | Added quarrel → Time refuses requests → six o’clock → tea-time. | answered / local context / DEV |
| `av055` | Voice variant was artificial and duplicated exposed facts. | p. 31: “fetch me a pair of gloves and a fan.” | **PARTIALLY_CONFIRMED** | Fact was correct. Rewrote as plausible punctuation-free speech and linked it to `q014/q015`; retained only as DEV voice robustness. | answered / voice-like / DEV |
| `q002` | It was mislabeled multi-source. | p. 6 contents line: “12 Alice’s Evidence.” | **PARTIALLY_CONFIRMED** | Both requested facts are explicit in one local unit. Consolidated duplicate evidence and made it direct factual. | answered / direct factual / DEV |
| `q013` | Prize case did not satisfy multi-source criteria. | pp. 27–28: comfits were “handed … round as prizes”; Alice accepted “this elegant thimble.” | **CONFIRMED** | The value is the local contrast between other racers’ comfits and Alice’s returned thimble. Reclassified as contrastive and linked its family. | answered / contrastive / DEV |
| `c006` | It duplicated the prize fact without adding breadth. | Same pp. 27–28 spans as `q013`. | **PARTIALLY_CONFIRMED** | It remains a useful relation/wording variant, but is explicitly linked to the same metamorphic/contrastive family and is not counted as independent breadth. | answered / contrastive / DEV |
| `av044` | One exact span was a broken extraction fragment. | p. 28: Alice “took the thimble.” | **CONFIRMED** | Replaced the line-broken span with a literal supporting span and retained the case as a contrastive DEV member. | answered / contrastive / DEV |
| `q022` | Multiple evidence IDs were mistaken for multi-source evidence. | p. 52: tea-party participants; “There isn’t any” wine. | **CONFIRMED** | Resolution depends on one continuous dialogue and negation. Reclassified to local-context reasoning. | answered / local context / DEV |
| `q026` | The school-subject answer omitted the later list. | pp. 71–72: “Reeling and Writhing”; “Mystery, ancient and modern, with Seaography,” followed by the later subjects. | **CONFIRMED** | Expanded the reference and material claims to cover the complete two-page curriculum. | answered / multi-source multi-fact / DEV |
| `sg085` | The causal answer over-attributed Mary’s abandonment to her parents’ deaths. | canonical line 227 onward: cholera panic; “the few native servants who had not died also had left the house.” | **PARTIALLY_CONFIRMED** | Parents’ deaths alone are insufficient. Reference now says Mary was forgotten amid the outbreak and the survivors fled without remembering her. | answered / multi-source multi-fact / holdout |
| `sg086` | Garden-access evidence was duplicated/incomplete. | lines 2053, 2319, 2338: buried key; wind moved ivy; key fitted the keyhole. | **CONFIRMED** | Consolidated three distinct access steps and mapped each to canonical line plus generated-PDF page. | answered / multi-source multi-fact / holdout |
| `sg087` | Cousin relation was mislabeled distributed multi-source. | “Mr. Craven is my uncle”; Colin: “He is my father.” | **CONFIRMED** | The relation is inferred inside one continuous exchange. Reclassified to local-context reasoning and mapped both speakers. | answered / local context / holdout |
| `sg094` | Evidence explained closure but did not refute “always disliked.” | line 1025: “had it shut when his wife died”; later narration: “the happy eyes he had adored.” | **CONFIRMED** | Added independent narrator evidence that directly contradicts the false premise. | answered / contrastive / holdout |
| `sg095` | Required claims did not cover every relationship in the reference. | “Mr. Craven is my uncle”; Colin: “He is my father.” | **PARTIALLY_CONFIRMED** | The answer was right. Claims now explicitly cover son, niece, and cousin relations. | answered / contrastive / holdout |
| `sg088` | Pronoun “he” might not resolve to Mr. Craven. | Mrs. Medlock first discusses “Mr. Craven”; then says “_He’s_ not going to trouble himself about you.” | **REJECTED** | Continuous dialogue gives one clear antecedent: Archibald Craven. Preserved the answer and supplied adjacent context. | answered / local context / holdout |
| `sg091` | Speaker of “The Magic is in me” might be misidentified. | Colin says, “Then I will chant”; the quoted chant follows. | **REJECTED** | The explicit speech tag establishes Colin as speaker and the line as dialogue. Preserved answer; packaged speaker context. | answered / local context / holdout |
| `sg092` | Ivy-hidden entrance conclusion was unsupported. | “gust of wind swung aside some loose ivy trails”; “It was the knob of a door”; Mary then unlocks the garden. | **REJECTED** | The continuous scene establishes the secret-garden entrance. Preserved the answer and linked it to `sg086` as a related family. | answered / paraphrase mismatch / holdout |
| `at063` | Final TEST reused the Mary Ann/fan scene exposed by DEV. | p. 31: “Why, Mary Ann”; “took me for his housemaid.” DEV `q014/q015/av055` already expose the scene. | **CONFIRMED** | Removed from TEST and replaced by an independent candidate. | removed; replacement `at101–at116` set retains 20 TEST cases |
| `at070` | Final TEST answer-bearing context was already visible in DEV. | p. 62: “She boxed the Queen’s ears.” The same page/context is exposed by DEV croquet annotations. | **CONFIRMED** | Removed conservatively rather than claiming independent TEST breadth. | removed and replaced |
| `at071` | Final TEST was a paraphrase of exposed Caucus-race evidence. | p. 26: “best thing to get us dry would be a Caucus-race”; DEV `q012` exposes the fact. | **CONFIRMED** | Removed and replaced. | removed and replaced |

## Alice DEV / final TEST semantic leakage audit

Leakage was defined by answer fact, scene, answer-bearing passage, entity/relation, and any evidence already exposed in DEV answers, negative-search snippets, or ambiguity evidence. String similarity was not used as the decision rule.

| Removed TEST ID(s) | DEV exposure independently confirmed | Decision |
|---|---|---|
| `at061`, `at065`, `at066` | `q028`, `av057`, and `av046` expose the Knave/charge/name scene and relations. | Remove all three. |
| `at063` | `q014`, `q015`, `av055` expose the Mary Ann/gloves/fan scene. | Remove. |
| `at064` | `q006` plus `av053` context expose the relevant card/garden scene. | Remove. |
| `at067` | `q009`, `c005`, `av052`, `av056`, and `av046` expose the height/pool/Rabbit neighborhood. | Remove. |
| `at070` | `q024`/`av042` evidence exposes the same croquet-page discourse containing the answer. | Remove. |
| `at071` | `q012` exposes the Caucus-race remedy. | Remove. |
| `at072` | `q024`/`av042` expose the same croquet equipment fact. | Remove. |
| `at074`, `at080` | `q030` exposes the underlying trial fact family. | Remove. |
| `at077` | DEV tea, croquet, and trial evidence (`q023`, `av037`, `q024`, `av042`, `q029`, `av040`, `av060`) makes the ambiguity alternatives development-visible. | Remove. |
| `at078` | `q012`, `q024`, `av042`, and `av046` expose its plausible referents/context. | Remove. |
| `at079` | `q005` exposes the same fact; noisy wording does not create TEST independence. | Remove. |
| `at062`, `at069` | Additional page/evidence-family audit found development-exposed scene context even though these were not in the initial short list. | Remove conservatively. |

Sixteen cases were replaced: `at061`, `at062`, `at063`, `at064`, `at065`, `at066`, `at067`, `at069`, `at070`, `at071`, `at072`, `at074`, `at077`, `at078`, `at079`, `at080`. No case moved between splits. Four independently verified original TEST cases remain: `at068`, `at073`, `at075`, `at076`. New candidates `at101–at116` use TEST-only fact-family IDs; the validator rejects any Alice TEST family shared with DEV. These candidates have not been run.

## Ambiguity audit

| Case | Exact source/context check | Verdict and action |
|---|---|---|
| `c003` | Distinct shrinking/growing scenes at pp. 16, 21, and 42. | **CONFIRMED** multiple events; recorded three representative events. |
| `c004` | “What happened next?” supplies no prior conversational event. | **CONFIRMED** missing conversational referent; no book evidence needed. |
| `av050` | “swallowed one of the cakes” versus “nibbling first at one and then at the other.” | **CONFIRMED** after repair to “a small piece”; asks cake vs mushroom and which side. |
| `av051` | Separate anger/rudeness moments in the tea-party scene. | **CONFIRMED** multiple events; two contexts retained. |
| `av052` | The Rabbit leaves/moves in more than one distinct scene. | **CONFIRMED** multiple events; two contexts retained. |
| `av053` | Card gardeners “threw themselves flat” versus “the whole pack rose up.” | **CONFIRMED** after repair to “What happened to the cards?”; two genuine card referents/events. |
| `at116` | Alice rejects claimed proof on p. 89 and sentence-before-verdict on p. 91. | **CONFIRMED** new TEST ambiguity with two independently sourced objections. |
| `sg098` | Manor’s many doors, ivy-covered garden door, and curtained Colin-room door are distinct. | **CONFIRMED** multiple door referents; three contexts retained. |
| `sg099` | Colin is upset about his father, quarrels with Mary, and fears illness in distinct scenes. | **CONFIRMED** multiple events; three contexts retained. |

Every ambiguity now has `ambiguity_type`, at least two `plausible_referents` for book-dependent ambiguity, and source context for each plausible event. Broad questions without a necessary missing referent were not labeled ambiguous.

## Whole-document negative verification audit

All ten negative candidates (`c001`, `c002`, `av046`, `av047`, `av048`, `av049`, `at075`, `at076`, `sg096`, `sg097`) now record entity aliases, relation vocabulary, morphology, semantic paraphrases, plausible counterexamples, match disposition, exact scope, and a bounded conclusion. Regex hits are inputs to human semantic review, not proof of absence. Alice checks are scoped to the exact evaluation PDF. Secret Garden checks use canonical text as semantic truth and the generated PDF as parser-coverage validation.

The two old TEST negatives (`at075`, `at076`) were retained because their White Rabbit age and King personal-name facts are not exposed as answered DEV facts; their potentially confusing age/name matches were explicitly reviewed. The conclusion in every negative case is: no supporting evidence was found after targeted whole-document verification. It does not claim mathematical absence.

## Secret Garden holdout inspection

| Case | Source-backed finding | Verdict/action |
|---|---|---|
| `sg081` | “born in India.” | Direct fact confirmed; PDF page mapped. |
| `sg082` | “sent to Misselthwaite Manor.” | Direct fact confirmed; linked to voice variant `sg100`. |
| `sg083` | “Susan Sowerby”; Mary wishes she were her mother “as well as Dickon’s.” | Name/relation confirmed with two contexts. |
| `sg084` | “near a hundred rooms.” | Approximate count retained as approximate. |
| `sg085` | Cholera panic plus surviving servants’ flight. | Causal wording repaired; related to `sg089/sg093`. |
| `sg086` | Buried key, ivy-revealed door, fitting lock. | Three-step evidence repaired; linked to `sg092`. |
| `sg087` | “Mr. Craven is my uncle”; “He is my father.” | Cousin inference and category repaired; linked to `sg095`. |
| `sg088` | Prior explicit Mr. Craven mention resolves “He.” | Astra semantic concern rejected; context expanded. |
| `sg089` | Narration names Barney before “There is nobody left to come.” | Speaker attribution confirmed. |
| `sg090` | Wife’s death immediately precedes “It was her garden.” | Pronoun/possessor resolved; linked to `sg094`. |
| `sg091` | “Then I will chant,” said by Colin before the chant. | Speaker/dialogue annotation confirmed. |
| `sg092` | Wind moves ivy and reveals a door knob in the access scene. | Entrance conclusion confirmed; linked to `sg086`. |
| `sg093` | “The cholera had broken out.” | Epidemic fact confirmed; linked to `sg085/sg089`. |
| `sg094` | Closure report plus narrator’s “eyes he had adored.” | False premise now directly refuted; linked to `sg090`. |
| `sg095` | Uncle/father statements imply niece/son/cousin. | Claim/reference alignment repaired; linked to `sg087`. |
| `sg096` | Archibald aliases and birth/age variants reviewed; matches concern other people/events. | Negative plan strengthened; bounded no-support conclusion. |
| `sg097` | Dickon/Sowerby aliases, home/cottage/road/address variants reviewed. | Cottage/moor is not an exact street address; bounded conclusion. |
| `sg098` | Three materially different doors. | Ambiguity evidence repaired. |
| `sg099` | Three materially different upsetting events. | Ambiguity evidence repaired. |
| `sg100` | Spoken variant of “sent to Misselthwaite Manor.” | Retained as a deliberate holdout voice/metamorphic pair, not independent breadth. |

All twenty holdout cases now have canonical locations and generated-PDF page mappings where positive/ambiguity evidence exists. Related families are explicit and are counted once when assessing broad fact coverage.

## Canonical/PDF representation reconciliation

**Astra claim:** unequal `sg096` regex hits, superficially equal `sg097` counts, and extracted `·` glyphs showed that word counts alone could not establish representation equivalence.

**Verdict: PARTIALLY_CONFIRMED.** The representation problem was real: the base PDF font collapsed several Unicode punctuation characters, so raw regex-hit equality was not a valid contract. It did not establish semantic content loss.

The generator now maps curly quotes, dashes, ellipsis, and non-breaking space deterministically before PDF creation. Both representations are normalized with NFKD, case-folded, and compared as ordered alphanumeric token sequences. Final result:

- canonical semantic source: Project Gutenberg eBook #113, SHA-256 `6b0bb5fbd0c4e873d2d22028da9d753cf3977d5f70ac58221556b28060badbf5`;
- generated PDF: parser coverage only, SHA-256 `499f246e4f1ecbe265d8c942f39d4c9825cd4d8e08dc8c1a7e8d2b6c49c9561e`;
- 83,165 canonical tokens and 83,165 extracted tokens after the shared `œ → oe` compatibility mapping;
- exact ordered-token sequence equality;
- zero missing/extra token spans;
- 27 canonical and 27 extracted chapter headings;
- zero empty PDF pages;
- no semantic content loss detected.

No unsupported middle-dot glyph remains after regeneration. Raw punctuation and regex-hit counts remain diagnostic observations, not semantic equivalence criteria. See `eval/v2/sources/source_consistency_report.json`.

## Final repair accounting

- Annotation/category/negative/ambiguity cases explicitly repaired: `av044`, `av046`, `av047`, `av048`, `av049`, `av050`, `av051`, `av052`, `av053`, `av055`, `av057`, `at075`, `at076`, `c001`, `c002`, `c003`, `c004`, `c005`, `c006`, `q002`, `q007`, `q010`, `q011`, `q013`, `q018`, `q022`, `q023`, `q026`, `q027`, `sg085`, `sg086`, `sg087`, `sg094`, `sg095`, `sg096`, `sg097`, `sg098`, `sg099`.
- Evidence context was repackaged for all 100 candidates using preceding/supporting/following local units where available.
- Replaced TEST cases: 16 removed IDs and 16 new IDs `at101–at116`.
- Cases moved between splits: none.
- Review tiers: 38 `FAST_CONFIRM`, 62 `DEEP_REVIEW`, 0 `BLOCKED`.
- Owner approval remains incomplete. Nothing is frozen or executed.

## Final targeted Alice TEST semantic-independence repair

The second Astra audit's remaining Alice TEST concerns were adjudicated against
all development-visible material: answer evidence, local context, negative
search excerpts, ambiguity evidence, metamorphic/contrastive variants, and the
underlying event or relation even when IDs differed.

| Case | Verdict | Decision |
|---|---|---|
| `at101` | **CONFIRMED strong exposure** | Removed. Its Lory answer/event was already visible through DEV negative-search material. |
| `at107` | **CONFIRMED strong exposure** | Removed. The callback/advice event was exposed by DEV context, even where the excerpt was truncated. |
| `at111` | **CONFIRMED strong exposure** | Removed. The threat and resulting outcome were directly represented in DEV evidence. |
| `at116` | **CONFIRMED strong exposure** | Removed. The trial challenge/aftermath relation was exposed across DEV cases and surrounding context. |
| `at103` | **CONFIRMED partial exposure** | Removed conservatively. The Dinah/birds event was visible through DEV surrounding and negative-search text. |
| `at105` | **CONFIRMED partial exposure** | Removed conservatively. The Rabbit-house/Bill aftermath event overlapped DEV evidence and context. |
| `at108` | **CONFIRMED partial exposure** | Removed conservatively. The Cheshire Cat direction exchange was already represented in DEV. |

The seven cases were replaced by independent Alice TEST cases `at117` through
`at123`. They use distinct fact families and evidence events, with no DEV
sources declared in their exposure records. The replacement facts were checked
against the local Alice source and packaged with page, block, exact span, and
surrounding context. No case moved to DEV; the Alice TEST split remains 20.

The validator now rejects the seven known exposed IDs, shared DEV/TEST event
IDs, and exact supporting spans that occur in DEV-visible material. This is a
deterministic guardrail, not a claim that string checks discover every semantic
relationship; the event-level adjudication above remains part of owner review.

<!-- CHECKPOINT_C_CLEANUP_START -->
## Checkpoint C — negative / ambiguity / provenance / metadata cleanup

- Bounded negative verification retained for `c001`, `c002`, `av048`, `at075`, `sg096`, `sg097`; absolute absence is not claimed.
- Secret Garden negative cases now rely on canonical Gutenberg text for semantics; rebuild-specific generated-PDF match excerpts are not embedded in case annotations. Current PDF coverage/hash remains in `source_consistency_report.json`.
- `av052` was not a defensible ambiguity case because both evidence entries duplicated the same Rabbit event; it was converted to a grounded answered local-context case.
- `av053` stale garden-related plausible-referent metadata was corrected to the card gardeners vs whole pack.
- `sg098` was repaired so the ambiguity is ivy/door-knob vs silk-curtain/portrait rather than misusing the portrait scene as a door discovery.
- `av050`, `av051`, `sg099` received speech-vs-narration epistemic cleanup.
- `q016`, `q024`, `q027`, `at106` were reclassified as multi-fact single-context; `q030` is direct factual single-source rather than contrastive.
- `at110` exact spans now contain the competing propositions themselves.
- Same-event relationships are explicit for `q018`↔`av039`, `q023`↔`av037`, `q028`↔`av057`; fact-family count must not be described as a count of independent events.

Remaining non-dataset follow-ups for final delta review: `q014/q015` family-semantics wording and historical audit-log person/page wording.
<!-- CHECKPOINT_C_CLEANUP_END -->
