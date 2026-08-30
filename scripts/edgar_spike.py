import json
import time

from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin

from app.sec.client import EdgarClient


def find_candidate_filings(client, cik, limit=250):
    data = client.get_submissions(cik)

    recent = data["filings"]["recent"]

    candidate_filings = []
    for i in range(len(recent["form"])):
        if recent["form"][i] == "8-K":

            accession = recent["accessionNumber"][i]
            accession_no_dashes = accession.replace("-", "")

            filing_index_url = (
                f"https://www.sec.gov/Archives/edgar/data/"
                f"{cik}/{accession_no_dashes}/"
                f"{accession}-index.html"
            )

            html = client.get_text(filing_index_url)

            if "EX-10.1" in html or "EX-10.2" in html:
                candidate_filings.append(
                {
                    "filing_date": recent["filingDate"][i],
                    "accession": accession,
                    "filing_index_url": filing_index_url,
                }
                )
                print("found one")
            if len(candidate_filings) >= limit:
                break
            time.sleep(0.2)
    return candidate_filings
        
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

def fetch_document(client, doc_url):
    html = client.get_text(doc_url)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text("\n", strip=True)

def save_results(results, path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


def main():
    client = EdgarClient("edgar-amendments ericwquang@gmail.com")
    cik = "12927"

    candidate_filings = find_candidate_filings(client, cik)

    results = []
    for filing in candidate_filings:
        exhibits = extract_exhibits(client, filing)
        time.sleep(0.2)

        for exhibit in exhibits:
            document_url = exhibit["document_url"]

            text = fetch_document(client, document_url)

            exhibit["text"] = text
            time.sleep(0.2)

        results.append(
            {
                **filing,
                "exhibits": exhibits,
            }
        )
    print("candidate filings:", len(candidate_filings))
    print("total exhibits:", sum(len(f["exhibits"]) for f in results))

    ROOT = Path(__file__).resolve().parents[1]

    OUTPUT_PATH = ROOT / "data"  / "boeing_exhibits.json"

    save_results(results, OUTPUT_PATH)
    print(f"saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()

# Slice 1 checkpoint:
# We can now go from Boeing's CIK -> 8-K -> EX-10 exhibit -> readable contract text.
# Next: inspect text quality and determine minimal HTML-cleaning rules before
# generalizing retrieval across multiple filings.