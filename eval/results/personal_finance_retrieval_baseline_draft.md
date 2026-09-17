# Personal Finance Retrieval Baseline (Draft)

- Document: `Personal Finance.pdf` / `74028ca792a24e18b60e89cee1f877aa`
- Source: 297 PDF pages, 700 chunks; `fixed-window-dense-v1`; `voyage-4`; local exact cosine.
- Scope: retrieval only. No production setting, prompt, Top-K default, reranker, frozen corpus, Qwen, or holdout was changed or run.
- Query embeddings were made with `voyage-4`; all document vectors came from the existing complete local cache.

## Bad Case: Financial Risk

The source does not define the precise term **financial risk**. It uses the phrase on page 190 only to describe insurance as a system for shifting it, while page 243 defines **investment risk**. Therefore the human question is a source-semantics / answerability issue, not a failed retrieval target.

- `里面的金融风险是怎么定义的。`: generic investment-risk definition (chunk `00563`, p. 243) is rank 7; the exact financial-risk phrase (chunk `00433`, p. 190) is rank 124 and outside top 50.
- `How does the book define financial risk?`: generic investment-risk definition is rank 1; exact financial-risk phrase is rank 78.
- `How does the book define risk?`: generic investment-risk definition is rank 2; the insurance discussion ranks 1 and 3.

The relevant sections are `2.5 Income and Risk` (chunks `00094`-`00096`, pages 42-45), `10 Personal Risk Management - Insurance` (chunks `00429`-`00433`, pages 187-190), and `13.3 Risk and Return` (chunks `00562`-`00566`, pages 242-245). The exact terms `financial risk`, `risk management`, and `risk and return` occur, but only the last section gives the requested definitional form for risk.

### Top 50: `里面的金融风险是怎么定义的。`

Stored chunks do not have structured chapter/heading metadata, so that field is unavailable rather than inferred. Pages are persisted provenance.

