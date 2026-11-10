




import json
import time

from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin

from app.sec.client import EdgarClient
from scripts.edgar_spike import find_candidate_filings

def find_candidate_filings(client, cik, limit=18):
    """access the filings attached to 8K; returns a list of filing index url"""
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



def main():
    client = EdgarClient("edgar-amendments ericwquang@gmail.com")
    data = client.get_submissions("12927")
    recent = data["filings"]["recent"]

    print(type(recent))          # dict
    print(list(recent.keys()))   # the parallel lists
    print(recent["acceptanceDateTime"][:3])
    print(recent["filingDate"][:3])


if __name__ == "__main__":
    main()