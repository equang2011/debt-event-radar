from bs4 import BeautifulSoup
from pathlib import Path

from app.sec.client import EdgarClient


ROOT = Path(__file__).resolve().parents[1]

data = ROOT / "data" 

url = "https://www.sec.gov/Archives/edgar/data/12927/000001292725000064/a202508aug258kex101.htm"



def fetch_document(client, doc_url):
    html = client.get_text(doc_url)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text("\n", strip=True)


def chunk_text(text: str, size: int) -> list:
    pass



def main():
    # get the file
    client = EdgarClient("edgar-amendments ericwquang@gmail.com")

    text = fetch_document(client, url)

    result = []
    idx = 0
    n = len(text)

    while idx < n:

        right_bound = min(n, idx+ 3250)

        chunk = text[idx: right_bound]
        result.append(chunk)
        idx += 3000


    print(len(result))
    print(result[2])


if __name__ == '__main__':
    main()



"""
Chunk
├── chunk_id
├── text
├── start/end position
├── section/title if known
├── tags / concepts
└── embedding





"""