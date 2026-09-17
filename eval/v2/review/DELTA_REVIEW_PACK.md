# V2 DELTA REVIEW PACK

Purpose: independent final delta audit after Checkpoints A/B/C. This is NOT a full benchmark re-audit.

## Frozen current-state summary

- cases: 98
- splits: {'alice_dev_regression': 60, 'alice_final_test': 20, 'secret_garden_holdout': 18}
- statuses: {'answered': 83, 'insufficient_evidence': 8, 'ambiguous': 7}
- categories: {'local_context_reasoning': 20, 'paraphrase_vocabulary_mismatch': 7, 'contrastive_distractor': 9, 'unanswerable_false_premise': 8, 'ambiguous_underspecified': 7, 'voice_like_noisy_text': 9, 'multi_fact_single_context': 10, 'direct_factual_single_source': 23, 'multi_source_multi_fact': 5}
- review tiers: {'DEEP_REVIEW': 64, 'FAST_CONFIRM': 34}
- known Alice TEST development exposures: 0
- TEST / holdout executed: 0
- source consistency: PASS

Two low-value Secret Garden whole-document negatives, sg096 and sg097, were intentionally removed. Benchmark defensibility takes priority over maintaining an arbitrary round-number size.

## Reviewer instructions

Review only the cases below. Look specifically for: incorrect ground truth, speaker/narrator attribution, belief-vs-fact errors, insufficient local context, fake ambiguity, stale metadata, category inflation, shared-event/fact-family misrepresentation, or unsupported exact spans.

Do not recommend adding replacement questions merely to restore a count of 100. If a case remains materially dubious and low-value, recommend deletion.

For each issue, return: case_id, severity (BLOCKER / MATERIAL / MINOR), specific field(s), evidence for the issue, and the smallest defensible fix. Do not rescore or rank the whole benchmark.

---

## c001

```json
{
  "case_id": "c001",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "What was Alice's exact home street address?",
  "expected_status": "insufficient_evidence",
  "reference_answer": "No supporting evidence was found in the reviewed text of the exact evaluation book after targeted whole-document verification.",
  "required_answer_claims": [],
  "valid_evidence_locations": [],
  "exact_supporting_spans": [],
  "local_surrounding_context": [],
  "primary_category": "unanswerable_false_premise",
  "category": "unanswerable_false_premise",
  "tags": [
    "historical_case",
    "phase4_reuse",
    "whole_document_negative_check"
  ],
  "difficulty": "hard",
  "annotation_notes": "A plausible biographical detail that the story does not supply; tests refusal to fill a gap from world knowledge. Negative verification is bounded whole-document review, not mathematical proof of absence; absolute_absence_claimed remains false.",
  "annotation_confidence": "needs_owner_review",
  "historical_case": true,
  "requires_owner_attention": true,
  "negative_verification": {
    "entity_aliases": [
      "Alice",
      "Alice's home",
      "her house"
    ],
    "negative_search_terms": [
      "Alice street address",
      "home address",
      "postal address"
    ],
    "relation_variants": [
      "lives at",
      "resides at",
      "address is",
      "home in"
    ],
    "morphological_variants": [
      "address",
      "addresses",
      "addressed",
      "residence",
      "street"
    ],
    "semantic_variants": [
      "where exactly does Alice live",
      "house number and street"
    ],
    "plausible_counterexamples": [
      "The mock address to ALICE'S RIGHT FOOT",
      "mentions of Alice's home and Dinah"
    ],
    "counterexample_disposition": "The foot address is a joke addressed to her foot, and home references contain no street or house number.",
    "verification_scope": "complete text content of Alice PDF SHA-256 49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
    "source_coverage_status": "pass_with_documented_normalization",
    "searches": [
      {
        "query": "street/home address",
        "pattern": "\\b(?:street|home)\\s+address\\b",
        "canonical_or_parsed_source_matches": [],
        "generated_pdf_matches": null,
        "all_matches_reviewed": true,
        "semantic_assessment": "No direct address relation."
      },
      {
        "query": "address variants",
        "pattern": "\\baddress\\w*\\b",
        "canonical_or_parsed_source_matches": [
          {
            "location": "page 29",
            "excerpt": "ce of an oyster!’ ‘I wish I had our Dinah here, I know I do!’ said Alice aloud, addressing nobody in particular. ‘She’d soon fetch it back!’ ‘And who is Dinah, if I might venture to ask the question?’ said the"
          },
          {
            "location": "page 37",
            "excerpt": "time in silence: at last the Caterpillar took the hookah out of its mouth, and addressed her in a languid, sleepy voice. ‘Who are YOU?’ said the Caterpillar. This was not an encouraging opening for a conversa"
          },
          {
            "location": "page 45",
            "excerpt": "den violence that Alice quite jumped; but she saw in another moment that it was addressed to the baby, and not to her, so she took courage, and went on again:– ‘I didn’t know that Cheshire cats always grinned;"
          }
        ],
        "generated_pdf_matches": null,
        "all_matches_reviewed": true,
        "semantic_assessment": "Hits are speech verbs, not postal locations."
      },
      {
        "query": "street/residence",
        "pattern": "\\b(?:streets?|residence)\\b",
        "canonical_or_parsed_source_matches": [],
        "generated_pdf_matches": null,
        "all_matches_reviewed": true,
        "semantic_assessment": "No residential location is supplied."
      }
    ],
    "all_regex_matches_reviewed": true,
    "semantic_completeness_not_inferred_from_regex": true,
    "conclusion": "No supporting evidence was found in the reviewed book text after targeted whole-document verification.",
    "absolute_absence_claimed": false
  },
  "ambiguity_rationale": null,
  "expected_clarification": null,
  "evaluation_execution": null,
  "review_tier": "DEEP_REVIEW",
  "fact_family_id": "fact_c001",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [],
  "evidence_event_id": "event_fact_c001",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "c001"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## c002

```json
{
  "case_id": "c002",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "What was the Queen of Hearts' date of birth?",
  "expected_status": "insufficient_evidence",
  "reference_answer": "No supporting evidence was found in the reviewed text of the exact evaluation book after targeted whole-document verification.",
  "required_answer_claims": [],
  "valid_evidence_locations": [],
  "exact_supporting_spans": [],
  "local_surrounding_context": [],
  "primary_category": "unanswerable_false_premise",
  "category": "unanswerable_false_premise",
  "tags": [
    "historical_case",
    "phase4_reuse",
    "whole_document_negative_check"
  ],
  "difficulty": "hard",
  "annotation_notes": "Tests a confident-sounding unsupported request about a real character. Negative verification is bounded whole-document review, not mathematical proof of absence; absolute_absence_claimed remains false.",
  "annotation_confidence": "needs_owner_review",
  "historical_case": true,
  "requires_owner_attention": true,
  "negative_verification": {
    "entity_aliases": [
      "Queen of Hearts",
      "Queen",
      "her Majesty"
    ],
    "negative_search_terms": [
      "Queen date of birth",
      "Queen birthday",
      "Queen age"
    ],
    "relation_variants": [
      "was born",
      "birthday is",
      "years old",
      "age of the Queen"
    ],
    "morphological_variants": [
      "born",
      "birth",
      "birthday",
      "age",
      "aged"
    ],
    "semantic_variants": [
      "when was the Queen born",
      "how old is the Queen"
    ],
    "plausible_counterexamples": [
      "birthday-present discussion",
      "ages of Alice/Lory",
      "edition years in the PDF front matter"
    ],
    "counterexample_disposition": "None relates a birth date or age to the Queen of Hearts; front-matter years are not story chronology.",
    "verification_scope": "complete text content of Alice PDF SHA-256 49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
    "source_coverage_status": "pass_with_documented_normalization",
    "searches": [
      {
        "query": "birth-date variants",
        "pattern": "\\b(?:date of birth|birth date|born)\\b",
        "canonical_or_parsed_source_matches": [],
        "generated_pdf_matches": null,
        "all_matches_reviewed": true,
        "semantic_assessment": "No birth-date assertion."
      },
      {
        "query": "birthday/age",
        "pattern": "\\b(?:birthday|age|years? old)\\b",
        "canonical_or_parsed_source_matches": [
          {
            "location": "page 20",
            "excerpt": "e!’ And she began thinking over all the children she knew that were of the same age as herself, to see if she could have been changed for any of them. ‘I’m sure I’m not Ada,’ she said, ‘for her hair goe"
          },
          {
            "location": "page 25",
            "excerpt": "without knowing how old it was, and, as the Lory positively refused to tell its age, there was no more to be said. At last the Mouse, who seemed to be a person of authority among them, called out, ‘Sit d"
          },
          {
            "location": "page 38",
            "excerpt": "e very white; And yet you incessantly stand on your head– Do you think, at your age, it is right?’ ‘In my youth,’ Father William replied to his son, ‘I feared it might injure the brain; But, now that I’"
          },
          {
            "location": "page 69",
            "excerpt": "‘A cheap sort of present!’ thought Alice. ‘I’m glad they don’t give birthday presents like that!’ But she did not venture to say it out loud. ‘Thinking again?’ the Duchess asked, with another dig"
          },
          {
            "location": "page 81",
            "excerpt": "roud of it: for she thought, and rightly too, that very few little girls of her age knew the meaning of it at all. However, ‘jury-men’ would have done just as well. The twelve jurors were all writing ver"
          }
        ],
        "generated_pdf_matches": null,
        "all_matches_reviewed": true,
        "semantic_assessment": "Hits concern other people or birthday presents, not the Queen’s birth date."
      },
      {
        "query": "Queen of Hearts",
        "pattern": "\\bQueen of Hearts\\b",
        "canonical_or_parsed_source_matches": [
          {
            "location": "page 53",
            "excerpt": "th his tea spoon at the March Hare,) ‘–it was at the great concert given by the Queen of Hearts, and I had to sing “Twinkle, twinkle, little bat!"
          },
          {
            "location": "page 60",
            "excerpt": "imson velvet cushion; and, last of all this grand procession, came THE KING AND QUEEN OF HEARTS. Alice was rather doubtful whether she ought not to lie down on her face like the three gardeners, but she could not re"
          },
          {
            "location": "page 81",
            "excerpt": "Chapter 11 Who Stole the Tarts? The King and Queen of Hearts were seated on their throne when they arrived, with a great crowd assembled about them–all sorts of little birds and be"
          },
          {
            "location": "page 82",
            "excerpt": "he trumpet, and then unrolled the parchment scroll, and read as follows:– ‘The Queen of Hearts, she made some tarts, All on a summer day: The Knave of Hearts, he stole those tarts, And took them quite away!’ ‘Cons"
          }
        ],
        "generated_pdf_matches": null,
        "all_matches_reviewed": true,
        "semantic_assessment": "Entity scenes do not supply a birth date."
      }
    ],
    "all_regex_matches_reviewed": true,
    "semantic_completeness_not_inferred_from_regex": true,
    "conclusion": "No supporting evidence was found in the reviewed book text after targeted whole-document verification.",
    "absolute_absence_claimed": false
  },
  "ambiguity_rationale": null,
  "expected_clarification": null,
  "evaluation_execution": null,
  "review_tier": "DEEP_REVIEW",
  "fact_family_id": "fact_c002",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [],
  "evidence_event_id": "event_fact_c002",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "c002"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## av048

```json
{
  "case_id": "av048",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "In what exact calendar year do the Wonderland events occur?",
  "expected_status": "insufficient_evidence",
  "reference_answer": "No supporting evidence was found in the reviewed text of the exact evaluation book after targeted whole-document verification.",
  "required_answer_claims": [],
  "valid_evidence_locations": [],
  "exact_supporting_spans": [],
  "local_surrounding_context": [],
  "primary_category": "unanswerable_false_premise",
  "category": "unanswerable_false_premise",
  "tags": [
    "whole_document_negative_check"
  ],
  "difficulty": "hard",
  "annotation_notes": "Negative verification is bounded whole-document review, not mathematical proof of absence; absolute_absence_claimed remains false.",
  "annotation_confidence": "needs_owner_review",
  "historical_case": false,
  "requires_owner_attention": true,
  "negative_verification": {
    "entity_aliases": [
      "Alice",
      "Wonderland",
      "the events",
      "that day"
    ],
    "negative_search_terms": [
      "calendar year",
      "in 18xx",
      "in 19xx",
      "year of the story"
    ],
    "relation_variants": [
      "events occurred in",
      "year was",
      "dated"
    ],
    "morphological_variants": [
      "year",
      "years",
      "date",
      "dated"
    ],
    "semantic_variants": [
      "when exactly does the story take place"
    ],
    "plausible_counterexamples": [
      "Project Gutenberg release/copyright years in front matter",
      "story-relative references such as yesterday"
    ],
    "counterexample_disposition": "Metadata years describe the electronic edition, while story-relative time does not identify a calendar year.",
    "verification_scope": "complete text content of Alice PDF SHA-256 49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
    "source_coverage_status": "pass_with_documented_normalization",
    "searches": [
      {
        "query": "four-digit years",
        "pattern": "\\b(?:17|18|19|20)\\d{2}\\b",
        "canonical_or_parsed_source_matches": [
          {
            "location": "page 2",
            "excerpt": "Project Gutenberg Etext of Alice in Wonderland [Originally released in January, 1991] Copyright laws are changing all over the world, be sure to check the copyright laws for your country before posting th"
          },
          {
            "location": "page 2",
            "excerpt": "Vanilla Electronic Texts Etexts Readable By Both Humans and By Computers, Since 1971 These Etexts Prepared By Hundreds of Volunteers and Donations Information on contacting Project Gutenberg to get Etexts"
          },
          {
            "location": "page 4",
            "excerpt": "this year as we release thirty-six text files per month, or 432 more Etexts in 1999 for a total of 2000+. If these reach just 10total should reach over 200 billion Etexts given away this year. The Goal o"
          },
          {
            "location": "page 4",
            "excerpt": "ease thirty-six text files per month, or 432 more Etexts in 1999 for a total of 2000+. If these reach just 10total should reach over 200 billion Etexts given away this year. The Goal of Project Gutenberg"
          },
          {
            "location": "page 4",
            "excerpt": "l of Project Gutenberg is to Give Away One Trillion Etext Files by December 31, 2001. [10,000 x 100,000,000 = 1 Trillion] This is ten thousand titles each to one hundred million readers, which is only 5%"
          },
          {
            "location": "page 4",
            "excerpt": "ed rates of production, we will reach only one-third of that goal by the end of 2001, or about 3,333 Etexts unless we manage to get some real funding; currently our funding is mostly from Michael Hart’s s"
          },
          {
            "location": "page 9",
            "excerpt": "niversity”. We are planning on making some changes in our donation structure in 2000, so you might want to email me, hart@pobox.com beforehand. *END THE SMALL PRINT! FOR PUBLIC DOMAIN ETEXTS* Ver.04.29.93"
          }
        ],
        "generated_pdf_matches": null,
        "all_matches_reviewed": true,
        "semantic_assessment": "Numeric years occur in Gutenberg front matter, not the story chronology."
      },
      {
        "query": "year/date",
        "pattern": "\\b(?:year|date)\\b",
        "canonical_or_parsed_source_matches": [
          {
            "location": "page 3",
            "excerpt": "ght of the last day of the month of any such announcement. The official release date of all Project Gutenberg Etexts is at Midnight, Central Time, of the last day of the stated month. A preliminary versio"
          },
          {
            "location": "page 3",
            "excerpt": "n, comment and editing by those who wish to do so. To be sure you have an up to date first edition [xxxxx10x.xxx] please check file sizes in the first week of the next month. Since our ftp program has a b"
          },
          {
            "location": "page 3",
            "excerpt": "eek of the next month. Since our ftp program has a bug in it that scrambles the date [tried to fix and failed] a look at the file size will have to do, but we will try to see a new copy has at least one b"
          },
          {
            "location": "page 4",
            "excerpt": "inally estimated at one dollar then we produce $2 million dollars per hour this year as we release thirty-six text files per month, or 432 more Etexts in 1999 for a total of 2000+. If these reach just 10t"
          },
          {
            "location": "page 4",
            "excerpt": "f these reach just 10total should reach over 200 billion Etexts given away this year. The Goal of Project Gutenberg is to Give Away One Trillion Etext Files by December 31, 2001. [10,000 x 100,000,000 = 1"
          },
          {
            "location": "page 5",
            "excerpt": "get or mget [to get files. . . set bin for zip files] GET GUTINDEX.?? [to get a year’s listing of books, e.g., GUTINDEX.99] GET GUTINDEX.ALL [to get a listing of ALL books]"
          },
          {
            "location": "page 8",
            "excerpt": "nberg Association/Carnegie-Mellon University” within the 60 days following each date you prepare (or were legally required to prepare) your annual (or equivalent periodic) tax return."
          },
          {
            "location": "page 52",
            "excerpt": "ck it is!’ ‘Why should it?’ muttered the Hatter. ‘Does YOUR watch tell you what year it is?’ ‘Of course not,’ Alice replied very readily: ‘but that’s because it stays the same year for such a long time to"
          },
          {
            "location": "page 52",
            "excerpt": "course not,’ Alice replied very readily: ‘but that’s because it stays the same year for such a long time together.’"
          }
        ],
        "generated_pdf_matches": null,
        "all_matches_reviewed": true,
        "semantic_assessment": "Story hits do not establish a calendar year."
      }
    ],
    "all_regex_matches_reviewed": true,
    "semantic_completeness_not_inferred_from_regex": true,
    "conclusion": "No supporting evidence was found in the reviewed book text after targeted whole-document verification.",
    "absolute_absence_claimed": false
  },
  "ambiguity_rationale": null,
  "expected_clarification": null,
  "evaluation_execution": null,
  "review_tier": "DEEP_REVIEW",
  "fact_family_id": "fact_av048",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [],
  "evidence_event_id": "event_fact_av048",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "av048"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## at075

```json
{
  "case_id": "at075",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_final_test",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "How old was the White Rabbit?",
  "expected_status": "insufficient_evidence",
  "reference_answer": "No supporting evidence was found in the reviewed text of the exact evaluation book after targeted whole-document verification.",
  "required_answer_claims": [],
  "valid_evidence_locations": [],
  "exact_supporting_spans": [],
  "local_surrounding_context": [],
  "primary_category": "unanswerable_false_premise",
  "category": "unanswerable_false_premise",
  "tags": [
    "whole_document_negative_check"
  ],
  "difficulty": "hard",
  "annotation_notes": "Retained independent TEST negative about the White Rabbit’s age. Negative verification is bounded whole-document review, not mathematical proof of absence; absolute_absence_claimed remains false.",
  "annotation_confidence": "needs_owner_review",
  "historical_case": false,
  "requires_owner_attention": true,
  "negative_verification": {
    "entity_aliases": [
      "White Rabbit",
      "Rabbit",
      "herald"
    ],
    "negative_search_terms": [
      "White Rabbit age",
      "Rabbit years old",
      "old Rabbit"
    ],
    "relation_variants": [
      "was aged",
      "how old",
      "years of age",
      "born"
    ],
    "morphological_variants": [
      "age",
      "aged",
      "old",
      "older",
      "born"
    ],
    "semantic_variants": [
      "the Rabbit's numerical age"
    ],
    "plausible_counterexamples": [
      "Lory says it is older",
      "Father William poem",
      "Alice's age-related comparisons"
    ],
    "counterexample_disposition": "Age language concerns other characters and never supplies the White Rabbit's age.",
    "verification_scope": "complete text content of Alice PDF SHA-256 49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
    "source_coverage_status": "pass_with_documented_normalization",
    "searches": [
      {
        "query": "Rabbit-age relation",
        "pattern": "\\b(?:White Rabbit|Rabbit).{0,60}(?:age|years? old)\\b",
        "canonical_or_parsed_source_matches": [],
        "generated_pdf_matches": null,
        "all_matches_reviewed": true,
        "semantic_assessment": "No age assertion."
      },
      {
        "query": "age terms",
        "pattern": "\\b(?:age|years? old)\\b",
        "canonical_or_parsed_source_matches": [
          {
            "location": "page 20",
            "excerpt": "e!’ And she began thinking over all the children she knew that were of the same age as herself, to see if she could have been changed for any of them. ‘I’m sure I’m not Ada,’ she said, ‘for her hair goe"
          },
          {
            "location": "page 25",
            "excerpt": "without knowing how old it was, and, as the Lory positively refused to tell its age, there was no more to be said. At last the Mouse, who seemed to be a person of authority among them, called out, ‘Sit d"
          },
          {
            "location": "page 38",
            "excerpt": "e very white; And yet you incessantly stand on your head– Do you think, at your age, it is right?’ ‘In my youth,’ Father William replied to his son, ‘I feared it might injure the brain; But, now that I’"
          },
          {
            "location": "page 81",
            "excerpt": "roud of it: for she thought, and rightly too, that very few little girls of her age knew the meaning of it at all. However, ‘jury-men’ would have done just as well. The twelve jurors were all writing ver"
          }
        ],
        "generated_pdf_matches": null,
        "all_matches_reviewed": true,
        "semantic_assessment": "Hits concern other characters or general narration."
      }
    ],
    "all_regex_matches_reviewed": true,
    "semantic_completeness_not_inferred_from_regex": true,
    "conclusion": "No supporting evidence was found in the reviewed book text after targeted whole-document verification.",
    "absolute_absence_claimed": false
  },
  "ambiguity_rationale": null,
  "expected_clarification": null,
  "evaluation_execution": null,
  "review_tier": "DEEP_REVIEW",
  "fact_family_id": "fact_at075",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [],
  "evidence_event_id": "event_fact_at075",
  "development_exposure": {
    "status": "no_known_development_exposure",
    "sources": [],
    "review_method": "Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants."
  }
}
```

---

## av050

```json
{
  "case_id": "av050",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "What happened after Alice ate a small piece?",
  "expected_status": "ambiguous",
  "reference_answer": "Clarification is required because several small pieces cause different size changes.",
  "required_answer_claims": [],
  "valid_evidence_locations": [
    {
      "evidence_id": "E1",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 35,
        "chapter": "4",
        "pdf_block": 5
      },
      "exact_supporting_span": "she swallowed one of the cakes",
      "preceding_context": "Alice noticed with some surprise that the pebbles were all turning into little cakes as they lay on the ﬂoor, and a bright idea came into her head. ‘If I eat one of these cakes,’ she thought, ‘it’s sure to make SOME change in my size; and as it can’t possibly make me larger, it must make me smaller, I suppose.’",
      "supporting_context": "So she swallowed one of the cakes, and was delighted to ﬁnd that she began shrinking directly. As soon as she was small enough to get through the door, she ran out of the house, and found quite a crowd of little animals and birds waiting outside. The poor little Lizard, Bill, was in the middle, being held up by two guinea-pigs, who were giving it something out of a bottle. They all made a rush at Alice the moment she appeared; but she ran oﬀas hard as she could, and soon found herself safe in a thick wood.",
      "following_context": "‘The ﬁrst thing I’ve got to do,’ said Alice to herself, as she wandered about in the wood, ‘is to grow to my right size again; and the second thing is to ﬁnd my way into that lovely garden. I think that will be the best plan.’",
      "why_supports": "This passage establishes one plausible referent used to verify the ambiguity.",
      "epistemic_status": "narrator_fact",
      "context_incomplete": false
    },
    {
      "evidence_id": "E2",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 42,
        "chapter": "5",
        "pdf_block": 6
      },
      "exact_supporting_span": "nibbling first at one and then at the other",
      "preceding_context": "‘It matters a good deal to ME,’ said Alice hastily; ‘but I’m not looking for eggs, as it happens; and if I was, I shouldn’t want YOURS: I don’t like them raw.’",
      "supporting_context": "‘Well, be oﬀ, then!’ said the Pigeon in a sulky tone, as it settled down again into its nest. Alice crouched down among the trees as well as she could, for her neck kept getting entangled among the branches, and every now and then she had to stop and untwist it. After a while she remembered that she still held the pieces of mushroom in her hands, and she set to work very carefully, nibbling ﬁrst at one and then at the other, and growing sometimes taller and sometimes shorter, until she had succeeded in bringing herself down to her usual height.",
      "following_context": "It was so long since she had been anything near the right size, that it felt quite strange at ﬁrst; but she got used to it in a few minutes, and began talking to herself, as usual. ‘Come, there’s half my plan done now! How puzzling all these changes are! I’m never sure what I’m going to be, from one minute to another! However, I’ve got back to my right size: the next thing is, to get into that beautiful garden–how IS that to be done, I wonder?’ As she said this, she came suddenly upon an open place, with a little house in it about four feet high. ‘Whoever lives there,’ thought Alice, ‘it’ll never do to come upon them THIS size: why, I should frighten them out of their wits!’ So she began nibbling at the righthand bit again, and did not venture to go near the house till she had brought herself down to nine inches high.",
      "why_supports": "This passage establishes one plausible referent used to verify the ambiguity.",
      "epistemic_status": "narrator_fact",
      "context_incomplete": false
    }
  ],
  "exact_supporting_spans": [
    "she swallowed one of the cakes",
    "nibbling first at one and then at the other"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "E1",
      "preceding": "Alice noticed with some surprise that the pebbles were all turning into little cakes as they lay on the ﬂoor, and a bright idea came into her head. ‘If I eat one of these cakes,’ she thought, ‘it’s sure to make SOME change in my size; and as it can’t possibly make me larger, it must make me smaller, I suppose.’",
      "supporting": "So she swallowed one of the cakes, and was delighted to ﬁnd that she began shrinking directly. As soon as she was small enough to get through the door, she ran out of the house, and found quite a crowd of little animals and birds waiting outside. The poor little Lizard, Bill, was in the middle, being held up by two guinea-pigs, who were giving it something out of a bottle. They all made a rush at Alice the moment she appeared; but she ran oﬀas hard as she could, and soon found herself safe in a thick wood.",
      "following": "‘The ﬁrst thing I’ve got to do,’ said Alice to herself, as she wandered about in the wood, ‘is to grow to my right size again; and the second thing is to ﬁnd my way into that lovely garden. I think that will be the best plan.’",
      "context_incomplete": false
    },
    {
      "evidence_id": "E2",
      "preceding": "‘It matters a good deal to ME,’ said Alice hastily; ‘but I’m not looking for eggs, as it happens; and if I was, I shouldn’t want YOURS: I don’t like them raw.’",
      "supporting": "‘Well, be oﬀ, then!’ said the Pigeon in a sulky tone, as it settled down again into its nest. Alice crouched down among the trees as well as she could, for her neck kept getting entangled among the branches, and every now and then she had to stop and untwist it. After a while she remembered that she still held the pieces of mushroom in her hands, and she set to work very carefully, nibbling ﬁrst at one and then at the other, and growing sometimes taller and sometimes shorter, until she had succeeded in bringing herself down to her usual height.",
      "following": "It was so long since she had been anything near the right size, that it felt quite strange at ﬁrst; but she got used to it in a few minutes, and began talking to herself, as usual. ‘Come, there’s half my plan done now! How puzzling all these changes are! I’m never sure what I’m going to be, from one minute to another! However, I’ve got back to my right size: the next thing is, to get into that beautiful garden–how IS that to be done, I wonder?’ As she said this, she came suddenly upon an open place, with a little house in it about four feet high. ‘Whoever lives there,’ thought Alice, ‘it’ll never do to come upon them THIS size: why, I should frighten them out of their wits!’ So she began nibbling at the righthand bit again, and did not venture to go near the house till she had brought herself down to nine inches high.",
      "context_incomplete": false
    }
  ],
  "primary_category": "ambiguous_underspecified",
  "category": "ambiguous_underspecified",
  "tags": [
    "ambiguity"
  ],
  "difficulty": "medium",
  "annotation_notes": "Both candidate interpretations are distinct book events; mushroom-size change is narrator-described.",
  "annotation_confidence": "needs_owner_review",
  "historical_case": false,
  "requires_owner_attention": true,
  "negative_verification": null,
  "ambiguity_rationale": "A ‘small piece’ could mean a pebble-cake that makes Alice shrink or a piece from either side of the mushroom, whose effects differ.",
  "expected_clarification": "Do you mean a pebble-cake or a piece of the mushroom, and if the mushroom, which side?",
  "evaluation_execution": null,
  "ambiguity_type": "book_dependent_multiple_events",
  "plausible_referents": [
    "the pebble-cake that made Alice shrink",
    "a piece of mushroom that changed her height"
  ],
  "review_tier": "DEEP_REVIEW",
  "fact_family_id": "fact_av050",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [],
  "evidence_event_id": "event_fact_av050",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "av050"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## av051