| Rank | Cosine | PDF page(s) | Heading metadata | Chunk ID | Short excerpt |
|---:|---:|---|---|---|---|
| 1 | 0.493890 | 290 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00679` | oyer misconduct to authorities. retention rate \| The rate at which a company retains earnings for use as additional capital or the earnings retained (not paid out as dividends) ... |
| 2 | 0.476840 | 286 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00663` | nterest rate risk \| The risk that a bond's market value will be affected by a change in interest rates. intermediary \| A third party that facilitates trade between two parties. ... |
| 3 | 0.463564 | 286 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00662` | lower currency values (one unit of currency is worth less because it buys a smaller quantity of goods and services). Inflation risk \| The risk that the value of a bond's returns... |
| 4 | 0.461350 | 291 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00682` | ponsible investment \| An investment strategy to achieve both ethical and financial goals. specialized budgets \| A budget that focuses on one particular financial asset, activity... |
| 5 | 0.438422 | 244, 245 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00566` | urns require greater tolerance for fluctuation and uncertainty. • Risk is shaped by time horizon, emotional resilience, and financial flexibility. • The difference between expec... |
| 6 | 0.438280 | 188, 189 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00430` | ent- Insurance is shared under a CC BY-NC-SA 3.0 license and was authored, remixed, and/or curated by Guy Buker via source content that was edited to the style and standards of ... |
| 7 | 0.433506 | 243 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00563` | rcent every year. No surprises. No losses. • Option B: Some years, you earn 12 percent. Other years, you lose 5 percent. Over time, you might average around 6 percent, but it’s ... |
| 8 | 0.432781 | 290, 291 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00680` | ment may decline in the future. risk averse \| An investor's preference to minimize exposure to risk. Risk shifting \| Selling risk to avoid bearing the full consequence of uninte... |
| 9 | 0.431968 | 284, 285 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00656` | ified percentage of actual cash value. F face value \| For a bond, the amount to be repaid to the bondholder upon redemption. fiduciary \| A person or organization that acts on be... |
| 10 | 0.423986 | 280, 281 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00640` | covers the costs of physician expenses, surgical expenses, and hospital expenses. basis point \| A unit of measure that is one one-hundredth of a percentage point, or 0.01 percen... |
| 11 | 0.421792 | 280 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00637` | adjusted without cancellation of the policy. adjustable-rate mortgage (ARM) \| A mortgage loan with a floating or adjustable rate of interest. Advisory dealing \| An investor-brok... |
| 12 | 0.417479 | 283 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00649` | ness in the credit rating process. Credit unions \| A retail banking institution that is either depositor- or member-owned. Membership is usually defined and limited to affiliati... |
| 13 | 0.413986 | 243, 244 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00564` | pect a 7 percent return this year. Great. But the market doesn’t read your plan. A headline, a war, a company’s misstep, or a surge in demand - any of these can jolt prices up o... |
| 14 | 0.413079 | 285 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00658` | Framing \| The idea that the presentation or perception of a decision influences the decision maker. Free cash flow \| Income remaining after the deduction of living expenses and ... |
| 15 | 0.406488 | 244 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00565` | he horizon. Even a small loss can make an investor anxious. One may decide to keep some money in safer options. Others realize they may be overestimating their tolerance and dia... |
| 16 | 0.401636 | 189 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00431` | able way to protect yourself from these risks is to avoid engaging in them. However, other risks emerge without invitation. They don't offer a prize; they exact a price. A light... |
| 17 | 0.399770 | 33, 34 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00069` | osts and sunk costs as implicit but critical considerations in financial thinking. 2.1: Introduction 2.2: Income and Expenses 2.3: Assets 2.4: Debt and Equity 2.5: Income and Ri... |
| 18 | 0.396800 | 289, 290 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00676` | common design of an income tax. Property damage liability \| Responsibility for damage to property owned by people other than the driver at fault. property transfer tax \| A tax o... |
| 19 | 0.395228 | 242, 243 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00562` | ose ratios shift over time? This page titled 13.2: Investing vs. Saving is shared under a license and was authored, remixed, and/or curated by LibreTexts. 228 (13.2.2) 13.3: Ris... |
| 20 | 0.395014 | 262 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00601` | y Company B’s bond unless they’re compensated for the extra risk. So Company B increases its coupon rate to 7 percent. Now it has your attention. This is the risk-return tradeof... |
| 21 | 0.394149 | 285 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00657` | the interest rate remains constant over the maturity of the loan. fixed-rate mortgage \| A mortgage loan with a fixed interest rate over the life of the loan. flexible savings ac... |
| 22 | 0.393499 | 283 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00650` | r trading for its own account. debenture \| A bond secured by only the 'full faith and credit' of the borrower and not by any specific asset. debit card \| A card that allows poin... |
| 23 | 0.392785 | 258 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00591` | use a combination of these instruments to balance risk and reward. Over time, the blend may shift based on goals, life stage, and market outlook. What matters most is understand... |
| 24 | 0.390368 | 282, 283 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00648` | g to pay interest on the principal. cost of equity \| The cost of having to share the benefits (capital gains or income (dividends)) from the investment. coupon \| The interest pa... |
| 25 | 0.390303 | 285, 286 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00660` | Individually owned and financed savings accounts that may be used to finance health care costs with tax-deductible contributions. high-yield bonds \| Bonds rated BB or Ba or lowe... |
| 26 | 0.386733 | 286 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00661` | ption or saved. income statement \| A summary statement of income and expenses for a period; an income statement shows the difference between them or the net profit (net loss) fo... |
| 27 | 0.382786 | 28, 29 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00059` | s Vegas Eliminate debt and increase surplus a lot (no Airfare and hotel in Risk of increased deficit Eliminate debt payments) Vegas and debt alternatives You may sometimes choos... |
| 28 | 0.380425 | 267, 268 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00612` | gher yield might seem help assess default risk. AAA safer, while corporate bonds tempting, but it often reflects is the safest; anything below carry more variation in risk. grea... |
| 29 | 0.376242 | 262 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00600` | Jordan need to consider the question that every investor eventually faces: “How do I know what kind of investment is right for me?” It’s a deceptively simple question, because b... |
| 30 | 0.375045 | 42, 43, 44 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00094` | ucation? 2. If payments on student loans become overwhelming, what should you do to avoid default? 28 (2.4.2) [1] The Investopedia Team. If You Had Invested Right After Google's... |
| 31 | 0.374138 | 288, 289 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00672` | unity cost \| The cost of sacrificing the next best choice because of the choice made; the value of the next best choice, which is forgone once a choice is made. Options \| The ri... |
| 32 | 0.373106 | 290 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00678` | six consecutive months or two consecutive quarters. redeemable \| A bond that is eligible for redemption. refinancing \| Attaining a new mortgage and simultaneously paying off the... |
| 33 | 0.371112 | 289 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00675` | rs. prime rate \| A benchmark interest rate understood to be the rate that major banks charge corporate borrowers with the least default risk. principal \| The original amount of ... |
| 34 | 0.370863 | 287 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00667` | vities of daily living in the event of disabling injury or illness. Loss aversion \| An investor's preference to avoid losses, even when the costs outweigh the benefits, in which... |
| 35 | 0.370557 | 281 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00641` | providing steady returns. Bodily injury liability \| Responsibility for financial losses from injuries sustained in an accident for people outside of the car of the driver at fau... |
| 36 | 0.367905 | 284 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00655` | t of assets but is traded like stocks on a stock exchange. Exchange-traded funds (ETFs) \| A mutual fund that is structured as a closed-end fund and actively traded on an exchang... |
| 37 | 0.367311 | 280 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00639` | en authorized for issuance by a corporation's board of directors. Automatic payments \| A direct payment of an expense or a debt payment made as an electronic transfer of funds f... |
| 38 | 0.366552 | 27, 28 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00057` | irfare and hotel in Risk of increased deficit and payments) Vegas debt Laying out Alice's choices in this way shows the consequences more clearly. The alternative with the most ... |
| 39 | 0.363033 | 245 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00568` | technical, but it’s really just a written summary of four things: 1. What you’re trying to achieve 2. What kind of risk you’re willing to take 3. What constraints or needs you h... |
| 40 | 0.359543 | 288 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00670` | a bond whose return is secured by the income (mortgage payments) from a pool of mortgages. multiple-unit dwelling \| A residential building including more than one housing unit, ... |
| 41 | 0.359327 | 17, 18 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00028` | t enough to advance toward goals, and prescient enough to protect against unforeseen risks. One of the most critical resources in the planning process is information. We live in... |
| 42 | 0.358493 | 280 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00638` | d to do appraisals. arbitrage \| Trading that profits from the market mispricing of assets in the capital markets. arbitrage opportunities \| A market mispricing that provides an ... |
| 43 | 0.357748 | 245, 246 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00569` | e isn’t just about math; it’s about mindset. It includes • Your ability to take risks (based on your time horizon, current savings, and income) • Your willingness to take risks ... |
| 44 | 0.355268 | 287 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00665` | ed in 1975. Leveraged funds \| A mutual fund that invests borrowed funds as well as investors' funds. liens \| An interest in a property granted to secure payment of debt. life cy... |
| 45 | 0.355014 | 27, 28 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00058` | ternatives that she had initially rejected as too costly (see Figure 1.4.5 ). 13 (1.4.3) Figure 1.4.5 : Considering Risk in Alice's Choice The Vegas option becomes the least des... |
| 46 | 0.354473 | 187, 188 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00429` | buyers become involved either directly or indirectly in mortgage or real estate fraud? 5. Explore the ways to avoid foreclosure (www.usa.gov/avoid-foreclosure) at USA.gov. What ... |
| 47 | 0.354113 | 283, 284 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00652` | ss. discount rate \| The effect of time on value or the rate at which time affects value; used when calculating the equivalent present value of a nominal future value. Discretion... |
| 48 | 0.351459 | 288 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00669` | ustained in an accident for people inside of the car of the driver at fault. Medicare \| A federal program financing health care costs with eligibility based on age (for those ov... |
| 49 | 0.351242 | 283 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00651` | ute to. defined contribution retirement plans \| A retirement savings plan sponsored by an employer that both employer and employee may contribute to. deflation \| Period characte... |
| 50 | 0.349562 | 68, 69 | unavailable | `74028ca792a24e18b60e89cee1f877aa:chunk:00152` | - A Stream of Payments Over Time 4.7: Amortization - Breaking Down Big Payments Over Time 4.8: Putting It All Together This page titled 4: Time Value of Money is shared under a ... |

## Draft Ground Truth

The full human-reviewable source excerpts, pages, chunk IDs, answerability notes, and pair labels are in [`personal_finance_acceptance_draft.json`](../dataset/personal_finance_acceptance_draft.json). The original financial-risk question is intentionally unscored because no exact source definition exists; the remaining 11 cases are scored.

| Case | Language | Category | Gold chunk(s) | Evidence requirement |
|---|---|---|---|---|
| `pf-01-financial-risk-zh` | zh | insufficient-evidence | none (unscored) | single / answerability |
| `pf-02-risk-definition-en` | en | direct-factual | `00563` | single / answerability |
| `pf-03-risk-definition-zh` | zh | direct-factual | `00563` | single / answerability |
| `pf-04-liquidity-definition-en` | en | direct-factual | `00153` | single / answerability |
| `pf-05-liquidity-definition-zh` | zh | paraphrase-vocabulary-mismatch | `00153` | single / answerability |
| `pf-06-diversification-paraphrase-en` | en | paraphrase-vocabulary-mismatch | `00095` | single / answerability |
| `pf-07-income-diversification-multifact-en` | en | multi-fact-cross-section | `00095`, `00096` | multiple |
| `pf-08-risk-tolerance-multifact-en` | en | multi-fact-cross-section | `00564`, `00566` | multiple |
| `pf-09-term-vs-whole-life-en` | en | contrastive-distractor-sensitive | `00464`, `00465`, `00466` | multiple |
| `pf-10-right-investment-ambiguous-en` | en | ambiguous | `00600` | single / answerability |
| `pf-11-cash-flow-matching-en` | en | english-uncommon-finance-terminology | `00643` | single / answerability |
| `pf-12-net-worth-definition-en` | en | direct-factual | `00110` | single / answerability |

## Current K Sweep

Metrics use the 11 scored cases. Recall@K means at least one gold chunk is retrieved; full-evidence coverage requires every listed gold chunk. MRR is truncated at K.

| Group | K | Recall@K | MRR@K | Full Evidence Coverage@K |
|---|---:|---:|---:|---:|
| All scored (n=11) | 5 | 0.9091 | 0.7576 | 0.9091 |
| All scored (n=11) | 10 | 1.0000 | 0.7689 | 1.0000 |
| All scored (n=11) | 20 | 1.0000 | 0.7689 | 1.0000 |
| All scored (n=11) | 30 | 1.0000 | 0.7689 | 1.0000 |
| All scored (n=11) | 50 | 1.0000 | 0.7689 | 1.0000 |
| English-only (n=9) | 5 | 0.8889 | 0.8333 | 0.8889 |
| English-only (n=9) | 10 | 1.0000 | 0.8472 | 1.0000 |
| English-only (n=9) | 20 | 1.0000 | 0.8472 | 1.0000 |
| English-only (n=9) | 30 | 1.0000 | 0.8472 | 1.0000 |
| English-only (n=9) | 50 | 1.0000 | 0.8472 | 1.0000 |
| Mandarin -> English source (n=2) | 5 | 1.0000 | 0.4167 | 1.0000 |
| Mandarin -> English source (n=2) | 10 | 1.0000 | 0.4167 | 1.0000 |
| Mandarin -> English source (n=2) | 20 | 1.0000 | 0.4167 | 1.0000 |
| Mandarin -> English source (n=2) | 30 | 1.0000 | 0.4167 | 1.0000 |
| Mandarin -> English source (n=2) | 50 | 1.0000 | 0.4167 | 1.0000 |
| Direct factual (n=4) | 5 | 1.0000 | 0.7500 | 1.0000 |
| Direct factual (n=4) | 10 | 1.0000 | 0.7500 | 1.0000 |
| Direct factual (n=4) | 20 | 1.0000 | 0.7500 | 1.0000 |
| Direct factual (n=4) | 30 | 1.0000 | 0.7500 | 1.0000 |
| Direct factual (n=4) | 50 | 1.0000 | 0.7500 | 1.0000 |
| Paraphrase (n=2) | 5 | 1.0000 | 0.6667 | 1.0000 |
| Paraphrase (n=2) | 10 | 1.0000 | 0.6667 | 1.0000 |
| Paraphrase (n=2) | 20 | 1.0000 | 0.6667 | 1.0000 |
| Paraphrase (n=2) | 30 | 1.0000 | 0.6667 | 1.0000 |
| Paraphrase (n=2) | 50 | 1.0000 | 0.6667 | 1.0000 |
| Multi-evidence (n=2) | 5 | 1.0000 | 1.0000 | 1.0000 |
| Multi-evidence (n=2) | 10 | 1.0000 | 1.0000 | 1.0000 |
| Multi-evidence (n=2) | 20 | 1.0000 | 1.0000 | 1.0000 |
| Multi-evidence (n=2) | 30 | 1.0000 | 1.0000 | 1.0000 |
| Multi-evidence (n=2) | 50 | 1.0000 | 1.0000 | 1.0000 |

## First Relevant Rank

| Case | First relevant rank | All gold ranks |
|---|---:|---|
| `pf-02-risk-definition-en` | 2 | 2 |
| `pf-03-risk-definition-zh` | 2 | 2 |
| `pf-04-liquidity-definition-en` | 1 | 1 |
| `pf-05-liquidity-definition-zh` | 3 | 3 |
| `pf-06-diversification-paraphrase-en` | 1 | 1 |
| `pf-07-income-diversification-multifact-en` | 1 | 1, 2 |
| `pf-08-risk-tolerance-multifact-en` | 1 | 1, 2 |
| `pf-09-term-vs-whole-life-en` | 1 | 5, 1, 2 |
| `pf-10-right-investment-ambiguous-en` | 8 | 8 |
| `pf-11-cash-flow-matching-en` | 1 | 1 |
| `pf-12-net-worth-definition-en` | 1 | 1 |

## English vs Mandarin

- Risk-definition pair: English rank 2; Mandarin rank 2.
- Liquidity-definition pair: English rank 1; Mandarin rank 3.
- Both Mandarin-to-English-source cases have Recall@5 and full-evidence coverage@5 of 1.0000. Their MRR@5 is 0.4167 versus 0.8333 for the 9 English-only cases, but this is only a two-case sample and is driven by positions 2 and 3 rather than missed evidence.

## Taxonomy and Next Experiment

- Human financial-risk case: **E. source itself does not explicitly define the requested concept**. It is not an evidence-packing failure: the exact requested definition does not exist. The generic risk evidence is present at rank 7 for the Chinese formulation and rank 1 for the English formulation.
- K sweep: Recall and full-evidence coverage first reach 1.0000 at K=10 and remain flat through K=50. The sole K=5 miss is the source's exact ambiguous-question framing at rank 8.
- Next experiment only: **increase candidate K**. This draft supports testing K=10 against K=5 before a reranker, because K=10 recovers the only scored miss and no sampled case gains after K=10. Do not treat the two Mandarin cases as sufficient evidence for a cross-language representation change.
