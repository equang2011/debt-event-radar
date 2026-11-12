
## 2026-11-11

- used script to check acceptance time
- acceptance time is 4 hours ahead of time in header
- decision: Use the JSON acceptanceDateTime (verified UTC) to store

## 2026-11-09
- Learned: recent is a dict of parallel lists; acceptanceDateTime looks like UTC.
- Gotcha: python scripts/x.py fails; use python -m (sys.path[0] is the script's folder).
- Next: verify timestamp against filing header; parse_acceptance_ts() + test.


## 2026-08-29 — TF-IDF Logistic Regression v2

### Dataset
- 99 labeled EX-10 exhibits
- 39 positive / 60 negative
- 75/25 stratified train-test split

### Representation
- TF-IDF
- English stop words
- unigrams + bigrams
- 190,421 features

### Result
- 25/25 held-out predictions correct
- weakest positive probability: 0.508
- positive features included lender, borrower, administrative agent, revolving, credit
- negative features included award, shares, plan, employee, stock

### Interesting failure/risk
- 0.508 example was a securitization omnibus amendment.
- Likely harder because vocabulary differs from conventional corporate credit agreements.
- Random split may leak issuer/document-family similarity.

### Next experiment
- Evaluate on unseen issuer(s) rather than another random split.