```json
{
  "case_id": "av051",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "Why was Alice angry?",
  "expected_status": "ambiguous",
  "reference_answer": "The question needs the scene because Alice becomes angry more than once.",
  "required_answer_claims": [],
  "valid_evidence_locations": [
    {
      "evidence_id": "A1",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 51,
        "chapter": "7",
        "pdf_block": 5
      },
      "exact_supporting_span": "said Alice angrily",
      "preceding_context": "‘Have some wine,’ the March Hare said in an encouraging tone. Alice looked all round the table, but there was nothing on it but tea. ‘I don’t see any wine,’ she remarked.",
      "supporting_context": "‘There isn’t any,’ said the March Hare. ‘Then it wasn’t very civil of you to oﬀer it,’ said Alice angrily. ‘It wasn’t very civil of you to sit down without being invited,’ said the March Hare.",
      "following_context": "‘I didn’t know it was YOUR table,’ said Alice; ‘it’s laid for a great many more than three.’",
      "why_supports": "This original passage demonstrates one distinct plausible referent or event.",
      "context_incomplete": false,
      "epistemic_status": "narrator_fact"
    },
    {
      "evidence_id": "A2",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 55,
        "chapter": "7",
        "pdf_block": 10
      },
      "exact_supporting_span": "Alice was beginning very angrily",
      "preceding_context": "The Dormouse again took a minute or two to think about it, and then said, ‘It was a treacle-well.’",
      "supporting_context": "‘There’s no such thing!’ Alice was beginning very angrily, but the Hatter and the March Hare went ‘Sh! sh!’ and the Dormouse sulkily remarked, ‘If you can’t be civil, you’d better ﬁnish the story for yourself.’",
      "following_context": "‘No, please go on!’ Alice said very humbly; ‘I won’t interrupt again. I dare say there may be ONE.’",
      "why_supports": "This original passage demonstrates one distinct plausible referent or event.",
      "context_incomplete": false,
      "epistemic_status": "narrator_fact"
    }
  ],
  "exact_supporting_spans": [
    "said Alice angrily",
    "Alice was beginning very angrily"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "A1",
      "preceding": "‘Have some wine,’ the March Hare said in an encouraging tone. Alice looked all round the table, but there was nothing on it but tea. ‘I don’t see any wine,’ she remarked.",
      "supporting": "‘There isn’t any,’ said the March Hare. ‘Then it wasn’t very civil of you to oﬀer it,’ said Alice angrily. ‘It wasn’t very civil of you to sit down without being invited,’ said the March Hare.",
      "following": "‘I didn’t know it was YOUR table,’ said Alice; ‘it’s laid for a great many more than three.’",
      "context_incomplete": false
    },
    {
      "evidence_id": "A2",
      "preceding": "The Dormouse again took a minute or two to think about it, and then said, ‘It was a treacle-well.’",
      "supporting": "‘There’s no such thing!’ Alice was beginning very angrily, but the Hatter and the March Hare went ‘Sh! sh!’ and the Dormouse sulkily remarked, ‘If you can’t be civil, you’d better ﬁnish the story for yourself.’",
      "following": "‘No, please go on!’ Alice said very humbly; ‘I won’t interrupt again. I dare say there may be ONE.’",
      "context_incomplete": false
    }
  ],
  "primary_category": "ambiguous_underspecified",
  "category": "ambiguous_underspecified",
  "tags": [
    "ambiguity"
  ],
  "difficulty": "medium",
  "annotation_notes": "The anger labels are narrator descriptions attached to two different tea-party moments.",
  "annotation_confidence": "needs_owner_review",
  "historical_case": false,
  "requires_owner_attention": true,
  "negative_verification": null,
  "ambiguity_rationale": "Different scenes give different reasons for Alice’s anger.",
  "expected_clarification": "Which scene or conversation do you mean?",
  "evaluation_execution": null,
  "ambiguity_type": "book_dependent_multiple_events",
  "plausible_referents": [
    "anger at tea-party rudeness",
    "anger during the Dormouse’s story"
  ],
  "review_tier": "DEEP_REVIEW",
  "fact_family_id": "fact_av051",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [],
  "evidence_event_id": "event_fact_av051",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "av051"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## av052

```json
{
  "case_id": "av052",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "What did Alice do after the White Rabbit dropped his gloves and fan and ran away?",
  "expected_status": "answered",
  "reference_answer": "She picked up the fan and gloves, kept fanning herself, and began wondering whether she had changed.",
  "required_answer_claims": [
    {
      "claim_id": "C1",
      "claim_text": "Alice picked up the fan and gloves.",
      "evidence_ids": [
        "A1"
      ]
    },
    {
      "claim_id": "C2",
      "claim_text": "She fanned herself and wondered whether she had changed.",
      "evidence_ids": [
        "A1"
      ]
    }
  ],
  "valid_evidence_locations": [
    {
      "evidence_id": "A1",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 20,
        "chapter": "2",
        "pdf_block": 2
      },
      "exact_supporting_span": "Alice took up the fan and gloves",
      "preceding_context": "After a time she heard a little pattering of feet in the distance, and she hastily dried her eyes to see what was coming. It was the White Rabbit returning, splendidly dressed, with a pair of white kid gloves in one hand and a large fan in the other: he came trotting along in a great hurry, muttering to himself as he came, ‘Oh! the Duchess, the Duchess! Oh! won’t she be savage if I’ve kept her waiting!’ Alice felt so desperate that she was ready to ask help of any one; so, when the Rabbit came near her, she began, in a low, timid voice, ‘If you please, sir–’ The Rabbit started violently, dropped the white kid gloves and the fan, and skurried away into the darkness as hard as he could go.",
      "supporting_context": "Alice took up the fan and gloves, and, as the hall was very hot, she kept fanning herself all the time she went on talking: ‘Dear, dear! How queer everything is to-day! And yesterday things went on just as usual. I wonder if I’ve been changed in the night? Let me think: was I the same when I got up this morning? I almost think I can remember feeling a little diﬀerent. But if I’m not the same, the next question is, Who in the world am I? Ah, THAT’S the great puzzle!’ And she began thinking over all the children she knew that were of the same age as herself, to see if she could have been changed for any of them.",
      "following_context": "",
      "why_supports": "The narrator states what Alice did immediately after the Rabbit fled: she picked up the fan and gloves, fanned herself, and started questioning whether she had changed.",
      "context_incomplete": false,
      "epistemic_status": "narrator_fact"
    }
  ],
  "exact_supporting_spans": [
    "Alice took up the fan and gloves"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "A1",
      "preceding": "After a time she heard a little pattering of feet in the distance, and she hastily dried her eyes to see what was coming. It was the White Rabbit returning, splendidly dressed, with a pair of white kid gloves in one hand and a large fan in the other: he came trotting along in a great hurry, muttering to himself as he came, ‘Oh! the Duchess, the Duchess! Oh! won’t she be savage if I’ve kept her waiting!’ Alice felt so desperate that she was ready to ask help of any one; so, when the Rabbit came near her, she began, in a low, timid voice, ‘If you please, sir–’ The Rabbit started violently, dropped the white kid gloves and the fan, and skurried away into the darkness as hard as he could go.",
      "supporting": "Alice took up the fan and gloves, and, as the hall was very hot, she kept fanning herself all the time she went on talking: ‘Dear, dear! How queer everything is to-day! And yesterday things went on just as usual. I wonder if I’ve been changed in the night? Let me think: was I the same when I got up this morning? I almost think I can remember feeling a little diﬀerent. But if I’m not the same, the next question is, Who in the world am I? Ah, THAT’S the great puzzle!’ And she began thinking over all the children she knew that were of the same age as herself, to see if she could have been changed for any of them.",
      "following": "",
      "context_incomplete": false
    }
  ],
  "primary_category": "local_context_reasoning",
  "category": "local_context_reasoning",
  "tags": [
    "sequence_context"
  ],
  "difficulty": "medium",
  "annotation_notes": "Former ambiguity candidate repaired: prior A1/A2 duplicated the same Rabbit departure, so the case is now an answered local-context sequence rather than artificial ambiguity.",
  "annotation_confidence": "medium",
  "historical_case": false,
  "requires_owner_attention": true,
  "negative_verification": null,
  "ambiguity_rationale": null,
  "expected_clarification": null,
  "evaluation_execution": null,
  "ambiguity_type": null,
  "plausible_referents": [],
  "review_tier": "DEEP_REVIEW",
  "fact_family_id": "fact_av052",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [],
  "evidence_event_id": "event_fact_av052",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "av052"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## av053

