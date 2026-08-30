import json
import httpx
import time

from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin

from app.sec.client import EdgarClient
from scripts.edgar_spike import find_candidate_filings, save_results, fetch_document


issuers = [
    {"name": "Ford", "cik": "37996"},
    {"name": "AT&T", "cik": "732717"},
    {"name": "Delta", "cik": "27904"},
    {"name": "General Motors", "cik": "1467858"},
]
"""
issuers = [
    {"name": "General Motors", "cik": "1467858"},
]
"""

# the debug version 
def extract_exhibits_debug(client, filing: dict[str,str])-> list[dict[str,str]]:
    print("\nFILING:", filing["filing_index_url"])
    html = client.get_text(filing["filing_index_url"])
    soup = BeautifulSoup(html, "html.parser")


    exhibit_docs = []

    for row in soup.find_all("tr"):
        cells = row.find_all("td")

        if len(cells) < 4:
            continue

        doc_type = cells[3].get_text(strip=True)

        if doc_type.startswith("EX-10."):
            link = cells[2].find("a")

            if link:
                exhibit_docs.append(
                    {
                        "exhibit_type": doc_type,
                        "document_name": link.get_text(strip=True),
                        "document_url": urljoin("https://www.sec.gov", link.get("href")),
                    }
                )
        else: # the doc type on the exhibit did not start with EX-10
            print(doc_type)

    return exhibit_docs


def main():
    # access the issuer filing pages
    # grab the exhibits
    client = EdgarClient("edgar-amendments ericwquang@gmail.com")

    all_results = []

    for issuer in issuers:
        name = issuer["name"]
        cik = issuer["cik"]


        try:
            candidate_filings = find_candidate_filings(client, cik)
        except httpx.HTTPStatusError as e:
            print("failed issuer:", name, e)
            continue
        print(f"retrieved {len(candidate_filings)} filings from {name}.")

        results = []
        for filing in candidate_filings:
            exhibits = extract_exhibits_debug(client, filing)
            time.sleep(0.2)

            print(
                filing["filing_index_url"],
                "EX-10 count:",
                len(exhibits),
            )

            for exhibit in exhibits:
                document_url = exhibit["document_url"]

                text = fetch_document(client, document_url)

                exhibit["text"] = text
                time.sleep(0.2)
            results.append(
                        {
                            "issuer_name": name,
                            "cik": cik,
                            **filing,
                            "exhibits": exhibits,
                        }
                    )
        print(f"Now printing results for: {name} (cik:{cik}")
        print("candidate filings:", len(candidate_filings))
        print("total exhibits:", sum(len(f["exhibits"]) for f in results))
        print("\n")

        all_results.extend(results)

    print("\n=== MULTI-ISSUER SUMMARY ===")
    print("total filings:", len(all_results))
    print(
    "total exhibits:",
    sum(len(filing["exhibits"]) for filing in all_results),
    )

    for issuer in issuers:
        name = issuer["name"]

        issuer_filings = [
        filing for filing in all_results
        if filing["issuer_name"] == name
        ]

        issuer_exhibits = sum(
        len(filing["exhibits"])
        for filing in issuer_filings
        )

        print(
        f"{name}: "
        f"{len(issuer_filings)} filings, "
        f"{issuer_exhibits} exhibits"
        )

    ROOT = Path(__file__).resolve().parents[1]
    
    OUTPUT_PATH = ROOT / "data"  / "multi_issuer_exhibits.json"

    save_results(all_results, OUTPUT_PATH)
    print(f"saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()


# MULTI-ISSUER SPIKE
#
# Goal:
# Prove that the EDGAR retrieval path that worked for Boeing also works
# across several unrelated public companies.
#
# Test issuers:
# - Ford: 37996
# - AT&T: 732717
# - Delta: 27904
#
# For each issuer:
# 1. Fetch recent submissions by CIK.
# 2. Find recent 8-K filings.
# 3. Build each filing's SEC index URL.
# 4. Parse the filing index structurally for EX-10.x exhibits.
# 5. Resolve exhibit URLs.
# 6. Fetch exhibit HTML and extract readable text.
# 7. Save issuer-specific results to JSON.
#
# Questions to answer:
# - Does the same filing/index structure work across issuers?
# - Do EX-10 exhibits appear under different numbering patterns?
# - Does any Boeing-specific assumption break?
# - Are there SEC parsing/text-extraction failure modes we have not seen yet?
#
# Important:
# Do not add history support, LLM classification, databases, or FastAPI here.
# This spike is only testing whether recent-filing retrieval generalizes.
#
# Success criterion:
# Retrieve readable EX-10 exhibit text for at least 2-3 different issuers
# using essentially the same pipeline.
#
# After success:
# Refactor the repeated retrieval logic out of the spike scripts into
# reusable functions/modules.