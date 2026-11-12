import time

from app.sec.client import EdgarClient


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

    shown = 0
    for i in range(len(recent["form"])):
        if recent["form"][i] != "8-K":
            continue
        accession = recent["accessionNumber"][i]
        filing_date = recent["filingDate"][i]
        acceptance_date_time = recent["acceptanceDateTime"][i]

        print(accession)
        print(filing_date)
        print(acceptance_date_time)

        accession_without_dashes = accession.replace("-", "")

        url = (
            "https://www.sec.gov/Archives/edgar/data/12927/"
            + accession_without_dashes
            + "/"
            + accession
            + "-index-headers.html"
        )

        text = client.get_text(url)
        for line in text.splitlines():
            if "ACCEPTANCE-DATETIME" in line:
                print(line)
        time.sleep(0.2)
        shown += 1
        if shown == 3:
            break


if __name__ == "__main__":
    main()