```json
{
  "case_id": "av053",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "What happened to the cards?",
  "expected_status": "ambiguous",
  "reference_answer": "Clarification is required because ‘the cards’ can refer to the card gardeners or the whole pack at the end.",
  "required_answer_claims": [],
  "valid_evidence_locations": [
    {
      "evidence_id": "E1",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 60,
        "chapter": "8",
        "pdf_block": 1
      },
      "exact_supporting_span": "the three gardeners instantly threw themselves flat upon their faces",
      "preceding_context": "Five and Seven said nothing, but looked at Two. Two began in a low voice, ‘Why the fact is, you see, Miss, this here ought to have been a RED rose-tree, and we put a white one in by mistake; and if the Queen was to ﬁnd it out, we should all have our heads cut oﬀ, you know. So you see, Miss, we’re doing our best, afore she comes, to–’ At this moment Five, who",
      "supporting_context": "had been anxiously looking across the garden, called out ‘The Queen! The Queen!’ and the three gardeners instantly threw themselves ﬂat upon their faces. There was a sound of many footsteps, and Alice looked round, eager to see the Queen.",
      "following_context": "First came ten soldiers carrying clubs; these were all shaped like the three gardeners, oblong and ﬂat, with their hands and feet at the corners: next the ten courtiers; these were ornamented all over with diamonds, and walked two and two, as the soldiers did. After these came the royal children; there were ten of them, and the little dears came jumping merrily along hand in hand, in couples: they were all ornamented with hearts. Next came the guests, mostly Kings and Queens, and among them Alice recognised the White Rabbit: it was talking in a hurried nervous manner, smiling at everything that was said, and went by without noticing her. Then followed the Knave of Hearts, carrying the King’s crown on a crimson velvet cushion; and, last of all this grand procession, came THE KING AND QUEEN OF HEARTS.",
      "why_supports": "This passage establishes one plausible referent used to verify the ambiguity.",
      "epistemic_status": "narrator_fact",
      "context_incomplete": false
    },
    {
      "evidence_id": "E2",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 91,
        "chapter": "12",
        "pdf_block": 6
      },
      "exact_supporting_span": "the whole pack rose up into the air",
      "preceding_context": "‘Who cares for you?’ said Alice, (she had grown to her full size by this time.) ‘You’re nothing but a pack of cards!’",
      "supporting_context": "At this the whole pack rose up into the air, and came ﬂying down upon her: she gave a little scream, half of fright and half of anger, and tried to beat them oﬀ, and found herself lying on the bank, with her head in the lap of her sister, who was gently brushing away some dead leaves that had ﬂuttered down from the trees upon her face.",
      "following_context": "‘Wake up, Alice dear!’ said her sister; ‘Why, what a long sleep you’ve had!’",
      "why_supports": "This passage establishes one plausible referent used to verify the ambiguity.",
      "epistemic_status": "narrator_fact",
      "context_incomplete": false
    }
  ],
  "exact_supporting_spans": [
    "the three gardeners instantly threw themselves flat upon their faces",
    "the whole pack rose up into the air"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "E1",
      "preceding": "Five and Seven said nothing, but looked at Two. Two began in a low voice, ‘Why the fact is, you see, Miss, this here ought to have been a RED rose-tree, and we put a white one in by mistake; and if the Queen was to ﬁnd it out, we should all have our heads cut oﬀ, you know. So you see, Miss, we’re doing our best, afore she comes, to–’ At this moment Five, who",
      "supporting": "had been anxiously looking across the garden, called out ‘The Queen! The Queen!’ and the three gardeners instantly threw themselves ﬂat upon their faces. There was a sound of many footsteps, and Alice looked round, eager to see the Queen.",
      "following": "First came ten soldiers carrying clubs; these were all shaped like the three gardeners, oblong and ﬂat, with their hands and feet at the corners: next the ten courtiers; these were ornamented all over with diamonds, and walked two and two, as the soldiers did. After these came the royal children; there were ten of them, and the little dears came jumping merrily along hand in hand, in couples: they were all ornamented with hearts. Next came the guests, mostly Kings and Queens, and among them Alice recognised the White Rabbit: it was talking in a hurried nervous manner, smiling at everything that was said, and went by without noticing her. Then followed the Knave of Hearts, carrying the King’s crown on a crimson velvet cushion; and, last of all this grand procession, came THE KING AND QUEEN OF HEARTS.",
      "context_incomplete": false
    },
    {
      "evidence_id": "E2",
      "preceding": "‘Who cares for you?’ said Alice, (she had grown to her full size by this time.) ‘You’re nothing but a pack of cards!’",
      "supporting": "At this the whole pack rose up into the air, and came ﬂying down upon her: she gave a little scream, half of fright and half of anger, and tried to beat them oﬀ, and found herself lying on the bank, with her head in the lap of her sister, who was gently brushing away some dead leaves that had ﬂuttered down from the trees upon her face.",
      "following": "‘Wake up, Alice dear!’ said her sister; ‘Why, what a long sleep you’ve had!’",
      "context_incomplete": false
    }
  ],
  "primary_category": "ambiguous_underspecified",
  "category": "ambiguous_underspecified",
  "tags": [
    "ambiguity"
  ],
  "difficulty": "medium",
  "annotation_notes": "Stale garden-related plausible_referents metadata was replaced with the two card referents actually evidenced.",
  "annotation_confidence": "needs_owner_review",
  "historical_case": false,
  "requires_owner_attention": true,
  "negative_verification": null,
  "ambiguity_rationale": "‘The cards’ can refer to the card gardeners in the croquet-ground scene or the whole pack that later flies at Alice.",
  "expected_clarification": "Do you mean the card gardeners at the croquet ground or the whole pack at the end of the trial?",
  "evaluation_execution": null,
  "ambiguity_type": "book_dependent_multiple_referents",
  "plausible_referents": [
    "the three card gardeners at the croquet ground",
    "the whole pack of cards at the end of the trial"
  ],
  "review_tier": "DEEP_REVIEW",
  "fact_family_id": "fact_av053",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [],
  "evidence_event_id": "event_fact_av053",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "av053"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## sg098

```json
{
  "case_id": "sg098",
  "lifecycle_status": "candidate",
  "split_candidate": "secret_garden_holdout",
  "source_book": "the_secret_garden",
  "source_book_sha256": "6b0bb5fbd0c4e873d2d22028da9d753cf3977d5f70ac58221556b28060badbf5",
  "question": "What did Mary see when a covering moved aside?",
  "expected_status": "ambiguous",
  "reference_answer": "Clarification is required: moving ivy exposed a door knob, while drawing back the silk curtain uncovered a picture of Colin’s mother.",
  "required_answer_claims": [],
  "valid_evidence_locations": [
    {
      "evidence_id": "A2",
      "source_location": {
        "book": "the_secret_garden",
        "canonical_line": 2319,
        "chapter": null,
        "generated_pdf_pages": [
          34
        ]
      },
      "exact_supporting_span": "It was the knob of a door",
      "preceding_context": "Mary Lennox had heard a great deal about Magic in her Ayah’s stories, and she always said that what happened almost at that moment was Magic.",
      "supporting_context": "One of the nice little gusts of wind rushed down the walk, and it was a stronger one than the rest. It was strong enough to wave the branches of the trees, and it was more than strong enough to sway the trailing sprays of untrimmed ivy hanging from the wall. Mary had stepped close to the robin, and suddenly the gust of wind swung aside some loose ivy trails, and more suddenly still she jumped toward it and caught it in her hand. This she did because she had seen something under it—a round knob which had been covered by the leaves hanging over it. It was the knob of a door.",
      "following_context": "She put her hands under the leaves and began to pull and push them aside. Thick as the ivy hung, it nearly all was a loose and swinging curtain, though some had crept over wood and iron. Mary’s heart began to thump and her hands to shake a little in her delight and excitement. The robin kept singing and twittering away and tilting his head on one side, as if he were as excited as she was. What was this under her hands which was square and made of iron and which her fingers found a hole in?",
      "why_supports": "In one scene, moving ivy reveals the knob of a hidden door.",
      "context_incomplete": false,
      "epistemic_status": "narrator_fact"
    },
    {
      "evidence_id": "A3",
      "source_location": {
        "book": "the_secret_garden",
        "canonical_line": 4297,
        "chapter": null,
        "generated_pdf_pages": [
          63
        ]
      },
      "exact_supporting_span": "silk curtain ran back on rings",
      "preceding_context": "“There is a cord hanging from it,” said Colin. “Go and pull it.”",
      "supporting_context": "Mary got up, much mystified, and found the cord. When she pulled it the silk curtain ran back on rings and when it ran back it uncovered a picture. It was the picture of a girl with a laughing face. She had bright hair tied up with a blue ribbon and her gay, lovely eyes were exactly like Colin’s unhappy ones, agate gray and looking twice as big as they really were because of the black lashes all round them.",
      "following_context": "“She is my mother,” said Colin complainingly. “I don’t see why she died. Sometimes I hate her for doing it.”",
      "why_supports": "In another scene, drawing back a silk curtain reveals a portrait of Colin’s mother.",
      "context_incomplete": false,
      "epistemic_status": "narrator_fact"
    }
  ],
  "exact_supporting_spans": [
    "It was the knob of a door",
    "silk curtain ran back on rings"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "A2",
      "preceding": "Mary Lennox had heard a great deal about Magic in her Ayah’s stories, and she always said that what happened almost at that moment was Magic.",
      "supporting": "One of the nice little gusts of wind rushed down the walk, and it was a stronger one than the rest. It was strong enough to wave the branches of the trees, and it was more than strong enough to sway the trailing sprays of untrimmed ivy hanging from the wall. Mary had stepped close to the robin, and suddenly the gust of wind swung aside some loose ivy trails, and more suddenly still she jumped toward it and caught it in her hand. This she did because she had seen something under it—a round knob which had been covered by the leaves hanging over it. It was the knob of a door.",
      "following": "She put her hands under the leaves and began to pull and push them aside. Thick as the ivy hung, it nearly all was a loose and swinging curtain, though some had crept over wood and iron. Mary’s heart began to thump and her hands to shake a little in her delight and excitement. The robin kept singing and twittering away and tilting his head on one side, as if he were as excited as she was. What was this under her hands which was square and made of iron and which her fingers found a hole in?",
      "context_incomplete": false
    },
    {
      "evidence_id": "A3",
      "preceding": "“There is a cord hanging from it,” said Colin. “Go and pull it.”",
      "supporting": "Mary got up, much mystified, and found the cord. When she pulled it the silk curtain ran back on rings and when it ran back it uncovered a picture. It was the picture of a girl with a laughing face. She had bright hair tied up with a blue ribbon and her gay, lovely eyes were exactly like Colin’s unhappy ones, agate gray and looking twice as big as they really were because of the black lashes all round them.",
      "following": "“She is my mother,” said Colin complainingly. “I don’t see why she died. Sometimes I hate her for doing it.”",
      "context_incomplete": false
    }
  ],
  "primary_category": "ambiguous_underspecified",
  "category": "ambiguous_underspecified",
  "tags": [
    "ambiguity"
  ],
  "difficulty": "medium",
  "annotation_notes": "Repaired ambiguity: the former version incorrectly treated a curtain/portrait passage as a door discovery. The new wording is supported by two genuinely distinct uncovering events.",
  "annotation_confidence": "medium",
  "historical_case": false,
  "requires_owner_attention": true,
  "negative_verification": null,
  "ambiguity_rationale": "Two separate scenes involve a covering moving aside: ivy reveals a door knob, while a silk curtain reveals a portrait.",
  "expected_clarification": "Do you mean the ivy in the garden or the silk curtain in Colin’s room?",
  "evaluation_execution": null,
  "ambiguity_type": "book_dependent_multiple_referents",
  "plausible_referents": [
    "ivy moving aside and revealing a door knob",
    "the silk curtain drawing back and revealing Colin’s mother’s portrait"
  ],
  "review_tier": "DEEP_REVIEW",
  "fact_family_id": "fact_sg098",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [],
  "evidence_event_id": "event_fact_sg098",
  "development_exposure": {
    "status": "not_applicable_different_book",
    "sources": [],
    "review_method": "Secret Garden is a separate-book holdout."
  }
}
```

---

## sg099

```json
{
  "case_id": "sg099",
  "lifecycle_status": "candidate",
  "split_candidate": "secret_garden_holdout",
  "source_book": "the_secret_garden",
  "source_book_sha256": "6b0bb5fbd0c4e873d2d22028da9d753cf3977d5f70ac58221556b28060badbf5",
  "question": "Why was Colin upset?",
  "expected_status": "ambiguous",
  "reference_answer": "The question needs the particular scene.",
  "required_answer_claims": [],
  "valid_evidence_locations": [
    {
      "evidence_id": "A1",
      "source_location": {
        "book": "the_secret_garden",
        "canonical_line": 4309,
        "chapter": null,
        "generated_pdf_pages": [
          63
        ]
      },
      "exact_supporting_span": "father would not have hated to look at me",
      "preceding_context": "“How queer!” said Mary.",
      "supporting_context": "“If she had lived I believe I should not have been ill always,” he grumbled. “I dare say I should have lived, too. And my father would not have hated to look at me. I dare say I should have had a strong back. Draw the curtain again.”",
      "following_context": "Mary did as she was told and returned to her footstool.",
      "why_supports": "Colin himself expresses distress about his mother’s death and his father’s reaction to him.",
      "context_incomplete": false,
      "epistemic_status": "character_statement"
    },
    {
      "evidence_id": "A2",
      "source_location": {
        "book": "the_secret_garden",
        "canonical_line": 5410,
        "chapter": null,
        "generated_pdf_pages": [
          78
        ]
      },
      "exact_supporting_span": "They were a nice agreeable pair as they glared at each other",
      "preceding_context": "“Shall they, Mr. Rajah!” said Mary fiercely. “They may drag me in but they can’t make me talk when they get me here. I’ll sit and clench my teeth and never tell you one thing. I won’t even look at you. I’ll stare at the floor!”",
      "supporting_context": "They were a nice agreeable pair as they glared at each other. If they had been two little street boys they would have sprung at each other and had a rough-and-tumble fight. As it was, they did the next thing to it.",
      "following_context": "“You are a selfish thing!” cried Colin.",
      "why_supports": "Narration and dialogue show a separate angry quarrel between Colin and Mary.",
      "context_incomplete": false,
      "epistemic_status": "narrator_fact"
    },
    {
      "evidence_id": "A3",
      "source_location": {
        "book": "the_secret_garden",
        "canonical_line": 5196,
        "chapter": null,
        "generated_pdf_pages": [
          75
        ]
      },
      "exact_supporting_span": "if he should feel a lump coming",
      "preceding_context": "“No, but he wishes he’d never been born. Mother she says that’s th’ worst thing on earth for a child. Them as is not wanted scarce ever thrives. Mester Craven he’d buy anythin’ as money could buy for th’ poor lad but he’d like to forget as he’s on earth. For one thing, he’s afraid he’ll look at him some day and find he’s growed hunchback.”",
      "supporting_context": "“Colin’s so afraid of it himself that he won’t sit up,” said Mary. “He says he’s always thinking that if he should feel a lump coming he should go crazy and scream himself to death.”",
      "following_context": "“Eh! he oughtn’t to lie there thinkin’ things like that,” said Dickon. “No lad could get well as thought them sort o’ things.”",
      "why_supports": "Mary reports Colin’s separate fear that he might develop a lump/hunchback.",
      "context_incomplete": false,
      "epistemic_status": "character_statement"
    }
  ],
  "exact_supporting_spans": [
    "father would not have hated to look at me",
    "They were a nice agreeable pair as they glared at each other",
    "if he should feel a lump coming"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "A1",
      "preceding": "“How queer!” said Mary.",
      "supporting": "“If she had lived I believe I should not have been ill always,” he grumbled. “I dare say I should have lived, too. And my father would not have hated to look at me. I dare say I should have had a strong back. Draw the curtain again.”",
      "following": "Mary did as she was told and returned to her footstool.",
      "context_incomplete": false
    },
    {
      "evidence_id": "A2",
      "preceding": "“Shall they, Mr. Rajah!” said Mary fiercely. “They may drag me in but they can’t make me talk when they get me here. I’ll sit and clench my teeth and never tell you one thing. I won’t even look at you. I’ll stare at the floor!”",
      "supporting": "They were a nice agreeable pair as they glared at each other. If they had been two little street boys they would have sprung at each other and had a rough-and-tumble fight. As it was, they did the next thing to it.",
      "following": "“You are a selfish thing!” cried Colin.",
      "context_incomplete": false
    },
    {
      "evidence_id": "A3",
      "preceding": "“No, but he wishes he’d never been born. Mother she says that’s th’ worst thing on earth for a child. Them as is not wanted scarce ever thrives. Mester Craven he’d buy anythin’ as money could buy for th’ poor lad but he’d like to forget as he’s on earth. For one thing, he’s afraid he’ll look at him some day and find he’s growed hunchback.”",
      "supporting": "“Colin’s so afraid of it himself that he won’t sit up,” said Mary. “He says he’s always thinking that if he should feel a lump coming he should go crazy and scream himself to death.”",
      "following": "“Eh! he oughtn’t to lie there thinkin’ things like that,” said Dickon. “No lad could get well as thought them sort o’ things.”",
      "context_incomplete": false
    }
  ],
  "primary_category": "ambiguous_underspecified",
  "category": "ambiguous_underspecified",
  "tags": [
    "ambiguity"
  ],
  "difficulty": "medium",
  "annotation_notes": "Holdout item: full owner review remains mandatory. Speech-vs-narration epistemic labels were separated for the three distinct upset scenes.",
  "annotation_confidence": "needs_owner_review",
  "historical_case": false,
  "requires_owner_attention": true,
  "negative_verification": null,
  "ambiguity_rationale": "Colin becomes upset for different reasons in several scenes, including secrecy, illness fears, and conflict with Mary.",
  "expected_clarification": "Which Colin scene or outburst do you mean?",
  "evaluation_execution": null,
  "ambiguity_type": "book_dependent_multiple_events",
  "plausible_referents": [
    "fear that his father hated him",
    "fear of a lump/illness",
    "his quarrel with Mary"
  ],
  "review_tier": "DEEP_REVIEW",
  "fact_family_id": "fact_sg099",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [],
  "evidence_event_id": "event_fact_sg099",
  "development_exposure": {
    "status": "not_applicable_different_book",
    "sources": [],
    "review_method": "Secret Garden is a separate-book holdout."
  }
}
```

---

## q016

```json
{
  "case_id": "q016",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "What did the pebbles thrown through the window become, and what happened when Alice ate one?",
  "expected_status": "answered",
  "reference_answer": "They became little cakes, and eating one made Alice shrink.",
  "required_answer_claims": [
    {
      "claim_id": "C1",
      "claim_text": "The pebbles became cakes.",
      "evidence_ids": [
        "E1"
      ]
    },
    {
      "claim_id": "C2",
      "claim_text": "Eating one made Alice shrink.",
      "evidence_ids": [
        "E2"
      ]
    }
  ],
  "valid_evidence_locations": [
    {
      "evidence_id": "E1",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 35,
        "chapter": "4",
        "pdf_block": 4
      },
      "exact_supporting_span": "pebbles were all turning into little cakes",
      "preceding_context": "‘A barrowful of WHAT?’ thought Alice; but she had not long to doubt, for the next moment a shower of little pebbles came rattling in at the window, and some of them hit her in the face. ‘I’ll put a stop to this,’ she said to herself, and shouted out, ‘You’d better not do that again!’ which produced another dead silence.",
      "supporting_context": "Alice noticed with some surprise that the pebbles were all turning into little cakes as they lay on the ﬂoor, and a bright idea came into her head. ‘If I eat one of these cakes,’ she thought, ‘it’s sure to make SOME change in my size; and as it can’t possibly make me larger, it must make me smaller, I suppose.’",
      "following_context": "So she swallowed one of the cakes, and was delighted to ﬁnd that she began shrinking directly. As soon as she was small enough to get through the door, she ran out of the house, and found quite a crowd of little animals and birds waiting outside. The poor little Lizard, Bill, was in the middle, being held up by two guinea-pigs, who were giving it something out of a bottle. They all made a rush at Alice the moment she appeared; but she ran oﬀas hard as she could, and soon found herself safe in a thick wood.",
      "why_supports": "The cited span and its adjacent discourse support: The pebbles became cakes.",
      "context_incomplete": false,
      "epistemic_status": "narrator_fact"
    },
    {
      "evidence_id": "E2",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 35,
        "chapter": "4",
        "pdf_block": 5
      },
      "exact_supporting_span": "began shrinking directly",
      "preceding_context": "Alice noticed with some surprise that the pebbles were all turning into little cakes as they lay on the ﬂoor, and a bright idea came into her head. ‘If I eat one of these cakes,’ she thought, ‘it’s sure to make SOME change in my size; and as it can’t possibly make me larger, it must make me smaller, I suppose.’",
      "supporting_context": "So she swallowed one of the cakes, and was delighted to ﬁnd that she began shrinking directly. As soon as she was small enough to get through the door, she ran out of the house, and found quite a crowd of little animals and birds waiting outside. The poor little Lizard, Bill, was in the middle, being held up by two guinea-pigs, who were giving it something out of a bottle. They all made a rush at Alice the moment she appeared; but she ran oﬀas hard as she could, and soon found herself safe in a thick wood.",
      "following_context": "‘The ﬁrst thing I’ve got to do,’ said Alice to herself, as she wandered about in the wood, ‘is to grow to my right size again; and the second thing is to ﬁnd my way into that lovely garden. I think that will be the best plan.’",
      "why_supports": "The cited span and its adjacent discourse support: Eating one made Alice shrink.",
      "context_incomplete": false,
      "epistemic_status": "narrator_fact"
    }
  ],
  "exact_supporting_spans": [
    "pebbles were all turning into little cakes",
    "began shrinking directly"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "E1",
      "preceding": "‘A barrowful of WHAT?’ thought Alice; but she had not long to doubt, for the next moment a shower of little pebbles came rattling in at the window, and some of them hit her in the face. ‘I’ll put a stop to this,’ she said to herself, and shouted out, ‘You’d better not do that again!’ which produced another dead silence.",
      "supporting": "Alice noticed with some surprise that the pebbles were all turning into little cakes as they lay on the ﬂoor, and a bright idea came into her head. ‘If I eat one of these cakes,’ she thought, ‘it’s sure to make SOME change in my size; and as it can’t possibly make me larger, it must make me smaller, I suppose.’",
      "following": "So she swallowed one of the cakes, and was delighted to ﬁnd that she began shrinking directly. As soon as she was small enough to get through the door, she ran out of the house, and found quite a crowd of little animals and birds waiting outside. The poor little Lizard, Bill, was in the middle, being held up by two guinea-pigs, who were giving it something out of a bottle. They all made a rush at Alice the moment she appeared; but she ran oﬀas hard as she could, and soon found herself safe in a thick wood.",
      "context_incomplete": false
    },
    {
      "evidence_id": "E2",
      "preceding": "Alice noticed with some surprise that the pebbles were all turning into little cakes as they lay on the ﬂoor, and a bright idea came into her head. ‘If I eat one of these cakes,’ she thought, ‘it’s sure to make SOME change in my size; and as it can’t possibly make me larger, it must make me smaller, I suppose.’",
      "supporting": "So she swallowed one of the cakes, and was delighted to ﬁnd that she began shrinking directly. As soon as she was small enough to get through the door, she ran out of the house, and found quite a crowd of little animals and birds waiting outside. The poor little Lizard, Bill, was in the middle, being held up by two guinea-pigs, who were giving it something out of a bottle. They all made a rush at Alice the moment she appeared; but she ran oﬀas hard as she could, and soon found herself safe in a thick wood.",
      "following": "‘The ﬁrst thing I’ve got to do,’ said Alice to herself, as she wandered about in the wood, ‘is to grow to my right size again; and the second thing is to ﬁnd my way into that lovely garden. I think that will be the best plan.’",
      "context_incomplete": false
    }
  ],
  "primary_category": "multi_fact_single_context",
  "category": "multi_fact_single_context",
  "tags": [
    "historical_case",
    "phase4_reuse"
  ],
  "difficulty": "medium",
  "annotation_notes": "Reused historical Phase-4 case; proposed V2 classification does not change its old result. Reclassified from multi-source: the answer components belong to one continuous local event/context.",
  "annotation_confidence": "medium",
  "historical_case": true,
  "requires_owner_attention": true,
  "negative_verification": null,
  "ambiguity_rationale": null,
  "expected_clarification": null,
  "evaluation_execution": null,
  "fact_family_id": "fact_q016",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [],
  "review_tier": "DEEP_REVIEW",
  "evidence_event_id": "event_fact_q016",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "q016"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## q024

