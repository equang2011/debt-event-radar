import time
from bs4 import BeautifulSoup

from app.sec.client import EdgarClient



client = EdgarClient("edgar-amendments ericwquang@gmail.com")

cik = "12927"
data = client.get_submissions("12927")

print(type(data))
print(data.keys())

recent = data["filings"]["recent"]

print(len(recent["filingDate"]))

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

        if "EX-10.1" in html:
            candidate_filings.append(
            {
                "filing_date": recent["filingDate"][i],
                "accession": accession,
                "filing_index_url": filing_index_url,
            }
            )
            print("found one")
        if len(candidate_filings) >= 12:
            break
        time.sleep(0.2)
        
        
print(candidate_filings[:3])

filing = candidate_filings[-2]

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
                    "filing_date": filing["filing_date"],
                    "accession": filing["accession"],
                    "exhibit_type": doc_type,
                    "document_name": link.get_text(strip=True),
                    "document_href": link.get("href"),
                }
            )
        
        
print(exhibit_docs[:5])
document_url = "https://www.sec.gov" + exhibit_docs[0]["document_href"]

document_html = client.get_text(document_url)

document_soup = BeautifulSoup(document_html, "html.parser")

text = document_soup.get_text("\n", strip=True)

print(text[:3000])

# Slice 1 checkpoint:
# We can now go from Boeing's CIK -> 8-K -> EX-10 exhibit -> readable contract text.
# Next: inspect text quality and determine minimal HTML-cleaning rules before
# generalizing retrieval across multiple filings.