
import httpx
import json
import time

from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin

from app.sec.client import EdgarClient
from scripts.edgar_spike import save_results, fetch_document
from scripts.ml_experiment.issuers import issuers, UNSEEN_TEST_ISSUERS


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR  = ROOT / "data" / "debt_classifier"

OUTPUT_PATH = DATA_DIR / "candidate_exhibits_v2.json"

def find_candidate_filings(client, cik, limit=75):
    """access the filings attached to 8K; returns a list of filing index url"""
    data = client.get_submissions(cik)
    
    recent = data["filings"]["recent"]
    
    filings = []
    for i in range(len(recent["form"])):
        if recent["form"][i] == "8-K":

            accession = recent["accessionNumber"][i]
            accession_no_dashes = accession.replace("-", "")

            filing_index_url = (
                f"https://www.sec.gov/Archives/edgar/data/"
                f"{cik}/{accession_no_dashes}/"
                f"{accession}-index.html"
            )

            filings.append({
                "filing_date": recent["filingDate"][i],
                "accession": accession,
                "filing_index_url": filing_index_url,
            })

            if len(filings) >= limit:
                break
    return filings





def extract_exhibits(client, filing):
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
    
    return exhibit_docs


def main():
    client = EdgarClient("edgar-amendments ericwquang@gmail.com")
    
    results = []

    for issuer in issuers:
        name = issuer["name"]
        cik = issuer["cik"]

        try:
            candidate_filings = find_candidate_filings(client, cik)
        except httpx.HTTPStatusError as e:
            print("failed issuer:", name, e)
            continue
        print(f"retrieved {len(candidate_filings)} filings from {name}.")

        for filing in candidate_filings:
            try:
                exhibits = extract_exhibits(client, filing)
            except httpx.ReadTimeout as e:
                print("timed out filing:", filing["filing_index_url"])
                continue

            if not exhibits:
                continue

            for exhibit in exhibits:
                try:
                    text = fetch_document(client, exhibit["document_url"])
                except httpx.ReadTimeout:
                    print("timed out exhibit:", exhibit["document_url"])
                    continue
                exhibit["text"] = text

                time.sleep(0.2)

            results.append({
                    "issuer_name": name,
                    "cik": cik,
                    **filing,
                    "exhibits": exhibits,
                })
    print("candidate filings with EX-10s:", len(results))
    print(
        "total exhibits:",
        sum(len(f["exhibits"]) for f in results),
    )

    save_results(results, OUTPUT_PATH)
    print(f"saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()

"""
issuer list
   ↓
recent 8-Ks
   ↓
parse EVERY filing index structurally
   ↓
collect every EX-10.*
   ↓
fetch text
   ↓
save larger raw corpus
"""