```json
{
  "case_id": "q024",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "What served as the balls, mallets, and arches in the Queen's croquet game?",
  "expected_status": "answered",
  "reference_answer": "Hedgehogs were the balls, flamingoes were the mallets, and soldiers bent over to form the arches.",
  "required_answer_claims": [
    {
      "claim_id": "C1",
      "claim_text": "Hedgehogs were the balls.",
      "evidence_ids": [
        "E1"
      ]
    },
    {
      "claim_id": "C2",
      "claim_text": "Flamingoes were the mallets.",
      "evidence_ids": [
        "E2"
      ]
    },
    {
      "claim_id": "C3",
      "claim_text": "Soldiers formed the arches.",
      "evidence_ids": [
        "E3"
      ]
    }
  ],
  "valid_evidence_locations": [
    {
      "evidence_id": "E1",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 62,
        "chapter": "8",
        "pdf_block": 3
      },
      "exact_supporting_span": "balls were live hedgehogs",
      "preceding_context": "‘She boxed the Queen’s ears–’ the Rabbit began. Alice gave a little scream of laughter. ‘Oh, hush!’ the Rabbit whispered in a frightened tone. ‘The Queen will hear you! You see, she came rather late, and the Queen said–’",
      "supporting_context": "‘Get to your places!’ shouted the Queen in a voice of thunder, and peo- ple began running about in all directions, tumbling up against each other; however, they got settled down in a minute or two, and the game began. Alice thought she had never seen such a curious croquet-ground in her life; it was all ridges and furrows; the balls were live hedgehogs, the mallets live ﬂamingoes, and the soldiers had to double themselves up and to stand on their hands and feet, to make the arches.",
      "following_context": "The chief diﬃculty Alice found at ﬁrst was in managing her ﬂamingo: she succeeded in getting its body tucked away, comfortably enough, under her arm, with its legs hanging down, but generally, just as she had got its neck nicely straightened out, and was going to give the hedgehog a blow with its head, it WOULD twist itself round and look up in her face, with such a puzzled expression that she could not help bursting out laughing: and when she had got its head down, and was going to begin again, it was very provoking to ﬁnd that the hedgehog had unrolled itself, and was in the act of crawling away: besides all this, there was generally a ridge or furrow in the way wherever she wanted to send the hedgehog to, and, as the doubled-up soldiers were always getting up and walking oﬀto other parts of the ground, Alice soon came to the conclusion that it was a very diﬃcult game indeed.",
      "why_supports": "The cited span and its adjacent discourse support: Hedgehogs were the balls.",
      "context_incomplete": false,
      "epistemic_status": "narrator_fact"
    },
    {
      "evidence_id": "E2",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 62,
        "chapter": "8",
        "pdf_block": 3
      },
      "exact_supporting_span": "mallets live flamingoes",
      "preceding_context": "‘She boxed the Queen’s ears–’ the Rabbit began. Alice gave a little scream of laughter. ‘Oh, hush!’ the Rabbit whispered in a frightened tone. ‘The Queen will hear you! You see, she came rather late, and the Queen said–’",
      "supporting_context": "‘Get to your places!’ shouted the Queen in a voice of thunder, and peo- ple began running about in all directions, tumbling up against each other; however, they got settled down in a minute or two, and the game began. Alice thought she had never seen such a curious croquet-ground in her life; it was all ridges and furrows; the balls were live hedgehogs, the mallets live ﬂamingoes, and the soldiers had to double themselves up and to stand on their hands and feet, to make the arches.",
      "following_context": "The chief diﬃculty Alice found at ﬁrst was in managing her ﬂamingo: she succeeded in getting its body tucked away, comfortably enough, under her arm, with its legs hanging down, but generally, just as she had got its neck nicely straightened out, and was going to give the hedgehog a blow with its head, it WOULD twist itself round and look up in her face, with such a puzzled expression that she could not help bursting out laughing: and when she had got its head down, and was going to begin again, it was very provoking to ﬁnd that the hedgehog had unrolled itself, and was in the act of crawling away: besides all this, there was generally a ridge or furrow in the way wherever she wanted to send the hedgehog to, and, as the doubled-up soldiers were always getting up and walking oﬀto other parts of the ground, Alice soon came to the conclusion that it was a very diﬃcult game indeed.",
      "why_supports": "The cited span and its adjacent discourse support: Flamingoes were the mallets.",
      "context_incomplete": false,
      "epistemic_status": "narrator_fact"
    },
    {
      "evidence_id": "E3",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 62,
        "chapter": "8",
        "pdf_block": 3
      },
      "exact_supporting_span": "make the arches",
      "preceding_context": "‘She boxed the Queen’s ears–’ the Rabbit began. Alice gave a little scream of laughter. ‘Oh, hush!’ the Rabbit whispered in a frightened tone. ‘The Queen will hear you! You see, she came rather late, and the Queen said–’",
      "supporting_context": "‘Get to your places!’ shouted the Queen in a voice of thunder, and peo- ple began running about in all directions, tumbling up against each other; however, they got settled down in a minute or two, and the game began. Alice thought she had never seen such a curious croquet-ground in her life; it was all ridges and furrows; the balls were live hedgehogs, the mallets live ﬂamingoes, and the soldiers had to double themselves up and to stand on their hands and feet, to make the arches.",
      "following_context": "The chief diﬃculty Alice found at ﬁrst was in managing her ﬂamingo: she succeeded in getting its body tucked away, comfortably enough, under her arm, with its legs hanging down, but generally, just as she had got its neck nicely straightened out, and was going to give the hedgehog a blow with its head, it WOULD twist itself round and look up in her face, with such a puzzled expression that she could not help bursting out laughing: and when she had got its head down, and was going to begin again, it was very provoking to ﬁnd that the hedgehog had unrolled itself, and was in the act of crawling away: besides all this, there was generally a ridge or furrow in the way wherever she wanted to send the hedgehog to, and, as the doubled-up soldiers were always getting up and walking oﬀto other parts of the ground, Alice soon came to the conclusion that it was a very diﬃcult game indeed.",
      "why_supports": "The cited span and its adjacent discourse support: Soldiers formed the arches.",
      "context_incomplete": false,
      "epistemic_status": "narrator_fact"
    }
  ],
  "exact_supporting_spans": [
    "balls were live hedgehogs",
    "mallets live flamingoes",
    "make the arches"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "E1",
      "preceding": "‘She boxed the Queen’s ears–’ the Rabbit began. Alice gave a little scream of laughter. ‘Oh, hush!’ the Rabbit whispered in a frightened tone. ‘The Queen will hear you! You see, she came rather late, and the Queen said–’",
      "supporting": "‘Get to your places!’ shouted the Queen in a voice of thunder, and peo- ple began running about in all directions, tumbling up against each other; however, they got settled down in a minute or two, and the game began. Alice thought she had never seen such a curious croquet-ground in her life; it was all ridges and furrows; the balls were live hedgehogs, the mallets live ﬂamingoes, and the soldiers had to double themselves up and to stand on their hands and feet, to make the arches.",
      "following": "The chief diﬃculty Alice found at ﬁrst was in managing her ﬂamingo: she succeeded in getting its body tucked away, comfortably enough, under her arm, with its legs hanging down, but generally, just as she had got its neck nicely straightened out, and was going to give the hedgehog a blow with its head, it WOULD twist itself round and look up in her face, with such a puzzled expression that she could not help bursting out laughing: and when she had got its head down, and was going to begin again, it was very provoking to ﬁnd that the hedgehog had unrolled itself, and was in the act of crawling away: besides all this, there was generally a ridge or furrow in the way wherever she wanted to send the hedgehog to, and, as the doubled-up soldiers were always getting up and walking oﬀto other parts of the ground, Alice soon came to the conclusion that it was a very diﬃcult game indeed.",
      "context_incomplete": false
    },
    {
      "evidence_id": "E2",
      "preceding": "‘She boxed the Queen’s ears–’ the Rabbit began. Alice gave a little scream of laughter. ‘Oh, hush!’ the Rabbit whispered in a frightened tone. ‘The Queen will hear you! You see, she came rather late, and the Queen said–’",
      "supporting": "‘Get to your places!’ shouted the Queen in a voice of thunder, and peo- ple began running about in all directions, tumbling up against each other; however, they got settled down in a minute or two, and the game began. Alice thought she had never seen such a curious croquet-ground in her life; it was all ridges and furrows; the balls were live hedgehogs, the mallets live ﬂamingoes, and the soldiers had to double themselves up and to stand on their hands and feet, to make the arches.",
      "following": "The chief diﬃculty Alice found at ﬁrst was in managing her ﬂamingo: she succeeded in getting its body tucked away, comfortably enough, under her arm, with its legs hanging down, but generally, just as she had got its neck nicely straightened out, and was going to give the hedgehog a blow with its head, it WOULD twist itself round and look up in her face, with such a puzzled expression that she could not help bursting out laughing: and when she had got its head down, and was going to begin again, it was very provoking to ﬁnd that the hedgehog had unrolled itself, and was in the act of crawling away: besides all this, there was generally a ridge or furrow in the way wherever she wanted to send the hedgehog to, and, as the doubled-up soldiers were always getting up and walking oﬀto other parts of the ground, Alice soon came to the conclusion that it was a very diﬃcult game indeed.",
      "context_incomplete": false
    },
    {
      "evidence_id": "E3",
      "preceding": "‘She boxed the Queen’s ears–’ the Rabbit began. Alice gave a little scream of laughter. ‘Oh, hush!’ the Rabbit whispered in a frightened tone. ‘The Queen will hear you! You see, she came rather late, and the Queen said–’",
      "supporting": "‘Get to your places!’ shouted the Queen in a voice of thunder, and peo- ple began running about in all directions, tumbling up against each other; however, they got settled down in a minute or two, and the game began. Alice thought she had never seen such a curious croquet-ground in her life; it was all ridges and furrows; the balls were live hedgehogs, the mallets live ﬂamingoes, and the soldiers had to double themselves up and to stand on their hands and feet, to make the arches.",
      "following": "The chief diﬃculty Alice found at ﬁrst was in managing her ﬂamingo: she succeeded in getting its body tucked away, comfortably enough, under her arm, with its legs hanging down, but generally, just as she had got its neck nicely straightened out, and was going to give the hedgehog a blow with its head, it WOULD twist itself round and look up in her face, with such a puzzled expression that she could not help bursting out laughing: and when she had got its head down, and was going to begin again, it was very provoking to ﬁnd that the hedgehog had unrolled itself, and was in the act of crawling away: besides all this, there was generally a ridge or furrow in the way wherever she wanted to send the hedgehog to, and, as the doubled-up soldiers were always getting up and walking oﬀto other parts of the ground, Alice soon came to the conclusion that it was a very diﬃcult game indeed.",
      "context_incomplete": false
    }
  ],
  "primary_category": "multi_fact_single_context",
  "category": "multi_fact_single_context",
  "tags": [
    "historical_case",
    "phase4_reuse"
  ],
  "difficulty": "medium",
  "annotation_notes": "Reused historical Phase-4 case; proposed V2 classification does not change its old result. All three croquet-equipment facts occur in the same narrator sentence; this is not multi-source evidence.",
  "annotation_confidence": "medium",
  "historical_case": true,
  "requires_owner_attention": true,
  "negative_verification": null,
  "ambiguity_rationale": null,
  "expected_clarification": null,
  "evaluation_execution": null,
  "fact_family_id": "alice_croquet_equipment",
  "metamorphic_pair_id": "meta_croquet_equipment",
  "contrastive_pair_id": null,
  "related_case_ids": [
    "av042"
  ],
  "review_tier": "DEEP_REVIEW",
  "evidence_event_id": "event_alice_croquet_equipment",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "q024"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## q027

```json
{
  "case_id": "q027",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "What final actions complete the first figure of the Lobster Quadrille?",
  "expected_status": "answered",
  "reference_answer": "After changing lobsters and retiring, the dancers throw the lobsters out to sea, swim after them, turn a somersault, change lobsters again, and return to land; that completes the first figure.",
  "required_answer_claims": [
    {
      "claim_id": "C1",
      "claim_text": "They change lobsters and retire, then throw the lobsters to sea, swim after them, and somersault.",
      "evidence_ids": [
        "E1"
      ]
    },
    {
      "claim_id": "C2",
      "claim_text": "They change lobsters again and return to land to finish the first figure.",
      "evidence_ids": [
        "E2"
      ]
    }
  ],
  "valid_evidence_locations": [
    {
      "evidence_id": "E1",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 73,
        "chapter": "10",
        "pdf_block": 5
      },
      "exact_supporting_span": "change lobsters, and retire in same order",
      "preceding_context": "‘No, indeed,’ said Alice. ‘What sort of a dance is it?’ ‘Why,’ said the Gryphon, ‘you ﬁrst form into a line along the sea-shore–’ ‘Two lines!’ cried the Mock Turtle. ‘Seals, turtles, salmon, and so on; then, when you’ve cleared all the jelly-ﬁsh out of the way–’",
      "supporting_context": "‘THAT generally takes some time,’ interrupted the Gryphon. ‘–you advance twice–’ ‘Each with a lobster as a partner!’ cried the Gryphon. ‘Of course,’ the Mock Turtle said: ‘advance twice, set to partners–’ ‘–change lobsters, and retire in same order,’ continued the Gryphon. ‘Then, you know,’ the Mock Turtle went on, ‘you throw the–’ ‘The lobsters!’ shouted the Gryphon, with a bound into the air. ‘–as far out to sea as you can–’ ‘Swim after them!’ screamed the Gryphon. ‘Turn a somersault in the sea!’ cried the Mock Turtle, capering wildly about.",
      "following_context": "‘Change lobsters again!’ yelled the Gryphon at the top of its voice. ‘Back to land again, and that’s all the ﬁrst ﬁgure,’ said the Mock Turtle, suddenly dropping his voice; and the two creatures, who had been jumping about like mad things all this time, sat down again very sadly and quietly, and looked at Alice.",
      "why_supports": "The cited span and its adjacent discourse support: They change lobsters and retire, then throw the lobsters to sea, swim after them, and somersault.",
      "epistemic_status": "character_statement",
      "context_incomplete": false
    },
    {
      "evidence_id": "E2",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 74,
        "chapter": "10",
        "pdf_block": 1
      },
      "exact_supporting_span": "Back to land again, and that’s all the first figure",
      "preceding_context": "‘THAT generally takes some time,’ interrupted the Gryphon. ‘–you advance twice–’ ‘Each with a lobster as a partner!’ cried the Gryphon. ‘Of course,’ the Mock Turtle said: ‘advance twice, set to partners–’ ‘–change lobsters, and retire in same order,’ continued the Gryphon. ‘Then, you know,’ the Mock Turtle went on, ‘you throw the–’ ‘The lobsters!’ shouted the Gryphon, with a bound into the air. ‘–as far out to sea as you can–’ ‘Swim after them!’ screamed the Gryphon. ‘Turn a somersault in the sea!’ cried the Mock Turtle, capering wildly about.",
      "supporting_context": "‘Change lobsters again!’ yelled the Gryphon at the top of its voice. ‘Back to land again, and that’s all the ﬁrst ﬁgure,’ said the Mock Turtle, suddenly dropping his voice; and the two creatures, who had been jumping about like mad things all this time, sat down again very sadly and quietly, and looked at Alice.",
      "following_context": "‘It must be a very pretty dance,’ said Alice timidly. ‘Would you like to see a little of it?’ said the Mock Turtle. ‘Very much indeed,’ said Alice. ‘Come, let’s try the ﬁrst ﬁgure!’ said the Mock Turtle to the Gryphon. ‘We can do without lobsters, you know. Which shall sing?’",
      "why_supports": "The cited span and its adjacent discourse support: They change lobsters again and return to land to finish the first figure.",
      "epistemic_status": "character_statement",
      "context_incomplete": false
    }
  ],
  "exact_supporting_spans": [
    "change lobsters, and retire in same order",
    "Back to land again, and that’s all the first figure"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "E1",
      "preceding": "‘No, indeed,’ said Alice. ‘What sort of a dance is it?’ ‘Why,’ said the Gryphon, ‘you ﬁrst form into a line along the sea-shore–’ ‘Two lines!’ cried the Mock Turtle. ‘Seals, turtles, salmon, and so on; then, when you’ve cleared all the jelly-ﬁsh out of the way–’",
      "supporting": "‘THAT generally takes some time,’ interrupted the Gryphon. ‘–you advance twice–’ ‘Each with a lobster as a partner!’ cried the Gryphon. ‘Of course,’ the Mock Turtle said: ‘advance twice, set to partners–’ ‘–change lobsters, and retire in same order,’ continued the Gryphon. ‘Then, you know,’ the Mock Turtle went on, ‘you throw the–’ ‘The lobsters!’ shouted the Gryphon, with a bound into the air. ‘–as far out to sea as you can–’ ‘Swim after them!’ screamed the Gryphon. ‘Turn a somersault in the sea!’ cried the Mock Turtle, capering wildly about.",
      "following": "‘Change lobsters again!’ yelled the Gryphon at the top of its voice. ‘Back to land again, and that’s all the ﬁrst ﬁgure,’ said the Mock Turtle, suddenly dropping his voice; and the two creatures, who had been jumping about like mad things all this time, sat down again very sadly and quietly, and looked at Alice.",
      "context_incomplete": false
    },
    {
      "evidence_id": "E2",
      "preceding": "‘THAT generally takes some time,’ interrupted the Gryphon. ‘–you advance twice–’ ‘Each with a lobster as a partner!’ cried the Gryphon. ‘Of course,’ the Mock Turtle said: ‘advance twice, set to partners–’ ‘–change lobsters, and retire in same order,’ continued the Gryphon. ‘Then, you know,’ the Mock Turtle went on, ‘you throw the–’ ‘The lobsters!’ shouted the Gryphon, with a bound into the air. ‘–as far out to sea as you can–’ ‘Swim after them!’ screamed the Gryphon. ‘Turn a somersault in the sea!’ cried the Mock Turtle, capering wildly about.",
      "supporting": "‘Change lobsters again!’ yelled the Gryphon at the top of its voice. ‘Back to land again, and that’s all the ﬁrst ﬁgure,’ said the Mock Turtle, suddenly dropping his voice; and the two creatures, who had been jumping about like mad things all this time, sat down again very sadly and quietly, and looked at Alice.",
      "following": "‘It must be a very pretty dance,’ said Alice timidly. ‘Would you like to see a little of it?’ said the Mock Turtle. ‘Very much indeed,’ said Alice. ‘Come, let’s try the ﬁrst ﬁgure!’ said the Mock Turtle to the Gryphon. ‘We can do without lobsters, you know. Which shall sing?’",
      "context_incomplete": false
    }
  ],
  "primary_category": "multi_fact_single_context",
  "category": "multi_fact_single_context",
  "tags": [
    "historical_case",
    "known_bad_case",
    "phase4_reuse"
  ],
  "difficulty": "hard",
  "annotation_notes": "The old answer omitted throw/swim/somersault/change-again steps; the repaired answer covers the complete ending sequence. Reclassified from multi-source: the answer components belong to one continuous local event/context.",
  "annotation_confidence": "medium",
  "historical_case": true,
  "requires_owner_attention": true,
  "negative_verification": null,
  "ambiguity_rationale": null,
  "expected_clarification": null,
  "evaluation_execution": null,
  "fact_family_id": "fact_q027",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [],
  "review_tier": "DEEP_REVIEW",
  "evidence_event_id": "event_fact_q027",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "q027"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## q030

