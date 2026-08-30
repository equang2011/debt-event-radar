import json

from app.sec.client import EdgarClient





def main():

    client = EdgarClient("edgar-amendments ericwquang@gmail.com")

    data = client.get_submissions("12927")

    print(data.keys())
    print(data["filings"].keys())

    history_files = data["filings"]["files"]

    first_history_file = history_files[0]

    history = client.get_submission_history(
        first_history_file["name"]
    )

    print(history.keys())

    print(type(history["form"]))
    print(history["form"][:99])
    print(len(history["form"]))

if __name__ == "__main__":
    main()