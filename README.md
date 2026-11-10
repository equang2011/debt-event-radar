# debt-event-radar

Extracts structured debt events from SEC EDGAR financing exhibits, keyed to the
moment the market could first know about them: the filing's **acceptance timestamp**,
not its filing date or reporting period.

Each event records: issuer, CIK, accession number, acceptance timestamp, agreement
type, facility amount, maturity, administrative agent / lead arrangers, and
financial maintenance covenants.

## Status

Early. Retrieval from EDGAR (submissions → 8-K → filing index → EX-10 exhibit text)
works across issuers as exploratory scripts in `scripts/`. Schema, extraction,
gold set and evaluation are in progress.

## Scope (v1, January 2027)

**In scope**
- 8-K filings tagged Item 1.01 or 2.03, from a fixed list of ~12 issuers
- EX-10 exhibits: credit agreements and amendments
- A hand-labeled gold set, split by issuer into dev and test
- Field-level extraction accuracy, reported per field
- Point-in-time queries: "what did we know about issuer X as of time T?"

**Out of scope (known limitations)**
- Indentures and notes, which are mostly filed as EX-4
- Financing exhibits filed with 10-Q / 10-K
- Full lender syndicate lists (agent and lead arrangers only)
- Applying amendments to reconstruct a facility's current terms
- Filings older than the submissions API's `recent` window

## Planned pipeline

```
issuer list → submissions JSON → candidate 8-Ks (Items 1.01 / 2.03)
  → filing index → EX-10 exhibits → raw cache → text
  → extraction (LLM, structured output) → validation → SQLite
  → as-of queries + evaluation against gold set
```

## Running the spikes

From the repo root (the code is not yet packaged, so it is not pip-installable):

```bash
pip install httpx "beautifulsoup4>=4.9.0" "scikit-learn>=1.4" pytest ruff
python -m scripts.multi_issuer_spike
```