```json
{
  "case_id": "q030",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "Under Rule Forty-two, which people had to leave the court?",
  "expected_status": "answered",
  "reference_answer": "All persons more than a mile high.",
  "required_answer_claims": [
    {
      "claim_id": "C1",
      "claim_text": "All persons more than a mile high.",
      "evidence_ids": [
        "E1"
      ]
    }
  ],
  "valid_evidence_locations": [
    {
      "evidence_id": "E1",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 88,
        "chapter": "12",
        "pdf_block": 4
      },
      "exact_supporting_span": "more than a mile high",
      "preceding_context": "Some of the jury wrote it down ‘important,’ and some ‘unimportant.’ Alice could see this, as she was near enough to look over their slates; ‘but it doesn’t matter a bit,’ she thought to herself.",
      "supporting_context": "At this moment the King, who had been for some time busily writing in his note-book, cackled out ‘Silence!’ and read out from his book, ‘Rule Forty-two. ALL PERSONS MORE THAN A MILE HIGH TO LEAVE THE COURT.’",
      "following_context": "Everybody looked at Alice. ‘I’M not a mile high,’ said Alice. ‘You are,’ said the King. ‘Nearly two miles high,’ added the Queen. ‘Well, I shan’t go, at any rate,’ said Alice: ‘besides, that’s not a regular rule: you invented it just now.’",
      "why_supports": "The cited span and its adjacent discourse support: All persons more than a mile high.",
      "context_incomplete": false,
      "epistemic_status": "character_statement"
    }
  ],
  "exact_supporting_spans": [
    "more than a mile high"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "E1",
      "preceding": "Some of the jury wrote it down ‘important,’ and some ‘unimportant.’ Alice could see this, as she was near enough to look over their slates; ‘but it doesn’t matter a bit,’ she thought to herself.",
      "supporting": "At this moment the King, who had been for some time busily writing in his note-book, cackled out ‘Silence!’ and read out from his book, ‘Rule Forty-two. ALL PERSONS MORE THAN A MILE HIGH TO LEAVE THE COURT.’",
      "following": "Everybody looked at Alice. ‘I’M not a mile high,’ said Alice. ‘You are,’ said the King. ‘Nearly two miles high,’ added the Queen. ‘Well, I shan’t go, at any rate,’ said Alice: ‘besides, that’s not a regular rule: you invented it just now.’",
      "context_incomplete": false
    }
  ],
  "primary_category": "direct_factual_single_source",
  "category": "direct_factual_single_source",
  "tags": [
    "character_statement",
    "historical_case",
    "known_bad_case",
    "phase4_reuse",
    "rule_content"
  ],
  "difficulty": "medium",
  "annotation_notes": "Direct question about the content of the King’s stated Rule Forty-two. It is not a contrastive item; the evidence establishes what the King read out, not the legitimacy of the rule.",
  "annotation_confidence": "high",
  "historical_case": true,
  "requires_owner_attention": true,
  "negative_verification": null,
  "ambiguity_rationale": null,
  "expected_clarification": null,
  "evaluation_execution": null,
  "fact_family_id": "fact_q030",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [],
  "review_tier": "DEEP_REVIEW",
  "evidence_event_id": "event_fact_q030",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "q030"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## at106

```json
{
  "case_id": "at106",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_final_test",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "How did Alice distract the enormous puppy and get away?",
  "expected_status": "answered",
  "reference_answer": "She held out a stick and dodged around a thistle while the puppy charged; when it tired and sat panting, she ran away.",
  "required_answer_claims": [
    {
      "claim_id": "C1",
      "claim_text": "Alice distracted the puppy with a stick and the thistle.",
      "evidence_ids": [
        "E1",
        "E2"
      ]
    },
    {
      "claim_id": "C2",
      "claim_text": "She escaped when the puppy became tired and stopped at a distance.",
      "evidence_ids": [
        "E2",
        "E3"
      ]
    }
  ],
  "valid_evidence_locations": [
    {
      "evidence_id": "E1",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 35,
        "chapter": "4",
        "pdf_block": 9
      },
      "exact_supporting_span": "she picked up a little bit of stick, and held it out to the puppy",
      "preceding_context": "An enormous puppy was looking down at her with large round eyes, and feebly stretching out one paw, trying to touch her. ‘Poor little thing!’ said Alice, in a coaxing tone, and she tried hard to whistle to it; but she was terribly frightened all the time at the thought that it might be hungry, in which case it would be very likely to eat her up in spite of all her coaxing.",
      "supporting_context": "Hardly knowing what she did, she picked up a little bit of stick, and held it out to the puppy; whereupon the puppy jumped into the air oﬀall its feet at once, with a yelp of delight, and rushed at the stick, and made believe to worry it; then Alice dodged behind a great thistle, to keep herself from being",
      "following_context": "run over; and the moment she appeared on the other side, the puppy made another rush at the stick, and tumbled head over heels in its hurry to get hold of it; then Alice, thinking it was very like having a game of play with a cart-horse, and expecting every moment to be trampled under its feet, ran round the thistle again; then the puppy began a series of short charges at the stick, running a very little way forwards each time and a long way back, and barking hoarsely all the while, till at last it sat down a good way oﬀ, panting, with its tongue hanging out of its mouth, and its great eyes half shut.",
      "why_supports": "The cited span and its adjacent discourse support: Alice distracted the puppy with a stick and the thistle.",
      "epistemic_status": "narrator_fact",
      "context_incomplete": false
    },
    {
      "evidence_id": "E2",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 36,
        "chapter": "4",
        "pdf_block": 1
      },
      "exact_supporting_span": "ran round the thistle again",
      "preceding_context": "Hardly knowing what she did, she picked up a little bit of stick, and held it out to the puppy; whereupon the puppy jumped into the air oﬀall its feet at once, with a yelp of delight, and rushed at the stick, and made believe to worry it; then Alice dodged behind a great thistle, to keep herself from being",
      "supporting_context": "run over; and the moment she appeared on the other side, the puppy made another rush at the stick, and tumbled head over heels in its hurry to get hold of it; then Alice, thinking it was very like having a game of play with a cart-horse, and expecting every moment to be trampled under its feet, ran round the thistle again; then the puppy began a series of short charges at the stick, running a very little way forwards each time and a long way back, and barking hoarsely all the while, till at last it sat down a good way oﬀ, panting, with its tongue hanging out of its mouth, and its great eyes half shut.",
      "following_context": "This seemed to Alice a good opportunity for making her escape; so she set oﬀat once, and ran till she was quite tired and out of breath, and till the puppy’s bark sounded quite faint in the distance.",
      "why_supports": "The cited span and its adjacent discourse support: Alice distracted the puppy with a stick and the thistle.; She escaped when the puppy became tired and stopped at a distance.",
      "epistemic_status": "narrator_fact",
      "context_incomplete": false
    },
    {
      "evidence_id": "E3",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 36,
        "chapter": "4",
        "pdf_block": 2
      },
      "exact_supporting_span": "This seemed to Alice a good opportunity for making her escape",
      "preceding_context": "run over; and the moment she appeared on the other side, the puppy made another rush at the stick, and tumbled head over heels in its hurry to get hold of it; then Alice, thinking it was very like having a game of play with a cart-horse, and expecting every moment to be trampled under its feet, ran round the thistle again; then the puppy began a series of short charges at the stick, running a very little way forwards each time and a long way back, and barking hoarsely all the while, till at last it sat down a good way oﬀ, panting, with its tongue hanging out of its mouth, and its great eyes half shut.",
      "supporting_context": "This seemed to Alice a good opportunity for making her escape; so she set oﬀat once, and ran till she was quite tired and out of breath, and till the puppy’s bark sounded quite faint in the distance.",
      "following_context": "‘And yet what a dear little puppy it was!’ said Alice, as she leant against a buttercup to rest herself, and fanned herself with one of the leaves: ‘I should have liked teaching it tricks very much, if–if I’d only been the right size to do it! Oh dear! I’d nearly forgotten that I’ve got to grow up again! Let me see–how IS it to be managed? I suppose I ought to eat or drink something or other; but the great question is, what?’",
      "why_supports": "The cited span and its adjacent discourse support: She escaped when the puppy became tired and stopped at a distance.",
      "epistemic_status": "narrator_fact",
      "context_incomplete": false
    }
  ],
  "exact_supporting_spans": [
    "she picked up a little bit of stick, and held it out to the puppy",
    "ran round the thistle again",
    "This seemed to Alice a good opportunity for making her escape"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "E1",
      "preceding": "An enormous puppy was looking down at her with large round eyes, and feebly stretching out one paw, trying to touch her. ‘Poor little thing!’ said Alice, in a coaxing tone, and she tried hard to whistle to it; but she was terribly frightened all the time at the thought that it might be hungry, in which case it would be very likely to eat her up in spite of all her coaxing.",
      "supporting": "Hardly knowing what she did, she picked up a little bit of stick, and held it out to the puppy; whereupon the puppy jumped into the air oﬀall its feet at once, with a yelp of delight, and rushed at the stick, and made believe to worry it; then Alice dodged behind a great thistle, to keep herself from being",
      "following": "run over; and the moment she appeared on the other side, the puppy made another rush at the stick, and tumbled head over heels in its hurry to get hold of it; then Alice, thinking it was very like having a game of play with a cart-horse, and expecting every moment to be trampled under its feet, ran round the thistle again; then the puppy began a series of short charges at the stick, running a very little way forwards each time and a long way back, and barking hoarsely all the while, till at last it sat down a good way oﬀ, panting, with its tongue hanging out of its mouth, and its great eyes half shut.",
      "context_incomplete": false
    },
    {
      "evidence_id": "E2",
      "preceding": "Hardly knowing what she did, she picked up a little bit of stick, and held it out to the puppy; whereupon the puppy jumped into the air oﬀall its feet at once, with a yelp of delight, and rushed at the stick, and made believe to worry it; then Alice dodged behind a great thistle, to keep herself from being",
      "supporting": "run over; and the moment she appeared on the other side, the puppy made another rush at the stick, and tumbled head over heels in its hurry to get hold of it; then Alice, thinking it was very like having a game of play with a cart-horse, and expecting every moment to be trampled under its feet, ran round the thistle again; then the puppy began a series of short charges at the stick, running a very little way forwards each time and a long way back, and barking hoarsely all the while, till at last it sat down a good way oﬀ, panting, with its tongue hanging out of its mouth, and its great eyes half shut.",
      "following": "This seemed to Alice a good opportunity for making her escape; so she set oﬀat once, and ran till she was quite tired and out of breath, and till the puppy’s bark sounded quite faint in the distance.",
      "context_incomplete": false
    },
    {
      "evidence_id": "E3",
      "preceding": "run over; and the moment she appeared on the other side, the puppy made another rush at the stick, and tumbled head over heels in its hurry to get hold of it; then Alice, thinking it was very like having a game of play with a cart-horse, and expecting every moment to be trampled under its feet, ran round the thistle again; then the puppy began a series of short charges at the stick, running a very little way forwards each time and a long way back, and barking hoarsely all the while, till at last it sat down a good way oﬀ, panting, with its tongue hanging out of its mouth, and its great eyes half shut.",
      "supporting": "This seemed to Alice a good opportunity for making her escape; so she set oﬀat once, and ran till she was quite tired and out of breath, and till the puppy’s bark sounded quite faint in the distance.",
      "following": "‘And yet what a dear little puppy it was!’ said Alice, as she leant against a buttercup to rest herself, and fanned herself with one of the leaves: ‘I should have liked teaching it tricks very much, if–if I’d only been the right size to do it! Oh dear! I’d nearly forgotten that I’ve got to grow up again! Let me see–how IS it to be managed? I suppose I ought to eat or drink something or other; but the great question is, what?’",
      "context_incomplete": false
    }
  ],
  "primary_category": "multi_fact_single_context",
  "category": "multi_fact_single_context",
  "tags": [],
  "difficulty": "hard",
  "annotation_notes": "Cross-page action sequence with distinct setup and outcome evidence. Reclassified from multi-source: the answer components belong to one continuous local event/context.",
  "annotation_confidence": "medium",
  "review_tier": "DEEP_REVIEW",
  "historical_case": false,
  "requires_owner_attention": true,
  "negative_verification": null,
  "ambiguity_rationale": null,
  "ambiguity_type": null,
  "plausible_referents": [],
  "expected_clarification": null,
  "evaluation_execution": null,
  "fact_family_id": "fact_at106",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [],
  "evidence_event_id": "event_fact_at106",
  "development_exposure": {
    "status": "no_known_development_exposure",
    "sources": [],
    "review_method": "Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants."
  }
}
```

---

## at110

```json
{
  "case_id": "at110",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_final_test",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "Could the executioner behead the Cheshire Cat’s visible head, according to both sides of the dispute?",
  "expected_status": "answered",
  "reference_answer": "They disagreed: the executioner said a head could not be cut off without a body, while the King said anything with a head could be beheaded.",
  "required_answer_claims": [
    {
      "claim_id": "C1",
      "claim_text": "The executioner said a body was required.",
      "evidence_ids": [
        "E1"
      ]
    },
    {
      "claim_id": "C2",
      "claim_text": "The King argued that possessing a head was sufficient.",
      "evidence_ids": [
        "E2"
      ]
    }
  ],
  "valid_evidence_locations": [
    {
      "evidence_id": "E1",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 64,
        "chapter": "8",
        "pdf_block": 6
      },
      "exact_supporting_span": "you couldn’t cut oﬀa head unless there was a body to cut it oﬀfrom",
      "preceding_context": "The moment Alice appeared, she was appealed to by all three to settle the question, and they repeated their arguments to her, though, as they all spoke at once, she found it very hard indeed to make out exactly what they said.",
      "supporting_context": "The executioner’s argument was, that you couldn’t cut oﬀa head unless there was a body to cut it oﬀfrom: that he had never had to do such a thing before, and he wasn’t going to begin at HIS time of life.",
      "following_context": "The King’s argument was, that anything that had a head could be be- headed, and that you weren’t to talk nonsense.",
      "why_supports": "The narrator reports the executioner’s position that beheading requires a body.",
      "epistemic_status": "narrator_fact",
      "context_incomplete": false
    },
    {
      "evidence_id": "E2",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 64,
        "chapter": "8",
        "pdf_block": 7
      },
      "exact_supporting_span": "anything that had a head could be be- headed",
      "preceding_context": "The executioner’s argument was, that you couldn’t cut oﬀa head unless there was a body to cut it oﬀfrom: that he had never had to do such a thing before, and he wasn’t going to begin at HIS time of life.",
      "supporting_context": "The King’s argument was, that anything that had a head could be be- headed, and that you weren’t to talk nonsense.",
      "following_context": "The Queen’s argument was, that if something wasn’t done about it in less than no time she’d have everybody executed, all round. (It was this last remark that had made the whole party look so grave and anxious.)",
      "why_supports": "The narrator reports the King’s opposing position that having a head is sufficient for beheading.",
      "epistemic_status": "narrator_fact",
      "context_incomplete": false
    }
  ],
  "exact_supporting_spans": [
    "you couldn’t cut oﬀa head unless there was a body to cut it oﬀfrom",
    "anything that had a head could be be- headed"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "E1",
      "preceding": "The moment Alice appeared, she was appealed to by all three to settle the question, and they repeated their arguments to her, though, as they all spoke at once, she found it very hard indeed to make out exactly what they said.",
      "supporting": "The executioner’s argument was, that you couldn’t cut oﬀa head unless there was a body to cut it oﬀfrom: that he had never had to do such a thing before, and he wasn’t going to begin at HIS time of life.",
      "following": "The King’s argument was, that anything that had a head could be be- headed, and that you weren’t to talk nonsense.",
      "context_incomplete": false
    },
    {
      "evidence_id": "E2",
      "preceding": "The executioner’s argument was, that you couldn’t cut oﬀa head unless there was a body to cut it oﬀfrom: that he had never had to do such a thing before, and he wasn’t going to begin at HIS time of life.",
      "supporting": "The King’s argument was, that anything that had a head could be be- headed, and that you weren’t to talk nonsense.",
      "following": "The Queen’s argument was, that if something wasn’t done about it in less than no time she’d have everybody executed, all round. (It was this last remark that had made the whole party look so grave and anxious.)",
      "context_incomplete": false
    }
  ],
  "primary_category": "contrastive_distractor",
  "category": "contrastive_distractor",
  "tags": [],
  "difficulty": "hard",
  "annotation_notes": "Competing propositions from two sides remain distinct. Exact spans now contain the propositions themselves; epistemic status records that narration reports each argument, not that either argument is objectively true.",
  "annotation_confidence": "medium",
  "review_tier": "DEEP_REVIEW",
  "historical_case": false,
  "requires_owner_attention": true,
  "negative_verification": null,
  "ambiguity_rationale": null,
  "ambiguity_type": null,
  "plausible_referents": [],
  "expected_clarification": null,
  "evaluation_execution": null,
  "fact_family_id": "fact_at110",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [],
  "evidence_event_id": "event_fact_at110",
  "development_exposure": {
    "status": "no_known_development_exposure",
    "sources": [],
    "review_method": "Compared with DEV answers, preceding/supporting/following context, negative-search excerpts, ambiguity evidence, and declared variants."
  }
}
```

---

## q018

```json
{
  "case_id": "q018",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "Why did the Pigeon call Alice a serpent?",
  "expected_status": "answered",
  "reference_answer": "The Pigeon was guarding its eggs against serpents and, seeing Alice’s unusually long neck, insisted she was a serpent. When Alice said little girls eat eggs too, the Pigeon replied conditionally that if that were true, little girls were a kind of serpent.",
  "required_answer_claims": [
    {
      "claim_id": "C1",
      "claim_text": "The Pigeon was watching its eggs for serpents and treated Alice’s unusually long neck as a reason to call her a serpent.",
      "evidence_ids": [
        "E1",
        "E2"
      ]
    },
    {
      "claim_id": "C2",
      "claim_text": "After Alice said little girls eat eggs, the Pigeon said conditionally that if girls do eat eggs, they are a kind of serpent.",
      "evidence_ids": [
        "E2"
      ]
    }
  ],
  "valid_evidence_locations": [
    {
      "evidence_id": "E1",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 41,
        "chapter": "5",
        "pdf_block": 6
      },
      "exact_supporting_span": "As if it wasn’t trouble enough hatching the eggs",
      "preceding_context": "Alice was more and more puzzled, but she thought there was no use in saying anything more till the Pigeon had ﬁnished.",
      "supporting_context": "‘As if it wasn’t trouble enough hatching the eggs,’ said the Pigeon; ‘but I must be on the look-out for serpents night and day! Why, I haven’t had a wink of sleep these three weeks!’",
      "following_context": "‘I’m very sorry you’ve been annoyed,’ said Alice, who was beginning to see its meaning.",
      "why_supports": "The cited span and its adjacent discourse support: The Pigeon was exhausted from guarding its eggs against serpents.",
      "context_incomplete": false,
      "epistemic_status": "character_statement"
    },
    {
      "evidence_id": "E2",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 42,
        "chapter": "5",
        "pdf_block": 2
      },
      "exact_supporting_span": "No, no! You’re a serpent; and there’s no use denying it.",
      "preceding_context": "The Pigeon challenges Alice’s claim that she is a little girl and focuses on her altered appearance.",
      "supporting_context": "neck as that! No, no! You’re a serpent; and there’s no use denying it. I suppose you’ll be telling me next that you never tasted an egg!’ ‘I HAVE tasted eggs, certainly,’ said Alice, who was a very truthful child; ‘but little girls eat eggs quite as much as serpents do, you know.’ ‘I don’t believe it,’ said the Pigeon; ‘but if they do, why then they’re a kind of serpent, that’s all I can say.’",
      "following_context": "The exchange continues with the Pigeon accusing Alice of looking for eggs.",
      "why_supports": "The continuous dialogue shows the Pigeon’s long-neck accusation and later conditional egg-based reasoning; both are character beliefs, not narrator facts.",
      "context_incomplete": false,
      "epistemic_status": "character_statement"
    }
  ],
  "exact_supporting_spans": [
    "As if it wasn’t trouble enough hatching the eggs",
    "No, no! You’re a serpent; and there’s no use denying it."
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "E1",
      "preceding": "Alice was more and more puzzled, but she thought there was no use in saying anything more till the Pigeon had ﬁnished.",
      "supporting": "‘As if it wasn’t trouble enough hatching the eggs,’ said the Pigeon; ‘but I must be on the look-out for serpents night and day! Why, I haven’t had a wink of sleep these three weeks!’",
      "following": "‘I’m very sorry you’ve been annoyed,’ said Alice, who was beginning to see its meaning.",
      "context_incomplete": false
    },
    {
      "evidence_id": "E2",
      "preceding": "The Pigeon challenges Alice’s claim that she is a little girl and focuses on her altered appearance.",
      "supporting": "neck as that! No, no! You’re a serpent; and there’s no use denying it. I suppose you’ll be telling me next that you never tasted an egg!’ ‘I HAVE tasted eggs, certainly,’ said Alice, who was a very truthful child; ‘but little girls eat eggs quite as much as serpents do, you know.’ ‘I don’t believe it,’ said the Pigeon; ‘but if they do, why then they’re a kind of serpent, that’s all I can say.’",
      "following": "The exchange continues with the Pigeon accusing Alice of looking for eggs.",
      "context_incomplete": false
    }
  ],
  "primary_category": "local_context_reasoning",
  "category": "local_context_reasoning",
  "tags": [
    "historical_case",
    "phase4_reuse"
  ],
  "difficulty": "hard",
  "annotation_notes": "Preserves chronology and epistemic status: long-neck suspicion first, then conditional reasoning about girls eating eggs. Linked to av039: distinct target claim, shared source event; fact-family IDs are not independent-event counts.",
  "annotation_confidence": "medium",
  "historical_case": true,
  "requires_owner_attention": true,
  "negative_verification": null,
  "ambiguity_rationale": null,
  "expected_clarification": null,
  "evaluation_execution": null,
  "fact_family_id": "fact_q018",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [
    "av039"
  ],
  "review_tier": "DEEP_REVIEW",
  "evidence_event_id": "event_alice_pigeon_serpent_reasoning",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "q018"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## av039

