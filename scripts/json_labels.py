import json
from pathlib import Path



ROOT = Path(__file__).resolve().parents[1]

file_path = ROOT/ "data" / "multi_issuer_exhibits.json"
false_output_path = ROOT/ "data" / "false_exhibits.json"
true_output_path = ROOT/ "data" / "true_exhibits.json"

print(file_path)
print(file_path.exists())

magic_words = [
    "borrower",
    "lender",
    "administrative agent",
    "borrowing",
    "loan",
    "commitment",
    "maturity",
    "default",
    "obligations",
]


cnt_true = 0
cnt_false = 0
arr_true = []
arr_false = []

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for obj in data:

    cnt = 0
    for exhibit in obj["exhibits"]:

        text = exhibit["text"]
        counts = {term: text.lower().count(term) for term in magic_words}
        total = sum(counts.values())

        exhibit["text"] = exhibit["text"][:3200]

        if total >= 60:
            exhibit["is_debt_doc"] = True
            arr_true.append(exhibit)
            cnt_true +=1

        else:
            exhibit["is_debt_doc"] = False
            arr_false.append(exhibit)
            cnt_false +=1

output_path = false_output_path

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(arr_false, f, indent=2)
    print(f"wrote false file to: {output_path}")

output_path = true_output_path

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(arr_true, f, indent=2)
    print(f"wrote true file to: {output_path}")


print(cnt_true)
print(cnt_false)
            






