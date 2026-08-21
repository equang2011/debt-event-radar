import httpx

class EdgarClient:
    BASE_URL = "https://data.sec.gov"

    def __init__(self, user_agent: str):
        self.client = httpx.Client(
            headers={"User-Agent": user_agent},
            timeout=15.0,
        )

    def get_submissions(self, cik: str) -> dict:
        cik = cik.strip().zfill(10)

        url = self.BASE_URL + "/submissions/CIK" + cik + ".json"

        response = self.client.get(url)

        response.raise_for_status()
        return response.json()

    def get_text(self, url: str) -> str:
        response = self.client.get(url)
        response.raise_for_status()
        return response.text