```json
{
  "case_id": "av039",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "Did the Pigeon accept Alice’s claim that she was a little girl? Why?",
  "expected_status": "answered",
  "reference_answer": "No. The Pigeon insisted she was a serpent because of her unusual neck and her admission that little girls eat eggs.",
  "required_answer_claims": [
    {
      "claim_id": "C1",
      "claim_text": "The Pigeon rejected Alice’s little-girl claim because of her neck.",
      "evidence_ids": [
        "E1",
        "E2"
      ]
    },
    {
      "claim_id": "C2",
      "claim_text": "The Pigeon connected egg-eating with being a serpent.",
      "evidence_ids": [
        "E3"
      ]
    }
  ],
  "valid_evidence_locations": [
    {
      "evidence_id": "E1",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 41,
        "chapter": "5",
        "pdf_block": 11
      },
      "exact_supporting_span": "never ONE with such a",
      "preceding_context": "‘I–I’m a little girl,’ said Alice, rather doubtfully, as she remembered the number of changes she had gone through that day.",
      "supporting_context": "‘A likely story indeed!’ said the Pigeon in a tone of the deepest contempt. ‘I’ve seen a good many little girls in my time, but never ONE with such a",
      "following_context": "neck as that! No, no! You’re a serpent; and there’s no use denying it. I suppose you’ll be telling me next that you never tasted an egg!’",
      "why_supports": "The cited span and its adjacent discourse support: The Pigeon rejected Alice’s little-girl claim because of her neck.",
      "context_incomplete": false,
      "epistemic_status": "character_statement"
    },
    {
      "evidence_id": "E2",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 42,
        "chapter": "5",
        "pdf_block": 1
      },
      "exact_supporting_span": "neck as that! No, no! You’re a serpent",
      "preceding_context": "‘A likely story indeed!’ said the Pigeon in a tone of the deepest contempt. ‘I’ve seen a good many little girls in my time, but never ONE with such a",
      "supporting_context": "neck as that! No, no! You’re a serpent; and there’s no use denying it. I suppose you’ll be telling me next that you never tasted an egg!’",
      "following_context": "‘I HAVE tasted eggs, certainly,’ said Alice, who was a very truthful child; ‘but little girls eat eggs quite as much as serpents do, you know.’",
      "why_supports": "The cited span and its adjacent discourse support: The Pigeon rejected Alice’s little-girl claim because of her neck.",
      "context_incomplete": false,
      "epistemic_status": "character_statement"
    },
    {
      "evidence_id": "E3",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 42,
        "chapter": "5",
        "pdf_block": 2
      },
      "exact_supporting_span": "little girls eat eggs quite as much as serpents do",
      "preceding_context": "neck as that! No, no! You’re a serpent; and there’s no use denying it. I suppose you’ll be telling me next that you never tasted an egg!’",
      "supporting_context": "‘I HAVE tasted eggs, certainly,’ said Alice, who was a very truthful child; ‘but little girls eat eggs quite as much as serpents do, you know.’",
      "following_context": "‘I don’t believe it,’ said the Pigeon; ‘but if they do, why then they’re a kind of serpent, that’s all I can say.’",
      "why_supports": "The cited span and its adjacent discourse support: The Pigeon connected egg-eating with being a serpent.",
      "context_incomplete": false,
      "epistemic_status": "character_statement"
    }
  ],
  "exact_supporting_spans": [
    "never ONE with such a",
    "neck as that! No, no! You’re a serpent",
    "little girls eat eggs quite as much as serpents do"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "E1",
      "preceding": "‘I–I’m a little girl,’ said Alice, rather doubtfully, as she remembered the number of changes she had gone through that day.",
      "supporting": "‘A likely story indeed!’ said the Pigeon in a tone of the deepest contempt. ‘I’ve seen a good many little girls in my time, but never ONE with such a",
      "following": "neck as that! No, no! You’re a serpent; and there’s no use denying it. I suppose you’ll be telling me next that you never tasted an egg!’",
      "context_incomplete": false
    },
    {
      "evidence_id": "E2",
      "preceding": "‘A likely story indeed!’ said the Pigeon in a tone of the deepest contempt. ‘I’ve seen a good many little girls in my time, but never ONE with such a",
      "supporting": "neck as that! No, no! You’re a serpent; and there’s no use denying it. I suppose you’ll be telling me next that you never tasted an egg!’",
      "following": "‘I HAVE tasted eggs, certainly,’ said Alice, who was a very truthful child; ‘but little girls eat eggs quite as much as serpents do, you know.’",
      "context_incomplete": false
    },
    {
      "evidence_id": "E3",
      "preceding": "neck as that! No, no! You’re a serpent; and there’s no use denying it. I suppose you’ll be telling me next that you never tasted an egg!’",
      "supporting": "‘I HAVE tasted eggs, certainly,’ said Alice, who was a very truthful child; ‘but little girls eat eggs quite as much as serpents do, you know.’",
      "following": "‘I don’t believe it,’ said the Pigeon; ‘but if they do, why then they’re a kind of serpent, that’s all I can say.’",
      "context_incomplete": false
    }
  ],
  "primary_category": "local_context_reasoning",
  "category": "local_context_reasoning",
  "tags": [
    "character_belief",
    "negation"
  ],
  "difficulty": "hard",
  "annotation_notes": "Linked to q018: distinct target claim, shared source event; fact-family IDs are not independent-event counts.",
  "annotation_confidence": "medium",
  "historical_case": false,
  "requires_owner_attention": true,
  "negative_verification": null,
  "ambiguity_rationale": null,
  "expected_clarification": null,
  "evaluation_execution": null,
  "fact_family_id": "fact_av039",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [
    "q018"
  ],
  "review_tier": "DEEP_REVIEW",
  "evidence_event_id": "event_alice_pigeon_serpent_reasoning",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "av039"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## q023

```json
{
  "case_id": "q023",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "Why was it always tea-time at the Hatter's table?",
  "expected_status": "answered",
  "reference_answer": "The Hatter said he and Time had quarreled. After the concert incident, Time would no longer do anything the Hatter asked, so it stayed six o’clock and therefore was always tea-time.",
  "required_answer_claims": [
    {
      "claim_id": "C1",
      "claim_text": "The Hatter said he had quarreled with Time and that afterward Time would no longer do what he asked.",
      "evidence_ids": [
        "E1"
      ]
    },
    {
      "claim_id": "C2",
      "claim_text": "The Hatter said it stayed six o’clock and confirmed that this was why it was always tea-time.",
      "evidence_ids": [
        "E1",
        "E2"
      ]
    }
  ],
  "valid_evidence_locations": [
    {
      "evidence_id": "E1",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 54,
        "chapter": "7",
        "pdf_block": 6
      },
      "exact_supporting_span": "It’s always six o’clock now",
      "preceding_context": "The Hatter personifies Time and says that if one stays on good terms with him, Time can move or hold the clock as requested. When Alice asks whether that is how the Hatter manages, he says no and explains that they quarrelled last March.",
      "supporting_context": "The Hatter says that at the concert the Queen cried, ‘He’s murdering the time! Off with his head!’ He continues that ever since then, Time ‘won’t do a thing I ask! It’s always six o’clock now.’",
      "following_context": "A bright idea came into Alice’s head. ‘Is that the reason so many tea- things are put out here?’ she asked.",
      "why_supports": "The expanded context resolves ‘he’ as Time and supplies the quarrel to non-cooperation to six-o’clock causal chain.",
      "context_incomplete": false,
      "epistemic_status": "character_statement"
    },
    {
      "evidence_id": "E2",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 54,
        "chapter": "7",
        "pdf_block": 8
      },
      "exact_supporting_span": "it’s always tea-time",
      "preceding_context": "A bright idea came into Alice’s head. ‘Is that the reason so many tea- things are put out here?’ she asked.",
      "supporting_context": "‘Yes, that’s it,’ said the Hatter with a sigh: ‘it’s always tea-time, and we’ve no time to wash the things between whiles.’",
      "following_context": "‘Then you keep moving round, I suppose?’ said Alice. ‘Exactly so,’ said the Hatter: ‘as the things get used up.’ ‘But what happens when you come to the beginning again?’ Alice ven- tured to ask.",
      "why_supports": "The cited span and its adjacent discourse support: The time remained six o’clock, which made it perpetually tea-time.",
      "context_incomplete": false,
      "epistemic_status": "character_statement"
    }
  ],
  "exact_supporting_spans": [
    "It’s always six o’clock now",
    "it’s always tea-time"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "E1",
      "preceding": "The Hatter personifies Time and says that if one stays on good terms with him, Time can move or hold the clock as requested. When Alice asks whether that is how the Hatter manages, he says no and explains that they quarrelled last March.",
      "supporting": "The Hatter says that at the concert the Queen cried, ‘He’s murdering the time! Off with his head!’ He continues that ever since then, Time ‘won’t do a thing I ask! It’s always six o’clock now.’",
      "following": "A bright idea came into Alice’s head. ‘Is that the reason so many tea- things are put out here?’ she asked.",
      "context_incomplete": false
    },
    {
      "evidence_id": "E2",
      "preceding": "A bright idea came into Alice’s head. ‘Is that the reason so many tea- things are put out here?’ she asked.",
      "supporting": "‘Yes, that’s it,’ said the Hatter with a sigh: ‘it’s always tea-time, and we’ve no time to wash the things between whiles.’",
      "following": "‘Then you keep moving round, I suppose?’ said Alice. ‘Exactly so,’ said the Hatter: ‘as the things get used up.’ ‘But what happens when you come to the beginning again?’ Alice ven- tured to ask.",
      "context_incomplete": false
    }
  ],
  "primary_category": "local_context_reasoning",
  "category": "local_context_reasoning",
  "tags": [
    "historical_case",
    "phase4_reuse"
  ],
  "difficulty": "medium",
  "annotation_notes": "Evidence now includes the Time antecedent and causal chain through permanent six o’clock and tea-time. Linked to av037: distinct target claim, shared source event; fact-family IDs are not independent-event counts.",
  "annotation_confidence": "medium",
  "historical_case": true,
  "requires_owner_attention": true,
  "negative_verification": null,
  "ambiguity_rationale": null,
  "expected_clarification": null,
  "evaluation_execution": null,
  "fact_family_id": "fact_q023",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [
    "av037"
  ],
  "review_tier": "DEEP_REVIEW",
  "evidence_event_id": "event_alice_hatter_time_quarrel",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "q023"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## av037

```json
{
  "case_id": "av037",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "In the tea-party scene, who does the Hatter mean by “he” in “he won’t do a thing I ask”?",
  "expected_status": "answered",
  "reference_answer": "He means Time.",
  "required_answer_claims": [
    {
      "claim_id": "C1",
      "claim_text": "The pronoun “he” refers to the personified Time.",
      "evidence_ids": [
        "E1",
        "E2"
      ]
    }
  ],
  "valid_evidence_locations": [
    {
      "evidence_id": "E1",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 53,
        "chapter": "7",
        "pdf_block": 5
      },
      "exact_supporting_span": "If you knew Time as well as I do",
      "preceding_context": "‘Have you guessed the riddle yet?’ the Hatter said, turning to Alice again. ‘No, I give it up,’ Alice replied: ‘what’s the answer?’ ‘I haven’t the slightest idea,’ said the Hatter. ‘Nor I,’ said the March Hare. Alice sighed wearily. ‘I think you might do something better with the time,’ she said, ‘than waste it in asking riddles that have no answers.’",
      "supporting_context": "‘If you knew Time as well as I do,’ said the Hatter, ‘you wouldn’t talk about wasting IT. It’s HIM.’",
      "following_context": "‘I don’t know what you mean,’ said Alice. ‘Of course you don’t!’ the Hatter said, tossing his head contemptuously. ‘I dare say you never even spoke to Time!’",
      "why_supports": "The cited span and its adjacent discourse support: The pronoun “he” refers to the personified Time.",
      "context_incomplete": false,
      "epistemic_status": "character_statement"
    },
    {
      "evidence_id": "E2",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 54,
        "chapter": "7",
        "pdf_block": 6
      },
      "exact_supporting_span": "he won’t do a thing I ask",
      "preceding_context": "‘Well, I’d hardly ﬁnished the ﬁrst verse,’ said the Hatter, ‘when the Queen jumped up and bawled out, “He’s murdering the time! Oﬀwith his head!”’",
      "supporting_context": "‘How dreadfully savage!’ exclaimed Alice. ‘And ever since that,’ the Hatter went on in a mournful tone, ‘he won’t do a thing I ask! It’s always six o’clock now.’",
      "following_context": "A bright idea came into Alice’s head. ‘Is that the reason so many tea- things are put out here?’ she asked.",
      "why_supports": "The cited span and its adjacent discourse support: The pronoun “he” refers to the personified Time.",
      "context_incomplete": false,
      "epistemic_status": "character_statement"
    }
  ],
  "exact_supporting_spans": [
    "If you knew Time as well as I do",
    "he won’t do a thing I ask"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "E1",
      "preceding": "‘Have you guessed the riddle yet?’ the Hatter said, turning to Alice again. ‘No, I give it up,’ Alice replied: ‘what’s the answer?’ ‘I haven’t the slightest idea,’ said the Hatter. ‘Nor I,’ said the March Hare. Alice sighed wearily. ‘I think you might do something better with the time,’ she said, ‘than waste it in asking riddles that have no answers.’",
      "supporting": "‘If you knew Time as well as I do,’ said the Hatter, ‘you wouldn’t talk about wasting IT. It’s HIM.’",
      "following": "‘I don’t know what you mean,’ said Alice. ‘Of course you don’t!’ the Hatter said, tossing his head contemptuously. ‘I dare say you never even spoke to Time!’",
      "context_incomplete": false
    },
    {
      "evidence_id": "E2",
      "preceding": "‘Well, I’d hardly ﬁnished the ﬁrst verse,’ said the Hatter, ‘when the Queen jumped up and bawled out, “He’s murdering the time! Oﬀwith his head!”’",
      "supporting": "‘How dreadfully savage!’ exclaimed Alice. ‘And ever since that,’ the Hatter went on in a mournful tone, ‘he won’t do a thing I ask! It’s always six o’clock now.’",
      "following": "A bright idea came into Alice’s head. ‘Is that the reason so many tea- things are put out here?’ she asked.",
      "context_incomplete": false
    }
  ],
  "primary_category": "local_context_reasoning",
  "category": "local_context_reasoning",
  "tags": [
    "coreference",
    "speaker_identity"
  ],
  "difficulty": "hard",
  "annotation_notes": "Linked to q023: distinct target claim, shared source event; fact-family IDs are not independent-event counts.",
  "annotation_confidence": "medium",
  "historical_case": false,
  "requires_owner_attention": true,
  "negative_verification": null,
  "ambiguity_rationale": null,
  "expected_clarification": null,
  "evaluation_execution": null,
  "fact_family_id": "fact_av037",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [
    "q023"
  ],
  "review_tier": "DEEP_REVIEW",
  "evidence_event_id": "event_alice_hatter_time_quarrel",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "av037"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## q028

```json
{
  "case_id": "q028",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "What was the Knave of Hearts accused of, and who was called as the first witness?",
  "expected_status": "answered",
  "reference_answer": "He was accused of stealing the Queen's tarts, and the Hatter was the first witness.",
  "required_answer_claims": [
    {
      "claim_id": "C1",
      "claim_text": "The Knave was accused of stealing the tarts.",
      "evidence_ids": [
        "E1"
      ]
    },
    {
      "claim_id": "C2",
      "claim_text": "The Hatter was first witness.",
      "evidence_ids": [
        "E2"
      ]
    }
  ],
  "valid_evidence_locations": [
    {
      "evidence_id": "E1",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 82,
        "chapter": "11",
        "pdf_block": 7
      },
      "exact_supporting_span": "The Knave of Hearts, he stole those tarts",
      "preceding_context": "‘Herald, read the accusation!’ said the King. On this the White Rabbit blew three blasts on the trumpet, and then unrolled the parchment scroll, and read as follows:–",
      "supporting_context": "‘The Queen of Hearts, she made some tarts, All on a summer day: The Knave of Hearts, he stole those tarts, And took them quite away!’",
      "following_context": "‘Consider your verdict,’ the King said to the jury. ‘Not yet, not yet!’ the Rabbit hastily interrupted. ‘There’s a great deal to come before that!’",
      "why_supports": "The cited span and its adjacent discourse support: The Knave was accused of stealing the tarts.",
      "context_incomplete": false,
      "epistemic_status": "character_statement"
    },
    {
      "evidence_id": "E2",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 82,
        "chapter": "11",
        "pdf_block": 10
      },
      "exact_supporting_span": "The first witness was the Hatter",
      "preceding_context": "‘Call the ﬁrst witness,’ said the King; and the White Rabbit blew three blasts on the trumpet, and called out, ‘First witness!’",
      "supporting_context": "The ﬁrst witness was the Hatter. He came in with a teacup in one hand and a piece of bread-and-butter in the other. ‘I beg pardon, your Majesty,’ he began, ‘for bringing these in: but I hadn’t quite ﬁnished my tea when I was sent for.’",
      "following_context": "‘You ought to have ﬁnished,’ said the King. ‘When did you begin?’",
      "why_supports": "The cited span and its adjacent discourse support: The Hatter was first witness.",
      "context_incomplete": false,
      "epistemic_status": "narrator_fact"
    }
  ],
  "exact_supporting_spans": [
    "The Knave of Hearts, he stole those tarts",
    "The first witness was the Hatter"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "E1",
      "preceding": "‘Herald, read the accusation!’ said the King. On this the White Rabbit blew three blasts on the trumpet, and then unrolled the parchment scroll, and read as follows:–",
      "supporting": "‘The Queen of Hearts, she made some tarts, All on a summer day: The Knave of Hearts, he stole those tarts, And took them quite away!’",
      "following": "‘Consider your verdict,’ the King said to the jury. ‘Not yet, not yet!’ the Rabbit hastily interrupted. ‘There’s a great deal to come before that!’",
      "context_incomplete": false
    },
    {
      "evidence_id": "E2",
      "preceding": "‘Call the ﬁrst witness,’ said the King; and the White Rabbit blew three blasts on the trumpet, and called out, ‘First witness!’",
      "supporting": "The ﬁrst witness was the Hatter. He came in with a teacup in one hand and a piece of bread-and-butter in the other. ‘I beg pardon, your Majesty,’ he began, ‘for bringing these in: but I hadn’t quite ﬁnished my tea when I was sent for.’",
      "following": "‘You ought to have ﬁnished,’ said the King. ‘When did you begin?’",
      "context_incomplete": false
    }
  ],
  "primary_category": "multi_source_multi_fact",
  "category": "multi_source_multi_fact",
  "tags": [
    "historical_case",
    "phase4_reuse"
  ],
  "difficulty": "medium",
  "annotation_notes": "Reused historical Phase-4 case; proposed V2 classification does not change its old result. Linked to av057: distinct target claim, shared source event; fact-family IDs are not independent-event counts.",
  "annotation_confidence": "medium",
  "historical_case": true,
  "requires_owner_attention": true,
  "negative_verification": null,
  "ambiguity_rationale": null,
  "expected_clarification": null,
  "evaluation_execution": null,
  "fact_family_id": "fact_q028",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [
    "av057"
  ],
  "review_tier": "DEEP_REVIEW",
  "evidence_event_id": "event_alice_tart_trial_opening",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "q028"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## av057

```json
{
  "case_id": "av057",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "uh who was accused of stealing the queen’s tarts again",
  "expected_status": "answered",
  "reference_answer": "The Knave of Hearts was accused of stealing them.",
  "required_answer_claims": [
    {
      "claim_id": "C1",
      "claim_text": "The court accusation names the Knave of Hearts as the alleged thief.",
      "evidence_ids": [
        "E1"
      ]
    }
  ],
  "valid_evidence_locations": [
    {
      "evidence_id": "E1",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 82,
        "chapter": "11",
        "pdf_block": 7
      },
      "exact_supporting_span": "The Knave of Hearts, he stole those tarts",
      "preceding_context": "‘Herald, read the accusation!’ said the King. On this the White Rabbit blew three blasts on the trumpet, and then unrolled the parchment scroll, and read as follows:–",
      "supporting_context": "‘The Queen of Hearts, she made some tarts, All on a summer day: The Knave of Hearts, he stole those tarts, And took them quite away!’",
      "following_context": "‘Consider your verdict,’ the King said to the jury. ‘Not yet, not yet!’ the Rabbit hastily interrupted. ‘There’s a great deal to come before that!’",
      "why_supports": "The cited span and its adjacent discourse support: The court accusation names the Knave of Hearts as the alleged thief.",
      "context_incomplete": false,
      "epistemic_status": "character_statement"
    }
  ],
  "exact_supporting_spans": [
    "The Knave of Hearts, he stole those tarts"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "E1",
      "preceding": "‘Herald, read the accusation!’ said the King. On this the White Rabbit blew three blasts on the trumpet, and then unrolled the parchment scroll, and read as follows:–",
      "supporting": "‘The Queen of Hearts, she made some tarts, All on a summer day: The Knave of Hearts, he stole those tarts, And took them quite away!’",
      "following": "‘Consider your verdict,’ the King said to the jury. ‘Not yet, not yet!’ the Rabbit hastily interrupted. ‘There’s a great deal to come before that!’",
      "context_incomplete": false
    }
  ],
  "primary_category": "voice_like_noisy_text",
  "category": "voice_like_noisy_text",
  "tags": [
    "metamorphic",
    "voice_like"
  ],
  "difficulty": "medium",
  "annotation_notes": "The answer now preserves accusation status rather than treating the charge as proven fact. Linked to q028: distinct target claim, shared source event; fact-family IDs are not independent-event counts.",
  "annotation_confidence": "high",
  "historical_case": false,
  "requires_owner_attention": false,
  "negative_verification": null,
  "ambiguity_rationale": null,
  "expected_clarification": null,
  "evaluation_execution": null,
  "fact_family_id": "fact_av057",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [
    "q028"
  ],
  "review_tier": "FAST_CONFIRM",
  "evidence_event_id": "event_alice_tart_trial_opening",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "av057"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## q014

```json
{
  "case_id": "q014",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "What did the White Rabbit order 'Mary Ann' to fetch?",
  "expected_status": "answered",
  "reference_answer": "A pair of gloves and a fan.",
  "required_answer_claims": [
    {
      "claim_id": "C1",
      "claim_text": "A pair of gloves and a fan.",
      "evidence_ids": [
        "E1"
      ]
    }
  ],
  "valid_evidence_locations": [
    {
      "evidence_id": "E1",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 31,
        "chapter": "4",
        "pdf_block": 3
      },
      "exact_supporting_span": "Run home this moment, and fetch me a pair of gloves and a fan",
      "preceding_context": "It was the White Rabbit, trotting slowly back again, and looking anxiously about as it went, as if it had lost something; and she heard it muttering to itself ‘The Duchess! The Duchess! Oh my dear paws! Oh my fur and whiskers! She’ll get me executed, as sure as ferrets are ferrets! Where CAN I have dropped them, I wonder?’ Alice guessed in a moment that it was looking for the fan and the pair of white kid gloves, and she very good-naturedly began hunting about for them, but they were nowhere to be seen–everything seemed to have changed since her swim in the pool, and the great hall, with the glass table and the little door, had vanished completely.",
      "supporting_context": "Very soon the Rabbit noticed Alice, as she went hunting about, and called out to her in an angry tone, ‘Why, Mary Ann, what ARE you doing out here? Run home this moment, and fetch me a pair of gloves and a fan! Quick, now!’ And Alice was so much frightened that she ran oﬀat once in the direction it pointed to, without trying to explain the mistake it had made.",
      "following_context": "‘He took me for his housemaid,’ she said to herself as she ran. ‘How surprised he’ll be when he ﬁnds out who I am! But I’d better take him his fan and gloves–that is, if I can ﬁnd them.’ As she said this, she came upon a neat little house, on the door of which was a bright brass plate with the name ‘W. RABBIT’ engraved upon it. She went in without knocking, and hurried upstairs, in great fear lest she should meet the real Mary Ann, and be turned out of the house before she had found the fan and gloves.",
      "why_supports": "The cited span and its adjacent discourse support: A pair of gloves and a fan.",
      "context_incomplete": false,
      "epistemic_status": "narrator_fact"
    }
  ],
  "exact_supporting_spans": [
    "Run home this moment, and fetch me a pair of gloves and a fan"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "E1",
      "preceding": "It was the White Rabbit, trotting slowly back again, and looking anxiously about as it went, as if it had lost something; and she heard it muttering to itself ‘The Duchess! The Duchess! Oh my dear paws! Oh my fur and whiskers! She’ll get me executed, as sure as ferrets are ferrets! Where CAN I have dropped them, I wonder?’ Alice guessed in a moment that it was looking for the fan and the pair of white kid gloves, and she very good-naturedly began hunting about for them, but they were nowhere to be seen–everything seemed to have changed since her swim in the pool, and the great hall, with the glass table and the little door, had vanished completely.",
      "supporting": "Very soon the Rabbit noticed Alice, as she went hunting about, and called out to her in an angry tone, ‘Why, Mary Ann, what ARE you doing out here? Run home this moment, and fetch me a pair of gloves and a fan! Quick, now!’ And Alice was so much frightened that she ran oﬀat once in the direction it pointed to, without trying to explain the mistake it had made.",
      "following": "‘He took me for his housemaid,’ she said to herself as she ran. ‘How surprised he’ll be when he ﬁnds out who I am! But I’d better take him his fan and gloves–that is, if I can ﬁnd them.’ As she said this, she came upon a neat little house, on the door of which was a bright brass plate with the name ‘W. RABBIT’ engraved upon it. She went in without knocking, and hurried upstairs, in great fear lest she should meet the real Mary Ann, and be turned out of the house before she had found the fan and gloves.",
      "context_incomplete": false
    }
  ],
  "primary_category": "direct_factual_single_source",
  "category": "direct_factual_single_source",
  "tags": [
    "historical_case",
    "phase4_reuse"
  ],
  "difficulty": "easy",
  "annotation_notes": "Reused historical Phase-4 case; proposed V2 classification does not change its old result.",
  "annotation_confidence": "high",
  "historical_case": true,
  "requires_owner_attention": false,
  "negative_verification": null,
  "ambiguity_rationale": null,
  "expected_clarification": null,
  "evaluation_execution": null,
  "fact_family_id": "alice_rabbit_mary_ann_errand",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [
    "q015",
    "av055"
  ],
  "review_tier": "FAST_CONFIRM",
  "evidence_event_id": "event_alice_rabbit_mary_ann_errand",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "q014"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## q015

```json
{
  "case_id": "q015",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "What name was engraved on the brass plate at the Rabbit's house?",
  "expected_status": "answered",
  "reference_answer": "W. RABBIT.",
  "required_answer_claims": [
    {
      "claim_id": "C1",
      "claim_text": "W. RABBIT.",
      "evidence_ids": [
        "E1"
      ]
    }
  ],
  "valid_evidence_locations": [
    {
      "evidence_id": "E1",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 31,
        "chapter": "4",
        "pdf_block": 4
      },
      "exact_supporting_span": "name ‘W. RABBIT’ engraved upon it",
      "preceding_context": "Very soon the Rabbit noticed Alice, as she went hunting about, and called out to her in an angry tone, ‘Why, Mary Ann, what ARE you doing out here? Run home this moment, and fetch me a pair of gloves and a fan! Quick, now!’ And Alice was so much frightened that she ran oﬀat once in the direction it pointed to, without trying to explain the mistake it had made.",
      "supporting_context": "‘He took me for his housemaid,’ she said to herself as she ran. ‘How surprised he’ll be when he ﬁnds out who I am! But I’d better take him his fan and gloves–that is, if I can ﬁnd them.’ As she said this, she came upon a neat little house, on the door of which was a bright brass plate with the name ‘W. RABBIT’ engraved upon it. She went in without knocking, and hurried upstairs, in great fear lest she should meet the real Mary Ann, and be turned out of the house before she had found the fan and gloves.",
      "following_context": "‘How queer it seems,’ Alice said to herself, ‘to be going messages for a rabbit! I suppose Dinah’ll be sending me on messages next!’ And she began",
      "why_supports": "The cited span and its adjacent discourse support: W. RABBIT.",
      "context_incomplete": false,
      "epistemic_status": "character_statement"
    }
  ],
  "exact_supporting_spans": [
    "name ‘W. RABBIT’ engraved upon it"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "E1",
      "preceding": "Very soon the Rabbit noticed Alice, as she went hunting about, and called out to her in an angry tone, ‘Why, Mary Ann, what ARE you doing out here? Run home this moment, and fetch me a pair of gloves and a fan! Quick, now!’ And Alice was so much frightened that she ran oﬀat once in the direction it pointed to, without trying to explain the mistake it had made.",
      "supporting": "‘He took me for his housemaid,’ she said to herself as she ran. ‘How surprised he’ll be when he ﬁnds out who I am! But I’d better take him his fan and gloves–that is, if I can ﬁnd them.’ As she said this, she came upon a neat little house, on the door of which was a bright brass plate with the name ‘W. RABBIT’ engraved upon it. She went in without knocking, and hurried upstairs, in great fear lest she should meet the real Mary Ann, and be turned out of the house before she had found the fan and gloves.",
      "following": "‘How queer it seems,’ Alice said to herself, ‘to be going messages for a rabbit! I suppose Dinah’ll be sending me on messages next!’ And she began",
      "context_incomplete": false
    }
  ],
  "primary_category": "direct_factual_single_source",
  "category": "direct_factual_single_source",
  "tags": [
    "historical_case",
    "phase4_reuse"
  ],
  "difficulty": "medium",
  "annotation_notes": "Reused historical Phase-4 case; proposed V2 classification does not change its old result.",
  "annotation_confidence": "high",
  "historical_case": true,
  "requires_owner_attention": false,
  "negative_verification": null,
  "ambiguity_rationale": null,
  "expected_clarification": null,
  "evaluation_execution": null,
  "fact_family_id": "alice_rabbit_mary_ann_errand",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [
    "q014",
    "av055"
  ],
  "review_tier": "FAST_CONFIRM",
  "evidence_event_id": "event_alice_rabbit_mary_ann_errand",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "q015"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## q002

```json
{
  "case_id": "q002",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "How many chapters are listed, and what is the final chapter called?",
  "expected_status": "answered",
  "reference_answer": "There are twelve chapters; the final chapter is Alice's Evidence.",
  "required_answer_claims": [
    {
      "claim_id": "C1",
      "claim_text": "The contents list has twelve chapters and names chapter twelve ‘Alice’s Evidence.’",
      "evidence_ids": [
        "E1"
      ]
    }
  ],
  "valid_evidence_locations": [
    {
      "evidence_id": "E1",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 11,
        "chapter": null,
        "pdf_block": 12
      },
      "exact_supporting_span": "12 Alice’s Evidence",
      "preceding_context": "11 Who Stole the Tarts? 81",
      "supporting_context": "12 Alice’s Evidence 87",
      "following_context": "Down the Rabbit-Hole",
      "why_supports": "The cited span and its adjacent discourse support: The contents list has twelve chapters and names chapter twelve ‘Alice’s Evidence.’",
      "epistemic_status": "narrator_fact",
      "context_incomplete": false
    }
  ],
  "exact_supporting_spans": [
    "12 Alice’s Evidence"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "E1",
      "preceding": "11 Who Stole the Tarts? 81",
      "supporting": "12 Alice’s Evidence 87",
      "following": "Down the Rabbit-Hole",
      "context_incomplete": false
    }
  ],
  "primary_category": "direct_factual_single_source",
  "category": "direct_factual_single_source",
  "tags": [
    "historical_case",
    "phase4_reuse"
  ],
  "difficulty": "medium",
  "annotation_notes": "Both requested values are explicit in one contents entry, so this is one local evidence unit rather than multi-source evidence.",
  "annotation_confidence": "high",
  "historical_case": true,
  "requires_owner_attention": false,
  "negative_verification": null,
  "ambiguity_rationale": null,
  "expected_clarification": null,
  "evaluation_execution": null,
  "fact_family_id": "fact_q002",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [],
  "review_tier": "FAST_CONFIRM",
  "evidence_event_id": "event_fact_q002",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "q002"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## q011

```json
{
  "case_id": "q011",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "Why did Alice address the Mouse in French?",
  "expected_status": "answered",
  "reference_answer": "Alice guessed that the Mouse might not understand English and might be a French mouse that had come with William the Conqueror, so she tried the first sentence from her French lesson-book.",
  "required_answer_claims": [
    {
      "claim_id": "C1",
      "claim_text": "Alice guessed, rather than knew, that the Mouse might be French.",
      "evidence_ids": [
        "E1"
      ]
    },
    {
      "claim_id": "C2",
      "claim_text": "She therefore tried a sentence from her French lesson-book.",
      "evidence_ids": [
        "E1"
      ]
    }
  ],
  "valid_evidence_locations": [
    {
      "evidence_id": "E1",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 22,
        "chapter": "2",
        "pdf_block": 5
      },
      "exact_supporting_span": "French mouse, come over with William the Conqueror",
      "preceding_context": "‘Would it be of any use, now,’ thought Alice, ‘to speak to this mouse? Everything is so out-of-the-way down here, that I should think very likely it can talk: at any rate, there’s no harm in trying.’ So she began: ‘O Mouse, do you know the way out of this pool? I am very tired of swimming about here, O Mouse!’ (Alice thought this must be the right way of speaking to a mouse: she had never done such a thing before, but she remembered having seen in her brother’s Latin Grammar, ‘A mouse–of a mouse–to a mouse–a mouse–O mouse!’) The Mouse looked at her rather inquisitively, and seemed to her to wink with one of its little eyes, but it said nothing.",
      "supporting_context": "‘Perhaps it doesn’t understand English,’ thought Alice; ‘I daresay it’s a French mouse, come over with William the Conqueror.’ (For, with all her knowledge of history, Alice had no very clear notion how long ago anything had happened.) So she began again: ‘Ou est ma chatte?’ which was the ﬁrst sentence in her French lesson-book. The Mouse gave a sudden leap out of the water, and seemed to quiver all over with fright. ‘Oh, I beg your pardon!’ cried Alice hastily, afraid that she had hurt the poor animal’s feelings. ‘I quite forgot you didn’t like cats.’",
      "following_context": "‘Not like cats!’ cried the Mouse, in a shrill, passionate voice. ‘Would YOU like cats if you were me?’",
      "why_supports": "The cited span and its adjacent discourse support: Alice guessed, rather than knew, that the Mouse might be French.; She therefore tried a sentence from her French lesson-book.",
      "context_incomplete": false,
      "epistemic_status": "character_statement"
    }
  ],
  "exact_supporting_spans": [
    "French mouse, come over with William the Conqueror"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "E1",
      "preceding": "‘Would it be of any use, now,’ thought Alice, ‘to speak to this mouse? Everything is so out-of-the-way down here, that I should think very likely it can talk: at any rate, there’s no harm in trying.’ So she began: ‘O Mouse, do you know the way out of this pool? I am very tired of swimming about here, O Mouse!’ (Alice thought this must be the right way of speaking to a mouse: she had never done such a thing before, but she remembered having seen in her brother’s Latin Grammar, ‘A mouse–of a mouse–to a mouse–a mouse–O mouse!’) The Mouse looked at her rather inquisitively, and seemed to her to wink with one of its little eyes, but it said nothing.",
      "supporting": "‘Perhaps it doesn’t understand English,’ thought Alice; ‘I daresay it’s a French mouse, come over with William the Conqueror.’ (For, with all her knowledge of history, Alice had no very clear notion how long ago anything had happened.) So she began again: ‘Ou est ma chatte?’ which was the ﬁrst sentence in her French lesson-book. The Mouse gave a sudden leap out of the water, and seemed to quiver all over with fright. ‘Oh, I beg your pardon!’ cried Alice hastily, afraid that she had hurt the poor animal’s feelings. ‘I quite forgot you didn’t like cats.’",
      "following": "‘Not like cats!’ cried the Mouse, in a shrill, passionate voice. ‘Would YOU like cats if you were me?’",
      "context_incomplete": false
    }
  ],
  "primary_category": "local_context_reasoning",
  "category": "local_context_reasoning",
  "tags": [
    "historical_case",
    "phase4_reuse"
  ],
  "difficulty": "hard",
  "annotation_notes": "The repair preserves Alice’s uncertain belief and avoids presenting it as narrator fact.",
  "annotation_confidence": "medium",
  "historical_case": true,
  "requires_owner_attention": true,
  "negative_verification": null,
  "ambiguity_rationale": null,
  "expected_clarification": null,
  "evaluation_execution": null,
  "fact_family_id": "fact_q011",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [],
  "review_tier": "DEEP_REVIEW",
  "evidence_event_id": "event_fact_q011",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "q011"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## q022

```json
{
  "case_id": "q022",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "Who was at the tea table, and what beverage did the March Hare falsely offer Alice?",
  "expected_status": "answered",
  "reference_answer": "The March Hare, Hatter, and Dormouse were there; the March Hare offered wine even though there was none.",
  "required_answer_claims": [
    {
      "claim_id": "C1",
      "claim_text": "The March Hare, Hatter, and Dormouse were at the table.",
      "evidence_ids": [
        "E1"
      ]
    },
    {
      "claim_id": "C2",
      "claim_text": "The March Hare offered wine although there was none.",
      "evidence_ids": [
        "E2"
      ]
    }
  ],
  "valid_evidence_locations": [
    {
      "evidence_id": "E1",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 51,
        "chapter": "7",
        "pdf_block": 2
      },
      "exact_supporting_span": "Hatter were having tea",
      "preceding_context": "A Mad Tea-Party",
      "supporting_context": "There was a table set out under a tree in front of the house, and the March Hare and the Hatter were having tea at it: a Dormouse was sitting between them, fast asleep, and the other two were using it as a cushion, resting their elbows on it, and talking over its head. ‘Very uncomfortable for the Dormouse,’ thought Alice; ‘only, as it’s asleep, I suppose it doesn’t mind.’",
      "following_context": "The table was a large one, but the three were all crowded together at one corner of it: ‘No room! No room!’ they cried out when they saw Alice coming. ‘There’s PLENTY of room!’ said Alice indignantly, and she sat down in a large arm-chair at one end of the table.",
      "why_supports": "The cited span and its adjacent discourse support: The March Hare, Hatter, and Dormouse were at the table.",
      "context_incomplete": false,
      "epistemic_status": "narrator_fact"
    },
    {
      "evidence_id": "E2",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 51,
        "chapter": "7",
        "pdf_block": 5
      },
      "exact_supporting_span": "There isn’t any",
      "preceding_context": "‘Have some wine,’ the March Hare said in an encouraging tone. Alice looked all round the table, but there was nothing on it but tea. ‘I don’t see any wine,’ she remarked.",
      "supporting_context": "‘There isn’t any,’ said the March Hare. ‘Then it wasn’t very civil of you to oﬀer it,’ said Alice angrily. ‘It wasn’t very civil of you to sit down without being invited,’ said the March Hare.",
      "following_context": "‘I didn’t know it was YOUR table,’ said Alice; ‘it’s laid for a great many more than three.’",
      "why_supports": "The cited span and its adjacent discourse support: The March Hare offered wine although there was none.",
      "context_incomplete": false,
      "epistemic_status": "character_statement"
    }
  ],
  "exact_supporting_spans": [
    "Hatter were having tea",
    "There isn’t any"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "E1",
      "preceding": "A Mad Tea-Party",
      "supporting": "There was a table set out under a tree in front of the house, and the March Hare and the Hatter were having tea at it: a Dormouse was sitting between them, fast asleep, and the other two were using it as a cushion, resting their elbows on it, and talking over its head. ‘Very uncomfortable for the Dormouse,’ thought Alice; ‘only, as it’s asleep, I suppose it doesn’t mind.’",
      "following": "The table was a large one, but the three were all crowded together at one corner of it: ‘No room! No room!’ they cried out when they saw Alice coming. ‘There’s PLENTY of room!’ said Alice indignantly, and she sat down in a large arm-chair at one end of the table.",
      "context_incomplete": false
    },
    {
      "evidence_id": "E2",
      "preceding": "‘Have some wine,’ the March Hare said in an encouraging tone. Alice looked all round the table, but there was nothing on it but tea. ‘I don’t see any wine,’ she remarked.",
      "supporting": "‘There isn’t any,’ said the March Hare. ‘Then it wasn’t very civil of you to oﬀer it,’ said Alice angrily. ‘It wasn’t very civil of you to sit down without being invited,’ said the March Hare.",
      "following": "‘I didn’t know it was YOUR table,’ said Alice; ‘it’s laid for a great many more than three.’",
      "context_incomplete": false
    }
  ],
  "primary_category": "local_context_reasoning",
  "category": "local_context_reasoning",
  "tags": [
    "historical_case",
    "phase4_reuse"
  ],
  "difficulty": "hard",
  "annotation_notes": "The wine answer requires resolving an offer against the following admission that no wine existed; it is one local dialogue, not multi-source.",
  "annotation_confidence": "medium",
  "historical_case": true,
  "requires_owner_attention": true,
  "negative_verification": null,
  "ambiguity_rationale": null,
  "expected_clarification": null,
  "evaluation_execution": null,
  "fact_family_id": "alice_tea_party_wine",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": "contrast_tea_wine",
  "related_case_ids": [
    "av045"
  ],
  "review_tier": "DEEP_REVIEW",
  "evidence_event_id": "event_alice_tea_party_wine",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "q022"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## c005

```json
{
  "case_id": "c005",
  "lifecycle_status": "candidate",
  "split_candidate": "alice_dev_regression",
  "source_book": "alice_in_wonderland",
  "source_book_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
  "question": "How tall did Alice become before the pool formed, and how deep was the pool?",
  "expected_status": "answered",
  "reference_answer": "Alice became more than nine feet tall, and the pool was about four inches deep.",
  "required_answer_claims": [
    {
      "claim_id": "C1",
      "claim_text": "Alice became more than nine feet tall.",
      "evidence_ids": [
        "E1"
      ]
    },
    {
      "claim_id": "C2",
      "claim_text": "The pool was about four inches deep.",
      "evidence_ids": [
        "E2"
      ]
    }
  ],
  "valid_evidence_locations": [
    {
      "evidence_id": "E1",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 19,
        "chapter": "2",
        "pdf_block": 8
      },
      "exact_supporting_span": "more than nine feet high",
      "preceding_context": "And she went on planning to herself how she would manage it. ‘They must go by the carrier,’ she thought; ‘and how funny it’ll seem, sending presents to one’s own feet! And how odd the directions will look!",
      "supporting_context": "Oh dear, what nonsense I’m talking!’ Just then her head struck against the roof of the hall: in fact she was now more than nine feet high, and she at once took up the little golden key and hurried oﬀto the garden door.",
      "following_context": "Poor Alice! It was as much as she could do, lying down on one side, to look through into the garden with one eye; but to get through was more hopeless than ever: she sat down and began to cry again.",
      "why_supports": "The cited span and its adjacent discourse support: Alice became more than nine feet tall.",
      "context_incomplete": false,
      "epistemic_status": "narrator_fact"
    },
    {
      "evidence_id": "E2",
      "source_location": {
        "book": "alice_in_wonderland",
        "page": 20,
        "chapter": "2",
        "pdf_block": 1
      },
      "exact_supporting_span": "about four inches deep",
      "preceding_context": "Poor Alice! It was as much as she could do, lying down on one side, to look through into the garden with one eye; but to get through was more hopeless than ever: she sat down and began to cry again.",
      "supporting_context": "‘You ought to be ashamed of yourself,’ said Alice, ‘a great girl like you,’ (she might well say this), ‘to go on crying in this way! Stop this moment, I tell you!’ But she went on all the same, shedding gallons of tears, until there was a large pool all round her, about four inches deep and reaching half down the hall.",
      "following_context": "After a time she heard a little pattering of feet in the distance, and she hastily dried her eyes to see what was coming. It was the White Rabbit returning, splendidly dressed, with a pair of white kid gloves in one hand and a large fan in the other: he came trotting along in a great hurry, muttering to himself as he came, ‘Oh! the Duchess, the Duchess! Oh! won’t she be savage if I’ve kept her waiting!’ Alice felt so desperate that she was ready to ask help of any one; so, when the Rabbit came near her, she began, in a low, timid voice, ‘If you please, sir–’ The Rabbit started violently, dropped the white kid gloves and the fan, and skurried away into the darkness as hard as he could go.",
      "why_supports": "The narrator states that the pool around Alice was about four inches deep.",
      "context_incomplete": false,
      "epistemic_status": "narrator_fact"
    }
  ],
  "exact_supporting_spans": [
    "more than nine feet high",
    "about four inches deep"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "E1",
      "preceding": "And she went on planning to herself how she would manage it. ‘They must go by the carrier,’ she thought; ‘and how funny it’ll seem, sending presents to one’s own feet! And how odd the directions will look!",
      "supporting": "Oh dear, what nonsense I’m talking!’ Just then her head struck against the roof of the hall: in fact she was now more than nine feet high, and she at once took up the little golden key and hurried oﬀto the garden door.",
      "following": "Poor Alice! It was as much as she could do, lying down on one side, to look through into the garden with one eye; but to get through was more hopeless than ever: she sat down and began to cry again.",
      "context_incomplete": false
    },
    {
      "evidence_id": "E2",
      "preceding": "Poor Alice! It was as much as she could do, lying down on one side, to look through into the garden with one eye; but to get through was more hopeless than ever: she sat down and began to cry again.",
      "supporting": "‘You ought to be ashamed of yourself,’ said Alice, ‘a great girl like you,’ (she might well say this), ‘to go on crying in this way! Stop this moment, I tell you!’ But she went on all the same, shedding gallons of tears, until there was a large pool all round her, about four inches deep and reaching half down the hall.",
      "following": "After a time she heard a little pattering of feet in the distance, and she hastily dried her eyes to see what was coming. It was the White Rabbit returning, splendidly dressed, with a pair of white kid gloves in one hand and a large fan in the other: he came trotting along in a great hurry, muttering to himself as he came, ‘Oh! the Duchess, the Duchess! Oh! won’t she be savage if I’ve kept her waiting!’ Alice felt so desperate that she was ready to ask help of any one; so, when the Rabbit came near her, she began, in a low, timid voice, ‘If you please, sir–’ The Rabbit started violently, dropped the white kid gloves and the fan, and skurried away into the darkness as hard as he could go.",
      "context_incomplete": false
    }
  ],
  "primary_category": "multi_fact_single_context",
  "category": "multi_fact_single_context",
  "tags": [
    "contrastive_pair",
    "historical_case",
    "phase4_reuse"
  ],
  "difficulty": "hard",
  "annotation_notes": "Metamorphic restatement of q009. Both numeric facts belong to one continuous growth-and-tears sequence; the four-inch depth is narrator description.",
  "annotation_confidence": "medium",
  "historical_case": true,
  "requires_owner_attention": true,
  "negative_verification": null,
  "ambiguity_rationale": null,
  "expected_clarification": null,
  "evaluation_execution": null,
  "fact_family_id": "alice_height_pool_depth",
  "metamorphic_pair_id": "meta_height_pool",
  "contrastive_pair_id": null,
  "related_case_ids": [
    "q009",
    "av056"
  ],
  "review_tier": "DEEP_REVIEW",
  "evidence_event_id": "event_alice_height_pool_depth",
  "development_exposure": {
    "status": "development_material",
    "sources": [
      "c005"
    ],
    "review_method": "This case and its reviewer-facing context are development-visible."
  }
}
```

---

## sg083

```json
{
  "case_id": "sg083",
  "lifecycle_status": "candidate",
  "split_candidate": "secret_garden_holdout",
  "source_book": "the_secret_garden",
  "source_book_sha256": "6b0bb5fbd0c4e873d2d22028da9d753cf3977d5f70ac58221556b28060badbf5",
  "question": "What was the name of Dickon’s mother?",
  "expected_status": "answered",
  "reference_answer": "Susan Sowerby.",
  "required_answer_claims": [
    {
      "claim_id": "C1",
      "claim_text": "The woman is identified as Susan Sowerby.",
      "evidence_ids": [
        "E1"
      ]
    },
    {
      "claim_id": "C2",
      "claim_text": "Colin identifies her as Dickon’s mother.",
      "evidence_ids": [
        "E2"
      ]
    }
  ],
  "valid_evidence_locations": [
    {
      "evidence_id": "E1",
      "source_location": {
        "book": "the_secret_garden",
        "canonical_line": 8906,
        "chapter": null,
        "generated_pdf_pages": [
          129
        ]
      },
      "exact_supporting_span": "Susan Sowerby got up at last",
      "preceding_context": "One of the things they talked of was the visit they were to make to her cottage. They planned it all. They were to drive over the moor and lunch out of doors among the heather. They would see all the twelve children and Dickon’s garden and would not come back until they were tired.",
      "supporting_context": "Susan Sowerby got up at last to return to the house and Mrs. Medlock. It was time for Colin to be wheeled back also. But before he got into his chair he stood quite close to Susan and fixed his eyes on her with a kind of bewildered adoration and he suddenly caught hold of the fold of her blue cloak and held it fast.",
      "following_context": "“You are just what I—what I wanted,” he said. “I wish you were my mother—as well as Dickon’s!”",
      "why_supports": "The cited span and its adjacent discourse support: The woman is identified as Susan Sowerby.",
      "context_incomplete": false,
      "epistemic_status": "narrator_fact"
    },
    {
      "evidence_id": "E2",
      "source_location": {
        "book": "the_secret_garden",
        "canonical_line": 8912,
        "chapter": null,
        "generated_pdf_pages": [
          129
        ]
      },
      "exact_supporting_span": "I wish you were my mother—as well as Dickon’s",
      "preceding_context": "Susan Sowerby got up at last to return to the house and Mrs. Medlock. It was time for Colin to be wheeled back also. But before he got into his chair he stood quite close to Susan and fixed his eyes on her with a kind of bewildered adoration and he suddenly caught hold of the fold of her blue cloak and held it fast.",
      "supporting_context": "“You are just what I—what I wanted,” he said. “I wish you were my mother—as well as Dickon’s!”",
      "following_context": "All at once Susan Sowerby bent down and drew him with her warm arms close against the bosom under the blue cloak—as if he had been Dickon’s brother. The quick mist swept over her eyes.",
      "why_supports": "The cited span and its adjacent discourse support: Colin identifies her as Dickon’s mother.",
      "context_incomplete": false,
      "epistemic_status": "narrator_fact"
    }
  ],
  "exact_supporting_spans": [
    "Susan Sowerby got up at last",
    "I wish you were my mother—as well as Dickon’s"
  ],
  "local_surrounding_context": [
    {
      "evidence_id": "E1",
      "preceding": "One of the things they talked of was the visit they were to make to her cottage. They planned it all. They were to drive over the moor and lunch out of doors among the heather. They would see all the twelve children and Dickon’s garden and would not come back until they were tired.",
      "supporting": "Susan Sowerby got up at last to return to the house and Mrs. Medlock. It was time for Colin to be wheeled back also. But before he got into his chair he stood quite close to Susan and fixed his eyes on her with a kind of bewildered adoration and he suddenly caught hold of the fold of her blue cloak and held it fast.",
      "following": "“You are just what I—what I wanted,” he said. “I wish you were my mother—as well as Dickon’s!”",
      "context_incomplete": false
    },
    {
      "evidence_id": "E2",
      "preceding": "Susan Sowerby got up at last to return to the house and Mrs. Medlock. It was time for Colin to be wheeled back also. But before he got into his chair he stood quite close to Susan and fixed his eyes on her with a kind of bewildered adoration and he suddenly caught hold of the fold of her blue cloak and held it fast.",
      "supporting": "“You are just what I—what I wanted,” he said. “I wish you were my mother—as well as Dickon’s!”",
      "following": "All at once Susan Sowerby bent down and drew him with her warm arms close against the bosom under the blue cloak—as if he had been Dickon’s brother. The quick mist swept over her eyes.",
      "context_incomplete": false
    }
  ],
  "primary_category": "direct_factual_single_source",
  "category": "direct_factual_single_source",
  "tags": [],
  "difficulty": "medium",
  "annotation_notes": "Holdout item: full owner review remains mandatory.",
  "annotation_confidence": "high",
  "historical_case": false,
  "requires_owner_attention": true,
  "negative_verification": null,
  "ambiguity_rationale": null,
  "expected_clarification": null,
  "evaluation_execution": null,
  "fact_family_id": "fact_sg083",
  "metamorphic_pair_id": null,
  "contrastive_pair_id": null,
  "related_case_ids": [],
  "review_tier": "FAST_CONFIRM",
  "evidence_event_id": "event_fact_sg083",
  "development_exposure": {
    "status": "not_applicable_different_book",
    "sources": [],
    "review_method": "Secret Garden is a separate-book holdout."
  }
}
```

---

## Current source-consistency report

```json
{
  "purpose": "Offline representation-consistency validation; no retrieval, QA, or provider calls.",
  "source_policy": {
    "secret_garden_canonical_text": "semantic source of truth",
    "secret_garden_generated_pdf": "parser coverage validation",
    "raw_regex_hit_count_equality_required": false
  },
  "alice_in_wonderland": {
    "semantic_source_of_truth": "locally ingested Alice text-layer PDF",
    "pdf_sha256": "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e",
    "stored_page_count": 92,
    "reparsed_page_count": 92,
    "stored_pages_equal_reparsed_normalized_pages": true,
    "differing_pages": [],
    "status": "pass"
  },
  "the_secret_garden": {
    "semantic_source_of_truth": "Project Gutenberg eBook #113 canonical text",
    "pdf_role": "parser coverage validation only",
    "canonical_text_sha256": "6b0bb5fbd0c4e873d2d22028da9d753cf3977d5f70ac58221556b28060badbf5",
    "generated_pdf_sha256": "499f246e4f1ecbe265d8c942f39d4c9825cd4d8e08dc8c1a7e8d2b6c49c9561e",
    "pdf_page_count": 137,
    "empty_pdf_pages": [],
    "canonical_chapter_heading_count": 27,
    "pdf_chapter_heading_count": 27,
    "chapter_boundary_alignment": true,
    "normalization_contract": "Shared typography/ligature mapping, then NFKD, casefold, ordered ASCII-alphanumeric tokens; layout punctuation is ignored",
    "canonical_ordered_token_count": 83165,
    "pdf_extracted_ordered_token_count": 83165,
    "ordered_token_sequence_equal": true,
    "missing_or_extra_token_spans": [],
    "punctuation_or_layout_artifacts": {
      "unsupported_middle_dot_glyph_count_after_repair": 0,
      "interpretation": "Punctuation/layout differences do not constitute semantic loss when the normalized ordered token sequence is equal."
    },
    "content_loss_detected": false,
    "status": "pass"
  },
  "overall_status": "pass"
}

```
